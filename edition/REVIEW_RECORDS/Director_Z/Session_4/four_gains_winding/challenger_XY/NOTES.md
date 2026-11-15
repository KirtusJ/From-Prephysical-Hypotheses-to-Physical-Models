# challenger_XY notes (15 Nov 2026)
step 0: wrote y_linalg.py. command: python3 y_linalg.py result_y_linalg_run1.json
step 1: y_linalg run finished or running; see log_y_linalg_run1.txt. Claimed cases (quotient 2): P0,P1,P2 all true. Contrast quotient>=4: R strictly larger from size 4 on.
step 2: wrote x_lemma.py. command: python3 x_lemma.py result_x_lemma_run1.json 20261115
step 3: wrote t_prop.py. command: python3 t_prop.py result_t_prop_run1.json 20261115
 ambiguities resolved: (1) ADV masks relative to the source deficit at the START of the ADV; s += 2 after it.
 (2) empty group: its slot, RUN and MERGE are skipped; KILL mask = stock positions (empty if no stocks).
 (3) MERGE tick-2 mask = others u {k+2} even if residue 2 unoccupied; 'one IDLE' = mask of occupied positions after merge.
 (4) RUN X to p = repeated 'RUN by one'; 'others' includes the source at 0 while it is alive.
 (5) mode (ii) 'RUN B to M' happens after MERGE A (order of the schedule line).
 (6) FINAL masks in mode (ii): {1,2},{2}; Q = B at unwrapped M.
step 4 results (all three programs exit 0, each run once; no fresh-directory rerun done):
 y_linalg: 20 cases. Quotient-2 (claimed) cases 9: P0,P1,P2 true at every cut 2..n. Contrast: R and R2 have one EXTRA
   solution from size 4 on for (Z2xZ4,(1,2)), (Z2xZ4,(1,0)), (Z4xZ2,(2,0)), Z10 delta=5, Z2^3 (cut 4,5 only); none for Z6 d=3, Z8 d=4, Z12 d=3.
 x_lemma: 111,731 events; X1 pairs 15,019,986 (boundary l'-l=M: 9,016,931); X2 pairs 16,276,749 (boundary 2M: 7,727,096; tau=T-1 in 337,594);
   no tau/member/end/inj/count failure. KEPT FAILED (not claimed) predicate: X2 at l'-l=M fails in 22,409 of 23,072 instances.
   X.1: 9,604 and 9,236 qualifying instances, 0 failures. Not broken down by N (qualifying pairs for odd N>=5 not counted separately).
 t_prop: M>=8 (N=16,9,11,17,18,13,32): 14,892 cases, T1 fail 0, T2 fail 0 (max mask 5). Subbound: M=7 (N=7,14) fails
   (e.g. N=7,q=1,mode i,G1={0},G3={0}: 2 walks at lambda 11 on L instead of 1); M=2..6 fail as well.
