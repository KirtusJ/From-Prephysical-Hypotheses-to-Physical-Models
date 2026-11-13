Target: edition/PAPERS/G10_*/source/body.tex, Theorem 5.5 (thm:conj) and Proposition 5.6 (prop:compo), at commit e53742c.
Outcome: GAP (wording, three places; no step of either proof fails).
Reviewer kind: pcp-challenger + pcp-micro-review, served by the queue session; same model family as the author, paper text only. Not independent review.

Theorem 5.5, step by step
- Rules (5.5) are consistent: follows (sigma_j commutes with conjugation; the right side is a function of |alpha| because R embeds in C).
- Realisation of any alpha at x and beta at x' by one event: follows from the hypothesis and -1 = zeta^(q/2).
- Moduli |alpha + w beta|, |alpha - w beta|; substitution beta -> w^-1 beta; parallelogram law on R: follows.
- Extension of B to R tensor R, invariance under zeta, eigenvalue argument, one real parameter per plane: follows. Only invariance under zeta is used for necessity; dependence on the modulus alone is then automatic.
- Dimension phi(q)/2 and uniqueness exactly for q in {2,4,6}: follows (checked for even q <= 400).

GAP 1 (sentence opening the subsection, line 100): "a norm-preserving digraph of degree two needs -1 among its gains [G9], so the order is even." G9 Theorem 4.3 assumes a finite vertex set. Section 2 of G10 allows a countable one, and the paper's own binary tree with all gains +1 is norm-preserving of degree two without -1. The sentence holds for finite carriers, or whenever two vertices share a successor. Theorem 5.5 is not affected: it assumes a block, and then w and -w are both q-th roots of unity.
GAP 2 (statement): "q even" is in the subsection text, not in the statement; "block" is defined through G9 Theorem 4.3 (finite). For a countable carrier the statement needs only: two distinct vertices with a common successor; orthogonality of two columns with two entries then gives exactly two common successors. One clause would make the statement self-contained.
GAP 3 (Proposition 5.6(b), quantifier): the proof needs the multiplicativity hypothesis to hold on at least one pair of carriers satisfying the hypothesis of Theorem 5.5. The statement says "for gain digraphs with gains in the q-th roots of unity", which reads as all and is sufficient; if a reader restricts it to one given carrier without that hypothesis, the proof does not apply.

Proposition 5.6: (a) both directions follow; (b) follows given GAP 3.

Computed (challenge_thm_conj_prop_compo.py, exact arithmetic in Z[zeta], seed 20261113)
- Hypothesis on B_q tested per q = 2,4,6,8,10,12: all six qualify (every (vertex, root) reached by >= 50 walks at length 8..12); A*A = 2 exactly.
- Conjugate rules on 300 random events per q: defect <= 1.8e-13.
- Solution space of the consistency equations on a box of R (every unknown occurs in an equation: 7, 15, 16, 52, 92, 80 unknowns): dimension 1,1,1,2,2,2 = expected; singular-value gap ratio >= 3.8e14 (recorded); each |sigma_j|^2 lies in it.
- N_j linearly independent; N_j multiplicative (500 pairs).
- 5.6(b): identity holds for c = 0 and c = e_j; smallest defect for 2e_j, -e_j, e_j+e_k, (e_j+e_k)/2 is 8.0, and for 100 random c is 3.8 (q = 8, 10, 12, 16).
- Micro boundary cases, all PASS: q = 2; alpha = 0; beta = 0; alpha = beta; complete cancellation; q = 4 and q = 6 one-dimensional; q = 8 with c = (1,3) consistent on events and not a multiple of one N_j.

Failed predicates (kept)
- A1 (5.6(a), "a negative value is found"): failed for q = 16 on 50 weight vectors of the kind (1, -1e-3, 1, 1): the search region (coefficients up to 40) was too small. Follow-up A1b (followup_A1_units.py): products of conjugates of the unit 1+zeta+zeta^2 give an element with phi = -0.988 for each position of the negative weight. Met.
- A1c (same file): failed for q = 8, 10, 12. Cause in my own predicate: the acceptance guard equalled the tested weight 1e-6. It says nothing about the paper. Follow-up A1d (followup_A1_units_2.py) with weight -1e-4: met, phi between -0.029 and -0.014.

Not checked: the product of G8 Section 6 and v_{S1 x S2} = v_{S1} tensor v_{S2} (taken from the statement); carriers other than B_q; the five-sheet values (3 +- sqrt 5)/16; Proposition 8.1 of G8; q > 16.
