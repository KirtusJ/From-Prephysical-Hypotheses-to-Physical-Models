# Calibration record and ACR use log | Director D | 11 November 2026

## Calibration (what was actually established before work began)

- ACR 1.0 Implementation packet read from the PCP 1.0 Enterprise Edition: `START_HERE.md`, `KERNEL.md`, Entry Card, Core §§1–6 and §15 in full, §7.4 and §10.2–10.3, module outlines. Other clauses were not read and are not relied on.
- PCP edition verifier: PASS on a clean extraction (edition fingerprint `6e0cd24f…a8d1f6`; Implementation packet SHA-256 `7f9b3692…74d0853`). ACR Implementation verifier: PASS, 57 payloads, release fingerprint `42341ddf…41c79`. These are local file checks; they authenticate nobody.
- Delivery here is ABSORBED_TEXT plus RETRIEVAL from the packet's own Markdown. No host enforcement, no tool server, no command interface. "PCP" is used only as the package alias (§15.7).
- Participants: one. The host offers no sub-agent facility in this session. Under §3.1 and §15.7 a single actor must not present role exchanges as distinct participants; every challenge is recorded as SELF_CHECK with exposure. Nested assessments ("ACR within ACR") were run as separate bounded executions of the same participant, each with its own Target, Claim and disposition.
- Grounding: EXTERNAL_INSPECTED for the cited mathematical and experimental precedents (web retrieval, 11 Nov 2026); SUPPLIED_ONLY for the program's own documents; RECALL_ONLY for textbook mathematics, which was then executed rather than asserted.
- Evidence status of the method: untested, not peer reviewed, not independently reviewed (packet `EVIDENCE_STATUS.md`). No claim of calibration beyond the items above is made.

## Intake integrity (all EXECUTED, same-input reproduction)

| Artifact | Check | Result |
|---|---|---|
| Review packet 2026-11-10 (sha256 `fde41b37…6669cf`) | `tools/verify_packet.py --strict-file-set` | PASS, 445 files, 85 components |
| Director B handoff (sha256 `547a89f0…a5925`) | `verify_release.py` | PASS, 18 payloads |
| Director C audit (sha256 `0bf18a8f…6296b`) | `validate_release.py` | PASS, 15 payloads |
| Toy Universe packet (sha256 `6c512b6a…891cb2`) | `verify_toy_models.py` with hard-coded `/mnt/data/...` output path redirected | PASS; output byte-identical to shipped JSON |
| Nested `PCP_1_0.zip` in B's source archive (sha256 `30ea3cdb…37a24`) | byte comparison with Enterprise Implementation | Core differs by 344 lines; modules differ |

## ACR use log (lightweight)

| # | Act | Profile | Target / Claim | Outcome |
|---|---|---|---|---|
| 1 | G1 intake of all five packets; provenance chain checked | root Unary Review, TOTAL extent | program whole | G1 remains OPEN (unchanged) |
| 2 | D-TRN-A | FOCUSED (G1, G5, G6) | principal's transport stipulation, strong reading | NOT_IDENTIFIED_IN_SCOPE |
| 3 | D-TRN-B | FOCUSED | substitute claim: exact transport correspondences within/between mechanics | SUPPORTED_IN_SCOPE (mathematics) |
| 4 | D-TRN-C | FOCUSED | discriminator ladder and obligation on finite candidates | SUPPORTED_IN_SCOPE / CONDITIONAL |
| 5 | Check-against: EPS | SCREENING | precedent template | recorded, no construction |
| 6 | Reconciliation note: PCP R13 vs ACR 1.0 | SCREENING | basis compatibility | UNRESOLVED; Reconciliation Review justified |
| 7 | Candidate feed (§10.2) | — | seven candidate observations considered; one FRAME_ALTERNATIVE (EPS), one DISCRIMINATOR_CANDIDATE (triple phase), one ORIGINAL_SCOPE_COUNTEREXAMPLE (representation nonselection) promoted; the rest (Hannay angle, Wilczek–Zee, Aharonov–Bohm) left as background | logged, not promoted |

Deviations: none from the kernel. Nothing was commissioned as FULL. No halt occurred. No consequential effect outside the container was dispatched. The baseline was treated as a pinned assessment basis (§7.4), not as a lock; no baseline file was modified.
