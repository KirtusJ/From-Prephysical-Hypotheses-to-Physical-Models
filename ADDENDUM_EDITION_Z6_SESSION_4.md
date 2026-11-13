# Director Z, fourth session | Second addendum: edition Z6

13 November 2026. Same session, same participant, same limits as the fourth-session disposition. Root Review: G1, OPEN. No ontology is selected.

## Subject

Edition Z5 left open whether the square is forced for gains that are not real (finding Z-056: ten agreeing instances of order four, no proof). The question for this addendum: for gains in the q-th roots of unity, which rules of the record-sum form are consistent under continuation?

## Assessment Z4-H (FOCUSED)

**Claim.** On a degree-two norm-preserving carrier with gains in the q-th roots of unity (q even), under a growth hypothesis on one block, the consistent rules are exactly phi(|alpha|) = sum over conjugate characters of c_j |sigma_j(alpha)|^2. They form a space of dimension phi(q)/2, and the rule is unique up to a factor exactly for q = 2, 4, 6.

**Case.** G10 Lemma 5.4: a real function on an abelian group that satisfies the parallelogram law is a quadratic form (proof included; the group is a lattice, so the usual argument by halving is not available). G10 Theorem 5.5: one block gives the parallelogram law on Z[zeta]; the quadratic form is invariant under multiplication by zeta; the invariant forms are the combinations of the Euclidean norms on the planes of the conjugate embeddings; conversely each conjugate squared modulus is the rule of a conjugate character, for which the step is still norm-preserving. The hypothesis holds on the two-vertex carrier with step matrix [[1, zeta], [1, -zeta]] (the digraph of pairs of a vertex and a gain is strongly connected with a loop).

**Executed.** `verify_cyclotomic_modulus_rules.py`, four predicates fixed before the run, all met on the first run: exact arithmetic in Z[zeta]; solution dimension 1, 1, 1, 2, 2, 2 for q = 2, 4, 6, 8, 10, 12, each containing every conjugate squared modulus (defect below 3e-14); for q = 8 the rule of sigma_3 differs from the squared modulus by more than half its value on sampled moduli, and the fourth power violates the equations. Rerun in a fresh directory: result file byte-identical.

**Challenge and resolution (SELF_CHECK with exposure).** *The hypothesis may fail on other carriers.* Then the solution space can only be larger; the theorem is stated under the hypothesis and one carrier satisfying it is exhibited for each even q. *A combination with unequal weights might be excluded by something else.* Not examined: positivity of the rule on all moduli, and compatibility with products, are entered under OP-30. *Odd orders.* Excluded for degree two by G9 Theorem 4.3; nothing is claimed for higher degree.

**Disposition.** SUPPORTED_IN_SCOPE (Z-058), mathematics, unrefereed, one participant. Finding Z-056 of the first addendum is superseded: for gains of order four the square is forced, as the case q = 4. The favourable reading "consistency on histories selects the squared modulus of the given character": REFUTED_IN_SCOPE for every order other than 2, 4, 6 (Z-059; checked contrary evidence: the conjugate rules and the solution dimensions).

## Effect on the map

Consistency on history events forces the order of the rule and stops at the choice of embedding. This is the ordering-of-values obligation (OP-21) met from a second side: G7 Proposition 7.4 and G8 Proposition 8.1 showed that algebraic data do not fix the values; Theorem 5.5 shows that the requirement which fixes the order does not fix them either, and that the orders 2, 4, 6 are exactly where it does. No gate state changes; evidence under P5 and P10 is amended.

## Contact with Director G

The principal informed this participant during the session that another director works on the same repository. Director G (a Codex participant) wrote on the review thread of the program (pull request 1 of the repository, comment 6847136370, 13 November 2026, 07:40 UTC), stating two lines of work: which measurement assumptions select the ordinary embedding of algebraic amplitudes, and a controlled constant-force Schroedinger and classical limit of the signed walk; and reporting an instance on five sheets with three-step values (3 + sqrt 5)/16 and (3 - sqrt 5)/16 under two embeddings. This participant replied on the same thread (comment 6847160354) with the claim of Theorem 5.5, its executed check, the results of G10 Sections 6 and 7 that bear on a force limit, the baseline and the identifiers in use. Director G's instance and results were not inspected; they are quoted in G10 Section 5.3 as communicated. A comment on a thread is a claim by its author (Core 15.5); nothing of Director G's is counted here as support.

## Records

Paper G10 revised (12 pages, 9 labelled statements). Register: review `Z6`. Amended: OP-19, OP-21, OP-30.
