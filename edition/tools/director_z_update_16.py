#!/usr/bin/env python3
"""Apply the nineteenth addendum of the fourth Director Z session (13 November 2026) to a copy of edition Z22, giving edition Z23:
paper G10 revised (Corollary 5.29: the return weight), one program, a challenger's program, cross-review addendum 10, register amendments.
Arguments: build directory (g10, comp_rec, rec), copy of edition Z22, optional directory holding the session register (.pcp).
Rewrites MANIFEST.json last.  Requires PyMuPDF and Graphviz (dot)."""
import csv, hashlib, json, os, shutil, subprocess, sys
import pymupdf
SRC, OUT = sys.argv[1], sys.argv[2]
PCP = sys.argv[3] if len(sys.argv) > 3 else None
REG = os.path.join(OUT, "PROGRAM", "registers")
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
def rd(n):
    with open(os.path.join(REG, n), newline="") as f: return list(csv.DictReader(f))
def wcsv(n, rows):
    with open(os.path.join(REG, n) if not os.path.isabs(n) else n, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
OLD, NEW = "FPHPM-BASELINE-2026-11-13-Z22", "FPHPM-BASELINE-2026-11-13-Z23"
changes = []
def put(src, rel, why):
    dst = os.path.join(OUT, rel); os.makedirs(os.path.dirname(dst), exist_ok=True)
    k = "changed" if os.path.exists(dst) else "added"; shutil.copy(src, dst); changes.append((k, rel, why))
def edit(rel, pairs, why):
    p = os.path.join(OUT, rel); s = open(p).read()
    for a, b in pairs:
        assert a in s, (rel, a[:70]); s = s.replace(a, b)
    open(p, "w").write(s); changes.append(("changed", rel, why))
predecessor_manifest = sha(os.path.join(OUT, "MANIFEST.json"))
T10 = "Histories as Events: the Order of the Pair Rule, First-Order Weights and Forces from Gains of Bounded Order"
P10 = [d for d in os.listdir(os.path.join(OUT, "PAPERS")) if d.startswith("G10_")][0]; PD = "PAPERS/" + P10
PDF10 = PD + "/" + P10 + ".pdf"; PART10 = PD + "/parts/01_G10_manuscript.pdf"
old_pages = pymupdf.open(os.path.join(OUT, PDF10)).page_count
put(os.path.join(SRC, "g10", "G10_manuscript.pdf"), PDF10, "paper G10, revised"); put(os.path.join(SRC, "g10", "G10_manuscript.pdf"), PART10, "paper G10, revised")
for f in ("G10_manuscript.tex", "body.tex"): put(os.path.join(SRC, "g10", f), PD + "/source/" + f, "paper G10, revised")
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
ba = "COMPUTATION/Baseline_Additions/"

for f in sorted(os.listdir(os.path.join(SRC, "comp_rec"))): put(os.path.join(SRC, "comp_rec", f), ba + "Vertex_Law/" + f, "computation cited by paper G10 (Corollary 5.29); written by the director")


rr = os.path.join(OUT, "COMPUTATION", "RERUN_RECORD_2026-11-12.csv")
with open(rr, newline="") as f: rows = list(csv.DictReader(f))
rows += [dict(program="Baseline_Additions/Vertex_Law: verify_return_weight.py", status="RAN_OK", stored_output_compared="yes", stdout_equals_stored="rerun in a fresh directory byte-identical; a first run crashed while writing its result and its partial file is kept", note="edition Z23; needs numpy")]
wcsv(rr, rows); changes.append(("changed", "COMPUTATION/RERUN_RECORD_2026-11-12.csv", "one row appended"))
reg = rd("THEOREM_REGISTRY.csv")
NEWST = [("G10-01-32", "Corollary", "5.29", "On a carrier of Theorem 5.26, for a normalized non-negative consistent rule with count coefficient a, the return weight is at most 1 - a(1 - 1/d) at every positive length and has limsup at least 1 - a; it has limsup one exactly when a = 0")]
RENAME = {}
for r in reg:
    if r["id"] in RENAME: r["name"] = RENAME[r["id"]]


labels = [f"{r['kind']} {r['number']}" for r in reg if r["paper"] == "G10"] + [f"{k} {n}" for _, k, n, _ in NEWST]
n10, pg = pages_of(PDF10, labels)
for r in reg:
    if r["paper"] == "G10": r["paper_file_page"] = r["part_page"] = str(pg[f"{r['kind']} {r['number']}"])
for i_, k, num, name in NEWST:
    reg.append(dict(id=i_, paper="G10", part="1", part_title=T10, kind=k, number=num, name=name, status="PROOF_IN_MANUSCRIPT", paper_file_page=str(pg[f"{k} {num}"]), part_page=str(pg[f"{k} {num}"]), legacy_locator=""))
wcsv("THEOREM_REGISTRY.csv", reg); changes.append(("changed", "PROGRAM/registers/THEOREM_REGISTRY.csv", "G10 pages updated; row G10-01-32 added"))
old_statements = [r["statements"] for r in rd("PAPER_INDEX.csv") if r["id"] == "G10"][0]
index = rd("PAPER_INDEX.csv")
for r in index:
    if r["id"] == "G10": r.update(pages=str(n10), statements="32")
wcsv("PAPER_INDEX.csv", index); changes.append(("changed", "PROGRAM/registers/PAPER_INDEX.csv", "paper G10 revised"))
cross = rd("COMPONENT_CROSSWALK.csv")
for c in cross:
    if c["paper"] == "G10": c.update(baseline_sha256=sha(os.path.join(OUT, PART10)), pages=str(n10), change="first issued with edition Z4; revised in editions Z5 to Z23")
wcsv("COMPONENT_CROSSWALK.csv", cross); changes.append(("changed", "PROGRAM/registers/COMPONENT_CROSSWALK.csv", "G10 digest"))
ready = rd("READINESS.csv")
for r in ready:
    if r["paper"] == "G10": r.update(pages=str(n10), labelled_statements="32", gaps=r["gaps"] + " Edition Z23: Corollary 5.29 added (the return weight: a requirement of near-return excludes the count); idea due to Director G for a staircase walk, general statement and proof by the author, examined by a challenger; the requirement itself is a premise.")
wcsv("READINESS.csv", ready); changes.append(("changed", "PROGRAM/registers/READINESS.csv", "paper G10 revised"))
ops = rd("OPEN_PROBLEMS.csv")
AM = {"OP-19": " Edition Z23: between the first-order rule (the count) and the second-order rules a requirement on returns decides: for a normalized non-negative consistent rule the return weight stays below 1 - a(1 - 1/d) at positive lengths, so near-return to the starting vertex forces the count coefficient a to zero (G10-01-32). The requirement is a premise; Director G argues it from a state space of finite affine dimension with a reversible step.",
      "OP-30": " Edition Z23: with near-return as a premise the count is excluded (G10-01-32), and with multiplicativity the rule is the squared norm for one class of characters (G10-01-31). Open: a derivation of near-return, or of reversibility of the complete system, from the carrier; the choice among the characters."}
for r in ops:
    if r["id"] in AM: r["statement"] += AM[r["id"]]
wcsv("OPEN_PROBLEMS.csv", ops); changes.append(("changed", "PROGRAM/registers/OPEN_PROBLEMS.csv", "OP-19 and OP-30 amended"))
bp = os.path.join(REG, "BRIDGE_CANDIDATE_REGISTER.json"); br = json.load(open(bp))
br["retained_outliers"]["coherent_return_on_ring_of_five_in_lengths_1000_to_2000"] = 0.955
json.dump(br, open(bp, "w"), indent=1, ensure_ascii=False); changes.append(("changed", "PROGRAM/registers/BRIDGE_CANDIDATE_REGISTER.json", "one retained value added"))
gp = os.path.join(REG, "ONTOLOGY_GATE_MAP.json"); gm = json.load(open(gp)); gm["edition"] = NEW
for g in gm["gates"]:
    if g["id"] == "P5": g["evidence"] += " Edition Z23: a requirement that the return weight come arbitrarily close to one excludes the count (G10-01-32); the requirement is a premise, argued by Director G from a finite-dimensional reversible state space and not derived in G10. With it and multiplicativity the rule is one character's squared norm; the character is not selected."
json.dump(gm, open(gp, "w"), indent=1, ensure_ascii=False); changes.append(("changed", "PROGRAM/registers/ONTOLOGY_GATE_MAP.json", "evidence of P5 amended; no state changed"))
dp = os.path.join(OUT, "PROGRAM", "figures", "Gate_Map_2026-11-13.dot"); dot = open(dp).read(); assert "edition Z22, 13 November 2026" in dot
open(dp, "w").write(dot.replace("edition Z22, 13 November 2026", "edition Z23, 13 November 2026").replace("Editions Z4 to Z22 change evidence", "Editions Z4 to Z23 change evidence")); changes.append(("changed", "PROGRAM/figures/Gate_Map_2026-11-13.dot", "edition label"))
subprocess.run(["dot", "-Tpdf", dp, "-o", dp[:-4] + ".pdf"], check=True); changes.append(("changed", "PROGRAM/figures/Gate_Map_2026-11-13.pdf", "edition label"))
HDR = (OLD + ", 13 November 2026", NEW + ", 13 November 2026")
edit("CONSTRUCTED_TRIALS/README.md", [HDR], "edition identifier")
S4 = "REVIEW_RECORDS/Director_Z/Session_4/"
for dp_, _, fs_ in os.walk(os.path.join(SRC, "rec")):
    for f in sorted(fs_):
        rel_ = os.path.relpath(os.path.join(dp_, f), os.path.join(SRC, "rec")); put(os.path.join(dp_, f), S4 + rel_, "nineteenth addendum to the fourth-session record")
if PCP:
    put(os.path.join(PCP, "register.jsonl"), S4 + "register/register.jsonl", "register of the fourth session, extended by review Z23")
    nev = len(open(os.path.join(PCP, "register.jsonl")).read().strip().split("\n"))
    import re
    p4 = os.path.join(OUT, S4 + "README_SESSION_4.md"); t = open(p4).read(); m = re.search(r"The register: .*?present chain\)\.", t, re.S); assert m
    t = t.replace(m.group(0), "The register: %d events; head digest of the chain `%s`; SHA-256 of the file `%s` (edition Z23; earlier editions end at earlier events of the present chain)." % (nev, os.environ.get("PCP_HEAD", "see pcpos verify"), sha(os.path.join(PCP, "register.jsonl"))))
    a_ = "findings Z-122 to Z-124 |"; assert a_ in t
    t = t.replace(a_, a_ + "\n| `ADDENDUM_EDITION_Z23.md`, `NEW_Z_SCOPED_FINDINGS_SESSION_4_ADDENDUM_19.csv`, `challenger_11/`, further files in `cross_review/` | the nineteenth addendum: Corollary 5.29 of paper G10 (the return weight) with a challenger's program, and the cross-review of Director G's note on return records (addendum 10); findings Z-125 to Z-127 |").replace("`CHANGES_Z20_TO_Z21.md`, `CHANGES_Z21_TO_Z22.md`", "`CHANGES_Z20_TO_Z21.md`, `CHANGES_Z21_TO_Z22.md`, `CHANGES_Z22_TO_Z23.md`")
    open(p4, "w").write(t); changes.append(("changed", S4 + "README_SESSION_4.md", "register digests; nineteenth addendum listed"))
for rel in ("PROGRAM/CONTRIBUTIONS.md", "PROGRAM/PAPER_INDEX.md", "PROGRAM/STANDARDS.md", "PROGRAM/CHARTER.md", "REVIEW_RECORDS/README.md", "README.md", "LEGACY/README.md", "NEGATIVE_CONTROLS/README.md"):
    extra = []
    if rel == "PROGRAM/PAPER_INDEX.md": extra = [(f"| G10 | {T10} | article | {old_pages} | {old_statements} |", f"| G10 | {T10} | article | {n10} | 32 |")]
    if rel == "README.md": extra = [(f"({637 + old_pages} assembled pages;", f"({637 + n10} assembled pages;"), (f"theorem registry ({len(reg) - len(NEWST)} rows)", f"theorem registry ({len(reg)} rows)")]
    edit(rel, [HDR] + extra, "edition identifier" + ("; paper G10 revised" if extra else ""))
shutil.copy(os.path.abspath(__file__), os.path.join(OUT, "tools", "director_z_update_16.py")); changes.append(("added", "tools/director_z_update_16.py", "the program that applied these changes"))
changes.append(("added", S4 + "CHANGES_Z22_TO_Z23.md", "this list")); changes.append(("changed", "MANIFEST.json", "edition identifier, digests"))
with open(os.path.join(OUT, S4, "CHANGES_Z22_TO_Z23.md"), "w") as f:
    f.write("# Changes from edition Z22 to edition Z23\n\n13 November 2026. Every other file is byte-identical to edition Z22.\n\n| Change | File | Reason |\n|---|---|---|\n")
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
print("edition Z23:", len(files), "files;", len(reg), "registry rows;", n10, "pages in G10;", len(changes), "changes")






