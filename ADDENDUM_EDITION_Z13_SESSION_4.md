# Director Z, fourth session | Ninth addendum: edition Z13

13 November 2026. Same session and participant. Root Review: G1, OPEN. No ontology is selected.

## 1. The review stack now runs without the director

- Agent definitions (`.claude/agents/`) and a file queue (`REVIEW_QUEUE/`) are in the repository. A separate cloud session serves the queue and is woken every three hours; it commits only under `REVIEW_QUEUE/` on the branch `pcp/review-queue`.
- Its first working period produced eight reports with their programs (`queue_reports/` in this folder): four challenger reports on statements of G10 that had been read by their author only, one on G9 Theorem 4.3, one formalization, one cross-review of Director G and one outlier scan of 46 result files.
- Each report was read here; the Lean file was rerun; the findings below were checked against the paper source before the paper was changed.
- Worker trials through the ACR reference host (`pcp_workers/`): a Claude worker and a local Qwen worker ran concurrently under a supervisor (overlap 9.18 s, outputs re-read after exit), and a Claude worker called the Qwen worker through a host tool and rejected its unusable reply. Qwen scored 0 of 3 on bounded checks. PCP OS wrote no task events for these workers; its registers hold the inputs and outputs as artifacts.

## 2. Findings of the queue carried into paper G10

| Statement | Finding | Change |
|---|---|---|
| Lemma 3.1 | the hypothesis "every vertex has an outgoing arc" stood before the lemma and not in it; without it "only if" in (a) fails (11 of 11 random digraphs with a dead end); the algebra is one of histories from one fixed vertex | both stated in the lemma and in the summary |
| Theorem 5.2 | no failing step on 528 instances of 88 carriers; the convexity argument can be replaced by a termwise inequality | proof replaced by the termwise argument, checked in Lean with Mathlib (`PowerSumConvexity.lean`) |
| Opening of Section 5.4 | "a norm-preserving digraph of degree two needs -1" is false for the countable binary tree | restricted to carriers in which two vertices share a successor |
| Theorem 5.5 | "q even" and the meaning of "block" were outside the statement | stated |
| Proposition 5.6(b) | the quantifier over carriers was open to a narrower reading under which the proof does not apply | stated |
| Proposition 6.1 | on a ring the factor must be an N-th root of unity; the order of the group is a multiple of the order of the factor | stated |
| Propositions 4.1, 6.2; G9 Theorem 4.3 | no failing step; G9's Table 1 recounted exactly | none |

No proof of the paper failed. One statement (Lemma 3.1) was false as worded outside its surrounding sentence (Z-093).

## 3. An instrument artefact

The outlier scan found that the column `rms_width` of the staircase rows in `Continuation_Selection_Results.json` is wrong at 13 samples (4096 against about 17): the program subtracts an unwrapped centroid. The column enters no predicate and no statement of the paper. The result file is kept as it is; the defect is recorded here and among the retained outliers (Z-094).

## 4. Cross-review of Director G

`cross_review/CROSS_REVIEW_OF_DIRECTOR_G_ADDENDUM_5.md` (periodic interaction and two limits): no defect; five points of scope. The queue made a second cross-review of the same note by a separate run; it agrees on the absence of a defect and raises wording, evidence and a toolchain pin (Z-095).

## Records

Paper G10 revised (20 pages, 15 labelled statements). Register: review `Z13`. Amended: OP-24, OP-27. Findings Z-093 to Z-095.
