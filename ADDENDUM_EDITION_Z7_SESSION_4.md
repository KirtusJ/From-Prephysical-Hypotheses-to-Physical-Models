# Director Z, fourth session | Third addendum: edition Z7

13 November 2026. Same session and participant as the fourth-session disposition. Root Review: G1, OPEN. No ontology is selected.

## 1. What changed in the conditions of the session

The principal stated during the session that a second director works on the same repository, with full rights for both to change it, and directed cooperation. Director G (Codex) made contact on the review thread of pull request 1 and published research supplements as pull request 2 (commit b626c0d). From this point the stack has two participants of different model families. They share the baseline, the papers G7 to G10 and the conventions; each has read the other's text. Exposure between them is total and their agreement is not replication (Core 4.2, 4.3).

## 2. Corrections to paper G10 after Director G's cross-reading

Director G read Proposition 4.1 and Theorems 5.1, 5.2 and 5.3 in edition Z5 and reports that the four arguments hold within their stated hypotheses. Director G also found the following, each checked here before it was acted on.

| Point of Director G | Check made here | Effect |
|---|---|---|
| The summary of Section 5 ("on any branching norm-preserving carrier it is the only consistent power") is false: on the countable directed binary tree A*A = 2, there is branching, and every power is consistent | Verified by hand: distinct vertices have no common child, so the columns are orthogonal with squared length 2; from the root every walk is the only walk to its end vertex, so every event has measure equal to its number of walks and continuation doubles it | REFUTED_IN_SCOPE for the summary sentence (Z-063). Theorem 5.2 itself carries the merging hypothesis and stands. The sentence, the list of assumptions in Section 8, the ledger of GH-1 and the trials README are corrected; the tree is cited in G10 with attribution. The same wording in the fourth-session disposition (section 2.2: "a branching norm-preserving carrier") is wrong in the same way; that record is not rewritten, this addendum supersedes it on the point |
| For q = 2 the dimension is one, not phi(2)/2 | Theorem 5.5 as issued states "dimension one for q = 2"; the abstract, the introduction and this participant's message on the thread did not | wording corrected in the abstract and introduction |
| To realize a prescribed pair of amplitudes the multiplicities at the two vertices must be available at one common length | Theorem 5.5 as issued requires "a length at which" both hold; the example B_q has a loop at every pair (vertex, gain) with the first vertex and is strongly connected, hence aperiodic | no change to the theorem; noted |

This is the fourth error of an edition found by another Director and not by this participant's self-check (three in Z1, one in Z2, now one in Z4 to Z6), against none found by self-check alone in issued text. It remains an observation, not a measurement.

## 3. Assessment Z4-I (FOCUSED): positivity and composition

**Claim.** A consistent rule of the record-sum form for gains in the q-th roots of unity is non-negative exactly when its weights are; if it is multiplicative on products of carriers it is zero or the squared modulus in exactly one conjugate character.

**Case.** G10 Proposition 5.6. (a) The lattice Z[zeta] has dense rays in the sum of planes. (b) With M_j(S) the conjugate measures, multiplicativity reads sum_j c_j M_j M_j = sum_{j,k} c_j c_k M_j M_k and the M_j are independent, so c_j c_k = delta_jk c_j.

**Executed.** `verify_composition_selects_one_character.py`, four predicates fixed before the run, all met on the first run (q = 8, 10, 12): the conjugate measures have rank 2; unit weights are multiplicative to 4e-16; weights (1/2, 1/2), (1, 1), (2, 0), (1, -1) have defects 0.50 to 2.0; weights (1, -0.2) give a negative value on sampled moduli and (1, 0.2) do not.

**Priority.** Part (b) coincides in conclusion with the classification of Director G, which was issued first (commit b626c0d, 07:47 UTC; this participant's statement of (b) on the thread followed within a minute and was written without sight of it). The premises differ: a marginal test on records there, consistency on histories here. G10 says so.

**Disposition.** SUPPORTED_IN_SCOPE (Z-064), mathematics, unrefereed; part (b) agrees with a result of another participant reached from different premises.

## 4. Cross-review of Director G

`cross_review/CROSS_REVIEW_OF_DIRECTOR_G.md`, with its two programs and result files. Summary: the nine result files of Director G's four checkers were reproduced on another platform (exact outputs identical apart from line endings; floating outputs to 1.5e-6 relative; no predicate changed). The field-embedding classification and the spinor bound with its position law were read step by step without finding a gap, and each was checked by a route that imports nothing from Director G: an exact nullspace computation for the classification (dimension phi(M) for M = 3, 5, 7, 9) and a real-space walk for the bound (three runs, largest ratio of distance to bound 0.011). One predicate of this participant's check failed through double-precision cancellation and is kept; the follow-up in 60-digit arithmetic holds (Z-061, Z-062, Z-065).

## 5. Effect on the map

No gate state changes. What the two lines of work now say together, each conditional on its own premises:

- **Order and embedding (P5, P6, P10; OP-19, OP-21).** Consistency on histories forces the second order (Z); the consistent rules are the combinations over conjugate characters (Z); composition leaves one character (G first, then Z from other premises); a localized sheet with native operations cannot choose among the characters (G); three kinds of added control could (G). What selects the ordinary embedding from the carrier is not identified by either participant.
- **Force and classical record (P7, P9; OP-23, OP-26, OP-28).** Near a band edge a linear gain gives a constant-force Schroedinger envelope with a proved bound and, for a shrinking packet, weak convergence of the position law to a Newtonian trajectory (G; bound checked by Z). An exact force of size 2 pi / n needs gains of order at least n (Z), so the limit uses gains of unbounded order, for which the measure depends on the character unless the embedding is fixed: the two open items meet here. Over a full Bloch period the centroid follows the packet-averaged ray with a first-order remainder in instances only (Z); no bound (OP-26 open, as G states).

## 6. Layout

From this edition the repository holds the current edition as an unpacked tree in `edition/` and no new archive; Director G was told on the thread before the change. The archive of edition Z3 stays as the principal committed it.

## Records

Paper G10 revised (13 pages, 10 labelled statements). Register: review `Z7`. Amended: OP-21, OP-23, OP-24, OP-26, OP-30. Findings Z-061 to Z-066.
