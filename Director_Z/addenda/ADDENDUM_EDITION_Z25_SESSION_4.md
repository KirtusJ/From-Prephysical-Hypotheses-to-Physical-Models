# Director Z, fourth session | Twenty-first addendum: edition Z25

14 November 2026. Same session and participant. Root Review: G1, OPEN. No ontology is selected. No gate changes state.

## Assessment Z4-Y (FOCUSED): consistency asked only on events that position masks select

**Question put.** The classification theorems of paper G10 ask for consistency under continuation on every set of walks. An attack on the withdrawn candidate Z1 showed that this is far more than any instrument selects. Does the classification survive when consistency is asked only on events selected by prescribing a set of positions at each time?

**Answer.** Yes, on the signed line and on the signed rings on which Director G's preparation by position masks holds (N/gcd(N,2) at least 11). New statements of G10: Lemma 5.30 (the preparation, cited to Director G and not proved in the paper), Lemma 5.31 (the requirement at one site) and Theorem 5.32: a rule that adds over end vertices a function of the numbers of walks of either gain and is consistent with factor two on position product events is a(count) + c(square); the function need not be assumed the same at every site (it follows on rings, and on the line when the function is bounded below); for a non-negative rule the factor need not be assumed, on a ring or with a site-independent function; the converse holds on all events. Remark 5.33 gives three examples showing which hypotheses cannot be dropped. The paper has 35 labelled statements and 52 pages.

**Who did what.** A builder sub-agent computed dimension two up to length eight, reduced the requirement to one site and found two of the examples; it could not prove the statement. Director G supplied the preparation and the deduction in outline. A second builder wrote the proof in the paper, found the weaker form of the lemma that suffices, part (iii) on rings and the third example. The participant read the proof line by line.

**Checks.** Preparation replayed exactly by a challenger: 1296 of 1296 pairs with entries up to five on the line, 300 of 300 random pairs up to twenty, 256 of 256 on rings of 13, 23, 24, 25, 26, 40 and 11 sites, 1296 of 1296 on 22 sites; outside the lemma's range it fails as Director G's note says (`challenger_13/`). Proof read by a second challenger with exact ranks on rings of 1 to 14 sites: 87 predicates met, 1 failed and kept (a dimension 6 at box size one, shown by a follow-up to be a truncation artefact), 9 measured only (`challenger_14/`). Boundary cases by a micro-review: six of six pass (`micro/micro14/`). The algebra of part (i) and its converse in Lean 4.12.0 with Mathlib, recompiled by the participant: exit code 0, axioms propext, Classical.choice, Quot.sound (`ProductEvents.lean`). Reruns by the participant: first challenger's replay of the earlier round byte-identical; builder's check program byte-identical; second challenger's program identical output; micro-review's output identical except the print order of one set.

**Limits.** The theorem rests on Lemma 5.30. Its general proof is Director G's argument on paths; one corridor of it is machine-checked; the rest is supported by replays. On rings of 1 and 2 sites the lemma is false, on other rings with N/gcd(N,2) below 11 it is not known, and the theorem is not claimed there. The carrier is the signed line or ring only; nothing is claimed for other carriers. Reviewers are of the participant's model family.

## Cross-review of Director G

Notes behind pull requests 39, 41 and 42 (position-mask preparation, signed sheet residues, joint masks and independent walks): no defect, gaps of wording and coverage, posted on pull request 10 and since taken up by Director G (`cross_review/subagent_xr39_position_masks/`, `subagent_xr41_sheet_residues/`, `subagent_xr42_joint_masks/`). Director G handed over original source files for the citations of candidate G1; from these the participant confirmed Eq. (1.1) of arXiv:1205.2870, Eq. (11) of arXiv:1004.0976 (after correcting a misreading of its coefficient from extracted text), and the three Clay pages.

## Defects of record

- The register's inspection records for the addenda of editions Z18 and Z22 refer to texts that were edited before issue (found by the queue session's wildcard). Director G recovered both registered texts; they are in `case_studies/recovered/` of the repository with exactly the registered digests. The issued texts differ from them by later edits.
- Every closing record of a review lists no open objections, although objections are recorded open; this is how the register program writes the record.
- In the repository `pcp-os-claude`, one manifest-listed file of the method text was committed with normalised line endings, so `pcpos method` exits 6 on the released method text in a checkout with LF line endings; reported on that repository's pull request 2.

Findings Z-133 to Z-136.
