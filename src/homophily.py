"""Workstream C - homophily and departments.

Do people email inside their own department more than chance predicts?

    python3 src/homophily.py                 # 1,000 label shuffles, seed 427
    python3 src/homophily.py --shuffles 5000

Reads  data/email-eu-core.gml (built by src/build_graph.py)
Writes analysis/figures/homophily.png         observed vs chance, per department
       analysis/figures/homophily_mixing.png  department-to-department mixing matrix
       analysis/homophily_departments.csv     the per-department table
       analysis/homophily_summary.txt         the headline numbers

Chance model. Keep the graph fixed and shuffle the department labels across the
1,005 people, which keeps every department's size. Under that model the chance a
given edge u -> v (u != v) joins two people of the same department is

    sum_d n_d (n_d - 1) / (N (N - 1))

exactly, for every edge, so the analytic expectation and the mean of the
shuffles must agree - that agreement is the check that both are right.

A second, degree-aware baseline is also reported: sum_d a_d b_d / m^2, where a_d
and b_d are the total out- and in-degree of department d. It asks "if each
department kept its email volume but chose recipients at random", and it is the
baseline that the assortativity coefficient r is measured against.
"""

import argparse
import csv
import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import networkx as nx  # noqa: E402
import numpy as np  # noqa: E402

GML = os.path.join("data", "email-eu-core.gml")
FIG_DIR = os.path.join("analysis", "figures")
FIG = os.path.join(FIG_DIR, "homophily.png")
FIG_MIX = os.path.join(FIG_DIR, "homophily_mixing.png")
TABLE = os.path.join("analysis", "homophily_departments.csv")
SUMMARY = os.path.join("analysis", "homophily_summary.txt")

# colours (validated categorical slots 1 and 2, plus neutral ink and gray)
BLUE = "#2a78d6"
ORANGE = "#eb6834"
GRAY = "#9a9994"
INK = "#0b0b0b"
INK2 = "#52514e"
SURFACE = "#fcfcfb"

MIN_SIZE = 10  # departments smaller than this are listed but not ranked


def load(path):
    if not os.path.isfile(path):
        sys.exit("missing %s - run python3 src/build_graph.py first" % path)
    G = nx.read_gml(path)
    nodes = list(G)
    index = {v: i for i, v in enumerate(nodes)}
    dept = np.array([int(G.nodes[v]["department"]) for v in nodes])
    edges = np.array([(index[u], index[v]) for u, v in G.edges()], dtype=np.int64)
    return G, dept, edges


def within_fraction(dept, edges):
    return float(np.mean(dept[edges[:, 0]] == dept[edges[:, 1]]))


def assortativity(dept, edges, k):
    """Newman's r for a categorical attribute, from the k x k mixing matrix.

    Same quantity as nx.attribute_assortativity_coefficient, but vectorised so
    it can be run on every shuffle.
    """
    e = np.zeros((k, k))
    np.add.at(e, (dept[edges[:, 0]], dept[edges[:, 1]]), 1.0)
    e /= e.sum()
    a, b = e.sum(axis=1), e.sum(axis=0)
    ab = float(a @ b)
    return (float(np.trace(e)) - ab) / (1.0 - ab)


def department_table(dept, edges, n_nodes):
    k = int(dept.max()) + 1
    src, dst = dept[edges[:, 0]], dept[edges[:, 1]]
    mix = np.zeros((k, k), dtype=np.int64)
    np.add.at(mix, (src, dst), 1)

    rows = []
    for d in range(k):
        n = int(np.sum(dept == d))
        internal = int(mix[d, d])
        sent_out = int(mix[d].sum() - internal)  # d -> other departments
        recv_in = int(mix[:, d].sum() - internal)  # other departments -> d
        ends = 2 * internal + sent_out + recv_in
        partners = int(np.sum(((mix[d] + mix[:, d]) > 0) & (np.arange(k) != d)))
        observed = 2 * internal / ends if ends else float("nan")
        chance = (n - 1) / (n_nodes - 1)
        rows.append({
            "department": d,
            "size": n,
            "internal_edges": internal,
            "edges_sent_out": sent_out,
            "edges_received_in": recv_in,
            # share of this department's edge ends that stay inside it
            "within_share": observed,
            "within_share_chance": chance,
            "lift": observed / chance if chance > 0 and ends else float("nan"),
            # density of email inside the department, vs the whole graph
            "internal_density": internal / (n * (n - 1)) if n > 1 else float("nan"),
            "partner_departments": partners,
            "share_of_all_cross_edges": (sent_out + recv_in) / max(1, 2 * int(np.sum(src != dst))),
        })
    return rows, mix


