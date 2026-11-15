# NOTES (challenger, ringprep) 
- Read PREP_RING.md, draft subsection, body.tex 775-800, 876-890 (Lemma 5.34 = prepq).
- Control (by hand, before program): Z_5, A=Z_2 additive, (a,b,c,d)=(1,0,0,1).
  B = b+c-2a = 0 mod 2; B*M = 5*0 = 0 mod 2 OK. delta = a+d-b-c = 0.
  5 right steps from (0,R): rho=5, lam=0: kappa = (rho-lam)a + lam(b+c) = 5 mod 2 = 1.
  Check: g(w) = 5a = 1, g_delta(w) = 0, ratio g - g_delta = 1 = kappa. Ends at (0,R). Program to confirm.
- run 1 started (chal.py results.txt), in background
- run 1 exit 0, 3m14s. P0 PASS; P1 0 failures; P2 10226 hyp instances, 0 failures; P2' 22574 nohyp all broken in T<=12;
  P4 OK (N=1,2 prefixes not unique, not closed; N>=3 unique and closed); P3 22449 pass, 0 fail, 19971 beyond BFS bound (depth 9/7, cap 4 walks).
- next: rerun in fresh dir for bytes; coverage counter (how many P3 passes used i>0, j>0, odd N).
- rerun in fresh dir: exit 0, identical sha256 3151e545...a505. coverage: i>0 2475, j>0 8955, odd N 13393, s!=0 5048 of 22449 passes.
