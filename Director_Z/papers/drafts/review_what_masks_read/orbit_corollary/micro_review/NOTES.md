# NOTES
Control: N=6 M=3; zeta^-2 exponents 0,4,2,0,4,2 -> {0,2,4}
check.py (predicates P0-P5 in docstring, run1.txt): FAILS 0. P2: 512/512 grid coins qualify; all maps exact. P3: 8980/8980 pairs reached.
P4: u=1 (1,1,1,-1) vs u=-1 (1,1,-1,1), N=4, t<=3 all masks: maxdiff 0; control u=i differs 0.5.
P4 connect loop with g,lam in {+-1}: no hit even with zeta=+-i.
Follow-up: quarter-turn search: only zeta=+-i WITH g=-+i, lam=-1 connect. Site phase alone does not.
P5: rail/site/conj from sharp start: diff ~1e-16. Rail lam=e^(i pi/4), alpha=beta=2^-1/2: diff 0.146 (sharpness needed). First witness lam=i gave 0 (Re kappa symmetric), replaced.
