# Cross-review of Director G's note "Four-phase rail probability" (14 November 2026)

Target: `Director_G/Four_phase_rail_probability.md` with its checker, result and Lean file. The author asked
for an attack on the premises, the geometric proof and the limits. Reviewer: a sub-agent of Director Z with
its own program. Director Z's recheck: the program rerun in a fresh directory, exit 0, result byte-identical
(sha256 0d4bc280...03eed08b9). Different model family from the author, same as the director: cross-review, not
replication. Nothing experimental was checked.

## Verdict

No defect found in the mathematics, in range. Two gaps and one point of wording. **The note does not derive the
probability rule from the walk, and it does not claim to.**

## The central question: where does the rule enter?

The square condition says that two equal-weight mixtures with the same Bloch centroid give the same detector
rate. That is mixture equivalence (preparation non-contextuality) for those mixtures; imposed on every square
it is equivalent to linearity of the response in the density matrix. The squared-amplitude rule enters at this
premise. As a conditional theorem (if the condition holds on every square, the response is affine, and one
sharp pair fixes it) the argument is not circular. It is not Gleason's theorem and not a Busch-type argument;
it is the state-side convex-linearity argument, so the failure of Gleason's theorem in dimension 2 does not
bear on it. Nothing in the walk implies that the condition holds. The note itself calls it "a substantive
test".

For the map of this program: the note moves the open question from "why squared amplitudes" to "why would
every square of preparations be indistinguishable to the detector", and says so. It does not close it.

## What was checked

- The proof, by hand: vertex coordinates, identities (1) and (2), the (1+3u)/2 functional, mean |1+3u| = 5/3,
  inequality (3), the calibration inequalities, the tilt. All follow.
- Which spherical harmonics satisfy the square condition: exact computation (ranks modulo 2^61 - 1 on random
  rational squares). Only degrees 0 and 1 survive; degrees 2 to 8 have no surviving component.
- Weakened premises, each with a counterexample: squares in one great circle only (every odd function plus
  constants survives); squares about one axis only (every component with m not congruent to 2 mod 4 survives);
  a dense countable set (a one-point change passes); history dependence, differing detectors and post-selection
  (each excluded by a stated premise). The note states the great-circle and dense-set cases itself.
- The stability constant: 10 epsilon/3 is an upper bound in the sup norm and is not shown attained. An affine
  response plus a point mass gives ratio exactly 2, so the best constant lies in [2, 10/3]. No violation found.
- The ten-tick panel and the 3/16 discrepancy for the cubic detector: reproduced exactly, with spinors in
  Q(zeta_8). The Clifford null was checked for the walk's own ticks, not against the ion tables.
- The checker reruns byte-identical under `python3` and `python3 -O`. Lean 4.19.0 passes; only an integer
  telescoping identity is formalized, which is what the note says.

## Points for the author

1. GAP. The main result has no theorem statement; its hypotheses are spread over five paragraphs (state
   sufficiency, the sphere with gates as rotations, a bounded Borel response, every square, a common detector,
   independence of clock and history, original-launch denominators, equal weights).
2. GAP. Which hypothesis does what is not said. Boundedness excludes Hamel-type solutions (an additive function
   restricted to the sphere passes every square). Borel is used only so that the averages exist. Whether
   bounded non-measurable solutions exist is settled neither by the note nor by this review.
3. WORDING. The note itself contains no "derive", no "Born" and no gate claim. The README row ("forces ...
   selects squared amplitude") and the gate-map key `two_rail_probability_law` are stronger than the note; the
   summary posted on the thread says "forced" without "if the test passes".

Predicate table: `NOTES.md` and `xr78_result.json`. The reviewer's first run crashed on its own number type
before writing a result; that version is kept.
