# NOTES - builder, two-rail starts. Same model family as the director; not independent review. No gate claimed.

## Step 0. CONTROL
Port (tick 1, site 1, rail R), start (R+L)/sqrt2: two words, right step from R (gain a) and from L (gain c).
P = |chi(a)+chi(c)|^2 / 4.  Carrier 1 (a=c=1): P = 1.  Carrier 2 (a=1, c=g, chi(g)=i): P = 1/2.
(The follow-up's 4 and 2 are the unnormalised |chi(a)+chi(c)|^2.)

## Step 1. Hand derivation, to be tested by program
Word from start rail L: G_L(w) = (c/a) a^t (a/c)^e B^l H^m, m counting the first arc (L,s_1).
With gamma = chi(c/a), kappa = conj(alpha) beta gamma, omega = chi(B)^D, eta = chi(H):
 2^t P = |alpha|^2 |S_R|^2 + |beta|^2 |S_L|^2 + 2 Re(kappa conj(S_R) S_L), S_R, S_L real Laurent polynomials in omega.
Candidate list: |alpha|^2, eta, Re omega, Re kappa, Im omega * Im kappa.

## Step 2. Program rails.py written (predicates in docstring before first run).
Run 1 (result_v1.json, empty): CRASH, shape error in my multiplication helper (product not folded mod x^12-1).
Kept as rails_v1_crashed.py. Fix: fold products; predicates unchanged. No predicate had been evaluated.

## Step 3. Run 2 (result_v2.json): exit 0, 15 s, rerun in rerun/ byte-identical.
549 carriers drawn, 260 qualify (eta=+1: 183, eta=-1: 77); N=3..8; 16 events per N.
P1 3629/0 fail, P2 4981/0, P3a 1560/0, P3b 462/0, P3c 462/0, P3d 462/0, P4 462/0 (342 "unreadable" side, 120 "readable"),
P5 130260/0 (230 distinct non-real prepared values). Controls: C1 8 counterexamples of 3696, C2 3289 of 6650, C3 328 of 6650.
Distinct keys exceed distinct signatures per N (e.g. 88 vs 71 at N=3): those are eta=+1 data, where P2 is not claimed.
sha256 rails.py 12bb0819090803e3c88067143ca84097d65c775e41531e42234c43a5d241a1dc
sha256 result_v2.json fc71ae357ae9b241736e95f57bbafe0fbea38bc61f2f6fa15e9d4b6b23327976

## Step 4. Proofs: see FINDINGS.md (written next).
Failed / replaced: (F-a) task's conjecture "reads chi(c/a) combined with arg(conj(alpha)beta)" as a phase: REPLACED;
only Re kappa and Im omega*Im kappa are read (C2: 3289 pairs with equal statistics and different gamma).
(F-b) "depends only on (eta, Re omega, Re kappa)": FALSE, 8 counterexample pairs (C1); third invariant needed.
(F-c) "all of chi(B) is read with two rails": FALSE (C3: 328 pairs, equal statistics, different omega).
Not done: whether |alpha|^2 is readable; eta not real; Lean; N=1,2.
