# Director Z, fourth session | Twelfth addendum: edition Z16

13 November 2026. Same session and participant. Root Review: G1, OPEN. No ontology is selected.

## Assessment Z4-Q (FOCUSED): the block law, without the modulus

**Question put.** The results so far assume that the rule adds over end vertices a function of the modulus of the summed gains. Does gauge invariance alone (invariance under the unit phases that switching produces) suffice?

**Answer.** More than that. For a d x d block B of roots of unity with B*B = d, d >= 2, and ANY real function Phi on Z[zeta], the block law (the sum over outputs of Phi equals d times the sum over inputs, for all inputs) holds exactly when Phi is a real quadratic form invariant under the entries of B (Theorem 5.16). If Phi is invariant under all roots, or the entries generate them, Phi is a combination of the conjugate squared moduli. On a carrier with a full block and abundant gains, a rule that adds over end vertices any function of the summed gains, vanishing at zero, and is consistent with factor d is such a form; with switching invariance it is a combination of the conjugate squared moduli (Corollary 5.17).

**Case.** Elementary. A mixed difference in two inputs and a shift along one output give vanishing threefold differences with one step in dR, so Phi is a polynomial of degree at most two on each coset of dR. The identity then holds for polynomials on each vector of cosets; parts of degree zero and one vanish by a maximum argument; the parts of degree two are equal on all cosets and commute with the entries.

**Origin.** Asked by the director as a question about gauge invariance; theorem and proof found by a sub-agent; each step rechecked by the director before it entered the paper.

**Executed.**

| Check | Outcome |
|---|---|
| Exact solutions of the block law on boxes, twelve blocks, unknowns per gauge orbit and per element | dimension equal to that of the invariant forms in every run |
| Homogeneous polynomial solutions of degrees one to six, fourteen blocks | none outside degree two; 84 of 84 |
| Predicates that expected two-input equations to suffice | four failed, as they should (the cubic for the Fourier block of degree three); kept |
| Lean with Mathlib, `GaugeBlock.lean` | two steps of linear algebra; exit code 0 |
| Challenger | no failing step in the theorem; own exact solution spaces on four blocks with no symmetry assumed agree; functions quadratic on each coset and different between cosets do not survive |

**Corrections before issue (challenger).** The corollary needs Phi(0) = 0, because the rule sums over all vertices; stated. "Every norm-preserving digraph of degree two consists of blocks" needed "finite"; the sentence on removing the modulus needed the abundance hypothesis; the step from vanishing threefold differences to a quadratic polynomial is now given (Z-102).

**Disposition.** SUPPORTED_IN_SCOPE (Z-101), mathematics, unrefereed; the main proof is not formalized.

**What it changes.** For finite norm-preserving carriers of degree two with abundant gains, the form of the rule is reduced to: a sum over end vertices of a function of the summed gains. That the function is of the modulus, and of the second order, are now consequences (with switching invariance for the first). What remains assumed in this line: events are sets of histories; gains with a common end vertex are added; end vertices are records over which the rule adds; the carrier.

Bounds on the hypotheses, each with an example in the paper: two-input events do not suffice in degree three; invariance under all roots cannot be dropped when the block's entries generate a proper subgroup; degree one forces nothing but invariance.

## Records

Paper G10 revised (26 pages, 21 labelled statements). Register: review `Z16`. Amended: OP-19, OP-30. Findings Z-101, Z-102.
