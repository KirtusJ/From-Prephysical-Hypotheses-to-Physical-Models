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