def classify(rows):
    """Quartiles of within-share among departments big enough to rank.

    Partner count is not used: almost every department exchanges mail with 33-40
    of the other 41, so it does not separate them.
    """
    ranked = [r for r in rows if r["size"] >= MIN_SIZE]
    shares = np.array([r["within_share"] for r in ranked])
    hi_s, lo_s = np.percentile(shares, 75), np.percentile(shares, 25)
    for r in rows:
        if r["size"] < MIN_SIZE:
            r["role"] = "too small to rank"
        elif r["within_share"] >= hi_s:
            r["role"] = "insular"
        elif r["within_share"] <= lo_s:
            r["role"] = "bridge"
        else:
            r["role"] = "mixed"


def style(ax):
    ax.set_facecolor(SURFACE)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(GRAY)
    ax.tick_params(colors=INK2, labelsize=9)
    ax.grid(color="#e6e5e1", linewidth=0.6)
    ax.set_axisbelow(True)


def plot_main(obs, null, analytic, degree_exp, rows, path):
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(12, 4.8), facecolor=SURFACE,
                                 gridspec_kw={"width_ratios": [1, 1.25]})

    # (a) the headline: observed vs the two chance baselines
    labels = ["Observed", "Chance:\nshuffled labels", "Chance:\nsize + volume"]
    vals = [obs, null.mean(), degree_exp]
    colors = [BLUE, GRAY, GRAY]
    style(a1)
    a1.grid(axis="x", visible=False)
    bars = a1.bar(labels, [100 * v for v in vals], color=colors, width=0.55,
                  edgecolor=SURFACE, linewidth=2)
    lo, hi = np.percentile(null, [0.5, 99.5])
    a1.errorbar([1], [100 * null.mean()], yerr=[[100 * (null.mean() - lo)], [100 * (hi - null.mean())]],
                color=INK, capsize=4, linewidth=1)
    for b, v in zip(bars, vals):
        a1.text(b.get_x() + b.get_width() / 2, 100 * v + 1.2, "%.1f%%" % (100 * v),
                ha="center", va="bottom", color=INK, fontsize=11)
    a1.set_ylabel("Email links inside one department (%)", color=INK2, fontsize=10)
    a1.set_ylim(0, max(100 * obs * 1.2, 10))
    a1.set_title("(a) %.1fx more same-department links than chance" % (obs / analytic),
                 loc="left", color=INK, fontsize=11)
    a1.text(1, 100 * hi + 3.5, "1,000 shuffles,\n99%% range\n(analytic %.1f%%)" % (100 * analytic),
            ha="center", va="bottom", color=INK2, fontsize=8)

    # (b) per department: observed within-share vs what chance gives that size
    style(a2)
    groups = (
        ([r for r in rows if r["role"] in ("mixed", "too small to rank") and r["size"] > 1],
         GRAY, "other departments"),
        ([r for r in rows if r["role"] == "bridge"], ORANGE, "bridges (bottom quartile)"),
        ([r for r in rows if r["role"] == "insular"], BLUE, "insular (top quartile)"),
    )
    for group, c, lab in groups:
        a2.scatter([100 * r["within_share_chance"] for r in group],
                   [100 * r["within_share"] for r in group],
                   s=[14 + 1.6 * r["size"] for r in group], color=c, alpha=0.9,
                   edgecolor=SURFACE, linewidth=1.5, label=lab, zorder=3)
    xmax = 100 * max(r["within_share_chance"] for r in rows) * 1.1
    a2.plot([0, xmax], [0, xmax], color=INK2, linestyle="--", linewidth=1, zorder=2)
    a2.text(xmax * 0.97, xmax * 0.97 + 2, "chance", color=INK2, fontsize=8, ha="right")

    by_dept = {r["department"]: r for r in rows}
    insular = sorted((r for r in rows if r["role"] == "insular"), key=lambda r: -r["within_share"])
    largest = max(rows, key=lambda r: r["size"])
    for r, text in [(r, "dept %d" % r["department"]) for r in insular[:3]] + \
                   [(largest, "dept %d (largest)" % largest["department"])]:
        a2.annotate(text, (100 * r["within_share_chance"], 100 * r["within_share"]),
                    xytext=(7, 3), textcoords="offset points", fontsize=8, color=INK)
    bridges = sorted(r["department"] for r in rows if r["role"] == "bridge")
    top_b = max(100 * by_dept[d]["within_share"] for d in bridges)
    a2.text(4.0, top_b + 5, "bridges: depts " + ", ".join(map(str, bridges)) +
            "\n- most of their mail leaves the department",
            fontsize=8, color=INK2, va="bottom")
    a2.set_xlabel("Within-department share expected by chance (%)", color=INK2, fontsize=10)
    a2.set_ylabel("Observed within-department share (%)", color=INK2, fontsize=10)
    a2.set_ylim(bottom=0)
    a2.set_xlim(left=0)
    n_above = sum(1 for r in rows if r["size"] > 1 and r["within_share"] > r["within_share_chance"])
    n_multi = sum(1 for r in rows if r["size"] > 1)
    a2.set_title("(b) %d of %d departments sit above the chance line" % (n_above, n_multi),
                 loc="left", color=INK, fontsize=11)
    leg = a2.legend(frameon=False, fontsize=8, labelcolor=INK2, loc="upper left")
    for h in leg.legend_handles:
        h.set_sizes([40])

    fig.tight_layout()
    fig.savefig(path, dpi=150, facecolor=SURFACE)
    plt.close(fig)


