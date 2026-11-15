Target: edition/verify_baseline.py as on master a8c9608 (it carries the queue's second chaos patch), on a copy of the edition.
Control: the untouched copy passes (exit 0). Control passed.
Outcome: DEFECT in the check, smaller than before: 14 of 40 planted errors pass (22 of 32 did on 14 November).
Reviewer kind: pcp-chaos run as a sub-agent of the queue session; copies only; the repository was untouched. The queue session rechecked what is stated at the end. Same model family as the author.

Baseline: exit 0, 1842 files, 41 papers, 434 registry rows. Outside the repository two checks are skipped with a notice (predecessor digest: no git history; live register: no .pcp/), so the mutant runs supplied copies of both; with them the copy also passes. pdfinfo is present, so the page check runs; PyMuPDF is absent, so the front-matter check is skipped.

Counts: CAUGHT 25, SURVIVED 14, EQUIVALENT 1 (registry line endings). Of the 32 kinds replanted: 21 caught, 10 survived. Of 8 new kinds: 4 caught.
Earlier survivors now caught (9): page count, predecessor digest, register copy truncated at the end or the start or altered and re-chained (three), a result file cut short, a planned paper with registry rows, the count sentence removed, a fake compiled file. Four of these are caught only when git history and .pcp/ are reachable; in a bare copy they pass with a notice.

Remaining survivors and the cheapest check
- A digit in a result file; all_pass changed from true to false: rerun and compare bytes.
- A registry status word: a reader.
- A count in the addendum's summary: recompute from the chaos result file (one line).
- The verifier disabled inside the tree: run a trusted copy from git, from outside.
- Three program changes (a loop, a predicate): record each program's source digest in its result file and compare.
- A Lean hypothesis deleted; a proof replaced by sorry: build with Lean, or grep for sorry and compare statements with the predecessor.
- Register copy missing its last lines: require its last sequence number to equal the one recorded in the edition's review (one line).
- A file renamed, removed or added together with its manifest entry: compare the manifest with the predecessor's plus the edition's list of changes (about ten lines).
- A row removed with all counts lowered to agree: compare with the predecessor registry (one line).
- A result truncated and renamed to a name containing "partial" (escapes the parse check): forbid new partial files not in the predecessor (one line).
- A compiled-file name whose first bytes pass the magic test with arbitrary content: reject every .pyc (one line).

Rechecked by the queue session: the control log; the counts in chaos3_result.json. Not rechecked: the 40 runs.
Cost reported by the sub-agent: about 6 minutes, 9 tool calls.
