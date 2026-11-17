# Phishing Cascades in an Email Network

CECS 427 — Dynamic Networks — Final Group Project

## The question

How does a phishing email spread through a real organisation's email network, and
where should limited security effort be spent to slow it down?

We model the spread as an epidemic on a real email graph, identify the users whose
position makes them the most dangerous carriers, and compare targeted security
training against random training.

## Dataset

**email-Eu-core** (SNAP) — 1,005 members of a European research institution.
An edge `u -> v` means u sent v at least one email. A companion file labels every
node with one of 42 departments.

After removing self-loops the graph we analyse has **1,005 nodes and 24,929
directed edges**. See `data/README.md` for why SNAP publishes three different
edge counts and how they reconcile.

- https://snap.stanford.edu/data/email-Eu-core.html
- Optional, for the time-ordered version: https://snap.stanford.edu/data/email-Eu-core-temporal.html

**Important:** the dataset contains no phishing. It gives us the real contact
network; we simulate the spread on top of it. This is standard practice and we
state it plainly in the report.

## Course topics we apply

| Topic | Where it shows up |
|---|---|
| Graph theory and network structure | degree distribution, SCC/WCC, density |
| Centrality measures | degree vs betweenness vs PageRank as spreader risk |
| Link analysis (PageRank) | ranking who is reachable from everywhere |
| Cascades and diffusion | threshold model of who forwards a phishing email |
| SIR / SIS epidemic models | the core simulation |
| Small-world phenomenon | path lengths explain how fast it reaches everyone |

Six of the nine topics the assignment lists, plus homophily (does a phishing mail
spread faster inside a department than across?), which the threshold model in
`2.5` uses: a department dense enough is what stops a cascade.

Each should do real work in the report rather than being name-dropped.

## Getting set up

```bash
git clone <this repo>
cd phishing-cascades
pip install -r requirements.txt

# download the data (see data/README.md)
bash data/download.sh

# build the graph everyone works from
python3 src/build_graph.py
```

That writes `data/email-eu-core.gml` plus `data/summary.txt`. Every other script
starts from the `.gml`.

## Repo map

```
data/            download instructions; raw files are gitignored
src/             analysis scripts, one per workstream
analysis/        figures and result tables that go in the report
report/          the 4-page report
presentation/    the 9-slide deck
literature/      paper notes for the literature review
PLAN.md          timeline and who does what
CONTRIBUTIONS.md the per-member contribution document we have to submit
```

## Team

Seven members, seven workstreams — see `TEAM.md` for the table and `PLAN.md`
for what each one covers.

| Name | Workstream |
|---|---|
| Trung Le | A — data and pipeline |
| Ryan Allen Madayag | B — network structure |
| Trong Le | C — homophily and departments |
| Sean Roser | D — centrality and super-spreaders |
| Zhihan Yao | E — SIR/SIS simulation |
| Jack Nguyen | F — interventions and results |
| Matthew Saldivar | G — literature and report assembly |


## Ground rules

- Branch per workstream (`feature/centrality`), pull request into `main`
- Do not commit raw data or large files — `data/raw/` is gitignored
- Every figure is produced by a script in `src/`, never by hand, so it can be regenerated
- Log what you did in `CONTRIBUTIONS.md` as you go, not at the end
