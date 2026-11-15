Target: every JSON result file changed since 13 November 2026 under Director_G/results/, Director_Z/ and REVIEW_QUEUE/reports/ (547 paths; 545 exist; list.txt), at master a8c9608.
Control: FAILED in the first run, then passed after a repair. The first run is void as a scan and is kept as a finding about the queue's own scanner.
Outcome: DEFECT in the queue's instrument (two faults, repaired in REVIEW_QUEUE/lib/outlier_scan.py); for the files, no finding is verified (flags listed below are unchecked).
Reviewer kind: pcp-micro-review run as a sub-agent of the queue session; the repair and the second run were done by the queue session. Same model family as the author.

Control: a column of twenty 1s, one 1.0001 and one 1000, with a failed predicate beside it. Expected at least two flags. The scanner of 13 November raised one (the predicate). It missed 1000 because it skips every column whose median absolute deviation is zero, and 3819 of the 19623 columns in this tree are such columns. Second fault: the scanner stops with OverflowError on integers too large for a float, which occur in this tree.
Repair (REVIEW_QUEUE/lib/outlier_scan.py, from the sub-agent's copy): integers with |x| >= 1e300 are not tested by the deviation rule; a column with zero deviation flags any value farther than 10 max(|median|, 1) from the median (the factor 10 is the same screening convention as the deviation cut, not a derived tolerance). With the repair the control raises both flags (control_run2.json).

Second run (the repaired scanner on the same 545 files; exit 0): R1 (NaN, infinity) 0; R2 (failed predicate) 44771 values; R3 (deviation) 50868, of which 1522 from the zero-deviation fallback; R4 (residual-like) 137; R5 0 (it found only 3 records of the shape it reads). These are counts of flagged values, not of distinct places.

Flags the sub-agent judged, from the first run
- Failed predicates EXPLAINED as kept: ledger_bytes L3 ("kept" in its FINDINGS); Director_G/results/verification.json, 15 retained failures; results_xr39.json (field failed_predicates_kept); the chaos run's planted failures; two_scale_record.json first_fail, a census key, not a predicate (false positive of the rule).
- UNEXPLAINED: periodic_force.json maximum_step_rounding_error 0.393 against a median 5e-7 (about pi/8: perhaps a phase step under a rounding name); loop_coin_flight.json angular_error = pi with every other value 0; compact_residue_preparation.json relative_residue 1.0 with every other value 0; the state counts of the small-ring wildcard files (probably growth with ring size).
- NOT CHECKED: folded_pair.json residuals 0.339; the deviation clusters in common_ray_source, native_multiscale_selector, clock_bandwidth, shared_mass_force, confined_loop, xr19 and results_gauge_bl (probably sweep parameters).
New in the second run, NOT CHECKED: the 1522 zero-deviation flags, most in flight_window (266), finite_record_memory (218), staircase_echo (195), folded_gaussian (194), native_gain_ports (172), gain_abundance (121). Columns that are mostly zero with a few nonzero entries produce such flags; whether any is an error was not looked at.

Not checked: the flags marked so; whether the other failed predicates are acknowledged; the two deleted paths.
