# Paper notes

One entry per paper. Keep the takeaway to one line.
Grouped by theme, in the order they appear in the Introduction.

---

## Phishing: the problem

**Verizon (2026).** 2026 Data Breach Investigations Report. *Verizon Business.*
Link: https://www.verizon.com/business/resources/reports/dbir/
Takeaway: 62% of breaches involve a human element and 16% involve social engineering; vulnerability exploitation (31%) has overtaken credential abuse as the top entry point.
Where we use it: Introduction, opening motivation.

---

**Ho, G., Cidon, A., Gavish, L., Schweighauser, M., Paxson, V., Savage, S., Voelker, G.M., Wagner, D. (2019).** Detecting and Characterizing Lateral Phishing at Scale. *USENIX Security Symposium.*
Link: https://www.usenix.org/conference/usenixsecurity19/presentation/ho
Takeaway: Across 92 organizations, 154 hijacked employee accounts sent 1,902 phishing emails to colleagues, and about 41% of recipients were fellow employees, so phishing really does spread internally once one account falls.
Where we use it: Introduction (justifies modelling spread inside the email graph); 3.3; future work on external mail.

---

**Jagatic, T.N., Johnson, N.A., Jakobsson, M., Menczer, F. (2007).** Social Phishing. *Communications of the ACM* 50(10), 94–100.
Link: https://doi.org/10.1145/1290958.1290968
Takeaway: A phishing email that appeared to come from a friend fooled 72% of targets versus 16% from a stranger, so who sends the email matters as much as what it says.
Where we use it: Introduction; justifies treating email links as trust channels; future work on weighted edges.

---

**Lain, D., Kostiainen, K., Čapkun, S. (2022).** Phishing in Organizations: Findings from a Large-Scale and Long-Term Study. *IEEE Symposium on Security and Privacy (S&P).*
Link: https://arxiv.org/abs/2112.07498
Takeaway: In a 15-month study of 14,000+ employees, embedded training did not make people more resilient (and sometimes made them worse), while a crowdsourced "report phishing" button worked well at scale.
Where we use it: Introduction (training is costly and uneven); 3.3 (what "immunizing" a user should actually mean).

---

## Network epidemiology

**Pastor-Satorras, R., Vespignani, A. (2001).** Epidemic Spreading in Scale-Free Networks. *Physical Review Letters* 86(14), 3200–3203.
Link: https://doi.org/10.1103/PhysRevLett.86.3200
Takeaway: In networks with a heavy-tailed degree distribution the epidemic threshold can vanish, so even a weak contagion can spread widely.
Where we use it: Introduction (why spread is fast on heavy-tailed networks).

---

**Newman, M.E.J., Forrest, S., Balthrop, J. (2002).** Email Networks and the Spread of Computer Viruses. *Physical Review E* 66, 035101(R).
Link: https://doi.org/10.1103/PhysRevE.66.035101
Takeaway: Email address-book networks are heavy-tailed, so viruses spread through them easily, and protecting the best-connected users slows spread far more than protecting random ones.
Where we use it: Introduction; the closest prior work to ours.

---

## Targeted immunization

**Pastor-Satorras, R., Vespignani, A. (2002).** Immunization of Complex Networks. *Physical Review E* 65, 036104.
Link: https://doi.org/10.1103/PhysRevE.65.036104
Takeaway: Random immunization barely helps on heavy-tailed networks, while immunizing the highest-degree nodes restores an epidemic threshold.
Where we use it: Introduction (theory behind targeted vs. random training).

---

**Cohen, R., Havlin, S., ben-Avraham, D. (2003).** Efficient Immunization Strategies for Computer Networks and Populations. *Physical Review Letters* 91(24), 247901.
Link: https://doi.org/10.1103/PhysRevLett.91.247901
Takeaway: Immunizing random acquaintances of random nodes finds hubs without knowing the whole network, getting close to targeted immunization.
Where we use it: Introduction; future work (a strategy needing less network knowledge).

---

**Holme, P., Kim, B.J., Yoon, C.N., Han, S.K. (2002).** Attack Vulnerability of Complex Networks. *Physical Review E* 65, 056109.
Link: https://doi.org/10.1103/PhysRevE.65.056109
Takeaway: Removing nodes by betweenness can fragment a network faster than removing them by degree, because bridges hold separate groups together.
Where we use it: Introduction (betweenness-based targeting).

---

## Influence maximization and spreaders

**Kempe, D., Kleinberg, J., Tardos, É. (2003).** Maximizing the Spread of Influence through a Social Network. *Proceedings of the 9th ACM SIGKDD Conference*, 137–146.
Link: https://doi.org/10.1145/956750.956769
Takeaway: Choosing the k seeds that maximize spread under independent-cascade and threshold models is NP-hard, but a greedy algorithm is provably within about 63% of optimal and beats degree and centrality heuristics.
Where we use it: Introduction; the "inverse" of our question (we pick k nodes to block rather than seed).

---

**Kitsak, M., Gallos, L.K., Havlin, S., Liljeros, F., Muchnik, L., Stanley, H.E., Makse, H.A. (2010).** Identification of Influential Spreaders in Complex Networks. *Nature Physics* 6, 888–893.
Link: https://doi.org/10.1038/nphys1746
Takeaway: A node's position in the network core (k-shell) predicts its spreading power better than its raw degree or betweenness.
Where we use it: Introduction (why we compare several centrality measures).

---

## The dataset

**Leskovec, J., Kleinberg, J., Faloutsos, C. (2007).** Graph Evolution: Densification and Shrinking Diameters. *ACM Transactions on Knowledge Discovery from Data* 1(1).
Link: https://doi.org/10.1145/1217299.1217301
Takeaway: The source paper for the European research institution email data that email-Eu-core is built from.
Where we use it: Introduction (dataset citation).

---

**Yin, H., Benson, A.R., Leskovec, J., Gleich, D.F. (2017).** Local Higher-Order Graph Clustering. *Proceedings of the 23rd ACM SIGKDD Conference*, 555–564.
Link: https://doi.org/10.1145/3097983.3098069
Takeaway: Introduced the email-Eu-core network with its 42 department labels as ground-truth communities.
Where we use it: Introduction (dataset and department labels).

---

**Easley, D., Kleinberg, J. (2010).** Networks, Crowds, and Markets: Reasoning About a Highly Connected World. *Cambridge University Press.*
Link: https://www.cs.cornell.edu/home/kleinber/networks-book/
Takeaway: Course textbook; standard definitions of centrality, PageRank, cascades and epidemic models.
Where we use it: Anywhere a definition needs a citation.
