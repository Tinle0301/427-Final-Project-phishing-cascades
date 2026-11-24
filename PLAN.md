# Work Plan

**DUE: Monday Dec 7, 2026.** (Moved from Dec 1.)

**Code still finishes Wednesday Nov 25 — the day before Thanksgiving.** Four of
the five analysis workstreams are already done, and letting them drift into the
holiday would turn finished work back into unfinished work. The extra week goes
to writing and the deck, which is where we are actually behind.

Seven workstreams of roughly equal size. Everyone owns one, and everyone writes
the part of the report that comes out of their own work.

## Timeline

| Dates | What happens |
|---|---|
| **done** | A, B, C, D, E — code, figures and data all in the repo. |
| **Wed Nov 25** | **All code done, all PRs merged.** This is F (immunization). |
| **Thu Nov 26 – Fri Nov 27** | Thanksgiving. Nothing scheduled. |
| **Sun Nov 29** | Every report subsection written in the Doc. F if it slipped. |
| **Tue Dec 1** | G has the full 4-page draft assembled. |
| **Thu Dec 3** | All 9 slides built. |
| **Fri Dec 4** | Everyone reads the whole report. Timed rehearsal. |
| **Sat Dec 5 – Sun Dec 6** | Buffer and polish. |
| **Mon Dec 7** | **Submit.** |

### Hard checkpoints

| When | What must be true | Who is blocked if it slips |
|---|---|---|
| **Wed Nov 25** | F done; every branch merged into `main` | G cannot assemble |
| **Sun Nov 29** | All 11 report subsections written | G cannot assemble |
| **Tue Dec 1** | 4-page draft exists | everyone — no draft, nothing to rehearse |
| **Thu Dec 3** | 9 slides built | — |
| **Fri Dec 4** | Rehearsal done, timed | — |
| **Mon Dec 7** | Report + slides + contribution doc submitted | — |

**The date that matters now is Sun Nov 29.** The analysis is nearly finished;
the writing has barely started. Two of eleven report subsections exist. If the
29th slips, every date after it slips with it, because assembly cannot begin
until the sections are written.

**Still to confirm with the professor:** whether the *presentation* moved with
the submission, or whether we still present during the last week of classes. If
the presentation stays put, the deck is due before the report and this schedule
is the wrong way round.

## Workstreams

Each one is: **a script** in `src/`, **one figure or table** in `analysis/`,
**one subsection** of the report, **one slide**.

### A — Data and pipeline · *Trung Le* · due Tue Nov 17
Own `src/build_graph.py`. Verify our counts against the SNAP page (its own two
pages disagree, so our numbers come from the file). Produce the counts table for
the Notation section.
**Deliver:** `data/summary.txt` + the dataset paragraph.

### B — Network structure · *Ryan Allen Madayag* · DONE
In/out-degree distributions log-log. SCC and WCC counts and largest. Average
shortest path length on the largest SCC, average clustering. Compare both
against `nx.gnm_random_graph` of the same size — that comparison is what
justifies the small-world claim.
**Deliver:** `analysis/figures/degree_distribution.png` + one sentence with the
numbers.

### C — Homophily and departments · *Trong Le* · DONE
What fraction of edges stay inside a department? What would chance predict —
computed analytically and by shuffling labels 1,000 times? Which departments are
insular, which bridge? Report
`nx.attribute_assortativity_coefficient(G, "department")`.
**Deliver:** `analysis/figures/homophily.png` + a short table.

### D — Centrality and super-spreaders · *Sean Roser* · DONE, merged
In-degree, out-degree, betweenness, PageRank for all 1,005 nodes. Top 20 by
each. Spearman correlation between the measures. Exact betweenness runs in
seconds at this size.
**Deliver:** `analysis/top_spreaders.csv` + `figures/centrality_overlap.png`.
**Jack is blocked until you push.**

### E — SIR / SIS simulation · *Zhihan Yao* · DONE
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
**Sean's rankings and Zhihan's `simulate()` are both ready.** Before writing the sweep, note that outbreak sizes are bimodal: at beta=0.05 roughly 30% of runs fizzle at ~1 person and 70% reach ~800, with nothing in between, because 181 of 1,005 people have out-degree 0. Seed only from nodes with out-degree > 0, or report the mean given the outbreak took off — and say which in 3.2.

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
A, B, C, D, E   done
D + E       ──►  F (Nov 25)
everyone    ──►  report sections (Nov 29)
sections    ──►  G assembles draft (Dec 1), slides (Dec 3)
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
