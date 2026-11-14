# MUTANTS: chaos run of 14 November 2026 on pcplib.py and two queue programs

Every file named here is a scratch copy. Nothing was written under the repository. Seed 20261113 recorded; mutation sites were chosen by hand, no random choice was made.
Verdict rule, fixed before reading the runs: CAUGHT = a predicate's `met` differs from the baseline rerun, or the program crashes; SURVIVED = no `met` flag moves although a true statement was made false; EQUIVALENT = no claim altered.

Counts: CAUGHT 16 / SURVIVED 7 / EQUIVALENT 0 of 23. Of the caught, 4 are crashes only (L04, L10, L11, L12) and 1 is a failed predicate turning to met (L05).

Originals (sha256):
- lib: `96890af9a5c055fc154ee32057cc451157765b86194949f0172813f5d37833f3`
- p2: `0cc2cc6f1d96a48ee9d48905fb73c13d27098479e143eba8e0bcb0e74fbb0206`
- p3: `5488d1eb293fabd04e0bbfaabcdec51d46c5a1ec80ba097f98badfe495c53c37`
- r2: `b95adff5a072c8a67e1bdb5ce371dcdf315991c0071088e8a7c228130940b470`
- r3: `5ef4fc639e1c50e6cde49740a41cd4153edab9997be03fc1bbded5620907991a`

Baseline: both unmutated copies rerun in `base/`; result bytes equal to the stored files (program 2 only with default BLAS threads).

