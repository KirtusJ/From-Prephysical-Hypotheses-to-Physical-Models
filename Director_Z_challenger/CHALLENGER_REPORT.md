# Challenger report on G10 Theorem 5.8 and Corollary 5.9 (edition Z10 draft)

13 November 2026. Written by a sub-agent of the Director Z session (same model family, a separate context). It was given the paper source and the definitions it cites, and no notes of the author. Its instruction was to break the two statements. The text below is its report, shortened only by removing the path of its working directory. Its two programs are beside this file.

**Outcome.** No counterexample to either statement. Four gaps in the wording of the corollary; no defect.

**Steps examined, nothing found:** Theorem (i); the single-walk equation; the count of pairs in the continued event and the identification of the sum with the entry of A*A; the use of linear independence of characters (the hypothesis is strong enough; "of one common length" may be read per quotient); the case f(1) = 0; the case without common successors; that no event mixes starting vertices; Corollary (a), (b), (c).

**Gaps.**

1. Corollary, first sentence: "the other entries off the diagonal are zero" needs the successor pairs of different blocks to be disjoint. The corollary did not assume it. If "fall into blocks" meant only the pairing, the claim about X(D) is false: with two blocks sharing one successor pair, X(D) differed from the characters with chi(eps) = -1 in 10 of 10 carriers for each of 7 groups. For finite vertex sets the hypothesis of part (ii) forces disjointness, so the equivalence is safe there; the unconditional claim needs in-degree two stated.
2. Corollary (d): "a rule that is multiplicative" must be restricted to consistent kernel rules; the constant kernel is multiplicative and is not of the stated form. The product for kernel rules was not defined in the section.
3. The corollary said "a kernel f not zero" where the theorem says "mu_f not identically zero".
4. The proof of the symmetry criterion wrote out one direction only; the proof of (a) reused the letter d.

**Computation.** Own code (`k.py`, `brute.py`): exact reachability of pair states per starting vertex and length; the integer system on even kernels solved in fractions and compared with X(D) computed from the matrices. Groups Z4, Z6, Z8, Z12, Z3 x Z3 x Z2, Z2 x Z2, Z2 x Z4; about 2500 carriers over four seeds (block carriers of degree two, random digraphs of degree two and three, block carriers of degree three). Among carriers with the hypothesis: no mismatch between the solution dimension and the number of conjugate classes in X(D). Without the hypothesis the space was often larger. A direct evaluation of the rule on 300 random events per character on four carriers agreed.

**Not checked.** Infinite vertex sets; degree four; the cited statements of G8 and G9; Corollary (d) by computation; the count of 47 carriers and the author's programs; carriers with more than six vertices.

**Standing.** Same model family as the author, a fresh context, and the author's paper as its only input. This is a second reading with reduced exposure. It is not an independent review.
