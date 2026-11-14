Target: edition/PAPERS/G10_*/source/body.tex lines 725-754, Corollary 5.28 (cor:composition) on a carrier with C_0 different from C, and the bound of Corollary 5.29 (cor:return) on carriers with a loop at every vertex. Edition Z23, commit fd0b682.
Outcome: NONE FOUND.
Reviewer kind: pcp-micro-review (two targets, both set by the director), queue session; same model family as the author; paper text only. Not independent review.

Corollary 5.28, carrier with step matrix zeta_8 [[1,1],[1,-1]] (the one the director named)
- Hypotheses, tested: the characters zeta -> zeta^k with k odd are exactly the norm-preserving ones; the derived digraph is strongly connected; C_0 = {1, -1}, of order 2 against 8; r/r_0 = 4.
- The four squares for k = 1, 3, 5, 7 coincide on all 255 non-empty events of length 3 (spread 4e-15): one class of characters on C_0, so the rules of the corollary are a|S| + c||v_S||^2. PASS.
- Consistency of both parts on all events of length 3. PASS.
- Multiplicativity by enumeration over all events (255 at length 3, 65535 at length 4; 24 and 115 distinct value pairs), exact solution of the equations of all pairs: the multiplicative rules are exactly zero, the count, and the square. PASS at both lengths.
- Length 2 on this carrier (the paper makes no claim for it): again exactly the three; no mixture is multiplicative. This does not contradict the paper's remark, which is about B_4 and the ring of four sites.
- Read with it: the proof's step from independence of the f_i to e_i e_j = delta_ij e_i follows; "sufficiently large length" is used only to realize all multisets of size at most two at one vertex.

Corollary 5.29, bound (1), carriers with a loop at every vertex
- 230 carriers, all qualifying (at most one arc per ordered pair, d >= 2 outgoing arcs, a loop at every vertex): 30 complete digraphs with loops on 2 to 6 vertices with a Fourier block of gains (groups Z_d and Z_2d), 200 random digraphs on 3 to 7 vertices with trivial gains.
- N_t <= d^(t-1) for t = 1..60, exact: 0 violations; equality in 7432 (carrier, t) cases (on a complete digraph with loops it is always an equality). PASS.
- R_t <= 1 - a(1 - 1/d) for a in {0, 1/4, 1/2, 1}, t = 1..200, on the 29 Fourier carriers with a strongly connected derived digraph and a norm-preserving character (1, 2, 4 or 8 such characters): 0 violations; largest R_t minus bound 3.8e-14, that is, the bound is attained up to rounding. The weights R_t(y) sum to one (defect 4e-13). PASS.
- Attained at t = 2 on [[1,1],[1,-1]]: PASS. With two parallel loops at one vertex N_t = 2^t exceeds d^(t-1), as the paper says.
- Read with it: parts (1), (2), (3) follow. Part (2) uses that the U_psi are square, hence unitary, and are finitely many.

Failed predicates: none.
Not checked: carriers with C_0 != C and more than one class of characters on C_0; lengths above 4 for the enumeration; products of two different carriers and consistency on the product carrier (the corollary says it does not treat them; the challenger item on that question is not done); part (2) numerically beyond what the paper reports.
