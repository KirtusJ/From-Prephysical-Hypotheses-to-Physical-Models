Target: edition/PAPERS/G10_*/source/body.tex lines 302-328, Proposition 5.14 (prop:abund) and Corollary 5.15 (cor:abund), edition Z15, commit b84056e.
Outcome: GAP (one sentence of the remark after the corollary); no step of either proof fails.
Reviewer kind: pcp-challenger (second challenger on these statements), queue session; same model family as the author; paper text only. Not independent review.

Proof, step by step
- 5.14(a): r0 divides r; d predecessors (square matrix, finite); C acts on D-hat by automorphisms with a constant class shift (uses that C is abelian); pi(h) = length mod r for a closed walk with gain h; image r0 Z/r: all follow. The last step uses that a non-empty subset of Z/r closed under addition is a subgroup (formalized, see the formalizer report of this date).
- 5.14(b): common successor in D-hat; vertices over y1 in one class are a coset of C0; primitivity on a class; growth of counts: follow. "At no length do gains of two cosets occur": follows.
- 5.14(c): follows. Nothing in (a), (b), (c) uses that C is cyclic; degree four needs nothing special.
- 5.15: u u_z' in C0 and their sum is zero, so C0 is not trivial; events with components g a' and g u b'; reduction to (V) on Z[C0]; factor d; converse by extending each conjugate character of the q0-th roots to the q-th roots: all follow.

GAP (remark after 5.15, line 328): "where the gains of closed walks generate a proper subgroup, D-hat is not strongly connected and the proposition applies with that subgroup in place of C". (i) The equivalence needs D itself strongly connected: on 27 of my 261 carriers D was disconnected and D-hat failed to be strongly connected although the closed-walk gains at a vertex generate C (failed predicate N1; with D strongly connected the equivalence held on 234 of 234, N1b). For a finite norm-preserving D connectedness of the underlying graph suffices, but the sentence does not say it. (ii) The gains of single arcs need not lie in the subgroup; "applies with that subgroup" needs a switching first. Wording only.

Computed (challenge_prop_abund_cor_abund.py and four follow-ups; seed 20261113; library REVIEW_QUEUE/lib/pcplib.py)
- 261 carriers built, all with A*A = d exactly; 148 with D-hat strongly connected (hypothesis), among them 55 with a non-cyclic group (Z2xZ2, Z2xZ4, Z2xZ6, Z3xZ3, Z4xZ2), 51 of degree four, 17 with r != r0.
- (a): degrees, r0 | r, the shift is constant, pi is a homomorphism with image r0 Z/r, index of C0 = r/r0: 0 failures.
- (b): 789 pairs, two starting vertices each, every coset: a length exists with gains exactly K at y1 and K u at y2, each at least 25 times: 0 failures. Gains at a vertex within one coset at every length: 0 failures.
- (c): both directions, 0 failures. Last sentence of (c): 34 instances found where a character that is not faithful has all its values at both vertices at one length although r != r0.
- 5.15: q0 >= 2 on 79 cyclic carriers; u u_z' in C0 with zero sum: 0 failures. Squared modulus solves the consistency equations on actual events (12 carriers): 0 failures.
- The paper's four-vertex example for q = 4: A*A = 2, D aperiodic, D-hat strongly connected of period 2; at most two gains at any vertex at any length, forming a coset of the subgroup of order two; exactly two from length 5 on.

Failed predicates (all kept; each traced to the reviewer's predicate, none to the paper)
- K3 (dimension of the solutions of (V) on a box of Z[C0]) failed on 19 carriers with four common successors; K3b on larger boxes failed for q0 = 12 and the multisets with exponents (0,1,6,7), (0,2,6,8), (0,4,6,10), (0,5,6,11): dimension 4 against 2; K3c and K3e on still larger boxes (up to 6561 x 625 pairs): still 4. An exploratory script showed the two extra solutions are concentrated on four unknowns, the largest moduli of the box, which too few equations determine. K3h: the solution space restricted to the moduli of elements with coefficients -2..2 has rank 2 (third singular value 7e-17 against 0.037). So this is an effect of the finite box, as the paper reports for its own runs, and not a counterexample to Theorem 5.12. A diagnostic of mine (K3d, "support 712 of 714" with a cut of 1e-8) was badly designed and is kept.
- N1: see the GAP. X1: I required exactly two gains from length 3; one gain occurs at some vertices at lengths 3 and 4. X1b met.

Not checked: Theorem 5.12 itself beyond its use (it has its own challenger report; I read its three steps and found no failing step); consistency on all events of a carrier for q0 > 6; the counts 660, 483, 130, 473, 110 quoted in the paper; infinite carriers.
