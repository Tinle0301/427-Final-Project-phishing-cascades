# Data

Raw files are **not committed** — they are gitignored. Download them yourself.

## Download

```bash
bash data/download.sh
```

Or by hand, into `data/raw/`:

| File | What it is |
|---|---|
| `email-Eu-core.txt.gz` | the edge list, `sender recipient` per line |
| `email-Eu-core-department-labels.txt.gz` | `node department`, 42 departments (0–41) |
| `email-Eu-core-temporal.txt.gz` | optional: `sender recipient time`, 332,334 timestamped emails |

All from https://snap.stanford.edu/data/

## Then build the graph

```bash
python3 src/build_graph.py
```

Writes `data/email-eu-core.gml` (directed, each node carries a `department`
attribute) and `data/summary.txt`.

## What to expect

SNAP's page reports 1,005 nodes and 25,571 edges. The page also quotes 25,552
edges for the largest weakly connected component while the temporal page quotes
24,929 for what it calls the same thing — **the two pages do not agree**, so we
take our numbers from `summary.txt`, generated from the actual file, not from
the website.

## Caveats to state in the report

- An edge means *at least one* email was sent. It carries no volume or frequency.
- Only internal mail. Nothing entering or leaving the institution is recorded.
- There is no phishing in this data. We simulate the spread on a real contact
  network; the network is real, the outbreak is not.
