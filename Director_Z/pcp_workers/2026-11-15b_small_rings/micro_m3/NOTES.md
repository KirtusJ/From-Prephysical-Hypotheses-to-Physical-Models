# micro_m3 notes (micro-review, author's model family, not independent; no gate passed)
## Step 0 control
M = N/gcd(N,2): N=6 -> 3; N=10 -> 5.
## Step 1 inputs read
PAPER_TEXT_subsections.tex. Definition of "position product event" is NOT in this file ("as in the subsection on them above").
Interpretation used (stated assumption): event of length T = all walks of length T from (0,R) whose
position at each time t=1..T lies in a chosen set A_t of sites (a product of position masks).
Gain on D_delta: delta per L->L arc; lambda = number of left steps.
## Step 2 program enum_pp.py (predicates in docstring before first run; output opened 'x'; RLIMIT_AS 2 GB)
Commands (cwd /tmp/claude-0/micro_m3_r1): python3 enum_pp.py 3 3 {8,10,12} z3_T{8,10,12}.txt -> exit 0, 1 (MemoryError building layer 10), 1 (same).
Layers fully checked on Z_3: T=0..9 (T=9: 211602 states, 432 MB). Diff L-R = 1 never seen (P1 PASS to 9).
Controls: diff 0 first at T=2; diff 2 first at T=3.
Z_6: python3 enum_pp.py 6 3 {5,6,7} -> exit 0; same state counts as Z_3 (parity class of Z_6 ~ Z_3, M=3); P1 PASS to 7.
Rerun T=8 in /tmp/claude-0/micro_m3_r2: exit 0, bytes equal.
Note: on Z_3, x_t = t + lambda_t mod 3, so a mask = a constraint on lambda_t mod 3; gain = lambda - #L-runs. No proof found in budget.
