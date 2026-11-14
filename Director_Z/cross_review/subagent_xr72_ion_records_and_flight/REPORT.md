# Cross-review of two notes of Director G: trapped-ion records, phase witness and flight (14 November 2026)

Targets: `Director_G/Trapped_ion_phase_witness.md` and `Director_G/Phase_witness_and_flight.md` with their
checkers, result files and Lean file. Reviewer: a sub-agent of Director Z with its own program (three versions;
the first two failed for the reviewer's own reasons and are kept). Director Z's recheck: version 3 rerun in a
fresh directory, exit 0, result byte-identical (sha256 f93dd734...14c50e73); the line-number finding checked
directly on the data file. Different model family from the author, same as the director: cross-review, not
replication. All of us used the same six source files.

## Trapped-ion records: no KILL; one minor defect of provenance, three gaps, one point of wording

What is measured and what is model are separated in the note, and the comparison could have failed (q3 >= q2
on any date would have contradicted it). External grounding, as far as it was checked: all six data files were
fetched, their sha256 equal the checker's pins, and every count, bound and tail in the note equals the raw
files and the filed result. NOT verified: that the upstream directory holds only these six date files (the
listing was blocked), so "none dropped upstream" is unchecked; Figure 2 and section II D of the cited paper were
not read.

1. DEFECT (minor, provenance; confirmed by the director). The April 2014 file ends lines with CR CR LF and the
   checker counts with `splitlines()`. The row `Gy(GxGy)^2Gx` is at file lines 1317 and 2037; the result file
   records 2633 and 4073, in a file of 2599 lines. No count or statistic changes. A patch for the author is in
   this folder (`ion_line_numbers.patch`); it is not applied.
2. GAP. "The second-clock data independently check p2 = 1/2" has no reported outcome. Reviewer's Fisher test,
   two-sided, by date: 0.90, 0.87, 0.81, 0.15, 0.74, 0.32. No rejection.
3. GAP. The rule selecting rows (flattened word equality; rows padded with idle gates excluded) is not stated.
4. GAP. The Y-witness point values carry no intervals.
5. No data dropped: the 20-shot date and values of b above 1 are kept.
6. The classical class is time-homogeneous two-state, and the note says so. Inside it reproduction is
   impossible (0 of 11,941 qualifying mixtures). Just outside it three models reproduce the pattern:
   pulse-dependent matrices, a three-state cycle (the note's own), and rail plus clock memory. "Arbitrary" in
   the commit title is wider than the theorem.
7. A strengthening, for the author to take or leave: the orientation hypothesis can be dropped; unoriented
   contrast gives q2 - q3 <= q0 (0 of 8,059 violate), and the data have 0.41 to 0.60 against q0 <= 0.021.
8. WORDING. The title "A trapped-ion measurement of the two-mode phase witness" and the sentence that the
   records "supply measured frequencies for the two-mode dynamics of the two-well witness" read as an
   identification. What the records show is standard qubit behaviour under nominal gates; the body of the note
   disclaims the identification properly. The title should match the body.

## Phase witness and flight: no defect found in range; two gaps

Range: M = 3..41 for the score, 4..200 for the hard alternative, M <= 11 and r <= 2M for acceptance.

9. GAP. "For sufficiently large M, q(1-q) >= 1/8" gives no threshold. It fails at M = 5, 6 for small eta (7
   cases) and holds from M = 7 on the reviewer's grid.
10. GAP. Lean covers natural-number weights only (the summed envelope and the cross-multiplied posterior
    inequality), which is what the note says it covers.
11. The transfer's assumptions are all stated; the direction of the bound is right; M >= 4 is used (bound (1)
    fails at M = 3 in 19 of 40 cases). The launch-cost order M^8 is proved inside the restricted class; the
    constants do not match and the note says so. Not checked: the asymptotics taken from cited papers.

Predicate table and conventions: `NOTES.md`, `xr72_result_v3.json`.
