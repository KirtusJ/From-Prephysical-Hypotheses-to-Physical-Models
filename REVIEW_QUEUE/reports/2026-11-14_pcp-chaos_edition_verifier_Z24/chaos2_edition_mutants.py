"""CHAOS 2 (edition Z24 verifier). Scratch copies only. Seed 20261113.
Each mutant: applied to work/ (a copy of edition/), original verifier run inside the copy, patched verifier
run from outside on the copy, planted files saved to planted/<id>/MUTANT_<id>__<name>, work/ restored from
pristine/ and the restore verified by a digest of the whole tree. Predictions are in the table below, fixed
before the run."""
import hashlib, json, os, random, re, shutil, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__)); W = os.path.join(H, "work"); P = os.path.join(H, "pristine")
SEED = 20261113
sha = lambda b: hashlib.sha256(b).hexdigest()
def tree(root):
    d = {}
    for dp, _, fs in os.walk(root):
        for f in fs:
            p = os.path.join(dp, f); d[os.path.relpath(p, root)] = sha(open(p, "rb").read())
    return d
def tdig(d): return sha(json.dumps(sorted(d.items())).encode())
rd = lambda rel: open(os.path.join(W, rel), "rb").read()
def wr(rel, b):
    os.makedirs(os.path.dirname(os.path.join(W, rel)), exist_ok=True); open(os.path.join(W, rel), "wb").write(b)
def man(fn):
    m = json.loads(rd("MANIFEST.json")); fn(m); wr("MANIFEST.json", json.dumps(m, indent=1).encode())
def redig(*rels):
    def f(m):
        for rel in rels: b = rd(rel); m["files"][rel] = dict(m["files"].get(rel, {}), sha256=sha(b), size=len(b))
    man(f)
def sub(rel, a, b, cons=True, n=1):
    t = rd(rel); a, b = a.encode(), b.encode(); assert t.count(a) == n, (rel, a, t.count(a)); wr(rel, t.replace(a, b))
    if cons: redig(rel)
def find(name):
    return sorted(r for r in json.loads(rd("MANIFEST.json"))["files"] if r.endswith("/" + name))[0]
REG = "REVIEW_RECORDS/Director_Z/Session_4/register/register.jsonl"
TR = "PROGRAM/registers/THEOREM_REGISTRY.csv"; PI = "PROGRAM/registers/PAPER_INDEX.csv"
RES = "COMPUTATION/Baseline_Additions/Monodromy_Index_Results.json"
ADD = "REVIEW_RECORDS/Director_Z/Session_4/ADDENDUM_EDITION_Z24.md"
def reglines(): return rd(REG).split(b"\n")
def tsdigit(line):
    m = re.search(rb'"ts":"(\d{4}-\d\d-\d\dT\d\d:\d\d:\d)(\d)Z"', line); d = (int(m.group(2)) + 1) % 10
    return line[:m.start(2)] + str(d).encode() + line[m.end(2):]
note = {}
def m01(r): wr("PAPERS/__pycache__/MUTANT_M01_stray_paper.tex", b"% MUTANT M01 stray paper\n")
def m02(r): sub("README.md", "theorem registry (413 rows)", "theorem registry (431 rows)")
def droprow(rid):
    ls = rd(TR).split(b"\n"); k = [i for i, l in enumerate(ls) if l.startswith(rid.encode() + b",")]; assert len(k) == 1
    del ls[k[0]]; wr(TR, b"\n".join(ls)); redig(TR)
def m03(r): droprow("G8-01-03")
def m04(r):
    def f(m):
        k = r.choice(sorted(m["files"])); m["files"][k]["size"] += 1; note["M04"] = "size +1 of " + k
    man(f)
def m05(r):
    ls = reglines(); k = r.randrange(1, 500); ls[k] = tsdigit(ls[k]); note["M05"] = "line seq %d ts last digit +1" % k
    wr(REG, b"\n".join(ls)); redig(REG)
