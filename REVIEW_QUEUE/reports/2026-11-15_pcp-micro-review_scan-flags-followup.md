Target: the 1,522 zero-deviation flags of REVIEW_QUEUE/reports/2026-11-15_pcp-micro-review_outlier-scan/outlier_scan_results_run2.json and the three flags left unexplained there; master a8c9608.
Control: is 7 more than 10 max(|median|, 1) from the median of [0 x 9, 7]? Expected no; reported no. Control passed.
Outcome: NONE FOUND.
Reviewer kind: pcp-micro-review run as a sub-agent of the queue session; rechecked as stated at the end. Same model family as the author.

The six files with most flags (1,166 of the 1,522), all EXPLAINED: exact integer site numerators that are 54-77% zero (flight_window, folded_gaussian); a structurally zero projector matrix, 2,442 of 2,808 entries zero (finite_record_memory); an autocorrelation whose largest value 4096 is the lag-0 norm (staircase_echo); a label column (native_gain_ports polynomial_ids); bitmasks with maximum 2^30 - 1, combinatorial counts and an index (gain_abundance). The other about 356 flags are NOT CHECKED.
The three standing flags, EXPLAINED from the checkers' code:
- periodic_force maximum_step_rounding_error 0.393 = pi/8 at sheet order 3; the checker (check_periodic_force.py line 269) requires at most pi/sheet_order, so it passes. The key name says "rounding error" for what is a phase step bound; a naming point only.
- loop_coin_flight angular_error = pi: a control row with the reference scale tripled; the formula at check_loop_coin_flight.py line 143 gives 3 pi/2 - pi/2 = pi by design.
- compact_residue_preparation relative_residue 1.0: the checker requires that exact pattern.
Rechecked by the queue session: the control; the two cited lines of the checkers. Groups file: scratchpad only (groups.txt).
