# Status of the review queue

Working period: 13 November 2026, 21:05 to about 21:40 UTC (third period of the day). Targets at commit `fd0b682` (edition Z23); branch merged with `master` at that commit.

Reviewers are of the author's model family. Nothing here is independent review. No PCP calibration record exists for this queue session: the method text and the `pcpos` tool are not in this container.

## Items

| Item | Agent | Minutes | Tool calls | Outcome |
|---|---|---|---|---|
| Cor. 5.28 on a carrier with C_0 != C; Cor. 5.29 bound with loops at every vertex | micro-review (queue session) | 12 | 3 | NONE FOUND |
| Cor. 5.29: count of returning walks; recurrence of unitary powers | formalizer (sub-agent), rerun by the session | 6 + 2 | 6 + 1 | NONE FOUND, both check |

No DEFECT and no GAP this period.

## Scope chosen, and why

The queue held 17 open entries at the start. The director's note for edition Z18 says this session shares the account's model limit with the director. I therefore served only the two newest director targets that could be done by enumeration and by one short Lean task, with one sub-agent, and left the rest. Reading the two statements and their context took most of the time: about 100 long lines of the paper for a two-minute micro-review.

## What was slow or wasted

- The micro-review ran 12 minutes against a budget of 2. The enumeration itself took 50 seconds; the rest was reading the statement and the text around it. A micro-review target that comes with the line range and the definitions it needs (here: the form of the rule, the meaning of C_0 and of the classes of characters) would fit the budget.
- The sympy solution of the multiplicativity equations at length 4 took 40 of the 50 seconds; reducing the equations to a Groebner basis over the value pairs first would cut it.

## Workflow change this period and its effect

- Both items reused `REVIEW_QUEUE/lib/pcplib.py` and the standing Lean project: no set-up time, one program, one sub-agent. The formalizer delivered two general statements in 6 minutes (the comparable first Lean item of the day took about 15 with set-up).
- Proposed for the director (not done here, it changes how targets are written): give each "Wanted" entry the line range of the statement and of the definitions it uses.

## Not done on request of another session

The per-period comment on pull request 3 asked for by the director session is not posted: it is an outward post that the routine and the protocol file do not call for. This file carries the content.

## Open

See `QUEUE.md`: 17 entries. Not started this period: the challenger parts for editions Z16, Z17, Z20, Z21, Z22; the micro-review parts for Z16, Z17, Z19, Z20, Z21; the reading of G10 as issued in Z18; Director G's five requests (some are answered in the director's addenda 6 to 10 and can be closed by their author); the two earlier notes on the coin qubit and sector control; the outlier scan of files added since `e53742c`.
