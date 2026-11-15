# Work Plan

Four weeks, seven workstreams of roughly equal size. Everyone owns one, and
everyone writes the part of the report that comes out of their own work — that
is what keeps the contribution document honest and the marks even.

**Adjust the dates** once we confirm the exact presentation date.

## Timeline

| Week | Dates | What happens |
|---|---|---|
| 1 | Nov 16 – Nov 22 | Setup. Data downloaded, graph built, everyone can run the repo. Workstreams claimed. |
| 2 | Nov 23 – Nov 29 | Each person does their analysis. Thanksgiving Nov 26 — short week, plan around it. |
| 3 | Nov 30 – Dec 6 | Integrate. All figures final. Full report draft. Slides drafted. |
| 4 | Dec 7 – Dec 13 | Polish, rehearse, submit. |

### Hard checkpoints

| When | What must exist |
|---|---|
| **Wed Nov 18** | `data/email-eu-core.gml` builds for everyone. Anyone blocked says so now, not in December. |
| **Sun Nov 29** | Every workstream has its figure and a one-paragraph finding. |
| **Sun Dec 6** | Report draft complete at 4 pages. Slides at 9. |
| **Wed Dec 9** | Full rehearsal, timed. |
| **Presentation day** | Report, slides and contribution doc submitted by the group leader. |

## Workstreams

Each one is: **a script** in `src/`, **one figure or table** in `analysis/`,
**one subsection** of the report, **one slide**.

### A — Data and pipeline · *Trung Le*
Download, clean, convert SNAP format to GML with department labels attached.
Maintain the shared loader everyone imports. Produce the basic counts table.

**Done when:** `python3 src/build_graph.py` works on a clean clone and
`data/summary.txt` holds the numbers we quote in the Notation section.

### B — Network structure · *Ryan Allen Madayag*
In- and out-degree distributions. Strongly and weakly connected components.
Average shortest path length and clustering coefficient — is it small-world?
Density and reciprocity.

**Done when:** a degree-distribution plot and a small-world claim backed by
numbers, in `analysis/figures/degree_distribution.png`.

### C — Homophily and departments · *Trong Le*
With 42 department labels: what fraction of edges stay inside a department
versus what chance would predict? Which departments are insular, which are
bridges? This is the homophily topic from the course, applied directly.

**Done when:** a figure comparing observed vs expected cross-department edges,
plus a short table of the most and least insular departments.

### D — Centrality and super-spreaders · *Sean Roser*
Degree, betweenness and PageRank for every node. Do the three agree on who is
dangerous? Rank-correlate them. Produce the top 20 by each measure.

**Done when:** `analysis/top_spreaders.csv` and a figure showing how much the
three rankings overlap.

### E — SIR / SIS simulation · *Zhihan Yao*
Implement SIR on the directed graph. One infected seed, infection probability
beta per contact, recovery after tau steps. Sweep beta. Average over many runs
so the curves are stable.

**Done when:** infected-over-time curves across a range of beta, and a stated
epidemic threshold — the beta below which the outbreak dies out.

### F — Interventions and results · *Jack Nguyen*
The payoff. Immunise k users before the outbreak — by degree, by betweenness,
by PageRank, and at random — then measure the final outbreak size. Sweep k from
0 to about 100. Uses D's rankings and E's simulation, so coordinate with both.

**Done when:** one figure, final outbreak size vs k, four curves. This is our
headline result and the slide people will remember.

### G — Literature and report assembly · *Matthew Saldivar*
Find and summarise the papers the solution is grounded in: network epidemiology,
targeted immunization, phishing susceptibility. Write Abstract, Introduction and
Conclusion. Assemble everyone's subsections into 4 pages and enforce the limit.

**Done when:** `literature/notes.md` holds at least 8 papers with one-line
takeaways, and `report/` holds a 4-page document.

## Dependencies — who is waiting on whom

```
A (data)  ──►  B, C, D, E          everyone needs the .gml first
D + E     ──►  F                   F needs rankings and a working simulation
all       ──►  G                   G assembles last
```

So **A finishes first** (week 1), **F starts once D and E have something
runnable** (midway through week 2), and **G is writing throughout** rather than
only at the end.

## Report sections and who drafts them

| Section | Pages | Drafted by |
|---|---|---|
| Abstract | 0.2 | G |
| Introduction — motivation, problem statement | 0.6 | G, with E |
| Notation / Model — graph definition, SIR equations, parameters | 1.2 | A + B + C + E |
| Proposed Solution — centrality targeting, immunization results | 1.4 | D + F |
| Conclusion and Future Work | 0.6 | G |

## Slides — nine, one owner each

| # | Slide | Owner |
|---|---|---|
| 1 | Motivation — phishing costs, why networks matter | shared, presented by E |
| 2 | Problem statement and dataset | A — Trung |
| 3 | The network — structure and small-world | B — Ryan |
| 4 | Homophily — spread inside vs across departments | C — Trong |
| 5 | Model — SIR on a directed email graph | E — Zhihan |
| 6 | Who spreads it — centrality comparison | D — Sean |
| 7 | **Results** — targeted vs random immunization | F — Jack |
| 8 | Limitations and future work | G — Matthew |
| 9 | Conclusion | shared |

## Working agreement

- Branch per workstream (`feature/homophily`), pull request into `main`
- Do not commit raw data — `data/raw/` is gitignored
- Every figure is produced by a script, never by hand, so it can be regenerated
- Log what you did in `CONTRIBUTIONS.md` as you go
- Blocked for more than a day? Say so in the group chat. Silence is what sinks
  group projects, not difficulty.
