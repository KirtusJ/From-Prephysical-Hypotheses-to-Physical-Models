# chal_q78 notes (challenger, same model family as author; not independent review)
## CONTROL
q=2, F(u0,u1)=(u0-u1)^2 for both R and L. eps(U+V)=eps(U)+eps(V), eps(U+TV)=eps(U)-eps(V) (T swaps the two entries),
so LHS=(a+b)^2+(a-b)^2=2a^2+2b^2=RHS. ANSWER: YES, it is a solution. (Also enumerated in program, predicate P0.)
## Step 1: read THEOREM_Q.tex only. Hand check of proof steps 1-6: all follow (details in report).
Predicted before run: dropping F(0)=0 gives extra solution F_R=-b, F_L=+b (constants).
## Step 2: probe run (NMAX=6 all q), probe_result.json kept. 35.6 s, exit 0.
P1 all pass n=2..6, q=1..8. P1x reduced==full==Fraction. P6 (k=1,3) nullity 0. P7 pass. P8 pass, neg controls fail as expected. P10 pass.
FAILED (kept): P4 (F(0) free): claimed+1 everywhere (predicted: F_R=-b,F_L=+b). P5 (no zero instances): claimed+2 everywhere.
P5 analysis: F_R=+1, F_L=-1 on nonzero multisets is an exact extra solution (1-1=2-2). Second extra dimension suspected truncation
artifact (q=1: F_R(n)-F_L(n) free at top size). Added P5b AFTER the probe: nullity restricted to sizes <= n-1 == claimed+1.
## Step 3: final run result.json exit 0 (69 s); rerun in rerun/ compared by sha256 (see report).
P1 pass for q=1..8, n=2..(16,14,12,10,9,8,8,8). q=7 n=7,8 and q=8 n=8 contain 1. Failed kept: P4, P5 (see result.json).
## Step 4: wrote wording_THEOREM_Q.patch (+description). Report next.
