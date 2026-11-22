# Sean Roser

from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
from scipy.stats import spearmanr


ROOT = Path(__file__).resolve().parents[1]
GRAPH_PATH = ROOT / "data" / "email-eu-core.gml"
ANALYSIS_DIR = ROOT / "analysis"
FIGURES_DIR = ANALYSIS_DIR / "figures"
CSV_PATH = ANALYSIS_DIR / "top_spreaders.csv"
FIGURE_PATH = FIGURES_DIR / "centrality_overlap.png"

METRICS = ("in_degree", "out_degree", "betweenness", "pagerank")


def rank_nodes(scores):
    # Return node IDs sorted by descending score, with stable tie-breaking.
    return sorted(scores, key=lambda node: (-scores[node], str(node)))


def main():
    if not GRAPH_PATH.is_file():
        raise FileNotFoundError(
            f"Could not find {GRAPH_PATH}. Build the graph first with "
            "'python3 src/build_graph.py'."
        )

    G = nx.read_gml(GRAPH_PATH)
    if not G.is_directed():
        raise ValueError("Expected a directed graph in data/email-eu-core.gml.")

    print(
        f"Loaded graph: {G.number_of_nodes():,} nodes, "
        f"{G.number_of_edges():,} directed edges"
    )

    scores = {
        "in_degree": dict(G.in_degree()),
        "out_degree": dict(G.out_degree()),
        "betweenness": nx.betweenness_centrality(G, normalized=True),
        "pagerank": nx.pagerank(G),
    }

    rankings = {metric: rank_nodes(scores[metric]) for metric in METRICS}
    top_nodes = {metric: rankings[metric][:20] for metric in METRICS}

    # One row per rank; each measure gets its own node, score, and department.
    rows = []
    for rank in range(20):
        row = {}
        for metric in METRICS:
            node = top_nodes[metric][rank]
            row[f"{metric}_rank"] = rank + 1
            row[f"{metric}_node"] = node
            row[f"{metric}_score"] = scores[metric][node]
            row[f"{metric}_department"] = G.nodes[node].get("department", "")
        rows.append(row)

    ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(CSV_PATH, index=False)

    # Pairwise Spearman correlations use scores for all 1,005 nodes.
    print("\nPairwise Spearman correlations (all nodes):")
    correlations = np.eye(len(METRICS), dtype=float)
    for i, metric_a in enumerate(METRICS):
        for j in range(i + 1, len(METRICS)):
            metric_b = METRICS[j]
            result = spearmanr(
                [scores[metric_a][node] for node in G.nodes()],
                [scores[metric_b][node] for node in G.nodes()],
            )
            correlations[i, j] = correlations[j, i] = result.statistic
            print(f"  {metric_a:12s} vs {metric_b:12s}: "
                  f"rho = {result.statistic:.4f} (p = {result.pvalue:.3g})")

    # Pairwise counts of shared node IDs among the four top-20 lists.
    overlap = np.zeros((len(METRICS), len(METRICS)), dtype=int)
    print("\nShared nodes between top-20 lists:")
    for i, metric_a in enumerate(METRICS):
        for j, metric_b in enumerate(METRICS):
            overlap[i, j] = len(set(top_nodes[metric_a]) & set(top_nodes[metric_b]))
        for j in range(i + 1, len(METRICS)):
            print(f"  {metric_a:12s} vs {METRICS[j]:12s}: "
                  f"{overlap[i, j]:2d} shared nodes")

    # Heatmap: diagonal is 20; off-diagonal cells show shared top-20 nodes.
    fig, ax = plt.subplots(figsize=(8, 6))
    image = ax.imshow(overlap, cmap="Blues", vmin=0, vmax=20)
    ax.set_xticks(range(len(METRICS)), METRICS, rotation=25, ha="right")
    ax.set_yticks(range(len(METRICS)), METRICS)
    ax.set_title("Overlap Between Top-20 Centrality Rankings")
    ax.set_xlabel("Centrality measure")
    ax.set_ylabel("Centrality measure")

    for i in range(len(METRICS)):
        for j in range(len(METRICS)):
            value = overlap[i, j]
            ax.text(
                j, i, str(value), ha="center", va="center",
                color="white" if value >= 11 else "black",
                fontweight="bold",
            )

    colorbar = fig.colorbar(image, ax=ax)
    colorbar.set_label("Shared nodes (out of 20)")
    fig.tight_layout()
    fig.savefig(FIGURE_PATH, dpi=150, bbox_inches="tight")
    plt.close(fig)

    print(f"\nWrote {CSV_PATH.relative_to(ROOT)}")
    print(f"Wrote {FIGURE_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
