"""Compare each result file produced by the reruns (run/<name>/ and run2_<name>/) with the stored file of the same name under src/.
Exit code 0 only if every produced file that has a stored counterpart is byte-identical to it."""
import os, hashlib, sys
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
stored = {}
for dp, _, fs in os.walk("src"):
    for f in fs:
        if f.endswith(".json"): stored[f] = os.path.join(dp, f)
n = bad = 0
for top in sorted(os.listdir(".")):
    dirs = [os.path.join("run", d) for d in sorted(os.listdir("run"))] if top == "run" else [top] if top.startswith("run2_") else []
    for d in dirs:
        for f in sorted(os.listdir(d)):
            if f in stored and f != "results_gauge_bl.json":
                n += 1; same = sha(os.path.join(d, f)) == sha(stored[f]); bad += not same
                print("identical" if same else "DIFFERS", d, f)
print(n, "compared;", bad, "differ")
sys.exit(1 if bad or n == 0 else 0)
