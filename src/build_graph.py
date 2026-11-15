"""Turn the raw SNAP files into a GML the rest of the project can load.

    python3 src/build_graph.py

Reads   data/raw/email-Eu-core.txt
        data/raw/email-Eu-core-department-labels.txt
Writes  data/email-eu-core.gml      directed, every node carries its department
        data/summary.txt            the numbers we quote in the report

Run this once. Everyone else starts from the .gml.
"""

import os
import sys

import networkx as nx

RAW = os.path.join("data", "raw")
EDGES = os.path.join(RAW, "email-Eu-core.txt")
LABELS = os.path.join(RAW, "email-Eu-core-department-labels.txt")
OUT = os.path.join("data", "email-eu-core.gml")
SUMMARY = os.path.join("data", "summary.txt")


def need(path):
    if not os.path.isfile(path):
        sys.exit("missing %s - see data/README.md for the download commands" % path)


def main():
    need(EDGES)
    need(LABELS)

    # SNAP format: one "sender recipient" pair per line, '#' lines are comments
    G = nx.DiGraph()
    with open(EDGES) as f:
        for line in f:
            if line.startswith("#"):
                continue
            parts = line.split()
            if len(parts) == 2:
                G.add_edge(parts[0], parts[1])

    # "node department", 42 departments numbered 0-41
    depts = {}
    with open(LABELS) as f:
        for line in f:
            if line.startswith("#"):
                continue
            parts = line.split()
            if len(parts) == 2:
                depts[parts[0]] = int(parts[1])

    missing = [v for v in G if v not in depts]
    for v in G:
        G.nodes[v]["department"] = depts.get(v, -1)

    loops = list(nx.selfloop_edges(G))
    G.remove_edges_from(loops)

    nx.write_gml(G, OUT)

    scc = sorted((len(c) for c in nx.strongly_connected_components(G)), reverse=True)
    wcc = sorted((len(c) for c in nx.weakly_connected_components(G)), reverse=True)
    lines = [
        "email-Eu-core, as loaded by src/build_graph.py",
        "",
        "nodes                    %d" % G.number_of_nodes(),
        "directed edges           %d" % G.number_of_edges(),
        "self-loops removed       %d" % len(loops),
        "nodes with no department %d" % len(missing),
        "departments              %d" % len(set(depts.values())),
        "",
        "strongly connected components %d  (largest %d)" % (len(scc), scc[0]),
        "weakly connected components   %d  (largest %d)" % (len(wcc), wcc[0]),
        "",
        "mean out-degree          %.3f" % (G.number_of_edges() / G.number_of_nodes()),
        "reciprocity              %.3f" % nx.reciprocity(G),
    ]
    with open(SUMMARY, "w") as f:
        f.write("\n".join(lines) + "\n")

    print("\n".join(lines))
    print("\nwrote %s and %s" % (OUT, SUMMARY))


if __name__ == "__main__":
    main()
