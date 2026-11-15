# REPORT: PREP(Delta_N) for four gains on rings (builder; same model family as the director)

First line: NOTHING strengthened in general. PREP is REFUTED (with a written proof) on Z_1, Z_2 and Z_4 for every choice of gains,
and therefore for B^M != 1 too. On Z_3 (= Z_6) it is a bounded miss only. No construction for M >= 6 was obtained.

Control: Z_6, M=3, A=Z_4, (0,1,0,0): delta=3, B=1, B*M=3 (nonzero), Delta_N=<3,0>=Z_4. Note (a/d)^M is trivial here although B^M != 1.

## Claims
1. PROVED (no computation). Doubling law on Z_N, N in {1,2,4}. Positions at time s have the parity of s (N even) and every site of
   parity s+1 is adjacent to every site of parity s (for N=4: the two sites x+-1; N=1,2 trivial). Hence in a non-empty position product
   event no alive walk dies: at a time where A_s contains both (for N=4) sites of that parity, every walk keeps both continuations;
   where it contains one, every walk has exactly one continuation into it (from y=z-1 step right, from y=z+1 step left; z-1 != z+1 mod 4).
   The final selection of a site x keeps exactly the walks there; so |m_S(x,R)|+|m_S(x,L)| in {0} or a power of 2.
   Consequence: PREP fails on Z_4 for every finite abelian A and every gains: e.g. |U|=3, V empty is never realized. Same for Z_1, Z_2
   (there every mask is forced; |U|=1, V empty is never realized because both rails at the site receive walks).
2. PROVED (hand classification). On Z_4 the events with |U|+|V|=2 have exactly one free time s0; before it a single path to site y on
   rail eps, then two walks differing only in steps s0, s0+1 by (RR vs LL, ending at y+2) or (RL vs LR, ending at y), then a common suffix Q.
   Writing e_{eps,R}=a or c, e_{eps,L}=b or d (eps=R or L), the gain ratio of the two walks is:
   Q empty, RR/LL: V/U = e_{eps,L} d/(e_{eps,R} a); Q empty, RL/LR: V/U = e_{eps,R} b/(e_{eps,L} c);
   Q non-empty: those ratios times (c/a or d/b), resp. (a/c or b/d), both walks then on one rail.
   For the control gains (0,1,0,0) in Z_4 this gives V-U in {0,1} (different rails) and same-rail differences in {0,+-1}, never 2:
   exactly the 12 unreached targets of size 2 found by the program (U=0,V={g,g+2}; U={g,g+2},V=0; U={u},V={v}, v-u in {2,3}).
3. COMPUTED (closed exhaustive search, which by claim 1 is complete for N=4): N=4, Z_4, (0,1,0,0): 32/44 targets of size <=2 reached,
   all 120 of size 3 missed; misses unchanged at caps 9,14,30,60 (BFS closed). One-gain carrier d=1 on Z_4: 44/44 of size <=2.
4. COMPUTED, bounded (T<=TMAX, every intermediate state <= KCAP walks; on N odd walks can die so the cap is restrictive, misses are not refutations):
   - A=Z2xZ2, gains ((0,1),(1,0),0,0) (B*M != 0, Delta_N = A): N=3 44/44 (size<=2, cap 8, T<=16), 156/164 (size<=3, cap 9);
     N=5 44/44 (truncated T=10); N=6 44/44.
   - A=Z_4, (0,1,0,0): N=3 32/44 (cap 12 and 14, closed under cap), the same 12 misses as on Z_4; N=5 44/44 (cap 10, truncated at T=10).
   - A=Z_4 one gain d=1 (B*M=0): N=3 40/44 (4 misses: U={u},V={u+1}); N=5 44/44 (truncated).
5. PROVED (small). For N=2m, m odd, x -> x mod m is a bijection from the sites of each parity class onto Z_m commuting with +-1; so Z_{2m}
   and Z_m have the same position product events, walk counts, and M. (Explains equal state counts for N=3 and N=6.)
6. Remark (proved, by Lemma "gains at one length"): the black-box use of the one-gain lemma (Lemma 5.34) on D_h reads only the single
   statistic lambda0 - Mj - n mod q; a homomorphism Z_q -> A sending it to e^j delta^-n with e=(a/d)^M exists iff e = delta^-M,
   i.e. B^M = 1. So for B^M != 1 a new construction (two-track excursions) is needed; I sketched one (two tracks with relative
   distance >= 4 except at the ends, needing N large) but did NOT prove that it composes with the one-gain construction. CONJECTURED only.

Threshold: visibly fails at N in {1,2,4} for all gains (claim 1); N=3,6 (M=3) has bounded misses for the control gains Z_4 (0,1,0,0)
and for the one-gain carrier too, so small-M failure there is not specific to B^M != 1. N=5 reached everything tested (bounded, truncated).
Nothing claimed for M >= 6.

Files (this folder): ringprep.py (program; 'closed' flag added after res_A/res_B were written), res_smoke.jsonl, res_A.jsonl, res_B.jsonl,
res_C.jsonl, res_D_cap30.jsonl, res_D_cap60.jsonl, SHA256SUMS, NOTES.md. Predicates P0 PASS, P3 PASS in all runs, P4 PASS (N=1,2: 1/44).
No package installed. Repository untouched.
