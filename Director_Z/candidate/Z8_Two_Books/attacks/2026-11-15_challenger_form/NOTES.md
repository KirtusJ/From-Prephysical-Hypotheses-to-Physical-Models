# Challenger notes, Z8 Two Books, 2026-11-15 (same model family as the author)
Inputs read: CANDIDATE_PROCESS.md, FORM.md, SPECIFICATION.md, BRAND.md, method sections named in the brief. Not read: function/, sprint folder.

CONTROL. Site x: rail R eps=1, n=3; rail L eps=1, n=1. Before: W=2, p=1/2 each, H = (1/2)log 3 + (1/2)log 1 = (1/2) log 3.
After a free step: (x+1,R) eps=2, n=4; (x-1,L) eps=0, n=4. W=4, p=1 on (x+1,R). H = log 4. Rose (log 4 > (1/2) log 3).

## Target 1 (python3 t1.py -> result_t1_run1.json, exit 0, 10 s)
Proof read line by line: every step follows. N=1: (x+1,R)=(0,R), (x-1,L)=(0,L), distinct vertices, one source site. N=2: both children at site x+1, rails differ, one source site. Sign: only L->L flips, so (x-1,L) gets eps_R - eps_L. Equality case: follows (p_R>0 and p_L>0 forces strict; p_R>0,p_L=0 equal iff n_L=0).
Computed: A0 propagation = explicit walks 1204/1204. Product events (mask sequences, masks = non-empty subsets of reachable sites):
ring1 11/11 qualify, ring2 11/11, ring3 (T<=6) 8998/9769, ring4 (T<=9) 15521/29524, ring5 (T<=4) 783/801, ring6 (T<=5) 1828/1956, ring7 (T<=4) 783/801, line (T<=4) 783/801.
Total qualifying 28718 (of 43674 sequences); A1..A5, T4: 0 failures. 16759 equal, 11959 strict. 15 sign decisions used 80-digit decimals (min relative margin 0.084), the rest integer products.
A5 (BRAND wording "every occupied site") never differed from A4 (FORM wording "site that carries chance") in range. Not found, not proved equal.
N1: arbitrary sets of walks (not product events): 316,225 qualifying sets, 0 failures of A2, A3, A4. T-1 holds for any set of walks of one length (the proof never uses the product property). HELD, with note: the hypothesis "position product event" is not needed.
B3 (plain count): 0 failures. C3 (|eps|), D3 (eps^4): 0 failures IN THIS RANGE (kept; see t5 for a wider search).
R1: 478 pairs of distinct before-states with equal after-state (eps equal, counts differ), e.g. ring 3, T=6: {(2,R):(3,5)} and {(2,R):(3,3),(2,L):(0,2)}.
M3 mirror carrier: 1345 qualifying, 0 failures.
