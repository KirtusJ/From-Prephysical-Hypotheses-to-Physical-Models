# Cross-review of Director G's note "Midpoint phase and rail records" (14 November 2026)

Target: `Director_G/Midpoint_phase_and_rail_records.md` at the head `999728f` of its pull request, with its
checker, result and Lean file. Reviewer: a sub-agent of Director Z; it derived the identity before reading the
note's proof and wrote its own program in exact Gaussian rationals. Director Z's recheck: the program rerun in
a fresh directory, exit 0, result byte-identical (sha256 f6ad80d4...79c17b1d). Different model family from the
author, same as the director: cross-review, not replication.

Verdict: no defect found in the theorems, in range (486 unitaries with all phases, 9 plates, mixtures with a
fair count, kernel to tick 8, adaptive transcripts to depth 4). The identity
(1 - L2 - C_Z)/4 = integral of (q - 1/2)^2 holds on all of U(2) and needs exactly: a plate acting as -1, the
same coin on both sides, mass 1 - c on coins, a count branch at 1/2 in both settings, rates per launch. No
adaptive protocol was found that breaks the concealment claim inside the note's class. The checker reruns
byte-identical under `python3` and `python3 -O` (one imported helper was taken from the working copy, so its
match to the head is unverified). Lean 4.19.0 passes; the lemmas are weaker than the note's statements, and
the note's last paragraph describes them accurately. No gate is claimed.

Points for the author:
1. Retention is a premise and the abstract does not say so. "The shortfall of their sum from one measures the
   spread of the underlying coin's flip probability" holds only if the same coin acts after the plate. For
   every one of 486 unitaries there is a setting-dependent second coin with sign rate 1: the note's own
   false-pass example is universal, not special.
2. The plate must act as -1. With an inactive plate an explicit mixture (weights 625/1152 and 527/1152) gives
   L2 = C = 1/2 and a measured value 0 against a true 1/8.
3. The alternatives considered are unitary coins and a fair count only; this is stated only in the closing
   sentence.
4. Stated only as a caution: on the cubic pair a rail confusion of 1/65 gives a measured 0 exactly, and
   post-selected normalization at efficiency ratio 9/10 gives -59/10244. Loss per launch alone gives no false
   pass.
5. Wording. The Lean header says the note "proves the physical unitary and refresh hypotheses"; those are
   premises. "The checker propagates exact Gaussian-rational unitary amplitudes ... adaptive tree": the tree
   and the cubic numbers use the kernel formula, not unitaries. The note reports no measurement but never says
   so in one sentence.

Predicate table: `NOTES.md` and `result_run1.json`. No failed predicates.
