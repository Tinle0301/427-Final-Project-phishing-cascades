"""Turn the raw SNAP files into a GML the rest of the project can load.

    python3 src/build_graph.py

Reads   data/raw/email-Eu-core.txt
        data/raw/email-Eu-core-department-labels.txt
Writes  data/email-eu-core.gml      directed, every node carries its department
        data/summary.txt            the numbers we quote in the report

Run this once. Everyone else starts from the .gml.

The two SNAP pages for this dataset disagree with each other on the edge
count, so this script reports what is actually in the file: how many lines
it read, how many of those were duplicate pairs, how many were self-loops,
and what is left. Those are the numbers that go in the report.
"""

import os
import sys
from collections import Counter

import networkx as nx

RAW = os.path.join("data", "raw")
EDGES = os.path.join(RAW, "email-Eu-core.txt")
LABELS = os.path.join(RAW, "email-Eu-core-department-labels.txt")
OUT = os.path.join("data", "email-eu-core.gml")
SUMMARY = os.path.join("data", "summary.txt")


def need(path):
    if not os.path.isfile(path):
        sys.exit("missing %s - see data/README.md for the download commands" % path)


def read_pairs(path):
    # SNAP format: two whitespace-separated fields per line, '#' lines are comments
    pairs = []
    with open(path) as f:
        for line in f:
            if line.startswith("#"):
                continue
            parts = line.split()
            if len(parts) == 2:
                pairs.append((parts[0], parts[1]))
    return pairs


def main():
    need(EDGES)
    need(LABELS)

    raw_edges = read_pairs(EDGES)
    depts = {v: int(d) for v, d in read_pairs(LABELS)}

    # count what we are about to drop, before we drop it
    seen = Counter(raw_edges)
    duplicates = sum(n - 1 for n in seen.values() if n > 1)
    self_loops = sum(1 for u, v in seen if u == v)

    G = nx.DiGraph()
    # every labelled person is a node, even one who never sent or received mail
    G.add_nodes_from(depts)
    for u, v in seen:
        if u != v:
            G.add_edge(u, v)

    missing = [v for v in G if v not in depts]
    for v in G:
        G.nodes[v]["department"] = depts.get(v, -1)

    nx.write_gml(G, OUT)

    scc = sorted((len(c) for c in nx.strongly_connected_components(G)), reverse=True)
    wcc = sorted((len(c) for c in nx.weakly_connected_components(G)), reverse=True)

    sizes = Counter(G.nodes[v]["department"] for v in G)
    biggest = sizes.most_common(1)[0]
    smallest = sizes.most_common()[-1]
    isolated = sum(1 for v in G if G.degree(v) == 0)

    lines = [
        "email-Eu-core, as loaded by src/build_graph.py",
        "",
        "-- what the file contained --",
        "lines read from the edge file   %d" % len(raw_edges),
        "duplicate pairs dropped         %d" % duplicates,
        "self-loops dropped              %d" % self_loops,
        "",
        "-- the graph we analyse --",
        "nodes                           %d" % G.number_of_nodes(),
        "directed edges                  %d" % G.number_of_edges(),
        "nodes with no edges             %d" % isolated,
        "nodes with no department label  %d" % len(missing),
        "departments                     %d" % len(sizes),
        "largest department              %d people (dept %s)" % (biggest[1], biggest[0]),
        "smallest department             %d people (dept %s)" % (smallest[1], smallest[0]),
        "",
        "strongly connected components   %d  (largest %d)" % (len(scc), scc[0]),
        "weakly connected components     %d  (largest %d)" % (len(wcc), wcc[0]),
        "",
        "mean out-degree                 %.3f" % (G.number_of_edges() / G.number_of_nodes()),
        "reciprocity                     %.3f" % nx.reciprocity(G),
    ]
    with open(SUMMARY, "w") as f:
        f.write("\n".join(lines) + "\n")

    print("\n".join(lines))
    print("\nwrote %s and %s" % (OUT, SUMMARY))


if __name__ == "__main__":
    main()
