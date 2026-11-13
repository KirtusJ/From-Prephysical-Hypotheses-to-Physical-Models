# Calibration record, direction and ACR use log | Director Z | 12 November 2026

## 1. Calibration: what was actually established before work began

- **Packet checks (executed).** `verify_edition.py` on a clean extraction of the PCP 1.0 Enterprise Edition: PASS, edition fingerprint `6e0cd24f…a8d1f6`, Implementation packet SHA-256 `7f9b3692…74d0853`. `TOOLS/verify_release.py` of the ACR 1.0 Implementation packet: PASS, 57 payloads, release fingerprint `42341ddf…41c79`. A first run of the edition verifier failed because the nested archives had been unpacked inside the edition folder; that was an error of this participant's extraction, not of the packet. These are local file checks and authenticate nobody.
- **Text read.** `README.md`, `EVIDENCE_STATUS.md`, `START_HERE.md`, `KERNEL_CARD.md`, `KERNEL.md` in full (Core opening, 1.2, 2.1, 5.2, 15). Fetched with `TOOLS/acr.py clause core …` and read: 1.3, 3.1, 4.2, 4.3, 4.4, 5.1, 6.1, 7.1, 7.2, 7.4, 10.2, 10.3, 14.3. No other clause and no module Specification was read; none is relied on.
- **Settings (Core 15.8).**

| Setting | Value |
|---|---|
| Delivery | ABSORBED_TEXT for the kernel; RETRIEVAL of the clauses listed above through the packet's own lookup program run in the session container. Not HOST_ENFORCED: no halt, permission or fence is enforced by anything outside this participant's context |
| Extent | ACR 1.0 Implementation packet, release fingerprint `42341ddf38a21a659d974af7d27c739605dd192b2d16c76ef1ae2dcdbdd41c79`; Core descriptor `bf1952a3…fa460386` as printed in `KERNEL.md` |
| Grounding | EXTERNAL_INSPECTED for the sources named in section 5 of the disposition, inspected as retrieved extracts, not as full texts; SUPPLIED_ONLY for the program's documents; RECALL_ONLY for textbook mathematics and for most bibliographic details in paper G7 (listed in the disposition, section 6) |
| Execution | EXECUTED for every verifier run and every predicate of the verification program; REASONED for the proofs in paper G7 |
| Observability | BLACK_BOX. This participant's account of its own processing is not evidence |
| Participants | One. The session offers no sub-agent facility and the container holds no model credential. The instruction to use sub-agents could not be carried out. Nested reviews were separate bounded pieces of work by the same participant, each with its own claim and disposition; under Core 3.1 and 4.2 each challenge is a SELF_CHECK made with exposure to the case it challenges |

- **Evidence status of the method.** ACR is untested, not peer reviewed and not independently reviewed (`EVIDENCE_STATUS.md`). Nothing in this session measures whether its use improved the work. No calibration beyond the items above is claimed.

## 2. Intake integrity (executed)

| Artifact | Check | Result |
|---|---|---|
| `files_15_.zip` (SHA-256 `7792807a…744949e`) → `FPHPM_Baseline_2026-11-12` | `verify_baseline.py` | PASS, 645 files, 38 papers, 344 registry rows; front-matter check passed after PyMuPDF was installed |
| `D8_Uniform_Sobolev_Bound.pdf` supplied beside the baseline | digest against paper D8, part 17 | identical (`f4fc6675…4a37635f`) |
| `Toy_Universe_Session_Packet.zip` (SHA-256 `6c512b6a…891cb2`, as recorded in the baseline manifest) | file comparison with `NEGATIVE_CONTROLS/FAR-1`; `verify_toy_models.py` with its fixed output path redirected | files identical; output identical to `verified_toy_results.json` |
| `PCP_1_0_Enterprise_Edition.zip` (SHA-256 `1282bcd3…907be7`, as recorded in the baseline manifest) | see section 1 | PASS |
| `REVIEW_RECORDS/Director_D` | `validate_release.py` | PASS, 7 payloads, fresh verification agrees with stored results |

## 3. Direction of the review stack

What directing the stack meant in this session, in plain terms:

1. **One root, kept open.** The root review has the program whole as its subject and "an explained emergence of quantum and classical mechanics with a full map" as its target. No candidate structure has been put forward as a claim that could pass its first gate, so the root stays at G1 and nothing done below is reported as advancing it.
2. **Children only where a claim can be decided or sharpened.** A child review was opened only for a claim with a decisive check available in this session: a proof, an executed computation, or an inspected external theorem. Open-ended topics were left as entries in the open-problem register.
3. **The claim as posed is reported beside any substitute.** Where the favourable reading of a claim failed and a narrower statement held, both dispositions are recorded (Core 5.2).
4. **Weight comes from checks.** With one participant, a second pass adds no independence. Each derived statement was therefore tied either to an executed computation that takes a different route from the proof (Schild's ladder against the closed-form transport) or to an inspected external source.
5. **Foundational before computational.** Computation was limited to instances that could falsify a derived statement or exhibit a named possibility. The Wilson–Dirac series and the statistical series were not reopened.
6. **Nothing discarded.** Residuals, a failed tolerance and near-ties are retained in the result file and in section 7 of the disposition.
7. **Constructed ontologies only on sufficient support.** No toy universe was built: no region of the map reached the support that would make one a test of anything. One bounded constructed trial was run instead, with its stipulations named (finding Z-008).
8. **Lifecycle.** Each child closed with its disposition in this session. The root remains open. The baseline was treated as a pinned assessment basis; the changes made to it are listed in `CHANGES_TO_BASELINE.md` and issued as edition Z1.

## 4. ACR use log

| # | Act | Procedure | Subject and claim | Outcome |
|---|---|---|---|---|
| 1 | Intake and integrity checks of the three uploads | root, G1 | program whole | G1 remains OPEN |
| 2 | Z-A | FOCUSED (G1, G3, G5, G6) | the Levi-Civita holonomy of a transition-probability geometry, with monodromy, separates complex quantum theory inside the class without third-order interference | CONDITIONAL |
| 3 | Z-A1, child of Z-A | FOCUSED | determinant law for geodesic polygons in complex projective space | SUPPORTED_IN_SCOPE (mathematics, unrefereed) |
| 4 | Z-A2, child of Z-A | SCREENING | adverse case: real three-level theory against the qubit | adverse case holds locally; resolved by the non-contractible loop |
| 5 | Z-B | FOCUSED (G1, G5, G6) | a finite carrier with exact transitive symmetry can approximate a quantum pure-state space | REFUTED_IN_SCOPE for subsets of the Bloch sphere; CONDITIONAL on quoted theorems in general |
| 6 | Z-B1, child of Z-B | constructed trial (Core 10.3) | words in two stipulated rotations | EXECUTED; shows a possibility, derives nothing |
| 7 | Z-C | SCREENING | a common description of classical and quantum pure-state spaces exists in the literature | recorded as external precedent |
| 8 | Z-D | FOCUSED (G1, G5, G6) | the planned manuscript G7 can be written from the D and Z records with every statement proved, quoted or marked as computed | manuscript issued; proofs unrefereed |
| 9 | Candidate feed (Core 10.2) | — | seven candidates considered; see disposition, section 4 | three promoted to the bridge register, one run as a trial, three left as background |
| 10 | Recheck of own draft | SELF_CHECK | paper G7 | six corrections made before issue (disposition, section 7) |

Deviations: sub-agents were asked for and were not available. No clause outside those listed in section 1 was applied. Nothing was commissioned as FULL. No halt occurred. No effect outside the session container was dispatched.
