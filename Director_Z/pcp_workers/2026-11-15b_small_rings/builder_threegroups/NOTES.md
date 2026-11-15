# Builder notes: Proposition prop:threegroups for M = 3, 5, 6, 7

## CONTROL (answered from the paper text alone, before any other work)
In mode (i) the walks of G_2 end on R at level l (lambda = l) and those of G_1 end on L at level l+M.
So the numbers of left steps differ by exactly M, and G_1 has the larger number (lambda(G_1) - lambda(G_2) = M).

## Step 1 (reading)
Inputs read: PAPER_TEXT_subsections.tex (Four arc gains; winding subsection, prop:fgonelevel, P^+_delta,
prop:threegroups with proof), PAPER_TEXT_draft_winding_products.tex (thm:tp, cor:tp). No other file read.

## Step 2 (reduction, before any program)
Facts used (proofs to be written in FINDINGS section below):
(R1) survival of a walk depends only on its site; after t steps the site is t-2e (e = left steps), and e -> t-2e mod N
     is a bijection from Z_M onto the sites reachable at time t (N=M odd, or N=2M). So masks = arbitrary subsets of Z_M
     of deficits, and the problem is the same for N=M and N=2M.
(R2) walks do not interact; a packet = the walks at one deficit residue; a packet at residue j has candidates j (R) and
     j+1 (L). Deterministic packet: exactly one candidate in the mask.
(R3) lift order: no overtaking. While the source S lives all stocks lie in (S, S+M) in integer deficit; G_1 one lap
     above G_3 in one packet forces S dead before that merge; creation order is A=G_1, B=G_2, C=G_3, cyclic order S,C,B,A.
Plan: packet-model search (program tg_search.py), then replay on Z_N for N=M and N=2M (tg_replay.py).

## Step 3 (packet-model search, tg_search.py)
Runs (each in a fresh /tmp/claude-0/builder_tg_runK/, command `python3 tg_search.py runK.jsonl <Ms>`):
- run1 (M=3,5,6,7,8,9; RESTRICTED=True, stocks may never take an increment): exit 0 (a first launch under
  /usr/bin/time failed with exit 127, time not installed). FAILED PREDICATE KEPT: P2 false for every M, including
  the control M=8. Cause: a stock just created by an L step from S must take L next unless it receives another
  deposit, so "no increment on stocks" is too strong. Result file not kept (rerun superseded by run2).
- run2 (restricted off, weight psi_k): exit 0; phase 3 never reached for any M. BUG (kept): normalisation required
  label C at position 0 in phases <=3.
- run3: bug fixed; P3 false for all M including M=8. BUG (kept): FINAL states detected by phase tuple, never matched.
- run4 (M=3,5,6,7,8,9,10): exit 0. sha256 run4.jsonl 54cf78f8caeff725abf6918a0fb150cf2250ac7733e64bfed12b83f5310be16e,
  tg_search.py 7a84b2d170a2605fc104af5de78f3879bc2128a69a736d2ec169a24249584022. State cap 2,000,000 not hit
  (largest graph 1994 states at M=10). Hypothesis M>=3: 7 of 7 qualify.
  P3 (modes i and ii) TRUE for M=7,8,9,10; FALSE for M=3,5,6.
  M=6: good SCCs in phases 1,2; phase 3 has 11 nodes and no SCC with a deposit edge and gcd 1.
  M=5: good SCC in phase 1 only; phase 2 has 14 nodes, no good SCC; phase 3 one node.
  M=3: phase 1 has 4 nodes, no good SCC.
  This is a statement about the packet model only (single source, at most one copy in transit, no split of a stock,
  no junk packets, mixed-rail packets may not step left in phases 1-3). Not an impossibility on the ring.
Next: replay an explicit M=7 schedule on Z_7 and Z_14 with gains.

## Step 4 (replay on Z_N, tg_replay.py)
Planner bugs found and fixed (kept): (a) deposits accepted into dead-end nodes (fixed: a deposit must land in the
good SCC of its phase); (b) the creation node itself is outside the good SCC (fixed: creation must land in a node
that reaches the good SCC by non-deposit edges). Earlier runs rp1-rp3 superseded.
Run rp4 (fresh dir /tmp/claude-0/builder_tg_rp4), commands `python3 tg_replay.py rp_M{M}_n300.jsonl {M} 300`,
M = 7, 8, 6, 5, 3, all exit 0. 332 requests each for odd M (N = M and 2M), 316 for M = 6, 8 (N = 2M).
Q0 qualifying: all requests. Results:
  M=7: planner 332/332, Q2 (exact replay on Z_7 and Z_14) 332/332.
  M=8 (control): 316/316, 316/316.
  M=6: planner 81/316, all 81 replayed exactly; every success has G3 empty; every request with G3 nonempty fails
       in the planner (no good SCC in phase 3 of the packet graph).
  M=5, M=3: planner 0/332.
sha256: rp_M3 0f52bd89..., rp_M5 5ab647ef..., rp_M6 981303d5..., rp_M7 dc70b931..., rp_M8 1a126e5d...,
tg_replay.py 1680217e87ec1f91cc98d7d65fd697be7af75bc4d0e12013833a57440fceec8b.

## Step 5 (bounded exhaustive search over ALL events, q = 1, tg_exh.py; no packet model)
Commands (fresh dir /tmp/claude-0/builder_tg_ex1, all exit 0):
  python3 tg_exh.py ex_W4.jsonl 4 16 40 3 5 6 7     sha256 a7e18565...
  python3 tg_exh.py ex_W7.jsonl 7 30 80 3 5 6 7     sha256 90dd1d1b...
  python3 tg_exh.py ex_W12_M3.jsonl 12 40 200 3     sha256 88b038e1...
In every run the frontier emptied before the layer bound, spread bound never hit, state cap never hit.
Results: M=5,6,7: every count profile with total <= 7 is met in both modes (238 of 238).
M=3: missing in both modes e.g. (n1,n2,n3) = (1,2,1), (1,2,3), (1,3,2), (1,4,1), (2,3,1), (3,2,1), ... (154 of 908 missing at W=12).
KEY LEMMA found (proof in FINDINGS): shrinking every mask to the sites visited by the final walks keeps the final
walks and leaves at most n = (number of final walks) walks at every time. So the count-pruned search is COMPLETE for
profiles of total <= W. Hence M=3, profile (1,2,1) is impossible (computed + lemma), for every q (take all exponents 0).
