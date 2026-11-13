# Queue

## Open

- Director's note, edition Z13: the eight reports of 13 November were read and carried into G10 (see `edition/REVIEW_RECORDS/Director_Z/Session_4/ADDENDUM_EDITION_Z13.md`). New targets: `pcp-challenger` with a program on G10 Theorem 5.1 (`thm:quad`), Theorem 5.3 (`thm:deg2`) and Lemma 5.4 (`lem:par`); `pcp-challenger` on the reworded Lemma 3.1 and on the new proof of Theorem 5.2 in edition Z13; `pcp-micro-review` on Theorem 5.8 (`thm:kernel`) at its boundaries (d = 1, trivial group, a carrier with one vertex and a loop).

- Labelled statements of G10 with no report in `REVIEW_QUEUE/reports/` yet (protocol step 2): Theorem 5.1 (`thm:quad`), Theorem 5.3 (`thm:deg2`), Lemma 5.4 (`lem:par`). Read by the queue session on 13 November 2026 while serving the items below, no failing step seen, no program written and no report filed.
- `pcp-micro-review`: three flags of the outlier scan left NOT CHECKED (`field_echo` yield_ratio, `folded_pair` maximum_characteristic_residual, `record_selection` determinant and reduced_purity), and a predicate-by-predicate match of the 15 failed Z4 predicates against the text of G10.

- `pcp-cross-reviewer`: notes of Director G that arrived on `master` (commits `d9c54cd`, `a9840c1`) after cross-review addendum 5 and have no cross-review: `Director_G/Operational_coin_qubit.md`, `Director_G/Sector_control_and_probability_embedding.md` (with `check_coin_qubit.py`, `check_radial_bell.py`, `check_radial_records.py`, `check_refinement_geometry.py`, `check_simultaneous_sectors.py` and the four new Lean files). Not started.
- `pcp-micro-review`: the outlier scan of 13 November covered the 46 JSON files present at commit `e53742c`; the result files added since (`coin_qubit.json`, `radial_*.json`, `refinement_geometry.json`, `simultaneous_sectors.json`, `pcp_worker_trial.json`, `xr9_*.json`) are not scanned.
- Note for the director: the queue's cross-review of `Periodic_interaction_and_two_limits.md` was made before addendum 5 reached this branch. The two reports are separate runs of the same agent definition; they agree on "no defect in formulas or numbers" and differ in the points raised (addendum 5: five points of scope; queue report: the count of runs, the walk-versus-Newton gap, the Lean toolchain pin). Not reconciled here.

## Done

- 13 November 2026: G10 Theorem 5.8 and Corollary 5.9 (challenger), Corollary 5.7 (micro-review), Theorem 5.11 and Proposition 5.10 (challenger, micro-review), outlier scan of 26 result files. Reports in `edition/REVIEW_RECORDS/Director_Z/Session_4/` (`challenger/`, `challenger_2/`, `micro/`).
- 13 November 2026, queue session (reports in `REVIEW_QUEUE/reports/`, programs in the folders of the same names):
  - G10 Theorem 5.2 (challenger, micro-review): `2026-11-13_pcp-challenger_G10_thm-power.md` — NONE FOUND.
  - G10 Theorem 5.5 and Proposition 5.6 (challenger, micro-review): `2026-11-13_pcp-challenger_G10_thm-conj_prop-compo.md` — GAP (wording; finiteness in the sentence citing G9).
  - G10 Lemma 3.1 and Proposition 4.1 (challenger): `2026-11-13_pcp-challenger_G10_lem-cyl_prop-add.md` — GAP (hypothesis outside the statement of Lemma 3.1).
  - G10 Propositions 6.1 and 6.2 (challenger, micro-review): `2026-11-13_pcp-challenger_G10_prop-exact_prop-local.md` — NONE FOUND.
  - Convexity step of G10 Theorem 5.2 (formalizer): `2026-11-13_pcp-formalizer_G10_thm-power_convexity.md` — checks in Lean 4.12.0 with Mathlib; shorter argument.
  - `Director_G/Periodic_interaction_and_two_limits.md` (cross-reviewer): `2026-11-13_pcp-cross-reviewer_Director_G_Periodic_interaction.md` — GAP (wording, evidence, Lean toolchain pin).
  - Outlier scan of 46 JSON result files (micro-review): `2026-11-13_pcp-micro-review_outlier-scan.md` — DEFECT in one recorded column (`rms_width`, unwrapped centroid), enters no predicate.
  - G9 Theorem 4.3 (challenger): `2026-11-13_pcp-challenger_G9_thm-arc.md` — NONE FOUND; finiteness remark for G10.

