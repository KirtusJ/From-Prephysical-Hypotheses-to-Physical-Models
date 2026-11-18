Target: the 356 zero-MAD flags of the repaired outlier scan left unchecked by the follow-up (`2026-11-15_pcp-micro-review_outlier-scan`, `..._scan-flags-followup`).
Control: median and MAD of [1,2,2,3,100]. Expected 2 and 1; got 2 and 1. Passed.
Outcome: NONE FOUND. All 356 flags (48 file/column groups, listed in `groups.txt`) are expected structural values: exact counts, field numerators, indices, powers of two in mostly-zero tables, wall-clock seconds, against a zero or one baseline.
Reviewer kind: pcp-micro-review sub-agent of the queue session; same model family as the queue session. Not independent review.
Predicates P1 (356 flags remain of 1,522), P2 (each group classified), P3 (producing program opened for any candidate) all met.
One candidate, explained: `Director_G/results/fixed_ring_moments.json`, panel 12 (D=8, q=21), column `binary64_cosine_estimates_true_value_one` reads 1.0 x8, -0.0, 2461597696.0, -5.03e18. The file's precision note and `Director_G/check_fixed_ring_moments.py` lines 132-166 build it deliberately in rounded binary64 to show the recursion breaking down; the exact integer inversions are correct. Reported only; Director G's file.
With this, every flag of the repaired scan is checked. Not rerun by the queue session.
