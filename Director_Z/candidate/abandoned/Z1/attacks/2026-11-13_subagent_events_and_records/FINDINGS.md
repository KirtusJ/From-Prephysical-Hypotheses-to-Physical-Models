# Findings log: attacks on S2 (W1) and S3 (W2) of candidate model Z1

Attacker: a sub-agent of the model author's family (Claude). This is not independent review.
Instance: Z1-R, start (0,R). "Unwrapped" = ring so long that nothing wraps; N=3 = ring of 3 sites.
All arithmetic exact (integers; python-flint ranks and nullspaces; every nullspace checked against every equation).

## Programs and result files (none overwritten)
- ev_classify.py -> ev_classify_results.json (smoke run: smoke_M17_M18.json; log run1.log)
- ev_compare.py -> ev_compare_T4.json, ev_compare_T6_nob.json (log cmp6.log)
- ev_interior.py -> ev_interior_T5_b.json, ev_interior_T6_cheap.json, ev_interior_T7_cheap.json, ev_interior_T8_uni.json, ev_interior_T6_b2_uni.json (logs int5b.log, int6.log, int8.log, int6b2.log)
- ev_extra.py -> ev_extra_a_T7.json, ev_extra_a_T8.json, ev_extra_b1_T8.json
- ev_records.py -> ev_records_T5.json; the T=6 run was interrupted (too slow in mode per): its completed lines are in ev_records_T6_partial.log, no result file.
- ev_quantum.py -> ev_quantum_results.json
- ev_linegraph.py -> ev_linegraph_results.json

