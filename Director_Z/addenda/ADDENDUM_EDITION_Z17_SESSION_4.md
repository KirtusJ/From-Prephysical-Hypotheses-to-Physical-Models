# Director Z, fourth session | Thirteenth addendum: edition Z17

13 November 2026. Same session and participant. Root Review: G1, OPEN. No ontology is selected.

## Assessment Z4-R (FOCUSED): the block law on multisets, without the sum

**Question put.** Every result so far assumes that gains of walks with a common end vertex are added before the rule is applied. Can that be derived? Let the rule add over end vertices any function F of the multiset of gains of the walks that end there.

**Answer.** For a cyclic group C, any d x d matrix B with entries in C, d >= 2, and any real F on multisets, the block law (sum over outputs of F equals d times the sum over inputs, for all inputs) holds exactly when F = L + Q: L additive in the counts with a mean-value condition, Q a real quadratic form in the counts that satisfies the law (Theorem 5.18). B*B = d is not assumed. In characters: L is spanned by the sigma_j for which B^(j) is the all-ones matrix, Q by the products sigma_j conj(sigma_k) with B^(j)* B^(j) = d and chi^(j-k) trivial on the entries. If the entries generate C, the solutions are exactly a |m| + sum of c_j |sigma_j(m)|^2 over the j with B^(j)* B^(j) = d (Corollary 5.19). On a carrier with such a block and abundant gains, a consistent rule of this kind is of that form (Corollary 5.20).

**What it changes.** On those carriers, the addition of gains at a common end vertex, through some character, is a consequence for every part of the rule that is not the count. The first-order rule (counting) and the second-order rules (squares) appear together as the only solutions, and Theorem 5.16 and Proposition 4.1 become cases of one statement. Still assumed: events are sets of walks; the rule is a sum over end vertices; it depends on the walks at a vertex only through the multiset of their gains; the carrier, with a block whose entries generate the group and with abundant gains. Nothing selects between the count and the squares, or among the characters. Positivity restricts the coefficients and nothing more is claimed.

**Case.** A polynomial of degree at most two that agrees with F on multisets of size at most two satisfies the law (its defect is a polynomial of degree two vanishing at enough points). A solution vanishing on sizes at most two vanishes, by induction on the size, in the eigenbasis of translation: a nonzero value on a product of N >= 3 eigenvectors forces a triple pairing identity that makes a vector with entries of modulus one vanish.

**Origin.** Conjectured by the director from exact solution spaces on five blocks; theorem in general form (without B*B = d) and proof found by a sub-agent; each step rechecked by the director before it entered the paper.

**Executed.**

| Check | Outcome |
|---|---|
| Director's exploration, five blocks, sizes up to 10 | nullities 2, 5, 2, 2, 9; equal to the character count |
| Author-side program, 62 matrices (18 blocks), exact rank over Q | 216 of 216 instances equal the dimension formula; corollary count 13 of 13; follow-up on six blocks of degree four over C_6, 6 of 6 |
| Non-faithful characters | exist: Fourier block of degree three with a column negated over C_6 has U = {1,2,4,5}; blocks of degree four over C_6 with U = {1,3,5} |
| Challenger, 41 other matrices | no failing step; 118 of 118 instances; five hand-built candidates (cubes, parities) violate the law in 205 of 205 tests; d = 1 controls exceed the formula, 6 of 6 |
| Micro-review, ten boundary cases (q = 1, all-ones, equal columns, j = q/2) | all equal the formula |
| Lean with Mathlib, `MultisetBlock.lean`, ten theorems | exit code 0; rerun by the director; axioms propext, Classical.choice, Quot.sound |

No predicate failed in these programs. One defect of the first program is kept: it stored as its search example a block whose core lies in a subgroup; the follow-up covers the generating case.

**Corrections before issue (Z-104).** The challenger found the director's summary paragraph false without the condition that the entries generate the group (for q = 4 and a real Hadamard block the solutions include sigma_2 and Re sigma_1^2), "squared moduli of summed gains" wrong for characters that are not faithful, "histories" used where the paper's term is walks, "every such rule is consistent" ambiguous, and the claim of a second proof of Theorem 5.16 stronger than what is written. All corrected. The micro-review found that the list of products in the theorem spans and is not a basis; stated. In the same pass the introduction's "every norm-preserving digraph of degree two" received the word "finite", missed in edition Z16.

**Disposition.** SUPPORTED_IN_SCOPE (Z-103), mathematics, unrefereed. Cyclic groups only. The reviewers are sub-agents of the participant's model family.

## Cross-review addendum 6

Three notes of Director G were read by cross-review sub-agents at Director G's request (optical fixed-phase embedding test; local reciprocal fairness; phase-clock preparation). No defect found; gaps of wording, Lean scope, Lean version and reproducibility are listed in `cross_review/CROSS_REVIEW_OF_DIRECTOR_G_ADDENDUM_6.md` (Z-105). Two failed reviewer predicates are kept.

## Register

Review `Z17`. In review Z16 the first group of calls was submitted twice by an operator error of this participant; the register keeps the thirteen duplicate events and the duplicate objection is withdrawn there (Z-106).

## Records

Paper G10 revised (31 pages, 24 labelled statements). Amended: OP-19, OP-30. Findings Z-103 to Z-106.
