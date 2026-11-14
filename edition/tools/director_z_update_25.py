#!/usr/bin/env python3
"""Apply the twenty-first addendum of the fourth Director Z session (14 November 2026) to a copy of edition Z24, giving edition Z25:
paper G10 revised (Lemmas 5.30, 5.31, Theorem 5.32: consistency on position product events), one Lean file, review records, register amendments.
Arguments: build directory (g10, mathlib, rec), copy of edition Z24, optional directory holding the session register (.pcp).
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
OLD, NEW = "FPHPM-BASELINE-2026-11-14-Z24", "FPHPM-BASELINE-2026-11-14-Z25"
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

for f in sorted(os.listdir(os.path.join(SRC, "mathlib"))): put(os.path.join(SRC, "mathlib", f), "COMPUTATION/Lean/Mathlib/" + f, "Lean 4 lemma used in Theorem 5.32(i) and its converse")
edit("COMPUTATION/Lean/README.md", [("holds nineteen files for Lean 4.12.0 with Mathlib v4.12.0", "holds twenty files for Lean 4.12.0 with Mathlib v4.12.0 (and the compiler output of the newest)")], "one Mathlib file added")
rr = os.path.join(OUT, "COMPUTATION", "RERUN_RECORD_2026-11-12.csv")
with open(rr, newline="") as f: rows = list(csv.DictReader(f))
rows += [dict(program="COMPUTATION/Lean/Mathlib/ProductEvents.lean", status="RAN_OK", stored_output_compared="not applicable", stdout_equals_stored="exit code 0; axioms propext, Classical.choice, Quot.sound", note="rerun by the director for edition Z25")]
wcsv(rr, rows); changes.append(("changed", "COMPUTATION/RERUN_RECORD_2026-11-12.csv", "one row appended"))


rr = os.path.join(OUT, "COMPUTATION", "RERUN_RECORD_2026-11-12.csv")
with open(rr, newline="") as f: rows = list(csv.DictReader(f))
reg = rd("THEOREM_REGISTRY.csv")
NEWST = [("G10-01-33", "Lemma", "5.30", "Preparation (Director G; cited, not proved in the paper): on the signed line and on signed rings with N/gcd(N,2) at least 11, for every site and every pair of multisets of signed walks some position product event has exactly these on the two rails of the site"),
         ("G10-01-34", "Lemma", "5.31", "If a rule additive over end vertices is consistent with factor k on position product events and such an event has U and V on the two rails of a site, then F(U+V) at the right daughter plus F(U+JV) at the left daughter equals k F(U) + k F(V)"),
         ("G10-01-35", "Theorem", "5.32", "Given the preparation, a rule additive over end vertices with a function of the numbers of walks of either gain, consistent with factor two on position product events, is a(count) + c(square); site-independence follows on rings and for functions bounded below on the line; for non-negative rules the factor two follows on rings or for site-independent functions; conversely such rules are consistent on all events")]
RENAME = {}
for r in reg:
    if r["id"] in RENAME: r["name"] = RENAME[r["id"]]


labels = [f"{r['kind']} {r['number']}" for r in reg if r["paper"] == "G10"] + [f"{k} {n}" for _, k, n, _ in NEWST]
n10, pg = pages_of(PDF10, labels)
for r in reg:
    if r["paper"] == "G10": r["paper_file_page"] = r["part_page"] = str(pg[f"{r['kind']} {r['number']}"])
for i_, k, num, name in NEWST:
    reg.append(dict(id=i_, paper="G10", part="1", part_title=T10, kind=k, number=num, name=name, status="PROOF_IN_MANUSCRIPT", paper_file_page=str(pg[f"{k} {num}"]), part_page=str(pg[f"{k} {num}"]), legacy_locator=""))
wcsv("THEOREM_REGISTRY.csv", reg); changes.append(("changed", "PROGRAM/registers/THEOREM_REGISTRY.csv", "G10 pages updated; rows G10-01-33 to G10-01-35 added"))
old_statements = [r["statements"] for r in rd("PAPER_INDEX.csv") if r["id"] == "G10"][0]
index = rd("PAPER_INDEX.csv")
for r in index:
    if r["id"] == "G10": r.update(pages=str(n10), statements="35")
wcsv("PAPER_INDEX.csv", index); changes.append(("changed", "PROGRAM/registers/PAPER_INDEX.csv", "paper G10 revised"))
cross = rd("COMPONENT_CROSSWALK.csv")
for c in cross:
    if c["paper"] == "G10": c.update(baseline_sha256=sha(os.path.join(OUT, PART10)), pages=str(n10), change="first issued with edition Z4; revised in editions Z5 to Z25")
wcsv("COMPONENT_CROSSWALK.csv", cross); changes.append(("changed", "PROGRAM/registers/COMPONENT_CROSSWALK.csv", "G10 digest"))
ready = rd("READINESS.csv")
for r in ready:
    if r["paper"] == "G10": r.update(pages=str(n10), labelled_statements="35", gaps=r["gaps"] + " Edition Z25: Lemmas 5.30 (cited to Director G), 5.31 and Theorem 5.32 added: consistency asked only on position product events gives count plus square on the signed line and on rings where the preparation holds; proof by a sub-agent read by the author, two challengers, a micro-review, Lean for the algebra; rests on the cited preparation lemma.")
wcsv("READINESS.csv", ready); changes.append(("changed", "PROGRAM/registers/READINESS.csv", "paper G10 revised"))
ops = rd("OPEN_PROBLEMS.csv")
AM = {"OP-19": " Edition Z25: on the signed line and on rings where Director G's preparation holds, the choice between first and second order is the same when consistency is asked only on events selected by position masks (G10-01-35): count plus square, with the count excluded by one frequency fact as before.",
      "OP-30": " Edition Z25: the demand of consistency on every event is removed on the signed line and rings (G10-01-33 to G10-01-35). Open: the same for other carriers and for gains of higher order; a proof of the preparation that is machine-checked beyond one corridor; rings with N/gcd(N,2) below 11."}
for r in ops:
    if r["id"] in AM: r["statement"] += AM[r["id"]]
wcsv("OPEN_PROBLEMS.csv", ops); changes.append(("changed", "PROGRAM/registers/OPEN_PROBLEMS.csv", "OP-19 and OP-30 amended"))
bp = os.path.join(REG, "BRIDGE_CANDIDATE_REGISTER.json"); br = json.load(open(bp))
br["retained_outliers"]["solution_dimension_at_box_size_one_on_the_line_before_follow_up"] = 6
json.dump(br, open(bp, "w"), indent=1, ensure_ascii=False); changes.append(("changed", "PROGRAM/registers/BRIDGE_CANDIDATE_REGISTER.json", "one retained value added"))
gp = os.path.join(REG, "ONTOLOGY_GATE_MAP.json"); gm = json.load(open(gp)); gm["edition"] = NEW
for g in gm["gates"]:
    if g["id"] == "P5": g["evidence"] += " Edition Z25: consistency need only be asked on events selected by position masks, on the signed line and on rings where the preparation holds (G10-01-35, with Director G); the form of the rule (additive over end vertices, a function of the numbers of walks of either gain, independent of the length) and the absence of the count remain premises."
json.dump(gm, open(gp, "w"), indent=1, ensure_ascii=False); changes.append(("changed", "PROGRAM/registers/ONTOLOGY_GATE_MAP.json", "evidence of P5 amended; no state changed"))
dp = os.path.join(OUT, "PROGRAM", "figures", "Gate_Map_2026-11-13.dot"); dot = open(dp).read(); assert "edition Z24, 14 November 2026" in dot
open(dp, "w").write(dot.replace("edition Z24, 14 November 2026", "edition Z25, 14 November 2026").replace("Editions Z4 to Z24 change evidence", "Editions Z4 to Z25 change evidence")); changes.append(("changed", "PROGRAM/figures/Gate_Map_2026-11-13.dot", "edition label"))
subprocess.run(["dot", "-Tpdf", dp, "-o", dp[:-4] + ".pdf"], check=True); changes.append(("changed", "PROGRAM/figures/Gate_Map_2026-11-13.pdf", "edition label"))
HDR = (OLD + ", 14 November 2026", NEW + ", 14 November 2026")
edit("CONSTRUCTED_TRIALS/README.md", [HDR], "edition identifier")
S4 = "REVIEW_RECORDS/Director_Z/Session_4/"
for dp_, _, fs_ in os.walk(os.path.join(SRC, "rec")):
    for f in sorted(fs_):
        rel_ = os.path.relpath(os.path.join(dp_, f), os.path.join(SRC, "rec")); put(os.path.join(dp_, f), S4 + rel_, "twenty-first addendum to the fourth-session record")
if PCP:
    put(os.path.join(PCP, "register.jsonl"), S4 + "register/register.jsonl", "register of the fourth session, extended by review Z25")
    nev = len(open(os.path.join(PCP, "register.jsonl")).read().strip().split("\n"))
    import re
    p4 = os.path.join(OUT, S4 + "README_SESSION_4.md"); t = open(p4).read(); m = re.search(r"The register: .*?present chain\)\.", t, re.S); assert m
    t = t.replace(m.group(0), "The register: %d events; head digest of the chain `%s`; SHA-256 of the file `%s` (edition Z25; earlier editions end at earlier events of the present chain)." % (nev, os.environ.get("PCP_HEAD", "see pcpos verify"), sha(os.path.join(PCP, "register.jsonl"))))
    a_ = "findings Z-128 to Z-132 |"; assert a_ in t
    t = t.replace(a_, a_ + "\n| `ADDENDUM_EDITION_Z25.md`, `NEW_Z_SCOPED_FINDINGS_SESSION_4_ADDENDUM_21.csv`, `challenger_13/`, `challenger_14/`, `micro/micro14/`, `builder_T/`, further files in `cross_review/` and `pcp_workers/` | the twenty-first addendum: Lemmas 5.30, 5.31 and Theorem 5.32 of paper G10 (consistency on position product events, with Director G's preparation), two challengers, a micro-review, the builder's proof, cross-reviews of three notes of Director G; findings Z-133 to Z-136 |").replace("`CHANGES_Z23_TO_Z24.md`", "`CHANGES_Z23_TO_Z24.md`, `CHANGES_Z24_TO_Z25.md`")
    open(p4, "w").write(t); changes.append(("changed", S4 + "README_SESSION_4.md", "register digests; twenty-first addendum listed"))
for rel in ("PROGRAM/CONTRIBUTIONS.md", "PROGRAM/PAPER_INDEX.md", "PROGRAM/STANDARDS.md", "PROGRAM/CHARTER.md", "REVIEW_RECORDS/README.md", "README.md", "LEGACY/README.md", "NEGATIVE_CONTROLS/README.md"):
    extra = []
    if rel == "PROGRAM/PAPER_INDEX.md": extra = [(f"| G10 | {T10} | article | {old_pages} | {old_statements} |", f"| G10 | {T10} | article | {n10} | 35 |")]
    if rel == "README.md": extra = [(f"({637 + old_pages} assembled pages;", f"({637 + n10} assembled pages;"), (f"theorem registry ({len(reg) - len(NEWST)} rows)", f"theorem registry ({len(reg)} rows)")]
    edit(rel, [HDR] + extra, "edition identifier" + ("; paper G10 revised" if extra else ""))
shutil.copy(os.path.abspath(__file__), os.path.join(OUT, "tools", "director_z_update_25.py")); changes.append(("added", "tools/director_z_update_25.py", "the program that applied these changes"))
changes.append(("added", S4 + "CHANGES_Z24_TO_Z25.md", "this list")); changes.append(("changed", "MANIFEST.json", "edition identifier, digests"))
with open(os.path.join(OUT, S4, "CHANGES_Z24_TO_Z25.md"), "w") as f:
    f.write("# Changes from edition Z24 to edition Z25\n\n14 November 2026. Every other file is byte-identical to edition Z24.\n\n| Change | File | Reason |\n|---|---|---|\n")
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
print("edition Z25:", len(files), "files;", len(reg), "registry rows;", n10, "pages in G10;", len(changes), "changes")






