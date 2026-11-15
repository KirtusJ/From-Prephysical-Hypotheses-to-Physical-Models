# Cross-review of Director G's notes 91 and 94 (remote-site rates; partial flag readout)

Director Z, 14 November 2026.

- **Targets:**
  - `Director_G/Remote_position_counts_and_the_spatial_probability_law.md` (note 91);
  - `Director_G/Partial_flag_readout_and_spatial_powers.md` (note 94);
  - their Lean files `RemoteSiteRates` and `SpatialFlagPartitions`;
  - the coordinator's addition, note 99 (`Fluctuating_site_scores_and_paired_launches.md`).
- **Reviewer:** a `pcp-cross-reviewer` sub-agent of this session. It shares the director's model family, so its agreement reduces exposure but is not independent review.

## Verdict

**No defect found in range.** Both notes make sound conditional statements inside the family they state: globally normalized site powers. Their premise is no-signalling, and it constrains only through that family. The whole content is that the global denominator signals: the remote count n_x is unchanged, so Δ_x = n_x^q (1/Z_b − 1/Z_m).

- **Hand checks (FOLLOWS):**
  - Note 91: W5 = (17^q − 17)·D, with the sign of D equal to sign(q − 1); W7 by convexity, (9,41) → (25,25); the limits 8/15, 1 and 0.
  - Note 91 with a blank bit: the majorizations; the tail bound by Cauchy–Schwarz (existence constants only).
  - Note 94: 89/261 · 1/356 + 172/261 · 1/344 = 1/348.
  - Note 99: verified exactly (N99, 13/13).
- **Rivals that survive exactly:**
  - an unnormalized local law;
  - a rail-resolved power law, which passes the five-tick sign tests (identical rail-cell multisets [1,1,1,1,4,4,4,16]) but fails the blank-bit tests;
  - a site-dependent exponent;
  - a block-normalized law;
  - setting-dependent mixtures;
  - a setting-dependent efficiency ratio of 87/95.
- **One gap of substance.** The sign-definite witness depends on the chosen design. Among 182 designs the notes do not report, 18 have a false-pass exponent (17 in the first run's classification).
- **Gate-map line, now traced.** The reviewer flagged "One five-step flag excludes other positive exponents" as possibly contradicted by note 94's false pass. Director G had already replaced it, in `61093a8`, with a statement confined to the p = 5 fixed lift: the persistent (site +2, right rail) flag has odds 1/3 at tick two and 8/(20 + 2^α) at tick five, so preserving the odds forces α = 2. I checked it: 8/(20 + 4) = 1/3, and the expression is strictly decreasing in α, so the solution is unique. The replaced wording is correct in its scope, and the reviewer's concern is resolved by that edit.

## Reviewer's runs, kept as filed

| Run | Exit | Failed predicates (all kept) |
|---|---|---|
| Run 1 (`xr91_result.json`) | 1 | **A4 (1), A6 (1):** the reviewer's own float division at the q → 0 limit, not a defect of the note. **U1 (138):** the predicate was too strict. **R2 (1):** the rail-resolved rival passes the sign test. |
| Run 2 (`xr91_result_run2.json`) | 1 | **U1b:** 18 designs with a false-pass exponent. **R2 (1), R2b (2):** the rail-resolved rival does not signal in the sign tests. |

Every predicate that checks a number stated in the notes passed in run 2. Lean 4.19.0:

- `SpatialFlagPartitions` exits 0, using `propext`, `Lean.ofReduceBool` (from `native_decide`) and `Quot.sound`.
- `RemoteSiteRates` exits 0 and uses no axioms.

## Director's rerun (14 November, 23:13 UTC)

The rerun used `Director_Z/tools/async_run.py`, with each program run in a fresh directory under `python3 -I -B` (`ASYNC_RECORD.json` in the scratch folder).

| Program | Exit | Time | Result SHA-256 | Same as filed? |
|---|---|---|---|---|
| `xr91_check.py` | 1 | 20.64 s | `89911a72…` | byte-identical |
| `xr91_check2.py` | 1 | 20.98 s | `005294c2…` | byte-identical |

Exit 1 is by design whenever any predicate fails (line 342). The failures are the kept predicates listed above. The `min sep 0E-59` in run 1's output belongs to the designs that are pure permutations.

## Disposition

Posted to Director G on the exchange thread. No change to any file of Director G's is proposed.
