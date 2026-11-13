# From Prephysical Hypotheses to Physical Models

**Kirtus Justus**, Theoretical Physicist
Port Coquitlam, British Columbia, Canada

Research contributors include **Director G (OpenAI Codex)** and **Director Z (Claude)**. [Contributors and roles](CONTRIBUTORS.md)

This repository holds the current baseline edition of the research program as an unpacked tree in `edition/`, with the documents of the latest review sessions beside it for direct reading. The program's aim, structure and standards are in `PROGRAM/CHARTER.md` and `PROGRAM/STANDARDS.md` inside each edition. No edition claims a physical ontology; no gate of the program's gate map is passed.

| Item | Content |
|---|---|
| `edition/` | edition Z17 (13 November 2026), unpacked: 41 papers, registers, computation, review records. Current. From this edition on no archive is committed; `git archive` of this folder gives one. Editions Z4, Z5 and Z6 of the same day are in the history of this repository as archives (commits `50568e7`, `dfc151d`, `5594e35`) and editions Z7, Z8 and Z9 as trees (commits `90fbe08`, `c1a9a31`, `30beaac`); each edition names its predecessor by digest in its manifest |
| [Director G’s research supplements](Director_G/README.md) | Fixed transport, probability from persistent records, quantum and classical limits, and [Lean proofs](Director_G/lean/README.md) |
| `FPHPM_Baseline_2026-11-12_Z3.zip` | edition Z3 (12 November 2026), as first committed, kept unchanged |
| `G10_Histories_as_Events.pdf` | paper G10, first issued in edition Z4, revised in editions Z5 (Theorem 5.3), Z6 (Lemma 5.4, Theorem 5.5) , Z7 (Proposition 5.6; corrections after Director G) , Z8 (Corollary 5.7, the rule on the signed lift; one sentence corrected at the request of Director G) , Z9 (Theorem 5.8, which pair rules are consistent) , Z10 (Theorem 5.8 for any finite abelian group and any degree; Corollary 5.9) , Z11 (Proposition 5.10, degrees three and four) , Z12 (Theorem 5.11, Fourier blocks of every degree) , Z13 (corrections after the review queue) , Z14 (Theorem 5.12: any norm-preserving carrier with a merging pair) , Z15 (Proposition 5.14: when the gains are abundant) , Z16 (Theorem 5.16: the block law for any function of the summed gains) and Z17 (Theorem 5.18: the block law for any function of the multiset of gains) |
| `G7_…pdf`, `G8_…pdf`, `G9_…pdf` | papers G7 to G9 as in editions Z3 and Z4 |
| `Gate_Map_2026-11-13.pdf`, `Gate_Map_2026-11-12.pdf` | gate map figures of editions Z17 and Z3 |
| `DIRECTOR_Z_TECHNICAL_DISPOSITION_SESSION_4.md`, `CALIBRATION_AND_ACR_USE_LOG_SESSION_4.md`, `NEW_Z_SCOPED_FINDINGS_SESSION_4.csv` | records of the fourth Director Z session (copies of files in `edition/`) |
| `ADDENDUM_EDITION_Z5_SESSION_4.md`, `ADDENDUM_EDITION_Z6_SESSION_4.md`, `ADDENDUM_EDITION_Z7_SESSION_4.md`, `ADDENDUM_EDITION_Z8_SESSION_4.md`, `ADDENDUM_EDITION_Z9_SESSION_4.md`, `ADDENDUM_EDITION_Z10_SESSION_4.md`, `ADDENDUM_EDITION_Z11_SESSION_4.md`, `ADDENDUM_EDITION_Z12_SESSION_4.md`, `ADDENDUM_EDITION_Z13_SESSION_4.md`, `ADDENDUM_EDITION_Z14_SESSION_4.md`, `ADDENDUM_EDITION_Z15_SESSION_4.md`, `ADDENDUM_EDITION_Z16_SESSION_4.md`, `ADDENDUM_EDITION_Z17_SESSION_4.md`, `NEW_Z_SCOPED_FINDINGS_SESSION_4_ADDENDUM*.csv` | six addenda of the same session: the revisions of paper G10, the corrections after Director G's cross-reading, the record of contact, and a statement of this participant withdrawn |
| `Director_Z_cross_review/` | Director Z's cross-review of eight results of Director G, with its programs and result files (copy of `edition/REVIEW_RECORDS/Director_Z/Session_4/cross_review/`) |
| `…_SESSION_3.md`, `CROSS_DIRECTOR_ADJUDICATION_SESSION_3.csv` | records of the third session |
| `Z4_COMPUTATION/` | the nineteen programs of the fourth session with their result files (copies of `edition/COMPUTATION/Baseline_Additions`) |
| `Z4_LEAN/` | four Lean 4 files for the core library and, in `Mathlib/`, five for Mathlib v4.12.0, proving the algebraic lemmas of G10 and the sequential-projection inequality (copies of `edition/COMPUTATION/Lean`); see the README there |
| `Director_Z_challenger/` | report and programs of a challenger sub-agent on G10 Theorem 5.8 and Corollary 5.9 (copy of `edition/REVIEW_RECORDS/Director_Z/Session_4/challenger/`) |
| `Z4_CALIBRATION/` | the Calibration Record of the fourth session with the committed retrieval answers and their scores |
| `.pcp/` | the register kept for the fourth session by the PCP OS program, and the text it stored beside it |

To check the current edition run `python3 edition/verify_baseline.py`; to check the archive of edition Z3, extract it and run `python3 verify_baseline.py` in its folder. The file `.gitattributes` keeps the edition's bytes unchanged on checkout, since the manifest holds digests. A pass is a local fact about the files; it authenticates nobody and certifies no proof. Research direction and scholarly responsibility: Kirtus Justus. Assistance by AI systems is recorded in `PROGRAM/CONTRIBUTIONS.md` of each edition and implies no endorsement by their providers.

Director Z (Claude) maintains the editions and Director G (Codex) maintains the research supplements. Both sets of work are integrated on the default branch. Their cross-reviews record which results were checked, the assumptions each review used, and the adverse controls. [Director exchange](Director_G/Director_exchange.md) · [Edition discussion](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/pull/1) · [Supplement discussion](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/pull/2)
