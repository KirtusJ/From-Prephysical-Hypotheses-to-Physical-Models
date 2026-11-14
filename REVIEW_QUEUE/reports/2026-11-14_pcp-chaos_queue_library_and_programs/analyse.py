#!/usr/bin/env python3
"""Chaos harness, step 3: compare each mutant run with the baseline rerun.  Per program:
 CAUGHT-predicate: some predicate's `met` differs from the baseline, or the program crashed;
 values-only: all `met` equal but the result bytes differ (only a rerun-and-compare would notice);
 identical: result bytes equal to the baseline."""
import json, os, glob, hashlib
W = os.path.dirname(os.path.abspath(__file__))
N = {"2": ("2026-11-13_pcp-challenger_G10_prop-abund_cor-abund", "challenge_prop_abund_cor_abund"),
     "3": ("2026-11-13_pcp-micro-review_G10_cor-composition_cor-return", "micro_cor_composition_cor_return")}
def load(root, w):
    d = f"{root}/reports/{N[w][0]}"; st = f"{d}/status.RERUN.json"
    if not os.path.exists(st): return None
    s = json.load(open(st)); r = f"{d}/{N[w][1]}_results.RERUN.json"
    s["bytes"] = open(r, "rb").read() if os.path.exists(r) else None; s["res"] = json.loads(s["bytes"]) if s["bytes"] else None
    return s
truthy = lambda v: str(v) == "True"
base = {w: load(f"{W}/base", w) for w in "23"}
out = {}
for root in sorted(glob.glob(f"{W}/mutants/*")):
    mid = os.path.basename(root); out[mid] = {}
    for w in "23":
        s = load(root, w)
        if s is None: continue
        o = dict(pcplib_is_local=s["pcplib_is_local"])
        if s["exit"] != "ok": o["verdict"] = "CAUGHT-crash"; o["how"] = s["error"]
        else:
            bp, mp = base[w]["res"]["predicates"], s["res"]["predicates"]
            flips = [k for k in bp if truthy(bp[k]["met"]) != truthy(mp[k]["met"])]
            changed = [k for k in bp if json.dumps(bp[k], sort_keys=True) != json.dumps(mp[k], sort_keys=True)]
            if flips: o["verdict"] = "CAUGHT-predicate"; o["how"] = "met flipped: " + ", ".join(f"{k} {bp[k]['met']}->{mp[k]['met']}" for k in flips)
            elif s["bytes"] != base[w]["bytes"]: o["verdict"] = "values-only"; o["how"] = "no met flipped; values differ in: " + ", ".join(changed or ["carriers list"])
            else: o["verdict"] = "identical"; o["how"] = "result bytes identical to baseline"
            o["detail"] = {k: {a: b for a, b in mp[k].items() if a not in ("detail", "per_length", "length_2", "note")} for k in changed}
        out[mid][w] = o
for mid, w, pat in (("R01", "3", "STORED_MUTANT"), ("R02", "2", "STORED_MUTANT")):
    f = glob.glob(f"{W}/mutants/{mid}/reports/{N[w][0]}/*{pat}.json")[0]
    same = open(f, "rb").read() == base[w]["bytes"]
    out[mid][w] = dict(verdict="SURVIVED" if same else "CAUGHT-rerun-compare", how="stored file vs fresh rerun of the unmutated program: " + ("identical" if same else "bytes differ"))
json.dump(out, open(f"{W}/RESULTS.json", "w"), indent=1)
for mid, v in out.items():
    for w, o in v.items(): print(mid, "P" + w, o["verdict"], "|", o["how"][:330], "|", json.dumps(o.get("detail", {}))[:420] if o["verdict"] == "values-only" else "")
