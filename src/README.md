# Scripts

One script per workstream. Each one reads `data/email-eu-core.gml` and writes
its figures into `analysis/figures/` and any numbers into `analysis/`.

| File | Workstream | Owner |
|---|---|---|
| `build_graph.py` | A — builds the GML everyone else loads | Trung |
| `structure.py` | B — degrees, components, path length, homophily | Ryan |
| `centrality.py` | C — degree, betweenness, PageRank, rank correlation | Sean |
| `simulate_sir.py` | D — the SIR model and beta sweep | Zhihan |
| `immunize.py` | E — targeted vs random immunization | open |

## Conventions

- Take arguments from the command line, never `input()`
- Use `matplotlib.use("Agg")` and save files; never `plt.show()`
- Seed anything random, so results reproduce
- Write figures to `analysis/figures/<name>.png` at `dpi=150`
