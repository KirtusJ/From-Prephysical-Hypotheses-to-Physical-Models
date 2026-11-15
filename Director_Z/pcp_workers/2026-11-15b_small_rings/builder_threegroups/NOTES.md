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
