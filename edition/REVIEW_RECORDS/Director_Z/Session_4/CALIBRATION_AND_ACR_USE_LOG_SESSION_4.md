# Calibration record, direction and ACR use log | Director Z, fourth session | 13 November 2026

## 1. Onboarding and calibration: what was actually established

- **What arrived.** Four repositories: this program (edition Z3 as one archive, with five loose documents of the third session), the PCP 1.0 Enterprise Edition (build 19, with the ACR 1.0 Implementation packet), and the two PCP plugins for Claude as separate repositories (`pcp` and `pcp-os`, version 1.0.22, build 22, edition file "Commercial").
- **Method text: three builds are in play.** Sessions 1 to 3 pinned the release fingerprint `42341ddf…41c79`. The Implementation packet received now has the fingerprint `6b6d3a68…53c6` (build 19; Core descriptor `f15686b3…86a7`). The method text inside the two plugins is that of build 22 (manifest `7ff72eed…4707`; Core descriptor `9f5998dd…6fb0`). Builds 19 and 22 were compared by diff over every Specification. Build 22 adds Core Section 14.4 (Calibration), the notion of an instrument (Core 14.1 and a Section 10 in each module), one sentence in Core 15.2 and one in 15.8; nothing else in Core, Mathematics or Science differs apart from dates and the descriptor. This session worked under the build-22 text, which contains the build-19 requirements. The text of the earlier fingerprint was not available and was not compared.
- **Integrity checks (executed).** `verify_baseline.py` on edition Z3: PASS, 967 files, 40 papers, 381 registry rows. `TOOLS/verify_release.py` of the build-19 packet: PASS, 57 payloads. `verify_edition.py` on a copy of the edition without version-control metadata: FAIL on one file, `PCP_1.0_Plugins/plugins/pcp/method/REFERENCE/Clause_Index.csv`; the file differs from the packet's copy by carriage returns only (57297 against 57551 bytes, 254 lines), a line-ending normalization by version control, not a change of content. `pcpos method` on the build-22 plugin: 41 files present and equal, 16 absent (programs and probes), the same index file differing. These are local file checks and authenticate nobody.
- **Text read.** Core Specification of build 19 in full (Sections 1 to 15, Appendices A to C); the additions of build 22 in full; Mathematics and Science Specifications in full; kernel; Known Limitations of both builds; the plugin's skills (review, adopt, calibrate, status, verify, workspace, system), its four subagent definitions and its event bodies. Not opened: the Engineering, Cryptography, Statistics and Quality Assurance Specifications, the Overviews, the Methods Catalog, the Record Contracts, the Command Interface, the Integration Guide, the Safety Handbook, the probes.
- **Calibration Record (Core 14.4).** `registers/CALIBRATION_RECORD_SESSION_4.json`. Acquisition: as above. Retrieval: 9 items, 9 for, 0 against, 0 invented, one run each; the answers were committed to a file (SHA-256 `fde3c49c…9a08`) before the comparison, and scored by exact comparison with the output of `pcpos clause`. The items were chosen by this participant from provisions it had read in this session, with their text in its context: the count measures recall within one context, under that confinement, and nothing more. The packet's item generator is in no archive received. Application: NOT_MEASURED; a participant does not score itself. Thresholds: none stated. Claim: none. The instrument `core.calibration` returns CONSISTENT AS DECLARED for the record, which says that its numbers agree with each other and not that they are true. **No statement that this participant is onboarded or calibrated is made.** The entry for any use of this session's record is: one self-administered retrieval count; otherwise NONE.
- **Settings (Core 15.8).**

| Setting | Value |
|---|---|
| Delivery | RETRIEVAL for the method text (files read; clauses fetched with `pcpos clause`). The `pcp-os` tool server kept a register for this session, but it was reached through a client written in the session and not through the host's plugin mechanism: no hook ran, nothing is HOST_ENFORCED, and no command was observed by a host |
| Extent | as listed under "Text read" |
| Grounding | EXTERNAL_INSPECTED for the four sources of section 6 of the disposition (full texts retrieved, named parts read); SUPPLIED_ONLY for program documents; RECALL_ONLY for the reference to Li and So |
| Execution | EXECUTED for 26 predicates in six programs, each rerun in a fresh directory with byte-identical result files; REASONED for the proofs of G10 |
| Observability | BLACK_BOX. The host named three model identifiers in the course of the session |
| Participants | One. A sub-agent facility exists in this host and was not used (disposition, section 7) |

