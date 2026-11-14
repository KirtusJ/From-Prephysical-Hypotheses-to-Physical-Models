# Cross-review xr256

## Control
1/27 = 0.0370 (0.037037...); words of length 3 over a 3-letter alphabet: 3^3 = 27.

Reviewer shares the director model family (Claude); cross-review, not independent replication.

## Notes
- HEAD of repo is 3dd8ee0 (brief said 4232b3c); target files present.
- Author checker rerun from copy /tmp/claude-0/-home-user/1b3e59a6-be8f-5e36-be7c-26b1885eea91/scratchpad/xr256/rerun/ve with python3 -I -B -O: exit 0, stdout sha256 166ed158...2d41, one line "Verified all 27 positive leaves...". Inputs byte-identical to repo. No stored result file to compare (checker only prints).
- Lean 4.19.0: AddressedCoinEmbedding.lean exit 0 (1.6 s). Axioms: mass_conjugate [propext]; first_write none; all_words, selected_conjugate_maxima, selected_weights [Lean.ofReduceBool] (native_decide; disclosed in note). Under 4.12: exit 1, List.flatMap missing (version, not a note failure).
- Lean formalizes: flipH (all H -> -H) weights == conj of specified for all 64 words; support 27/37; total 512; greedy conjugate maxima on (2,3,1); l,m,h values; m^2<lh; m>2l. NOT formalized: flipping only the addressed H (relative phase) == flipping all H; any power model; 1/27 bound; P_m<=P_l; AM-GM; theta<1/2 from logs; J>1/100; mixture/Hoeffding; analyzer scaling.
- Own program xr_check.py (v1 sha 1e2b1665..., crashed in P7b overflow at q=-100, kept as xr_check_v1_crashed.py and run1/results_xr.txt; v2 sha 9622cfee... fixes negative-q scaling only). run2: exit 0, P1-P6 PASS, results_xr.txt sha 7345770b...6d24; run3 byte-identical; overwrite refused.
- P5: 4000 conjugate carriers, 4000 qualify, 0 failures; min 27*P_l = 1.000000000000000 (q=0, tight); max P_m/P_l = 1.0 (q=0); min J = 0.011685 = (A-M+B)/27.
- P6: 4000 specified carriers, 4000 qualify, 0 failures; min J = 0 (q=1 and q=inf, global spec max outside prefix).
- P3: conj(eps=+1) == spec(eps=-1) on all 64 words; branch amplitudes agree up to one global sign per tick (-1 on H ticks, +1 after writes).
- Probes: block mode (joint power on first two writes) also >= 1/27 since (2,3) is unique conj depth-2 max (234.51 vs 109.25); negative q: min J = -3.07e-5 (exclusion needed); 64-cell q=0 convention: J = 0.00493 < 1/100.

## Verdict
No defect found in range. GAPs: Lean steps rest on Lean.ofReduceBool (disclosed); the analytic chain (power models, 1/27, AM-GM, J>1/100) is not formalized. Wording edges: unlabeled conjugate child lists; title vs the eps condition; J>1/100 relies on the q=0 positive-support convention.

## Director's recheck (Director Z, 14 November 2026, 23:4x UTC)

- I reran the reviewer's `xr_check.py` in a fresh folder: exit 0 after 1 s. Its `results_xr.txt` is byte-identical to the reviewer's runs 2 and 3 (SHA-256 `7345770b62ddcc6ebeef57e0751fecc24d239744da6760fa5bc8264456126d24`).
- I reran the author's checker from master (`python3 -I -B -O check_embedding_selection.py`). Its output's SHA-256 is `166ed158…`, the same as the reviewer's.
- I checked wording point 1 against the note's line 15. The paragraph is about the conjugate path, so the weights are the conjugate ones. The fix is a label only.
- Both of us are from the same model family, so this is not independent review.
