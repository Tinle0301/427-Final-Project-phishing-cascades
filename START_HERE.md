# Start Here

Read this once, find your name, do your part.

## ⏰ DUE MONDAY DEC 7, 2026

**Code still finishes Wednesday Nov 25 — the day before Thanksgiving.** The
deadline moved from Dec 1, but do not let everything slide with it: four of the
five analysis workstreams are already done. The extra week goes to writing and
the deck, which is where we are behind.

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
bash data/download.sh          # Windows: python src\download_data.py
python3 src/build_graph.py
```

**On Windows**, `bash data/download.sh` fails with `cd: $'data\r'` errors —
that is a line-ending problem, not your setup. Run `python src\download_data.py`
instead; it does the same thing and needs no bash.

If the last command prints a table of counts and writes
`data/email-eu-core.gml`, you are ready. If it fails, post in the chat **that
day**.

Then add your GitHub username to your row in `TEAM.md`.

---

## 2. Deadlines

| Date | What must be true |
|---|---|
| ~~Sat Nov 21~~ | B, C, D, E — **done**, code is in the repo |
| **Wed Nov 25** | All code done, every branch merged into `main` |
| **Thu Nov 26 – Fri Nov 27** | Thanksgiving — nothing scheduled |
| **Sun Nov 29** | Every report subsection written in the Doc |
| **Tue Dec 1** | Full 4-page draft assembled |
| **Thu Dec 3** | All 9 slides built |
| **Fri Dec 4** | Everyone reads the whole report; timed rehearsal |
| **Sat Dec 5 – Sun Dec 6** | Buffer and polish |
| **Mon Dec 7** | **SUBMIT** |

**Sun Nov 29 is the date that matters now.** The analysis is nearly finished and
the writing has barely started — 2 of 11 report subsections exist. Assembly
cannot begin until the sections are written, so if the 29th slips, every date
after it slips too.

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

### B — Network structure · Ryan Allen Madayag · **done** · slide 3
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

### C — Homophily and departments · Trong Le · **done** · slide 4
`src/homophily.py`
- What fraction of edges connect two people in the same department?
- What would chance predict? Two ways: analytically from department sizes, and
  by shuffling labels 1,000 times
- Which departments are insular, which are bridges?
- Report `nx.attribute_assortativity_coefficient(G, "department")`

**Deliver:** `figures/homophily.png` (observed vs expected) + a short table.

### D — Centrality and super-spreaders · Sean Roser · **done** · slide 6
`src/centrality.py`
- In-degree, out-degree, betweenness, PageRank for all 1,005 nodes
- Top 20 by each → `analysis/top_spreaders.csv`
- Do they agree? `scipy.stats.spearmanr` between each pair, and how many names
  the top-20 lists share

Exact betweenness runs in seconds at 1,005 nodes — no sampling needed.

**Deliver:** the CSV + `figures/centrality_overlap.png`.
**Push as soon as the rankings work — Jack is blocked on you.**

### E — SIR / SIS simulation · Zhihan Yao · **done** · slide 5
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
**Sean's rankings and Zhihan's simulate() are ready.** Read the note in the
chat about outbreak sizes being bimodal before you write the sweep.

### G — Literature and report assembly · Matthew Saldivar · **draft Tue Dec 1 · slides Thu Dec 3** · slide 8
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
A, B, C, D, E   done
D + E       ──►  F (Nov 25)
everyone    ──►  report sections (Nov 29)
sections    ──►  G assembles draft (Dec 1), slides (Dec 3)
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
