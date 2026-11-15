# Four or more classes of winding: findings (continuation worker, 2026-11-15)
Same model family as the author and the coordinator; no Agent tool; not independent review.

## PROVED (hand proof in NOTES.md Steps 4-7; identities in Lean)
P1 (correction to Step 2(c)). Let r be even, beta^s = delta^{k0}, sigma = (-1)^{k0}. A sign relation
c_A prod(p_i+q_iX) = eps c_B prod(p'_i+q'_iX) mod X^s - sigma (integer factors, j = 0) is realised as P_A = T_{delta^e} P_B in
N[A], factors (N+p)D0+(N-p)D1+((N+q)D0+(N-q)D1)e_beta, padded with (p,q)=(1,0). The claim for j != 0 with counts (2N,2N)
is FALSE: counts then differ by X^j mod X^s-1 (counterexample: the coordinator's s=4 relation with j=2; check_c.py C2).
P2 (schema, every s >= 3, both twists). Hypotheses of thm:fgprod with r even. If finitely many realised (j = 0)
coincidences have h0 with gcd m(w) (squarefree part of C_s(w) - 2 sigma), then for every k and P^(i):
F_R(P^(1)*...*P^(k)) = alpha prod|P^(i)| + Qbar_s(phi(pi)), phi = reduction mod X^s - sigma,
Qbar_s(e) = c_0 sum e_i^2 + sum_{1<=d<s/2} c_d sum_{i<s} e_i e~_{i+d} + [s even] c_{s/2} sum_{i<s/2} e_i e_{i+s/2},
e~_{i+s} = sigma e_i, with c_{s/2} = 0 when s is even and sigma = -1; and c_{s-d} = sigma c_d, c_{d+s} = sigma c_d.
The same with F_R(. * m), constants depending on m.
P3 (s=4, sigma=+1). One coincidence: A=(7D0+D0e_b)*(D0+D0e_b)^2, B=(D0+3D0e_b)^2*(D0+D0e_b), e_b*A = B;
h0 = -2(r/2)^6 (w^3-4w). Hence Qbar_4 = q sum e_j^2 + c(e0e1+e1e2+e2e3+e3e0) + c_2(e0e2+e1e3), c_2 a new constant.
With e_1 in place of D0 the identity needs beta^4 = 1 (fails for k0 = 2: C3).
P4 (s=4 sigma=-1; s=5, 6 both twists). Two explicit j=0 relations each (pick_*.json, Q5_pick) with gcd(h0_1,h0_2)=m:
the conclusion of P2 holds. Relations: RelSmall2.lean; h0 from factors, m | h0_i and u1h1+u2h2=m: Bezout2.lean.

## COMPUTED (scratch fc2/, all exit 0)
python3 check_c.py res_check_c.json
python3 relsearch.py S SIG BF BL NREL OUT, (S,SIG) in all of 4..8 x +-1, (BF,BL)=(10,200),(30,1000); relpick.py same args
python3 verify_pick.py ver_small2.json RelSmall2.lean pick_s{4,6,5}_sig-1_BF30_BL1000.json pick_s{5,6}_sig1_BF30_BL1000.json
python3 bezout_lean2.py Bezout2.lean (same five pick files)
lake env lean FourClasses.lean / RelSmall2.lean / Bezout2.lean: exit 0, axioms within propext, Classical.choice, Quot.sound.
No single relation with h0 = const*m found for s=4 sigma=-1, s=5, 6 (boxes as above).
s=7 (sigma=+1; -1 by X -> -X) at (BF,BL) = (30,1000),(80,4000),(200,1500),(400,600) and s=8 sigma=-1 at (200,1500):
only the trivial relation X (h0 = 0). s=8 sigma=+1 at (30,1000): 20 relations, gcd degree 57 (j=0) / 13 (all), not m.

## Failed / stopped (kept in run_2026-11-15c/)
Step 2(c) as written (j != 0): false, see P1. relpick s=8 sigma=+1 at (80,4000) and (100,2000): stopped by time limit
(exit 143 after 854 s; empty result files kept). FAILED_ver_small_typeerror.json, FAILED_RelSmall*.lean: program bugs, fixed.

## Not checked / open
s >= 7: no relation with gcd m found; no proof that none exists; no general argument for all s.
Whether a single coincidence suffices for s=4 sigma=-1, 5, 6. Theorems rest on thm:fgprod and its inputs as drafted.
Tool installed: python-flint 0.9.0 (pip --user), for exact nullspace, LLL and gcd in Q[w].
