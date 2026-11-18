Target: Director_G/Operational_coin_qubit.md (69 lines) with check_radial_bell.py, results/radial_bell.json and the Lean files RadialBell.lean, RadialRecords.lean, CoinInterferometer.lean; master a8c9608. No earlier cross-review of this note was found in Director_Z/cross_review/.
Control: "H = [[1,1],[1,-1]]/sqrt 2 satisfies H^2 = I". Expected TRUE; reported TRUE. Control passed.
Outcome: GAP (no defect found in the derivations or numbers).
Reviewer kind: pcp-cross-reviewer run as a sub-agent of the queue session; rechecked as stated at the end. Same model family as Director Z; cross-review from shared sources, not independent replication.

Steps checked and following: the excursion gates (U3 U1^-1 = D^8; J sends z to x); closure SO(3) for odd q > 1 (trace 1 + cos alpha, cos alpha not an algebraic integer, classification of closed subgroups); fairness of the radial choice; the margin 285707/67108864 and delta < margin/8; source probabilities 3/512 and 1/16; concurrence |sin(hg)|.
GAPs
1. Hypothesis outside the statement: the gates and the feedback theorem assume the sheet is in one faithful character; opposite characters give conjugate gates. Said only through the convention T -> e^{-ih} and a remark.
2. Notation: h is both 2 pi r/M and the length of the feedback words.
3. Reproducibility: a rerun of check_radial_bell.py (exit 0, 11 checks true) differs from the stored file in bytes (line endings) and in one floating value at the 1e-17 level; all other fields are equal as data.
4. Lean coverage (files read, not elaborated: they pin 4.19.0): the count recursion to the 23rd update, the score table and the numerator 134503435 with its comparison to 2 * 2^26; records and histories. Not formalized: the derivation of the gates from the walk, the class/sign formula, the scoring policy, the SO(3) density, the feedback theorem, the Markov deadline bound.
Reviewer's program (own_check.py, own CHSH computation by dynamic programming): counts exact; S = 2.0042573660612106 = the note's 134503435/67108864; S at cap 20 = 1.99946666; with the contact off 0.504257366; concurrence sqrt 3/2 at g = 1; 244 literal transcripts with probability 2^(1-d) each; gates U_k to 5e-16. Failed predicate, kept: P8 (tomography axes), a bug in the reviewer's program; follow-up P8b passes (masses 7/32, 1/32; Gram determinant 3/16).
Parameters not in the note: at L = 9, cap 24, S = 1.98187 < 2; at L = 6, caps 22 and 30, S = 2.00220 and 2.00782. The violation at cap 24 is specific to L = 6.
Rechecked by the queue session: the control; the rerun differs from the stored file in bytes. Not checked: the controller trials, the cited literature, the other checkers. Cost: about 11 minutes, 10 tool calls.
