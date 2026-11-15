# Challenger on the product lemmas and theorems (draft subsection), 15 November 2026

Two contexts did this work: one on the session model, stopped by the usage limit after its hand checks (its notes are the first part of `NOTES.txt`), and one on Opus that continued from those notes. Both are of the author's model family; this is not independent review. Neither could write a report file; the second returned its report as its final message, and the director files its content here.

Control: answered correctly by both ((A_i): v in C_{i+1}; (B_i): u in C_i).

Findings:
- lem:twist: FOLLOWS. GAPs, closed in the draft: N >= 3 was not in the statement; "occurs alone" comes from the proof, not the statement, of lem:fginv; the last sentence had no proof.
- lem:twolevelabs: the proof of thm:fgadj uses only the three hypotheses of the lemma. DEFECT of wording, closed by the challenger's patch: after the first correction the statement assumed r even and then made a claim for r odd.
- lem:symquad: NONE FOUND; both dimensions computed independently for k = 2, 3, 4 (6, 10, 15).
- thm:fgprod: the product step, the scalar transfer as rewritten, part (i) with an empty G_2, and the independence of the coefficients from k all follow. DEFECTs of wording, closed: the range of the undetermined constants (c_2 to c_{s-1}, not c_{s-2}); r even against the r odd clause. GAP, closed: that alpha_m does not depend on k was only implicit.
- thm:fgthree: NONE FOUND. The identity e_beta * A = B was expanded by hand; the family c_d = 2 Re u^d takes equal values at the two products for d = 2 to 8 exactly when u^3 = sigma (exact computation, both signs); the sign on eps_2 eps_0 agrees with thm:fgadj; the statement for general m needs nothing unstated.
- cor:pplus8: NONE FOUND given prop:threegroups as stated; wording about M <= 5 corrected.
- Kept failures: run 1 ended with exit code 2 on an error of its own program; run 2's predicate P7 failed 2 of 2 through a fault of the predicate; one start in the wrong folder ended with exit code 1 without overwriting anything.
- Not checked by it: prop:threegroups itself; cor:pplus8 by simulation; Lean.

Director's recheck: `python3 check2.py result_run3.json 20261115` rerun in a fresh directory, exit 0; the result file agrees with the challenger's in every field except the seconds. The patch was applied with `git apply` after `--check`. The identity and the two inequalities of the induction are also checked in Lean (`Director_Z/lean/WindingCoincidence.lean`, exit 0, axioms propext and Quot.sound only). Run 1 (program, result file, output before the crash) is filed under `run1/` as it stood.
