Target: Director_G/Marker_kernel_from_one_launch.md with its checker, results/marker_replay.json and the Lean file it links; commit 4ad1dec. Named in the director's note of 13 November (late).
Control (known answer, set by the queue session): "the probability that a simple symmetric walk is at its start after 20 steps is 46189/262144" - the sub-agent answered TRUE with the exact computation. Control passed.
Outcome: GAP (no defect found in the derivations or the reported numbers).
Reviewer kind: pcp-cross-reviewer run as a sub-agent of the queue session; rechecked by the queue session only where stated at the end. Same model family as Director Z; cross-review from shared sources, not independent replication. Director G's files were read, not modified.

Claims of the note. Premises (all in running text): blank probabilities D^2/2^t from another note, a sharp source, a conserved marker moved locally, dynamics before a read independent of the planned depth, a universal continuous kernel K invariant under positive rescaling, a same-permutation copy, transfer of K to tagged sectors. Derived: the kernel h; an asymptotic formula for an amplitude; density of directions; K = h on the circle; an induction for the joint law; a Lipschitz bound; non-uniqueness by a bump. Computed: 9/16 against 5/16; counts 18 and 10; gaps and residuals of a 144-point panel.

GAPs
1. The note has no set-off statements, so every hypothesis sits in the running text. None was found stated nowhere.
2. The remainder O(t^(-3/2)) of the asymptotic formula is sketched with a citation, not proved. Numerically residual times t^(3/2) stays between 0.708 and 1.5164 for n up to 1500.
3. The bound e + (L+1) r is never evaluated at the note's own panel. At 12 points r = 0.6014, and with e = 0 the bound exceeds the trivial value 1 for every L >= 0.663, so it says nothing there. At 144 points r = 0.1258: L = 1 gives 0.2517, and the bound is vacuous for L >= 6.95.
4. Wording: "normalized spinor" means scaling by 2^(-t/2) in one place while "normalized direction" means a unit direction earlier.
5. Checker: its "adjacent blank panels" check is true by construction (the successor is built as u + v); "depth at most six" holds in the stored data and is not enforced.

No finding: h and the worked example (9/10; parent mass 5/8; 9/16, 5/16, difference 1/4, midpoint 7/16); the stationary-phase constants, checked by hand and exactly; irrationality, density, K = h by continuity, the induction; the bump alternative. The summary sentences match their rows, signs included (gaps 1.20282 and 0.25169, residuals 0.08845 and 0.00007356). "No extrapolation needed" is correctly limited to the short test: extending the same flight by two ticks produces parent pairs absent from every blank panel to depth 40.

Reviewer's program (xr_marker.py and followup.py, seed 20261113, exact fractions, 50 digits where needed)
- Routing by h equals enumeration of words at every port in 17 of 17 instances (the note's and 16 not in it); all satisfy the hypothesis.
- All four printed numbers reproduced. Gaps at panel sizes not in the note: 0.1950 at 300 points, 0.1054 at 600.
- Failed predicates, kept: P1 (the reviewer's symbolic simplification did not reduce an inverse-trigonometric form; at 80 digits the difference is 1e-81) and P4 (the reviewer's predicate was stricter than the O-claim: the supremum over a later range is 1.516443 against 1.516312 earlier; block maxima to n = 1500 stay bounded). Both are faults of the reviewer's tests.
Checker rerun: equal as data, not as bytes (15 floating values differ, by at most 5.6e-17). The checker refuses to overwrite its result file.
Lean (file read, not elaborated: it pins 4.19.0): formalizes the two-output step, the replay step and its induction, and a tagged replay. Not formalized: h as a ratio, the normalization, the example's numbers, stationary phase, density, continuity, the Lipschitz bound. The note's sentence about the file matches, and it discloses most of what is not formalized.

Rechecked by the queue session: the control's answer; that the checker's rerun differs in bytes from the stored file; that the gap figures 1.20282 and 0.25169 appear in the note. Nothing else.
Not checked: Lean elaboration; the cited literature; the specification the note builds on; a proof of the remainder.
Cost reported by the sub-agent: about 15 minutes, 9 tool calls.
