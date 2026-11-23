
from pathlib import Path
import random

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


# Project folders
ROOT = Path(__file__).resolve().parent.parent
GRAPH_FILE = ROOT / "data" / "email-eu-core.gml"
OUTPUT = ROOT / "analysis" / "figures"


# Simulation settings
BETAS = [0.01, 0.03, 0.05, 0.10, 0.20]
TAU = 5
STEPS = 40
RUNS = 100
SEED = 42


# Simulate one SIR or SIS outbreak
def simulate(G, model="SIR", beta=0.1, tau=5,
             steps=40, seed=42, initial_infected=None,
             immune_nodes=None):

    if model not in ("SIR", "SIS"):
        raise ValueError("Model must be SIR or SIS")

    if not 0 <= beta <= 1 or tau < 1:
        raise ValueError("Invalid beta or tau")

    rng = random.Random(seed)

    # Protected nodes cannot become infected
    immune = set(immune_nodes or [])
    nodes = set(G.nodes())

    if not immune.issubset(nodes):
        raise ValueError("Unknown immune nodes")

    available = list(nodes - immune)

    if not available:
        raise ValueError("No available nodes")

    # Start with one infected person
    if initial_infected is None:
        initial_infected = [rng.choice(available)]

    infected = set(initial_infected)

    if not infected or not infected.issubset(nodes - immune):
        raise ValueError("Invalid initial infected nodes")

    recovered = set()
    ever_infected = set(infected)

    # Infection duration for each infected person
    timers = {node: 0 for node in infected}

    S = []
    I = []
    R = []

    for step in range(steps + 1):

        susceptible_count = (
            len(G) - len(immune) - len(infected) - len(recovered)
        )

        S.append(susceptible_count)
        I.append(len(infected))
        R.append(len(recovered))

        if step == steps or not infected:
            break

        new_infected = set()

        # Infection spreads along directed outgoing edges
        for node in sorted(infected, key=str):
            for neighbor in G.successors(node):

                if (neighbor not in infected
                        and neighbor not in recovered
                        and neighbor not in immune
                        and neighbor not in new_infected):

                    if rng.random() < beta:
                        new_infected.add(neighbor)

        # Update infection timers
        new_recovered = set()

        for node in infected:
            timers[node] += 1

            if timers[node] >= tau:
                new_recovered.add(node)

        # Remove people who finish their infection
        infected.difference_update(new_recovered)

        if model == "SIR":
            # Recovered users cannot become infected again
            recovered.update(new_recovered)

        # SIS: recovered users return to susceptible
        # They may be infected again on the next time step

        for node in new_infected:
            timers[node] = 0

        for node in new_recovered:
            timers.pop(node, None)

        infected.update(new_infected)
        ever_infected.update(new_infected)

    # Fill remaining time steps
    while len(I) < steps + 1:
        S.append(S[-1])
        I.append(0)
        R.append(R[-1])

    return {
        "S": S,
        "I": I,
        "R": R,
        "ever_infected": len(ever_infected)
    }


# Repeat experiments for each beta
def run_experiments(G, model):

    print(f"\nRunning {model} simulation...")

    results = {}

    for beta in BETAS:

        infected_curves = []
        outbreak_sizes = []

        for run in range(RUNS):

            result = simulate(
                G,
                model=model,
                beta=beta,
                tau=TAU,
                steps=STEPS,
                seed=SEED + run
            )

            infected_curves.append(result["I"])
            outbreak_sizes.append(result["ever_infected"])

        results[beta] = {
            "curve": np.mean(infected_curves, axis=0),
            "mean_size": np.mean(outbreak_sizes),
            "large_outbreak_probability": np.mean(
                np.array(outbreak_sizes) >= 0.10 * len(G)
            )
        }

        print(
            f"beta={beta:.2f} | "
            f"mean reached={results[beta]['mean_size']:.1f} | "
            f"large outbreak probability="
            f"{results[beta]['large_outbreak_probability']:.2f}"
        )

    return results


# Plot average infected curves
def plot_curves(results, model):

    plt.figure(figsize=(10, 6))

    for beta, data in results.items():
        plt.plot(
            range(STEPS + 1),
            data["curve"],
            label=f"beta = {beta}",
            linewidth=2
        )

    plt.xlabel("Time Step")
    plt.ylabel("Average Active Infected Users")
    plt.title(f"{model} Phishing Spread Simulation")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()

    filename = (
        "sir_curves.png" if model == "SIR"
        else "sis_curves.png"
    )

    plt.savefig(OUTPUT / filename, dpi=300)
    plt.close()

    print("Saved:", OUTPUT / filename)


# Compare SIR and SIS at the same beta
def plot_comparison(sir_results, sis_results, beta=0.10):

    plt.figure(figsize=(10, 6))

    plt.plot(
        range(STEPS + 1),
        sir_results[beta]["curve"],
        label="SIR",
        linewidth=2
    )

    plt.plot(
        range(STEPS + 1),
        sis_results[beta]["curve"],
        label="SIS",
        linewidth=2
    )

    plt.xlabel("Time Step")
    plt.ylabel("Average Active Infected Users")
    plt.title(f"SIR vs SIS (beta = {beta}, tau = {TAU})")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()

    plt.savefig(OUTPUT / "sir_vs_sis.png", dpi=300)
    plt.close()

    print("Saved:", OUTPUT / "sir_vs_sis.png")


# Find an empirical epidemic threshold
def find_threshold(results, model):

    # Operational definition:
    # At least 50% of runs reach 10% of network users

    for beta, data in results.items():

        if data["large_outbreak_probability"] >= 0.5:
            print(
                f"{model} empirical large-outbreak threshold "
                f"(first tested beta): {beta}"
            )
            return beta

    print(f"{model}: threshold not found in tested betas")
    return None


def main():

    OUTPUT.mkdir(parents=True, exist_ok=True)

    if not GRAPH_FILE.exists():
        print("Graph file not found:", GRAPH_FILE)
        print("Run: python3 src/build_graph.py")
        return

    G = nx.read_gml(GRAPH_FILE)

    # Keep outgoing email direction
    if not G.is_directed():
        raise ValueError("Expected a directed email graph")

    print("Network loaded")
    print("Nodes:", G.number_of_nodes())
    print("Edges:", G.number_of_edges())

    # Run both models
    sir_results = run_experiments(G, "SIR")
    sis_results = run_experiments(G, "SIS")

    # Generate three figures
    plot_curves(sir_results, "SIR")
    plot_curves(sis_results, "SIS")

    plot_comparison(
        sir_results,
        sis_results,
        beta=0.10
    )

    # Estimate thresholds
    find_threshold(sir_results, "SIR")
    find_threshold(sis_results, "SIS")

    print("\nAll simulations completed!")


if __name__ == "__main__":
    main()
