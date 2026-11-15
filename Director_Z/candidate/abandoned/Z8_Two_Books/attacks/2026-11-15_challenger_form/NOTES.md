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

## Target 4 (python3 t4.py -> result_t4_run1.json, exit 0)
Sharp start, 240 free steps, rings 1..12 and line. Zero increments only at steps 0->1 (all carriers) and 1->2 (N>=3 and line); none later. E1/E2 mismatches 0, negative increments 0.
Smallest increment for T>=2: (1/2) log 2 = 0.34657... at step 2->3 (rings 3,5..12, line); log 2 on rings 1, 2, 4. Last 100 steps: rings >= 0.69299 (ring 11), line >= 0.53104.
On rings T log 2 - H(T) tends to a constant (ring 3: log 6, ring 4: log 4, ring 5: log 10, ring 8: log 8, ring 12: 2.4849=log 12): counts become uniform over reachable vertices, so late H is T log 2 - log(#vertices) whatever p is. Line: gap 2.907941, 7.381311, 12.790752, 41.317337 at T=8,32,64,240 (FORM's three figures reproduced; 12.790752 rounds to 12.791).
Verdict: HELD (range 240 steps, not a proof; a proof sketch: once both rails of every occupied site are occupied, n_R,n_L>0 for ever since counts never cancel, so every later step is strict).

## Target 2 (python3 t2.py > t2_run2.log 2>&1 -> result_t2_run2.json, exit 0, 43 s)
Run 1 (python3 t2.py, BITLIM 3e6, wider ranges) was killed by me after 9 min with no output and no result file (exit 144). Run 2: BITLIM 1e5, 'same site' T<=4, coarse-graining ring 4 T<=5. Kept as a deviation.
(a) Pair events (my extension; the candidate defines only products). Qualify = pair weight and both marginal weights > 0.
 Subadditivity H12 <= H1+H2 FAILS: all sets of pairs ring 1 T=2: set marginals 2664 of 64942, multiset marginals 24 of 65230. Joint-mask events ring 3 T=3: set 652 of 3844, multiset 0 of 3847; line T=3: set 609 of 3870, multiset 0 of 3872. Ring 3 T=2 (all sets and joint masks): 0 (all n=1 for set marginals).
 Smallest, checked by hand: ring 1, T=2, pairs {(RR,RR),(RL,LL),(LL,RL)}: pair records ((0,R),(0,R)) eps 1 n 1; ((0,L),(0,L)) eps -2 n 2; H12=(4/5)log 2. Each marginal {RR,RL,LL}: (0,R) eps 1 n 1; (0,L) eps 0 n 2; H=0. So 0.5545 > 0+0 (same with multiplicity).
 Joint-mask example checked by hand: ring 3, T=3, {(RRL,RRR),(RLL,RLL),(LRL,LRL),(LLR,LRL)}: H12=(2/3)log 2, set marginals H1=H2=0.
 H12 >= H1 FAILS very often (multiset: about 95 per cent; set: e.g. 21472 of 64942). Smallest: {(RR,RR),(RR,RL)} multiset; {(RR,RL),(LR,RR)} set.
 Cause: per record log n IS subadditive for set marginals (n(v,v') <= n1(v) n2(v')); the mean fails because the chance of the part computed from the part's own walks (S3) is not the marginal of the pair's chance (signed sums cancel in the part and not in the pair).
(b) Merging two records (eps and n added): ring 3 (T<=5) 2735 qualifying merges: 2378 rise, 133 fall, 224 equal; line: 1246 rise, 97 fall, 421 equal; ring 4: 157 rise, 0 fall, 64 equal. Fall example ring 3: {(1,R):(-1,3),(2,R):(1,5),(2,L):(-1,3)}, merge (1,R),(2,R): H 1.2689 -> 1.0986.
(c) No sentence of FORM, BRAND or SPECIFICATION asserts subadditivity, monotonicity or behaviour under merging; correlated pairs are not objects of S1-S2. SPECIFICATION section 1 lists "a property that any entropy must have and that H lacks" as counting against. Verdict: WOUND to S5 (the word "entropy" needs narrowing to "mean log-count, additive on products only"); not a KILL, because the counterexample lives in an extension the candidate does not define. Director's decision point: if the pair extension with set marginals is accepted as the candidate's and subadditivity as required, SPEC section 1's own criterion is met.
 BRAND "the growth of entropy ... has nothing to do with ignorance or coarse-graining": S4's n(v) is the number of histories sharing the end vertex, i.e. the record is a coarse-graining of the history (record = whole walk gives n=1, H=0 always). Summary sentence at odds with S4. WOUND (wording).

## Target 3 (in t1.py: R1, M3)
Signed sums invert: eps_R(x) = (e(x+1,R)+e(x-1,L))/2, eps_L(x) = (e(x+1,R)-e(x-1,L))/2 (half-integers in general for a state not produced by a free step). Counts do not: the free step sends (n_R,n_L) to n_R+n_L twice; not injective (478 collisions among enumerated events) and not surjective (image has n(x+1,R)=n(x-1,L)). So "running free backwards" is undefined on the candidate's state (eps,n). On events (sets of walks) the only backward operation is deleting the last step, which undoes a free step and then H does not increase.
Mirror carrier (walks ENDING at a pinned vertex, steps prepended): children of old start (y,R) are (y-1,R),(y-1,L); of (y,L) are (y+1,R),(y+1,L); new (x,R) = a+b, (x,L) = a-b with a=eps(x+1,R), b=eps(x-1,L); weights double, counts n_a+n_b >= each. T-1 holds verbatim in the opposite direction: 1345 qualifying mirror events, 0 failures. The sign rule (number of adjacent LL pairs) is reversal symmetric; the only asymmetry is S1's pinned start.
Verdict: WOUND to S6. S6 is not derived, so it does not assume a conclusion; but its direction is the direction away from the pinned end of S1, and S2's "next step" already carries it. FORM weak point 4 says this case "would need a reason the candidate does not have".

## Targets 5, 6 (python3 t5.py -> result_t5_run1.json, exit 0, 5 s)
27000 random masked events (rings 3..10, line, T 3..12). sq: 24563 qualify, 0 fail. count: 27000, 0 fail. NOT conserved site by site: |eps| 5 fail, eps^4 60 fail, support 161 fail, 1/n 1026 fail (each confirmed by the exact sign routine).
Hand-checked: ring 9, masks [1,8],[2,7],[1,3,6],[0,4,5,7],[1,4,5,6,8],[4,5,6,7],[4,5]; state (4,L):(3,3), (5,R):(1,1), (5,L):(1,1); eps^4: H = (81/83) log 3 = 1.07214 -> (162/178) log 3 + (16/178) log 2 = 1.06217.
So T-1 is not empty with respect to the chance rule: it needs site-wise conservation. BRAND says it is not special to the squared rule. Verdict target 5: HELD, with the note of target 4 (on rings late H = T log 2 - log(#vertices) whatever p).
T-2: 400 random products of ring-3 events: H12 = H1 + H2 exactly, 0 fail. GAP: the proof needs both weights > 0 and a definition of a product event and of the sign of a pair; neither is in S1-S6 (nowhere). HELD.
T-3: ring 3, 1454 qualifying events of length 5, 1146 qualify after mask {2}, 20 fall to H=0; values before: 0.366204, 0.462098, 0.549306, 0.554518. Example masks (1,2),(1,2),(0,1),(0,1),(1,2): state (1,R):(-1,1),(2,R):(2,2),(2,L):(1,1), H=(2/3)log 2=0.4621 -> after {2}: (2,R):(-1,1), H=0. HELD.
T-4: n bounds 0 failures on 43674 sequences (t1), H bounds 0 failures on 400 (t5). HELD.
Not checked: weak point 2 (observability); FORM's figure 45,218 (different enumeration, function/ not read); Lean; no plot made.
