# challenger10 findings (cor:composition), same model family as author
- Run 1 comp.py -> results.json. Carriers T2, B4, R4 all meet H (3/3). B4: U={chi,chi^3}, one class (chi^2 is NOT in U; my prior guess was wrong). All C_0 = C.
- P1 6/6 (256 and 65536 pairs per carrier), P2 6/6, P6 3/3, P7 3/3.
- P3 met 44, FAILED 4 (kept): at length 2 on B4 and R4 the rules (1/2,1/2) and (1,-1) are multiplicative on all 256 pairs. Cause: rank of (|S|, ||v||^2) is 1 there (no two walks share an end vertex, so |S| = ||v_S||^2). Predicate was too strong at short lengths; corollary not contradicted (needs every length; proof uses one large n).
- P4 met 4, FAILED 2 (same two instances, rank 1 of 2 at length 2).
- P5 not exercised in run 1 (no carrier with k>=2). Run 2 comp_b8.py -> results_b8.json: B_8, U={1,3,5,7}, classes {1,7},{3,5}, rank 3 at length 3, Q1 65536/65536, Q2 14/14.
- Hand checks: proof steps follow. Gaps: citation of thm:periodic(c) for independence on M(C_0) (that is in the theorem's proof, not statement (c)); paragraph after omits the zero rule; F_y(0)=0 dropped in the paragraph (harmless).
- Not computed: any carrier with C_0 != C (coset support on product events checked by hand only).
