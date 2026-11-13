# Challenger 9 findings (periodic carriers)
- Program periodic_check.py, seed 20261113, results_run1.json; rerun in fresh/ byte-identical.
- 168 carriers generated, 110 satisfy the hypothesis (58 fail: hatD not strongly connected), 103 with r>1, 48 with r != r0, 30 with predicted dim < naive 1+#(U(D)/~).
- All fixed predicates met on all qualifying carriers: L1 L2 L3 L4 Q1 Q2 U1 U2 SOL IND DIM NV A 110/110; NC 103/103; PER 62/62; DP 100/100 (rank mod p, size-limited); C2 104/104 (size-limited).
- No failed predicate in run 1 (only one run made).
- Named examples reproduce: ring 4,6,8 (r=r0=2,U={sign},dim 2); zeta8*H (r=4,r0=1,C0={+-1},U=4 faithful,dim 2, naive 3); C2xC2 (r=2,r0=1,C0={1,b},U={psi(b)=-1},dim 2, naive 3); four-vertex (r=2,r0=1,C0={+-1},U={chi,chi^-1},dim 2) in both readings of the arc triples.
- C2: 506 (psi,lambda) pairs on 90 carriers admit a nonzero c with a consistent rule; in every one the family is zero on fibre multisets (statement of cor (2) holds; c itself need not be 0).
- Wording: proof of cor (2), case psi' != lambda': the two monomials coincide when psi', lambda' are both real; conclusion unaffected.
- Wording: "every instance of (GL) that has a term which is not vacuous is an instance for a family on one layer" is false read literally (two-layer families have non-vacuous terms); it is commentary, the equivalence is proved before it.
- GAP: Lemma lem:classes statement takes all hypotheses from the paragraph above ("as above"); index |C:C0|=r/r0 is taken from the proof of prop:abund(a), whose statement assumes A*A=d (the cited lines do not use it).
