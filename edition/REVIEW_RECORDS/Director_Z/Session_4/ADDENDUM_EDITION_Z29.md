# Director Z, fourth session | Twenty-fifth addendum: edition Z29

15 November 2026, UTC. Same session and participant. Root Review: G1, OPEN. No ontology is selected. No gate changes state.

## Assessment Z4-AC (FOCUSED): the four-gain preparation on rings

**Result.** New in G10: Proposition 5.52. On rings with M ≥ 6 and (bc/a²)^M = 1, the preparation reduces to Director G's Lemma 5.34, as on the line, so Theorem 5.51(i) holds there.
- The recoding ratio is a function of length and end vertex exactly when (bc/a²)^M = 1.
- A second prefix, N steps right, multiplies the ratio by a^N. It removes the parity obstruction that a challenger of edition Z28 found for odd N.
- The case (bc/a²)^M ≠ 1 stays open. Used as it stands, Lemma 5.34 controls one statistic of the walks at a vertex, and the gain there depends on two.
- On rings of 1, 2 and 4 sites no preparation exists for any gains: every position product event leaves 0 or a power of 2 walks at a site. A builder found this and the participant checked it by hand.

G10 now has 53 labelled statements and 63 pages.

**Checks.**
- A challenger followed the proof end to end on rings of 3 to 8 sites, with a brute-force stand-in for Lemma 5.34. 22,449 targets passed, none failed, and 19,971 were beyond its search bound.
- The ratio is constant in all 10,226 cases with (bc/a²)^M = 1 and breaks in all 22,574 with (bc/a²)^M ≠ 1.
- Corrections applied: two hypotheses moved into the statements, the reason the prefixes are unique corrected, and one slip fixed.
- The participant reran the challenger's program in a fresh folder; the output was byte-identical.
- The ring algebra, including (a/d)^M = δ^(−M) when (bc/a²)^M = 1, is already in `PrepReduction.lean` (edition Z28).

**Limits.**
- Rests on Lemma 5.34, which is Director G's and is not reproved.
- The case (bc/a²)^M ≠ 1 is open.
- The reviewers are of the participant's model family.

## Cross-review of Director G (#260 to #262)

- **#262:** a gap of substance. The tangent certificate needs the competing rules to pool the unread tag. When the tag is scored branch by branch, 161 exact mixtures without q = 1 reproduce both rates. The participant reran the solver byte-identical.
- **#260:** no defect found in range.
- **#261:** not assessed in depth.

Sent to Director G.

Finding Z-146.
