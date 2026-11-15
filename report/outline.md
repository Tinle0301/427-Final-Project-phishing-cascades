# Report outline — 4 pages

Hard limit. Anything that does not earn its space comes out.

## Abstract (~150 words)
What we did, on what data, what we found, what we recommend. Written last.

## 1. Introduction (~0.6 page)
- Phishing is the entry point for most breaches; one click compromises an org
- Security training is expensive, so it cannot go to everyone equally
- **Problem statement:** given an organisation's email network, where does
  limited security effort do the most good?

## 2. Notation / Model (~1.2 pages)
- The graph: G = (V, E), directed, |V| = 1,005, |E| = 25,571, node attribute `department`
- Why directed matters: phishing travels the way mail travels
- Centrality definitions: degree, betweenness, PageRank
- The SIR model: states S/I/R, infection probability beta per contact, recovery
  after tau steps, discrete time
- Structural facts that shape the spread: path length, clustering, homophily

## 3. Proposed Solution (~1.4 pages)
- Target training by network position, not at random
- Compare four strategies for choosing the k users to train
- Results: final outbreak size vs k, for each strategy
- The headline number: *targeted training on k = __ users cuts the outbreak by __%
  compared with training __ at random*
- Why it works, in terms of the structure from section 2
- Ethics and feasibility: this uses metadata, not message content; who gets
  flagged and what that means for them

## 4. Conclusion and Future Work (~0.6 page)
- What we showed
- Limits: simulated outbreak, no message content, one organisation, static graph
- Future: use the temporal version for a real time-ordered cascade; model
  heterogeneous susceptibility instead of one beta for everyone

## Sources
Every claim that is not ours gets a citation.
