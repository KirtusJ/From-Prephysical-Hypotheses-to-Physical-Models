#!/usr/bin/env python3
"""Apply the tenth addendum of the fourth Director Z session (13 November 2026) to a copy of edition Z13, giving edition Z14:
paper G10 revised (Theorem 5.12, Corollary 5.13), the programs of the folder Vanishing_Sums, one Lean file, reports of a challenger
and a micro-review, register amendments.
Arguments: build directory (g10, comp_vsl, mathlib, rec), copy of edition Z13, optional directory holding the session register (.pcp).
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
OLD, NEW = "FPHPM-BASELINE-2026-11-13-Z13", "FPHPM-BASELINE-2026-11-13-Z14"
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
for f in sorted(os.listdir(os.path.join(SRC, "comp_vsl"))): put(os.path.join(SRC, "comp_vsl", f), ba + "Vanishing_Sums/" + f, "computation cited by paper G10 (Theorem 5.12); written by a sub-agent")
for f in sorted(os.listdir(os.path.join(SRC, "mathlib"))): put(os.path.join(SRC, "mathlib", f), "COMPUTATION/Lean/Mathlib/" + f, "Lean 4 certificates for special vanishing sums")
edit("COMPUTATION/Lean/README.md", [("holds eight files for Lean 4.12.0 with Mathlib v4.12.0", "holds nine files for Lean 4.12.0 with Mathlib v4.12.0")], "one Mathlib file added")
rr = os.path.join(OUT, "COMPUTATION", "RERUN_RECORD_2026-11-12.csv")
with open(rr, newline="") as f: rows = list(csv.DictReader(f))
rows += [dict(program="Baseline_Additions/Vanishing_Sums: t1_poly.py, t1b_multi.py, t2_lattice.py, t3_cert.py", status="RAN_OK", stored_output_compared="no", stdout_equals_stored="not rerun in a fresh directory; logs and two result files kept as produced by the sub-agent", note="edition Z14; 60 of 63 predicates met, three small boxes failed and kept"),
         dict(program="COMPUTATION/Lean/Mathlib/VslCertificates.lean with Mathlib v4.12.0", status="RAN_OK", stored_output_compared="not applicable", stdout_equals_stored="exit code 0; axioms propext, Classical.choice, Quot.sound", note="rerun by the director for edition Z14")]
wcsv(rr, rows); changes.append(("changed", "COMPUTATION/RERUN_RECORD_2026-11-12.csv", "two rows appended"))
reg = rd("THEOREM_REGISTRY.csv")
NEWST = [("G10-01-16", "Theorem", "5.12", "A function of the modulus on Z[zeta] satisfying the vanishing-sum equation for one multiset of roots of unity with sum zero is a combination of the conjugate squared moduli"),
         ("G10-01-17", "Corollary", "5.13", "On a norm-preserving gain digraph with gains in the roots of unity, a merging pair of vertices and abundance of gains at it, the consistent rules of the record-sum form are the combinations of the conjugate squared moduli, with factor d")]
labels = [f"{r['kind']} {r['number']}" for r in reg if r["paper"] == "G10"] + [f"{k} {n}" for _, k, n, _ in NEWST]
n10, pg = pages_of(PDF10, labels)
for r in reg:
    if r["paper"] == "G10": r["paper_file_page"] = r["part_page"] = str(pg[f"{r['kind']} {r['number']}"])
for i_, k, num, name in NEWST:
    reg.append(dict(id=i_, paper="G10", part="1", part_title=T10, kind=k, number=num, name=name, status="PROOF_IN_MANUSCRIPT", paper_file_page=str(pg[f"{k} {num}"]), part_page=str(pg[f"{k} {num}"]), legacy_locator=""))
wcsv("THEOREM_REGISTRY.csv", reg); changes.append(("changed", "PROGRAM/registers/THEOREM_REGISTRY.csv", "G10 pages updated; rows G10-01-16 and G10-01-17 added"))
old_statements = [r["statements"] for r in rd("PAPER_INDEX.csv") if r["id"] == "G10"][0]
index = rd("PAPER_INDEX.csv")
for r in index:
    if r["id"] == "G10": r.update(pages=str(n10), statements="17")
wcsv("PAPER_INDEX.csv", index); changes.append(("changed", "PROGRAM/registers/PAPER_INDEX.csv", "paper G10 revised"))
cross = rd("COMPONENT_CROSSWALK.csv")
for c in cross:
    if c["paper"] == "G10": c.update(baseline_sha256=sha(os.path.join(OUT, PART10)), pages=str(n10), change="first issued with edition Z4; revised in editions Z5 to Z14")
wcsv("COMPONENT_CROSSWALK.csv", cross); changes.append(("changed", "PROGRAM/registers/COMPONENT_CROSSWALK.csv", "G10 digest"))
ready = rd("READINESS.csv")
for r in ready:
    if r["paper"] == "G10":
        r.update(pages=str(n10), labelled_statements="17", gaps=r["gaps"] + " Edition Z14: Theorem 5.12 and Corollary 5.13 added (any norm-preserving carrier with a merging pair); proof found with a sub-agent, rechecked by the author, examined by a challenger and a micro-review; not formalized.")
wcsv("READINESS.csv", ready); changes.append(("changed", "PROGRAM/registers/READINESS.csv", "paper G10 revised"))
ops = rd("OPEN_PROBLEMS.csv")
AM = {"OP-19": " Edition Z14: for gains in the roots of unity the second order of a rule of the record-sum form holds on every norm-preserving carrier, of any degree and with blocks of any form, that has two vertices with a common successor reached by every gain in abundance; the consistent rules are the combinations of the conjugate squared moduli (G10-01-16, G10-01-17). The earlier cases (signed line, degree two, Fourier blocks) are instances where that hypothesis holds.",
      "OP-30": " Edition Z14: the classification of rules of the record-sum form no longer depends on the form of the blocks (G10-01-17). Dependence on the modulus cannot be weakened to invariance under units, signs and conjugation (Re(a^4) on the Gaussian integers). Open: carriers on which the abundance of gains fails, and whether it follows from finiteness and connectedness; characters of infinite order; a bound on the order K of the differences in the proof; rules that are neither pair rules nor of the record-sum form; non-abelian gain groups."}
for r in ops:
    if r["id"] in AM: r["statement"] += AM[r["id"]]
assert sum(1 for r in ops if r["id"] in AM) == 2
wcsv("OPEN_PROBLEMS.csv", ops); changes.append(("changed", "PROGRAM/registers/OPEN_PROBLEMS.csv", "OP-19 and OP-30 amended"))
bp = os.path.join(REG, "BRIDGE_CANDIDATE_REGISTER.json"); br = json.load(open(bp)); k = 0
for e in br["edges"]:
    if e["statement"].startswith("Among rules that add over end vertices a function of the modulus"):
        e["statement"] += " Edition Z14: the same holds on every norm-preserving carrier with gains in the roots of unity that has a merging pair of vertices with abundance of gains, whatever the degree and the form of the blocks (G10-01-16, G10-01-17)."; e["locator"] += "; G10-01-16; G10-01-17"; k += 1
assert k == 1
br["retained_outliers"]["vanishing_sum_box_runs_failed_at_smallest_box_of_36"] = 3
json.dump(br, open(bp, "w"), indent=1, ensure_ascii=False); changes.append(("changed", "PROGRAM/registers/BRIDGE_CANDIDATE_REGISTER.json", "one edge amended; one retained value added"))
gp = os.path.join(REG, "ONTOLOGY_GATE_MAP.json"); gm = json.load(open(gp)); gm["edition"] = NEW; k = 0
for g in gm["gates"]:
    if g["id"] == "P5": g["evidence"] += " Edition Z14: within the record-sum form, for gains in the roots of unity, the second order and the residual freedom of conjugate characters hold on every norm-preserving carrier with a merging pair and abundance of gains, independently of degree and block form (G10-01-16, G10-01-17). Still assumed: events as sets of histories, the record-sum form, the carrier."; k += 1
assert k == 1
json.dump(gm, open(gp, "w"), indent=1, ensure_ascii=False); changes.append(("changed", "PROGRAM/registers/ONTOLOGY_GATE_MAP.json", "evidence of P5 amended; no state changed"))
dp = os.path.join(OUT, "PROGRAM", "figures", "Gate_Map_2026-11-13.dot"); dot = open(dp).read(); assert "edition Z13, 13 November 2026" in dot
open(dp, "w").write(dot.replace("edition Z13, 13 November 2026", "edition Z14, 13 November 2026").replace("Editions Z4 to Z13 change evidence", "Editions Z4 to Z14 change evidence")); changes.append(("changed", "PROGRAM/figures/Gate_Map_2026-11-13.dot", "edition label"))
subprocess.run(["dot", "-Tpdf", dp, "-o", dp[:-4] + ".pdf"], check=True); changes.append(("changed", "PROGRAM/figures/Gate_Map_2026-11-13.pdf", "edition label"))
HDR = (OLD + ", 13 November 2026", NEW + ", 13 November 2026")
edit("CONSTRUCTED_TRIALS/README.md", [HDR], "edition identifier")
p = os.path.join(OUT, "CONSTRUCTED_TRIALS", "GH-1", "GH-1_Assumptions_and_Dispositions.json"); d = json.load(open(p))
d["derived"].append(dict(id="G10-01-17", text="record-sum form on any norm-preserving carrier with a merging pair and abundance of gains: the consistent rules are the conjugate squared moduli")); d["revised"] = "2026-11-13, edition Z14"
json.dump(d, open(p, "w"), indent=1, ensure_ascii=False); changes.append(("changed", "CONSTRUCTED_TRIALS/GH-1/GH-1_Assumptions_and_Dispositions.json", "GH-1 ledger amended"))
S4 = "REVIEW_RECORDS/Director_Z/Session_4/"
for dp_, _, fs_ in os.walk(os.path.join(SRC, "rec")):
    for f in sorted(fs_):
        rel_ = os.path.relpath(os.path.join(dp_, f), os.path.join(SRC, "rec")); put(os.path.join(dp_, f), S4 + rel_, "tenth addendum to the fourth-session record")
if PCP:
    put(os.path.join(PCP, "register.jsonl"), S4 + "register/register.jsonl", "register of the fourth session, extended by review Z14")
    nev = len(open(os.path.join(PCP, "register.jsonl")).read().strip().split("\n"))
    import re
    p4 = os.path.join(OUT, S4 + "README_SESSION_4.md"); t = open(p4).read(); m = re.search(r"The register: .*?present chain\)\.", t, re.S); assert m
    t = t.replace(m.group(0), "The register: %d events; head digest of the chain `%s`; SHA-256 of the file `%s` (edition Z14; earlier editions end at earlier events of the present chain)." % (nev, os.environ.get("PCP_HEAD", "see pcpos verify"), sha(os.path.join(PCP, "register.jsonl"))))
    a_ = "findings Z-093 to Z-095 |"; assert a_ in t
    t = t.replace(a_, a_ + "\n| `ADDENDUM_EDITION_Z14.md`, `NEW_Z_SCOPED_FINDINGS_SESSION_4_ADDENDUM_10.csv`, `challenger_3/`, `micro/micro4/` | the tenth addendum: Theorem 5.12 and Corollary 5.13 of paper G10 with the reports of a challenger and a micro-review; findings Z-096, Z-097 |").replace("`CHANGES_Z11_TO_Z12.md`, `CHANGES_Z12_TO_Z13.md`", "`CHANGES_Z11_TO_Z12.md`, `CHANGES_Z12_TO_Z13.md`, `CHANGES_Z13_TO_Z14.md`")
    assert "CHANGES_Z13_TO_Z14.md" in t
    open(p4, "w").write(t); changes.append(("changed", S4 + "README_SESSION_4.md", "register digests; tenth addendum listed"))
for rel in ("PROGRAM/CONTRIBUTIONS.md", "PROGRAM/PAPER_INDEX.md", "PROGRAM/STANDARDS.md", "PROGRAM/CHARTER.md", "REVIEW_RECORDS/README.md", "README.md", "LEGACY/README.md", "NEGATIVE_CONTROLS/README.md"):
    extra = []
    if rel == "PROGRAM/PAPER_INDEX.md": extra = [(f"| G10 | {T10} | article | {old_pages} | {old_statements} |", f"| G10 | {T10} | article | {n10} | 17 |")]
    if rel == "README.md": extra = [(f"({637 + old_pages} assembled pages;", f"({637 + n10} assembled pages;"), (f"theorem registry ({len(reg) - 2} rows)", f"theorem registry ({len(reg)} rows)")]
    edit(rel, [HDR] + extra, "edition identifier" + ("; paper G10 revised" if extra else ""))
shutil.copy(os.path.abspath(__file__), os.path.join(OUT, "tools", "director_z_update_14.py")); changes.append(("added", "tools/director_z_update_14.py", "the program that applied these changes"))
changes.append(("added", S4 + "CHANGES_Z13_TO_Z14.md", "this list")); changes.append(("changed", "MANIFEST.json", "edition identifier, digests"))
with open(os.path.join(OUT, S4, "CHANGES_Z13_TO_Z14.md"), "w") as f:
    f.write("# Changes from edition Z13 to edition Z14\n\n13 November 2026. Every other file is byte-identical to edition Z13.\n\n| Change | File | Reason |\n|---|---|---|\n")
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
print("edition Z14:", len(files), "files;", len(reg), "registry rows;", n10, "pages in G10;", len(changes), "changes")






