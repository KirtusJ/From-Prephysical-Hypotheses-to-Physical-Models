Target: all JSON result files under Z4_COMPUTATION/, Director_Z_cross_review/ and Director_G/results/ at commit e53742c.
Outcome: DEFECT in one recorded column (an instrument artefact that enters no predicate); otherwise NONE FOUND beyond failed predicates already kept.
Reviewer kind: pcp-micro-review run as a sub-agent of the queue session, its report rechecked in part by the queue session (stated below); same model family as the author. Not independent review.

Scanner: outlier_scan.py in the folder of this name, rules fixed in its docstring before the first run; result file beside it. Rerun by the queue session in a fresh directory: the per-rule counts are identical; the files are not byte-identical because the root paths were given in another form.

Scanned: 46 JSON files (19, 11, 16), all parsed.
Counts: NaN or infinity 0. Failed predicates 62 (24 distinct; 40 are per-record repeats in band_preparation_first_oracle.json). Robust deviation above 10 (a conventional screening cut-off, not a derived tolerance): 1117 values in about 100 columns; 535 columns tested, 218 skipped for zero spread. Residual-like 115 (13 distinct). Self-contradiction rule: 0, but no record had the shape the rule reads, so that rule tested nothing.

DEFECT (rechecked by the queue session in the file and the program)
- Z4_COMPUTATION/Continuation_Selection_Results.json, predicate S5, rows "staircase_period_64" (and others): rms_width = 4096.04 at 13 samples against about 17 elsewhere. N = 4096 in that program (the sub-agent wrote 8192; corrected here). Cause: verify_continuation_selection.py line 154 subtracts centroid(cur), which lies in [-N, 0], from site coordinates in [-N/2, N/2) without wrapping; when the packet centre is on the positive side the difference is off by N. The displacement column on the same line is wrapped and is not affected. rms_width enters no predicate. Whether any text quotes these widths was not checked.

Failed predicates
- Z4 files, 15: Bounded_Order_Confinement C1, C1b; Continuation_Selection S5 (two); Degree_Two_Quadratic_Rule Q1; Fourier_Blocks_Any_Degree A1, A3; Kernel_Rules K1, K2, K3; Kernel_Rules_General G4; Kernel_Rules_General_Followup G2b; Modulus_Rules_and_Local_Spectra M1, L3; Ray_Error_Scaling E1. None is marked kept or superseded inside its own file. G10 says in its text that failed predicates of the kernel, Fourier, degree-two, staircase and ray computations are kept; a predicate-by-predicate match against the paper was NOT CHECKED.
- Crosscheck_Director_G X4, Two_Rays B4, xr8_result_run2 P8: EXPLAINED (recorded as kept in the cross-review texts, per the sub-agent; not rechecked).
- Director_G band_preparation_first_oracle.json and orientation_oracle_first_run.json: EXPLAINED (retained failures named in verification.json, per the sub-agent; not rechecked).

Other numeric flags (sub-agent's reading, not rechecked)
- Kernel_Rules K3 / K3b oddness_defect 2.0: EXPLAINED, rows with hypothesis false.
- Fourier A3 / A3b residual 856.6: EXPLAINED by key name only (control rows).
- periodic_force rounding errors up to 0.39 and bound 81.7: EXPLAINED, coarse-sheet controls.
- field_echo yield_ratio down to 1e-5 in 66 of 160 profiles: NOT CHECKED.
- folded_pair maximum_characteristic_residual 0.11 to 0.45 with all checks true: NOT CHECKED (which check uses it was not found).
- record_selection determinant 0.433 and reduced_purity 0.625: NOT CHECKED.
- Remaining deviation flags: parameter sweeps and counts, judged by column name only.

Not checked: CSV files; Director_Z_cross_review/subagent_fixed_transport/ (no JSON); result files under edition/; individual deviation values outside the columns named.
