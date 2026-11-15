# From Prephysical Hypotheses to Physical Models

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada, directs the research and holds scholarly responsibility. Claude (Anthropic) developed the transport and gain-graph studies in G7–G10, contributed to the Wilson–Dirac analysis and organized the issued edition. ChatGPT (OpenAI) contributed derivations and manuscripts across the collection. Codex developed and tested the walk models and checked arguments used in G10. [Paper contributions and sources](papers/contributions.md) · [Contributors and roles](CONTRIBUTORS.md)

The program asks whether quantum mechanics and classical mechanics can both emerge from the same primitives, with an explicit map from preparations and records to physical predictions. All 13 physical identification gates (P0–P12) remain open. [Charter](edition/PROGRAM/CHARTER.md) · [Standards for claims and evidence](edition/PROGRAM/STANDARDS.md)

## Where to start

| If you want to… | Start here |
|---|---|
| Read the research papers | [Paper catalog and PDFs](papers/README.md) · [A1 program overview](papers/A1%20-%20Program%20Overview%20%E2%80%93%20Questions%2C%20Models%20and%20Physical%20Correspondence.pdf) · [Issued edition Z30](edition/README.md) |
| Find what a result establishes | Look up its paper, statement and status in the [issued theorem registry](edition/PROGRAM/registers/THEOREM_REGISTRY.csv). Follow the [open problems](edition/PROGRAM/registers/OPEN_PROBLEMS.csv) and [readiness register](edition/PROGRAM/registers/READINESS.csv) for outstanding obligations. |
| Trace the route to physical identification | The [issued gate map](edition/PROGRAM/registers/ONTOLOGY_GATE_MAP.json) records the edition’s assessment. [Codex’s working gate map](Director_G/ontology_gate_map.json) tracks the supplement studies and their assumptions, starting from the Z3 baseline. The [bridge register](edition/PROGRAM/registers/BRIDGE_CANDIDATE_REGISTER.json) covers proposed relations between models, including transport. |
| Find the current disposition of a proposed universe | Use the [stipulated candidate catalog](candidates/README.md) for each specification, attacks and dated disposition. For example, **Edge Record Walk G1** is open for attack. **Paper G1**, *Relational Structures and the Limits of Observation*, is an issued paper with a different subject. |
| Contact Director G (Codex) | Introduce your session and the work you want to coordinate in the [first-contact issue](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/issues/270). |
| Follow active research or reproduce a result | [Codex supplements and checkers](Director_G/README.md) · [Claude edition addenda](Director_Z/addenda/) · [Scoped findings](Director_Z/findings/) · [Cross-director exchange](Director_G/Director_exchange.md) |
| Pick up a review | Read the [live work list](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/pcp/review-queue/REVIEW_QUEUE/QUEUE.md) and [reviewer status](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/pcp/review-queue/REVIEW_QUEUE/STATUS.md) on `pcp/review-queue`. The [standing review PR](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/pull/3) carries that branch. The [queue protocol](REVIEW_QUEUE/README.md) explains how to file a report. |
| Trace a scientific review | [Research case studies](case_studies/README.md) show the claim under review, the evidence checked and the resulting correction or disposition. |
| Check a source’s provenance | The [quarantine guide](quarantine/README.md) identifies the fictional and mixed-source packets retained from the program’s intake. |

## Papers

The [paper catalog](papers/README.md) lists the 40 manuscripts by title and subject and links directly to their PDFs and available sources. F7 is a [planned manuscript](papers/README.md#planned-manuscript). The [mathematical review](papers/review/math.md) and [PDF review](papers/review/pdf.md) identify corrections and the limits of the checks.

## Evidence and working records

To recover an earlier mainline or branch revision, use the [protected recovery tags, branch inventory and restore procedure](version_control/README.md).

- For an issued calculation, start at the [computation index](edition/PROGRAM/registers/COMPUTATION_INDEX.csv). The edition also preserves [constructed trials](edition/CONSTRUCTED_TRIALS/), [negative controls](edition/NEGATIVE_CONTROLS/) and [review records](edition/REVIEW_RECORDS/).
- For a working supplement, start at the evidence linked in that note. Examples include [atom-loading counts and reported recapture losses](Director_G/Single_atom_loading_and_terminal_recapture.md), an [exact walk calculation for an unknown input coin](Director_G/Unknown_coin_position_reference.md) and [three registered replay examples](Director_G/replay_gain_orbits.md). The [supplement Lean guide](Director_G/lean/README.md) and [edition Lean guide](edition/COMPUTATION/Lean/README.md) identify their respective proof environments.
- For Claude’s edition work see the [historical paper copies and drafts](Director_Z/papers/), [computations](Director_Z/computation/), [cross-reviews](Director_Z/cross_review/) and [handoff](Director_Z/cross_review/Director_exchange.md). Reviewers’ [challenge programs](Director_Z/challenger/), [fine-grained checks](Director_Z/comb/), [session records](Director_Z/session_records/) and [calibration records](Director_Z/calibration/) preserve the basis for their decisions.
- To reconstruct a research review, use the [worker records](Director_Z/pcp_workers/), [register submission tools](Director_Z/tools/) and [session register](.pcp/). The [Codex](AGENTS.md) and [Claude](CLAUDE.md) guides explain how reviewers check a claim and report corrections.

## Verify or recover an edition

From the root of a checkout, run `python tools/verify_z26.py` (or `python3 tools/verify_z26.py`). The [Z26 replay tool](tools/verify_z26.py) checks the issued verifier’s digest and runs its checks on the edition. Editions Z27 to Z30 kept the Z26 verifier byte for byte, so the same tool checks them. On Windows it translates the native path separator for the manifest lookup in a temporary copy of the verifier. Install PyMuPDF in the same Python environment for PDF page counts and author/location checks. Read any skip notices in the output. A pass establishes local consistency of the files and registers. [Issued manifest](edition/MANIFEST.json) · [Issued verifier](edition/verify_baseline.py)

For a Windows checkout in a long destination path, use `git clone -c core.longpaths=true https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models.git`. This sets the option before Git checks out the files. [Git clone configuration](https://git-scm.com/docs/git-clone#Documentation/git-clone.txt---configltkeygtltvaluegt)

The issued Z27 tree is the `edition/` folder at commit `9080181`. The [issued Z26 tree](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/tree/e18a4cca023ccffb404303e65a8a730c49ef5409/edition) can be recovered from Git history. To export it from a clone, run `git archive --format=zip --output=Z26.zip e18a4cc edition`. The [Z3 archive](edition_archives/FPHPM_Baseline_2026-11-12_Z3.zip), [edition-by-edition history through Z26](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/381e10de377fb62c9c6f77c3a8e8cb01bcedc8eb/README.md) and [dated working-file move manifest](Director_Z/FLUSH_MANIFEST_2026-11-13.csv) preserve earlier versions and provenance.
