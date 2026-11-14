"""Builds verify_baseline_PATCHED.py from the pristine verifier (scratch only) and the patch file."""
import os, subprocess
H = os.path.dirname(os.path.abspath(__file__)); t = open(os.path.join(H, "pristine", "verify_baseline.py")).read()
def rep(a, b):
    global t; assert t.count(a) == 1, a; t = t.replace(a, b)
rep('ROOT = os.path.dirname(os.path.abspath(__file__))\n',
    'ROOT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))  # a trusted copy can be run from outside the tree\n')
rep('''not (os.path.basename(dp) == "__pycache__" and f.endswith(".pyc")): bad.append(("unlisted", rel))''',
    '''not (os.path.basename(dp) == "__pycache__" and f.endswith(".pyc") and open(os.path.join(dp, f), "rb").read(4)[2:] == b"\\r\\n"): bad.append(("unlisted", rel))''')
rep('''for n in re.findall(r"theorem registry \\((\\d+) rows\\)", open(os.path.join(ROOT, "README.md")).read()):
    if int(n) != len(registry): bad.append(("README registry count", n))
''', '''counts = re.findall(r"theorem registry \\((\\d+) rows\\)", open(os.path.join(ROOT, "README.md")).read())
if not counts: bad.append(("README registry count sentence not found", ""))
for n in counts:
    if int(n) != len(registry): bad.append(("README registry count", n))
for r in index:
    if r["kind"] == "planned" and any(q["paper"] == r["id"] for q in registry): bad.append(("planned paper has registry rows", r["id"]))
for rel in sorted(listed):
    if rel.endswith(".json") and "partial" not in os.path.basename(rel) and os.path.exists(os.path.join(ROOT, rel)):  # a kept crash output is named *partial*
        try: json.load(open(os.path.join(ROOT, rel), encoding="utf-8"))
        except ValueError: bad.append(("not JSON", rel))
import subprocess
pm = os.environ.get("FPHPM_PREDECESSOR_MANIFEST"); pred = []
if pm: pred = [hashlib.sha256(open(pm, "rb").read()).hexdigest()]
else:
    g = subprocess.run(["git", "-C", ROOT, "log", "--format=%H", "-n", "3", "--", "MANIFEST.json"], capture_output=True, text=True)
    for c in g.stdout.split() if g.returncode == 0 else []:
        s = subprocess.run(["git", "-C", ROOT, "show", c + ":./MANIFEST.json"], capture_output=True)
        if s.returncode == 0: pred.append(hashlib.sha256(s.stdout).hexdigest())
if not pred: print("notice: no predecessor manifest available (git history or FPHPM_PREDECESSOR_MANIFEST); predecessor digest not checked")
elif man.get("predecessor_manifest_sha256") not in pred: bad.append(("predecessor digest matches no earlier MANIFEST.json", man.get("predecessor_manifest_sha256")))
live = os.environ.get("FPHPM_LIVE_REGISTER") or os.path.join(ROOT, "..", ".pcp", "register.jsonl")
copy = os.path.join(ROOT, "REVIEW_RECORDS", "Director_Z", "Session_4", "register", "register.jsonl")
if not os.path.exists(live): print("notice: live register not found; register copy not compared")
elif not open(live, "rb").read().startswith(open(copy, "rb").read()): bad.append(("register copy is not an initial segment of the live register", ""))
''')
rep('''            if json.loads(ls[i + 1])["prev"] != hashlib.sha256(ls[i]).hexdigest(): bad.append(("register chain", os.path.relpath(dp, ROOT) + " seq %d" % i))
''', '''            if json.loads(ls[i + 1])["prev"] != hashlib.sha256(ls[i]).hexdigest(): bad.append(("register chain", os.path.relpath(dp, ROOT) + " seq %d" % i))
        if ls and (json.loads(ls[0])["prev"] != "0" * 64 or [json.loads(l)["seq"] for l in ls] != list(range(len(ls)))): bad.append(("register genesis or sequence", os.path.relpath(dp, ROOT)))
''')
rep('''    print("notice: PyMuPDF not installed; front-matter check skipped")
''', '''    print("notice: PyMuPDF not installed; front-matter check skipped")
    import shutil
    if shutil.which("pdfinfo"):
        for r in index:
            if r["kind"] == "planned": continue
            m = re.search(r"^Pages:\\s+(\\d+)", subprocess.run(["pdfinfo", os.path.join(ROOT, r["file"])], capture_output=True, text=True).stdout, re.M)
            if not m or int(m.group(1)) != int(r["pages"]): bad.append(("PAPER_INDEX pages differ from PDF (pdfinfo)", r["id"]))
    else: print("notice: pdfinfo not found either; PAGE COUNTS NOT CHECKED")
''')
open(os.path.join(H, "verify_baseline_PATCHED.py"), "w").write(t)
os.makedirs(os.path.join(H, "a", "edition"), exist_ok=True); os.makedirs(os.path.join(H, "b", "edition"), exist_ok=True)
open(os.path.join(H, "a", "edition", "verify_baseline.py"), "w").write(open(os.path.join(H, "pristine", "verify_baseline.py")).read())
open(os.path.join(H, "b", "edition", "verify_baseline.py"), "w").write(t)
d = subprocess.run(["diff", "-u", "a/edition/verify_baseline.py", "b/edition/verify_baseline.py"], cwd=H, capture_output=True, text=True).stdout
d = "diff --git a/edition/verify_baseline.py b/edition/verify_baseline.py\n" + "\n".join(l.split("\t")[0] if l.startswith(("--- ", "+++ ")) else l for l in d.split("\n"))
open(os.path.join(H, "verify_baseline_z24_chaos2.patch"), "w").write(d)
