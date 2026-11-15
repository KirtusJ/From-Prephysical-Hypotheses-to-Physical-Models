# Director Z | Disposition of the session of 15 November 2026

Kirtus Justus, Theoretical Physicist, Port Coquitlam, British Columbia, Canada; kept with the assistance of Director Z (a Claude session). Written at the principal's request so that a new session can start from it. Root review G1: OPEN. No gate changed state. No ontology is selected.

## Where everything is

- Branch `claude/keen-ptolemy-5flpbm`, draft pull request 282. `master` is at `d393d93` and was not touched; the editions below are on the branch only and are not merged.
- Issued on the branch: editions Z30 and Z31 (`edition/`), built by `edition/tools/director_z_update_30.py` and `_31.py`. `python3 edition/verify_baseline.py` and `python3 tools/verify_z26.py` pass: 1,968 files, 444 registry rows.
- Register `.pcp/register.jsonl`: 752 events, chain intact, 0 guard problems, head `3f4428d2…a320f7`. Reviews Z30 and Z31 closed. The Mathematics and Science modules are recorded as selected (event 714). One submission of Z31 was refused for the form of the module field and is kept in the ledger `Director_Z/tools/submitted_calls.jsonl`.

## Research results (paper G10, 70 pages, 63 labelled statements)

Four arc gains on a ring with (bc/a²)^M ≠ 1, by the number s of cosets of ⟨δ⟩ that the winding gain generates.

| Case | Result | Status |
|---|---|---|
| any ring | Lemmas 5.53 to 5.55: the numbers of left steps at one vertex are gap-free with n(l)n(l+2M) ≤ n(l+M)(n(l+M)−1), sharper when an outer level is single; Corollaries 5.56, 5.57; Lemma 5.59 (invariance without preparation) | PROVED |
| s = 1 | as on the line (Proposition 5.58) | CONDITIONAL on the stage statements of Director G's one-gain note |
| s = 2, M ≥ 8 | the count and the squares are the complete list (Theorem 5.61, with Proposition 5.60 proved in the paper) | PROVED |
| s ≥ 3, M ≥ 8 | the rule is fixed on multisets in two adjacent cosets (Theorem 5.62) | PROVED |
| s ≥ 3 | the rule on multisets meeting three cosets | OPEN; computed on the ring of 4 sites only |

Paper G8: one false clause in the proof of Proposition 5.2(c) corrected (finding Z-147); the statement stands. Findings Z-147 to Z-154.

## Candidate sprint (08:35 to 10:05 UTC)

Eight stipulated candidates for disproof, each with its kill test fixed first; all eight dead; none stands. Log: `Director_Z/candidate/LOG.md`. Plan and outcomes: `Director_Z/candidate/SPRINT_2026-11-15/00_PLAN.md`. Public catalog: `candidates/Director_Z_instances.md`.

Survives as mathematics, not proved: on the signed line the mean of log₂(number of histories behind a record) under squared chances grows at a rate approaching c* = 0.7715533031636 (gaps 0.016472, 0.009068, 0.004950, 0.002683 at 300, 600, 1200, 2400 ticks) and never exceeds the same mean under counting chances. Proved: that mean does not fall under free running.

## Open at the moment of writing

1. Two sub-agents, resumed after the usage limit was reset, are still attacking the already-dead candidate Z10: `Director_Z/candidate/Z10_Slow_Clock/attacks/2026-11-15_challenger_number/` and `…_wildcard_dial/`. Their folders are committed as they stood. When they have exited: read the reports, rerun their programs, add ledger rows, and `git mv Director_Z/candidate/Z10_Slow_Clock Director_Z/candidate/abandoned/Z10_Slow_Clock` (the log and catalog already say it is dead; the catalog links point at the present path and need the move reflected).
2. Director G has not replied on issue 270. One question is outstanding: whether their wire argument proves that the one-gain construction deposits walks of one winding (it would make s = 1 unconditional).
3. Not rerun by the director: a 51-carrier rank run (`four_gains_winding/challenger_draft/item1_fgtwo_v2.py`) and a 12-minute exploration (`builder_three_classes/explore.py`, run 2).
4. The reading copies under `papers/` are not refreshed for G10.
5. The review-queue child stays paused until 19 November.

## Tools in this container (lost when it is reclaimed)

Lean 4.12.0 with the Mathlib cache in a scratch project; XeLaTeX with DejaVu and TeX Gyre fonts; PyMuPDF; Graphviz; the PCP OS plot instrument built from pcp-os commit `e8d62e4` (branch `director-g/science-math-svg`, not on master). Register host: the packaged build 22, `pcp-os-claude/servers/linux-x86_64/pcpos`.

## Next, by the order of CLAUDE.md

1. s ≥ 3 on multisets meeting three cosets: a proof, or an explicit further rule. A builder found one undecided dimension on rings of 3, 5 and 6 sites.
2. A proof of the two conjectures about the walk above, or a counterexample.
3. s = 2 for M ≤ 7; a proof of the one-winding property without Director G's note.

## Standing instructions from the principal given in this session

- Focus entirely on the research program; the stack is at the director's discretion.
- Use the Mathematics and Science modules, and the plot instrument, along the stack.
- Log and catalogue every candidate as it goes; label each carefully.
- Write to the principal only in reply to a message from the principal.
- The principal's image for the work: a colony of mathematicians at the bottom of a cave, building a bridge to an earth it cannot see, without knowing how far the bridge extends.
