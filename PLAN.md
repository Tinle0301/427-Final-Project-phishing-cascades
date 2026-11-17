# Work Plan

**DUE: Tuesday Dec 1, 2026 at 23:59.**

**All seven workstreams finish Wednesday Nov 25 — the day before Thanksgiving.**
Everything after that is buffer, polish, and rehearsal. Nobody works over the
holiday, and if something slips we still have five days to fix it.

Seven workstreams of roughly equal size. Everyone owns one, and everyone writes
the part of the report that comes out of their own work.

## Timeline

| Dates | What happens |
|---|---|
| **Mon Nov 16 – Tue Nov 17** | Setup. Everyone clones, installs, builds the graph. |
| **Wed Nov 18 – Sat Nov 21** | Analyses B, C, D, E. Four days, all in parallel. |
| **Sun Nov 22 – Wed Nov 25** | F (immunization). G assembles the report and slides. |
| **Wed Nov 25, 23:59** | **EVERYTHING DONE.** All figures, all report text, all slides. |
| **Thu Nov 26 – Fri Nov 27** | Thanksgiving. Nothing scheduled. |
| **Sat Nov 28 – Sun Nov 29** | Buffer. Only used if something slipped. |
| **Mon Nov 30** | Rehearse. Final read-through. |
| **Tue Dec 1** | Final check. **Submit before 23:59.** |

### Hard checkpoints

| When | What must be true | Who is blocked if it slips |
|---|---|---|
| **Tue Nov 17, EOD** | Repo runs for all seven of us | everyone |
| **Sat Nov 21, EOD** | B, C, D, E figures done and pushed | **Jack cannot start** without D and E |
| **Wed Nov 25, 23:59** | All six figures + all report subsections + 9 slides | — |
| **Mon Nov 30** | Rehearsal done | — |
| **Tue Dec 1, 23:59** | Report + slides + contribution doc submitted | — |

**Sat Nov 21 is the one date that matters.** Jack has four days after it, and
nothing after Nov 25 depends on anyone but the group as a whole.

## Workstreams

Each one is: **a script** in `src/`, **one figure or table** in `analysis/`,
**one subsection** of the report, **one slide**.

### A — Data and pipeline · *Trung Le* · due Tue Nov 17
Own `src/build_graph.py`. Verify our counts against the SNAP page (its own two
pages disagree, so our numbers come from the file). Produce the counts table for
the Notation section.
**Deliver:** `data/summary.txt` + the dataset paragraph.

### B — Network structure · *Ryan Allen Madayag* · due Sat Nov 21
In/out-degree distributions log-log. SCC and WCC counts and largest. Average
shortest path length on the largest SCC, average clustering. Compare both
against `nx.gnm_random_graph` of the same size — that comparison is what
justifies the small-world claim.
**Deliver:** `analysis/figures/degree_distribution.png` + one sentence with the
numbers.

### C — Homophily and departments · *Trong Le* · due Sat Nov 21
What fraction of edges stay inside a department? What would chance predict —
computed analytically and by shuffling labels 1,000 times? Which departments are
insular, which bridge? Report
`nx.attribute_assortativity_coefficient(G, "department")`.
**Deliver:** `analysis/figures/homophily.png` + a short table.

### D — Centrality and super-spreaders · *Sean Roser* · due Sat Nov 21
In-degree, out-degree, betweenness, PageRank for all 1,005 nodes. Top 20 by
each. Spearman correlation between the measures. Exact betweenness runs in
seconds at this size.
**Deliver:** `analysis/top_spreaders.csv` + `figures/centrality_overlap.png`.
**Jack is blocked until you push.**

### E — SIR / SIS simulation · *Zhihan Yao* · due Sat Nov 21
Discrete-time SIR on the directed graph. One seed, infection probability beta
per contact, recovery after tau steps. Sweep beta ~0.01 to 0.2, average 100+
runs. Find the epidemic threshold.
**Deliver:** `analysis/figures/sir_curves.png` + the threshold value.
**Write it as an importable function — Jack reuses it.**

### F — Interventions and results · *Jack Nguyen* · due Wed Nov 25
Immunise k users before the outbreak — by degree, betweenness, PageRank, and at
random. Sweep k from 0 to ~100, measure final outbreak size, average over runs.
**Deliver:** `analysis/figures/immunization.png` — our headline figure — plus
the number: "targeting k users by X cuts the outbreak Y% versus random."
**You start Sun Nov 22.** Before then, help test D and E so they land on time.

### G — Literature and report assembly · *Matthew Saldivar* · due Wed Nov 25
At least 8 papers with one-line takeaways. Write Abstract, Introduction,
Conclusion. Assemble everyone's subsections into 4 pages and enforce the limit,
and build the 9 slides.
**Deliver:** `literature/notes.md` + a 4-page document in `report/` + the deck.
**Start the literature review now** — it does not depend on anyone's code, so
it is the one task you can finish early and then spend the rest of your time
assembling.

## Who is waiting on whom

```
A (Nov 17)  ──►  B, C, D, E (Nov 21)
D + E       ──►  F (Nov 25)
everyone    ──►  G (Nov 25)
```

## Report sections

| Section | Pages | Drafted by |
|---|---|---|
| Abstract | 0.2 | G |
| Introduction | 0.6 | G, with E |
| Notation / Model | 1.2 | A + B + C + E |
| Proposed Solution | 1.4 | D + F |
| Conclusion and Future Work | 0.6 | G |

Everyone's subsection is in the repo by **Wed Nov 25**, not handed to Matthew at
the end.

## Slides — nine, one owner each

| # | Slide | Owner |
|---|---|---|
| 1 | Motivation | shared — Zhihan opens |
| 2 | Problem and dataset | Trung Le |
| 3 | The network — structure, small-world | Ryan Allen Madayag |
| 4 | Homophily — inside vs across departments | Trong Le |
| 5 | Model — SIR on a directed email graph | Zhihan Yao |
| 6 | Who spreads it — centrality | Sean Roser |
| 7 | **Results** — targeted vs random | Jack Nguyen |
| 8 | Limitations | Matthew Saldivar |
| 9 | Conclusion | shared |

## Working agreement

- Branch per workstream, pull request into `main`
- Never commit raw data — `data/raw/` is gitignored
- Every figure comes from a script so it can be regenerated
- Log what you did in `CONTRIBUTIONS.md` as you go
- **Blocked for more than half a day? Post in the chat.** The whole point of
  finishing Nov 25 is that a slip has somewhere to go — but only if we know
  about it.

## One thing to confirm

The Dec 1 deadline is for the submission. The assignment also says the
presentation happens during the last week of classes, which may be a separate
date. **Someone should confirm with the professor** whether we present on Dec 1
or later. We are planning to be fully ready by Nov 25 either way.
