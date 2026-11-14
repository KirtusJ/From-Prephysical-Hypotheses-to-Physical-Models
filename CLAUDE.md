# Working method for Director Z sessions on this repository

This file is read by Claude sessions and their sub-agents working here. It records how the work is done and what has gone wrong before. It is method, not findings; findings live in `edition/`.

## Goal and standing limits

- Goal: an emergent, explained quantum and classical mechanics with a full map, pursued under the working assumption that it will not be reached. Never state that a gate is passed or an ontology obtained unless it is. No gate is passed today; the root review is open.
- Authorship line on every paper: Kirtus Justus, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Assistance is credited as assistance.
- Keep every failed predicate and every outlier. Do not delete or edit them away; add a follow-up.
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

The principal allows every sub-agent and worker in the stack to open pull requests, on any of the four repositories and from any branch, when the work needs it and only then (13 November 2026). A pull request is needed when a finding requires a change to a file outside the worker's own report folder: a wrong line in a program, a paper sentence, a tool, the method text. A report that changes nothing else is not a reason; it goes to `REVIEW_QUEUE/reports/` as before. Rules: one change per pull request, from a branch of the worker's own (`pcp/<role>-<topic>`), never a push to `master` or to another author's branch; the body names the target, what was rerun and the outcome, with failed predicates kept; the author never merges its own pull request; the director (or the other director for `Director_G/`) reruns and decides. A sub-agent without GitHub tools writes the change as a patch file with a short description in its work folder and says so in the first line of its report; its parent opens the pull request.

### What sub-agents and workers may make

Every sub-agent and worker using PCP may, when the task needs it and only then, write its own PCP application or helper program, install applications and packages, and generate Lean proofs (principal, 13 November 2026). The agent definitions say so. What is made is reported with what it is for, is kept in the worker's folder, and enters the repository only through the parent or a pull request; an installed tool is named in the report.

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
- Layout: the repository root holds only `README.md`, `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTORS.md`, `edition/`, `Director_G/`, `Director_Z/`, `REVIEW_QUEUE/`, `.pcp/`, `.claude/` and the archive of edition Z3. Director Z's working copies go under `Director_Z/` (`papers/`, `addenda/`, `findings/`, `computation/`, `lean/`, `challenger/`, `cross_review/`, `comb/`, `pcp_workers/`). When files are moved, use `git mv`, write a manifest of old path, new path and digest, and check that the set of blobs is unchanged; dated records keep the path names of their day.
- Path length: a Windows clone can fail with "Filename too long" on the longest paths of `edition/PAPERS/` (up to 190 characters; Windows allows about 260 including the clone's folder). The principal judged this not a project-wide issue (13 November 2026): no renaming is planned. Keep new paths at or below 150 characters; a Windows clone that hits the limit needs `git config --global core.longpaths true`.
- PCP itself: the principal allows changes to the PCP repositories (`pcp`, `pcp-os-claude`, `pcp-claude`) and a restart of PCP and of calibration, with care toward Director G, who uses the same method text (13 November 2026). Do it only when the work needs it. Before any change: write what and why in `Director_Z/cross_review/Director_exchange.md` and wait for the next exchange unless the change is confined to this side; work on the session branch of that repository and never on its default branch without agreement; never rewrite history; do not restart PCP or replace the method text while a review is open in `.pcp/register.jsonl`; record the digest of the method text before and after. A restart begins a new register session and a new calibration record; the old register stays. The principal also allows (14 November 2026) an upgraded PCP to be run as a separate version, in a separate container environment or on a new branch apart from the main branch, if that proves better and only if it is necessary; the same conditions hold, the main branch and Director G's copy are left as they are, and the reason and the outcome are logged in `Director_Z/pcp_workers/HIERARCHY_LOG.md`.
- Branches: work on the session branch, fetch before every push, fast-forward `master` only. Never rewrite history. Do not touch `Director_G/`.
- Identifiers: Director Z owns paper G10, findings `Z-…`, open problems to OP-30; Director G owns `Director_G/`, papers G11 on, OP-31 on.

## Candidate models

The principal's process (13 November 2026) is in `Director_Z/candidate/CANDIDATE_PROCESS.md`: steelman the best stipulated candidate in full (form, function, brand, plain-English overview, peer-review standard specification, stipulated map, stipulated answers to the problems of cosmology and to the Millennium Prize problems, each answer marked FOLLOWS, ADDED or SILENT and none a claim), invite attacks from every agent and director, and abandon the candidate at once when a verified attack breaks it. Abandoned candidates are kept under `Director_Z/candidate/abandoned/` with the reason. A candidate is never an ontology.

## What to work on

Prefer, in order: a statement that removes an assumption from the map; a generalization that makes two results one; a machine check of a step already used; a cross-review of the other director's newest result. Do not issue an edition for bookkeeping alone.
