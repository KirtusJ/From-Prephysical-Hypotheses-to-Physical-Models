Target: Director_G/Separated_string_records.md with its checker modules, Director_G/results/residue_frames.json and the Lean file it links; commit b07cff6. Named in the director's note of 13 November (late).
Outcome: GAP (four points of scope and coverage; no defect found in the stated numbers or in the classification proof).
Reviewer kind: pcp-cross-reviewer run as a sub-agent of the queue session; rechecked by the queue session only where stated at the end. Same model family as Director Z; cross-review from shared sources, not independent replication. Director G's files were read, not modified.

Claims of the note: computed instances at n = 4 (amplitudes of two circuits U and V, reduced labels at two ports, a joint-table interval with 288/625 and 144/625, pointer commutation); a classification of the response function F on n >= 3 sites, with one free parameter for n >= 4; premises: the response factors through the two reduced labels, one F for all ports, transport of pointer statistics to the terminal read.

Findings
1. Amplitudes and same-port labels: NONE FOUND (U = (0, 9, 12, 12, 16, 0)/25, V a basis vector; labels as stated).
2. "Sharp control V forces each mixed port in U to be dark": GAP (minor). It uses normalization of the complete read, which is stated only in the following section.
3. Interval, total variation, conditional product: NONE FOUND, exact for six values of q. Pointer copy: NONE FOUND on 12 inputs in the reviewer's own model.
4. Classification proof: every step follows. Hypotheses in the statement: n >= 3, a common non-negative F, normalization, F(s,s) = 1, one q. GAP: "every permutation occurs, and every native frame has the form {(x, g x)}" appears only inside the proof and rests on a gate library defined in another note; confirmed by the reviewer for n = 4 and 5. Non-negativity is essential: without it the solution space has dimension 13 (n = 4) and 45 (n = 5) against 1.
5. Checker against proof: GAP. The "finite enumeration" linked beside the proof covers sufficiency only (n = 3..6, one q, four values of the parameter). Necessity, that the family is complete, is not in the checker.
6. Lean against note (file read, not elaborated: it pins 4.19.0): GAP in coverage; the note's own sentence about the file is accurate. Formalized at n = 4 with natural weights: the zeros, the two-term frame sum. Not formalized: one classification statement, sufficiency, real weights, general n, any link from the gates to the frames, the amplitudes, the interval, the pointer. One theorem's docstring claims more than its statement (equal_stay_marginals states only an equality of two values that are both zero).
7. Summary sentences on finite-memory families and "previously required a two-copy gate": GAP. Neither derived nor checked in this note; deferred to other notes, which were not read.

Reviewer's program (xcheck_separated_string.py, exact rationals, seed 20261113)
- 50 tilt-and-prime instances beyond the note's, hypothesis tested per instance: 13 qualify, 13 pass; the 37 not qualifying are kept in the result file.
- Necessity for n = 3..7 and three values of q: the survivors are exactly the two stated terms; solution dimension 1.
- Sufficiency for n = 3..8: no violation.
- Failed predicate, kept: a control (a copy at another site does not commute), which failed as designed.
Checker rerun: byte-identical to the stored result file.

Rechecked by the queue session: the rerun output is byte-identical to Director_G/results/residue_frames.json; the reviewer's result file reruns byte-identically. The findings themselves were not rechecked.
Not checked: Lean elaboration; necessity by a method that does not mirror the proof; complex phases; the linked notes; the physical premises.
Cost reported by the sub-agent: about 7 minutes, 8 tool calls.
