# Challenger 11 findings (cor:return)
- Run 1 of ret.py crashed in the C2 generator (random.sample with n<d); no result file written. Fix: n>=d in C2. Predicates unchanged. Kept as a failed first run.
- Run 2: 15 carriers, 13 qualify (2 deliberately non-qualifying kept: all-ones 2x2 fails H2,H3; paper's 3-vertex count-only example fails H3).
- P0,P1,P2,P3,P5 met 13/13. P2 worst margin -5.6e-13 (rounding; bound T*nV*1e-15 ~ 1e-11). Bound (1) attained with equality: Hadamard 2x2, t=2, a=1/3 (N_2/4=1/2, U^2=1).
- P4 failed on coined_ring_5 in window [1000,2000] (0.955); over t in [1,2000] its max is 0.99716 at t=264. Measured only; not a failure of the corollary (limsup).
- C1: 3028 simple out-regular digraphs, 0 violations of N_t <= d^(t-1), max ratio exactly 1. C2 (parallel arcs, hypothesis violated): 500/500 violate.
- Rerun in fresh directory: result bytes identical.
- Proof reading: (2) needs epsilon<=1 and a norm dominating diagonal entries and unitarily invariant; neither stated. Hypotheses are in the surrounding text via "With these assumptions", not in the statement.
