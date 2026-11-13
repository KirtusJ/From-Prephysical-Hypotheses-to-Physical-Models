# Review queue

A file-based queue that lets review work run without the director present. Any Claude session with this repository, a scheduled routine, or a sub-agent can serve it.

## Protocol

1. Read `CLAUDE.md` at the repository root and the agent definitions in `.claude/agents/`.
2. Find work, in this order:
   - items listed under **Open** in `REVIEW_QUEUE/QUEUE.md`;
   - any labelled statement of `edition/PAPERS/G10_*/source/body.tex` whose label has no report in `REVIEW_QUEUE/reports/` (run `pcp-challenger` and `pcp-micro-review` on it);
   - any note in `Director_G/` newer than the newest `CROSS_REVIEW_OF_DIRECTOR_G*` file in `Director_Z_cross_review/` (run `pcp-cross-reviewer`);
   - an outlier scan (`pcp-micro-review`) of every JSON result file if none is dated today.
3. Do one item at a time with the matching agent definition. Work in a scratch directory. Keep failed predicates.
4. Write one report per item: `REVIEW_QUEUE/reports/<UTC date>_<agent>_<target>.md`, beginning with three lines: target (file and label or commit), outcome (DEFECT / GAP / NONE FOUND), reviewer kind. Put the reviewer's program beside it in a folder of the same name. Move the item from **Open** to **Done** in `QUEUE.md` with the report's name.
5. Commit only files under `REVIEW_QUEUE/`. Push to the branch `pcp/review-queue` (create it from `master` if absent; merge `master` into it first; never rewrite history; never push to `master`).
6. Do not edit papers, registers, `edition/`, `Director_G/` or `.pcp/`. A defect is reported, not repaired: the director reads the queue, verifies each report and carries findings into the next edition.
7. Stop after the items you can finish in the time you have. Leave unfinished items under **Open** with a one-line note.

## Standing of the reports

Reviewers served by this queue are of the director's model family unless a report says otherwise. A report reduces exposure to the author's notes; it is not independent review. The director rechecks every report before using it.
