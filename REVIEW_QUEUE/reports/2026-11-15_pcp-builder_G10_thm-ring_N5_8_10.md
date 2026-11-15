Target: G10 Theorem 5.36(i) on the open rings N/gcd(N,2) in {4,5}, i.e. N = 5, 8, 10; master a8c9608.
Control: gcd(10,2) and 10/gcd(10,2). Expected 2 and 5; got 2 and 5. Passed.
Outcome: PARTIAL. Nothing proved; no obstruction found. Run cut off by its own 300 s timeout (exit 124).
Reviewer kind: pcp-builder sub-agent of the queue session; same model family as the author. Not independent review.

- Reduction: with site-independent F, mu(Ext S) - 2 mu(S) is a sum over sites of E(U_x,V_x) = F_R(U+V) + F_L(U+TV) - 2F_R(U) - 2F_L(V); a proof needs the preparation lemma or that the reachable (U,V) pairs still force Proposition solveq.
- COMPUTED (T <= 8, <= 6 walks, |U|+|V| <= 2): all pairs reached for N=5,8 at q=2; pairs missing (not shown unreachable) for N=5 q=3 (129/135), q=4 (169/220); N=8 q=3 (188/216), q=4 (199/352); N=10 q=2 (134/140), e.g. U=(0,0), V=(0,2) at site 3.
- COMPUTED: on all 7 cases run, the consistent site-independent (F_R,F_L) restricted to |m| <= 2 have dimension 2 (q even) / 1 (q odd), equal to the claimed family. Form forced at that size despite missing pairs.
- CONJECTURED: 5.36(i) holds on N = 5, 8, 10.
Not run: N=10 with q=3,4; control rings N=6,12. Program's own total line not reached.
Rerun: timeout 300 python3 explore.py res_T8_W6_B2.txt 8 6 2 (mode 'x' output; seed 20261113, no randomness). Not rerun by the queue session; digests checked against the sub-agent's.

Addendum (queue session, same day): full pass without the timeout, in a fresh directory, by the queue session.
Command: timeout 3000 python3 explore.py res_T8_W6_B2_full.txt 8 6 2; exit 0; 32 min 57 s; result sha256 f9b62d77124539008f27023a7fa5ef8b4d880ef85deb798b8d8f5d89e253d685 (`res_T8_W6_B2_full.txt`, `run.log`). The first seven cases agree with the cut-off run.
- New open cases: N=10 q=3 (203/270 pairs reached, projected dim 1 = expected), q=4 (220/440, dim 2 = expected). All 9 open (N, q) cases now give the claimed dimension at |m| <= 2.
- Control rings N=12 (M=6, where the lemma is claimed): pairs also missing (146/168, 204/324, 220/528) at the same bound. So missing pairs at T <= 8 are an artefact of the bound, not evidence about the small rings.
- Tension, not resolved: N=6 (M=3) with q=3, 4 also gives the claimed dimension at |m| <= 2, while the queue's small-ring report PROVED an obstruction for N=6, q >= 3. Either the obstruction appears only beyond |m| <= 2 or one of the two is wrong. Not checked; wanted: a micro-review comparing the two.