def plot_mixing(mix, dept, path):
    k = mix.shape[0]
    sizes = np.bincount(dept, minlength=k)
    order = np.argsort(-sizes)
    m = mix[np.ix_(order, order)].astype(float)
    row = m.sum(axis=1, keepdims=True)
    share = np.divide(m, row, out=np.zeros_like(m), where=row > 0)

    fig, ax = plt.subplots(figsize=(7.2, 6.4), facecolor=SURFACE)
    im = ax.imshow(100 * share, cmap="Blues", vmin=0, vmax=100 * np.percentile(share[share > 0], 98))
    ticks = np.arange(k)
    ax.set_xticks(ticks[::3])
    ax.set_xticklabels(order[::3], fontsize=7, color=INK2)
    ax.set_yticks(ticks[::3])
    ax.set_yticklabels(order[::3], fontsize=7, color=INK2)
    ax.set_xlabel("Recipient's department (largest first)", color=INK2, fontsize=9)
    ax.set_ylabel("Sender's department (largest first)", color=INK2, fontsize=9)
    ax.set_title("Where each department's email goes: the diagonal is home", loc="left",
                 color=INK, fontsize=10)
    cb = fig.colorbar(im, ax=ax, shrink=0.8)
    cb.set_label("% of the sender department's links", color=INK2, fontsize=8)
    cb.ax.tick_params(labelsize=7, colors=INK2)
    fig.tight_layout()
    fig.savefig(path, dpi=150, facecolor=SURFACE)
    plt.close(fig)


