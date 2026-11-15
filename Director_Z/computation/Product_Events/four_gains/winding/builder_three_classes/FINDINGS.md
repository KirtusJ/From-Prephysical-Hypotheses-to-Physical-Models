# builder_three_classes: findings (appended as the work proceeds; nothing here is issued)

Step 0 (reading). CONTROL: Lemma lem:winding(ii) needs n(l)n(l+2M) <= n(l+M)(n(l+M)-1).
(1,1,1): 1<=0 no. (1,2,1): 1<=2 yes. (2,2,2): 4<=2 no. (2,3,2): 4<=6 yes. (3,2,3): 9<=2 no.
So only (1,2,1) and (2,3,2) are not excluded by the lemma.

Step 1 (by hand, before any program). Lemma lem:windingrails already excludes the pairs the problem asks for:
if one rail of a site carries >= 3 levels and the other rail is non-empty, the other rail carries >= 2 levels.
Since a multiset in ONE coset of <delta> occupies one level only (levels form an interval, and classes are levels
mod 3), no pair (U,V) with U in three classes and V non-empty in one coset occurs, and no mirror pair. Proof in PROOFS.md.

Step 2 (program explore.py, run 1).  Command: `python3 -B explore.py results_run1.json 6 6 4000` (exit 0, about 40 s;
a second run with the same arguments in a scratch directory gave the same content apart from the command line).
Site totals <= 6.  Breadth-first over all masks with deduplication of states CLOSES (frontier empty: every reachable
state with all site totals <= 6 was visited, so the result is for ALL lengths) for q=1 on N=3 (12 layers), N=4 (8),
N=6 (14); on N=5 the layer cap 4000 was hit (exhaustive to length 5, sampled after).  For q=2 the cap was hit on
N=3, 5, 6 (exhaustive to lengths 7, 5, 7) and the search closed on N=4.
 P0 control: met.
 PW/PX: non-vacuous instances per ring (distinct profiles): PW(i),(ii) 12, PX1/PX2 10-12 (N=4: 2 and 1); failures 0.
 PN: 2 qualifying profiles on each of N=3,5,6 (0 on N=4); failures 0.
 PT: NEC (profiles of total <= 6 allowed by the two lemmas, <= 4 levels) minus SEEN: N=3: 22, N=4: 126, N=5: 6,
   N=6: 22; SEEN minus NEC: empty.  The six of N=5 are the one-vertex profiles (1,2,2), (2,2,1), (1,2,2,1) on R and
   on L: allowed by lem:winding(ii) (2 <= 2) and never seen.  This led to Lemma W' (PROOFS.md): if n(l)=1 or
   n(l+2M)=1 then n(l)n(l+2M) <= C(n(l+M),2).  N=4 (M=2): only (1,2,1) alone and R(1,1)+L(.,1,1) have three levels.
 PA (pairs seen, sizes <= 6; O_k = occurring orbits of size <= k; columns k, orbits, three-class orbits, sol, ref):
   N=3 and N=6, both groups: k<=3: sol=ref=3; k=4: sol 4, ref 3; k=5: 5 vs 3; k=6: 8 vs 3.
   N=5: k=4: 5 vs 3; k=5: 6 vs 3; k=6: 8 vs 3.   N=4: k>=4: 5 vs 3 (only 23 orbits occur at all, search closed).
   THE CLAIM sol_k == ref_k for k <= B-1 FAILS at k=4 and 5 with bound 6 on every ring.  Kept.  With bound 4 the
   excess at k=4 was 4 (N=3), with bound 6 it is 1, so the size cut is part of it; run 2 raises the bound.
   Two-class pairs alone (PA2): k=4: 9, k=5: 14, k=6: 40 on N=3: the three-class multisets are then free, as expected.

Step 3 (proofs, PROOFS.md).  Proposition N (PROVED): three levels on one rail force two levels or none on the other;
so for s >= 3 no pair "three classes against one non-empty coset" exists.  Lemma W' (PROVED): n(l)n(l+2M) <=
C(n(l+M),2) when an outer level is single.  Theorem A (PROVED given the conclusion of prop:threegroups): for s >= 3
the rule on multisets inside two adjacent cosets is alpha|m| + q(eps_i^2+eps_{i+1}^2) + c_i eps_i eps_{i+1}; for
s = 3 this fixes all three parameters of the count and the two squares.  Observation used in the proof: for s >= 3
prop:threegroups gives only the pairs (A_i) u two-coset, v in the UPPER coset, and (B_i) u in the LOWER coset,
v two-coset; the other two orientations, which the s = 2 proof gets from beta^2 in <delta>, are excluded by X1.
Steps 1, 3, 5 and the replacement of Step 6 had to be redone with (A), (B) only; they go through.

