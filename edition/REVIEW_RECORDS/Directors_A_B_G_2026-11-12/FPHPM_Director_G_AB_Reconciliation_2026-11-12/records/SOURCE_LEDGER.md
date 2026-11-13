# Source ledger, executed checks and external anchors

Research date: 12 November 2026, B.C. Pacific Time.

## User-supplied inputs inspected locally

| Artifact | SHA-256 of original ZIP/file | Source-bound reading |
|---|---|---|
| Director A Grounding Overlay | `7f42ed74d987fdc097a32a2127f3c7d99eb6674ddeac249a8ff7172dd91e4375` | 24 ZIP entries including 23 manifest payloads; six-page PDF, Markdown disposition, source TeX, scripts, 16-claim register, nine open problems |
| Director B Initial External Grounding B1 | `390b68f0ecd1b295f73068cca8b1ae385a9ed20252e540f510cc523709ce4b64` | 16 ZIP entries including 15 manifest payloads; five-page PDF, Markdown disposition, TeX, scripts and receipts |
| FPHPM baseline 2026-11-12 (pre-Z1) | `2d1efd40a27f8c33707aac745580d6bf30e8478292b24c3a80fbcd285c7ac348` | Local re-verifier PASS, no baseline edit |
| PCP 1.0 Enterprise Edition | `1282bcd3f0ec8bd22bfb0575a6cf7e3e38f29f8cbdb278082dcfd317da907be7` | Local edition verifier PASS, no host enforcement |
| Earlier Director G technical disposition | `ab616552142f9a0b65f13a1341201f9071ffd9613c9d70e9fd5e1cf4a5ed172a` | prior internal provenance, not outside corroboration |

`PCP 1.0` edition-manifest SHA-256: `6e0cd24f626c065eb5d00ad976caade59f4da286a4b1203362feb79a98a8d1f6`. ACR Implementation release-manifest SHA-256: `42341ddf38a21a659d974af7d27c739605dd192b2d16c76ef1ae2dcdbdd41c79`.

**Availability boundary:** Director Z's claimed Z1 baseline archive and the complete G7 paper were not present among the inspected local attachments. The quoted summary was not made into a fictitious source.

## Externally inspected sources (separate from internal copies)

1. Tsachik Gelander, *Limits of Finite Homogeneous Metric Spaces*, L'Enseignement Mathématique 59 (2013), 195-206: https://ems.press/content/serial-article-files/44250 . Its PDF first-page screenshot and displayed Theorem 1.1/Corollary 1.3 were directly inspected in the live source. **Applicability:** exact finite metric homogeneity, GH limit. **Not** all finite nets.
2. Howard Barnum, Markus P. Müller and Cozmin Ududec, *Higher-order interference and single-system postulates characterizing quantum theory*, New J. Phys. 16, 123029 (2014): https://doi.org/10.1088/1367-2630/16/12/123029 . Publisher page contains three postulates and an additional energy observability postulate for complex-only identification; not just no-I3.
3. Markus P. Müller, *Probabilistic theories and reconstructions of quantum theory*, SciPost Phys. Lect. Notes 28 (2021): https://doi.org/10.21468/SciPostPhysLectNotes.28 . Full-text publication metadata and extracts were available; publisher's own site blocked direct retrieval at this time, so the evidence is labelled corroborated retrieved extracts rather than a claimed full publisher-site inspection.
4. Giorgos Eftaxias, Mirjam Weilenmann and Roger Colbeck, *Multisystem measurements in generalized probabilistic theories and their role in information processing*, Phys. Rev. A 108, 062212 (2023): https://doi.org/10.1103/PhysRevA.108.062212 . Publisher text accessed; background confirms GPT composition and a separately stated no-restriction hypothesis.

## Internal computations produced here

- `verification/verify_composite_selection.py` (newly written rather than copied from A or B); `verification/composition_results.json` with 101 parameter records and numerical/symbolic tests.
- Source mathematical paper in `reports/Composition_Selection_and_Multipartite_Closure.tex` and the rendered PDF.
- Source baseline and two input packages remain unchanged. No external experiment or independent peer review was conducted.
