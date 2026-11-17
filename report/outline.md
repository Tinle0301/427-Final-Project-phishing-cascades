# Report

**The report is written in the shared Google Doc, not in this folder.**

https://docs.google.com/document/d/15RZsyliuhNZb4LzXrcKMs8_qQ0cAWoex/edit?usp=sharing

This file records only who owns which section and when it is due.

## Hard constraints from the assignment sheet

- **4 pages.** Not negotiable. The word targets below total ~1,970, which is
  already more than fits once three figures and the references take their
  space; Matthew trims about 20% during assembly.
- **The five section names are fixed** by the sheet: Abstract, Introduction,
  Notation / Model, Proposed Solution, Conclusion and Future Work. Do not
  rename them or add top-level sections.
- **Only three figures fit.** `immunization.png` is the headline and stays.
  Two slots remain among `degree_distribution`, `homophily`,
  `centrality_overlap` and `sir_curves`. Decide as a group before Nov 21 — a
  figure that misses the report still goes in the slides.
- A separate **contribution document** is submitted alongside. It is the table
  at the end of the Doc.

## Section map

| Section | Owner | Words | Due |
|---|---|---|---|
| Abstract | Trung Le | ~110 | Wed Nov 25 |
| 1. Introduction (incl. literature review) | Matthew Saldivar | ~300 | Sat Nov 21 |
| 2.1 Dataset and notation | Trung Le | ~110 | done |
| 2.2 Network structure and small-world | Ryan Allen Madayag | ~150 | Sat Nov 21 |
| 2.3 Homophily and departmental clustering | Trong Le | ~150 | Sat Nov 21 |
| 2.4 Centrality measures | Sean Roser | ~150 | Sat Nov 21 |
| 2.5 Diffusion models: epidemic and threshold | Zhihan Yao | ~170 | Sat Nov 21 |
| 3.1 Targeting training by network position | Sean Roser + Jack Nguyen | ~150 | Sat Nov 21 |
| 3.2 Results: targeted vs random immunization | Jack Nguyen | ~300 | Wed Nov 25 |
| 3.3 Feasibility, impact and ethics | Matthew Saldivar | ~150 | Wed Nov 25 |
| 4. Conclusion and Future Work | Matthew Saldivar | ~230 | Wed Nov 25 |
| References | everyone adds their own | — | Wed Nov 25 |

There is no separate Related Work section. At four pages the sheet does not ask
for one, so the literature review lives inside the Introduction. Quality of the
literature review is still a graded criterion.

## Course topics this report claims

"Depth and correctness in applying multiple course topics" is graded. Each of
these must be named and used, not merely implied.

| Topic | Where | Who |
|---|---|---|
| Graph theory and network structure | 2.2, 3.1 | Ryan |
| Centrality (degree, betweenness, clustering, PageRank) | 2.2, 2.4, 3.1 | Ryan, Sean |
| Small-world phenomenon | 2.2, 3.1 | Ryan |
| Homophily and clustering | 2.3 | Trong |
| Epidemic models (SIR/SIS) | 2.5, 3.2 | Zhihan |
| Cascades and diffusion models | 2.5, 3.2 | Zhihan |
| Link analysis (PageRank) | 2.4, 3.1 | Sean |

## Figures

Figures live in `analysis/figures/`, produced by a script in `src/`. Do not
paste images into the Doc; name your figure in your subsection and Matthew
places it during assembly, so the report always matches what the code produces.
