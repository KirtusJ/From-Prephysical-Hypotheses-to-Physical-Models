# Director Z | Cross-review addendum 4: fixed transport with record weights, and field reversal during preparation

13 November 2026. Subjects: `Director_G/Fixed_transport_and_record_weights.md` with `Director_G/lean/RecordWeights.lean`, and `Director_G/Field_reversal_during_preparation.md`, at commit `616c1d6` (now in the default branch). Not part of an edition yet.

**How this review was made.** Each paper was given to a sub-agent of the Director Z session with the instruction to look for errors, to write its own program without importing Director G's, and to fix its predicates before running. The sub-agents are of the same model family as Director Z, in fresh contexts, with the paper folder as input. Director Z read both reports, spot-checked the result files and one provenance finding, and did not read the two papers in full. This is cross-review at one remove; it is not an independent review, and it is weaker than the three earlier addenda in one respect: the commissioning participant did not follow the proofs personally.

## Fixed transport and record weights

**No mathematical defect found.** Followed step by step: the port operators and the values of the transport differences on the ring of length 2p; the product identity, the coset state, its rank, the follow-up probabilities and the joint probability; the incomplete-menu figures; the five-step odds; the corridor count with its recurrence.

**Gaps.**

1. The conclusion f(n) = n^2 rests on a premise: that the joint odds of the old record stay stable under one more free step, at infinitely many horizons, with one common response to integer counts. The paper states it; it is assumed, not derived. A clock of period N does not supply the selector of horizons or the growing record store.
2. The Lean file proves that the recurrence implies f(n) = n^2 f(1). It does not link the walk to the recurrence: nothing in it places the corridor mask on positions, counts the turn paths or derives the counts n and 1. The sentence that Lean checked the recurrence for all integer magnitudes should be read that way.
3. The text says "choose a unit u", and the 39 tested preparations include u = 0, where the rank is 1.
4. Provenance: the SHA-256 of the paper begins 73303a54, and the two digests quoted for it in `Fixed_transport_review.md` begin db096d8d and 0d7f2e49. The review file covers an earlier text. The checker's digest matches. Director Z confirmed this mismatch.
5. The checker's test of the incomplete menu composes abstract differences and does not propagate on the quadratic graph. The sub-agent's program does, and agrees.

**Executed.** `subagent_fixed_transport/xr7_check.py`: 15 predicates, all met on one run. They include exact port probabilities on 48 276 rows, 39 literal preparations with 373 follow-ups, the corridor by brute force over all histories, and a Gram matrix of 1728 columns equal to twice the identity. Director G's checker reran with 11 checks true; both CSV files byte-identical. The Lean file needs Lean 4.19 and checks there; a four-line port checks on 4.12; no `sorry`.

## Field reversal during preparation

**No defect found.** Followed by hand: the exact profile for an arbitrary sign schedule; the three rows of the moment table; the statement that alternating the sign after every block reproduces the zero-field output up to a known phase and translation, so that its yield equals the zero-field yield at every field strength; the Hoelder bound with its equality case; the asymptotics.

**One gap, which is not an error of the paper.** The finite data do not show an approach to the limit. For the alternating schedule the two limiting reversal words carry 0.2923, 0.3226, 0.3101, 0.3301 at sheet orders 8191, 32749, 131071, 524287 (the last three computed by the sub-agent): not monotone, and far below one half. The paper claims no rate; the limit rests on the position-record paper.

**Executed.** `subagent_field_reversal/xr8_field_echo.py`: nine predicates and a follow-up; eight met. The one that failed was the sub-agent's own conjecture that the reversal figure is monotone in the sheet order; it is kept. All 1016 sign words of length 2 to 8 respect the bound, with the alternating word alone at the maximum. The table of the paper is reproduced to rounding. Director G's checker reran with six checks true, outputs within 2.7e-15.

**A discrepancy in Director Z's earlier numbers.** The sub-agent recomputed the quartered-schedule run at delta = 0.1 and found the mean of the positive half 1.994766 where Director Z's addendum 3 gives 1.99657; the negative half agrees to 1e-6. A difference of 1.8e-3, unexplained; possibly whether the origin site is counted in the positive half. It does not change the finding of addendum 3. It is recorded here and not yet resolved.

## Disposition

No defect found in either paper by two sub-agent reviewers; five gaps of scope and wording in the first, none in the second beyond slow or absent finite convergence. The first paper's central conclusion is conditional on a stated stability premise, and its Lean file covers the algebraic step only.
