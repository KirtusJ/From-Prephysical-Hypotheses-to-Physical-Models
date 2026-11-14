# NOTES form_rails
Step 0 CONTROL: conj(3/5)*(4i/5)*1 = 12i/25, so Re = 0. (python: 0.48j)
Step 1 numeric check (check.py, seed 1, 1000 draws): max abs error R1..R6 all < 2e-13; all six statements true as written.
 R5 sign instance: alpha=1+2i, beta=3-i, gamma=i, w=0.6+0.8i: k=7+i; s=+1: lhs 27.2, rhs(+4 s w.im k.im) 27.2, rhs(-) 20.8;
 s=-1: lhs 32.8, rhs(+) 32.8, rhs(-) 39.2. Sign '+' confirmed.
Step 2 Lean: FPHPM/TwoRail.lean written; first run 'lake env lean FPHPM/TwoRail.lean' exit 0, no warnings, no failed attempts to keep.
 Axioms for R1..R6_general and main: propext, Classical.choice, Quot.sound. No sorry / native_decide / axiom (grep empty).
 Unused hypotheses found: R1 needs no |xd|=1 (general form: factor normSq(xa*xb*xc), no unit hyp); R2 needs no |xa|=1;
 R3 general holds for any xa with factor normSq xa; R4/R5 need only s^2=1; R6 general has factor normSq gamma.
 R5 does need |gamma|=1 and |w|=1.
Step 3 sha256 TwoRail.lean: 70e2780933f515ed7331d806c372ef0724dd56f0b5350a332c9805e7131a3296
