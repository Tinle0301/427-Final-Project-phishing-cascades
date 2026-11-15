# Start Here

Read this once, find your name, do your part. Everything else is detail.

**The project:** how a phishing email spreads through a real organisation's
email network, and where limited security training does the most good.

**The data:** `email-Eu-core` from SNAP — 1,005 people at a European research
institution, 25,571 directed emails, each person labelled with one of 42
departments. The network is real; the outbreak we simulate on top of it is not,
and we say so in the report.

---

## 1. Set up (15 minutes, do this first)

```bash
git clone https://github.com/Tinle0301/phishing-cascades.git
cd phishing-cascades
pip install -r requirements.txt
bash data/download.sh
python3 src/build_graph.py
```

If the last command prints a table of counts and writes
`data/email-eu-core.gml`, you are ready. If it fails, say so in the chat the
same day — do not sit on it.

Then add your GitHub username to your row in `TEAM.md`.

---

## 2. Deadlines

| Date | What must be true |
|---|---|
| **Wed Nov 18** | Everyone has the repo running. Nobody is blocked. |
| **Sun Nov 29** | Your figure exists and you can state your finding in one paragraph. |
| **Sun Dec 6** | Report is a full 4 pages. Slides are 9. |
| **Wed Dec 9** | We rehearse the whole talk, timed. |
| **Presentation day** | Leader submits report + slides + contribution doc. |

Thanksgiving is Thu Nov 26, so the second week is short. Plan around it.

---

## 3. How to work

```bash
git checkout -b feature/<your-thing>     # e.g. feature/homophily
# ...write src/<your-script>.py, save figures to analysis/figures/...
git add -A
git commit -m "short description of what you did"
git push -u origin feature/<your-thing>
```

Then open a pull request into `main` on GitHub.

**Rules that keep this from falling apart:**

- Every figure comes from a script. Never hand-made, so we can regenerate it.
- Save figures to `analysis/figures/<name>.png` at `dpi=150`.
- Use `matplotlib.use("Agg")` and `plt.savefig(...)`. Never `plt.show()`.
- Seed anything random so results reproduce.
- Add a line to `CONTRIBUTIONS.md` whenever you finish something. This is a
  graded deliverable and reconstructing it in December is how groups lose marks.

---

## 4. Your task

Everyone produces the same four things: **a script**, **a figure**, **a
subsection of the report**, and **one slide**.

### A — Data and pipeline · Trung Le · slide 2

Own `src/build_graph.py`. Keep it working for everyone.

- Verify our node and edge counts against the SNAP page. They disagree with
  themselves across two pages, so our numbers come from the actual file.
- Produce the counts table that goes in the Notation section.

**Deliver:** `data/summary.txt`, and the dataset paragraph of the report.
**Deadline:** Wed Nov 18 — everyone else is blocked until this works.

### B — Network structure · Ryan Allen Madayag · slide 3

Write `src/structure.py`.

- In-degree and out-degree distributions, plotted log-log
- Strongly and weakly connected components: how many, how big is the largest
- Average shortest path length on the largest SCC, and average clustering
- Compare both against a random graph with the same number of nodes and edges
  (`nx.gnm_random_graph`) — that comparison is what justifies calling it
  small-world

Useful: `G.in_degree()`, `nx.strongly_connected_components`,
`nx.average_shortest_path_length`, `nx.average_clustering(G.to_undirected())`

**Deliver:** `analysis/figures/degree_distribution.png` + a sentence of the form
"average path length is X versus Y in a random graph of the same size, while
clustering is Z versus W."

### C — Homophily and departments · Trong Le · slide 4

Write `src/homophily.py`. This is the homophily topic from the course, applied.

- What fraction of edges connect two people in the **same** department?
- What fraction would you expect if people emailed at random? Compute it two
  ways: analytically from department sizes, and by shuffling the labels 1,000
  times and measuring.
- Which departments are most insular, which act as bridges?
- Report `nx.attribute_assortativity_coefficient(G, "department")`

**Deliver:** `analysis/figures/homophily.png` comparing observed vs expected,
plus a short table of the most and least insular departments.

### D — Centrality and super-spreaders · Sean Roser · slide 6

Write `src/centrality.py`.

- In-degree, out-degree, betweenness and PageRank for all 1,005 nodes
- Top 20 by each measure → `analysis/top_spreaders.csv`
- Do the measures agree? Spearman rank correlation between each pair
  (`scipy.stats.spearmanr`), and how many names the top-20 lists share

At 1,005 nodes exact betweenness runs in seconds — no sampling needed.

**Deliver:** the CSV plus `analysis/figures/centrality_overlap.png`.
**Note:** Jack needs your rankings, so push them as soon as they work.

### E — SIR / SIS simulation · Zhihan Yao · slide 5

Write `src/simulate_sir.py`.

- Discrete-time SIR on the directed graph. Start with one infected node.
  Each step, an infected node infects each out-neighbour with probability
  `beta`; after `tau` steps it recovers and stops spreading.
- Sweep `beta` from about 0.01 to 0.2
- Average 100+ runs per setting, with different random seeds, so curves are smooth
- Find the epidemic threshold: the beta below which outbreaks die out

**Deliver:** `analysis/figures/sir_curves.png` — infected over time, one curve
per beta — and a stated threshold value.
**Note:** Jack reuses your simulation, so make it a function he can import.

### F — Interventions and results · Jack Nguyen · slide 7

Write `src/immunize.py`. **This is our headline result.**

- Before the outbreak starts, immunise `k` users — they cannot be infected and
  cannot spread
- Four ways to choose them: highest degree, highest betweenness, highest
  PageRank (all from Sean), and at random
- Sweep `k` from 0 to about 100, measure the **final outbreak size** each time
- Average over many runs

**Deliver:** `analysis/figures/immunization.png` — final outbreak size vs k,
four curves — and the headline number: "training k users chosen by X cuts the
outbreak by Y% compared with training k at random."

You depend on D and E, so expect to start around **Nov 24**. Until then, help
test their code.

### G — Literature and report assembly · Matthew Saldivar · slide 8

Own `literature/notes.md` and `report/`.

- At least 8 papers, one-line takeaway each. Start with: network epidemiology
  (Pastor-Satorras & Vespignani), targeted immunization, influence maximization
  (Kempe, Kleinberg & Tardos), phishing susceptibility studies, and the paper
  the dataset came from.
- Write the Abstract, Introduction and Conclusion
- Assemble everyone's subsections into 4 pages and enforce the limit

Open the papers you cite. Do not cite from an abstract.

**Deliver:** `literature/notes.md` and a 4-page document in `report/`.
You are writing throughout, not only at the end.

---

## 5. Who is waiting on whom

```
A (data)  ──►  B, C, D, E
D + E     ──►  F
everyone  ──►  G
```

A finishes first or everyone is stuck. F starts once D and E run. G writes the
whole time.

---

## 6. Where things live

| Folder | What goes in it |
|---|---|
| `src/` | your script |
| `analysis/figures/` | your figure |
| `report/` | the 4-page report (outline is in `report/outline.md`) |
| `presentation/` | the 9 slides (outline is in `presentation/outline.md`) |
| `literature/` | paper notes |
| `data/raw/` | downloaded data — gitignored, never commit it |

`PLAN.md` has the full timeline. `TEAM.md` has the roster and slide numbers.
