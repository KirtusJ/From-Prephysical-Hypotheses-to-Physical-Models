# Calibration record, direction and ACR use log | Director Z, third session | 12 November 2026

## 1. Calibration: what was actually established

- **Method text.** The PCP 1.0 Enterprise Edition was among the inputs. `verify_edition.py` passed (10 files; edition fingerprint `6e0cd24f…8d1f6`); `TOOLS/verify_release.py` of the ACR 1.0 Implementation packet passed (57 payloads; release fingerprint `42341ddf…41c79`, equal to the value carried from the first session; Core descriptor `bf1952a3…0386`). The kernel was read in full. Core 3.1, 4.2, 4.3, 4.4, 10.2 and 10.3 were fetched with `TOOLS/acr.py clause`. No other clause was fetched; the specialist modules (Mathematics, Science, Statistics, Quality Assurance) were not opened. Calibration is first-hand for the kernel and those six clauses and for nothing else. The six-stage outline of an ACR specification 2.1.0 on file with the principal was again not mapped to the ACR 1.0 gates.
- **Settings (Core 15.8).**

| Setting | Value |
|---|---|
| Delivery | RETRIEVAL for the kernel and six clauses; otherwise ABSORBED_TEXT from earlier records; not HOST_ENFORCED |
| Extent | ACR 1.0 Implementation, release fingerprint `42341ddf38a21a659d974af7d27c739605dd192b2d16c76ef1ae2dcdbdd41c79`, verified locally; not authenticated |
| Grounding | EXTERNAL_INSPECTED for the sources in section 6 of the disposition (abstracts and extracts); SUPPLIED_ONLY for program documents and Director packets; RECALL_ONLY for the items in section 7 of the disposition |
| Execution | EXECUTED for 74 predicates in five programs and for every rerun of a Director program; REASONED for the proofs in G7, G8 and G9 |
| Observability | BLACK_BOX |
| Participants | One. No sub-agent tool in the session; a request to a model interface from the container was refused (HTTP 401, no key). Nested reviews are bounded pieces of work by the same participant, each a SELF_CHECK with exposure (Core 4.2) |

- **Evidence status of the method.** Untested. Observations of this session, none of them a measurement: (i) one error of edition Z2 (the breadth of a sentence in G8) was found by Directors A, B and G and not by this participant's self-check; (ii) one erratum proposed by two Directors was not upheld on inspection of the source; both Directors appear to have read text extracted from the PDF, in which an overline is lost; (iii) five failures of this participant's own checking programs and one wrong assertion were caught by executed predicates, not by re-reading; (iv) a status statement made between two parts of the session was inaccurate (a program reported as relaunched had produced no output). Core 4.2 anticipates (iii): a self-challenge draws its weight from executed checks and inspected sources.

## 2. Intake integrity (executed)

| Artifact | Check | Result |
|---|---|---|
| `files_17_.zip` → edition Z2 | `verify_baseline.py` | PASS, 791 files, 39 papers, 367 registry rows |
| PCP 1.0 Enterprise Edition | `verify_edition.py`; `verify_release.py` | PASS; PASS |
| Director A, A3 | `verify_packet.py`; `verify_A3_selection_gates.py` | PASS, 19 payloads; pass, maximum residual 6.66e-16 |
| Director B, B3 | `verify_packet.py`; `verify_B3.py`; `negative_controls.py` | PASS, 23 payloads; pass; 8 controls; 15 floating residuals of the cycle table differ at 1e-16 from the stored file |
| Director G, G3 | `verify_packet.py`; three programs | PASS, 36 payloads; pass; stored trial files differ at rounding level |
| Director A, A4 | `verify_packet.py`; `verify_A4_independent.py` | PASS, 20 payloads; pass |
| Director B, B4 | `verify_packet.py`; `verify_B4.py` | PASS, 19 payloads; pass, 5 negative controls |
| Director G, G4 | `verify_packet.py`; `verify_director_g_followup.py` | PASS, 28 payloads; pass |

