"""Structure of the email-Eu-core network and the small-world comparison.

Produces analysis/figures/degree_distribution.png and prints the numbers.
Run from the repo root:  python src/structure.py [path/to/email-eu-core.gml]
"""
import os
import sys
import textwrap
from collections import Counter

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx

SEED = 42
N_RANDOM = 5  # random graphs averaged for the baseline
FIG_PATH = os.path.join("analysis", "figures", "degree_distribution.png")

# Default search paths for the graph file (first that exists wins).
CANDIDATES = [
    os.path.join("data", "email-eu-core.gml"),  # written by src/build_graph.py
    "email-eu-core.gml",
    "/mnt/user-data/uploads/email-eu-core.gml",
]


def load_graph(path=None):
    if path is None:
        path = next((p for p in CANDIDATES if os.path.exists(p)), None)
        if path is None:
            sys.exit("Graph file not found; pass its path as the first argument.")
    # build_graph.py writes this file (data/email-eu-core.gml) with person
    # ids as node labels, already without self-loops or duplicates.
    G = nx.DiGraph(nx.read_gml(path, label="label"))
    G.remove_edges_from(list(nx.selfloop_edges(G)))  # no-op safety net
    return G


def path_and_clustering(G):
    """Avg shortest path on largest SCC; avg clustering of the undirected graph."""
    scc = max(nx.strongly_connected_components(G), key=len)
    L = nx.average_shortest_path_length(G.subgraph(scc))
    C = nx.average_clustering(G.to_undirected())
    return L, C


def degree_plot(G, ax, degrees, title):
    counts = Counter(d for d in degrees if d > 0)  # zeros can't go on log axes
    xs = sorted(counts)
    ax.loglog(xs, [counts[x] for x in xs], "o", markersize=4, alpha=0.8)
    ax.set_xlabel("Degree (log scale)")
    ax.set_ylabel("Number of people (log scale)")
    ax.set_title(title)
    return len(degrees) - sum(counts.values())  # people with degree 0, not drawn


def main():
    G = load_graph(sys.argv[1] if len(sys.argv) > 1 else None)
    n, m = G.number_of_nodes(), G.number_of_edges()
    print(f"nodes {n}, directed edges {m}")

    sccs = list(nx.strongly_connected_components(G))
    wccs = list(nx.weakly_connected_components(G))
    print(f"SCCs {len(sccs)} (largest {max(map(len, sccs))})")
    print(f"WCCs {len(wccs)} (largest {max(map(len, wccs))})")

    L, C = path_and_clustering(G)
    print(f"real:   path length {L:.3f}, clustering {C:.3f}")

    Ls, Cs = [], []
    for i in range(N_RANDOM):
        R = nx.gnm_random_graph(n, m, seed=SEED + i, directed=True)
        l, c = path_and_clustering(R)
        Ls.append(l)
        Cs.append(c)
    Lr, Cr = sum(Ls) / N_RANDOM, sum(Cs) / N_RANDOM
    print(f"random: path length {Lr:.3f}, clustering {Cr:.3f} (mean of {N_RANDOM} seeds)")

    sentence = (
        "In- and out-degree are heavy-tailed; the network has "
        f"{len(sccs)} strongly connected components (largest {max(map(len, sccs))} people) and "
        f"{len(wccs)} weakly connected components (largest {max(map(len, wccs))}); "
        f"path length is {L:.2f} vs {Lr:.2f} random, clustering is {C:.3f} vs {Cr:.3f}, "
        "a small-world pattern."
    )

    fig, axes = plt.subplots(1, 2, figsize=(11, 5.6))
    z_in = degree_plot(G, axes[0], [d for _, d in G.in_degree()], "In-degree")
    z_out = degree_plot(G, axes[1], [d for _, d in G.out_degree()], "Out-degree")
    fig.suptitle("Network Structure: In- and Out-Degree Distributions")
    fig.tight_layout(rect=(0, 0.17, 1, 1))
    fig.text(0.5, 0.095, "\n".join(textwrap.wrap(sentence, 105)),
             ha="center", va="center", fontsize=10, fontweight="bold")
    fig.text(0.5, 0.012,
             f"People with degree 0 are not shown on log axes "
             f"(in-degree: {z_in}, out-degree: {z_out}). "
             f"Random baseline: mean of {N_RANDOM} seeded gnm_random_graph(n, m).",
             ha="center", fontsize=8)
    os.makedirs(os.path.dirname(FIG_PATH), exist_ok=True)
    plt.savefig(FIG_PATH, dpi=150)
    plt.close(fig)

    print("\n" + sentence)
    with open(os.path.join("analysis", "structure_result.txt"), "w") as f:
        f.write(sentence + "\n")


if __name__ == "__main__":
    main()
