# Director Z | Review hierarchy: what changed, what worked, what did not

A running log, newest last. One entry per change of the parent-child structure or of how findings travel. Short on purpose. Method lives in `CLAUDE.md`; this file records why it moved.

| When (13 Nov 2026) | Change | Worked | Did not work |
|---|---|---|---|
| Edition Z10 | First challenger sub-agent, given the paper text only | Found a missing hypothesis in a corollary before issue | Nothing checked the summary sentences |
| Edition Z11 | Formalizer tier (Lean, then Mathlib) | Twice gave a shorter proof; once exposed an arithmetic slip of the director | Covers single algebraic steps only; no statement about carriers is formalized |
| Edition Z12 | Micro-review tier: one narrow target, about 8 tool calls | Cheap; catches boundary wording (q = 2, j = -j, spans versus bases) | Too narrow to notice a stale sentence elsewhere in the paper |
| Edition Z12 | Agent definitions in `.claude/agents/`, file queue in `REVIEW_QUEUE/` | Any session can serve the queue; Director G uses it to request cross-reads | Depends on someone running it |
| Edition Z13 | Unattended child session on a three-hour trigger, reporting to branch `pcp/review-queue`, draft pull request 3 as channel | Eight reports in one sweep, all usable after recheck | Stopped when the account's weekly model limit was reached; a child shares the parent's budget and fails silently. Found only by looking at the session |
| Editions Z14 to Z17 | Proof search delegated: director states a conjecture with exact evidence, a general-purpose sub-agent proves or refutes it | Four theorems (5.12, 5.14, 5.16, 5.18), two of them stronger than the conjecture | The director's own first versions were wrong twice; the sub-agent's statement must be reread line by line before it enters the paper |
| Editions Z14 to Z17 | Challenger is also sent the corollaries and the summary paragraph | Every edition since: the proof stood, the summary was wrong | The correction was applied where the challenger pointed and not to the same sentence elsewhere (the word "finite" in the introduction, one edition late) |
| After Z17 | Full comb: two readers over the whole paper, a rerun of every program, a scan of all result files and registers | Found stale abstract and assumptions list, unrecorded failed predicates in reviewer programs, a folder named in the records and never copied | Reveals that propagation was upward only for the statement under review; nothing propagated sideways to summaries, README counts and older register entries |
| Edition Z18 | The director's rewritten summaries were sent to a third sub-agent before issue | Nine further errors found in the rewriting, two of them false sentences | The director twice re-submitted a register call file through a diagnostic command, and miscounted reruns by one; both found only because the register and a counting script were consulted |

## Current rules that follow from the log

1. A sub-agent's failed predicates are the director's to record. When a report is filed, its failed predicates are named in the addendum, not only kept in the result file.
2. After a correction, search the whole paper for the same claim (abstract, introduction, assumptions, status table) before issue.
3. Every third edition, or when a result changes what is assumed, run the full comb.
4. Check the child session's status at the start of each working period; a trigger that reports success only says the wake was delivered.
5. Report counts as "met, failed, measured only", never as "n of n" when a predicate has no verdict.
6. A register call file is submitted once, with its output saved to a file and read afterwards. Counts come from a program, not from reading a listing.
7. A rewriting by the director is new text and goes to a challenger like any other.

All reviewers in this hierarchy are of the director's model family. Their agreement reduces exposure and is not independent review.
