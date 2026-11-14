Target: the review queue's own instruments: REVIEW_QUEUE/lib/pcplib.py and two report programs that use it (challenge_prop_abund_cor_abund.py, micro_cor_composition_cor_return.py), at commit b07cff6. Asked for by the director's note of 13 November (late).
Outcome: DEFECT in the queue's checks (7 of 23 planted errors passed), repaired in part on the queue's own side; no finding about the paper.
Reviewer kind: pcp-chaos run as a sub-agent of the queue session (as a general agent reading .claude/agents/pcp-chaos.md); mutants were planted in scratch copies only. The queue session rechecked what is stated at the end. Same model family as the author.

Counts: 23 mutants (17 in the library, 2 in each program, 2 in result files). CAUGHT 16, SURVIVED 7, EQUIVALENT 0. Each mutant's expected catching predicate was written down before its run (PREDICTIONS.json).

Of the 16 caught
- 4 were caught by a crash, not by a predicate (lift dropping the gain, strongly_connected always true, two errors in group addition).
- 1 was caught in the wrong direction: walk_counts dropping length zero turned a failed predicate of program 2 (X1) to met.
- zero_sum always true and norm_preserving without the orthogonality test were caught by program 3 only; the output of program 2 did not change. Program 2's hypothesis test "A*A = d exactly" therefore rests on the library alone.
- Both altered result-file digits were caught by rerun and comparison.

Survivors
- null_space threshold 1e-9 changed to 1e-3, and to 1e-15: neither program calls null_space.
- null_dim gap 1e6 changed to 10, and to 1e15: all recorded gaps exceed 1e14, and the predicate K3 it feeds was already not met in the stored run, so its flag did not move (failures went from 19 to 53 unnoticed).
- norm_preserving without the test of equal out-degrees: no irregular carrier is built by either program.
- strongly_connected testing forward reach only: every lifted digraph in the programs is regular, where forward reach suffices.
- program 3, the bound of predicate RB changed from d^(t-1) to d^t: the violation count stays zero; and RE is hard-coded.

Other findings
1. The result file of program 2 depends on the number of linear-algebra threads: with one thread two recorded gap values differ from the stored file. A rerun-and-compare can therefore fail with no error present. The dimensions and flags do not change.
2. Program 2's stored run has three predicates not met (K3, N1, X1, each with a follow-up). An error that touches only those moves no flag. Predicates that are known failed should be superseded in a new program, not left as the only guard.
3. period() has no guard for a digraph that is not strongly connected; an exception from it is what stopped three mutants.

Done by the queue session on its own files
- Added REVIEW_QUEUE/lib/pcplib_selftest.py (written by the sub-agent, read and run by the queue session): 22 known-answer tests with negative controls. It passes on the library (exit 0) and, per the sub-agent's table selftest_vs_mutants.txt, fails on 16 of the 17 library mutants; the one it does not catch is the null_space threshold at 1e-15.
- Not yet done: a test system with eigenvalues between 1e-15 and 1e-9; a guard in period(); a shared bound variable and a computed control in program 3 (the filed program is a record and is not edited; the next program should do it); pinning the thread count in programs that record floating values.

Rechecked by the queue session: the self-test's text; that it exits 0 on the library in the repository; the table of mutants against the self-test as a file. The 23 runs themselves were not repeated.
Cost reported by the sub-agent: about 11 minutes, 16 tool calls.
