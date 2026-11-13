#!/usr/bin/env python3
"""Apply the eighth addendum of the fourth Director Z session (13 November 2026) to a copy of edition Z11, giving edition Z12:
paper G10 revised (Theorem 5.11; Proposition 5.10 and Corollary 5.7 corrected), two programs, two Lean files with Mathlib, reports of a
challenger and three micro-reviews, register amendments.
Arguments: build directory (g10, comp, mathlib, rec), copy of edition Z11, optional directory holding the session register (.pcp).
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
OLD, NEW = "FPHPM-BASELINE-2026-11-13-Z11", "FPHPM-BASELINE-2026-11-13-Z12"
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
for f in sorted(os.listdir(os.path.join(SRC, "comp"))): put(os.path.join(SRC, "comp", f), ba + f, "computation cited by paper G10 (Theorem 5.11)")
for f in sorted(os.listdir(os.path.join(SRC, "mathlib"))): put(os.path.join(SRC, "mathlib", f), "COMPUTATION/Lean/Mathlib/" + f, "Lean 4 proof with Mathlib")
edit("COMPUTATION/Lean/README.md", [("holds five files for Lean 4.12.0 with Mathlib v4.12.0", "holds seven files for Lean 4.12.0 with Mathlib v4.12.0"), ("place the five files in a folder", "place the files in a folder")], "two Mathlib files added")
rr = os.path.join(OUT, "COMPUTATION", "RERUN_RECORD_2026-11-12.csv")
with open(rr, newline="") as f: rows = list(csv.DictReader(f))
R = lambda p, n: dict(program=p, status="RAN_OK", stored_output_compared="yes", stdout_equals_stored="result file byte-identical", note=n)
rows += [R("Baseline_Additions/verify_fourier_blocks_any_degree.py (fresh directory)", "3 predicates, 2 failed and kept; added in edition Z12"),
         R("Baseline_Additions/verify_fourier_blocks_any_degree_followup.py (fresh directory)", "4 predicates; added in edition Z12"),
         dict(program="COMPUTATION/Lean/Mathlib: MkSmall.lean and MkGeneral.lean with Mathlib v4.12.0", status="RAN_OK", stored_output_compared="not applicable", stdout_equals_stored="exit code 0; axioms propext, Classical.choice, Quot.sound", note="added in edition Z12")]
wcsv(rr, rows); changes.append(("changed", "COMPUTATION/RERUN_RECORD_2026-11-12.csv", "three rows appended"))
reg = rd("THEOREM_REGISTRY.csv")
for r in reg:
    if r["id"] == "G10-01-14": r["name"] = "On blocks of degree three and four with gains of order 3, 6 or 4 and disjoint successor sets a consistent rule of the record-sum form is a multiple of the squared modulus"
NEWST = [("G10-01-15", "Theorem", "5.11", "For Fourier blocks of every degree d dividing q, with disjoint successor sets, the consistent rules of the record-sum form are the combinations of the conjugate squared moduli")]
labels = [f"{r['kind']} {r['number']}" for r in reg if r["paper"] == "G10"] + [f"{k} {n}" for _, k, n, _ in NEWST]
n10, pg = pages_of(PDF10, labels)
for r in reg:
    if r["paper"] == "G10": r["paper_file_page"] = r["part_page"] = str(pg[f"{r['kind']} {r['number']}"])
for i_, k, num, name in NEWST:
    reg.append(dict(id=i_, paper="G10", part="1", part_title=T10, kind=k, number=num, name=name, status="PROOF_IN_MANUSCRIPT", paper_file_page=str(pg[f"{k} {num}"]), part_page=str(pg[f"{k} {num}"]), legacy_locator=""))
wcsv("THEOREM_REGISTRY.csv", reg); changes.append(("changed", "PROGRAM/registers/THEOREM_REGISTRY.csv", "G10 pages updated; row G10-01-14 restated; row G10-01-15 added"))
old_statements = [r["statements"] for r in rd("PAPER_INDEX.csv") if r["id"] == "G10"][0]
index = rd("PAPER_INDEX.csv")
for r in index:
    if r["id"] == "G10": r.update(pages=str(n10), statements="15")
wcsv("PAPER_INDEX.csv", index); changes.append(("changed", "PROGRAM/registers/PAPER_INDEX.csv", "paper G10 revised"))
cross = rd("COMPONENT_CROSSWALK.csv")
for c in cross:
    if c["paper"] == "G10": c.update(baseline_sha256=sha(os.path.join(OUT, PART10)), pages=str(n10), change="first issued with edition Z4; revised in editions Z5 to Z12")
wcsv("COMPONENT_CROSSWALK.csv", cross); changes.append(("changed", "PROGRAM/registers/COMPONENT_CROSSWALK.csv", "G10 digest"))
ready = rd("READINESS.csv")
for r in ready:
    if r["paper"] == "G10":
        a_ = "and Z11 (Proposition 5.10). Proposition 4.1"; assert a_ in r["gaps"]
        r.update(pages=str(n10), labelled_statements="15", gaps=r["gaps"].replace(a_, ", Z11 (Proposition 5.10) and Z12 (Theorem 5.11; a condition missing from Proposition 5.10 added after a challenger's counterexample; wording of Corollary 5.7). Theorem 5.11 was examined by a challenger sub-agent and a micro-review. Proposition 4.1"))
wcsv("READINESS.csv", ready); changes.append(("changed", "PROGRAM/registers/READINESS.csv", "paper G10 revised"))
ops = rd("OPEN_PROBLEMS.csv")
AM = {"OP-19": " Edition Z12: for blocks rho_z kappa_y w^(zy) of every degree d dividing q, with disjoint successor sets, the consistent rules of the record-sum form are the combinations of the conjugate squared moduli (G10-01-15): within this family the second order does not depend on the degree, and G10-01-09 is the case d = 2.",
      "OP-24": " Edition Z12: a challenger sub-agent found that G10 Proposition 5.10 as issued in edition Z11 lacked the condition of disjoint successor sets and gave a counterexample; corrected. A lower tier of short micro-reviews was added at the principal's suggestion (edge cases of two statements; an outlier scan of all result files). The working method is recorded in CLAUDE.md at the root of the repository. The discrepancy of edition Z11 in a figure of the third cross-review is resolved (origin-site convention).",
      "OP-30": " Edition Z12: rules of the record-sum form are classified for Fourier blocks of every degree (G10-01-15). Open: blocks of other forms (real Hadamard blocks with other sign patterns, blocks from non-cyclic groups), carriers without disjoint successor sets (where the square itself need not be consistent), countable carriers, and the items of edition Z10."}
for r in ops:
    if r["id"] in AM: r["statement"] += AM[r["id"]]
assert sum(1 for r in ops if r["id"] in AM) == 3
wcsv("OPEN_PROBLEMS.csv", ops); changes.append(("changed", "PROGRAM/registers/OPEN_PROBLEMS.csv", "OP-19, OP-24 and OP-30 amended"))
bp = os.path.join(REG, "BRIDGE_CANDIDATE_REGISTER.json"); br = json.load(open(bp)); k = 0
for e in br["edges"]:
    if e["statement"].startswith("Among rules that add over end vertices a function of the modulus"):
        e["statement"] += " Edition Z12: for Fourier blocks of every degree the consistent rules are the conjugate squared moduli (G10-01-15); the condition of disjoint successor sets, missing from G10-01-14 as first issued, is necessary."; e["locator"] += "; G10-01-15"; k += 1
assert k == 1
br["retained_outliers"]["band_flatness_at_order_2_in_confinement_run_against_median"] = [2.5e-4, 3.3e-7]
br["retained_outliers"]["even_character_residual_outlier_in_first_kernel_run"] = 0.86
json.dump(br, open(bp, "w"), indent=1, ensure_ascii=False); changes.append(("changed", "PROGRAM/registers/BRIDGE_CANDIDATE_REGISTER.json", "one edge amended; two retained values added"))
gp = os.path.join(REG, "ONTOLOGY_GATE_MAP.json"); gm = json.load(open(gp)); gm["edition"] = NEW; k = 0
for g in gm["gates"]:
    if g["id"] == "P5": g["evidence"] += " Edition Z12: within the record-sum form the second order is forced on Fourier blocks of every degree, and what remains free is the combination of conjugate characters as in degree two (G10-01-15); the elimination is machine-checked for every degree."; k += 1
assert k == 1
json.dump(gm, open(gp, "w"), indent=1, ensure_ascii=False); changes.append(("changed", "PROGRAM/registers/ONTOLOGY_GATE_MAP.json", "evidence of P5 amended; no state changed"))
dp = os.path.join(OUT, "PROGRAM", "figures", "Gate_Map_2026-11-13.dot"); dot = open(dp).read(); assert "edition Z11, 13 November 2026" in dot and "Editions Z4 to Z11 change evidence" in dot
open(dp, "w").write(dot.replace("edition Z11, 13 November 2026", "edition Z12, 13 November 2026").replace("Editions Z4 to Z11 change evidence", "Editions Z4 to Z12 change evidence")); changes.append(("changed", "PROGRAM/figures/Gate_Map_2026-11-13.dot", "edition label"))
subprocess.run(["dot", "-Tpdf", dp, "-o", dp[:-4] + ".pdf"], check=True); changes.append(("changed", "PROGRAM/figures/Gate_Map_2026-11-13.pdf", "edition label"))
HDR = (OLD + ", 13 November 2026", NEW + ", 13 November 2026")
edit("CONSTRUCTED_TRIALS/README.md", [HDR], "edition identifier")
p = os.path.join(OUT, "CONSTRUCTED_TRIALS", "GH-1", "GH-1_Assumptions_and_Dispositions.json"); d = json.load(open(p))
d["derived"].append(dict(id="G10-01-15", text="record-sum form on Fourier blocks of every degree: the consistent rules are the conjugate squared moduli")); d["revised"] = "2026-11-13, edition Z12"
json.dump(d, open(p, "w"), indent=1, ensure_ascii=False); changes.append(("changed", "CONSTRUCTED_TRIALS/GH-1/GH-1_Assumptions_and_Dispositions.json", "GH-1 ledger amended"))
S4 = "REVIEW_RECORDS/Director_Z/Session_4/"
for dp_, _, fs_ in os.walk(os.path.join(SRC, "rec")):
    for f in sorted(fs_):
        rel_ = os.path.relpath(os.path.join(dp_, f), os.path.join(SRC, "rec")); put(os.path.join(dp_, f), S4 + rel_, "eighth addendum to the fourth-session record")
if PCP:
    put(os.path.join(PCP, "register.jsonl"), S4 + "register/register.jsonl", "register of the fourth session, extended by review Z12")
    nev = len(open(os.path.join(PCP, "register.jsonl")).read().strip().split("\n"))
    import re
    p4 = os.path.join(OUT, S4 + "README_SESSION_4.md"); t = open(p4).read(); m = re.search(r"The register: .*?present chain\)\.", t, re.S); assert m
    t = t.replace(m.group(0), "The register: %d events; head digest of the chain `%s`; SHA-256 of the file `%s` (edition Z12; earlier editions end at earlier events of the present chain)." % (nev, os.environ.get("PCP_HEAD", "see pcpos verify"), sha(os.path.join(PCP, "register.jsonl"))))
    a_ = "findings Z-083 to Z-087 |"; assert a_ in t
    t = t.replace(a_, a_ + "\n| `ADDENDUM_EDITION_Z12.md`, `NEW_Z_SCOPED_FINDINGS_SESSION_4_ADDENDUM_8.csv`, `challenger_2/`, `micro/` | the eighth addendum: Theorem 5.11 of paper G10, the correction of Proposition 5.10, the programs of a second challenger and of three micro-reviews; findings Z-088 to Z-092 |").replace("`CHANGES_Z9_TO_Z10.md`, `CHANGES_Z10_TO_Z11.md`", "`CHANGES_Z9_TO_Z10.md`, `CHANGES_Z10_TO_Z11.md`, `CHANGES_Z11_TO_Z12.md`")
    assert "CHANGES_Z11_TO_Z12.md" in t
    open(p4, "w").write(t); changes.append(("changed", S4 + "README_SESSION_4.md", "register digests; eighth addendum listed"))
for rel in ("PROGRAM/CONTRIBUTIONS.md", "PROGRAM/PAPER_INDEX.md", "PROGRAM/STANDARDS.md", "PROGRAM/CHARTER.md", "REVIEW_RECORDS/README.md", "README.md", "LEGACY/README.md", "NEGATIVE_CONTROLS/README.md"):
    extra = []
    if rel == "PROGRAM/PAPER_INDEX.md": extra = [(f"| G10 | {T10} | article | {old_pages} | {old_statements} |", f"| G10 | {T10} | article | {n10} | 15 |")]
    if rel == "README.md": extra = [(f"({637 + old_pages} assembled pages;", f"({637 + n10} assembled pages;"), (f"theorem registry ({len(reg) - 1} rows)", f"theorem registry ({len(reg)} rows)")]
    edit(rel, [HDR] + extra, "edition identifier" + ("; paper G10 revised" if extra else ""))
shutil.copy(os.path.abspath(__file__), os.path.join(OUT, "tools", "director_z_update_12.py")); changes.append(("added", "tools/director_z_update_12.py", "the program that applied these changes"))
changes.append(("added", S4 + "CHANGES_Z11_TO_Z12.md", "this list")); changes.append(("changed", "MANIFEST.json", "edition identifier, digests"))
with open(os.path.join(OUT, S4, "CHANGES_Z11_TO_Z12.md"), "w") as f:
    f.write("# Changes from edition Z11 to edition Z12\n\n13 November 2026. Every other file is byte-identical to edition Z11.\n\n| Change | File | Reason |\n|---|---|---|\n")
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
print("edition Z12:", len(files), "files;", len(reg), "registry rows;", n10, "pages in G10;", len(changes), "changes")





