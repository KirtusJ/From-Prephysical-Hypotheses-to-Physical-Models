Target: Director_G/Folded_field_and_native_gaussian.md with its two checkers and result files folded_free_field.json and folded_gaussian.json; commit d509426. Named in the director's note of 13 November (late).
Outcome: GAP (hypotheses and a constant outside the statements, a missing definition, reproducibility; no defect found in the derivations or the reported numbers).
Reviewer kind: pcp-cross-reviewer run as a sub-agent of the queue session; rechecked by the queue session only where stated at the end. Same model family as Director Z; cross-review from shared sources, not independent replication. Director G's files were read, not modified.

Claims of the note (proved in prose, no numbered theorem): the encoding is an on-site isometry; an exact local rule with a conjugate term; a fold identity |Z(q)|^2 + |Z(-q)|^2 = 2||F(q)||^2; a bound ||Z_{t+n} - e^{-i n q^2/2} Z_t|| <= C'Q + n Q^4/6 + 2 e_Q; the alternating-switch word gives sin^m k with yield C(2m,m)/4^m; the Gaussian limit; two closed forms. Computed instances: 0.778054 and -0.320574; a variance 0.997912 growing to 106.737 at m = n = 512. Premises: squared readout, coherent direction copy, the score extended to pointer words.

GAPs
1. Hypotheses of the bound (real rails, support on one parity, unit norm, free ticks, 0 < Q <= 1, ring size divisible by four) are in the surrounding text only.
2. The constant C' is never given in the note; the checker's comment uses 2 sqrt 2. The reviewer measured the relevant supremum as 1.0000 on |q| <= 1, so C' = 2 would do.
3. The walk's definition: the note links a commit (4f3468b) that is not in this clone, and the specification file is not in the tree. The reviewer took the update rule from the checker's code.
4. Wording: "controls arbitrarily many ticks" holds only for one coefficient; the bound itself grows as n Q^4/6.
5. The classical-flight section's "This proves..." rests on Flight_window_preparation.md (cross-reviewed separately, same date); the claim e_Q -> 0 is not verified here.
6. Checkers: they overwrite their result files without warning; their tolerances 1e-10, 2e-11, 2e-13 have no stated basis; the bound is asserted on 12 hand-built cases only. A rerun differs from the stored files in bytes and agrees as data (45 values, largest difference 1.8e-14; 822 values, largest 1.1e-13).

Derivations: the local rule, launch values, the eigenvector, the spectral gap, the fold identity, the bound, the imbalance identity, the closed forms and the variance all follow. The dispersion inequality |omega + pi/4 - q^2/2| <= q^4/6 holds numerically and is tight (ratio 0.99994 on 0.01 <= |q| <= 1); no analytic proof was checked.

Reviewer's program (xfolded_check.py, 18 predicates fixed first, seed 20261113, one thread)
- Local rule exact on 60 of 60 qualifying instances; a ring size not divisible by four violates it, as the condition predicts.
- The bound on 400 of 400 qualifying random instances, n up to 1e6: no violation; only 68 were informative (bound below 2), largest ratio of error to bound 0.62.
- Prepared amplitudes equal the signed binomials exactly for even m = 2..40. Distance to the Gaussian falls by a factor of 4 per step from 0.0262 to 2.5e-5 over m = 8..8192.
- The four reported figures reproduced by direct stepping: 0.7780543, -0.3205742, 0.9979125, 106.7367.
- At sizes not in the note (m = 64 to 4096) all errors decrease; block real parts converge only like m^(-1/2).
Failed predicates, kept: P2 and P3 (launch values, eigenvectors) failed because the reviewer's exact zero test did not reduce certain root-of-unity forms; follow-ups at 40 digits pass (residuals 0 and 2e-41). A defect of the reviewer's test, not of the note.

Lean: the note links no Lean file and none in Director_G/lean concerns it.

Rechecked by the queue session: the result files show P2 and P3 failed in the first run and the follow-ups passed; the commit 4f3468b named in the note is not an object of this clone. Nothing else.
Not checked: the two linked notes and the cited paper; the limits e_Q -> 0 and the concentration claim; the physical premises.
Cost reported by the sub-agent: about 17 minutes, 10 tool calls.
