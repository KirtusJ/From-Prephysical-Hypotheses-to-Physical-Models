# Director Z | Small PCP applications

Programs written when a recurring step of the workflow needed one. Each states in its docstring why it exists.

| Program | Purpose |
|---|---|
| `pcp_submit.py` | submits a PCP OS call file, skips a digest already in the completed-submission ledger and saves the server's replies. Written after the director submitted the same call file twice in reviews Z16 and Z18. Tested against a stand-in server and used on the register from review Z22 on |

The ledger counts successful calls, refusals and replies bearing the host's explicit `WRITTEN as event` receipt. A status lookup can succeed, and a session can begin, without such a receipt. Older ledger entries stored successful calls in `written`. Use the register itself when counting appended events.

Each completed submission has a separately created reply file in `submission_replies/`. Its ledger row records the file path in `output` and the SHA-256 of its UTF-8 bytes in `output_sha256`. Changed calls at the same path and explicit `--again` submissions receive new files. `<calls.json>.out` shows the latest replies. If an older ledger row refers to that path, the submitter preserves it and uses `<calls.json>.latest.out` for the view. A row's `latest_output` gives the chosen view. Files already lost before this change cannot be reconstructed from a legacy row.

Submitters sharing one ledger serialize the digest check, host calls and completed row. A concurrent ordinary retry therefore returns 4 after the first submission completes. An interruption between a host write and recording the completed row can leave an unledgered effect. Check the register before resubmitting such an interrupted batch.

The edition update scripts are kept in `edition/tools/` with the edition they produced.
