Target: Director_G/Four_tick_force.md with its checkers and the result files four_tick_force.json and prepared_force.json; commit d509426. Named in the director's note of 13 November (late).
Outcome: DEFECT in the evidence and in one summary sentence (not in the theorems), and two GAPs.
Reviewer kind: pcp-cross-reviewer run as a sub-agent of the queue session; the defect was rechecked by the queue session from Director G's stored result file, as stated below. Same model family as Director Z; cross-review from shared sources, not independent replication. Director G's files were read, not modified.

Claims of the note. Theorems: a free four-tick bound D(Q) = 4 sqrt 2 Q^3 + (2/3) Q^4; a forced bound E <= M D(Q) + T Delta |F| L/(2 eps); a weak terminal law Y0 + p0 T - F T^2/2; that (3+4i)/5 has infinite order; a two-squares obstruction; a selector with success probability between 1/8 and 1/2. Computed: 30 periodic trials, a compiler example with k = 8341, two selectors, nine sharp-launch panels.

DEFECT (sharp-launch evidence). In the stored Director_G/results/prepared_force.json, 6 of the 18 rows with a force move the conditional mean position in the direction opposite to the ideal displacement -F T^2/2, measured against the force-free row of the same panel. They are exactly the rows with p0 = +1 and slope -1, and p0 = -1 and slope +1, at all three scales:
  1/delta = 6:  shift -0.683 (ideal +0.318) and +0.546 (ideal -0.318)
  1/delta = 10: shift -0.501 (ideal +0.321) and +0.433 (ideal -0.321)
  1/delta = 14: shift -0.335 (ideal +0.321) and +0.335 (ideal -0.321)
The other twelve rows move in the ideal direction, by 0.19 to 0.36. The note's Checks section does not mention this, and the index line for the note in Director_G/README.md (line 45), "bend the conditional terminal position toward the constant-force Newtonian trajectory", is false at every computed scale for these six rows. The sub-agent's own program finds 10 of 30 such rows, at 1/delta = 8 and 12 as well, and at 1/delta = 20 a mean shift of -0.25.
What this does not show: the limit theorem is not refuted. At these parameters the note's own bound E is between 5.2 and 21.9 (sub-agent's figures), so it asserts nothing there, and it shrinks only like delta^(1/10).

GAPs
1. Nowhere does the note say that its bound is vacuous at the scales of its trials, or that the preparation offset is 0.77 at 1/delta = 14.
2. "A constant offset changes only a global phase" holds in the continuum only; the plate map is real-linear, so the plate's origin matters at finite scale (stored 0.546 against 0.559 with the plate referenced to the launch site).

No finding
- Free bound: every step follows, hypotheses in the statement; 268 qualifying instances, largest ratio 0.473; 112 controls outside the hypothesis kept.
- Forced bound: 207 of 210 instances qualify, largest ratio 0.035; only 57 have a bound below one.
- Integer part: least k = 8341 confirmed at 60 digits, largest site error 0.0036026; the obstruction holds to depth 40.
- Selector: exact for nine denominators.
Checker rerun: equal as data, not as bytes (largest difference 3.3e-16 and 1.1e-14). The numbers quoted in the note match the stored file. One checker overwrites its result file and uses a tolerance of 2e-12 without a stated basis.
Lean: the note links no Lean file.

Failed predicates of the reviewer, kept: A3, A6, B1 in the first run (faults of the reviewer's program: a double cast, a sign in its own exponent, rounding near q = 1e-4; the follow-up passes); G2, the direction of the mean shift, which is the DEFECT.

Rechecked by the queue session, from Director_G/results/prepared_force.json alone: for each of the nine panels the mean position of each forced row minus that of the force-free row, compared in sign with -slope * T^2/2 (the note states V = F Y and force -F). Result: 6 of 18 opposite, with the six shifts listed above. The README sentence is at line 45. Not rechecked: the sub-agent's own 30 rows, the values of the bound E, the offset 0.77, the no-finding items.
Not checked: the window, spread and recovery proofs cited from other notes; the weak-limit step; rings with a seam.
Cost reported by the sub-agent: about 11 minutes, 13 tool calls.
