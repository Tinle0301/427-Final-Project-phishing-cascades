# Scripts

One script per workstream. Each one reads `data/email-eu-core.gml` and writes
its figures into `analysis/figures/` and any numbers into `analysis/`.

| File | Workstream | Owner |
|---|---|---|
| `build_graph.py` | A — builds the GML everyone else loads | Trung Le |
| `structure.py` | B — degrees, components, path length, clustering | Ryan Allen Madayag |
| `homophily.py` | C — within vs across department edges | Trong Le |
| `centrality.py` | D — degree, betweenness, PageRank, rank correlation | Sean Roser |
| `simulate_sir.py` | E — the SIR model and beta sweep | Zhihan Yao |
| `immunize.py` | F — targeted vs random immunization | Jack Nguyen |

## Conventions

- Take arguments from the command line, never `input()`
- Use `matplotlib.use("Agg")` and save files; never `plt.show()`
- Seed anything random, so results reproduce
- Write figures to `analysis/figures/<name>.png` at `dpi=150`
