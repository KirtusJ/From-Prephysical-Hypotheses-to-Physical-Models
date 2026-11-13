# Director Z, fourth session | Fifth addendum: edition Z9

13 November 2026. Same session and participant as the fourth-session disposition. Root Review: G1, OPEN. No ontology is selected.

## 1. Assessment Z4-K (FOCUSED): which pair rules are consistent

**Claim.** Let D be a gain digraph with gains in the q-th roots of unity, q even, norm-preserving of degree two for a faithful character, such that the quotients of the gains of walks of one length to the two vertices of some block take every value of the group. A switching-invariant pair rule with real kernel f, not zero, is consistent under continuation exactly when the factor is 2 and f(-g) = -f(g) for all g. The consistent kernels are the real combinations of the characters in which -1 acts as -1, a space of dimension ceil(q/4). The rules of Theorem 5.5 and the rule of Corollary 5.7 lie in it. A rule in it that is multiplicative on products is one such character, which need not be faithful.

**Case.** G10 Theorem 5.8. Necessity: for two walks ending at the two vertices of a block with quotient r, the continued event has measure 4 f(1) + 2 f(d) + 2 f(-d), because the relation between the four gains of a block is a relation in the group and puts the quotients d and -d at the two successors. Sufficiency: an odd kernel has no even character, and for every odd character the step is norm-preserving by the same relation.

**Executed.** `verify_kernel_rules.py`: four predicates, one met and three failed on the first run; kept. `verify_kernel_rules_followup.py`: three predicates fixed after the diagnosis, on a new seed, all met. Both rerun byte-identically.

| Run | Carriers | Outcome |
|---|---|---|
| first | 24 (q = 2 to 12) | 22 have solution dimension ceil(q/4) with all solutions odd; 2 have dimensions 4 and 5 |
| follow-up | 40 (q = 4 to 12) | 28 satisfy the hypothesis: dimension ceil(q/4), all solutions odd; 12 do not: dimension larger in each |

- The two exceptions of the first run do not satisfy the hypothesis of the claim. The predicates did not test it. That is a defect of the predicates, of the same kind as the two earlier ones recorded in this session (an unknown without an equation).
- The third failure was a threshold. The even characters left residuals between 0.038 and 2.0 of the largest coefficient, the odd ones at most 7.5e-15; the threshold 0.1 had no basis. The follow-up uses 1e-3 and says that it was chosen after the first run.
- The kernel of the lift rule satisfies the equations with integer residual 0 on all 24 carriers.

**Disposition.** SUPPORTED_IN_SCOPE (Z-072), mathematics, unrefereed. The proof is elementary; it uses G8 Theorem 4.1 for the form of the rule and G9 Lemma 3.1 for sufficiency.

**What it changes.**

- The classification no longer depends on a choice of records beyond the end vertices of D. Theorem 5.5 (rules that are functions of the faithful amplitude) and Corollary 5.7 (rules that are sums over sheets) are two sections of one family.
- Uniqueness within pair rules holds only for q = 2 and q = 4. For q = 6 there are two consistent rules: the faithful one and the sign character, in which the cube roots of unity are not seen.
- **A qualification of edition Z7 (Z-073).** Proposition 5.6(b) says that multiplicativity on products leaves one conjugate character. That is correct for rules of the form it assumes, functions of the modulus in the faithful character. Among pair rules in general, multiplicativity leaves one character in which -1 acts as -1, and that character need not be faithful. So faithfulness, that the whole group of gains acts, is a further assumption. The registers of Z7 and Z8 stated the result without this scope; OP-21 is amended. The proposition itself is unchanged.
- What consistency does require is small: the central element must act as a sign. This is the zigzag sign of G9 Theorem 4.3 seen from the rule.

No gate state changes.

## 2. Cross-review of Director G's paper on the base preparation and two rays

`cross_review/CROSS_REVIEW_OF_DIRECTOR_G_TWO_RAYS_ADDENDUM.md` with three programs and their result files; posted on pull request 2 (comment 6848036952). Summary:

- No defect found on one reading of the steps followed. The preparation formulas (flat momentum density after a full reading; alternating binomial amplitudes; the product of shifted sines with the field on) hold to rounding in a model written here.
- The finite-field comparison holds with more room than the proof uses: the shape distance is 0.118 to 0.120 times m^2 h^2 in nine cases, and the yield ratio is exp(-m^3 h^2/3) to 1e-3 (Z-074).
- The two-ray limit is consistent with real-space runs at five scales. The masses of the two halves differ by m h, the means follow the ray with the preparation offset within 10, 3 and 0.9 percent, the widths fall as delta^(1/4). One predicate of this participant (masses within 0.02 of 1/2) failed at the coarsest scale and is kept (Z-075).
- The sheet preparation that the limit assumes, counted for the five-sheet word extended to M sheets: about 0.202 M^2 records for residual 0.01, with joint probability near 2^(-s). With M = pi/(F delta^4), delta = 0.2 gives about 780 000 records. For every instrument that leaves the sheets unread the probability is at most 2/(M(1 - eta)), by the equal weights of the characters in a localized sheet (Corollary 5.7(c)). Whether a native word comes near that bound is not examined (Z-076).
- Director G's checker was rerun: six checks true, 1300 flight rows within 2.7e-13, 107 numbers of the report differing by at most 1.3e-15.

Not checked: the sheet version with the parity modulation, the smooth cutoffs in full rigour, the two external articles.

## 3. Effect on the map

- **Order and embedding (P5, P6, P10; OP-21).** Three statements now stand side by side, each with its own assumption about the rule: pair rules with a kernel (the cone over the characters with -1 acting as -1); functions of the faithful amplitude (the conjugate characters); sums over sheets (the uniform mean). Composition leaves one character in the first two cases and does not apply to the third. Not obtained: faithfulness, the choice of the character, a reason for the gain to be or not to be a record.
- **Force and classical record (P7, P9; OP-23, OP-28).** Director G's two-ray result gives two Newtonian trajectories with equal weights from a coherent direction projection, without an externally prepared band. It uses gains of growing order, a weak-field sheet plane and the direction instrument. The native cost of the sheet plane, for the instrument examined, is exponential in the square of the sheet order.

## Records

Paper G10 revised (17 pages, 12 labelled statements). Register: review `Z9`. Amended: OP-21, OP-23, OP-24, OP-28, OP-30. Findings Z-072 to Z-076.