def pirow(pid, fn):
    import csv, io
    rows = list(csv.reader(io.StringIO(rd(PI).decode(), newline=""))); h = rows[0]
    for row in rows[1:]:
        if row[0] == pid: fn(h, row)
    o = io.StringIO(newline=""); csv.writer(o, lineterminator="\n").writerows(rows); wr(PI, o.getvalue().encode()); redig(PI)
def m06(r):
    def f(h, row): i = h.index("pages"); note["M06"] = "G10 pages %s -> %d" % (row[i], int(row[i]) + 1); row[i] = str(int(row[i]) + 1)
    pirow("G10", f)
def m07(r):
    t = bytearray(rd(RES)); ds = [i for i, c in enumerate(t) if 48 <= c <= 57]; i = r.choice(ds); o = t[i]
    t[i] = 48 + (o - 48 + 1) % 10; note["M07"] = "byte %d: %s -> %s" % (i, chr(o), chr(t[i])); wr(RES, bytes(t)); redig(RES)
def m08(r): sub(TR, "B1-05-05,B1,5,Scale POVM,Corollary,5,,PROOF_NOT_ADJACENT", "B1-05-05,B1,5,Scale POVM,Corollary,5,,PROOF_IN_MANUSCRIPT")
def m09(r): sub(ADD, "18 caught, 16 survived", "19 caught, 16 survived")
def m10(r):
    def f(m):
        s = m["predecessor_manifest_sha256"]; i = r.randrange(64); c = "0123456789abcdef"[(int(s[i], 16) + 1) % 16]
        m["predecessor_manifest_sha256"] = s[:i] + c + s[i + 1:]; note["M10"] = "hex digit %d: %s -> %s" % (i, s[i], c)
    man(f)
def m11(r):
    sub("verify_baseline.py", "\nif bad:\n", "\nif bad and False:  # MUTANT M11\n", cons=False)
    sub("README.md", "theorem registry (413 rows)", "theorem registry (431 rows)", cons=False)
def m12(r):
    ls = reglines(); k = max(i for i, l in enumerate(ls) if l); ls[k] = tsdigit(ls[k]); wr(REG, b"\n".join(ls)); redig(REG)
def prog(name, a, b, tag):
    rel = find(name); t = rd(rel).decode(); assert t.count(a) == 1, (name, a, t.count(a))
    wr(rel, ("# MUTANT %s\n" % tag + t.replace(a, b)).encode()); redig(rel)
def m13(r): prog("verify_periodic.py", "if len(found) == r and n >= 2 * r + 4: break", "if len(found) >= 1: break", "M13 walk stops at the first class found")  # yesterday's site 'if n == 400: break' is no longer in the program
def m14(r): prog("verify_periodic.py", 'P["P3"] = dim == len(vals)', 'P["P3"] = dim <= len(vals)', "M14 predicate == -> <=")
def m15(r): prog("verify_return_weight.py", "for t in range(1, T + 1):", "for t in range(1, T):", "M15 loop one short")
def m16(r):
    rel = find("RootsSum.lean"); t = rd(rel).decode(); a = "theorem c0_eq_zero_of_forall_roots (k : ℕ) (hk : 2 ≤ k)"
    assert t.count(a) == 1; wr(rel, ("-- MUTANT M16 hypothesis hk deleted\n" + t.replace(a, "theorem c0_eq_zero_of_forall_roots (k : ℕ)")).encode()); redig(rel)
def m17(r):
    ls = [l for l in reglines() if l]; wr(REG, b"\n".join(ls[:-3]) + b"\n"); redig(REG)
def m18(r):
    ls = [l for l in reglines() if l]; wr(REG, b"\n".join(ls[1:]) + b"\n"); redig(REG)
def m19(r):
    ls = [l for l in reglines() if l]; k = r.randrange(1, 500); ls[k] = tsdigit(ls[k]); note["M19"] = "line seq %d altered, later prev fields recomputed" % k
    for i in range(k + 1, len(ls)):
        ls[i] = re.sub(rb'"prev":"[0-9a-f]{64}"', b'"prev":"' + sha(ls[i - 1]).encode() + b'"', ls[i], count=1)
    wr(REG, b"\n".join(ls) + b"\n"); redig(REG)
