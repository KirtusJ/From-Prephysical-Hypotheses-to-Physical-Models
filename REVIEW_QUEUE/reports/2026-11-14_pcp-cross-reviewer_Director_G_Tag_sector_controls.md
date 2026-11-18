Target: Director_G/Tag_sector_controls.md, lines 1-118, with its four checkers and result files and the two Lean files it links; commit 4ad1dec. Named in the director's note of 13 November (late).
PARTIAL: the note has 249 lines at this commit (it had 118 when the item was written). Lines 120-249 were not reviewed; for them only the checkers were rerun and the Lean files read.
Control (known answer): "the sum of the 15th roots of unity whose order divides 5 is zero, and the sum of the primitive 15th roots is 1". Expected TRUE; reported TRUE with exact minimal polynomials. Control passed.
Outcome: GAP (three points; no defect found in lines 1-118).
Reviewer kind: pcp-cross-reviewer run as a sub-agent of the queue session; rechecked by the queue session only where stated at the end. Same model family as Director Z; cross-review from shared sources, not independent replication. Director G's files were read, not modified.

Claims (lines 1-118). Premises: the two-rail walk, a faithful terminal read, a common local routing law, and pure calibration giving h = 1/2 + uv/(u^2 + v^2). Computed: two settings, a cell 0 against 1/24, a cross ratio 6/5, a tick-8 example of the max rule, a tick-9 table, a weighting example. Theorems: finite calibration leaves distinct real-analytic rules; sign-contrast limits; a Taylor bound M/(2 n^2); a pooled-bias limit; a cusp counterexample.

Derivations: all steps follow (rederived by hand and by program).
GAPs
1. The finite-calibration statement (line 59) needs "the line or an unwrapped ring", which appears only at line 72. It matters: on rings of 10 and 12 sites the reviewer's runs differ from the line at ticks 7 and 8.
2. The sign limits and the bound (lines 88-102) use three hypotheses stated only in the surrounding text: homogeneity under positive scaling, a routing law depending only on the signed field at the current site, and pure calibration at the direction (n,1).
3. Summary wording (line 104; true as written): "The first clears this necessary test only". The reviewer measured the actual curvature of the two rules on the relevant segment as about 196.7 and 367.8, so a cap of 6 is violated by both, about 33-fold by the first; the mean test passes the first by a margin of 1/444.
The bound at the note's own parameters (M = 6, n = 6) is 1/12 against a pure excess of 6/37, so it is informative there.

Reviewer's program (xtag_own.py, exact fractions, 15 predicates fixed first, one run, none failed): sector mass equals amplitude squared over 2^t on 679 cells; the tables, the 1/24 cell and the 6/5 ratio reproduced; the max rule equals the sector rule through tick 4 and first differs at tick 8; calibration depths 3 to 12, not in the note, behave as the theorem says in 10 of 10 cases; the relative-sign rule for n = 0..12 (the note's checker stops at 6); the stored result file's 464 cells and 24 panels all equal the reviewer's values.
Checker reruns: all four byte-identical to the stored result files.
Lean (files read, not elaborated: they pin 4.19.0): both are linked only from the unreviewed part. They contain event inclusions on lists and integer inequalities. Nothing in lines 1-118 is formalized, and for the later sections no probability statement is formalized; the title "Lean proof of the deadline and timeout rules" covers the set-inclusion steps only.

Rechecked by the queue session: the control; the four reruns are byte-identical to Director_G/results; the note has 249 lines. Nothing else.
Not checked: lines 120-249; a density result cited from a pull request; the frame-relabel paragraph; Lean elaboration.
Cost reported by the sub-agent: about 14 minutes, 7 tool calls.
