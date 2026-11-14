# Review queue

A file-based queue that lets review work run without the director present. Any Claude session with this repository, a scheduled routine, or a sub-agent can serve it.

## Protocol

1. Read `CLAUDE.md` at the repository root and the agent definitions in `.claude/agents/`.
2. Find work, in this order:
   - items listed under **Open** in `REVIEW_QUEUE/QUEUE.md`;
   - any labelled statement of `edition/PAPERS/G10_*/source/body.tex` whose label has no report in `REVIEW_QUEUE/reports/` (run `pcp-challenger` and `pcp-micro-review` on it);
   - any note in `Director_G/` newer than the newest `CROSS_REVIEW_OF_DIRECTOR_G*` file in `Director_Z/cross_review/` (run `pcp-cross-reviewer`);
   - an outlier scan (`pcp-micro-review`) of every JSON result file if none is dated today.
3. Do one item at a time with the matching agent definition. Work in a scratch directory. Keep failed predicates.
4. Write one report per item: `REVIEW_QUEUE/reports/<UTC date>_<agent>_<target>.md`, beginning with three lines: target (file and label or commit), outcome (DEFECT / GAP / NONE FOUND), reviewer kind. Put the reviewer's program beside it in a folder of the same name. Move the item from **Open** to **Done** in `QUEUE.md` with the report's name.
5. Commit only files under `REVIEW_QUEUE/`. Push to the branch `pcp/review-queue` (create it from `master` if absent; merge `master` into it first; never rewrite history; never push to `master`).
6. Do not edit papers, registers, `edition/`, `Director_G/` or `.pcp/`. A defect is reported, not repaired: the director reads the queue, verifies each report and carries findings into the next edition.
7. Stop after the items you can finish in the time you have. Leave unfinished items under **Open** with a one-line note.

## Efficiency and periodic reports

- Budget per item: challenger 10 minutes, cross-reviewer 12, formalizer 5, micro-review 2. Stop an item at twice its budget, file what you have and mark it partial.
- Do not redo work that exists: before an item, list `REVIEW_QUEUE/reports/`, `Director_Z/cross_review/` and `edition/REVIEW_RECORDS/Director_Z/Session_4/` for the same target and commit; if a report exists for an unchanged statement, skip it.
- Run items in parallel as sub-agents when they do not share files. Give each sub-agent only the file paths and line ranges it needs.
- Reuse: keep one scratch library of carrier builders, exact cyclotomic arithmetic and consistency-equation solvers under `REVIEW_QUEUE/lib/` and import it, in place of rewriting them per item. Keep one Lean project with the Mathlib cache between items.
- Programs: sample sizes just large enough for the predicate; no run above three minutes without a stated reason.
- At the end of every working period write `REVIEW_QUEUE/STATUS.md` (replace it) with: date and commits covered; a table of items with minutes spent, tool calls, outcome; what was slow or wasted and why; one concrete change made to the workflow this period and its measured effect on the next comparable item; what is open. Append the same table to `REVIEW_QUEUE/STATUS_LOG.md`.
- If the same kind of defect is found twice (a hypothesis outside a statement, an untested hypothesis in a predicate, a missing structural condition), add a one-line check for it to the matching file in `.claude/agents/` on the queue branch and say so in `STATUS.md`; the director merges it.

## Standing of the reports

Reviewers served by this queue are of the director's model family unless a report says otherwise. A report reduces exposure to the author's notes; it is not independent review. The director rechecks every report before using it.

## Pull requests from workers

A worker serving this queue may open a pull request against `master` on any of the four repositories when a finding needs a change outside `REVIEW_QUEUE/`, and only then. One change per pull request, from a branch `pcp/<role>-<topic>`; say in the body what was rerun and the outcome; never merge it. Reports alone stay on `pcp/review-queue`. (Principal, 13 November 2026; rules in `CLAUDE.md`.)

## What workers may make

When a task needs it and only then, a worker or its sub-agents may write their own PCP applications or helper programs, install applications and packages, and generate Lean proofs. Name what was made or installed in the report. (Principal, 13 November 2026; rules in `CLAUDE.md`.)

## PCP OS

Workers serving this queue may report issues and open pull requests on the PCP OS source repository `KirtusJ/pcp-os` as they go: an issue with the command, input and output that shows the fault; a pull request from a branch `pcp/<role>-<topic>`, never to the default branch. (Principal, 14 November 2026, permanent; rules in `CLAUDE.md`.)
