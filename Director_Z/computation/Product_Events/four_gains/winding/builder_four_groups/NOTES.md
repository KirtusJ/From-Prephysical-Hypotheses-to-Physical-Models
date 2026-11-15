# Builder notes: four groups on three levels (append-only)

Builder is a sub-agent of the author's model family; nothing here is independent review. No gate is passed by anything here.

## Step 0. Control
prop:threegroups: the stage that needs M >= 8 rather than 7 is, by the proof's own account, the run of the first
group (A = G_1) from 2 to 6: its last refused candidate is 7, which for M = 7 is the source at 0.
Just before the source is removed the stocks sit at relative deficits A = G_1 at 6, B = G_2 at 4, C = G_3 at 2.

## Step 1. Necessary condition checked from cor:tp
Levels: R has G_3 at l, G_1 at l+M; L has G_2 at l+M, G_4 at l+2M. With l_0 = l: u_0=g3, u_1=g1, v_1=g2, v_2=g4,
so the sequence w is (w_1..w_4) = (g3, g2, g1, g4). Minor with rows i=0,1 and columns c=3,4:
w_3 w_2 - w_4 w_1 = g1 g2 - g3 g4 >= 0. Equality is allowed by the corollary and is attained:
multiply the pair (G_3 on R at l ; G_2 on L at l+M) (mode (ii), G_1 empty) by a two-level multiset e_1 + beta e_1
(lem:twist of the draft): g1=g3, g2=g4.

## Step 2. Abstract packet model (established before the interruption; scratch programs, exploration only)
In the deficit frame a "packet" is the set of walks at one residue of the deficit modulo M (one site); its content is a
polynomial in X (X = one lap = level +1) with multiset coefficients. Window order: packets P_1..P_k listed by residue
in [p, p+M); the cyclic successor of P_k is X^{-1}-shifted P_1, i.e. merging P_k upward into P_1 gives P_1 + X P_k.
One tick = each packet goes right (stays), left (moves up one residue) or both (copy); arrivals at one residue merge.
So every event is a sequence of: copy a packet to the adjacent place, merge adjacent packets (cyclically), delete.
Packets never cross. Final pair at a site: R-packet P and L-packet Q, adjacent, Q just below P.
Target of the task in this notation: window (P, Q) with P = G_3 + X G_1, Q = G_2' + X G_4' (Q at residue p-2+M).

Moves on a two-packet state (P below Q in the window), T any multiset of powers of delta (one copy per element):
  (alpha) Q += T P      (copy of P moved up into Q)
  (gamma) P += T Q      (copy of Q moved down into P)
  (beta)  P += X T Q    (copy of Q moved up into the next lap of P)
  (delta') Q += X^{-1} T P
Counts (a + bX, c + dX): alpha and gamma keep ad - bc. Euclid: if a >= c subtract Q from P (then b >= d follows from
ad <= bc); if a < c and d >= b subtract P from Q; if a < c and d < b the state is the BASE family
  P = A + X(B + E1),  Q = (delta^e A + E2) + X delta^e B
obtained from stocks (A, E2, E1, B): cyclic merge B onto A, copy P, merge copy with E2, merge E1 into P's upper level.
So in counts every (g3,g1,g2,g4) with g3 g4 <= g1 g2 is reducible to the base family or to three groups.

Exploration results (scratch, abstract model, counts only, delta = 1):
 - forward BFS (<=6 packets, total <=13, with deletion): the two-packet count profiles with total <= 9 and <= 6 entries
   are exactly the totally non-negative ones (agrees with rem:tpprod(c)).
 - profile of the test pair of task (3): w = (1,2,3,5,1) (u = 1+3X+X^2 on R, v = 2X+5X^2 on L; total 12).
   It IS allowed by cor:tp (Hurwitz determinants 13 and 1, roots of Y^4+5Y^3+3Y^2+2Y+1 all in the left half plane)
   but NOT reached by the forward BFS, and NOT reducible in a complete reverse search (rev.py: un-copy moves only,
   no bound on the number of packets). Same for (1,2,3,3,2) and its reverse (total 11).
   If the reverse search is complete (argument: a predecessor state may be assumed to have no packet that is wholly
   deleted, so totals do not increase backwards and the search is finite), then the test pair occurs on NO ring,
   and the question of rem:tpprod(b) "does every pair allowed by cor:tp(iii) occur on large rings" has answer NO.
   TO DO: write the proof of completeness, rerun as a fixed program with result file.
 - a new operation for gains not in the list above: R-packet P and L-packet Q at one site, both stepping both ways,
   give (P+Q at e, P + delta Q at e+1). For delta = 1 it is copy+merge. This is the extension step itself.
