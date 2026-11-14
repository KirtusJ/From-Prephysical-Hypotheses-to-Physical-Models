Target: .pcp/register.jsonl (530 records) against the files in the repository and its git history, at commit b07cff6. Chosen by the wildcard from the seed word "ledger".
Outcome: DEFECT (record integrity, two artifacts; nothing mathematical).
Reviewer kind: pcp-wildcard run as a sub-agent of the queue session (as a general agent reading .claude/agents/pcp-wildcard.md, because the type was not loaded when it started); the finding was rechecked by the queue session as stated below. Same model family as the author. Not independent review.

DEFECT. Two issued addenda are not the texts the register says were inspected, and the registered texts exist nowhere in git history.
- Edition Z18 addendum: registered with SHA-256 0c73c21e…2438 and size 8053 (records 374 and 391), declared inspected "all of it" (records 382 and 398), and cited as a basis of the finding at record 407. The issued file Director_Z/addenda/ADDENDUM_EDITION_Z18_SESSION_4.md has 8330 bytes and digest 527e17e9….
- Edition Z22 addendum: registered with SHA-256 41b05c87…ccb3 and size 4801 (record 492, 20:35:09 UTC), declared inspected at record 498. The issued file has 4934 bytes and digest a2594f9b…, committed in f37613b at 20:35:41 UTC, 32 seconds later.
Both records carry "stored": false, so the register kept no copy. A line-ending conversion does not explain either difference (the CRLF forms have other digests, and the sizes differ by 277 and 133 bytes). The sub-agent also tried removing every single contiguous span from the issued files and reproduced neither digest, so what changed between registration and commit cannot be recovered.
What this means: for these two addenda the register's inspection records and one finding's basis refer to texts that were not issued. It says nothing about whether the issued texts are right.

What holds
- The other 131 of 133 distinct artifact digests in the register, every revision of paper G10 among them, match a blob in git.
- The hash chain is intact (529 links, contiguous sequence numbers, non-decreasing times), and the edition's copy of the register is byte-identical to .pcp/register.jsonl.

Second point (from the same program, predicate L3)
- 23 objection records carry the resolution OPEN_RECORDED, while all 20 REVIEW_CLOSED records list "open_objections": [] with lifecycle CLOSED_COMPLETE. For edition Z23 the gate note says "one objection is recorded open" and the closing record lists none. A reader of the closing records alone counts no standing objection. Whether this is the register program's definition of "open" or an omission is for the director to say; CLAUDE.md asks that objections that stand be recorded open.

Third point (wording): the register's gates G1, G5, G6 are review-procedure gates; they share labels with papers G1, G5, G6. One line in the session's README would prevent a misreading.

How to check: `python3 -I ledger_bytes.py <repository> <fresh directory>` (program beside this report; predicates L1 to L3 in its docstring; L2 and L3 fail and are kept). The sub-agent reran it in a second directory with a byte-identical result.

Rechecked by the queue session: the six register records and their digests and sizes; the sizes and SHA-256 of the two issued files; that the CRLF forms do not match; the commit time of f37613b; the counts 20 closed reviews with empty open_objections and 23 records with OPEN_RECORDED. Not rechecked: the 131 matching digests, the hash chain, the span-deletion search.

Suggested by the sub-agent, for the director to decide (the queue does not edit registers or tools): record the mismatch in the next addendum; have the submit tool refuse a commit when a registered file's digest differs from the file on disk.
Cost reported by the sub-agent: about 6 minutes, 12 tool calls.
