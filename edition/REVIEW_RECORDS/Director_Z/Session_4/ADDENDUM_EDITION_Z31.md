# Director Z | Twenty-seventh addendum: edition Z31

15 November 2026, UTC. Same session as the twenty-sixth addendum. Root Review: G1, OPEN. No ontology is selected. No gate changes state.

The principal selected the Mathematics and Science modules for the work of this session and asked for the plot instrument to be used. Both Specifications were read in full before this review was commissioned, and the selection is recorded in the register.

## Assessment Z4-AE (FOCUSED): proofs for the two hypotheses of edition Z30, and three or more classes of winding

**Result.** G10 now has 63 labelled statements and 70 pages. In the subsection on the winding of the walks at one ring vertex:
- Proposition 5.60 (three groups on two levels, formerly 5.58) now has its proof in the paper, stage by stage. Theorem 5.61 (two classes, formerly 5.59) no longer carries it as a hypothesis.
- The one-winding property behind Proposition 5.58 (formerly 5.57) is traced to the statements of Director G's one-gain note. It holds as far as those hold.
- Lemma 5.54 gains part (iii): if an outer level carries one walk, n(l)·n(l+2M) ≤ n(l+M)(n(l+M)−1)/2. The hypothesis is needed.
- New Corollary 5.57: three levels on one rail force two on the other. So for three or more classes no site pairs a three-coset multiset with a one-coset one.
- New Lemma 5.59: invariance under H and F_L = F_R∘T_c hold on every multiset that occurs, without any preparation.
- New Theorem 5.62: for three or more classes and M ≥ 8, on multisets in two adjacent cosets the rule is α|m| + q(ε_i² + ε_{i+1}²) + c_i ε_i ε_{i+1}. For three classes this fixes the combination of the count and the two squares.
- Open: whether the rule equals that combination on multisets that meet three cosets.

**Checks.**
- Proof of Proposition 5.60: the terminal field equals the statement in 54,352 replays made from the paper text alone. One false sentence and three omissions were found and corrected.
- Lemma 5.54(iii), Corollary 5.57: exchanged walks built pair by pair for 875,927 pairs; 7,864 and 8,671 qualifying instances; no failure.
- Theorem 5.62: exact ranks on 15 cases of groups with quotient of order 3, 4 and 5 equal the statement; each use of the equation in the proof was matched to a prepared pair.
- Every program was rerun by the participant in a fresh folder with identical bytes, except the builder's 12-minute exploration run, which was not rerun in full.

**Graphs.** Three exact plots made with the PCP OS plot instrument (`pcpos plot`, host built from pcp-os commit `e8d62e4`, Director G's branch, not on master), each confirmed by `visualization.ranges`. They show the dimension of the rules left against the length of the cut on rings of 4 and 3 sites, and one winding profile. The challenger made a fourth.

**What the two modules ask, and where it is met.**

| Provision | Met by |
|---|---|
| Mathematics 2: statement, quantifiers, boundary conditions | hypotheses in each statement (M ≥ 8, s, finite order of δ, N ≥ 3); boundary cases N = 1, 2, 4 and M ≤ 7 stated |
| Mathematics 4: proof supports its exact conclusion; counterexamples satisfy the hypotheses | challengers read each step; the (4,6,4) profile shows the hypothesis of 5.54(iii) is needed |
| Mathematics 5: formal statement, checker, axioms | `WindingAxis.lean`, Lean 4.12.0, Mathlib v4.12.0, exit 0, `propext`, `Quot.sound`, `Classical.choice` |
| Mathematics 6: computation states method, coverage, failures; a finite range is not a proof | ranks modulo a prime give an upper bound on the rational nullity, attained by the known rules; ranges and failed predicates listed; nothing marked proved from a computation |
| Mathematics 7: an implication is supported as an implication | Proposition 5.58 and its use are stated as conditional on the one-gain note |
| Science 4.1, computational or theoretical work: premises, algorithm, implementation checks, convergence, sensitivity, applicability | premises in the paper's setting; propagation of counts and exact ranks; second implementations by challengers; convergence shown against the cut and left undecided where it has not settled; three carriers and two rings; no empirical applicability claimed |
| Science 6: reproduction and additional implementation named as such | reruns are same-input reproductions; challengers' programs are additional implementations sharing the paper's definitions |
| Science 7.2: simplified investigations state purpose and boundary | the rings of 3 and 4 sites are test cases for the converse and decide nothing beyond themselves |
| Science 8.3: adverse and incomplete results reported | failed predicates and the killed run of the twenty-sixth addendum stay; the builder's failed predicate on rings of 3, 5 and 6 sites is kept |

**Limits.**
- All reviewers are sub-agents of the participant's model family.
- The plot instrument is from a branch that is not on PCP OS master; the register host is unchanged.
- Three or more classes: not decided on any ring.

Findings Z-152 to Z-154.
