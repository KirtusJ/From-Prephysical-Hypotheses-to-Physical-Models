#!/usr/bin/env python3
"""Chaos harness, step 2: run one program copy inside one layout folder; print which pcplib was imported;
rename the result file so nothing is overwritten.  usage: run_one.py <root> <2|3> <tag>"""
import os, sys, runpy, traceback, io, contextlib, json
root, which, tag = os.path.abspath(sys.argv[1]), sys.argv[2], sys.argv[3]
N = {"2": ("2026-11-13_pcp-challenger_G10_prop-abund_cor-abund", "challenge_prop_abund_cor_abund"),
     "3": ("2026-11-13_pcp-micro-review_G10_cor-composition_cor-return", "micro_cor_composition_cor_return")}[which]
d = os.path.join(root, "reports", N[0]); prog = os.path.join(d, N[1] + ".py"); out = os.path.join(d, N[1] + "_results.json")
assert not os.path.exists(out)
status = dict(root=root, program=which, exit="ok", error=None)
buf = io.StringIO()
try:
    with contextlib.redirect_stdout(buf): runpy.run_path(prog, run_name="__main__")
except SystemExit as e: status["exit"] = "sysexit"; status["error"] = str(e)
except BaseException as e: status["exit"] = "crash"; status["error"] = type(e).__name__ + ": " + str(e)[:200] + " | " + traceback.format_exc().strip().splitlines()[-3].strip()[:160]
import pcplib
status["pcplib_file"] = os.path.abspath(pcplib.__file__); status["pcplib_is_local"] = status["pcplib_file"] == os.path.join(root, "lib", "pcplib.py")
if os.path.exists(out):
    new = os.path.join(d, f"{N[1]}_results.{tag}.json"); os.rename(out, new); status["result"] = new
open(os.path.join(d, f"stdout.{tag}.txt"), "w").write(buf.getvalue())
json.dump(status, open(os.path.join(d, f"status.{tag}.json"), "w"), indent=1)
print(json.dumps(status))
