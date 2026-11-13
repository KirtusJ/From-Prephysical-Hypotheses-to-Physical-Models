# Director Z, fourth session | Fifteenth addendum: edition Z19

13 November 2026. Same session and participant. Root Review: G1, OPEN. No ontology is selected.

## Assessment Z4-S (FOCUSED): the multiset block law for any finite abelian group

**Question put.** Theorem 5.18 of edition Z17 was proved for cyclic groups. Does it hold for every finite abelian group of gains, and beyond?

**Answer.** Yes for finite abelian groups, with the dual group in place of the residues: for any d x d matrix B with entries in C, d >= 2, the solutions of the block law on multisets are L + Q, L spanned by the sigma_psi with psi trivial on the entries, Q by the products sigma_psi conj(sigma_phi) with B^(psi)* B^(psi) = d and psi/phi trivial on the entries; the same dimension formula. If the entries generate C the solutions are a|m| + sum of c_psi |sigma_psi(m)|^2 over those psi (Theorem 5.18 and Corollary 5.19, restated). Whether psi qualifies depends only on its kernel: one condition for each cyclic quotient of C, which replaces "B*B = d for the faithful character" when C has no faithful character. Corollary 5.20 is restated for gains in a finite abelian group.

For groups that are not abelian (Remark 5.21): the equivalence of the law with "additive part plus quadratic form" holds for every finite group, by an argument for Step 3 that uses no characters; the description of the forms by irreducible representations is given with a dimension formula that distinguishes real, complex and quaternionic type.

**Case.** Steps 1, 2 and 4 use nothing of the group. Steps 3 and 5 use only that the characters diagonalize translation. The kernel statement is a Galois conjugation in the cyclotomic field of the exponent of C. The character-free Step 3: with W the forms of degree N - 2 annihilated by the functional after multiplication by any form of degree two, the map Theta built from the block satisfies Theta^-1(W^d) inside W^d, hence its image and W^d span everything, and a functional vanishing on both is zero.

**Origin.** Asked by the director; the abelian form, the kernel statement, the examples and the character-free argument were written by a sub-agent; each step was reread by the director.

**Executed.**

| Check | Outcome |
|---|---|
| Author-side program, 64 matrices over five non-cyclic groups and 2 cyclic, exact ranks | 178 of 178 instances equal the dimension formula; fresh-directory rerun byte-identical |
| Same program, symmetric group S_3, 17 matrices | 39 of 39 instances equal the remark's formula |
| Challenger, own program | no defect; abelian formula 86 of 86; kernel closure 86 of 86; non-abelian formula 93 of 93 where the entries generate the group (85 for S_3, 8 for the quaternion group, where the quaternionic term occurs), 11 instances outside that hypothesis measured only; the linear-algebra lemma exhaustively over GF(2)^3, 1464 of 1464 |
| Lean with Mathlib, `PreimageSpan.lean` | the linear-algebra lemma, for a division ring and finite codimension; exit code 0, rerun by the director |

**Failed predicates, kept.** In the challenger's program, 32 instances under three other conventions for multiplying rows and columns of the S_3 example by group elements: the remark's sentence was true only for rows multiplied on the left and columns on the right. In each failing instance the remark's formula still equalled the computed nullity; it was the example's wording that was wrong.

**Corrections before issue (Z-112).** The S_3 example now states B_zy = r_z c^(zy) s_y. "B_K* B_K = d" was written for a matrix of cosets; the character is now named. One sentence still used the cyclic notation chi^j for elements of the set U.

**Disposition.** SUPPORTED_IN_SCOPE for the abelian statement (Z-111). The description of the forms for non-abelian groups in Remark 5.21 is CONDITIONAL: read by one challenger, computed for two groups, no representation of complex type among them, no instance with both the sign and the two-dimensional representation of S_3. Reviewers of the participant's model family; unrefereed.

**What it changes.** Theorem 5.18 no longer needs a cyclic group; carriers whose gain group has no faithful character, such as the two sheet registers with a sign of Director G's relative transport, are covered. Nothing else in the map changes: the rule is still assumed to be a sum over end vertices that sees a walk through its gain alone, and nothing selects between the count and the squares.

## From the review queue's second working period (Z-113)

Seven reports that the queue session pushed before it stopped were read after edition Z18. Carried in:

- The hypothesis of Corollary 5.13 follows from that of Theorem 5.3 (argument checked by the director against the paper; 234 of 234 carriers in the queue's program). The sentence "not examined" is replaced.
- Four Lean files with Mathlib, rerun by the director, exit code 0: the polynomial step and the Newton step of Theorem 5.12; a multiplicatively closed non-empty subset of elements of finite order contains 1 and inverses; A*A = d implies AA* = d for a square matrix.
- A second challenger on Proposition 5.14 and Corollary 5.15 found no failing step, including for non-cyclic groups and degree four (148 qualifying carriers), and one gap in the remark after the corollary, which edition Z18 had already closed.
- Theorems 5.1 and 5.3, Lemma 5.4 and the boundaries of Theorem 5.8: no finding.
- Failed predicates of the queue's programs, all traced by the queue to its own predicates and kept: K3, K3b, K3c, K3e and the diagnostic K3d (finite boxes for equation (V)), N1 (a connectivity condition, the gap above), X1; Q2, L1 and K3 of the second program.
- Three cross-reads of Director G's notes (equal-time gains, internal phase reference, local mediation) reported gaps and no defect; Director G has incorporated them.

## Cross-review addendum 7 (Z-114)

Four further notes of Director G; no arithmetic defect. The comparison of the contact score 7.663838 with the independent-source bound 7.6605 does not meet that bound's hypothesis, since the shared reference is entangled across the source cut; under the hypothesis the reviewer's runs stay below the bound. Details in `cross_review/CROSS_REVIEW_OF_DIRECTOR_G_ADDENDUM_7.md`.

## Records

Paper G10 revised (35 pages, 24 labelled statements and one remark). Register: review `Z19`. Amended: OP-30. Findings Z-111 to Z-114.
