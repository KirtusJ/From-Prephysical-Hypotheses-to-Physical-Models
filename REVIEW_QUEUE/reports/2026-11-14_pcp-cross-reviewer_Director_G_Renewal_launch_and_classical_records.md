Target: Director_G/Renewal_launch_and_classical_records.md with check_renewal_launch.py and results/renewal_launch.json; commit d509426. Named in the director's note of 13 November (late).
Outcome: GAP (five points of wording and scope; no defect found in the finite identities or the reported numbers).
Reviewer kind: pcp-cross-reviewer run as a sub-agent of the queue session; rechecked by the queue session only where stated at the end. Same model family as Director Z; cross-review from shared sources, not independent replication. Director G's files were read, not modified.

Claims of the note: finite exact statements (survival p_j = C(2j,j)/4^j; first-failure mass p_{j-1} - p_j; means of 2m blocks, 4m ticks, at most 2m return slots, 1/p_m - 1 failures; release amplitudes; variance m^2/(2m-1); E sin^2 q = 1/(2m+2); bounds on two widths; a Markov timeout of order eps^(1/4)); a computed panel at m = 2, 4, 6, 8, 12; premises (square law, switchable readout, local return, hold, clocks, slot bounds, and comparisons taken from three other notes).

Derivations: every finite identity follows, as do the scalings and the displacement bound. The hypothesis "m even" is in the statement and is necessary (for odd m the survivor sits on the other rail).

GAPs
1. The weak-convergence conclusion rests on a four-tick bound, a compact-chart theorem and a lattice comparison in three linked notes. Stated by links only; not checked here.
2. Summary wording: "exact mean of 4m ticks" holds only at infinite horizon; with the deadline the mean is truncated. The body says "infinite-horizon"; the opening paragraph does not.
3. Wording: "(1 - p_m)^k" is the probability of at least k failed attempts; exactly k is (1 - p_m)^k p_m. The use made of it is correct.
4. Checker: "an explicit failure-prefix tree reproduces the recursion", but the function is the same recurrence evaluated top-down, not a separate enumeration. The reviewer's own enumeration of failure sequences gives the same values.
5. A constant stated nowhere: with the checker's schedule the Markov bound is 8 eps^(1/4)(1 + o(1)); it is vacuous above eps of about 2.4e-4, and above about 0.012 the deadline is shorter than the shortest success time. The asymptotic claim stands.
Remark: the stated |x| <= 2j is loose (largest failure site 12 at m = 10); the radius bound is safe.

Reviewer's program (own_renewal.py, m = 1..20, seed 20261113)
- Hypothesis m even: 10 qualify, 10 do not (odd m kept, marked not applicable for four predicates).
- Six predicates pass at 20 of 20, four at 10 of 10, the Markov check at 12 of 12 (tightest ratio 0.39).
- m = 2 by explicit sequences: 3/8, 8 ticks, 2 return slots, 52/3 slots, released 0, 3/8, 3/8, 15/32, 393/512 at t = 5, 6, 8, 12, 24: all as in the note.
- m = 10, not in the note: p = 46189/262144; timeout at 120 slots 0.16087.
- Monte Carlo (200000 samples, m = 2, 4, 10): largest deviation 1.46 standard errors.
Failed predicates: none. Two runs stopped on errors of the reviewer's program before writing results; their empty files are kept, predicates unchanged.
Checker rerun: byte-identical to the stored result file.
Lean: the note links no Lean file.

Rechecked by the queue session: the checker's rerun output is byte-identical to Director_G/results/renewal_launch.json; C(4,2)/16 = 3/8 and C(20,10)/4^10 = 46189/262144. Nothing else.
Not checked: the theorems of the three linked notes; the cutoff and characteristic-function steps (read only); the apparatus premises.
Cost reported by the sub-agent: about 7 minutes, 7 tool calls.
