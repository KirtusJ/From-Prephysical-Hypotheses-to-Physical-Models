# Challenger notes, cor:maskorbit (z27)
Same model family as the director; not independent review.

## Step 0: control
N=5: M = N/gcd(N,2) = 5. Coin (1,1,1,-1): all moduli 1; ad = -1, -bc = -1, so ad=-bc: evaluated coin, yes.
u = b c / a^2 = 1. (omega = u^M = 1, s = (-1)^(M-1) = 1; fork P = 2^-(M+1)*(2+2) = 1/16 for alpha=1.)

## Step 1: program written (predicates P0-P7 in docstring before first run); sha256 above in shell log
7b5863ac801533d3683b52c1598415b710e05d687c85c5aa6c5e14a9b59f988d  orbit_attack.py

## Step 2: run1.json (exit 0, 5.7 s). All P1, P2, P2b, P2fork, P3 hold for N=1..9 (16 qualifying coins of ~720-5040 candidates per N, 15-18 events, T=M+3).
P4: rail phase / conjugation change stats for start (1, i) in 14-16 of 16 per N (expected; sharp-only).
P5: eta=+1 no differences; eta=i: N=3 8/13, N=4 3/6 equal-Re(u^M) pairs differ (outside the corollary, eta=-1 there).
P6: N=1,2 orbit statement holds in range (corollary's N>=3 not needed for this statement).
P7: equal stats confirmed; relating maps need zeta=+-i, g=-+i; rail phase -1 only for target (1,1,-1,1), not for (1,-1,1,1).

## Step 3: all four u=-1 coins in {+-1}^4 (N=4): from (1,1,1,-1), zeta=i pairs with g=-i when target a=+1, but with g=+i when target a=-1; rail phase -1 needed for 2 of 4 targets.
Rerun run2.json byte-identical to run1.json (sha256 21904e92...); overwrite refused (exit 1).
