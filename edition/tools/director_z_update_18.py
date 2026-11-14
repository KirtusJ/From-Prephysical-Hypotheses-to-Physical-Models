#!/usr/bin/env python3
"""Apply the fourteenth addendum of the fourth Director Z session (13 November 2026) to a copy of edition Z17, giving edition Z18:
paper G10 revised without a new statement (corrections after a comb of the whole session), one program, the records of the comb, register amendments.
Arguments: build directory (g10, comp_comb, rec), copy of edition Z17, optional directory holding the session register (.pcp).
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
OLD, NEW = "FPHPM-BASELINE-2026-11-13-Z17", "FPHPM-BASELINE-2026-11-13-Z18"
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
for f in sorted(os.listdir(os.path.join(SRC, "comp_comb"))): put(os.path.join(SRC, "comp_comb", f), ba + f, "computation cited by paper G10 (Section 4); added at the comb")

edit("COMPUTATION/Lean/README.md", [("The files prove the algebraic lemmas used in paper G10 (the recursion of Theorem 5.1, Lemma 5.4, the reductions of Proposition 5.10, the character step of Theorem 5.8) and the sequential-projection inequality used by Director G.", "The files prove algebraic lemmas used in paper G10: the recursion of Theorem 5.1 (SignedLineRecursion), Lemma 5.4 (ParallelogramInt, ParallelogramGroup, Parallelogram), the convexity step of Theorem 5.2 (PowerSumConvexity), the character step of Theorem 5.8 (CharacterIndependence), the reductions of Proposition 5.10 (ThreeLaw, FourLaw), the law M_k of Theorem 5.11 (MkSmall, MkGeneral), certificates for Theorem 5.12 (VslCertificates), two steps of Theorem 5.16 (GaugeBlock), three steps of Theorem 5.18 (MultisetBlock); and the sequential-projection inequality used by Director G (SequentialProjections). All fifteen files were rerun at the comb after edition Z17.")], "list of contents completed")
rr = os.path.join(OUT, "COMPUTATION", "RERUN_RECORD_2026-11-12.csv")
with open(rr, newline="") as f: rows = list(csv.DictReader(f))
rows += [dict(program="Baseline_Additions: all programs with stored result files (26 completed reruns in fresh directories)", status="RAN_OK", stored_output_compared="yes", stdout_equals_stored="26 of 26 result files byte-identical; gauge_bl.py identical apart from 24 timing fields", note="comb after edition Z17; see REVIEW_RECORDS/Director_Z/Session_4/comb/rerun/status.txt"), dict(program="Baseline_Additions: verify_k4_additive_ratios.py", status="RAN_OK", stored_output_compared="yes", stdout_equals_stored="3 of 3 predicates; exact arithmetic", note="edition Z18"), dict(program="COMPUTATION/Lean: four core files and eleven Mathlib files", status="RAN_OK", stored_output_compared="not applicable", stdout_equals_stored="all exit code 0; permitted axioms only; six warnings of unused local facts", note="rerun by the director at the comb")]
wcsv(rr, rows); changes.append(("changed", "COMPUTATION/RERUN_RECORD_2026-11-12.csv", "three rows appended"))
reg = rd("THEOREM_REGISTRY.csv")
NEWST = []


labels = [f"{r['kind']} {r['number']}" for r in reg if r["paper"] == "G10"] + [f"{k} {n}" for _, k, n, _ in NEWST]
n10, pg = pages_of(PDF10, labels)
for r in reg:
    if r["paper"] == "G10": r["paper_file_page"] = r["part_page"] = str(pg[f"{r['kind']} {r['number']}"])
for i_, k, num, name in NEWST:
    reg.append(dict(id=i_, paper="G10", part="1", part_title=T10, kind=k, number=num, name=name, status="PROOF_IN_MANUSCRIPT", paper_file_page=str(pg[f"{k} {num}"]), part_page=str(pg[f"{k} {num}"]), legacy_locator=""))
wcsv("THEOREM_REGISTRY.csv", reg); changes.append(("changed", "PROGRAM/registers/THEOREM_REGISTRY.csv", "G10 pages checked"))
old_statements = [r["statements"] for r in rd("PAPER_INDEX.csv") if r["id"] == "G10"][0]
index = rd("PAPER_INDEX.csv")
for r in index:
    if r["id"] == "G10": r.update(pages=str(n10), statements="24")
wcsv("PAPER_INDEX.csv", index); changes.append(("changed", "PROGRAM/registers/PAPER_INDEX.csv", "paper G10 revised"))
cross = rd("COMPONENT_CROSSWALK.csv")
for c in cross:
    if c["paper"] == "G10": c.update(baseline_sha256=sha(os.path.join(OUT, PART10)), pages=str(n10), change="first issued with edition Z4; revised in editions Z5 to Z18")
wcsv("COMPONENT_CROSSWALK.csv", cross); changes.append(("changed", "PROGRAM/registers/COMPONENT_CROSSWALK.csv", "G10 digest"))
ready = rd("READINESS.csv")
for r in ready:
    if r["paper"] == "G10": r.update(pages=str(n10), labelled_statements="24", gaps=r["gaps"] + " Edition Z18: no new statement; one false sentence, one overstated sentence and the abstract, introduction and assumptions list corrected after two readers went over the whole paper; Corollary 5.9(d) narrowed.")
wcsv("READINESS.csv", ready); changes.append(("changed", "PROGRAM/registers/READINESS.csv", "paper G10 revised"))
ops = rd("OPEN_PROBLEMS.csv")
AM = {"OP-21": " Edition Z18: where the text of edition Z9 above cites G10-01-12 for the statement that the consistent kernels in degree two are those that change sign under -1, with dimension ceil(q/4), the row is G10-01-13 since edition Z10 (G10-01-12 is the general statement for any finite abelian group and degree). The bridge register and the gate map carry the same citation."}
for r in ops:
    if r["id"] in AM: r["statement"] += AM[r["id"]]
wcsv("OPEN_PROBLEMS.csv", ops); changes.append(("changed", "PROGRAM/registers/OPEN_PROBLEMS.csv", "OP-21 amended"))
bp = os.path.join(REG, "BRIDGE_CANDIDATE_REGISTER.json"); br = json.load(open(bp))
br["retained_outliers"]["reviewer_predicates_failed_and_first_named_in_edition_Z18"] = 7
json.dump(br, open(bp, "w"), indent=1, ensure_ascii=False); changes.append(("changed", "PROGRAM/registers/BRIDGE_CANDIDATE_REGISTER.json", "one retained value added"))
gp = os.path.join(REG, "ONTOLOGY_GATE_MAP.json"); gm = json.load(open(gp)); gm["edition"] = NEW
for g in gm["gates"]:
    if g["id"] == "P5": g["evidence"] += " Edition Z18: no new evidence; a comb of the session corrected summary sentences of paper G10 that omitted hypotheses. Where an earlier entry cites G10-01-12 for the degree-two kernel statement, the row is G10-01-13."
json.dump(gm, open(gp, "w"), indent=1, ensure_ascii=False); changes.append(("changed", "PROGRAM/registers/ONTOLOGY_GATE_MAP.json", "evidence of P5 amended; no state changed"))
dp = os.path.join(OUT, "PROGRAM", "figures", "Gate_Map_2026-11-13.dot"); dot = open(dp).read(); assert "edition Z17, 13 November 2026" in dot
open(dp, "w").write(dot.replace("edition Z17, 13 November 2026", "edition Z18, 13 November 2026").replace("Editions Z4 to Z17 change evidence", "Editions Z4 to Z18 change evidence")); changes.append(("changed", "PROGRAM/figures/Gate_Map_2026-11-13.dot", "edition label"))
subprocess.run(["dot", "-Tpdf", dp, "-o", dp[:-4] + ".pdf"], check=True); changes.append(("changed", "PROGRAM/figures/Gate_Map_2026-11-13.pdf", "edition label"))
HDR = (OLD + ", 13 November 2026", NEW + ", 13 November 2026")
edit("CONSTRUCTED_TRIALS/README.md", [HDR], "edition identifier")
S4 = "REVIEW_RECORDS/Director_Z/Session_4/"
for dp_, _, fs_ in os.walk(os.path.join(SRC, "rec")):
    for f in sorted(fs_):
        rel_ = os.path.relpath(os.path.join(dp_, f), os.path.join(SRC, "rec")); put(os.path.join(dp_, f), S4 + rel_, "fourteenth addendum to the fourth-session record")
if PCP:
    put(os.path.join(PCP, "register.jsonl"), S4 + "register/register.jsonl", "register of the fourth session, extended by review Z18")
    nev = len(open(os.path.join(PCP, "register.jsonl")).read().strip().split("\n"))
    import re
    p4 = os.path.join(OUT, S4 + "README_SESSION_4.md"); t = open(p4).read(); m = re.search(r"The register: .*?present chain\)\.", t, re.S); assert m
    t = t.replace(m.group(0), "The register: %d events; head digest of the chain `%s`; SHA-256 of the file `%s` (edition Z18; earlier editions end at earlier events of the present chain)." % (nev, os.environ.get("PCP_HEAD", "see pcpos verify"), sha(os.path.join(PCP, "register.jsonl"))))
    a_ = "findings Z-103 to Z-106 |"; assert a_ in t
    t = t.replace(a_, a_ + "\n| `ADDENDUM_EDITION_Z18.md`, `NEW_Z_SCOPED_FINDINGS_SESSION_4_ADDENDUM_14.csv`, `comb/`, `micro/micro4/`, `pcp_workers/HIERARCHY_LOG.md` | the fourteenth addendum: a comb of the whole session (reruns, scans, two readers of paper G10) with its records, the corrections to the paper, failed reviewer predicates named, a folder that had not been copied, and a log of the review hierarchy; findings Z-107 to Z-110 |").replace("`CHANGES_Z15_TO_Z16.md`, `CHANGES_Z16_TO_Z17.md`", "`CHANGES_Z15_TO_Z16.md`, `CHANGES_Z16_TO_Z17.md`, `CHANGES_Z17_TO_Z18.md`")
    open(p4, "w").write(t); changes.append(("changed", S4 + "README_SESSION_4.md", "register digests; fourteenth addendum listed"))
for rel in ("PROGRAM/CONTRIBUTIONS.md", "PROGRAM/PAPER_INDEX.md", "PROGRAM/STANDARDS.md", "PROGRAM/CHARTER.md", "REVIEW_RECORDS/README.md", "README.md", "LEGACY/README.md", "NEGATIVE_CONTROLS/README.md"):
    extra = []
    if rel == "PROGRAM/PAPER_INDEX.md": extra = [(f"| G10 | {T10} | article | {old_pages} | {old_statements} |", f"| G10 | {T10} | article | {n10} | 24 |")]
    if rel == "README.md": extra = [(f"({637 + old_pages} assembled pages;", f"({637 + n10} assembled pages;"), (f"theorem registry ({len(reg) - len(NEWST)} rows)", f"theorem registry ({len(reg)} rows)")]
    edit(rel, [HDR] + extra, "edition identifier" + ("; paper G10 revised" if extra else ""))
shutil.copy(os.path.abspath(__file__), os.path.join(OUT, "tools", "director_z_update_16.py")); changes.append(("added", "tools/director_z_update_16.py", "the program that applied these changes"))
changes.append(("added", S4 + "CHANGES_Z17_TO_Z18.md", "this list")); changes.append(("changed", "MANIFEST.json", "edition identifier, digests"))
with open(os.path.join(OUT, S4, "CHANGES_Z17_TO_Z18.md"), "w") as f:
    f.write("# Changes from edition Z17 to edition Z18\n\n13 November 2026. Every other file is byte-identical to edition Z17.\n\n| Change | File | Reason |\n|---|---|---|\n")
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
print("edition Z18:", len(files), "files;", len(reg), "registry rows;", n10, "pages in G10;", len(changes), "changes")






