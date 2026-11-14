# NOTES chal_cs (challenger, same model family as author; not independent)
Step 0: read CRITERION.md sections only. Conventions: start (0,R); R step -> (x+1,R), L step -> (x-1,L);
arc gain named prev-rail,new-rail (RR=a, RL=b, LR=c, LL=d); first arc leaves rail R; ticks 1..t; mask S_j applied
to the site after step j; port prob = 2^-t |sum chi(G)|^2; well = sum of the two rails.
Step 1: CONTROL answer: fork N=7 length 8, chi(z)=-1, chi(g)=1, port (1,R): 1/64 (brute 256 words; admitted RRRRRRRR, LLLLLLLR; L rail 0). chi(g)=w: 1/256.
Step 2: chal.py written with predicates in docstring, run once: exit 0, no failed predicate. A1d (power control) found 14090 mismatches as expected.
 A1 336/700 carriers qualify (273 noncyclic, 334 with a or c nontrivial), 942 pairs, 187707 comparisons, 0 mismatch.
 A2 complete for N=1..14 (672 ports, unique l for t<=D). A4 only 23 qualifying cross-carrier pairs (thin). A4s: superposed start reads chi(c/a) (outside setting).
Step 3: rerun in fresh dir rerun/, byte-identical; in-place rerun refuses (exit 3).
Wording findings: see final report (Re chi(B)^D precedence; (iii) needs product-carrier step; corollary N=1,2 needs port; summary depends on sharp one-rail start).
Note: the Read tool returned the whole CRITERION.md; table / failed-attempts sections were seen but not used; table.py, control.py and result files not opened.
