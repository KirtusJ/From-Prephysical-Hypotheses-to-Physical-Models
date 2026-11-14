# Working method for Director Z sessions on this repository

This file is read by Claude sessions and their sub-agents working here. It records how the work is done and what has gone wrong before. The issued findings are in `edition/`.

The [repository guide](README.md) links the issued edition, working research, candidate dispositions and the live review queue. At issue, check its edition label, paper links and verification command against the new edition.

## Goal and standing limits

- Goal: an emergent, explained quantum and classical mechanics with a full map, pursued under the working assumption that it will not be reached. Never state that a gate is passed or an ontology obtained unless it is. No gate is passed today; the root review is open.
- Authorship line on every paper: Kirtus Justus, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Assistance is credited as assistance.
- Keep every failed predicate and every outlier. Do not delete or edit them away; add a follow-up.
- The director keeps complete control of its own target and motion within the research program at all times (principal, restated 14 November 2026). Reviews, pull requests, the other director's requests and the stack's reports are inputs; what to work on next is the director's choice, by the order in "What to work on", and is said in the report.
- Reports to the principal: outcomes and blocks only. Say at once when the network or a tool blocks the work. Do not narrate corrections that are already recorded in the edition.

## The review stack, top to bottom

| Tier | Who | Used for | Budget |
|---|---|---|---|
| Director | this session | choosing questions, proofs, reading every report, issuing editions | whole session |
| Cross-director | Director G (Codex), same repository | reading each other's results; findings on the pull-request or issue thread | per result |
| Challenger | sub-agent, paper text only as input | trying to break one theorem and its proof, with its own program | 5 to 10 minutes |
| Formalizer | sub-agent with Lean | machine-checking the algebraic steps | 2 to 5 minutes |
| Micro-review | sub-agent, one narrow target | boundary cases, wording that an edge case makes false, outliers in result files | 1 to 2 minutes, about 8 tool calls |
| Builder (positive arc) | sub-agent `pcp-builder` | making one statement stronger: a hypothesis removed, a computed step proved, two results unified | 10 to 15 minutes |
| Wildcard | sub-agent `pcp-wildcard`, no assigned target | whatever it judges most worth attention anywhere in the repository, favourable or not | one per working period |
| Chaos | sub-agent `pcp-chaos`, scratch copies only | planted errors, to see which checks catch them | before an edition and when a check changes |

Rules for the stack:

1. A new statement gets, before issue: a program with predicates fixed first, a challenger, a micro-review of its boundary cases, and Lean for any step that is pure algebra.
2. Give a sub-agent the paper text and definitions, never the director's notes. Tell it to write its own program and to keep failed predicates.
3. Read every report and recheck its files (rerun Lean, open the result file) before using it. A sub-agent's "all pass" is a claim.
4. Sub-agents share the director's model family. Their agreement reduces exposure; it is not independent review. Say so in the record.
5. Findings propagate upward into the paper before issue and into the registers at issue; the report itself is filed under `REVIEW_RECORDS/Director_Z/Session_4/`.
6. Run an outlier scan over all result files at each edition.
7. The stack carries positive arcs as well as negative ones (principal, 13 November 2026): for a statement or candidate under attack, send a builder as well as the challengers, and carry what it proves upward in the same way as a defect. Propagate widely: prefer several narrow sub-agents in parallel to one reading by the director, and let workers pass work down one further level when it helps.

## Running without the director

The stack is defined in files so that it does not depend on one session: agent definitions in `.claude/agents/` (`pcp-challenger`, `pcp-micro-review`, `pcp-formalizer`, `pcp-cross-reviewer`) and a file queue in `REVIEW_QUEUE/` with its protocol. Any session, a scheduled routine or a sub-agent can serve the queue; reports go to the branch `pcp/review-queue` and never to `master`. The director reads that branch at the start of each working period, rechecks each report, and carries findings into the next edition. New statements are added to `REVIEW_QUEUE/QUEUE.md` when they are drafted. Changes to this hierarchy, with what worked and what did not, are logged in `Director_Z/pcp_workers/HIERARCHY_LOG.md`; check the child session's status at the start of each working period, because it shares the account's limits and stops silently.

### Pull requests from sub-agents and workers

For a change to a research paper, proof, checker or local review tool, open one pull request per finding from a worker branch. Give the target, rerun command, evidence and any failed predicates. Workers leave review and merge to the director. Reports alone go to the review queue. A worker without GitHub tools sends its parent a patch with these details.

### What sub-agents and workers may make

A research worker may write or install a checker, use an existing research instrument, or formalize a step in Lean when the question calls for it. Record the tool, version, purpose and output needed to reproduce the finding.

### Calibration of the stack

