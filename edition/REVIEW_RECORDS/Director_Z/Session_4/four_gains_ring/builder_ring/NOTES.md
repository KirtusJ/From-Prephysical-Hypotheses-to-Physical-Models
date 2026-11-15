# NOTES (builder, ring preparation for four gains)
Builder shares the director's model family.

## Step 0: control (by hand, before any program)
Z_6, M=3, A=Z_4 additive, (a,b,c,d)=(0,1,0,0):
delta = a+d-b-c = -1 = 3 mod 4; B = b+c-2a = 1; B*M = 3 mod 4 (nonzero, so B^M != 1);
Delta_N = <delta, M(a-d)> = <3, 0> = Z_4 (all of A). Note (a/d)^M is trivial here,
yet B^M != 1: the hypothesis B^M != 1 does not imply Delta_N != <delta>.

## Step 1: program ringprep.py written (predicates P0-P4 in docstring before first run)
Smoke run res_smoke.jsonl: P0 PASS; N=1,2 reach 1/44 targets (consistent with P4 proof); Z_6 control 32/44 at T<=10, cap 6.

## Step 2: res_A.jsonl, A=Z2xZ2, (a,b,c,d)=((0,1),(1,0),0,0), KT=2, KCAP=8, TMAX=16
N=3: 44/44 PASS (qualifies). N=4: not qualifying (B*M=0, Delta=<delta>), 28/28. N=5: 44/44 (truncated at T=10, 4e5 states). N=6: 44/44.
Observation: N=3 and N=6 give the same number of states (17084). Reason (proved in REPORT): for N=2m, m odd, positions
at time s have parity of s, and x -> x mod m is a bijection on each parity class commuting with +-1: Z_{2m} and Z_m carry
identical position product events and the same M. So small targets do NOT fail at M=3.

## Step 3: res_B.jsonl, KT=3, KCAP=9, TMAX=18
N=3 Z2xZ2: 156/164; N=4 Z4 control gains (B*M=2): 32/164; N=3 Z4 control gains: 104/164; N=4 Z4xZ2 (0,1,0,(0,1)): 64/328.
Typical misses: U empty, V={g, g+2} in Z4 (two L-walks whose gains differ by 2*delta).
Program change after this run (recorded): added 'closed' flag (BFS layer empty = all states under the cap enumerated for every T).

## Step 4: res_C.jsonl, KT=2
Z4, control gains (0,1,0,0): N=3 cap14 closed 32/44; N=4 cap14 closed (369 states, same as cap 9) 32/44; N=5 cap10 trunc 44/44.
Z4, one gain d=1 (B*M=0, not qualifying): N=3 cap14 not closed 40/44; N=4 44/44 closed; N=5 44/44 trunc.
So at N=4 the four-gain control case misses 12/44 small targets where the one-gain carrier reaches all 44 (bounded).
N=4 misses (Z4, gains=n_RL mod 4): U=0,V={g,g+2}; U={g,g+2},V=0; U={u},V={v} with v-u in {2,3}.

## Step 5: res_D_cap30/60.jsonl, N=4: misses unchanged at caps 30 and 60 (closed). Universal labels (Z4xZ4: n_RL, rho mod 4) at N=4:
same-site pairs never have n_RL differing by 2 mod 4 (within cap 10).
## Step 6: proof found for N=4 (see REPORT): walks never die and each time either keeps or doubles: total = 2^f;
size-2 outcomes classified by hand: they reproduce exactly the 12 misses. Z_3 control gains: same 12 misses (cap 12, closed, but on Z_3 walks can die,
so the cap restricts: bounded miss only). Z_3 one gain d=1: 4 misses (bounded).
## Step 7: REPORT.md written
