run1: crashed in my own program at P11 (keyword clash 'ok'), before any result file was written; variable renamed, predicates unchanged.
run2 (result/xr_string_result.json, not overwritten): 11 met / 1 failed (P5, kept) / 5 measured.
- 49/625 = ordinary two-hop return (amplitude -7/25); 1 = two-prime return. Both exact, n=3,4,5, 40 instances.
- P5 FAILED (kept): two-prime == ordinary on 132 of 300 random words; equality holds only for single hops from localized inputs (P1 128/128). Note claims only that. Follow-up: none needed; wording of lead "(b)" is consistent.
- Unreported: n=7 Lie rank 441=21^2; returns m=3,4; tilt (5,12,13): both reductions identity, 9/16 mixture gives stay 1 vs 25/169 (construction is specific to 3-4-5; note says other coefficients may change reductions).
- Author checkers rerun from copy: string_control.json and string_readouts.json byte-identical to stored.
- Lean 4.19.0 StringControl.lean: exit 0, no sorry, axioms propext/Classical.choice/Quot.sound. Formalizes only the integer layout identity and the edge contrast.
- GAP: lead sentence (d) omits certainty-calibration premise, exact signed swaps, d>=3, Gleason.
- GAP: closure of positive-word semigroup is a group (compactness) used, not stated.
- 5.28/5.29: two-prime rule is not a history-event rule; no conflict.
