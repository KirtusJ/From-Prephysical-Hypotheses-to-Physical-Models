# Calibration record, direction and ACR use log | Director Z, second session | 12 November 2026

## 1. Calibration: what was actually established

- **Method text.** The PCP 1.0 Enterprise Edition and its ACR 1.0 Implementation packet were not among this session's inputs. No clause was read in this session. The vocabulary used (Unary and Cross-Adversarial review, SCREENING and FOCUSED procedures, gates G1 to G6, the disposition values, Core 10.2 candidate feed, Core 10.3 constructed trials, Core 15.8 settings) is carried from the first-session record of this participant, from the Director D record, and from the logs of Directors A, B and G, each of which reports reading the packet. A separate six-stage outline (Grounding, Steelman, Strawman, Demolition, Certify, Ledger) of an ACR specification 2.1.0 is on file with the principal; it was not mapped to the ACR 1.0 gates. Calibration to the method in this session is therefore second-hand. No verifier of the packet was run here.
- **Settings.**

| Setting | Value |
|---|---|
| Delivery | absorbed from records; no retrieval from the packet; not HOST_ENFORCED |
| Extent | ACR 1.0 Implementation as fingerprinted in the first-session record (`42341ddf…41c79`); not re-verified |
| Grounding | EXTERNAL_INSPECTED for the sources in section 6 of the disposition (retrieved text, mostly extracts); SUPPLIED_ONLY for program documents and Director packets; RECALL_ONLY for the items in section 7 of the disposition |
| Execution | EXECUTED for 39 predicates in four programs and for every rerun of a Director program; REASONED for the proofs in G7 and G8 |
| Observability | BLACK_BOX |
| Participants | One in this stack. The instruction to use sub-agents could not be carried out: the session has no sub-agent tool, the container holds no model credential, and a request to the model interface from the container was refused for lack of a key (HTTP 401). Nested reviews are separate bounded pieces of work by the same participant |

- **Evidence status of the method.** Untested. This session offers one observation and no measurement: three errors in the text of edition Z1 that this participant's own second pass had left in place were found by Directors A, B and G, a different model family, and were confirmed here. Self-check with exposure did not find them; cross-review did.

## 2. Intake integrity (executed)

| Artifact | Check | Result |
|---|---|---|
| `files_16_.zip` → `FPHPM_Baseline_2026-11-12_Z1` | `verify_baseline.py` | PASS, 657 files, 38 papers, 353 registry rows |
| Director A overlay | `validate_overlay.py`; `verify_transition_geometry.py` | PASS, 23 payloads; ALL_CHECKS_PASS, maximum determinant error 7.36e-13 |
| Director B, B1 | `verify_packet.py`; three verification programs | PASS, 15 payloads; all pass |
| Director G, initial | `verify_packet.py`; `verify_director_g_claims.py` | PASS, 13 files; pass, 96 trials, maximum residual 1.53e-15 |
| Director A, A2 | `verify_packet.py`; `verify_cycle_and_phase.py` | PASS, 18 payloads; pass, 271 trials |
| Director B, B2 | `verify_packet.py`; `verify_B2.py` | PASS, 18 payloads; ran to completion with all data files preserved |
| Director G, reconciliation | `verify_packet.py`; `verify_composite_selection.py` | PASS; ran to completion |

The transmitted first-round text labelled Director B was identical to the text of Director A; the B1 packet itself was used. These are local file checks and reruns. They authenticate nobody and certify no proof.

## 3. Direction of the review stack

1. **One root, kept open.** As in the first session.
2. **Other Directors' packets as submissions.** Each claim was decided on its hypotheses and on a check made here by a different route, not on its author, its tier or the number of Directors asserting it. Where a Director was right against edition Z1 the edition was changed and the change recorded.
3. **Children only where decidable.** Six child reviews; each closed in the session with a disposition.
4. **The claim as posed beside any substitute.** GH-1 carries two dispositions: the conditional mathematics, and the emergence claim.
5. **Foundational before computational.** Computation was limited to predicates that could falsify a derived statement. The D, E and F series were not reopened.
6. **Constructed trial on support.** One trial was built, at the point where four records agreed on the constraints and the program's own primitives supplied the object. It was demolished in the same review and filed apart from the negative controls.
7. **Nothing discarded.** Failed first runs and superseded values are in section 8 of the disposition and in the result files.
8. **Recheck before issue.** Stored results were compared with every number typed into the manuscripts; one discrepancy was found and corrected.

## 4. ACR use log

| # | Act | Procedure | Subject and claim | Outcome |
|---|---|---|---|---|
| 1 | Intake of seven archives | root, G1 | program whole | G1 remains OPEN |
| 2 | Z2-X | Cross-Adversarial, FOCUSED | 23 claim groups of Directors A, B, G against edition Z1 | three points upheld against Z1; one resolved; four not decided; remainder concurred |
| 3 | Z2-A | FOCUSED (G1, G3, G5, G6) | transition probabilities determine Bargmann phases up to one conjugation, constructively | SUPPORTED_IN_SCOPE |
| 4 | Z2-B | FOCUSED | forms of the postulate selecting complex amplitudes | equivalences SUPPORTED_IN_SCOPE; warrant NOT_IDENTIFIED_IN_SCOPE |
| 5 | Z2-C | FOCUSED | algebraic generating data determine the transition probability | REFUTED_IN_SCOPE |
| 6 | Z2-D | FOCUSED | single-system geometry determines composite and relative orientation | REFUTED_IN_SCOPE; what fixes them NOT_IDENTIFIED |
| 7 | Z2-E, with child Z2-E1 (demolition) | constructed trial (Core 10.3) | GH-1 | conditional statements SUPPORTED_IN_SCOPE; emergence NOT_IDENTIFIED_IN_SCOPE |
| 8 | Z2-F | FOCUSED | manuscripts G7 (revised) and G8 | issued; unrefereed |
| 9 | Candidate feed (Core 10.2) | — | nine candidates | six promoted or recorded, three left as background |
| 10 | Recheck of own drafts | SELF_CHECK | G7, G8, registers | corrections listed in the disposition, section 8 |

Deviations: sub-agents were asked for and were not available. The method text was not available. Nothing was commissioned as FULL. No halt occurred. No effect outside the session container was dispatched.
