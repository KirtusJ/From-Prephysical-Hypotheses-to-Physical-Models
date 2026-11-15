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
- step 7: batch2: Z8_r4_kodd and Z4Z2_r4_keven on N=3 L=9 L0=6 (full, no beam) reached the extra-solution branch (dim_proj > predicted) and crashed: fmpq_mat has no nullspace() (exit 1, empty result files kept). Patched both programs (rref-based nullspace; DIMS printed before). Rerun in /tmp/claude-0/chal_rk_r4.
- step 8: r4 reruns (/tmp/claude-0/chal_rk_r4), N=3 full enumeration L=9: Z8_r4_kodd L0=6 dim 3 > pred 2 (candidate), L0=5,4 dim 2 = pred; Z4Z2_r4_keven L0=6 dim 6 > pred 3, L0=5,4 dim 3 = pred. Excess only at L0 = L-3: looks like a bound artifact; launched Z8_r4_kodd L=10 L0=6 to test.
- step 9: batch2 beam runs on N=5,7,12,16 mostly crashed in the extra-solution branch (old nullspace bug) because MAXSTATES counted all children and stopped at layer 8 < L or with L0 >= layers done: P was the whole frontier, so those excesses carry no information (FAILED RUN DESIGN, kept). N=5 runs that finished (bound hit at layer 8, L0=7) P3 pass for Z2Z3_rodd, Z2Z2_keven, Z4_kodd_c3.
- step 10: batch3.sh with beams sized so that L layers finish (children ~ beam*2^N per layer), L0 = L-4.
- step 11: batch3 beam runs: Z2Z2_keven N=5 L=12 L0=8 dim 7 > pred 3; Z2Z3_rodd N=5 dim 69 > pred 1. FAILED DESIGN (kept): with random sampling most Ext multisets of an equation have no equation of their own, so P is under-constrained; beam excess carries no information. batch3 stopped.
- step 12: width-capped enumeration (BEAM=-W): all PP events with |A_s| <= W, closed family, no sampling. Check: W=3 on N=3 equals full.
- step 13: Z8_r4_kodd N=3 full L=10 L0=6: MemoryError under the 3 GB cap (exit 1, 314 s): the L0=L-3 excess on N=3 remains unresolved by full enumeration.
- step 14: width W=2: Z2Z2_keven N=5 L=12 L0=8: 355001 states (no bound hit), 16999 unknowns, |P|=305 with 41 P-keys meeting both delta-cosets, dim_proj 3 = pred 3, P2 pass. W=3 N=5 L=10 L0=6: bound 2e6 hit, dim 3 = pred 3 (only 2 two-coset P keys). Launch batch4.sh (W=2) on the rest.
- step 15: batch4 (W=2): N=3 L=12 runs died (memory: SystemError/OOM, exit 1) or timed out (exit 124); N=5 Z4_kodd_c3 L=12 L0=8: dim 2 = pred 2; Z2Z3_rodd, Z8_r4_kodd N=5 timed out (600 s). Stopped the N=7 L=13 jobs (would time out); batch4 driver stopped, Z4Z2_r4_keven N=5 left running. Launching batch5: N=7 L=11 L0=7, N=12 L=10 L0=6, N=16 L=11 L0=8 (W=2), 3 in parallel.
- step 16: batch5 (W=2): N=7 L=11 L0=7 Z2Z2_keven, Z4_kodd_c1 and N=12 L=10 L0=6 Z8_M6_kodd, Z4Z2_M6_keven: dim = pred, but 0 P-keys meet two delta-cosets, so they do not probe the winding (no information on thm:fgtwo content). Need batch6 with L0 >= M+2.
- step 17: W=2 N=3 L=10 L0=6: Z8_r4_kodd dim 2 = pred 2, Z4Z2_r4_keven dim 3 = pred 3 (the L=9 L0=6 full-enumeration excess does not survive one more layer on the W=2 subfamily's P keys; full L=10 not run: memory). N=16 control L=11 L0=8 W=2: dim 2 = pred 2. Launched batch6 (N=7 L=13 L0=9; N=12 L=12 L0=8).