| id | mutated copy | change | made false? | prediction before run | verdict | what happened |
|---|---|---|---|---|---|---|
| L01 | `mutants/L01/lib/pcplib.py` (sha256 370e28a5af92, original 96890af9a5c0) | zero_sum always True | yes | P2: no predicate (baseline h1 = 261/261, every built carrier already passes; K2's zero-sum half goes vacuous) -> SURVIVE; P3: CA (norm-preserving characters become 0..7) and RC (non-unitary characters in U) | **CAUGHT** | P3: CA, RC flip. P2: nothing (bytes identical to single-thread baseline). As predicted. |
| L02 | `mutants/L02/lib/pcplib.py` (sha256 d8a72e5f53dc, original 96890af9a5c0) | norm_preserving skips the orthogonality test | yes | P2: SURVIVE (h1 already 261/261); P3: CA, RC | **CAUGHT** | P3: CA, RC flip. P2: nothing (bytes identical). As predicted. |
| L03 | `mutants/L03/lib/pcplib.py` (sha256 1daf0ed37746, original 96890af9a5c0) | period returns 1 and one class | yes | P2: H (with_r_ne_r0 = 0), C2 (none found); X1 would but is already not met in the baseline; P3: CA (r//r0 = 1) | **CAUGHT** | P2: H, B1, C1, C2 flip; P3: CA. Predicted H, C2, CA; B1 and C1 not predicted. |
| L04 | `mutants/L04/lib/pcplib.py` (sha256 f3320c9f546f, original 96890af9a5c0) | lift drops the gain in the successor | yes | P2: H (no carrier strongly connected; h1_and_h2 = 0), B1 (pairs = 0), K1; P3: CA (not strongly connected), RC (no carriers) | **CAUGHT** | by CRASH only, both programs (TypeError inside period on an unreachable vertex), not by a predicate. Predicted H/CA. |
| L05 | `mutants/L05/lib/pcplib.py` (sha256 867ce6bc9d8d, original 96890af9a5c0) | walk_counts drops length 0 (index t now holds length t+1) | yes | P2: SURVIVE (B1, C1 are existence over lengths, B2 holds at every length, X1 already not met); P3: not called -> SURVIVE | **CAUGHT** | P2: X1 flips False -> True, i.e. the planted error makes a recorded FAILED predicate pass (the baseline failure of X1 is at length 3 only). Noticed only by comparing met flags with the stored file; all_met stays False either way. Predicted SURVIVE: prediction wrong. P3: not called. |
| L06 | `mutants/L06/lib/pcplib.py` (sha256 295c7313733c, original 96890af9a5c0) | Ring.conj returns its argument | yes | P2: K4 (a^2 is not a solution; baseline K4 met) ; K3 changes but is already not met; P3: Ring not used -> SURVIVE | **CAUGHT** | P2: K4 flips. P3: Ring not used. As predicted. |
| L07 | `mutants/L07/lib/pcplib.py` (sha256 fe2ee3bf039b, original 96890af9a5c0) | Ring.N returns |a|^4 | yes | P2: K4 (|a|^4 does not solve the equations); K3 should NOT notice (keys are in bijection with |a|^2); P3: SURVIVE (not used) | **CAUGHT** | P2: K4 flips; K3 unchanged as predicted. P3: not used. |
| L08 | `mutants/L08/lib/pcplib.py` (sha256 257aa12f37f5, original 96890af9a5c0) | null_space threshold 1e-9 -> 1e-3 | yes | P2, P3: null_space is not called by either program -> SURVIVE, result bytes identical | **SURVIVED** | null_space is called by neither program; bytes identical. Caught by patch/pcplib_selftest.py. |
| L09 | `mutants/L09/lib/pcplib.py` (sha256 9978272b4de7, original 96890af9a5c0) | null_space threshold 1e-9 -> 1e-15 | yes | P2, P3: not called -> SURVIVE, result bytes identical | **SURVIVED** | null_space is called by neither program; bytes identical. ALSO passes patch/pcplib_selftest.py. |
| L10 | `mutants/L10/lib/pcplib.py` (sha256 8a69e16ad58b, original 96890af9a5c0) | strongly_connected always True | yes | P2: crash in period (level None on unreachable vertices) or A3; N1 changes but is already not met; P3: CA unaffected, RC carriers 29 -> 30, possibly crash-free -> SURVIVE in P3 | **CAUGHT** | P2: CRASH only (same TypeError in period). P3: no met flips, RC carriers 29 -> 30 (only rerun-compare sees it). |
| L11 | `mutants/L11/lib/pcplib.py` (sha256 b3430aa165b3, original 96890af9a5c0) | gadd ignores the modulus entirely | yes | P2: crash (KeyError in lift), not a predicate; P3: crash in the return-bound part (block_carrier + lift); CA uses hand-written gains reduced mod 8 so lift on E8 also crashes | **CAUGHT** | by CRASH only (KeyError in lift), both programs. As predicted. |
| L12 | `mutants/L12/lib/pcplib.py` (sha256 47f877aaa3f7, original 96890af9a5c0) | gadd reduces every component by the first modulus | yes | P2: A3 or H/h1 on groups Z2xZ4, Z2xZ6, Z4xZ2 (or KeyError for Z4xZ2); P3: cyclic groups only -> EQUIVALENT there | **CAUGHT** | P2: CRASH only (KeyError in lift, group Z2xZ4). P3: cyclic groups only, bytes identical (equivalent there). |
| L13 | `mutants/L13/lib/pcplib.py` (sha256 9b55b9fe9fd8, original 96890af9a5c0) | null_dim gap 1e6 -> 1e1 | yes | P2: SURVIVE (recorded gaps are 1e14..1e16, far above both); bytes identical; P3 not called | **SURVIVED** | bytes identical: all recorded gaps are above 1e14. Caught by the self-test. |
| L14 | `mutants/L14/lib/pcplib.py` (sha256 3f56d7881325, original 96890af9a5c0) | null_dim gap 1e6 -> 1e15 | yes | P2: K3 failure count changes (gaps 1e14..1e15 now give dim 0) but K3 is already not met in the baseline -> predicate verdict unchanged, SURVIVE at predicate level; rerun-compare notices | **SURVIVED** | K3 failures 19 -> 53 but K3 is already not met in the baseline, so no met flag moves; rerun-compare notices. Caught by the self-test. |
| L15 | `mutants/L15/lib/pcplib.py` (sha256 c7ce5ca2ec50, original 96890af9a5c0) | period: closed-walk length off by one | yes | P2: A2/A3 or H or a ZeroDivision crash (g = 0); P3: CA (r) | **CAUGHT** | P2: A3, B2, B1, C1, C2, K1; P3: CA. |
| L16 | `mutants/L16/lib/pcplib.py` (sha256 3969249a06c2, original 96890af9a5c0) | norm_preserving skips the equal out-degree test | yes | P2, P3: every carrier built is regular -> SURVIVE, bytes identical | **SURVIVED** | bytes identical: no carrier with unequal out-degrees is ever built. Caught by the self-test. |
| L17 | `mutants/L17/lib/pcplib.py` (sha256 03812e5dcd3f, original 96890af9a5c0) | strongly_connected tests forward reachability only | yes | P2, P3: all lifts are d-in d-out regular, where forward reachability implies strong connectivity -> SURVIVE, bytes identical | **SURVIVED** | bytes identical: every lift is d-in d-out regular. Caught by the self-test. |
| P01 | `mutants/P01/reports/2026-11-13_pcp-challenger_G10_prop-abund_cor-abund/challenge_prop_abund_cor_abund.py` (sha256 3237e08044e5, original 0cc2cc6f1d96) | program 2, B1: count comparison reversed (>= N becomes <= N) | yes | B1 fails for carriers where the full coset first appears with counts above 25 (large groups); if short lengths already show the coset with small counts it SURVIVES | **CAUGHT** | B1 flips. |
| P02 | `mutants/P02/reports/2026-11-13_pcp-challenger_G10_prop-abund_cor-abund/challenge_prop_abund_cor_abund.py` (sha256 3117bc05fa51, original 0cc2cc6f1d96) | program 2, A2: divisibility reversed (r divides r0) | yes | A2 fails on the 17 carriers with r != r0 | **CAUGHT** | A2 flips. |
| Q01 | `mutants/Q01/reports/2026-11-13_pcp-micro-review_G10_cor-composition_cor-return/micro_cor_composition_cor_return.py` (sha256 d61d56efd638, original 5488d1eb293f) | program 3, CD: sign of the c term in the multiplicativity equation | yes | CD (solutions become (0,0),(1,0),(0,-1)); CE too | **CAUGHT** | CD and CE flip. |
| Q02 | `mutants/Q02/reports/2026-11-13_pcp-micro-review_G10_cor-composition_cor-return/micro_cor_composition_cor_return.py` (sha256 309f7f8dfe47, original 5488d1eb293f) | program 3, RB: bound weakened from d^(t-1) to d^t | yes | RB cannot fail (N_t <= d^t always); equality_cases is counted on a separate line and stays 7432 -> SURVIVE, bytes identical; RE is a constant, not computed | **SURVIVED** | bytes identical: RB cannot fail under the weakened bound, equality_cases is computed on another line, RE is a constant and not computed. |
| R01 | `mutants/R01/reports/2026-11-13_pcp-micro-review_G10_cor-composition_cor-return/micro_cor_composition_cor_return_results.STORED_MUTANT.json` (sha256 6193325e5180, original 5ef4fc639e1c) | stored result of program 3: one digit | record altered | rerun and byte comparison | **CAUGHT** | rerun and byte comparison. |
| R02 | `mutants/R02/reports/2026-11-13_pcp-challenger_G10_prop-abund_cor-abund/challenge_prop_abund_cor_abund_results.STORED_MUTANT.json` (sha256 131100c065b0, original b95adff5a072) | stored result of program 2: one digit | record altered | rerun and byte comparison | **CAUGHT** | rerun and byte comparison (with default BLAS threads; see side finding 1). |

## Survivors and the check that would have caught each

- L08, L09 null_space threshold: not exercised by these two programs. Check: a known-answer test of null_space (L08 caught by the self-test in 1 s; L09 needs a system whose true null eigenvalues come out between 1e-15 and 1e-9 of the largest, not found in the time).
- L13 null_dim gap 1e1: a negative control with a singular-value ratio of 1e3 (self-test, 1 s).
- L14 null_dim gap 1e15: K3 is not met in the baseline, so nothing guards its failure count. Check: rerun-and-compare, or the self-test.
- L16 norm_preserving without the degree test: a negative control carrier with unequal out-degrees in predicate H (one line) or the self-test.
- L17 strongly_connected forward only: a negative control digraph 0 -> 1, 1 -> 1 (self-test).
- Q02 RB bound d^t: take the bound from one variable for both the violation and the equality count, and compute the control RE through the same line instead of writing it as a constant.

## Side findings

1. Program 2's result bytes depend on the BLAS thread count: with OMP_NUM_THREADS=1 the K3 `gap` floats differ from the stored file (351802984320487.3 against 356239575721047.25, two entries). A rerun-and-compare on another machine can fail with no error present. See `base/.../*_results.RERUN1T.json`.
2. Program 2's baseline has three predicates not met (K3, N1, X1; kept as failed predicates). An error that only touches those is invisible at the level of `met` (L14), and L05 turned X1 to met.
3. Four mutants were stopped by an exception in `period` or `lift`, not by a predicate; `period` has no guard for a digraph that is not strongly connected.

## Files

- `build_mutants.py` (plants, writes `PREDICTIONS.json` before any run), `run_one.py`, `analyse.py`, `RESULTS.json`, `jobs.txt`
- `mutants/<id>/lib/pcplib.py`, `mutants/<id>/reports/<name>/<program>.py`, `*_results.RERUN.json`, `status.RERUN.json` (records `pcplib.__file__`; local in all 40 runs), `stdout.RERUN.txt`
- `patch/pcplib_selftest.py`, `patch/add_pcplib_selftest.patch`, `selftest_vs_mutants.txt` (fails on 16 of 17 library mutants; passes on the baseline)
