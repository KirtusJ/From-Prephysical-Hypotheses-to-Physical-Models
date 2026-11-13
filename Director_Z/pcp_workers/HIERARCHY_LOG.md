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
| After Z18 | Read the queue branch again and found a second batch of seven reports, pushed after the director's last look and before the session stopped | The queue had answered a question the paper left open, added four Lean checks and proposed a line for the challenger definition, now adopted; its shared library cut its own program time by about half | The director had asked for one comment per working period on the channel pull request; the queue session declined it as outside its protocol, so nothing announced the batch. The director must fetch the branch, not wait for a signal |

## Current rules that follow from the log

1. A sub-agent's failed predicates are the director's to record. When a report is filed, its failed predicates are named in the addendum, not only kept in the result file.
2. After a correction, search the whole paper for the same claim (abstract, introduction, assumptions, status table) before issue.
3. A full comb is run when the principal asks for one, not on a schedule (principal's instruction after edition Z18). Rule 2 carries the sideways propagation in between.
4. Check the child session's status at the start of each working period; a trigger that reports success only says the wake was delivered.
5. Report counts as "met, failed, measured only", never as "n of n" when a predicate has no verdict.
6. A register call file is submitted once, with its output saved to a file and read afterwards. Counts come from a program, not from reading a listing.
7. A rewriting by the director is new text and goes to a challenger like any other.

All reviewers in this hierarchy are of the director's model family. Their agreement reduces exposure and is not independent review.

## How the sub-agents work with the workflow (observations, newest last)

Looked at from time to time, at the principal's request. Figures are those the harness reports when an agent finishes.

| Tier | Typical cost per run | What they do well | Where they drift | Change made |
|---|---|---|---|---|
| Challenger | 45 to 60 thousand tokens, 5 to 12 tool calls, 3 to 6 minutes | Read every step; write an own program without being told how; keep failed predicates and say which were their own fault; end with what was not checked | Rarely look outside the lines they were pointed at, so stale sentences elsewhere survive; a first predicate often fails through the reviewer's own expectation and costs a follow-up | Prompt now names the summary paragraph and asks for a list of hypotheses with where each is stated |
| Micro-review | about 35 thousand tokens, 4 tool calls, 1 to 2 minutes | Cheapest check that still finds real wording faults (spans versus bases; j = -j) | Needs the cases listed for it; left alone it picks easy ones | Cases are listed in the prompt; an unlisted case is asked for |
| Formalizer | 20 to 35 thousand tokens, 3 to 7 tool calls, 1 to 3 minutes | Returns statements more general than asked and says exactly what was not proved; twice a shorter argument | Proves the lemma as phrased; whether the lemma is the step the paper uses is the director's check, not its | The prompt quotes the paper's sentence and asks which form (row or column, left or right) that sentence needs |
| Cross-reviewer | 55 to 85 thousand tokens, 9 to 12 tool calls, 5 to 13 minutes, over its 12-minute budget about half the time | Reproduces numbers exactly; reruns a checker byte for byte; separates what the Lean file proves from what the note says | Tried the wrong Lean version until told; the long ones spend their time on a second or third note in one request | Lean version stated in the agent definition; one request is split when it names more than two notes |
| Proof search (general agent) | 120 to 150 thousand tokens, 11 to 15 tool calls, 8 to 15 minutes | Explores exactly first, then proves; states hypotheses its proof uses; twice proved more than was conjectured | Writes examples and remarks that go beyond what it checked (an example true under one of four conventions); labels in its programs are sometimes wrong while the numbers are right | Everything it writes beyond the theorem goes to a challenger as separate items |

Across about forty runs: no report was found false on recheck of its files. The errors that reached an edition or a status note were the director's (a rewritten summary with nine faults, a miscount of reruns, two duplicate register submissions). The stack therefore protects the paper better than it protects the director's own prose and bookkeeping; rules 6 and 7 above are aimed at that.

Things that cost time without benefit: an agent lost at a session restart with nothing on disk (now asked to append findings to a file as it goes); two programs timing out at four minutes and needing a second pass (the limit is now set from the stored run time); reports longer than asked, which is harmless.

Not yet tried, worth trying: giving the challenger the previous challenger's list of what was not checked, so the second one starts there; a fixed report skeleton (verdict table first) so that reports can be compared by a script.