How calibration works for this side and how the stack adapts to its results is kept in `Director_Z/calibration/HOW_CALIBRATION_WORKS.md` (principal, 14 November 2026): known-answer items with the key and thresholds fixed and hashed before the run, an assessor who is not the participant, a control in every brief to a lower-tier agent. Use it on lower-tier models and lower forms of integration, and add each run to that file's log.

### Asynchronous work

The following practices come from asynchronous checks of the research program.

1. Nothing is said about a background result until its exit code has been read. A rerun that has been started is not a rerun that passed.
2. Every asynchronous task ends as a recorded fact: exit code, timeout or not, duration, and the digest of each file it left, read back from disk after it has exited. `Director_Z/tools/async_run.py` does this for programs; for sub-agents the parent does it by rerunning the agent's program and comparing bytes.
3. A task writes as it goes (a notes file appended after each step, result files opened so that they are never overwritten), so that a task cut off by a limit leaves usable work.
4. At most three tasks at once; a stopped agent is resumed by message with its context, not relaunched.
5. A task is given a fresh directory and never reuses one; a call file is submitted once (`pcp_submit.py`).
6. A brief to a lower-tier agent carries a control with a known answer, answered first.

## Lessons paid for

- **Test the hypothesis in the predicate.** Four programs failed because random carriers did not satisfy the theorem's hypothesis (gains in a subgroup, an unknown without an equation) and the predicate did not check it. Every "for all carriers" predicate must first test the hypothesis per carrier and report how many qualify.
- **No thresholds without a basis.** State where a tolerance comes from, or measure a separation instead.
- **State conventions.** A difference of 1.8e-3 between two runs was whether the origin site counts as positive. Say which side zero is on.
- **Let Lean find the proof.** Twice the formal proof was shorter than the hand proof, and once it exposed an arithmetic slip. Ask for the statement in general form first.
- **Summaries are where errors hide.** Three of the corrections from other readers were to summary sentences, corollary wording or attributions, not to proofs. Send summaries and corollaries to a challenger too.
- **Scope of a hypothesis.** A theorem stated with "a faithful character" silently excluded non-cyclic groups. State hypotheses in the form the proof uses.

## Mechanics

- Edition: unpacked tree `edition/`; `python3 edition/verify_baseline.py` must pass before a push. Each edition is produced from the previous one by a script kept in `edition/tools/`, names its predecessor by digest, and lists every changed file.
- Programs: predicates in the docstring before the first run; result file that the program refuses to overwrite; fixed seed; rerun in a fresh directory and compare bytes.
- Register: `.pcp/register.jsonl`, written through the `pcpos` tool server; one review per edition; objections that stand are recorded open. Copy the register into the edition in the same commit.
- Lean: 4.12.0. Core-only files in `edition/COMPUTATION/Lean/`; Mathlib v4.12.0 files in `edition/COMPUTATION/Lean/Mathlib/` with their lakefile. A pass is exit code 0 with only `propext`, `Quot.sound` and `Classical.choice`.
- Use the [repository guide](README.md) to locate the edition, working notes, candidates and review queue. Director Z's working copies go under `Director_Z/` (`papers/`, `addenda/`, `findings/`, `computation/`, `lean/`, `challenger/`, `cross_review/`, `comb/`, `pcp_workers/`). When files are moved, use `git mv`, write a manifest of old path, new path and digest, and check that the set of blobs is unchanged; dated records keep the path names of their day.
- Path length: a Windows clone can fail with "Filename too long" on the longest paths of `edition/PAPERS/` (up to 190 characters; Windows allows about 260 including the clone's folder). The principal judged this not a project-wide issue (13 November 2026): no renaming is planned. Keep new paths at or below 150 characters; a Windows clone that hits the limit needs `git config --global core.longpaths true`.
- When a shared research tool or register session needs a restart, tell the other director which active reviews are affected. Preserve the existing register and record the versions and calibration for the resumed review.
- Branches: work on the session branch, fetch before every push, fast-forward `master` only. Never rewrite history. Do not touch `Director_G/`.
- Identifiers: Director Z owns paper G10, findings `Z-…`, open problems to OP-30; Director G owns `Director_G/`, papers G11 on, OP-31 on.

## Candidate models

The principal's process (13 November 2026) is in `Director_Z/candidate/CANDIDATE_PROCESS.md`: steelman the best stipulated candidate in full (form, function, brand, plain-English overview, peer-review standard specification, stipulated map, stipulated answers to the problems of cosmology and to the Millennium Prize problems, each answer marked FOLLOWS, ADDED or SILENT and none a claim), invite attacks from every agent and director, and abandon the candidate at once when a verified attack breaks it. Abandoned candidates are kept under `Director_Z/candidate/abandoned/` with the reason. A candidate is never an ontology.

## What to work on

Choose the next research question using the open obligations and external evidence. Prefer a result that removes a hypothesis, unifies two results, checks a step already used or resolves a cross-director review. Issue an edition when the research findings warrant it.
