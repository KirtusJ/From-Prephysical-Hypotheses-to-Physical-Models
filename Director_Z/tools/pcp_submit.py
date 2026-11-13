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
Files:        <repository_root>/Director_Z/tools/submitted_calls.jsonl   ledger of completed submissions
              <repository_root>/Director_Z/tools/submission_replies/    one reply file per submission
              <calls.json>.out                latest view (or .latest.out if .out is a legacy receipt)
Exit code: 0 if every call succeeded; 3 if any call was refused; 4 if the file was already submitted; 2 on usage.
The program carries calls; what the register accepts is decided by pcpos."""
import errno, hashlib, json, os, subprocess, sys, tempfile, time
from contextlib import contextmanager
from pathlib import Path


@contextmanager
def submission_lock(directory):
    """Serialize the digest check, host call and completion record for this ledger."""
    directory.mkdir(parents=True, exist_ok=True)
    with (directory / ".pcp_submit.lock").open("a+b") as lock:
        if os.name == "nt":
            import msvcrt
            if lock.tell() == 0:
                lock.write(b"0")
                lock.flush()
            lock.seek(0)
            while True:
                try:
                    msvcrt.locking(lock.fileno(), msvcrt.LK_NBLCK, 1)
                    break
                except OSError as error:
                    if error.errno != errno.EACCES:
                        raise
                    time.sleep(0.05)
        else:
            import fcntl
            fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
        yield  # Closing the descriptor releases the lock, including after a process exit.


def replace_view(path, data):
    view = tempfile.NamedTemporaryFile(dir=path.parent, delete=False)
    temp_path = Path(view.name)
    try:
        with view:
            view.write(data)
        os.replace(temp_path, path)
    finally:
        temp_path.unlink(missing_ok=True)

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
    root, calls_path = Path(args[0]).resolve(), Path(args[1]).absolute()
    raw = calls_path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    calls = json.loads(raw)
    ledger = root / "Director_Z" / "tools" / "submitted_calls.jsonl"
    with submission_lock(ledger.parent):
        return submit(root, calls_path, digest, calls, ledger, again)


def submit(root, calls_path, digest, calls, ledger, again):
    seen = []
    if ledger.exists():
        with ledger.open(encoding="utf-8") as stream:
            seen = [json.loads(line) for line in stream if line.strip()]
    prior = [e for e in seen if e["sha256"] == digest]
    if prior and not again:
        print(f"ALREADY SUBMITTED: {os.path.basename(calls_path)} ({digest[:12]}) at {prior[-1]['time']}: "
              f"{summary(prior[-1])}. Read {prior[-1]['output']}; nothing sent.")
        return 4
    # Preserve every recorded path. Old rows may point to the mutable view itself.
    latest = Path(str(calls_path) + ".out")
    old_outputs = [Path(row["output"]) for row in seen]
    archived_paths = {path.resolve() for path in old_outputs}
    # Historical relative paths did not record the working directory.
    while latest.resolve() in archived_paths or any(
        not path.is_absolute() and latest.match(path) for path in old_outputs
    ):
        latest = latest.with_suffix(".latest.out")
    archives = ledger.parent / "submission_replies"
    archives.mkdir(exist_ok=True)
    binary = os.environ.get("PCPOS_BIN", "pcpos")
    env = dict(os.environ); env["PCPOS_ROOT"] = str(root)
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
    p.wait()
    p.stdout.close(); p.stderr.close()
    report = ("\n".join(lines) + ("\n--- server stderr: " + err if err else "") + "\n").encode("utf-8")
    with tempfile.NamedTemporaryFile(dir=archives, prefix=digest + "-", suffix=".out", delete=False) as archive:
        archive.write(report)
        archive.flush()
        os.fsync(archive.fileno())
        out_path = archive.name
    entry = dict(sha256=digest, file=calls_path.name,
                 time=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), calls=len(calls),
                 succeeded=succeeded, refused=len(refusals), write_receipts=write_receipts, output=out_path,
                 output_sha256=hashlib.sha256(report).hexdigest(), latest_output=str(latest))
    with ledger.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")
        f.flush()
        os.fsync(f.fileno())
    print(f"{entry['file']} ({digest[:12]}): {len(calls)} calls, {summary(entry)}; output in {out_path}")
    try:
        replace_view(latest, report)
    except OSError as error:
        print(f"Replies saved; could not refresh {latest}: {error}", file=sys.stderr)
    for reply in refusals:
        print(reply[:300])
    return 3 if refusals else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
