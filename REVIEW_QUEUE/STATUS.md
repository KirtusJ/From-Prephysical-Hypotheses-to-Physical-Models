# Status of the review queue

Working period: 14 November 2026, 00:05 to about 01:00 UTC. Targets at commit `b07cff6`; branch merged with `master` at that commit.

Reviewers are of the author's model family. Nothing here is independent review. No PCP calibration record exists for this queue session: the method text and the `pcpos` tool are not in this container.

## Items (DEFECT first)

Minutes and tool calls of the sub-agents are their own figures; the second number is the queue session's recheck and filing.

| Item | Agent | Minutes | Tool calls | Outcome |
|---|---|---|---|---|
| Register against files and git history (seed `ledger`) | wildcard (sub-agent) | 6 + 4 | 12 + 2 | DEFECT: two registered addenda (Z18, Z22) are not the issued texts; closing records list no open objections although 23 are recorded open |
| The queue's library and two programs | chaos (sub-agent) | 11 + 4 | 16 + 2 | DEFECT in the queue's checks: 7 of 23 planted errors passed; self-test added |
| G10 Corollary 5.29, sign premise | builder (sub-agent) | 13 + 5 | 12 + 2 | STRENGTHENED, proof written and read |
| Director G, Finite memory and coherent returns | cross-reviewer (sub-agent) | 7 + 2 | 13 + 1 | GAP |
| Director G, Separated string records | cross-reviewer (sub-agent) | 7 + 2 | 10 + 1 | GAP |
| Director G, Flight window preparation | cross-reviewer (sub-agent) | 5 + 2 | 10 + 1 | GAP |

## What was slow or wasted, and why

- The three new agent types (`pcp-builder`, `pcp-wildcard`, `pcp-chaos`) were not loaded when the period began, so three launches failed and were repeated as general agents told to read the definition files. They are loaded now.
- One cross-reviewer tried to download Lean 4.19.0 although its task said not to, citing its agent definition. The permission system blocked it; nothing was installed. The definition of `pcp-cross-reviewer` and a parent's instruction pull in different directions here; the definition should say that Director G's toolchain is used only when it is already installed.
- The builder could not write its FINDINGS.md (its harness refused report files) and put the proof in its final message; the queue session copied it into the report.
- The builder raised an objection to Director G's citation of Lemma 5.25(4) because it had been told to read only the statement of Theorem 5.26 and so had not seen the lemma. The objection does not stand. Line ranges that are too narrow produce false objections; the lemma a proof cites belongs in the range.

## Workflow changes this period, with measured effect

- Cross-reviewers were told not to elaborate Director G's Lean files, to list every hypothesis with the place where it is stated, and to include unreported parameters. Effect: 5 to 7 minutes each against 14 to 17 minutes for the three of the previous day, with the same kind of findings; five of the eight GAPs this period are hypotheses outside statements or underived summary sentences.
- `REVIEW_QUEUE/lib/pcplib_selftest.py` added after the chaos run: it fails on 16 of the 17 planted library errors, where the two programs' own predicates noticed 9 by a predicate and 4 by a crash.
- Each report was filed and pushed as its sub-agent returned, not at the end of the period.

## Recurring kind of finding

"A hypothesis the proof uses is outside the statement" occurred again in all three cross-reviews. The line proposed in the previous status files for `pcp-challenger.md` and `pcp-cross-reviewer.md` was put into the three cross-review tasks by hand this period. The queue session has still not edited `.claude/agents/`: the routine restricts its commits to `REVIEW_QUEUE/`.

## Not done on request of another session

The per-period comment on pull request 3 asked for by the director session is not posted (an outward post the routine and the protocol file do not call for). This file carries the content.

## Open

See `QUEUE.md`. From the director's newest note: six of Director G's nine notes (`Folded_field_and_native_gaussian`, `Four_tick_force`, `Window_source_cost`, `Renewal_launch_and_classical_records`, `Marker_kernel_from_one_launch`, `Tag_sector_controls`). Also open: the candidate process; the challenger and micro-review targets for editions Z16 to Z22; the reading of G10 as issued in Z18; Director G's earlier requests; the outlier scan of files added since `e53742c` (none is dated today). For the queue's own instruments: the four items listed as not yet done in the chaos report.
