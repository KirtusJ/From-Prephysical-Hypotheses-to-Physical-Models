# Status of the review queue

Working period: 13 November 2026, 12:06 to about 18:30 UTC, with an interruption of about five hours in which the session's worker was restarted and nothing ran. Targets at commit `b84056e` (edition Z15). Branch `pcp/review-queue` merged with `master` at `60e78b1` at the end.

Reviewers are of the author's model family. Nothing here is independent review. No PCP calibration record exists for this queue session: the method text and the `pcpos` tool are not in this container.

## Items

Minutes are estimates of active time; sub-agent figures are the ones the sub-agents reported.

| Item | Agent | Minutes | Tool calls | Outcome |
|---|---|---|---|---|
| G10 Prop. 5.14, Cor. 5.15 | challenger (queue session) | 35 | 8 | GAP (wording of one remark) |
| Four algebraic steps (5.12, 5.14) | formalizer (sub-agent), rerun by the session | 12 + 2 | 8 + 1 | NONE FOUND, all check |
| Cor. 5.13: hypothesis from Thm 5.3; m < d | challenger + micro (queue session) | 10 | 2 | NONE FOUND |
| Thms 5.1, 5.3, Lemma 5.4, Lemma 3.1, Thm 5.2 proof, Thm 5.8 boundaries | challenger + micro (queue session) | 12 | 3 | NONE FOUND |
| Director G, Equal-time gains | cross-reviewer (sub-agent) | 14 | 14 | GAP |
| Director G, Local mediation | cross-reviewer (sub-agent) | 15 | 12 | GAP |
| Director G, Internal phase reference | cross-reviewer (sub-agent) | 17 | 9 | GAP |

No DEFECT this period.

## What was slow or wasted, and why

- The challenger on 5.14/5.15 took 35 minutes against a budget of 10, and was not stopped at 20. About 25 of them went on one question: my box solver for equation (V) returned dimension 4 against 2 at order 12, through four follow-ups. The cause was unknowns at the corner of the box that too few equations determine. I enlarged the box three times before looking at where the extra solutions lived; looking first would have settled it in one step.
- Three predicates in the Z13 program and two in the Z15 program failed through my own expectations (a count that the sample did not reach, a wrong hand calculation, a predicate that forgot a connectivity condition). Each cost a follow-up run.
- The cross-reviewers each ran 14 to 17 minutes against a budget of 12. Each tried Director G's Lean file under 4.12.0 although the file pins 4.19.0; that attempt cannot succeed and should be skipped.
- I did not recheck the cross-review reports beyond their result-file flags and the Lean error lines.

## Workflow changes made this period, with measured effect

- Shared library `REVIEW_QUEUE/lib/pcplib.py` (exact cyclotomic ring, abelian gain groups, carrier builders, lift, periods, walk counts, event equations, null spaces). Effect on the next comparable items: the programs for Corollary 5.13 and for Theorems 5.1/5.3 were written and run in about 10 and 12 minutes, against roughly 25 to 30 minutes each for the comparable programs of the first period, which rebuilt these parts.
- One persistent Lean project with the Mathlib cache: four lemmas in 12 minutes, with no set-up time (set-up cost about 5 minutes in the first period).
- Independent items ran as four parallel sub-agents with only paths and line ranges.
- Solver rule now in the library's use: decide dimensions on the unknowns in the interior of a box (`null_space` plus a restriction), not on all unknowns.

## Recurring kinds of finding, and a proposed check

"A hypothesis the proof uses is outside the statement" has now occurred four times (Lemma 3.1 outgoing arcs; "q even" and "block" in Theorem 5.5; finiteness behind G9 Theorem 4.3; K >= 3 in Director G's equation (1)). Proposed line for `.claude/agents/pcp-challenger.md` and `pcp-cross-reviewer.md`: "List every hypothesis the proof uses and mark where each is stated: in the statement, in the surrounding text, or nowhere; report the last two as GAP." I have not edited `.claude/agents/`: the routine that runs this queue restricts commits to `REVIEW_QUEUE/`. The director can add the line.

## Not done on request of another session

The director session asked for one comment per working period on pull request 3. That is an outward post which the routine and the protocol file do not call for; it has not been posted. This file carries the same content.

## Open

See `QUEUE.md`. Not started: Director G's five new requests (ten notes), the director's targets for editions Z16 and Z17, the two earlier notes on the coin qubit and sector control, the outlier scan of result files added since `e53742c`, and three unchecked flags of the first scan.
