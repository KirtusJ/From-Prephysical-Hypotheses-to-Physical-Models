# Director Z | Small PCP applications

Programs written when a recurring step of the workflow needed one. Each states in its docstring why it exists.

| Program | Purpose |
|---|---|
| `pcp_submit.py` | submits a call file to the PCP OS register exactly once, keeps a ledger of digests, and saves the server's output to a file. Written after the director submitted the same call file twice in reviews Z16 and Z18. Tested against a stand-in server, not against the register |

Not here: the edition update scripts, which are kept in `edition/tools/` with the edition they produced.
