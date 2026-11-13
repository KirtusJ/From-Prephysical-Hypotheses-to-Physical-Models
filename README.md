# From Prephysical Hypotheses to Physical Models

**Kirtus Justus**, Theoretical Physicist
Port Coquitlam, British Columbia, Canada

This repository holds the current baseline edition of the research program as an unpacked tree in `edition/`, with the documents of the latest review sessions beside it for direct reading. The program's aim, structure and standards are in `PROGRAM/CHARTER.md` and `PROGRAM/STANDARDS.md` inside each edition. No edition claims a physical ontology; no gate of the program's gate map is passed.

| Item | Content |
|---|---|
| `edition/` | edition Z7 (13 November 2026), unpacked: 41 papers, registers, computation, review records. Current. From this edition on no archive is committed; `git archive` of this folder gives one. Editions Z4, Z5 and Z6 of the same day are in the history of this repository as archives (commits `50568e7`, `dfc151d`, `5594e35`); each edition names its predecessor by digest in its manifest |
| `FPHPM_Baseline_2026-11-12_Z3.zip` | edition Z3 (12 November 2026), as first committed, kept unchanged |
| `G10_Histories_as_Events.pdf` | paper G10, first issued in edition Z4, revised in editions Z5 (Theorem 5.3), Z6 (Lemma 5.4, Theorem 5.5) and Z7 (Proposition 5.6; corrections after Director G) |
| `G7_…pdf`, `G8_…pdf`, `G9_…pdf` | papers G7 to G9 as in editions Z3 and Z4 |
| `Gate_Map_2026-11-13.pdf`, `Gate_Map_2026-11-12.pdf` | gate map figures of editions Z7 and Z3 |
| `DIRECTOR_Z_TECHNICAL_DISPOSITION_SESSION_4.md`, `CALIBRATION_AND_ACR_USE_LOG_SESSION_4.md`, `NEW_Z_SCOPED_FINDINGS_SESSION_4.csv` | records of the fourth Director Z session (copies of files in `edition/`) |
| `ADDENDUM_EDITION_Z5_SESSION_4.md`, `ADDENDUM_EDITION_Z6_SESSION_4.md`, `ADDENDUM_EDITION_Z7_SESSION_4.md`, `NEW_Z_SCOPED_FINDINGS_SESSION_4_ADDENDUM*.csv` | three addenda of the same session: the revisions of paper G10, the corrections after Director G's cross-reading, and the record of contact |
| `Director_Z_cross_review/` | Director Z's cross-review of two results of Director G, with its programs and result files (copy of `edition/REVIEW_RECORDS/Director_Z/Session_4/cross_review/`) |
| `…_SESSION_3.md`, `CROSS_DIRECTOR_ADJUDICATION_SESSION_3.csv` | records of the third session |
| `Z4_COMPUTATION/` | the ten programs of the fourth session with their result files (copies of `edition/COMPUTATION/Baseline_Additions`) |
| `Z4_CALIBRATION/` | the Calibration Record of the fourth session with the committed retrieval answers and their scores |
| `.pcp/` | the register kept for the fourth session by the PCP OS program, and the text it stored beside it |

To check the current edition run `python3 edition/verify_baseline.py`; to check the archive of edition Z3, extract it and run `python3 verify_baseline.py` in its folder. The file `.gitattributes` keeps the edition's bytes unchanged on checkout, since the manifest holds digests. A pass is a local fact about the files; it authenticates nobody and certifies no proof. Research direction and scholarly responsibility: Kirtus Justus. Assistance by AI systems is recorded in `PROGRAM/CONTRIBUTIONS.md` of each edition and implies no endorsement by their providers.

Two directors work on this repository. Director Z (Claude) keeps the edition and the fourth-session records on the branch `claude/cool-newton-bqk60b` (pull request 1); Director G (Codex) keeps research supplements in the folder `Director_G/` on the branch `director-g/records-and-forced-envelope` (pull request 2). Each has read and checked results of the other; coordination takes place on the review thread of pull request 1.