## Method note (what the dimensions mean)
At a finite truncation T (events of lengths 0..T, continuations to T+1) even the model's full demand leaves more than two rules, because the multisets of the last lengths occur in few equations. So every family is compared with the model's own demand at the same T: V_all = rules consistent on all events, V_fam = rules consistent on the family; "excess" = dim V_fam - dim(V_all restricted to the family's multisets); "interior excess at depth L" = the same after projecting onto multisets first occurring at length <= L.
Mode uni = one function per rail (independent of x); mode per = one function per vertex.

## Failed predicates (kept)
- P1, P3, P10 (ev_classify): mis-specified. At lengths <= 2 only one-walk multisets occur, so count and square coincide and "projected dimension 2" cannot hold. Follow-up: ev_compare, ev_interior, ev_records.
- P2 (ev_classify): predicted model span 3 with no extra on the unwrapped line in mode per. False: interior dimension 5 against 3 (ev_records_T5.json). The unwrapped line is an infinite carrier and has further first-order rules (W5 territory, not my target). On N=3, mode per, the interior dimension is 2.
- Q7 (ev_compare): predicted two reads leave an excess at T=5. False: excess 0. This is in the model's favour.
- S6 (ev_quantum; the task's expectation): "full event weight differs from the sum over z of through-z weights". False, as I expected: both equal 2^t (norm preservation). Follow-up S7 (end-vertex events) passes.
- X2 at T=8 (ev_extra_a_T8.json): passes formally, but the rule it prints contains an admixture of the count rule (count minus square vanishes on single walks), so it is not evidence of a rule outside D1. The T=7 rule (ev_extra_a_T7.json) is free of this; a separate exact check showed its restriction to lengths <= 5 lies in the projection of V_a(8) and is independent of count and square there.
- Blemish: ev_quantum.py S2 contains a dead branch commented "thin the enumeration"; it does nothing; all 725808 outcome sequences were checked.

## Attack A (S2, W1): dimensions, mode uni, unwrapped
Baseline (all events): interior dimension 2 (count, square) at every depth L <= T-1, T = 3..8.
Excess over the model's demand (interior, depth L, truncation T):
- b  = vertex product events (a set of vertices prescribed at every time): 0 at every depth including the last, T = 3, 4, 5 (315376 events at T=5), both modes.
- b2 = two reads: 0 at every depth, T <= 5; T = 6 (563535 events): 0 for L <= 6, 1 at the last depth.
- bpos = position product events: 0 for L <= T-1 (T=5,6); 1 to 3 at the last depth.
- b1 = one read at one time: L<=5: 0; L=6: 3 (T=6), 3 (T=7), 2 (T=8). End-vertex distributions of lengths <= 6 are nevertheless forced into the model's two-parameter family at T=8 (ev_extra_b1_T8.json: 2 = 2).
- b1pos: L=6: 4, 3, 3 (T=6,7,8).
- a  = end-vertex events (one step of continuation): L=5: 2, 1, 1, 1 (T=5..8). Persistent.
- apos = end-position events: L=4: 2 at T=5..8. Persistent.
- bs = product events with single-vertex reads: L=4: 1 at T=5..8. Persistent.
- c  = cylinders: L=4: 4 at T=5..8; L=5: 9. Persistent.
Explicit extra rule for family a (ev_extra_a_T7.json): F = square + (1/1152) delta, delta on multisets (plus count, minus count): F_L(3,1): -288, F_R(4,0): +288, F_R(2,2): +288, F_L(2,4): -288, F_R(3,3): +288 at lengths <= 5 (24 non-zero values in all, the rest at lengths 6 to 8). Non-negative, single walk weight 1, satisfies all 17267 end-vertex equations to length 7. Its end-vertex distribution at t=5: (-1,R) and (1,R): 1/128 each (model 0); (3,R): 65/128 (model 1/2); (-3,L),(-1,L),(1,L): 15/128 (model 1/8); the four outer vertices 1/32. Sums to 1.

## Attack A (ii): against quantum sequential measurement (ev_quantum_results.json)
- Every vertex product event at t <= 4 (725808 outcome sequences): model weight = ||P_{A_t} A ... P_{A_1} A e_0||^2 exactly.
- 424 product partitions (all sets of read times, single-vertex and single-position outcomes, t <= 5, plus 300 random coarse ones): cell weights sum to 2^t; no cell exceeds 2^t.
- Events with weight above the total: t=3: 2 of 255 (max 9/8); t=4: 1351 of 65535 (max 25/16). None is a product event (159 product events at t=3, 4287 at t=4, maximum exactly 1).
- Post-processed records: read the vertex at every time (t=3; eight outcome sequences of probability 1/8). For a set E of outcome sequences quantum mechanics gives |E|/8; the model's weight of the union differs for 96 of the 255 sets; "anything but R,L,L": quantum 7/8, model 9/8.

## Attack B (S3, W2)
Consistent rules for ALL events (the model's S2), by choice of records and of what the rule sees:
- records = position only: mode uni, T=4 exhaustive (65809 events): dimension 1, count only; square over positions inconsistent. Mode per: unwrapped 2 (count, x*count), N=3: 1. Seeing (gain, previous rail) as well: still 1.
- records = (position, rail), the model: interior dimension 2 (count, square); N=3 mode per: 2.
- records = (vertex, last arc): interior dimension 1, count only, to depth 6 at T=6 (uni, partial log) and depth 5 at T=5 (uni; N=3 per); arc-indexed square inconsistent.
- records = vertex, rule sees the multiset of (gain, previous rail): interior dimension 2 to depth 5 at T=6 (uni): no new rule. 'sqprev', 'crossprev', 'countprevR' inconsistent.
- Line digraph L(D) (ev_linegraph_results.json, N=3,4,5): satisfies S1; its walks from the arc into x0 are the walks of D with the same gains (t <= 6); A*A = 2 for neither character. So D1 applied to L(D) gives a|S| only, S4 gives a = 1, and the return weight is <= 1/2: S1 to S5 have no solution on L(D), which carries the same histories and gains as D.
- W2: full event = sum over z of through-z events for every s < t <= 5 (both 2^t). End-vertex events: 36 violations at t <= 5, none at t <= 2; smallest t=3: y=(-1,L): weight 0 against 1+1 = 2; y=(1,R): 4 against 2 (s = 1 and s = 2).
- Permanent records (additivity over through-z events at every earlier time, for every event): the rule is additive over single walks; S4 gives mu = |S|; return fraction <= 1/d (at most one arc y -> x0). Computed: walk-additive consistent rules have dimension 1 (uni; N=3 per); count return maximum 1/4 on rings 3, 4, 5, 8 (t <= 40); model reaches 1 on ring 4 at t=8, ring 8 at t=24.

## Not tried
- Product events beyond T=5 (b) and two reads beyond T=6; no proof that the classification survives on product events.
- Wrapping rings for the event families (only N=3 at T=4 in ev_classify: all 11, b 11, different unknown sets).
- Z1-F and other carriers; S6, S7.
- Records = position at T >= 5 (one component of 32 walks; T=4 already gives the minimum, count).
