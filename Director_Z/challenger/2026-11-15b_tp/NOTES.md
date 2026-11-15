# Challenger notes, thm:tp / cor:tp (appended per step)
Step 0: read draft lines 1-48 and body lem:fgkappa, lem:winding, lem:windingrails, position product events.
CONTROL: (ii) n0*n2 <= n1(n1-1): (1,1,1) 1<=0 excluded; (1,2,1) 1<=2 not excluded; (2,2,2) 4<=2 excluded; (2,3,2) 4<=6 not excluded.
Step 1 (hand check of proof): lattice/periodicity/sources/sinks/crossing/LGV follow for M>=2 (N=3: M=3; N=4: M=2 sinks consecutive integers, strict). 
Cor (i): second case indices: c=2j+3,c'=2j'+2, c<c' iff j'>=j+1, and lemma condition l'-l>=2M with l=l0+jM, l'=l0+(j'+1)M iff j'>=j+1. Draft says j'>=j+2: omits minor u_{j+1}v_{j+1}-v_{j+2}u_j (adjacent columns). Also only rows i'=i+1 treated; rows with i'-i>=2 give shifted-by-r inequalities, consequences not literally the lemmas.
Cor (iii): 'Equivalently' omits condition that g=gcd(u,v) has only real nonpositive roots. Counterexample u=v=X^2+X+1: u/g=v/g=1 (vacuous alternation) but W=(1+Y)(Y^4+Y^2+1) has root e^{i pi/3}. Also, without sign/nonnegativity of coefficients interlacing is insufficient (u=1, v=-(X+1)).
Step 2: v1 program had a bug (sympy count_roots counts distinct roots) -> 14 spurious P2 FAIL, 2 spurious P5 FAIL, then mpmath NoConvergence crash (exit 1); kept as tp_check_v1_failed.py and res_N3-4_T10_cap6.txt. v2: N=3,4 T<=10 cap 6 exit 0, no failures.