- **Evidence status of the method.** Untested. Observations of this session, none a measurement: (i) seven predicates fixed before their runs failed, two of them through wrong expectations of this participant about the subject and three through defects of its checking programs; all were caught by execution; (ii) the guards of the register accepted a supported finding for a claim settled by reading a proof this participant wrote, marking it a self-check with reasoning only; the register does not make such a finding more than that.

## 2. Intake integrity (executed)

| Artifact | Check | Result |
|---|---|---|
| `FPHPM_Baseline_2026-11-12_Z3.zip` (SHA-256 `e63c5669…7b1e`) | `verify_baseline.py` | PASS, 967 files |
| loose `G7`, `G8`, `G9`, gate map PDFs and three session-3 documents beside the archive | compared with the edition | G9 text identical to a rebuild of the source with XeLaTeX (13 pages, no differing line) |
| PCP 1.0 Enterprise Edition, build 19 | `verify_edition.py`; `verify_release.py` | one line-ending difference (above); PASS |
| `pcp-os` plugin, build 22 | `pcpos method`; program digest against its README | as above; `c2c6795d…3dcd` equal |

The toolchain was installed in the session: TeX Live with XeLaTeX (the papers use fontspec), Graphviz, sympy, mpmath, networkx, PyMuPDF. The environment's network allow-list was extended by two hosts, arxiv.org and export.arxiv.org, for source inspection.

## 3. Direction of the review stack

1. **One root, kept open.** As before.
2. **Children only where decidable.** Five child reviews; each closed with a disposition.
3. **The claim as posed beside any substitute (Core 5.2).** The second order "from the program's primitives" is NOT_IDENTIFIED as posed and CONDITIONAL in its narrowed form; the force from gains of bounded order is UNRESOLVED as posed with what was proved listed beside it; the first ray claim is REFUTED as posed and the second, fixed before its run, is reported as a different claim.
4. **Criteria before runs.** Every predicate was written before its program ran. Where a criterion failed, the result file was kept and a new program with new criteria was written; no result file was overwritten (each program refuses to).
5. **Foundational before computational.** Computation was confined to exhaustive or sampled tests of derived statements and to instances for the two open items.
6. **Nothing discarded.** Section 8 of the disposition and the six result files.
7. **Recheck before issue.** Fresh-directory reruns; numbers in G10 compared with the result files.

## 4. ACR use log

| # | Act | Procedure | Subject and claim | Outcome |
|---|---|---|---|---|
| 1 | Intake, verification, reading | root, G1 | program whole | G1 remains OPEN |
| 2 | Adoption | — | the principal's opening message asked for PCP onboarding and calibration and set the goal; recorded in the register as relayed by this participant (the host did not observe it); the whole message is kept as an artifact, the adoption basis is its first sentence because the program limits a basis to 2000 characters | ACR in use |
| 3 | Z4-A | FOCUSED | histories as events; additive rules | SUPPORTED_IN_SCOPE |
| 4 | Z4-B | FOCUSED | order of the rule | theorems SUPPORTED_IN_SCOPE; favourable reading NOT_IDENTIFIED_IN_SCOPE; narrowed form CONDITIONAL |
| 5 | Z4-C | FOCUSED | force from gains of bounded order | two propositions SUPPORTED_IN_SCOPE; claim as posed UNRESOLVED |
| 6 | Z4-D | FOCUSED | position of a ray | first claim REFUTED_IN_SCOPE; bound UNRESOLVED |
| 7 | Z4-E | FOCUSED | GH-1 and GH-2 with history events as a candidate | NOT_IDENTIFIED_IN_SCOPE |
| 8 | Z4-F | FOCUSED | manuscript G10 | issued; unrefereed |
| 9 | Candidate feed (Core 10.2) | — | ten candidates | three promoted, three executed or recorded, four background |
| 10 | Register | — | review `Z4` in `register/register.jsonl`: six claims, three objections (one recorded open), six findings | see the register; head digest in `README_SESSION_4.md` |

Deviations: the workspace of the register is Core only, because the program lets only the person directing the work select modules; the Mathematics and Science Specifications were read and their obligations applied as ordinary obligations, and no review of the register claims them. Nothing was commissioned as FULL. No halt occurred. Effects outside the session container: two hosts added to the network allow-list of the principal's cloud environment; commits pushed to the designated branch of this repository.