Local file checks and reruns. They authenticate nobody and certify no proof. Director B's supplement in B4 carries the file name `G9_Gain_Graph_Growth_and_History_Consistency`; it is a Director B submission and is not paper G9 of the program.

## 3. Direction of the review stack

1. **One root, kept open.** As before.
2. **Packets as submissions.** Each claim decided on its hypotheses and a check by a different route; neither the tier of a model nor the number of Directors asserting a point was given weight. One point of three Directors was upheld; one point of two Directors was not.
3. **Children only where decidable.** Six child reviews, each closed with a disposition in the session.
4. **The claim as posed beside any substitute (Core 5.2).** GH-2 carries the conditional mathematics and the emergence claim separately; the "favourable reading" of the complex structure was assessed as posed and refuted; an unmet numerical criterion was kept as a failed predicate and not re-scoped.
5. **Foundational before computational.** The session's new statements concern what a requirement forces on the carrier; computation was confined to exhaustive enumeration of small cases and to predicates able to falsify a derived statement. The D, E and F series were not reopened.
6. **Constructed trial on support (Core 10.3).** GH-2 was built where four records agreed on what was missing (Directors A and B on continuation; this participant on the involution; Director G on formal exponentials) and a theorem fixed the carrier. Stipulated, derived, observed and proposed transfer are separated in the ledger; demolition was done in the same review.
7. **Nothing discarded.** Failed first runs, the unmet criterion, adverse instances and superseded values are in section 8 of the disposition and in the result files.
8. **Recheck before issue.** Every program was rerun in a fresh directory with byte-identical result files; numbers typed into the manuscripts were compared with the stored results.

**Adjustment of technique made in this session, on a demonstrated cause.** After a status statement proved inaccurate, completion of a program is asserted only from its result file read in a later step, and long programs are divided so that each part finishes within one call. After the overline case, a disputed proof step is settled against the source and the rendered page, not against extracted text.

## 4. ACR use log

| # | Act | Procedure | Subject and claim | Outcome |
|---|---|---|---|---|
| 1 | Intake of eight archives | root, G1 | program whole | G1 remains OPEN |
| 2 | Z3-X | Cross-Adversarial, FOCUSED | 24 claim groups of Directors A, B, G (third and fourth rounds) | one point upheld against Z2; one erratum not upheld; three not decided; remainder concurred, two with additions |
| 3 | Z3-A | FOCUSED (G1, G3, G5, G6) | what consistency under continuation imposes | SUPPORTED_IN_SCOPE |
| 4 | Z3-B | FOCUSED | a reversible step as warrant for complex amplitudes | proposition SUPPORTED_IN_SCOPE; favourable reading REFUTED_IN_SCOPE; warrant NOT_IDENTIFIED_IN_SCOPE |
| 5 | Z3-C, with child Z3-C1 (demolition) | constructed trial (Core 10.3) | GH-2 | conditional statements SUPPORTED_IN_SCOPE or CONDITIONAL; emergence NOT_IDENTIFIED_IN_SCOPE; force with bounded gain order UNRESOLVED |
| 6 | Z3-D | FOCUSED | transport supplied by the carrier | SUPPORTED_IN_SCOPE as mathematics; selection NOT_IDENTIFIED_IN_SCOPE |
| 7 | Z3-E | FOCUSED | cover and growth condition of G8 | SUPPORTED_IN_SCOPE; growth item of OP-25 discharged |
| 8 | Z3-F | FOCUSED | manuscripts G9 (new), G8 and G7 (revised) | issued; unrefereed |
| 9 | Candidate feed (Core 10.2) | — | twelve candidates | eight promoted or examined, two recorded, two background |
| 10 | Recheck of own drafts and programs | SELF_CHECK | G7, G8, G9, registers, five programs | corrections listed in the disposition, section 8 |

Deviations: sub-agents were asked for and were not available. Nothing was commissioned as FULL. No halt occurred. No effect outside the session container was dispatched. The session ran in three parts separated by the limit on tool use; the first two ended without an edition.
