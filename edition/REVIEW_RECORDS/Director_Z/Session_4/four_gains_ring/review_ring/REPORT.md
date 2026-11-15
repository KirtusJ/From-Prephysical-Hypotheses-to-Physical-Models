Challenger report: Lemma R_N and Proposition P_N (PREP_RING.md). Same model family as the director; not independent.
Verdict: no defect in either proof in the tested range; two wording faults; hypotheses partly in surrounding text only.
Control: Z_5, Z_2, (1,0,0,1): B=0, 5B=0, kappa(5 right steps)=1=g-g_delta, end (0,R). PASS (hand and program).
Program chal.py, predicates in docstring, seed 20261115, results.txt (refuses overwrite), exit 0, 3m14s; fresh-dir rerun identical bytes (sha256 3151e545...a505).
R_N: formula 0 failures (all walks T<=12, N=1..10, 11 groups); well-definedness 0 failures over 10226 hypothesis instances; all 22574 non-hypothesis instances break in range.
P_N: 468 qualifying quadruples, N=3..8; 42420 targets; 22449 pass, 0 fail, 19971 beyond BFS bound (BFS stand-in for Lemma 5.34, M<6 included).
Prefixes: unique and closed iff N>=3; N=1,2 give 2/4 walks ending on both rails.
Wording: Step 5 reason ("distinct sites") wrong reason; left-right prefix uniqueness unargued; "from s lands at s-2" slip.
GAP: B^M=1 and Delta_N=<delta> are in the Setting, not the Lemma R_N statement; T0>=1 and site x-bar arbitrary come from Lemma 5.34 (stated there).
