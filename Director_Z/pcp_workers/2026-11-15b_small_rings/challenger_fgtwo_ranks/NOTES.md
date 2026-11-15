# Challenger notes: Theorem thm:fgtwo on rings with M = 3,5,6,7 (control M = 8)
Author's model family; not independent review; no gate is passed.

## CONTROL (from the paper text alone, answered before any run)
s = 2, r even, k odd: the theorem gives c = 0 and q free, so the consistent site-independent rules on
M(Delta_N) are the real combinations of TWO linearly independent functions: the count |m| and the one square
eps_0^2 + eps_1^2 = |sigma_chi(m)|^2 (chi(delta) = -1, chi(beta) = +-i; one pair {chi, chi^-1}).
(For k even: three, count, (eps0+eps1)^2, (eps0-eps1)^2; r odd: one, the count.)

## Log
- step 1: read PAPER_TEXT_ppcons.tex and PAPER_TEXT_subsections.tex (fgsolve, fgtwo, threegroups). Control written.
- step 2: wrote fgtwo_ranks.py (predicates in docstring). Trial (dense fmpz) on Z4_kodd_c3 N=3: L=6 L0=4 passed (dim 2 = predicted 2); L=8,10 FLINT dense matrix out of memory (exit 134). Replaced dense ranks by exact sparse elimination over Q (same predicates; rank method changed only).
