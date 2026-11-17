# Start Here

Read this once, find your name, do your part.

## ⏰ DUE TUESDAY DEC 1, 2026 AT 23:59

**But our internal deadline is Wednesday Nov 25 — the day before Thanksgiving.**
All seven parts are done by then. Nobody works over the holiday, and the days
after it are buffer in case something slipped.

**The project:** how a phishing email spreads through a real organisation's
email network, and where limited security training does the most good.

**The data:** `email-Eu-core` from SNAP — 1,005 people at a European research
institution, 24,929 directed email links after self-loops are removed, each
person labelled with one of 42 departments.
The network is real; the outbreak we simulate on top of it is not, and we say so
in the report.

---

## 1. Set up — do this today or tomorrow

```bash
git clone https://github.com/Tinle0301/phishing-cascades.git
cd phishing-cascades
pip install -r requirements.txt
bash data/download.sh
python3 src/build_graph.py
```

If the last command prints a table of counts and writes
`data/email-eu-core.gml`, you are ready. If it fails, post in the chat **that
day**.

Then add your GitHub username to your row in `TEAM.md`.

---

## 2. Deadlines

| Date | What must be true |
|---|---|
| **Tue Nov 17** | Everyone has the repo running |
| **Sat Nov 21** | B, C, D, E figures done and pushed |
| **Wed Nov 25, 23:59** | **EVERYTHING DONE** — all figures, all report text, all 9 slides |
| **Thu Nov 26 – Fri Nov 27** | Thanksgiving — nothing scheduled |
| **Sat Nov 28 – Sun Nov 29** | Buffer only |
| **Mon Nov 30** | Rehearsal |
| **Tue Dec 1, 23:59** | **SUBMIT** |

**Sat Nov 21 is the date that matters** — Jack cannot start the headline result
until Sean and Zhihan have pushed, and he needs those four days.

---

## 3. How to work

```bash
git checkout -b feature/<your-thing>
# write src/<your-script>.py, save figures to analysis/figures/
git add -A
git commit -m "short description"
git push -u origin feature/<your-thing>
```

Then open a pull request into `main`.

**Rules:**

- Every figure comes from a script, never made by hand
- Save to `analysis/figures/<name>.png` at `dpi=150`
- Use `matplotlib.use("Agg")` and `plt.savefig(...)`. Never `plt.show()`
- Seed anything random
- Add a line to `CONTRIBUTIONS.md` whenever you finish something — it is graded

---

## 4. Your task

Everyone produces: **a script**, **a figure**, **a report subsection**, **one slide**.

### A — Data and pipeline · Trung Le · **due Tue Nov 17** · slide 2
Own `src/build_graph.py`, keep it working for everyone. Verify counts against
SNAP (its pages contradict each other, so we trust the file). Produce the counts
table for the Notation section.
**Deliver:** `data/summary.txt` + the dataset paragraph.

### B — Network structure · Ryan Allen Madayag · **due Sat Nov 21** · slide 3
`src/structure.py`
- In- and out-degree distributions, log-log
- SCC and WCC: how many, how big is the largest
- Average shortest path length on the largest SCC, average clustering
- Compare both to `nx.gnm_random_graph` of the same size — that is the
  small-world claim

Useful: `G.in_degree()`, `nx.strongly_connected_components`,
`nx.average_shortest_path_length`, `nx.average_clustering(G.to_undirected())`

**Deliver:** `figures/degree_distribution.png` + "path length is X vs Y random,
clustering is Z vs W."

### C — Homophily and departments · Trong Le · **due Sat Nov 21** · slide 4
`src/homophily.py`
- What fraction of edges connect two people in the same department?
- What would chance predict? Two ways: analytically from department sizes, and
  by shuffling labels 1,000 times
- Which departments are insular, which are bridges?
- Report `nx.attribute_assortativity_coefficient(G, "department")`

**Deliver:** `figures/homophily.png` (observed vs expected) + a short table.

### D — Centrality and super-spreaders · Sean Roser · **due Sat Nov 21** · slide 6
`src/centrality.py`
- In-degree, out-degree, betweenness, PageRank for all 1,005 nodes
- Top 20 by each → `analysis/top_spreaders.csv`
- Do they agree? `scipy.stats.spearmanr` between each pair, and how many names
  the top-20 lists share

Exact betweenness runs in seconds at 1,005 nodes — no sampling needed.

**Deliver:** the CSV + `figures/centrality_overlap.png`.
**Push as soon as the rankings work — Jack is blocked on you.**

### E — SIR / SIS simulation · Zhihan Yao · **due Sat Nov 21** · slide 5
`src/simulate_sir.py`
- Discrete-time SIR, directed. One infected seed. Each step an infected node
  infects each out-neighbour with probability `beta`; after `tau` steps it
  recovers
- Sweep `beta` ~0.01 to 0.2, average 100+ runs per setting
- Find the epidemic threshold — the beta below which outbreaks die out

**Deliver:** `figures/sir_curves.png` + the threshold.
**Make the simulation an importable function — Jack reuses it.**

### F — Interventions and results · Jack Nguyen · **due Wed Nov 25** · slide 7
`src/immunize.py` — **our headline result**
- Immunise k users before the outbreak: they cannot be infected or spread
- Four strategies: top degree, top betweenness, top PageRank (all from Sean),
  and random
- Sweep k from 0 to ~100, measure final outbreak size, average over runs

**Deliver:** `figures/immunization.png` — outbreak size vs k, four curves — plus
the headline number.
**You start Sun Nov 22.** Until then, help test D and E so they land on the 21st.

### G — Literature and report assembly · Matthew Saldivar · **due Wed Nov 25** · slide 8
`literature/notes.md` and `report/`
- 8+ papers, one-line takeaway each: network epidemiology (Pastor-Satorras &
  Vespignani), targeted immunization, influence maximization (Kempe, Kleinberg
  & Tardos), phishing susceptibility, and the dataset's own paper
- Write Abstract, Introduction, Conclusion
- Assemble everyone's subsections into 4 pages and enforce the limit
- Build the 9 slides

Open the papers you cite; do not cite from an abstract.

**Start the literature review now** — it does not depend on anyone's code, so
finish it early and spend the rest of your time assembling.

---

## 5. Who is waiting on whom

```
A (Nov 17)  ──►  B, C, D, E (Nov 21)
D + E       ──►  F (Nov 25)
everyone    ──►  G (Nov 25)
```

---

## 6. Where things live

| Folder | What goes in it |
|---|---|
| `src/` | your script |
| `analysis/figures/` | your figure |
| `report/` | the 4-page report (`report/outline.md`) |
| `presentation/` | the 9 slides (`presentation/outline.md`) |
| `literature/` | paper notes |
| `data/raw/` | downloaded data — gitignored, never commit |

`PLAN.md` has the full schedule. `TEAM.md` has the roster and slide numbers.
