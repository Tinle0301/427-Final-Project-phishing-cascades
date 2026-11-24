
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
BETAS = [
    0.001, 0.002, 0.003, 0.005, 0.007,
    0.01, 0.015, 0.02, 0.03, 0.05, 0.10, 0.20
]
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

    available = sorted(nodes - immune, key=str)

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
            f"beta={beta:.3f} | "
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
    plt.legend(ncol=2, fontsize=9)
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


# Compare the average number of users reached
def plot_mean_reached(sir_results, sis_results):

    betas = list(sir_results.keys())

    sir_means = [
        sir_results[beta]["mean_size"]
        for beta in betas
    ]

    sis_means = [
        sis_results[beta]["mean_size"]
        for beta in betas
    ]

    plt.figure(figsize=(10, 6))

    plt.plot(
        betas,
        sir_means,
        marker="o",
        label="SIR",
        linewidth=2
    )

    plt.plot(
        betas,
        sis_means,
        marker="s",
        label="SIS",
        linewidth=2
    )

    plt.xlabel("Transmission Probability (Beta)")
    plt.ylabel("Mean Unique Users Reached")
    plt.title("SIR vs SIS: Mean Users Reached")
    plt.xscale("log")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()

    plt.savefig(
        OUTPUT / "mean_reached_comparison.png",
        dpi=300
    )
    plt.close()

    print("Saved:", OUTPUT / "mean_reached_comparison.png")


# Plot large outbreak probability for different beta values
def plot_outbreak_probability(sir_results, sis_results):

    betas = list(sir_results.keys())

    sir_probs = [
        sir_results[beta]["large_outbreak_probability"]
        for beta in betas
    ]

    sis_probs = [
        sis_results[beta]["large_outbreak_probability"]
        for beta in betas
    ]

    plt.figure(figsize=(10, 6))

    plt.plot(
        betas,
        sir_probs,
        marker="o",
        label="SIR",
        linewidth=2
    )

    plt.plot(
        betas,
        sis_probs,
        marker="s",
        linestyle="--",
        label="SIS",
        linewidth=2
    )

    plt.axhline(
        y=0.5,
        color="gray",
        linestyle=":",
        label="50% outbreak probability"
    )

    plt.xlabel("Transmission Probability (Beta)")
    plt.ylabel("Large Outbreak Probability")
    plt.title("Large Outbreak Probability vs Beta")
    plt.xscale("log")
    plt.ylim(0, 1.05)
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()

    plt.savefig(
        OUTPUT / "outbreak_probability.png",
        dpi=300
    )
    plt.close()

    print("Saved:", OUTPUT / "outbreak_probability.png")

# Find an empirical epidemic threshold
def find_threshold(results, model):

    # At least 50% of runs reach 10% of network users
    previous_beta = None

    for beta, data in results.items():

        if data["large_outbreak_probability"] >= 0.5:

            if previous_beta is None:
                print(
                    f"{model} threshold is at or below "
                    f"beta={beta:.3f}"
                )
            else:
                print(
                    f"{model} threshold is between "
                    f"beta={previous_beta:.3f} "
                    f"and beta={beta:.3f}"
                )

            return beta

        previous_beta = beta

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

    # Generate figures
    plot_curves(sir_results, "SIR")
    plot_curves(sis_results, "SIS")

    plot_comparison(
        sir_results,
        sis_results,
        beta=0.10
    )

    plot_mean_reached(sir_results, sis_results)
    plot_outbreak_probability(sir_results, sis_results)

    # Estimate thresholds
    find_threshold(sir_results, "SIR")
    find_threshold(sis_results, "SIS")

    print("\nAll simulations completed!")


if __name__ == "__main__":
    main()
