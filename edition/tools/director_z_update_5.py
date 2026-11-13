#!/usr/bin/env python3
"""Apply the addendum of the fourth Director Z session (13 November 2026) to a copy of edition Z4, giving edition Z5:
paper G10 revised (Theorem 5.3 added), two programs, register amendments.
Arguments: build directory (g10, comp, rec), copy of edition Z4, optional directory holding the session register (.pcp).
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
OLD, NEW = "FPHPM-BASELINE-2026-11-13-Z4", "FPHPM-BASELINE-2026-11-13-Z5"
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
for f in sorted(os.listdir(os.path.join(SRC, "comp"))): put(os.path.join(SRC, "comp", f), ba + f, "computation cited by paper G10 (Theorem 5.3)")
rr = os.path.join(OUT, "COMPUTATION", "RERUN_RECORD_2026-11-12.csv")
with open(rr, newline="") as f: rows = list(csv.DictReader(f))
R = lambda p, n: dict(program=p, status="RAN_OK", stored_output_compared="yes", stdout_equals_stored="result file byte-identical", note=n)
rows += [R("Baseline_Additions/verify_degree_two_quadratic_rule.py (fresh directory)", "4 predicates, of which one is failed and kept (Q1: an unknown without an equation on 2 of 40 carriers); added in edition Z5"),
         R("Baseline_Additions/verify_degree_two_quadratic_rule_followup.py (fresh directory)", "2 predicates; about one minute; added in edition Z5")]
wcsv(rr, rows); changes.append(("changed", "COMPUTATION/RERUN_RECORD_2026-11-12.csv", "two rows appended"))
reg = rd("THEOREM_REGISTRY.csv")
labels = [f"{r['kind']} {r['number']}" for r in reg if r["paper"] == "G10"] + ["Theorem 5.3"]
n10, pg = pages_of(PDF10, labels)
for r in reg:
    if r["paper"] == "G10": r["paper_file_page"] = r["part_page"] = str(pg[f"{r['kind']} {r['number']}"])
reg.append(dict(id="G10-01-07", paper="G10", part="1", part_title=T10, kind="Theorem", number="5.3", name="Every finite connected signed gain digraph that is norm-preserving of degree two: a rule adding over end vertices a function of the modulus is consistent only for the square",
                status="PROOF_IN_MANUSCRIPT", paper_file_page=str(pg["Theorem 5.3"]), part_page=str(pg["Theorem 5.3"]), legacy_locator=""))
wcsv("THEOREM_REGISTRY.csv", reg); changes.append(("changed", "PROGRAM/registers/THEOREM_REGISTRY.csv", "G10 pages updated; row G10-01-07 added"))
index = rd("PAPER_INDEX.csv")
for r in index:
    if r["id"] == "G10": r.update(pages=str(n10), statements="7")
wcsv("PAPER_INDEX.csv", index); changes.append(("changed", "PROGRAM/registers/PAPER_INDEX.csv", "paper G10 revised"))
cross = rd("COMPONENT_CROSSWALK.csv")
for c in cross:
    if c["paper"] == "G10": c.update(baseline_sha256=sha(os.path.join(OUT, PART10)), pages=str(n10), change="first issued with edition Z4; revised in edition Z5")
wcsv("COMPONENT_CROSSWALK.csv", cross); changes.append(("changed", "PROGRAM/registers/COMPONENT_CROSSWALK.csv", "G10 digest"))
ready = rd("READINESS.csv")
for r in ready:
    if r["paper"] == "G10": r.update(pages=str(n10), labelled_statements="7", gaps="first issued with edition Z4; revised in edition Z5 (Theorem 5.3 added); proofs not independently checked; equation (7.1) is heuristic and supported by computed instances only; the case of gains of order four in Section 5 rests on instances; the reference to Li and So was not inspected (OP-30)")
wcsv("READINESS.csv", ready); changes.append(("changed", "PROGRAM/registers/READINESS.csv", "paper G10 revised"))
ops = rd("OPEN_PROBLEMS.csv")
AM = {"OP-19": " Edition Z5: the square is forced on every finite connected signed gain digraph that is norm-preserving of degree two, whatever its base digraph (G10-01-07); for gains of order four the same is observed on ten carriers and not proved.",
      "OP-30": " Edition Z5: within the record-sum form the carrier is no longer restricted to the line: every connected signed carrier of degree two forces the square (G10-01-07). Open in addition: a proof for gains that are not real, and for degrees above two."}
for r in ops:
    if r["id"] in AM: r["statement"] += AM[r["id"]]
wcsv("OPEN_PROBLEMS.csv", ops); changes.append(("changed", "PROGRAM/registers/OPEN_PROBLEMS.csv", "OP-19 and OP-30 amended"))
bp = os.path.join(REG, "BRIDGE_CANDIDATE_REGISTER.json"); br = json.load(open(bp)); k = 0
for e in br["edges"]:
    if e["statement"].startswith("Among rules that add over end vertices a function of the modulus"):
        e["statement"] += " Edition Z5: the square is the only consistent rule of this form on every finite connected signed gain digraph that is norm-preserving of degree two (G10-01-07); observed, not proved, for gains of order four."
        e["locator"] += "; G10-01-07; verify_degree_two_quadratic_rule_followup.py"; k += 1
assert k == 1
br["retained_outliers"]["degree_two_first_program_carriers_with_two_dimensional_solution_space"] = "2 of 40 (an unknown without an equation; walks of length 10); 0 of 40 with walks of length 16"
json.dump(br, open(bp, "w"), indent=1, ensure_ascii=False); changes.append(("changed", "PROGRAM/registers/BRIDGE_CANDIDATE_REGISTER.json", "one edge amended; one retained value added"))
gp = os.path.join(REG, "ONTOLOGY_GATE_MAP.json"); gm = json.load(open(gp)); gm["edition"] = NEW
for g in gm["gates"]:
    if g["id"] == "P5": g["evidence"] += " Edition Z5: the square is forced on every finite connected signed carrier that is norm-preserving of degree two (G10-01-07)."
json.dump(gm, open(gp, "w"), indent=1, ensure_ascii=False); changes.append(("changed", "PROGRAM/registers/ONTOLOGY_GATE_MAP.json", "evidence of P5 amended; no state changed"))
dp = os.path.join(OUT, "PROGRAM", "figures", "Gate_Map_2026-11-13.dot"); dot = open(dp).read(); assert "edition Z4, 13 November 2026" in dot
open(dp, "w").write(dot.replace("edition Z4, 13 November 2026", "edition Z5, 13 November 2026").replace("Edition Z4 changes evidence", "Editions Z4 and Z5 change evidence")); changes.append(("changed", "PROGRAM/figures/Gate_Map_2026-11-13.dot", "edition label"))
subprocess.run(["dot", "-Tpdf", dp, "-o", dp[:-4] + ".pdf"], check=True); changes.append(("changed", "PROGRAM/figures/Gate_Map_2026-11-13.pdf", "edition label"))
HDR = (OLD + ", 13 November 2026", NEW + ", 13 November 2026")
edit("CONSTRUCTED_TRIALS/README.md", [HDR, ("G8 Section 9 (1); G10 Theorems 5.1, 5.2 |", "G8 Section 9 (1); G10 Theorems 5.1, 5.2, 5.3 (every connected signed carrier of degree two) |")], "edition identifier; GH-1 ledger")
p = os.path.join(OUT, "CONSTRUCTED_TRIALS", "GH-1", "GH-1_Assumptions_and_Dispositions.json"); d = json.load(open(p))
d["derived"].append(dict(id="G10-01-07", text="every finite connected signed carrier that is norm-preserving of degree two: consistent modulus rule is the square")); d["revised"] = "2026-11-13, edition Z5"
json.dump(d, open(p, "w"), indent=1, ensure_ascii=False); changes.append(("changed", "CONSTRUCTED_TRIALS/GH-1/GH-1_Assumptions_and_Dispositions.json", "GH-1 ledger amended"))
S4 = "REVIEW_RECORDS/Director_Z/Session_4/"
for f in sorted(os.listdir(os.path.join(SRC, "rec"))): put(os.path.join(SRC, "rec", f), S4 + f, "addendum to the fourth-session record")
if PCP:
    put(os.path.join(PCP, "register.jsonl"), S4 + "register/register.jsonl", "register of the fourth session, extended by review Z5")
    nev = len(open(os.path.join(PCP, "register.jsonl")).read().strip().split("\n"))
    edit(S4 + "README_SESSION_4.md", [("The register: 37 events; head digest of the chain `ea97886d0cc8dcd7aba4d95f9844cc8c95f312e56c4796f8da0d5123e1b250d8`; SHA-256 of the file `6862457fbd2565882024348639c109bb4522ef865f3eadf078f48d0413312f89`.",
        "The register: %d events; head digest of the chain `%s`; SHA-256 of the file `%s` (edition Z5; in edition Z4 it had 37 events and head `ea97886d0cc8dcd7aba4d95f9844cc8c95f312e56c4796f8da0d5123e1b250d8`, which is event 36 of the present chain)." % (nev, os.environ.get("PCP_HEAD", "see pcpos verify"), sha(os.path.join(PCP, "register.jsonl")))),
        ("| `CHANGES_Z3_TO_Z4.md` | every file added or changed |", "| `CHANGES_Z3_TO_Z4.md`, `CHANGES_Z4_TO_Z5.md` | every file added or changed |\n| `ADDENDUM_EDITION_Z5.md`, `NEW_Z_SCOPED_FINDINGS_SESSION_4_ADDENDUM.csv` | the addendum: Theorem 5.3 of paper G10, findings Z-055 to Z-057 |")], "register digests; addendum listed")
T9 = "Reversible Steps on Gain Digraphs: Arc Structure, Complex Structure and the Ray Limit"
for rel in ("PROGRAM/CONTRIBUTIONS.md", "PROGRAM/PAPER_INDEX.md", "PROGRAM/STANDARDS.md", "PROGRAM/CHARTER.md", "REVIEW_RECORDS/README.md", "README.md", "LEGACY/README.md", "NEGATIVE_CONTROLS/README.md"):
    extra = []
    if rel == "PROGRAM/PAPER_INDEX.md": extra = [(f"| G10 | {T10} | article | {old_pages} | 6 |", f"| G10 | {T10} | article | {n10} | 7 |")]
    if rel == "README.md": extra = [(f"({637 + old_pages} assembled pages;", f"({637 + n10} assembled pages;"), ("theorem registry (387 rows)", f"theorem registry ({len(reg)} rows)")]
    edit(rel, [HDR] + extra, "edition identifier" + ("; paper G10 revised" if extra else ""))
shutil.copy(os.path.abspath(__file__), os.path.join(OUT, "tools", "director_z_update_5.py")); changes.append(("added", "tools/director_z_update_5.py", "the program that applied these changes"))
changes.append(("added", S4 + "CHANGES_Z4_TO_Z5.md", "this list")); changes.append(("changed", "MANIFEST.json", "edition identifier, digests"))
with open(os.path.join(OUT, S4, "CHANGES_Z4_TO_Z5.md"), "w") as f:
    f.write("# Changes from edition Z4 to edition Z5\n\n13 November 2026. Every other file is byte-identical to edition Z4.\n\n| Change | File | Reason |\n|---|---|---|\n")
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
print("edition Z5:", len(files), "files;", len(reg), "registry rows;", n10, "pages in G10;", len(changes), "changes")
