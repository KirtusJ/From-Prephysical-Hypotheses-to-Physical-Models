#!/usr/bin/env python3
"""Apply the sixteenth addendum of the fourth Director Z session (13 November 2026) to a copy of edition Z19, giving edition Z20:
paper G10 revised (Theorem 5.22, Corollary 5.23, Lemma 5.24: a function at each end vertex), one program, one Lean file, a challenger's and two micro-reviews' programs, cross-review addendum 8, the manifest of the root tidy-up, register amendments.
Arguments: build directory (g10, comp_vl, mathlib, rec), copy of edition Z19, optional directory holding the session register (.pcp).
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
OLD, NEW = "FPHPM-BASELINE-2026-11-13-Z19", "FPHPM-BASELINE-2026-11-13-Z20"
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
for f in sorted(os.listdir(os.path.join(SRC, "comp_vl"))): put(os.path.join(SRC, "comp_vl", f), ba + "Vertex_Law/" + f, "computation cited by paper G10 (Theorem 5.22); written by a sub-agent")
for f in sorted(os.listdir(os.path.join(SRC, "mathlib"))): put(os.path.join(SRC, "mathlib", f), "COMPUTATION/Lean/Mathlib/" + f, "Lean 4 lemmas used in Theorem 5.22 and Lemma 5.24")

edit("COMPUTATION/Lean/README.md", [("holds sixteen files for Lean 4.12.0 with Mathlib v4.12.0", "holds seventeen files for Lean 4.12.0 with Mathlib v4.12.0"), ("the linear-algebra step of Remark 5.21 (PreimageSpan),", "the linear-algebra step of Remark 5.21 (PreimageSpan), three steps of Theorem 5.22 and Lemma 5.24 (VertexLaw),"), ("and the five added in edition Z19 at its issue.", "and the five added in edition Z19 and the one added in edition Z20 at their issue.")], "one Mathlib file added")
rr = os.path.join(OUT, "COMPUTATION", "RERUN_RECORD_2026-11-12.csv")
with open(rr, newline="") as f: rows = list(csv.DictReader(f))
rows += [dict(program="Baseline_Additions/Vertex_Law: verify_vertexlaw.py", status="RAN_OK", stored_output_compared="yes", stdout_equals_stored="rerun in a fresh directory byte-identical, by the sub-agent; a first result file is kept as superseded", note="edition Z20; needs python-flint"), dict(program="COMPUTATION/Lean/Mathlib/VertexLaw.lean", status="RAN_OK", stored_output_compared="not applicable", stdout_equals_stored="exit code 0; axioms propext, Classical.choice, Quot.sound", note="rerun by the director for edition Z20")]
wcsv(rr, rows); changes.append(("changed", "COMPUTATION/RERUN_RECORD_2026-11-12.csv", "two rows appended"))
reg = rd("THEOREM_REGISTRY.csv")
NEWST = [("G10-01-25", "Theorem", "5.22", "On a finite gain digraph with gains in a finite abelian group, at most one arc per ordered pair and exactly d >= 2 outgoing arcs at every vertex, a family of functions on multisets, one for each vertex, vanishing on the empty multiset, satisfies the global law exactly when each is an additive part plus a quadratic form and both families satisfy the law"), ("G10-01-26", "Corollary", "5.23", "On such a carrier with every gain reaching every vertex in abundance the consistent rules with a function at each end vertex are those of the theorem; if the carrier is strongly connected they are the combinations of the count and of the squares |sigma_psi|^2 over the characters with A^(psi)*A^(psi) = d, the same at every vertex"), ("G10-01-27", "Lemma", "5.24", "For an eigenvector of the step for the eigenvalue d the set of maximal modulus is closed under successors; every non-empty closed set contains a terminal class and a vertex with two predecessors")]
RENAME = {}
for r in reg:
    if r["id"] in RENAME: r["name"] = RENAME[r["id"]]


labels = [f"{r['kind']} {r['number']}" for r in reg if r["paper"] == "G10"] + [f"{k} {n}" for _, k, n, _ in NEWST]
n10, pg = pages_of(PDF10, labels)
for r in reg:
    if r["paper"] == "G10": r["paper_file_page"] = r["part_page"] = str(pg[f"{r['kind']} {r['number']}"])
for i_, k, num, name in NEWST:
    reg.append(dict(id=i_, paper="G10", part="1", part_title=T10, kind=k, number=num, name=name, status="PROOF_IN_MANUSCRIPT", paper_file_page=str(pg[f"{k} {num}"]), part_page=str(pg[f"{k} {num}"]), legacy_locator=""))
wcsv("THEOREM_REGISTRY.csv", reg); changes.append(("changed", "PROGRAM/registers/THEOREM_REGISTRY.csv", "G10 pages updated; rows G10-01-25 to G10-01-27 added"))
old_statements = [r["statements"] for r in rd("PAPER_INDEX.csv") if r["id"] == "G10"][0]
index = rd("PAPER_INDEX.csv")
for r in index:
    if r["id"] == "G10": r.update(pages=str(n10), statements="27")
wcsv("PAPER_INDEX.csv", index); changes.append(("changed", "PROGRAM/registers/PAPER_INDEX.csv", "paper G10 revised"))
cross = rd("COMPONENT_CROSSWALK.csv")
for c in cross:
    if c["paper"] == "G10": c.update(baseline_sha256=sha(os.path.join(OUT, PART10)), pages=str(n10), change="first issued with edition Z4; revised in editions Z5 to Z20")
wcsv("COMPONENT_CROSSWALK.csv", cross); changes.append(("changed", "PROGRAM/registers/COMPONENT_CROSSWALK.csv", "G10 digest"))
ready = rd("READINESS.csv")
for r in ready:
    if r["paper"] == "G10": r.update(pages=str(n10), labelled_statements="27", gaps=r["gaps"] + " Edition Z20: Theorem 5.22, Corollary 5.23 and Lemma 5.24 added (a function at each end vertex; no block needed on strongly connected carriers); found by a sub-agent, reread by the author, examined by a challenger and two micro-reviews; three steps in Lean.")
wcsv("READINESS.csv", ready); changes.append(("changed", "PROGRAM/registers/READINESS.csv", "paper G10 revised"))
ops = rd("OPEN_PROBLEMS.csv")
AM = {"OP-19": " Edition Z20: on a finite strongly connected carrier of constant out-degree d >= 2 without parallel arcs, with every gain reaching every vertex in abundance, a consistent rule that adds over end vertices a function of the multiset of gains, which may depend on the vertex and vanishes on the empty multiset, is a combination of the count and of the squares for the characters in which the step is norm-preserving, the same at every vertex (G10-01-25 to G10-01-27). No block and no norm preservation is assumed; where no character qualifies only the count is consistent.",
      "OP-30": " Edition Z20: the same function at every end vertex, a full block and generating block entries are no longer assumed on strongly connected carriers with abundant gains (G10-01-26). Still assumed: additivity over events with disjoint sets of end vertices; dependence on a walk through its gain alone; the value zero on the empty multiset; the carrier. Open: parallel arcs with merging, unequal out-degrees, non-abelian groups, carriers that are not strongly connected (a closed form for the quadratic part), and everything that selects between the count and the squares."}
for r in ops:
    if r["id"] in AM: r["statement"] += AM[r["id"]]
wcsv("OPEN_PROBLEMS.csv", ops); changes.append(("changed", "PROGRAM/registers/OPEN_PROBLEMS.csv", "OP-19 and OP-30 amended"))
bp = os.path.join(REG, "BRIDGE_CANDIDATE_REGISTER.json"); br = json.load(open(bp))
br["retained_outliers"]["three_vertex_carrier_where_a_block_character_fails_for_the_whole_step"] = 1
json.dump(br, open(bp, "w"), indent=1, ensure_ascii=False); changes.append(("changed", "PROGRAM/registers/BRIDGE_CANDIDATE_REGISTER.json", "one retained value added"))
gp = os.path.join(REG, "ONTOLOGY_GATE_MAP.json"); gm = json.load(open(gp)); gm["edition"] = NEW
for g in gm["gates"]:
    if g["id"] == "P5": g["evidence"] += " Edition Z20: on finite strongly connected carriers with abundant gains the rule need not be assumed to use one function at all end vertices, nor the carrier to have a block (G10-01-25 to G10-01-27); the consistent rules are the count and the squares for the characters in which the whole step is norm-preserving. Nothing selects between them."
json.dump(gm, open(gp, "w"), indent=1, ensure_ascii=False); changes.append(("changed", "PROGRAM/registers/ONTOLOGY_GATE_MAP.json", "evidence of P5 amended; no state changed"))
dp = os.path.join(OUT, "PROGRAM", "figures", "Gate_Map_2026-11-13.dot"); dot = open(dp).read(); assert "edition Z19, 13 November 2026" in dot
open(dp, "w").write(dot.replace("edition Z19, 13 November 2026", "edition Z20, 13 November 2026").replace("Editions Z4 to Z19 change evidence", "Editions Z4 to Z20 change evidence")); changes.append(("changed", "PROGRAM/figures/Gate_Map_2026-11-13.dot", "edition label"))
subprocess.run(["dot", "-Tpdf", dp, "-o", dp[:-4] + ".pdf"], check=True); changes.append(("changed", "PROGRAM/figures/Gate_Map_2026-11-13.pdf", "edition label"))
HDR = (OLD + ", 13 November 2026", NEW + ", 13 November 2026")
edit("CONSTRUCTED_TRIALS/README.md", [HDR], "edition identifier")
S4 = "REVIEW_RECORDS/Director_Z/Session_4/"
for dp_, _, fs_ in os.walk(os.path.join(SRC, "rec")):
    for f in sorted(fs_):
        rel_ = os.path.relpath(os.path.join(dp_, f), os.path.join(SRC, "rec")); put(os.path.join(dp_, f), S4 + rel_, "sixteenth addendum to the fourth-session record")
if PCP:
    put(os.path.join(PCP, "register.jsonl"), S4 + "register/register.jsonl", "register of the fourth session, extended by review Z20")
    nev = len(open(os.path.join(PCP, "register.jsonl")).read().strip().split("\n"))
    import re
    p4 = os.path.join(OUT, S4 + "README_SESSION_4.md"); t = open(p4).read(); m = re.search(r"The register: .*?present chain\)\.", t, re.S); assert m
    t = t.replace(m.group(0), "The register: %d events; head digest of the chain `%s`; SHA-256 of the file `%s` (edition Z20; earlier editions end at earlier events of the present chain)." % (nev, os.environ.get("PCP_HEAD", "see pcpos verify"), sha(os.path.join(PCP, "register.jsonl"))))
    a_ = "findings Z-111 to Z-114 |"; assert a_ in t
    t = t.replace(a_, a_ + "\n| `ADDENDUM_EDITION_Z20.md`, `NEW_Z_SCOPED_FINDINGS_SESSION_4_ADDENDUM_16.csv`, `challenger_8/`, `micro/micro8/`, `micro/micro9/`, `FLUSH_MANIFEST_2026-11-13.csv`, further files in `cross_review/` | the sixteenth addendum: Theorem 5.22, Corollary 5.23 and Lemma 5.24 of paper G10 with a challenger's and two micro-reviews' programs, the cross-review of four notes of Director G (addendum 8), and the manifest of the files moved from the repository root; findings Z-115 to Z-118 |").replace("`CHANGES_Z17_TO_Z18.md`, `CHANGES_Z18_TO_Z19.md`", "`CHANGES_Z17_TO_Z18.md`, `CHANGES_Z18_TO_Z19.md`, `CHANGES_Z19_TO_Z20.md`")
    open(p4, "w").write(t); changes.append(("changed", S4 + "README_SESSION_4.md", "register digests; sixteenth addendum listed"))
for rel in ("PROGRAM/CONTRIBUTIONS.md", "PROGRAM/PAPER_INDEX.md", "PROGRAM/STANDARDS.md", "PROGRAM/CHARTER.md", "REVIEW_RECORDS/README.md", "README.md", "LEGACY/README.md", "NEGATIVE_CONTROLS/README.md"):
    extra = []
    if rel == "PROGRAM/PAPER_INDEX.md": extra = [(f"| G10 | {T10} | article | {old_pages} | {old_statements} |", f"| G10 | {T10} | article | {n10} | 27 |")]
    if rel == "README.md": extra = [(f"({637 + old_pages} assembled pages;", f"({637 + n10} assembled pages;"), (f"theorem registry ({len(reg) - len(NEWST)} rows)", f"theorem registry ({len(reg)} rows)")]
    edit(rel, [HDR] + extra, "edition identifier" + ("; paper G10 revised" if extra else ""))
shutil.copy(os.path.abspath(__file__), os.path.join(OUT, "tools", "director_z_update_16.py")); changes.append(("added", "tools/director_z_update_16.py", "the program that applied these changes"))
changes.append(("added", S4 + "CHANGES_Z19_TO_Z20.md", "this list")); changes.append(("changed", "MANIFEST.json", "edition identifier, digests"))
with open(os.path.join(OUT, S4, "CHANGES_Z19_TO_Z20.md"), "w") as f:
    f.write("# Changes from edition Z19 to edition Z20\n\n13 November 2026. Every other file is byte-identical to edition Z19.\n\n| Change | File | Reason |\n|---|---|---|\n")
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
print("edition Z20:", len(files), "files;", len(reg), "registry rows;", n10, "pages in G10;", len(changes), "changes")






