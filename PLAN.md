# Work Plan

Four weeks. Six workstreams of roughly equal size. Everyone owns one, and
everyone writes the part of the report that comes out of their own work —
that is what keeps the contribution document honest.

**Adjust the dates** once we confirm the exact presentation date.

## Timeline

| Week | Dates | What happens |
|---|---|---|
| 1 | Nov 16 – Nov 22 | Setup. Data downloaded, graph built, everyone can run the repo. Workstreams claimed. |
| 2 | Nov 23 – Nov 29 | Each person does their analysis. Thanksgiving Nov 26 — lighter week, plan around it. |
| 3 | Nov 30 – Dec 6 | Integrate. All figures final. Full report draft. Slides drafted. |
| 4 | Dec 7 – Dec 13 | Polish, rehearse, submit. |

### Hard checkpoints

| When | What must exist |
|---|---|
| **Wed Nov 18** | `data/email-eu-core.gml` builds for everyone. Anyone blocked says so now. |
| **Sun Nov 29** | Every workstream has produced its figure and a 1-paragraph finding. |
| **Sun Dec 6** | Report draft complete at 4 pages. Slides at 9. |
| **Wed Dec 9** | Full rehearsal, timed. |
| **Presentation day** | Report, slides, contribution doc submitted by the group leader. |

## Workstreams

Each one is: **a script** in `src/`, **one figure or table** in `analysis/`,
**one subsection** of the report, and **one slide**.

### A — Data and pipeline · *Trung Le*
Download, clean, convert SNAP format to GML with department labels attached.
Write the shared loader everyone imports. Produce the basic counts table.

**Done when:** `python3 src/build_graph.py` works on a clean clone and
`data/summary.txt` has the numbers we quote in the Notation section.

### B — Structure and homophily · *Ryan Allen Madayag*
In/out-degree distribution, strongly and weakly connected components, average
path length, clustering coefficient. Then: what fraction of edges stay inside a
department, versus what you'd expect by chance?

**Done when:** a degree-distribution plot, a small-world claim with numbers, and
a homophily figure comparing observed vs expected cross-department edges.

### C — Centrality and super-spreaders · *Sean Roser*
Degree, betweenness and PageRank for every node. Do they agree on who is
dangerous? Rank-correlate them. Identify the top 20 by each measure.

**Done when:** a table of the top 20 by each measure, plus a figure showing how
much the three rankings overlap.

### D — SIR / SIS simulation · *Zhihan Yao*
Implement SIR on the directed graph. One infected seed, infection probability
beta per contact, recovery after a fixed number of steps. Sweep beta. Average
over many runs.

**Done when:** infected-over-time curves for a range of beta, and a stated
epidemic threshold — the beta below which it dies out.

### E — Interventions and results · *(open)*
The payoff section. Immunise k users before the outbreak — by degree, by
betweenness, by PageRank, at random — and measure the final outbreak size.
Sweep k from 0 to about 100.

**Done when:** one figure, final outbreak size vs k, four curves. This is our
headline result and the slide people will remember.

### F — Literature and report · *Matthew Saldivar*
Find and summarise the papers our solution is grounded in: network epidemiology,
targeted immunization, phishing susceptibility studies. Write Abstract,
Introduction and Conclusion. Assemble everyone's subsections into 4 pages and
enforce the page limit.

**Done when:** `literature/notes.md` has at least 8 papers with one-line
takeaways, and `report/` holds a 4-page document.

### Shared — presentation
Everyone turns their own figure into one slide. Matthew assembles, Zhihan opens
(motivation and problem), the person on E presents the headline result. Whole
group rehearses Dec 9.

## If we end up with 7 people

Split **D** into "model implementation" and "parameter sweep plus validation",
or split **F** into "literature" and "writing and editing".

## If we stay at 5

Workstream **E** goes to whoever finishes first — most likely C or D, since the
immunization code reuses their centrality rankings and simulation directly.

## Report sections and who drafts them

| Section | Pages | Drafted by |
|---|---|---|
| Abstract | 0.2 | F |
| Introduction — motivation, problem statement | 0.6 | F, with D |
| Notation / Model — graph definition, SIR equations, parameters | 1.2 | A + B + D |
| Proposed Solution — centrality targeting, immunization results | 1.4 | C + E |
| Conclusion and Future Work | 0.6 | F |

## Slides

| # | Slide | Owner |
|---|---|---|
| 1 | Motivation — phishing costs, why networks matter | D |
| 2 | Problem statement and dataset | A |
| 3 | The network — structure and homophily | B |
| 4 | Model — SIR on a directed email graph | D |
| 5 | Who spreads it — centrality comparison | C |
| 6 | Intervention — targeted vs random | E |
| 7 | Results — the headline figure | E |
| 8 | Limitations and future work | F |
| 9 | Conclusion | F |
