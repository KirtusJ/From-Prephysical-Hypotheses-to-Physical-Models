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
- step 3: added reported statistic (P keys meeting two delta-cosets); wrote batch.sh. Launch: batch.sh /tmp/claude-0/chal_rk_b1 (MAXSTATES 40000, timeout 400 s each, ulimit -v 3000000).
- step 4: batch b1 (N=3,6 at L=7,L0=4; N=5,10 at L=8,L0=5; ...). N=3/6: all qualifying carriers P3 pass, but only 2 P-keys meet two delta-cosets (weak). N=5: state bound 40000 hit early, 0 P-keys meet two cosets: the test does not reach the winding there (no information about thm:fgtwo content). Observed N=6 identical to N=3 (and expected N=10~5, N=14~7): for N=2M, M odd, the parity-class of sites is fixed by t, and CRT Z_2M -> Z_M maps the walk structure isomorphically.
- step 5: plan v2 (fgtwo_beam.py): equations per site pair (U,V) (Lemma onesite: restricting the last mask to one site is a PP event; the state equation is the sum of the site equations, so the systems are equivalent); beam BFS with at most B kept states per layer sampled with seed 20261113, all children of kept states generate equations. Sampling only adds valid equations from a subset: excess dim is then NOT a counterexample by itself, equality is evidence only.
- step 6: fgtwo_beam.py written; check vs v1 on Z4_kodd_c3 N=3 L=7 L0=4: same unknowns 1704, same rank 1468, dim_proj 2 = pred 2 (site-pair system equivalent as expected). Launch batch2.sh /tmp/claude-0/chal_rk_b2.
