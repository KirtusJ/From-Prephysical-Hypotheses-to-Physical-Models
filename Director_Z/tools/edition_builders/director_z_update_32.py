#!/usr/bin/env python3
"""Apply the twenty-eighth addendum of Director Z (15 November 2026) to a copy of edition Z31, giving edition Z32:
paper G10 revised (total positivity of the winding at one site; products of multisets in two adjacent cosets; three classes
of winding on products; three groups on two levels for M at least 5), Lean files, programs, review records, register.
Arguments: build directory (g10, mathlib, prog, rec), copy of edition Z31, directory holding the session register (.pcp).
Rewrites MANIFEST.json last.  Requires PyMuPDF and Graphviz (dot)."""
import csv, hashlib, json, os, re, shutil, subprocess, sys
import pymupdf
SRC, OUT, PCP = sys.argv[1], sys.argv[2], sys.argv[3]
REG = os.path.join(OUT, "PROGRAM", "registers")
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
def rd(n):
    with open(os.path.join(REG, n), newline="") as f: return list(csv.DictReader(f))
def wcsv(n, rows):
    with open(os.path.join(REG, n), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
OLD, NEW = "FPHPM-BASELINE-2026-11-15-Z31", "FPHPM-BASELINE-2026-11-15-Z32"
changes = []
def put(src, rel, why):
    dst = os.path.join(OUT, rel); os.makedirs(os.path.dirname(dst), exist_ok=True)
    k = "changed" if os.path.exists(dst) else "added"; shutil.copy(src, dst); changes.append((k, rel, why))
def edit(rel, pairs, why):
    p = os.path.join(OUT, rel); s = open(p).read()
    for a, b in pairs:
        assert a in s, (rel, a[:70]); s = s.replace(a, b)
    open(p, "w").write(s); changes.append(("changed", rel, why))
man0 = json.load(open(os.path.join(OUT, "MANIFEST.json"))); assert man0["baseline"] == OLD, man0["baseline"]
predecessor_manifest = sha(os.path.join(OUT, "MANIFEST.json"))
T10 = "Histories as Events: the Order of the Pair Rule, First-Order Weights and Forces from Gains of Bounded Order"
P10 = [d for d in os.listdir(os.path.join(OUT, "PAPERS")) if d.startswith("G10_")][0]; PD = "PAPERS/" + P10
PDF10 = PD + "/" + P10 + ".pdf"; PART10 = PD + "/parts/01_G10_manuscript.pdf"
old_pages = pymupdf.open(os.path.join(OUT, PDF10)).page_count
for dst in (PDF10, PART10): put(os.path.join(SRC, "g10", "G10_manuscript.pdf"), dst, "paper G10, revised")
for f in ("G10_manuscript.tex", "body.tex"): put(os.path.join(SRC, "g10", f), PD + "/source/" + f, "paper G10, revised")
for f in sorted(os.listdir(os.path.join(SRC, "mathlib"))): put(os.path.join(SRC, "mathlib", f), "COMPUTATION/Lean/Mathlib/" + f, "Lean file (Mathlib), winding products")
PROG = os.path.join(SRC, "prog")
for dp, _, fs in os.walk(PROG):
    for f in sorted(fs):
        rel = os.path.relpath(os.path.join(dp, f), PROG); put(os.path.join(dp, f), "COMPUTATION/Baseline_Additions/Four_Gains/winding_products/" + rel, "programs and results of the twenty-eighth addendum")
def pages_of(pdf, labels):
    d = pymupdf.open(os.path.join(OUT, pdf)); out = {}
    for i in range(d.page_count):
        for blk in d[i].get_text("dict")["blocks"]:
            for ln in blk.get("lines", []):
                t = " ".join("".join(sp["text"] for sp in ln["spans"] if "Bold" in sp["font"]).split())
                for lab in labels:
                    if lab not in out and (t == lab or t.startswith(lab + " ") or t.startswith(lab + ".")): out[lab] = i + 1
    for lab in labels: assert lab in out, (pdf, lab)
    return d.page_count, out
reg = rd("THEOREM_REGISTRY.csv")
NEWST = [
 ("G10-01-64", "Theorem", "5.64", "Total positivity of the winding at one site: the counts of walks at the two rails of one site of a position product event on a ring (N at least 3), listed by winding, form a totally non-negative array; each minor counts families of vertex-disjoint paths"),
 ("G10-01-65", "Corollary", "5.65", "The generating polynomials of the winding counts on each rail are real-rooted with non-positive roots; W(Y) = v(Y^2) + Y u(Y^2) has no root in the open right half-plane (part (iii) quoted from Holtz and Tyaglov and computed)"),
 ("G10-01-66", "Lemma", "5.66", "An event after an event: products of multisets that occur alone on R occur, for four arc gains on rings with N at least 3"),
 ("G10-01-67", "Lemma", "5.67", "Two levels in the abstract: a T_delta-invariant function on multisets in two cosets satisfying the pair equation at the two families of pairs is the count plus a quadratic form in the two signed sums (r even), the count alone (r odd)"),
 ("G10-01-68", "Lemma", "5.68", "A symmetric polynomial that is a quadratic form in each of k vectors of R^2 is a unique quadratic form in the coefficients of the product of the k linear forms"),
 ("G10-01-69", "Theorem", "5.69", "Products of multisets in two adjacent cosets, three or more classes of winding, M at least 8 (at least 5 by Corollary 5.74): a consistent rule is alpha prod|P_i| plus a banded quadratic form in the level-resolved signed sums of the product"),
 ("G10-01-70", "Theorem", "5.70", "Three classes of winding: on every product of multisets in two adjacent cosets the rule is the count and the two squares determined on two adjacent cosets"),
 ("G10-01-71", "Corollary", "5.72", "One class of winding without the one-gain note, M at least 8: property P+ holds by the three-group preparation"),
 ("G10-01-72", "Proposition", "5.73", "Three groups on two levels for M at least 5: hand proof for M at least 6, finite table for M = 5"),
 ("G10-01-73", "Corollary", "5.74", "Theorems 5.61, 5.62, 5.69, 5.70 and Corollary 5.72 hold for M at least 5; one class of winding for M at least 5 without the one-gain note")]
labels = [f"{r['kind']} {r['number']}" for r in reg if r["paper"] == "G10"] + [f"{k} {n}" for _, k, n, _ in NEWST]
n10, pg = pages_of(PDF10, labels)
for r in reg:
    if r["paper"] == "G10": r["paper_file_page"] = r["part_page"] = str(pg[f"{r['kind']} {r['number']}"])
for i_, k, num, name in NEWST:
    reg.append(dict(id=i_, paper="G10", part="1", part_title=T10, kind=k, number=num, name=name, status="PROOF_IN_MANUSCRIPT", paper_file_page=str(pg[f"{k} {num}"]), part_page=str(pg[f"{k} {num}"]), legacy_locator=""))
wcsv("THEOREM_REGISTRY.csv", reg); changes.append(("changed", "PROGRAM/registers/THEOREM_REGISTRY.csv", "G10 pages updated; rows G10-01-64 to G10-01-73 added"))
old_statements = [r["statements"] for r in rd("PAPER_INDEX.csv") if r["id"] == "G10"][0]; assert old_statements == "63", old_statements
index = rd("PAPER_INDEX.csv")
for r in index:
    if r["id"] == "G10": r.update(pages=str(n10), statements="73")
wcsv("PAPER_INDEX.csv", index); changes.append(("changed", "PROGRAM/registers/PAPER_INDEX.csv", "paper G10 revised"))
cross = rd("COMPONENT_CROSSWALK.csv")
for c in cross:
    if c["paper"] == "G10": c.update(baseline_sha256=sha(os.path.join(OUT, PART10)), pages=str(n10), change="first issued with edition Z4; revised in editions Z5 to Z32")
wcsv("COMPONENT_CROSSWALK.csv", cross); changes.append(("changed", "PROGRAM/registers/COMPONENT_CROSSWALK.csv", "G10 digest"))
ready = rd("READINESS.csv")
for r in ready:
    if r["paper"] == "G10": r.update(pages=str(n10), labelled_statements="73", gaps=r["gaps"] + " Edition Z32: total positivity of the winding (necessary, not sufficient: three allowed profiles occur on no ring with M from 3 to 8, computed); three classes settled on products of two-coset multisets; three groups and every dependent result for M at least 5; open: multisets that are not products, four or more classes in the paper (four to six computed and checked in Lean), M = 3 and M = 4 for two classes.")
wcsv("READINESS.csv", ready); changes.append(("changed", "PROGRAM/registers/READINESS.csv", "paper G10 revised"))
ops = rd("OPEN_PROBLEMS.csv")
for r in ops:
    if r["id"] == "OP-30": r["statement"] += " Edition Z32: the bound M at least 8 is lowered to M at least 5 (G10-01-72, G10-01-73); for three classes the rule is fixed on all products of two-coset multisets (G10-01-70); open: multisets that are not products, and which profiles allowed by total positivity (G10-01-64) occur."
wcsv("OPEN_PROBLEMS.csv", ops); changes.append(("changed", "PROGRAM/registers/OPEN_PROBLEMS.csv", "OP-30 amended"))
gp = os.path.join(REG, "ONTOLOGY_GATE_MAP.json"); gm = json.load(open(gp)); gm["edition"] = NEW
for g in gm["gates"]:
    if g["id"] == "P5": g["evidence"] += " Edition Z32: three classes of winding fixed on products of two-coset multisets; preparations for M at least 5; no state changed."
json.dump(gm, open(gp, "w"), indent=1, ensure_ascii=False); changes.append(("changed", "PROGRAM/registers/ONTOLOGY_GATE_MAP.json", "evidence of P5 amended; no state changed"))
dp = os.path.join(OUT, "PROGRAM", "figures", "Gate_Map_2026-11-13.dot"); dot = open(dp).read(); assert "edition Z31, 15 November 2026" in dot
open(dp, "w").write(dot.replace("edition Z31, 15 November 2026", "edition Z32, 15 November 2026").replace("Editions Z4 to Z31 change evidence", "Editions Z4 to Z32 change evidence")); changes.append(("changed", "PROGRAM/figures/Gate_Map_2026-11-13.dot", "edition label"))
subprocess.run(["dot", "-Tpdf", dp, "-o", dp[:-4] + ".pdf"], check=True); changes.append(("changed", "PROGRAM/figures/Gate_Map_2026-11-13.pdf", "edition label"))
HDR = (OLD + ", 15 November 2026", NEW + ", 15 November 2026")
edit("CONSTRUCTED_TRIALS/README.md", [HDR], "edition identifier")
S4 = "REVIEW_RECORDS/Director_Z/Session_4/"
for dp_, _, fs_ in os.walk(os.path.join(SRC, "rec")):
    for f in sorted(fs_):
        rel_ = os.path.relpath(os.path.join(dp_, f), os.path.join(SRC, "rec")); put(os.path.join(dp_, f), S4 + "winding_products/" + rel_, "twenty-eighth addendum to the fourth-session record")
put(os.path.join(PCP, "register.jsonl"), S4 + "register/register.jsonl", "register of the fourth session, extended by review Z32")
nev = len(open(os.path.join(PCP, "register.jsonl")).read().strip().split("\n"))
p4 = os.path.join(OUT, S4 + "README_SESSION_4.md"); t = open(p4).read(); m = re.search(r"The register: .*?present chain\)\.", t, re.S); assert m
t = t.replace(m.group(0), "The register: %d events; head digest of the chain `%s`; SHA-256 of the file `%s` (edition Z32; earlier editions end at earlier events of the present chain)." % (nev, os.environ.get("PCP_HEAD", "see pcpos verify"), sha(os.path.join(PCP, "register.jsonl"))))
a_ = "`four_gains_winding/challenger_three/` |"; assert a_ in t
i_ = t.index(a_); j_ = t.index("\n", i_)
t = t[:j_] + "\n| `winding_products/` | the twenty-eighth addendum (edition Z32): total positivity of the winding, products of multisets, three classes on products, three groups for M at least 5; challengers', micro-review's and workers' reports with the director's rechecks |" + t[j_:]
open(p4, "w").write(t); changes.append(("changed", S4 + "README_SESSION_4.md", "register digests; twenty-eighth addendum listed"))
for rel in ("PROGRAM/CONTRIBUTIONS.md", "PROGRAM/PAPER_INDEX.md", "PROGRAM/STANDARDS.md", "PROGRAM/CHARTER.md", "REVIEW_RECORDS/README.md", "README.md", "LEGACY/README.md", "NEGATIVE_CONTROLS/README.md"):
    extra = []
    if rel == "PROGRAM/PAPER_INDEX.md": extra = [(f"| G10 | {T10} | article | {old_pages} | {old_statements} |", f"| G10 | {T10} | article | {n10} | 73 |")]
    if rel == "README.md": extra = [(f"({637 + old_pages} assembled pages;", f"({637 + n10} assembled pages;"), (f"theorem registry ({len(reg) - len(NEWST)} rows)", f"theorem registry ({len(reg)} rows)")]
    edit(rel, [HDR] + extra, "edition identifier" + ("; paper G10 revised" if extra else ""))
shutil.copy(os.path.abspath(__file__), os.path.join(OUT, "tools", "director_z_update_32.py")); changes.append(("added", "tools/director_z_update_32.py", "the program that applied these changes"))
changes.append(("added", S4 + "CHANGES_Z31_TO_Z32.md", "this list")); changes.append(("changed", "MANIFEST.json", "edition identifier, digests"))
with open(os.path.join(OUT, S4, "CHANGES_Z31_TO_Z32.md"), "w") as f:
    f.write("# Changes from edition Z31 to edition Z32\n\n15 November 2026. Predecessor manifest SHA-256 `%s`. Every other file is byte-identical to edition Z31.\n\n| Change | File | Reason |\n|---|---|---|\n" % predecessor_manifest)
    for c in changes: f.write(f"| {c[0]} | `{c[1]}` | {c[2]} |\n")
man = json.load(open(os.path.join(OUT, "MANIFEST.json")))
man["baseline"] = NEW; man["predecessor"] = OLD; man["predecessor_manifest_sha256"] = predecessor_manifest
files = {}
for dpth, _, fs in os.walk(OUT):
    for f in sorted(fs):
        rel = os.path.relpath(os.path.join(dpth, f), OUT)
        if rel == "MANIFEST.json" or "__pycache__" in rel: continue
        files[rel] = dict(sha256=sha(os.path.join(OUT, rel)), size=os.path.getsize(os.path.join(OUT, rel)))
man["files"] = dict(sorted(files.items()))
json.dump(man, open(os.path.join(OUT, "MANIFEST.json"), "w"), indent=1, ensure_ascii=False)
print("edition Z32:", len(files), "files;", len(reg), "registry rows;", n10, "pages in G10;", len(changes), "changes")
