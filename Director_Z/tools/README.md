# Director Z | Small PCP applications

Programs written when a recurring step of the workflow needed one. Each states in its docstring why it exists.

| Program | Purpose |
|---|---|
| `pcp_submit.py` | submits a PCP OS call file, skips a digest already in the completed-submission ledger and saves the server's replies. Written after the director submitted the same call file twice in reviews Z16 and Z18. Tested against a stand-in server and used on the register from review Z22 on |

The ledger counts successful calls, refusals and replies bearing the host's explicit `WRITTEN as event` receipt. A status lookup can succeed, and a session can begin, without such a receipt. Older ledger entries stored successful calls in `written`. Use the register itself when counting appended events.

The edition update scripts are kept in `edition/tools/` with the edition they produced.
