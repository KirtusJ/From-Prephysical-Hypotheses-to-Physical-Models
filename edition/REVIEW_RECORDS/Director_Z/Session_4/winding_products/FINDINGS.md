# FINDINGS (second builder; same model family as the author, not independent review; no gate passed)

PROVED (PROOFS.md): Lemma 1, exact model: walk counts n_t on Z with n_t = 1_{B_t+MZ}(n_{t-1}+S n_{t-1}), B_t any
subset of Z_M; site profiles = restrictions of n_{T-1} to two adjacent classes. Lemma 2, trimming: a run to a profile
of total K can be replaced by one whose totals are nondecreasing and <= K. Lemma 3: width grows <= 1 per tick, so a
width-capped BFS whose largest width found is below the cap is complete.
The earlier builder's abstract copy/merge/delete packet model is NOT shown equivalent and is not used.

COMPUTED (exhaustive; completeness by Lemmas 1-3; folder run1/, scratch origin
/tmp/claude-0/-home-user/28e97793-3fca-58b9-952e-550ec29453c0/scratchpad/run1):
- python3 exact_bfs2.py 11 3,4,5,6,7 6 res2_cap11_M3to7.txt  (exit 0)
- python3 exact_bfs2.py 12 4,5,6 6 res2_cap12_M4to6.txt      (exit 0)
- python3 exact_bfs2.py 12 3,7,8 6 res2_cap12_M3_7_8.txt     (exit 0)
- python3 exact_bfs2.py 13 5,6 6 res2_cap13_M5_6.txt         (exit 0)
  (1,2,3,3,2), (2,3,3,2,1), (1,2,3,5,1) occur on no ring with 3 <= M <= 8; all satisfy cor:tp(ii),(iii).
- python3 allowed.py res2_cap11_M3to7.txt 7 11 allowed_K11_M7.txt; ... res2_cap12_M3_7_8.txt 8 12 allowed_K12_M8.txt;
  ... res2_cap13_M5_6.txt 6 13 allowed_K13_M6.txt (exit 0 each). Allowed-but-unreachable (length <= 6), each in both
  rail placements: total 11: 12332 and reverse; 12: 12351 and reverse; 13: 13342, 24331, 123421, 124321.
  Reachable but not allowed: none.
- brute.py N 7 for N=3,4,5 (exit 0): independent walk enumeration; its profiles are a subset of the model's.

FAILED / corrected: res_cap11_a.txt crashed (root finder on the control's double root). Control "(1,2,1) found" is
FALSE at M=3 (also absent in the brute force on N=3); the expected value was wrong. P2 (stable in W) was FALSE
between W=2M,3M (the set grew), so W was raised and Lemma 3 used instead.

CONJECTURED: reachable profile set of total <= K is independent of M for M >= M0(K) (M0(11) = 4, M0(12) = 5 in the
data); max gap between occupied points <= M (naive induction fails). Hence the NO answer to rem:tpprod(b) holds for
3 <= M <= 8 only; for large rings it is open.

NOT CHECKED: M >= 9; profiles longer than 6 entries in the allowed list; total 14; gains; Lean (no pure-algebra step).
