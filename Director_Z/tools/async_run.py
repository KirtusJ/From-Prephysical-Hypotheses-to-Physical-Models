#!/usr/bin/env python3
"""async_run: run several commands at once, each in its own fresh directory, and say afterwards exactly what ended how.

Why: asynchronous work fails quietly. In this session a worker was cut off with nothing on disk, a result was
reported before its rerun had finished (it had in fact exited with an error), and a call file was sent twice.
This helper makes the end of every task a recorded fact: exit code, duration, timeout or not, and the SHA-256
of each file the task left, read back from disk after the task has exited.  Nothing is claimed for a task whose
exit code is not zero.  It is a workspace helper in Python, not part of PCP OS (Rust holds primacy there).

Usage: python3 async_run.py <plan.json> <fresh output directory>
  plan.json: {"tasks": [{"id": "T1", "argv": ["python3", "prog.py", "out.json"], "timeout": 600,
                         "expect_exit": 0, "copy": ["prog.py"]}, ...], "width": 3}
  Each task runs in <output directory>/<id>/ (created here; the run stops if the directory exists).  "copy"
  lists files, relative to the plan's folder, copied into the task's directory first.  At most "width" tasks
  run at once (default 3; the account's allowance is the limit, see HIERARCHY_LOG.md).
  Writes <output directory>/ASYNC_RECORD.json (mode 'x') and prints one line per task.
Exit code: 0 if every task ended with its expected exit code and inside its timeout; 6 otherwise; 2 on usage.
"""
import hashlib, json, os, shutil, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor

def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()

def run(task, plan_dir, out):
    d = os.path.join(out, task["id"]); os.makedirs(d)          # fails if it exists: never reuse a directory
    for f in task.get("copy", []):
        shutil.copy(os.path.join(plan_dir, f), d)
    before = set(os.listdir(d)); t0 = time.time(); timed_out = False
    try:
        r = subprocess.run(task["argv"], cwd=d, capture_output=True, timeout=task.get("timeout", 600))
        code = r.returncode; so, se = r.stdout, r.stderr
    except subprocess.TimeoutExpired as e:
        timed_out, code, so, se = True, None, e.stdout or b"", e.stderr or b""
    except OSError as e:
        code, so, se = None, b"", str(e).encode()
    open(os.path.join(d, "STDOUT.txt"), "wb").write(so); open(os.path.join(d, "STDERR.txt"), "wb").write(se)
    files = {}
    for dp, _, fs in os.walk(d):                                 # read back from disk after the task has exited
        for f in sorted(fs):
            p = os.path.join(dp, f); files[os.path.relpath(p, d)] = dict(sha256=sha(p), bytes=os.path.getsize(p))
    ok = (not timed_out) and code == task.get("expect_exit", 0)
    return dict(id=task["id"], argv=task["argv"], exit=code, expect_exit=task.get("expect_exit", 0), timed_out=timed_out,
                seconds=round(time.time() - t0, 2), ended_as_expected=ok, copied_in=sorted(before), files=files)

def main(a):
    if len(a) != 3: print(__doc__); return 2
    plan = json.load(open(a[1])); out = a[2]; os.makedirs(out)   # fresh directory only
    ids = [t["id"] for t in plan["tasks"]]
    if len(set(ids)) != len(ids): print("duplicate task id"); return 2
    with ThreadPoolExecutor(max_workers=int(plan.get("width", 3))) as ex:
        recs = list(ex.map(lambda t: run(t, os.path.dirname(os.path.abspath(a[1])), out), plan["tasks"]))
    rec = dict(tool="async_run.py", plan=os.path.basename(a[1]), plan_sha256=sha(a[1]), width=int(plan.get("width", 3)), tasks=recs,
               all_ended_as_expected=all(r["ended_as_expected"] for r in recs))
    with open(os.path.join(out, "ASYNC_RECORD.json"), "x") as f: json.dump(rec, f, indent=1)
    for r in recs:
        print(f'{r["id"]:<8} {"OK " if r["ended_as_expected"] else "NOT AS EXPECTED"} exit={r["exit"]} timeout={r["timed_out"]} {r["seconds"]}s files={len(r["files"])}')
    return 0 if rec["all_ended_as_expected"] else 6

if __name__ == "__main__": sys.exit(main(sys.argv))