Step 4 (check_wprime.py).  Command: `python3 -B check_wprime.py results_wprime1.json 9 6000` (exit 0, 19 s).
q=1, site totals <= 9; search CLOSED (all lengths) on N=3, 4, 6; N=5 exhaustive to length 5 and sampled after.
 PW1 (Lemma W'): qualifying instances 70 (N=3), 18 (N=4), 80 (N=5), 70 (N=6); failures 0.
 PW2 (both outer levels >= 2): instances 4, 2, 4, 4; no violation of n0 n2 <= C(n1,2) seen (so the data do not show
   that the hypothesis "an outer level is single" is needed; no claim).
 One-vertex profiles (other rail empty) with >= 3 levels seen on N=5: (1,2,1) (1,3,1) (1,3,2) (1,4,1) (1,4,2) (1,4,3)
   (1,4,4) (1,5,1) (1,5,2) (1,5,3) (1,6,1) (1,6,2) (1,7,1) (2,3,1) (2,4,1) (2,4,2) (2,5,1) (2,5,2) (2,6,1) (3,4,1)
   (3,5,1) (4,4,1) and (1,3,3,1).  N=3 and N=6: the same without (1,6,1), (1,7,1).
 Allowed by lem:winding and by W' but NOT seen (N=5): (1,3,3) (2,3,2) (3,3,1) (2,3,3) (3,3,2) (2,4,3) (3,4,2)
   (1,3,3,2) (2,3,3,1).  Excluded by W' only, never seen: (1,2,2) (2,2,1) (1,2,2,1) (1,3,4) (1,3,5) (4,3,1) (5,3,1)
   (1,3,4,1) (1,4,3,1).
 So the two lemmas with W' are still not sufficient.  CONJECTURED (weak; totals <= 9 only, N=5 sampled): for a vertex
 with exactly three levels and the other rail empty, n0 n2 <= 2^(n1-2).  It fits every profile above ((1,4,4) and
 (2,4,2) attain it); it is FALSE as a condition on three consecutive levels of a longer profile: (1,3,3,1) occurs.
 Note for the control question: (2,3,2) is allowed by lem:winding and was not seen at any vertex with total <= 9.

Step 5 (explore.py, run 2).  Command: `python3 -B explore.py results_run2.json 8 8 20000` (exit 0, about 12 min).
Site totals <= 8.  q=1 search CLOSED on N=3 (14 layers), 4 (10), 6 (16); N=5 exhaustive to length 6, sampled after.
q=2 search closed on N=4 (16 layers); cap hit on N=3 (exhaustive to 9), N=5 (5), N=6 (8).
 PW/PX: instances 45-60 each on N=3,5,6 (11-22 on N=4); failures 0.  SEEN minus NEC empty on every ring.
 PN (Proposition N): qualifying profiles 16 (N=3), 6 (N=4), 20 (N=5), 16 (N=6); failures 0.
 PT: NEC minus SEEN: 88 (N=3), 342 (N=4), 32 (N=5), 88 (N=6): the lemmas are far from sufficient on small rings.
 PA, all pairs seen, both groups (Z2xZ3 and Z6 give the same numbers), sol_k against ref_k = 3:
   N=3 and N=6: k=1..3: 1,3,3 (equal to ref);  k=4: 4;  k=5: 4;  k=6: 5;  k=7: 6;  k=8: 13.
   N=5:         k=1..3 equal;                   k=4,5,6: 4;       k=7: 5;  k=8: 7.
   N=4 (search closed, so ALL events with site totals <= 8): k=1..7: equal to ref (3);  k=8: 5.
   THE CLAIM sol_k == ref_k for k <= B-1 FAILS on N=3, 5, 6 (excess 1 from k=4) and HOLDS on N=4.  Kept as a failed
   predicate.  The excess at k=4 went 4 -> 1 -> 1 (N=3) for bounds 4, 6, 8 and 2 -> 1 (N=5) for bounds 6, 8; it has
   not gone to 0.  Whether it is an effect of the size bound, of the sampling of the q=2 search, or a rule other than
   the count and the squares on these rings is NOT decided here.  Hypothesis counted: three-class orbits are present
   in O_k for k >= 4 (6 orbits at k=4; 151 to 179 at k=8), so the comparison is non-vacuous from k=4.
 PA2, two-class pairs only: the three-class orbits stay free (sol = 3 + number of three-class orbits, about).
 On k <= 3 (no three-class multiset occurs below size 4) sol = ref = 3 everywhere: agrees with Theorem A's content.

NOT DONE: item (2) of the problem (a construction for M >= 8 of pairs with three-class sums) and hence item (4).
By Proposition N such a construction must have BOTH rails on >= 2 levels (or one rail empty); the smallest shapes seen
in the enumeration are R levels (1,1,0) with L levels (0,1,1), (0,2,1), (0,1,2), (0,2,2), (0,3,1), and R (1,2,1) with
L (0,1,1); these are the targets a builder of wires should aim at.
