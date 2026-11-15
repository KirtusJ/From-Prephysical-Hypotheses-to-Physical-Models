# micro_Pplus (micro-review, 15 November 2026)

Target: property P+ for Director G's one-gain preparation on rings (masks from `Director_G/check_one_gain_preparation.py::prepare`, propagation my own).
Command: `python3 -B micro_pplus.py result_run1.jsonl` (cwd this folder); rerun in a fresh scratch directory, bytes identical.
sha256 result_run1.jsonl b8951c0c0abc71e839366142dcd11485533ed708fd25e2fbae5a6e9a64b36fe9; micro_pplus.py f19aa7408e9882c22dbbc2fae4a00ab48cfd3524e77b450e225079af8c7ba03a.

Control RLLRR from rail R: 2 left steps, 1 left-after-left.
Runs 8160 (N in 7,9,11,12,13,14,16,24; q 1..4; x in 0,1,N-1; matched False/True), errors 0, qualifying 8160.
Runs with more than one left-step count at the target: 0 (per rail and both rails together).
Degenerate: both empty (192 runs) no walk survives, P+ vacuous; one rail empty (960 each) only the other rail carries a value.
Winding (lifted end - x)/N is 0, 1 or 2 across runs, one value within each run. Lifted end = x mod N in all runs.
Outliers: ticks 7..57, median 35, MAD 7, none beyond 5 scaled MAD; left counts 4..16, median 10, none. No NaN.
Not covered: q >= 5, three or more items per rail, other targets, the line (size None).
Same model family as the author of the request; not independent review.