def main():
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--graph", default=GML)
    p.add_argument("--shuffles", type=int, default=1000)
    p.add_argument("--seed", type=int, default=427)
    args = p.parse_args()

    G, dept, edges = load(args.graph)
    N, m = len(dept), len(edges)
    k = int(dept.max()) + 1
    sizes = np.bincount(dept, minlength=k)

    obs = within_fraction(dept, edges)
    analytic = float(np.sum(sizes * (sizes - 1)) / (N * (N - 1)))
    a_vol = np.bincount(dept[edges[:, 0]], minlength=k)
    b_vol = np.bincount(dept[edges[:, 1]], minlength=k)
    degree_exp = float(a_vol @ b_vol) / m ** 2

    r_nx = nx.attribute_assortativity_coefficient(G, "department")
    r_ours = assortativity(dept, edges, k)
    assert abs(r_nx - r_ours) < 1e-9, (r_nx, r_ours)

    # the shuffle null: same graph, same department sizes, labels permuted
    rng = np.random.default_rng(args.seed)
    null = np.empty(args.shuffles)
    null_r = np.empty(args.shuffles)
    for i in range(args.shuffles):
        perm = rng.permutation(dept)
        null[i] = within_fraction(perm, edges)
        null_r[i] = assortativity(perm, edges, k)
    z = (obs - null.mean()) / null.std(ddof=1)
    p_emp = (1 + np.sum(null >= obs)) / (1 + args.shuffles)

    # reciprocated links only - pairs who email each other both ways
    und = G.to_undirected(reciprocal=True)
    index = {v: i for i, v in enumerate(G)}
    und_edges = np.array([(index[u], index[v]) for u, v in und.edges()], dtype=np.int64).reshape(-1, 2)
    obs_recip = within_fraction(dept, und_edges) if len(und_edges) else float("nan")

    rows, mix = department_table(dept, edges, N)
    classify(rows)

    os.makedirs(FIG_DIR, exist_ok=True)
    plot_main(obs, null, analytic, degree_exp, rows, FIG)
    plot_mixing(mix, dept, FIG_MIX)

    cols = ["department", "size", "role", "internal_edges", "edges_sent_out",
            "edges_received_in", "within_share", "within_share_chance", "lift",
            "internal_density", "partner_departments", "share_of_all_cross_edges"]
    with open(TABLE, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, lineterminator="\n")
        w.writeheader()
        for r in sorted(rows, key=lambda r: -r["size"]):
            w.writerow({c: (round(r[c], 4) if isinstance(r[c], float) else r[c]) for c in cols})

    ranked = [r for r in rows if r["size"] >= MIN_SIZE]
    above = sum(1 for r in ranked if r["within_share"] > r["within_share_chance"])
    insular = sorted((r for r in rows if r["role"] == "insular"), key=lambda r: -r["within_share"])
    bridges = sorted((r for r in rows if r["role"] == "bridge"), key=lambda r: r["within_share"])
    density = m / (N * (N - 1))
    w_dens = sum(r["internal_edges"] for r in rows) / sum(r["size"] * (r["size"] - 1) for r in rows)

    def row_line(r):
        return ("  dept %2d  %3d people  within %5.1f%% (chance %4.1f%%, %4.1fx)  "
                "%2d partner depts" % (r["department"], r["size"], 100 * r["within_share"],
                                       100 * r["within_share_chance"], r["lift"],
                                       r["partner_departments"]))

    lines = [
        "Homophily by department - src/homophily.py (seed %d, %d shuffles)" % (args.seed, args.shuffles),
        "",
        "nodes %d, directed edges %d, departments %d" % (N, m, k),
        "",
        "-- same-department edges --",
        "observed                        %.4f  (%d of %d edges)" % (obs, round(obs * m), m),
        "chance, analytic (sizes only)   %.4f" % analytic,
        "chance, 1,000-shuffle mean      %.4f  (sd %.4f, 99%% range %.4f-%.4f)" % (
            null.mean(), null.std(ddof=1), *np.percentile(null, [0.5, 99.5])),
        "chance, sizes + email volume    %.4f" % degree_exp,
        "observed / chance               %.1fx" % (obs / analytic),
        "z-score vs shuffles             %.0f" % z,
        "empirical p                     < %.4f  (no shuffle reached the observed value)" % p_emp
        if np.sum(null >= obs) == 0 else "empirical p                     %.4f" % p_emp,
        "reciprocated pairs only         %.4f  (%d mutual pairs)" % (obs_recip, len(und_edges)),
        "",
        "-- assortativity --",
        "attribute_assortativity(dept)   %.4f" % r_nx,
        "shuffled labels, mean (sd)      %.4f (%.4f)" % (null_r.mean(), null_r.std(ddof=1)),
        "",
        "-- density --",
        "whole graph                     %.4f" % density,
        "inside departments (pooled)     %.4f  (%.1fx the whole graph)" % (w_dens, w_dens / density),
        "",
        "departments with %d+ people      %d; above chance: %d" % (MIN_SIZE, len(ranked), above),
        "",
        "-- most insular (top quartile of within-share, %d+ people) --" % MIN_SIZE,
        *[row_line(r) for r in insular],
        "",
        "-- bridges (bottom quartile of within-share: most of their mail crosses) --",
        *[row_line(r) for r in bridges],
        "",
        "-- the hub: largest share of all cross-department links --",
        *["  dept %d  %d people  touches %.1f%% of cross-dept links, %.0f in-links per person "
          "from other depts (median dept %.0f)" % (
              h["department"], h["size"], 100 * h["share_of_all_cross_edges"],
              h["edges_received_in"] / h["size"],
              np.median([r["edges_received_in"] / r["size"] for r in ranked]))
          for h in [max(rows, key=lambda r: r["share_of_all_cross_edges"])]],
    ]
    with open(SUMMARY, "w") as f:
        f.write("\n".join(lines) + "\n")
    print("\n".join(lines))
    print("\nwrote %s, %s, %s, %s" % (FIG, FIG_MIX, TABLE, SUMMARY))


if __name__ == "__main__":
    main()
