# From Prephysical Hypotheses to Physical Models

**Kirtus Justus**, Theoretical Physicist
Port Coquitlam, British Columbia, Canada

Research contributors include **Director G (OpenAI Codex)** and **Director Z (Claude)**. [Contributors and roles](CONTRIBUTORS.md)

This repository holds the current baseline edition of the research program as an unpacked tree in `edition/`, with the documents of the latest review sessions beside it for direct reading. The program's aim, structure and standards are in `PROGRAM/CHARTER.md` and `PROGRAM/STANDARDS.md` inside each edition. No edition claims a physical ontology; no gate of the program's gate map is passed.

| Item | Content |
|---|---|
| `edition/` | edition Z20 (13 November 2026), unpacked: 41 papers, registers, computation, review records. Current. From this edition on no archive is committed; `git archive` of this folder gives one. Editions Z4, Z5 and Z6 of the same day are in the history of this repository as archives (commits `50568e7`, `dfc151d`, `5594e35`) and editions Z7, Z8 and Z9 as trees (commits `90fbe08`, `c1a9a31`, `30beaac`); each edition names its predecessor by digest in its manifest |
| [Director G’s research supplements](Director_G/README.md) | Fixed transport, probability from persistent records, quantum and classical limits, and [Lean proofs](Director_G/lean/README.md) |
| [Z3 archive](edition_archives/FPHPM_Baseline_2026-11-12_Z3.zip) | edition Z3 (12 November 2026), as first committed, kept unchanged |
| `Director_Z/` | Director Z's working copies beside the edition, all byte-identical to files in `edition/` unless noted. The [move manifest](Director_Z/FLUSH_MANIFEST_2026-11-13.csv) records 279 source digests. At the move commit 278 destination blobs matched exactly. The [exchange note](Director_Z/cross_review/Director_exchange.md) also updated two paths and added the handoff |
| `Director_Z/papers/` | `G10_Histories_as_Events.pdf`: paper G10, first issued in edition Z4, revised in editions Z5 (Theorem 5.3), Z6 (Lemma 5.4, Theorem 5.5) , Z7 (Proposition 5.6; corrections after Director G) , Z8 (Corollary 5.7, the rule on the signed lift; one sentence corrected at the request of Director G) , Z9 (Theorem 5.8, which pair rules are consistent) , Z10 (Theorem 5.8 for any finite abelian group and any degree; Corollary 5.9) , Z11 (Proposition 5.10, degrees three and four) , Z12 (Theorem 5.11, Fourier blocks of every degree) , Z13 (corrections after the review queue) , Z14 (Theorem 5.12: any norm-preserving carrier with a merging pair) , Z15 (Proposition 5.14: when the gains are abundant) , Z16 (Theorem 5.16: the block law for any function of the summed gains) , Z17 (Theorem 5.18: the block law for any function of the multiset of gains) , Z18 (no new statement; corrections after a comb of the whole session) , Z19 (Theorem 5.18 for every finite abelian group; Remark 5.21) and Z20 (Theorem 5.22: a function at each end vertex; no block needed on strongly connected carriers). Papers G7 to G9 as in editions Z3 and Z4. Gate map figures of editions Z20 and Z3 |
| `Director_Z/addenda/`, `Director_Z/findings/` | the addenda of the fourth session, one per edition from Z5 on, and the scoped findings Z-041 on |
| `Director_Z/session_records/` | technical dispositions and calibration logs of the third and fourth sessions; the cross-director adjudication of the third |
| `Director_Z/cross_review/` | Director Z's cross-reviews of results of Director G (the first review and eight addenda), with programs and result files, and [the exchange note](Director_Z/cross_review/Director_exchange.md) |
| `Director_Z/computation/` | the programs of the fourth session with their result files (copies of `edition/COMPUTATION/Baseline_Additions`) |
| `Director_Z/lean/` | Lean 4 files for the core library and, in `Mathlib/`, for Mathlib v4.12.0 (copies of `edition/COMPUTATION/Lean`); see the README in the edition |
| `Director_Z/challenger/`, `Director_Z/comb/` | programs and results of challenger and micro-review sub-agents; records of the comb after edition Z17 |
| `Director_Z/pcp_workers/` | trials of PCP workers, a tracking note on machine mode, and the log of the review hierarchy |
| `Director_Z/calibration/` | the Calibration Record of the fourth session with the committed retrieval answers and their scores |
| `REVIEW_QUEUE/` | the file queue of review requests with its protocol, reports and shared library |
| `.pcp/` | the register kept for the fourth session by the PCP OS program, and the text it stored beside it |

To check the current edition run `python3 edition/verify_baseline.py`; to check the archive of edition Z3, extract it and run `python3 verify_baseline.py` in its folder. The file `.gitattributes` keeps the edition's bytes unchanged on checkout, since the manifest holds digests. A pass is a local fact about the files; it authenticates nobody and certifies no proof. Research direction and scholarly responsibility: Kirtus Justus. Assistance by AI systems is recorded in `PROGRAM/CONTRIBUTIONS.md` of each edition and implies no endorsement by their providers.

Director Z (Claude) maintains the editions and Director G (Codex) maintains the research supplements. Both sets of work are integrated on the default branch. Their cross-reviews record which results were checked, the assumptions each review used, and the adverse controls. [Director exchange](Director_G/Director_exchange.md) · [Edition discussion](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/pull/1) · [Supplement discussion](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/pull/2)
