Target: edition/PAPERS/G10_*/source/body.tex: Theorem 5.1 (thm:quad), Theorem 5.3 (thm:deg2), Lemma 5.4 (lem:par); the reworded Lemma 3.1 and the new proof of Theorem 5.2 of edition Z13; Theorem 5.8 (thm:kernel) at its boundaries. Text of Z15, commit b84056e.
Outcome: NONE FOUND.
Reviewer kind: pcp-challenger + pcp-micro-review, queue session; same model family as the author; paper text only. Not independent review.

Theorem 5.1: c = 2 from one walk; the family of a+1 walks, its vector and the vector of its continuation; the recursion; induction; converse: all follow. Computed: the family for a = 1..10 exact; 1500 random events: solution space of rank 1 equal to n^2 for n = 1..8 (deviation 9e-15); no solution for c in {1, 1.5, 2.5, 3, 4}; with all gains +1, phi(t) = t solves the system exactly.
Theorem 5.3: strong connectivity; blocks; equal residue classes of x and x'; 2n-1 walks give n of equal gain; moduli n+1 and n-1; converse: all follow. Computed: 124 carriers built, 97 satisfy the hypothesis; proof steps hold on all 97 (same cyclic class within every block; for n = 1..4 a length with 2n-1 walks to x and one to x'); 500 random events each: rank 1, n^2 to 2.4e-14, on 97 of 97. Two disjoint blocks (hypothesis violated on purpose): the conclusion still holds there; recorded only.
Lemma 5.4: f(0) = 0, evenness, f(2x) = 4f(x), symmetry, the difference identity, additivity: all follow (and are checked in Lean in the edition). Computed: on a box of Z^2 every solution restricted to {-2..2}^2 is a quadratic form (rank 3, residual 7e-16). On finite groups the law has only the zero solution, so the lemma is vacuous there (17 groups, exact).
Lemma 3.1 as reworded in Z13: the hypothesis and the fixed starting vertex are now in the statement; the program of the first report (same date) tested exactly this form; no new finding.
Theorem 5.2, new proof: the two termwise inequalities and their sums follow; this is the argument of the Lean file of the first working period. "With equality only at t = 1" is true and not needed.
Theorem 5.8 at its boundaries (exact, small cases)
- d = 1, directed cycle, gains in Z3: X(D) is all characters; every even kernel is consistent with c = 1: PASS.
- d = 1 with two vertices pointing to a third: the hypothesis of (ii) fails (no start reaches both at one length), X(D) is empty, and a kernel with f(1) = 1 is consistent with c = 1. So the conclusion of (ii) fails without its hypothesis, as the paper says ("more kernels are consistent"): PASS.
- Trivial group, complete digraph with loops on two vertices: X(D) empty; single walks give the factor 2, the pair event the factor 4; no consistent non-zero rule: PASS (follow-up K3b).
- One vertex with a loop, gains in Z4 or trivial: X(D) all characters, consistent with c = 1: PASS.
No ambiguous wording found at these boundaries. For d = 1 the events from one vertex are single walks, so mu_f sees only f(1); part (ii) then says nothing about the other values of f, and claims nothing.

Failed predicates (kept; all through the reviewer's expectations)
- Q2 required phi(1..6) to occur; the sample reached 1..5. Follow-up Q2b with larger events: met.
- L1 required a finite group with a non-zero solution; there is none. Follow-up L1b records it.
- K3 expected the ratio 3 for the pair event; it is 4 (my arithmetic). Follow-up K3b: met.

Not checked: Theorem 5.1 on the infinite line beyond walks of length 12; Theorem 5.3 on carriers above 10 vertices; Lemma 5.4 on lattices of rank above 2.
