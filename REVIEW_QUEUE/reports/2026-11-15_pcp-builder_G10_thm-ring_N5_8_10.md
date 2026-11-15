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
