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

## Can sub-agents work recursively? (tested 13 November 2026, at the principal's request)

| Route | Depth below the director | Result |
|---|---|---|
| A sub-agent started with the director's Agent tool, asked to start its own sub-agent | 1 | Not possible. A sub-agent of any type, general-purpose included, has no Agent tool and is offered no agent types. The `pcp-*` definitions also list only Bash, Read, Grep, Glob, Write. The test agent stopped and said so; it did not simulate delegation |
| A headless worker (`claude -p`) started from a shell, asked to start a sub-agent | 2 from whoever runs the shell | Works. The worker has the Agent tool; its sub-agent wrote the test file (`NESTED OK`). Since every `pcp-*` sub-agent has a shell, a sub-agent can reach depth 3 this way (director, sub-agent, headless worker, its sub-agent) |
| The unattended cloud session (the review queue) starting sub-agents | 2 | Works and was used: its formalizer and three cross-reviewers of the second batch were sub-agents of that session |
| A sub-agent starting a new cloud session | not tried | The tool is visible to sub-agents; it spends the account's limit, which is what stopped the queue session |

What this means for the review stack:

- Recursion is available, but not through the ordinary sub-agent call. It needs the shell route or a cloud session.
- PCP OS does not see any of it: its task events come from hooks, which do not fire for headless workers or for sub-agents' shells (found earlier in this session). A nested worker therefore leaves no register event unless the parent submits one for it.
- Each level multiplies cost and shares one account limit. A nested worker also starts cold, with no agent definition unless the prompt carries it.
- Use so far: none in the edition. The flat stack (director to sub-agent) has been enough, because the director reads every report anyway. Where nesting would pay: a challenger that could hand one algebraic step to a formalizer and get the answer inside its own budget. To try once, with the shell route, on the next statement that has such a step; record cost and whether the report improves.

Director G reports the other outcome on their side (`AGENTS.md`, 13 November 2026): a Codex sub-agent started a PCP-equipped child with its own collaboration tool, two levels, with separate stores whose digests matched. So direct recursion depends on the host: available to Codex sub-agents, not to Claude sub-agents in this container.

### Nesting trial (13 November 2026, for G10 Theorem 5.26)

A challenger sub-agent was allowed one headless worker (`claude -p` from its shell) to formalize a small step in Lean and to use the answer inside its own report. Outcome: the worker returned a correct file in 53 seconds on the first attempt; the challenger reran it (exit code 0) and so did the director. The challenger's whole run took about 7 minutes and 92 thousand tokens, against 4 to 6 minutes and 50 to 70 thousand without nesting, and its report carried the Lean statement verbatim. Worth it when the step is small and sharply stated; the director still reruns the file. PCP OS recorded nothing of the nested worker, as expected.

## Limits of recursion (tested 13 November 2026, at the principal's request)

Scripts and logs: `recursion/` beside this file. Route: headless workers started from a shell, each starting the next.

| Test | Result |
|---|---|
| Relay of a token down a chain and back, 1, 2, 3, 5, 8 levels | Correct at every depth. 11, 21, 30, 51, 87 seconds: about 11 seconds per level, linear. No mechanical limit was reached at depth 8 |
| A fully specified counting task restated in each level's own words, 4 levels, solved at the bottom | Correct answer (eight numbers, checked against the director's own program). 78 seconds against 16 for one level. The text grew from 181 to about 300 words at the first restatement and then stayed; every condition survived; the vocabulary changed ("closed" became "sealed", "good" became "rich") |
| Fixed cost of one headless worker that does nothing | about 36 thousand tokens of context, mostly cached, 3 to 6 seconds, about 0.12 to 0.14 dollars as the tool reports it; a worker that runs one shell command about 73 thousand |
| Earlier: a challenger that delegated one Lean step | 53 seconds for the worker; useful |
| Direct nesting through the Agent tool | not available to sub-agents here (depth 1 only) |

Where recursion stops being efficient in this workflow:

1. Depth is not the limit; a level that adds nothing is. Every level costs a cold start (tens of thousands of tokens and 10 to 20 seconds) whatever it does. A level pays only if it brings something the level above lacks: a different tool (Lean), parallel width, or a context kept free of the parent's notes.
2. The director's recheck does not get cheaper with depth. Rule 3 of the stack (reread every report, rerun its files) applies to what comes back at the top; errors made two levels down are visible only through files, so nested workers must leave result files, not just an answer. Beyond depth 2 the director is rereading reports about reports.
3. Names drift. A task restated four times kept its meaning and changed its terms. For work on a paper, where labels and defined terms matter, a nested worker must be given the text or the file path, not a restatement.
4. The register sees none of it. PCP OS records no event for a nested worker; the parent must submit one, which adds a step per level.
5. One account limit is shared by all levels, and it is what stopped the unattended queue session.

