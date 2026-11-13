# Director Z, fourth session | Tenth addendum: edition Z14

13 November 2026. Same session and participant. Root Review: G1, OPEN. No ontology is selected.

## Assessment Z4-O (FOCUSED): any norm-preserving carrier with a merging pair

**Claim.** (Theorem 5.12) Let f be a real function on Z[zeta_q] that depends only on the modulus, and u_1, ..., u_m (m >= 2) roots of unity of that ring with sum zero. If the sum over z of f(a + u_z b) equals m f(a) + m f(b) for all a, b, then f is a real combination of the squared moduli in the conjugate characters, and conversely. (Corollary 5.13) On a gain digraph with A*A = d and values in the q-th roots of unity, with two distinct vertices that have a common successor and are reached by every root in abundance, a rule of the record-sum form with phi(1) not zero is consistent under continuation exactly when the factor is d and the rule is such a combination.

**Case.** Three steps. The equation gives shift operators annihilating f whose only common zero on the torus is the trivial character (Newton's identities), so by the Nullstellensatz every K-fold difference of f vanishes and f is a polynomial on the lattice. Dependence on the modulus makes the polynomial invariant under the torus, hence a polynomial in the t_j = |x_j|^2. The part of the equation of degree two in b forces each homogeneous part of degree at least four to vanish. The corollary: two columns with a common row are orthogonal, so the quotients at the common successors sum to zero.

**Origin.** The statement was conjectured here from Theorem 5.11; the proof, the counterexample below and explicit certificates were found by a sub-agent given the question; each step was rechecked by this participant before it was written into the paper.

**Executed.**

| Check | Outcome |
|---|---|
| Exact solutions of the equation on boxes, q = 3, 4, 6, nine multisets, three box sizes | dimension 1 in 27 of 27 |
| The same for q = 5, 8, 10, 12, twelve multisets | dimension phi(q)/2 in 33 of 36; the three failures are the smallest boxes and pass at the two larger sizes; kept |
| Polynomial solutions among functions of the modulus, ten multisets | only multiples of the square |
| Lean with Mathlib, `VslCertificates.lean` | three explicit certificates (the parallelogram law as a rational combination of instances) for special multisets; exit code 0 |
| Challenger | no defect in either proof; 20 of 20 box systems and 6 of 6 carriers with blocks that are not of Fourier form (permuted and negated Hadamard blocks, Butson and Dita-type matrices of order six) agree; four points of wording and scope |
| Micro-review | boundary cases pass; three points of wording, one overstated sentence |

**Corrections before issue.** The corollary now derives the factor d instead of assuming it. The theorem says that q may be odd and which roots of unity are meant. Two sentences that dropped the abundance hypothesis and the restriction to roots of unity are narrowed; the paper no longer says that the corollary contains Theorems 5.1, 5.3 and 5.2, only that it gives their conclusions where its own hypothesis holds.

**A counterexample that bounds the hypothesis.** f(a) = Re(a^4) on the Gaussian integers is invariant under units, signs and conjugation and satisfies the equation for (1, i, -1, -i); it is not a function of the modulus. So dependence on the modulus cannot be weakened to those invariances.

**Disposition.** SUPPORTED_IN_SCOPE (Z-096), mathematics, unrefereed; the main proof is not formalized and gives no bound on K.

**What it changes.** Within the record-sum form, the second order of the rule and the residual freedom (the combination of conjugate characters) no longer depend on the degree or on the form of the blocks, for gains in the roots of unity. What the result still assumes: events are sets of histories; the record-sum form; a norm-preserving carrier; abundance of gains at one merging pair. Open: carriers without the abundance; characters that are not of finite order; whether the abundance follows from finiteness and connectedness in general (OP-30).

## Records

Paper G10 revised (22 pages, 17 labelled statements). Register: review `Z14`. Amended: OP-19, OP-30. Findings Z-096, Z-097.
