#!/usr/bin/env python3
"""pcp_submit: submit a PCP OS call file and save its replies.

Why it exists. On 13 November 2026 the director twice submitted the same call file to the register a second time
through a diagnostic command (reviews Z16 and Z18); the register is append-only and keeps the duplicates. This program
checks completed submissions by digest before sending a file again. Read the saved replies after a completed
submission.

Usage:  pcp_submit.py <repository_root> <calls.json> [--again]
  calls.json   a list of {"name": <tool>, "arguments": {...}} for the pcpos tool server (acr_artifact, acr_submit, ...)
  --again      submit although the ledger already holds this file's digest (the earlier entry stays in the ledger)
Environment:  PCPOS_BIN  path of the pcpos program (default: "pcpos" on PATH)
Files:        <repository_root>/Director_Z/tools/submitted_calls.jsonl   ledger: digest, file name, time, counts
              <calls.json>.out                                the server's full output for this submission
Exit code: 0 if every call succeeded; 3 if any call was refused; 4 if the file was already submitted; 2 on usage.
The program carries calls; what the register accepts is decided by pcpos."""
import hashlib, json, os, subprocess, sys, time

def summary(counts):
    if "succeeded" in counts:
        receipts = counts["write_receipts"]
        label = "receipt" if receipts == 1 else "receipts"
        return f"{counts['succeeded']} succeeded, {counts['refused']} refused, {receipts} write {label}"
    return f"{counts['written']} succeeded, {counts['refused']} refused (legacy counts)"


def main(argv):
    args = [a for a in argv[1:] if not a.startswith("--")]
    again = "--again" in argv
    if len(args) != 2:
        print(__doc__); return 2
    root, calls_path = os.path.abspath(args[0]), args[1]
    raw = open(calls_path, "rb").read()
    digest = hashlib.sha256(raw).hexdigest()
    calls = json.loads(raw)
    ledger = os.path.join(root, "Director_Z", "tools", "submitted_calls.jsonl")
    seen = []
    if os.path.exists(ledger):
        seen = [json.loads(l) for l in open(ledger) if l.strip()]
    prior = [e for e in seen if e["sha256"] == digest]
    if prior and not again:
        print(f"ALREADY SUBMITTED: {os.path.basename(calls_path)} ({digest[:12]}) at {prior[-1]['time']}: "
              f"{summary(prior[-1])}. Read {prior[-1]['output']}; nothing sent.")
        return 4
    binary = os.environ.get("PCPOS_BIN", "pcpos")
    env = dict(os.environ); env["PCPOS_ROOT"] = root
    p = subprocess.Popen([binary, "mcp"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         env=env, text=True, cwd=root)
    def send(o):
        p.stdin.write(json.dumps(o) + "\n"); p.stdin.flush()
    send({"jsonrpc": "2.0", "id": 0, "method": "initialize",
          "params": {"protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "pcp_submit", "version": "1"}}})
    p.stdout.readline()
    send({"jsonrpc": "2.0", "method": "notifications/initialized"})
    lines, refusals = [], []
    succeeded = write_receipts = 0
    for i, c in enumerate(calls, 1):
        send({"jsonrpc": "2.0", "id": i, "method": "tools/call", "params": {"name": c["name"], "arguments": c.get("arguments", {})}})
        r = json.loads(p.stdout.readline())
        result = r.get("result", {})
        text = "\n".join(b.get("text", "") for b in result.get("content", []))
        if "error" in r: text += "\nRPC ERROR " + json.dumps(r["error"])
        kind = c.get("arguments", {}).get("kind", "")
        reply = f"=== [{i}] {c['name']} {kind}\n{text}"
        lines.append(reply)
        header = text.lstrip()
        if ("error" in r or "result" not in r or result.get("isError")
                or header.startswith("REFUSE (exit code ")):
            refusals.append(reply)
        else:
            succeeded += 1
            if header.startswith("WRITTEN as event "):
                write_receipts += 1
    p.stdin.close(); err = p.stderr.read().strip()
    out_path = calls_path + ".out"
    with open(out_path, "w") as f:
        f.write("\n".join(lines) + ("\n--- server stderr: " + err if err else "") + "\n")
    os.makedirs(os.path.dirname(ledger), exist_ok=True)
    entry = dict(sha256=digest, file=os.path.basename(calls_path),
                 time=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), calls=len(calls),
                 succeeded=succeeded, refused=len(refusals), write_receipts=write_receipts, output=out_path)
    with open(ledger, "a") as f:
        f.write(json.dumps(entry) + "\n")
    print(f"{entry['file']} ({digest[:12]}): {len(calls)} calls, {summary(entry)}; output in {out_path}")
    for reply in refusals:
        print(reply[:300])
    return 3 if refusals else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
