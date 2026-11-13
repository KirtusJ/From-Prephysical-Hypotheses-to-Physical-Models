# FINDINGS (attacker: sub-agent of the author's model family; not independent review)

## alt_rules.py (first run, result alt_rules_result.json) : 7 of 8 predicates
- P1-P5, P7, P8 pass. P6 FAILED and is kept: ALTGAIN (minus sign moved uniformly to the R->R arcs) is
  identical to the model on every event of length <= 4 (a switching of the gains), so it does not violate S3.
  Follow-up: alt_rules_followup.py searches non-uniform signings.
- COUNT, MIX violate only S5. NEG = (37/5)||v||^2 - (32/5)|S| violates only non-negativity and meets S5 literally (R_10 = 1).
- UNNORM = (1/2)|S| + (30719/32768)||v||^2 violates only normalization, R_24 = 1.
- GRAM = v^T G v violates only additivity over end vertices; same P_t(y) as the model.
- LOCAL (square at x0, count elsewhere) violates only S2.

## alt_rules_followup.py (result alt_rules_followup_result.json) : F1, F2 pass
- 24 of 24 single-site re-signings are norm-preserving. 4 of them differ from the model on events of length <= 3 and are
  not functions of the model's gains: site0_RL, site7_LR (exact return R_12 = 1), site0_LR, site1_RL (no exact return
  up to t = 4000, max 0.99637 at t = 2568).
- site0_RL: minus sign at site 0 on (0,R)->(7,L) instead of (0,L)->(7,L). P_3: (1,R) 0, (7,L) 1/2, others 1/8: the mirror
  image of the model's table. Passes S2, S3 additivity, S4, S5. Caveat: it is the model's rule on another S1 carrier.

## return_times.py, first run: CRASHED (kept on record)
- AttributeError in the minimal-polynomial step (int 0 divided by 2 became a float). No result file was written.
  Fix: one line (`Fr(x)/2`). Predicates unchanged. Second run below.

## return_times.py, second run (result return_times_result.json) : 4 of 6 predicates
First t with R_t = 1 / first t with R_t > 0.99, signed ring, x0 = (0,R), TMAX = 100000:
N=3: never / 38; N=4: 8 / 8; N=5: never / 264; N=6: never / 38; N=7: never / 504; N=8: 24 / 24;
N=9: never / 95946; N=10: never / 264; N=11: never / NOT REACHED by 100000; N=12: never / 6416.
- Q1 pass (8 and 24 reproduce). Q2 pass. Q3 pass: for N not in {4,8} the relative minimal polynomial of U^2 at e_x0 has a
  non-integer coefficient, so "never" is proved for all t, not only to TMAX; for N = 4, 8 it is integral.
- Q4 FAILED, kept: N = 11 does not exceed 0.99 within 100000 steps. Follow-up not run (budget).
- Q5 FAILED, kept: on N = 4 the return weight with the end vertex also recorded at the midpoint t = 4 is exactly 1
  (the walk is at one vertex with certainty at t = 4, so that record disturbs nothing). On N = 8, t = 24: midpoint
  record gives 1/4, a record at every step gives 2049/16384, no record gives 1. So the predicate "a midpoint record
  always lowers the return" is false; it does on N = 8.
- Q6 pass: on N = 8 the classes "at y at length 2 and at z at length 3" sum over y to 1/4 at (1,R) and 1/4 at (7,L),
  while P_3 = 1/2 and 0. The end-vertex distributions at lengths 2 and 3 are not marginals of one distribution.
