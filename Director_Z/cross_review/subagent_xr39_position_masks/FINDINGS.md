# xr39 findings (Claude sub-agent, same family as Director Z; in-project, not independent)
## Step 1 hypotheses (from note text)
- F zero at empty multiset: stated (sec. walk/event).
- F stationary across horizons (tick-independent): stated in body, NOT in lead. Essential: pair (U,V) is realized only at tick T(U,V).
- F position-independent: stated only at "Write F_R,F_L for position-independent scores" (body). Lead sentence "Under the stated continuation law, the only surviving endpoint terms are a path count and a squared signed count" drops it; false on the line for real site-dependent F (THEOREM.md Prop 2: F_y=x(y)(p+q)). Spatial section recovers it only with nonnegativity (line) or ring N/gcd(N,2)>11. -> GAP (lead).
- Rail independence: derived (V=0).
- Factor 2: assumed (premise); derived only for nonnegative nontrivial position-independent scores (common k).
- Jointly at one site: U on (x,R), V on (x,L) at same tick, all other wells empty; x=T-20, T fixed by (U,V); x_* prescribable via prefix, tick not.
- Ring: N/gcd(N,2)>11 stated; line otherwise. Launch (0,R) positive stated.
- Order of pulses across the two corridors: not stated (sequential implied by T formula).
## Step 2 (xr39.py -> results_xr39.json)
Line: P1 ok; P2 256/256 for orders A,B,C, max layer 5, T and x formula ok; P3 prefix 90/90; P4 tamper (2,1) ok; P5 three-tick ok. No stray survivors.
## Step 3
Deduction follows. Nullity exactly 2 for M=4..8 from all pairs, and also 2 from the three families alone. Rail independence derived; position independence and factor 2 assumed (spatial section: nullity 1 for single-input system on every ring 3..30).
## Step 5 (first run, order A only): rings 13,15,..,21,23 and >=24 pass 256/256 as note says; N=11 and 22 ALSO pass 256/256 (not covered by note's criterion). 3324 failed target/ring instances kept in results file. See xr39b for other orders.
## Step 5 follow-up (xr39b.py -> results_xr39b.json)
Orders A/B/C all 256/256 for every ring with N/gcd(N,2)>11 in 3..30. N=11 and 22: order A 256/256, order B 31/256, order C 54/256 (first fail U=(0,1),V=(0,1)): word leaving deficit 10 by L lands on deficit 11=0 and is deleted only if no corridor-0 pulse follows. Prefix on rings 11,13,22,24: all exact (order A). N=12: 1/256 (empty target only); N=10: 0/256.
## Step 4
Author checker rerun in fresh dir: byte-identical (sha256 04a82ec3...caefe). Its ring part: 12 rings x 16 targets (entries 0..1), one pulse order (corridor 0 first), inspects target site only; 78 failures = 16+15+15+16+16 (N=4,12,16,18,20). Its ring 22 passes with period 11, i.e. outside the note's own criterion.
Lean 4.19.0 (installed, no download): exit 0, axioms propext, Quot.sound. Proves: one isolated 5-site corridor (deficits 0..4, no inflow at 0, outflow past 4 dropped by construction), pulse [1,2,3] adds swapped reservoir, [1,2,2,3] adds reservoir, for arbitrary counts. Does not model the second corridor, phase 1, the closing six ticks, the ring, or the prefix.
