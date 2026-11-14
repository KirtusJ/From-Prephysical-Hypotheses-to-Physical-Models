# Wildcard, seed "ledger" - 14 November 2026

Chosen: `.pcp/register.jsonl` (530 records) read as a ledger: does each entry bind to bytes that exist?
Program `ledger_bytes.py`, result `run1/ledger_bytes_result.json` (run2 byte-identical). Predicates fixed in the docstring first.

- L1 PASS. Hash chain intact (529 links, prev = SHA-256 of preceding line), seq contiguous, timestamps monotone. Register copy in edition is byte-identical.
- L2 FAIL (kept). 131 of 133 distinct artifact digests match a blob in git history. Two match nothing:
  - addendum_Z18, 0c73c21e..., 8053 bytes, seq 374 and 391; inspected "all of it" at 382, 398; basis of finding at seq 407. Issued file is 8330 bytes.
  - addendum_Z22, 41b05c87..., 4801 bytes, seq 492; inspected at 498 (20:35:09Z). Issued file is 4934 bytes, committed f37613b 20:35:41.
  Deleting any single contiguous span of the issued file does not reproduce either digest (tried all offsets), so the reviewed texts cannot be recovered; `stored` is false and `.pcp/artifacts/` holds one file.
- L3 FAIL (kept). 23 objections have resolution OPEN_RECORDED; all 20 REVIEW_CLOSED records list open_objections [] with lifecycle CLOSED_COMPLETE. Seq 527 note says "one objection is recorded open"; seq 529 lists none.
- Not found: any gate-id collision between register gates G1/G5/G6 and ONTOLOGY_GATE_MAP (ids P0...); the register gates are review-procedure gates.