def m20(r): wr(REG, rd(REG).replace(b"\n", b"\r\n")); redig(REG)
def m21(r): wr(TR, rd(TR).replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")); redig(TR)
def m22(r): t = rd(RES); wr(RES, t[:len(t) // 2]); redig(RES)
def m23(r):
    new = RES.replace("Results.json", "Results_MUTANT_M23.json"); os.rename(os.path.join(W, RES), os.path.join(W, new))
    def f(m): m["files"][new] = m["files"].pop(RES)
    man(f)
def m24(r):
    rel = "REVIEW_RECORDS/Director_Z/Session_4/pcp_workers/chaos/2026-11-13/FINDINGS.md"
    os.makedirs(os.path.join(H, "planted", "M24"), exist_ok=True)
    shutil.move(os.path.join(W, rel), os.path.join(H, "planted", "M24", "MUTANT_M24__removed_FINDINGS.md"))
    man(lambda m: m["files"].pop(rel))
def m25(r): wr("COMPUTATION/MUTANT_M25_stray_result.json", b'{"MUTANT": "M25", "all_pass": true}\n'); redig("COMPUTATION/MUTANT_M25_stray_result.json")
def m26(r):
    def f(h, row): row[h.index("kind")] = "planned"
    pirow("G10", f)
def m27(r):
    droprow("G8-01-03")
    def f(h, row): i = h.index("statements"); row[i] = str(int(row[i]) - 1)
    pirow("G8", f); sub("README.md", "theorem registry (413 rows)", "theorem registry (412 rows)")
def m28(r): sub("README.md", "theorem registry (413 rows)", "theorem registry of 431 rows")
def m29(r):
    import csv, io
    rows = list(csv.reader(io.StringIO(rd("PROGRAM/registers/COMPONENT_CROSSWALK.csv").decode(), newline=""))); h = rows[0]; i = h.index("baseline_sha256"); k = h.index("kind")
    c = [x for x in rows[1:] if x[k] != "legacy" and x[i]]; x = r.choice(c); x[i] = x[i][:-1] + ("0" if x[i][-1] != "0" else "1")
    o = io.StringIO(newline=""); csv.writer(o, lineterminator="\n").writerows(rows); wr("PROGRAM/registers/COMPONENT_CROSSWALK.csv", o.getvalue().encode()); redig("PROGRAM/registers/COMPONENT_CROSSWALK.csv")
def m30(r):
    t = bytearray(rd(RES)); ds = [i for i, c in enumerate(t) if 48 <= c <= 57]; i = r.choice(ds); t[i] = 48 + (t[i] - 47) % 10; wr(RES, bytes(t))
def m31(r): wr("PAPERS/__pycache__/MUTANT_M31_stray_paper.pyc", b"% MUTANT M31 a .tex text under a .pyc name\n")
def m32(r):
    ls = reglines(); k = r.randrange(1, 500); note["M32"] = "line seq %d removed" % k; del ls[k]; wr(REG, b"\n".join(ls)); redig(REG)
# id, function, kind of error, check that ought to catch, prediction, true statement made false?, equivalent-if-pass
M = [
 ("M01", m01, "added file under a __pycache__ directory (old E06)", "verifier: unlisted file (new check)", "CAUGHT", "record altered", 0),
 ("M02", m02, "README registry count 413 -> 431, manifest consistent (old E14)", "verifier: README count (new check)", "CAUGHT", "yes", 0),
 ("M03", m03, "registry row G8-01-03 removed, manifest consistent (old E16)", "verifier: PAPER_INDEX statements and README count (new checks)", "CAUGHT", "yes", 0),
 ("M04", m04, "a size in the manifest +1 (old E19)", "verifier: size (new check)", "CAUGHT", "yes", 0),
 ("M05", m05, "register copy, a middle line altered, manifest consistent (old E20)", "verifier: register hash chain (new check)", "CAUGHT", "yes", 0),
 ("M06", m06, "PAPER_INDEX pages of G10 +1, manifest consistent (old E21)", "verifier: PDF page count (new check; needs PyMuPDF, absent here)", "SURVIVED here (check skipped)", "yes", 0),
 ("M07", m07, "digit in a result file, manifest consistent (remaining kind 1, old E13)", "rerun and byte comparison; not the verifier", "SURVIVED", "yes", 0),
 ("M08", m08, "registry status word, manifest consistent (remaining kind 2, old E15)", "reviewer comparing row and paper", "SURVIVED", "yes", 0),
 ("M09", m09, "count in the addendum's summary sentence (remaining kind 3, old E17)", "summary review", "SURVIVED", "yes", 0),
 ("M10", m10, "predecessor digest in the manifest (remaining kind 4, old E18)", "comparison with the predecessor manifest in git", "SURVIVED", "yes", 0),
 ("M11", m11, "verifier disabled, with README count wrong, manifest not updated (remaining kind 5, old E22)", "a trusted copy of the verifier run from outside", "SURVIVED", "yes", 0),
 ("M12", m12, "last line of the register copy altered, manifest consistent (remaining kind 6, old E23)", "comparison with .pcp/register.jsonl", "SURVIVED", "yes", 0),
 ("M13", m13, "program: walk loop of verify_periodic.py stops at the first class found (remaining kind 7; old P5 site no longer exists)", "source digest tied to the result; not the verifier", "SURVIVED", "yes (docstring says 400)", 0),
 ("M14", m14, "program: predicate == -> <= in verify_periodic.py (remaining kind 8, old P6)", "source digest tied to the result; not the verifier", "SURVIVED", "yes (predicate weaker than stated)", 0),
 ("M15", m15, "program: loop one short in verify_return_weight.py (remaining kind 9; old P3's program is not in the edition under its name, old P7 used)", "rerun and byte comparison", "SURVIVED the verifier", "yes", 0),
 ("M16", m16, "Lean: hypothesis deleted from a theorem in RootsSum.lean under the same name (remaining kind 10, as old L1/L3)", "Lean build; not the verifier", "SURVIVED the verifier", "yes", 0),
 ("M17", m17, "register copy truncated: last 3 lines dropped, manifest consistent", "comparison with .pcp/register.jsonl", "SURVIVED", "record altered", 0),
 ("M18", m18, "register copy: first line dropped, manifest consistent", "a genesis/sequence test", "SURVIVED", "record altered", 0),
 ("M19", m19, "register copy: a middle line altered and the chain recomputed after it, manifest consistent", "comparison with .pcp/register.jsonl", "SURVIVED", "yes", 0),
 ("M20", m20, "register copy converted to CRLF, manifest consistent", "verifier: hash chain", "CAUGHT", "record altered", 0),
 ("M21", m21, "THEOREM_REGISTRY.csv converted to CRLF, manifest consistent", "none needed", "EQUIVALENT", "no", 1),
 ("M22", m22, "result file truncated to half (no longer JSON), manifest consistent", "a parse of every listed .json", "SURVIVED", "record altered", 0),
 ("M23", m23, "result file renamed, manifest key renamed with it", "comparison of the file list with the predecessor and the change list", "SURVIVED", "record altered", 0),
 ("M24", m24, "file removed together with its manifest entry", "comparison of the file list with the predecessor and the change list", "SURVIVED", "record altered", 0),
 ("M25", m25, "file added together with a manifest entry", "comparison of the file list with the predecessor and the change list", "SURVIVED", "record altered", 0),
 ("M26", m26, "PAPER_INDEX: kind of G10 set to 'planned' (switches off its statement and page tests)", "a test that planned papers have no registry rows", "SURVIVED", "yes", 0),
 ("M27", m27, "registry row removed and PAPER_INDEX and README counts lowered to agree", "reviewer comparing registry with the paper", "SURVIVED", "yes", 0),
 ("M28", m28, "README count wrong and the sentence reworded so the pattern does not match", "a test that the pattern matches at least once", "SURVIVED", "yes", 0),
 ("M29", m29, "crosswalk baseline digest, one hex digit, manifest consistent", "verifier: crosswalk digest (old check)", "CAUGHT", "yes", 0),
 ("M30", m30, "digit in a result file, manifest not updated", "verifier: manifest digest (old check)", "CAUGHT", "yes", 0),
 ("M31", m31, "added text file named *.pyc under a __pycache__ directory", "a test of the .pyc magic bytes", "SURVIVED", "record altered", 0),
 ("M32", m32, "register copy: a middle line removed, manifest consistent", "verifier: hash chain", "CAUGHT", "record altered", 0),
]
if __name__ == "__main__":
    base = tree(P); bd = tdig(base); assert tdig(tree(W)) == bd
    env = dict(os.environ, FPHPM_LIVE_REGISTER=os.path.join(H, "reference_live_register_COPY.jsonl"), FPHPM_PREDECESSOR_MANIFEST=os.path.join(H, "predecessor_MANIFEST_Z23.json"))
    out = []; only = sys.argv[1:]
    for i, fn, kind, check, pred, false_, eq in M:
        if only and i not in only: continue
        fn(random.Random("%d-%s" % (SEED, i)))
        cur = tree(W); os.makedirs(os.path.join(H, "planted", i), exist_ok=True); ch = []
        for rel in sorted(set(cur) | set(base)):
            if cur.get(rel) != base.get(rel):
                ch.append(rel)
                if rel in cur:
                    b = os.path.basename(rel); shutil.copy(os.path.join(W, rel), os.path.join(H, "planted", i, b if "MUTANT" in b else "MUTANT_%s__%s" % (i, b)))
        a = subprocess.run([sys.executable, "-B", os.path.join(W, "verify_baseline.py")], capture_output=True, text=True)
        b = subprocess.run([sys.executable, "-B", os.path.join(H, "verify_baseline_PATCHED.py"), W], capture_output=True, text=True, env=env)
        ls = lambda x: [l.strip() for l in (x.stdout + x.stderr).strip().split("\n") if l.strip() and not l.startswith("notice") and "BASELINE_CHECK_FAIL" not in l]
        o = ("CAUGHT" if a.returncode else ("EQUIVALENT" if eq else "SURVIVED"))
        rec = dict(id=i, kind=kind, changed=ch, original_sha256={r_: base.get(r_, "(added file)") for r_ in ch}, note=note.get(i, ""), check=check, prediction=pred, made_false=false_,
                   exit=a.returncode, outcome=o, how=(ls(a)[-1][:160] if a.returncode and "Traceback" in a.stderr else (ls(a)[0][:160] if a.returncode else "")), crash="Traceback" in a.stderr,
                   patched_exit=b.returncode, patched_how=[l[:120] for l in ls(b)[:3]] if b.returncode else [], patched_crash="Traceback" in b.stderr)
        # restore: put pristine files back, move added files out (already copied to planted/)
        for rel in ch:
            if rel in base: os.makedirs(os.path.dirname(os.path.join(W, rel)), exist_ok=True); shutil.copy(os.path.join(P, rel), os.path.join(W, rel))
            else: os.replace(os.path.join(W, rel), os.path.join(H, "planted", i, "moved_out_" + (os.path.basename(rel) if "MUTANT" in rel else "MUTANT_" + os.path.basename(rel))))
        for dp, ds, fs in os.walk(W, topdown=False):
            if not ds and not fs: os.rmdir(dp)   # only empty directories that a mutant created
        rec["restored"] = tdig(tree(W)) == bd; assert rec["restored"], i
        out.append(rec); print(json.dumps({k: rec[k] for k in ("id", "exit", "outcome", "how", "patched_exit", "patched_how", "restored")})); sys.stdout.flush()
    json.dump(dict(seed=SEED, pristine_tree_digest=bd, mutants=out), open(os.path.join(H, "chaos2_result%s.json" % ("_" + "_".join(only) if only else "")), "x"), indent=1)