Working rule drawn from this: at most two levels below the director (sub-agent, plus one headless worker for a sharply stated step with a machine-checkable answer); pass file paths, not paraphrases; every nested worker writes a result file that the director can rerun. Deeper chains work and are kept as a tested option, not a default.

## Small applications

`Director_Z/tools/pcp_submit.py` was written after the second duplicate register submission: it refuses to send a call file whose digest is already in its ledger and saves the server's output to a file. This is rule 6 turned into a program. Applications are written only when a step has failed more than once or recurs at every edition.

## Pull requests from the stack (13 November 2026)

Principal: sub-agents and workers may open pull requests on all repositories and branches when necessary. Adopted as: patch file from sub-agents without GitHub tools, pull request from workers that have them, author never merges. Observed the same day: the director's own merge of another author's branch (Director G's pull requests 5, 6, 8) was refused by the session's permission layer, so merging is by the author or the principal. To watch: whether any worker opens one, and whether it was needed.

## Wider propagation, positive arcs, wildcard and chaos roles (13 November 2026)

Principal: propagate among the stack more and see if it works; not only negative arcs but positive ones; include wildcard parrots and chaos parrots. Adopted as three agent definitions (`pcp-builder`, `pcp-wildcard`, `pcp-chaos`) and rule 7 of the stack in `CLAUDE.md`.

First use, on Director G's candidate G1 and pull request 22: six narrow agents in parallel (theorem, premises, citations, mechanics, Lean and fixed rings, the parity note) in place of one reading by the director, then one builder, one wildcard and one chaos agent. What to record when they report: how many findings were new to the director, how many reports needed correction on recheck, wall time against a single reading, and for the chaos agent the count caught / survived.

### Result of the first wide fan-out (13 November 2026, about 23:00 UTC)

It did not work as launched. Eleven sub-agents started within a few minutes, with the queue session woken at the same time, used up the account's five-hour model allowance in about six minutes of wall time; all eleven stopped with rate-limit errors (reset 01:30 UTC) and none delivered a report. What was saved: the agents that had been told to append to `FINDINGS.md` as they went left usable partial work (citations: 11 of 11 links assessed; theorem: hypothesis list; mechanics: 4 of 8 items; pull request 22: rerun, own program and a patch); the agents that had not yet written anything left programs without findings.

What changes:
- Width is limited by the allowance, not by the tool. At most three sub-agents at once, and the queue session is not woken in the same window.
- The rule "append to FINDINGS.md after each item" is what made the stop survivable; it stays in every prompt, and the first item of every prompt is now the cheapest one that yields a usable result.
- Long prompts with eight items cost more than they return when the agent is cut off; prefer one or two items per agent.
- Stopped agents are resumed by message with their saved context, not relaunched.

### Second attempt, three at a time (13 to 14 November 2026)

Seven stopped agents were resumed by message in two batches of three and one; all seven reported. Tokens per resumed agent: 95k to 160k. The mechanics challenger and the case-study fact-check were not resumed (the director did the case-study check by hand in two commands).

| Role | New to the director | Needed correction on recheck | Note |
|---|---|---|---|
| Premises attack (negative) | yes: conservation alone leaves 37 dimensions by tick 12 when the detector sees both route numbers | none; director's rerun reproduced ticks 9 to 12, timed out at 14 | the decisive finding on G1 |
| Builder on G1 (positive) | yes: a weaker premise plus one measurement replaces "signed total only" | none; proof read, program rerun byte-identical | the attack's wound came back with its repair |
| Builder on product events (positive) | yes: the target was false as posed, with two explicit counterexamples | none found | a refuted strengthening is a result |
| Chaos | yes: 16 of 34 planted errors survive the checks | patch applies; not yet in the edition | first measurement of what the checks miss |
| Wildcard | yes: recomputed a table the director had not; one sentence of G10 depends on horizon | none | chose a record marked "not recomputed" |
| Lean and fixed rings | no defect; coverage limits of the Lean file | none; recompiled | did not write FINDINGS.md, citing a standing instruction of its own |
| Citations | prior art absent; network block found | page bodies not opened | search summaries only |

What worked: a builder beside each attacker; resuming by message; narrowing the brief on resume to one or two items. What did not: eleven at once; eight-item briefs; relying on WebFetch (arxiv.org and claymath.org are not reachable from this session).
