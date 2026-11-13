#!/usr/bin/env python3
"""Local validation of the Director D release: payload digests, then an isolated rerun of the verification program."""
import hashlib, json, os, shutil, subprocess, sys, tempfile
ROOT = os.path.dirname(os.path.abspath(__file__))
man = json.load(open(os.path.join(ROOT, "RELEASE_MANIFEST.json")))
bad = []
for rel, meta in man["payloads"].items():
    p = os.path.join(ROOT, rel)
    if not os.path.exists(p): bad.append((rel, "missing")); continue
    h = hashlib.sha256(open(p, "rb").read()).hexdigest()
    if h != meta["sha256"] or os.path.getsize(p) != meta["size"]: bad.append((rel, "digest/size mismatch"))
if bad:
    print("DIRECTOR_D_RELEASE_FAIL", bad); sys.exit(1)
with tempfile.TemporaryDirectory() as td:
    shutil.copy(os.path.join(ROOT, "verification", "verify_transport_bridges.py"), td)
    r = subprocess.run([sys.executable, "-I", "-B", "verify_transport_bridges.py"], cwd=td, capture_output=True, text=True)
    if r.returncode != 0:
        print("DIRECTOR_D_RELEASE_FAIL verification program failed\n", r.stdout, r.stderr); sys.exit(1)
    fresh = json.load(open(os.path.join(td, "Transport_Bridge_Results.json")))
saved = json.load(open(os.path.join(ROOT, "verification", "Transport_Bridge_Results.json")))
def close(a, b):
    if isinstance(a, float) and isinstance(b, float): return abs(a - b) <= 1e-9 * max(1.0, abs(b))
    if isinstance(a, dict) and isinstance(b, dict): return a.keys() == b.keys() and all(close(a[k], b[k]) for k in a)
    if isinstance(a, list) and isinstance(b, list): return len(a) == len(b) and all(close(x, y) for x, y in zip(a, b))
    return a == b
if not close(fresh, saved):
    print("DIRECTOR_D_RELEASE_FAIL fresh results differ from saved results"); sys.exit(1)
print(f"DIRECTOR_D_RELEASE_PASS {len(man['payloads'])} payloads; fresh verification agrees with saved results; "
      "integrity and reproduction only, not authentication, peer review or physical evidence")
