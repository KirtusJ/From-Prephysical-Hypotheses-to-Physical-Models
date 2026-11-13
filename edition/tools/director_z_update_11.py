#!/usr/bin/env python3
"""Apply the seventh addendum of the fourth Director Z session (13 November 2026) to a copy of edition Z10, giving edition Z11:
paper G10 revised (Proposition 5.10), one program, one Lean file for the core library and five for Mathlib, the fourth addendum to the
cross-review of Director G, register amendments.
Arguments: build directory (g10, comp, lean, mathlib, rec), copy of edition Z10, optional directory holding the session register (.pcp).
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
OLD, NEW = "FPHPM-BASELINE-2026-11-13-Z10", "FPHPM-BASELINE-2026-11-13-Z11"
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
for f in sorted(os.listdir(os.path.join(SRC, "comp"))): put(os.path.join(SRC, "comp", f), ba + f, "computation cited by paper G10 (Proposition 5.10)")
for f in sorted(os.listdir(os.path.join(SRC, "lean"))): put(os.path.join(SRC, "lean", f), "COMPUTATION/Lean/" + f, "Lean 4 proof, core library")
for f in sorted(os.listdir(os.path.join(SRC, "mathlib"))): put(os.path.join(SRC, "mathlib", f), "COMPUTATION/Lean/Mathlib/" + f, "Lean 4 proof with Mathlib, or its project file")
open(os.path.join(OUT, "COMPUTATION", "Lean", "README.md"), "w").write("# Lean proofs\n\nFour files in this folder need Lean 4.12.0 and the core library only: check each with `lean <file>`. The folder `Mathlib/` holds five files for Lean 4.12.0 with Mathlib v4.12.0, with the lakefile, toolchain file and manifest of the project they were checked in: place the five files in a folder `FPHPM/` beside the lakefile, run `lake exe cache get`, then `lake env lean FPHPM/<file>`. A pass is exit code 0 and a line naming only the axioms `propext`, `Quot.sound` and, with Mathlib, `Classical.choice`. The files prove the algebraic lemmas used in paper G10 (the recursion of Theorem 5.1, Lemma 5.4, the reductions of Proposition 5.10, the character step of Theorem 5.8) and the sequential-projection inequality used by Director G. No statement about gain digraphs, walks or events is formalized. Written by sub-agents of the fourth Director Z session and rechecked in that session.\n")
changes.append(("changed", "COMPUTATION/Lean/README.md", "how to check the Lean files, with Mathlib"))
rr = os.path.join(OUT, "COMPUTATION", "RERUN_RECORD_2026-11-12.csv")
with open(rr, newline="") as f: rows = list(csv.DictReader(f))
rows += [dict(program="Baseline_Additions/verify_record_sum_higher_degree.py (fresh directory)", status="RAN_OK", stored_output_compared="yes", stdout_equals_stored="result file byte-identical", note="3 predicates; added in edition Z11"),
         dict(program="COMPUTATION/Lean/ThreeLaw.lean with Lean 4.12.0; COMPUTATION/Lean/Mathlib: five files with Mathlib v4.12.0", status="RAN_OK", stored_output_compared="not applicable", stdout_equals_stored="exit code 0 for each; axioms propext, Quot.sound and, with Mathlib, Classical.choice", note="added in edition Z11"),
         dict(program="Director G, commit 616c1d6: check_fixed_transport.py and check_field_echo.py rerun by sub-agents", status="RAN_OK", stored_output_compared="yes", stdout_equals_stored="all checks true; two CSV files byte-identical; JSON outputs equal after parsing or within 2.7e-15", note="rerun for edition Z11")]
wcsv(rr, rows); changes.append(("changed", "COMPUTATION/RERUN_RECORD_2026-11-12.csv", "three rows appended"))
reg = rd("THEOREM_REGISTRY.csv")
NEWST = [("G10-01-14", "Proposition", "5.10", "On blocks of degree three and four with gains of order 3, 6 or 4 a consistent rule of the record-sum form is a multiple of the squared modulus")]
labels = [f"{r['kind']} {r['number']}" for r in reg if r["paper"] == "G10"] + [f"{k} {n}" for _, k, n, _ in NEWST]
n10, pg = pages_of(PDF10, labels)
for r in reg:
    if r["paper"] == "G10": r["paper_file_page"] = r["part_page"] = str(pg[f"{r['kind']} {r['number']}"])
for i_, k, num, name in NEWST:
    reg.append(dict(id=i_, paper="G10", part="1", part_title=T10, kind=k, number=num, name=name, status="PROOF_IN_MANUSCRIPT", paper_file_page=str(pg[f"{k} {num}"]), part_page=str(pg[f"{k} {num}"]), legacy_locator=""))
wcsv("THEOREM_REGISTRY.csv", reg); changes.append(("changed", "PROGRAM/registers/THEOREM_REGISTRY.csv", "G10 pages updated; row G10-01-14 added"))
old_statements = [r["statements"] for r in rd("PAPER_INDEX.csv") if r["id"] == "G10"][0]
index = rd("PAPER_INDEX.csv")
for r in index:
    if r["id"] == "G10": r.update(pages=str(n10), statements="14")
wcsv("PAPER_INDEX.csv", index); changes.append(("changed", "PROGRAM/registers/PAPER_INDEX.csv", "paper G10 revised"))
cross = rd("COMPONENT_CROSSWALK.csv")
for c in cross:
    if c["paper"] == "G10": c.update(baseline_sha256=sha(os.path.join(OUT, PART10)), pages=str(n10), change="first issued with edition Z4; revised in editions Z5 to Z11")
wcsv("COMPONENT_CROSSWALK.csv", cross); changes.append(("changed", "PROGRAM/registers/COMPONENT_CROSSWALK.csv", "G10 digest"))
ready = rd("READINESS.csv")
for r in ready:
    if r["paper"] == "G10":
        a_ = "The other statements after Theorem 5.3 have been read by their author only."; assert a_ in r["gaps"]
        r.update(pages=str(n10), labelled_statements="14", gaps=r["gaps"].replace("and Z10 (Theorem 5.8 restated", "Z10 (Theorem 5.8 restated").replace("Corollary 5.9). Proposition 4.1", "Corollary 5.9) and Z11 (Proposition 5.10). Proposition 4.1").replace("are checked in Lean 4.", "are checked in Lean 4; with Mathlib, Lemma 5.4, the recursion, the reductions of Proposition 5.10 and the character step of Theorem 5.8 are checked for real values."))
        assert "Z11 (Proposition 5.10)" in r["gaps"] and "with Mathlib" in r["gaps"]
wcsv("READINESS.csv", ready); changes.append(("changed", "PROGRAM/registers/READINESS.csv", "paper G10 revised"))
ops = rd("OPEN_PROBLEMS.csv")
AM = {"OP-19": " Edition Z11: the second order of a rule of the record-sum form is forced also on blocks of degree three and four with gains of order 3, 6 or 4 (G10-01-14). Director G (commit 616c1d6, in the default branch) derives f(n) = n^2 for integer record weights on a fixed ring carrier from the stability of the odds of an old record under one further free step; the premise of stable odds at every horizon with one common response is stated and not derived, and the accompanying Lean file proves that the recurrence implies the square, not that the walk gives the recurrence (cross-review by a sub-agent of Director Z).",
      "OP-23": " Edition Z11: Director G gives the exact output of the direction-switch preparation for every schedule of field signs; alternating the sign after each block gives the zero-field output up to a known phase and translation, so the yield is the zero-field yield at every field strength, and no schedule exceeds it. The finite reversal control stays between 0.29 and 0.33 over sheet orders 8191 to 524287 and is not monotone (sub-agent of Director Z); it is not yet evidence for the limit.",
      "OP-24": " Edition Z11: Director G merged pull request 2 into the default branch; both directors now work on one branch history. Fourth cross-review of Director G, made by two sub-agents of Director Z and read by Director Z, who did not follow the proofs personally: no defect found; points of scope recorded. Mathlib is available to Director Z; five files check the algebraic lemmas of G10 for real values and the sequential-projection inequality of Director G. A figure of Director Z's third cross-review differs by 1.8e-3 from a sub-agent's recomputation; unresolved.",
      "OP-30": " Edition Z11: rules of the record-sum form in degrees above two: settled for two block types (degree three with gains of order 3 or 6; degree four with gains of order 4), where the rule is the square (G10-01-14). Open: other blocks, other degrees, higher orders (where the conjugate characters will enter), and the items of edition Z10."}
for r in ops:
    if r["id"] in AM: r["statement"] += AM[r["id"]]
assert sum(1 for r in ops if r["id"] in AM) == 4
wcsv("OPEN_PROBLEMS.csv", ops); changes.append(("changed", "PROGRAM/registers/OPEN_PROBLEMS.csv", "OP-19, OP-23, OP-24 and OP-30 amended"))
bp = os.path.join(REG, "BRIDGE_CANDIDATE_REGISTER.json"); br = json.load(open(bp)); k = 0
for e in br["edges"]:
    if e["statement"].startswith("Among rules that add over end vertices a function of the modulus"):
        e["statement"] += " Edition Z11: the square is forced also on blocks of degree three and four with gains of order 3, 6 or 4 (G10-01-14)."; e["locator"] += "; G10-01-14"; k += 1
assert k == 1
br["retained_outliers"]["reversal_words_alternating_schedule_at_sheet_orders_8191_32749_131071_524287"] = [0.2923, 0.3226, 0.3101, 0.3301]
br["retained_outliers"]["unresolved_difference_in_quartered_schedule_mean_at_delta_0p1"] = 0.0018
json.dump(br, open(bp, "w"), indent=1, ensure_ascii=False); changes.append(("changed", "PROGRAM/registers/BRIDGE_CANDIDATE_REGISTER.json", "one edge amended; two retained values added"))
gp = os.path.join(REG, "ONTOLOGY_GATE_MAP.json"); gm = json.load(open(gp)); gm["edition"] = NEW; k = 0
for g in gm["gates"]:
    if g["id"] == "P5": g["evidence"] += " Edition Z11: the square is forced within the record-sum form also on blocks of degree three and four with gains of order 3, 6 or 4 (G10-01-14). Director G derives the square for integer record weights on a fixed carrier from a stated premise of stable record odds. The algebraic lemmas are machine-checked in Lean with Mathlib; nothing about carriers or events is formalized."; k += 1
assert k == 1
json.dump(gm, open(gp, "w"), indent=1, ensure_ascii=False); changes.append(("changed", "PROGRAM/registers/ONTOLOGY_GATE_MAP.json", "evidence of P5 amended; no state changed"))
dp = os.path.join(OUT, "PROGRAM", "figures", "Gate_Map_2026-11-13.dot"); dot = open(dp).read(); assert "edition Z10, 13 November 2026" in dot and "Editions Z4 to Z10 change evidence" in dot
open(dp, "w").write(dot.replace("edition Z10, 13 November 2026", "edition Z11, 13 November 2026").replace("Editions Z4 to Z10 change evidence", "Editions Z4 to Z11 change evidence")); changes.append(("changed", "PROGRAM/figures/Gate_Map_2026-11-13.dot", "edition label"))
subprocess.run(["dot", "-Tpdf", dp, "-o", dp[:-4] + ".pdf"], check=True); changes.append(("changed", "PROGRAM/figures/Gate_Map_2026-11-13.pdf", "edition label"))
HDR = (OLD + ", 13 November 2026", NEW + ", 13 November 2026")
edit("CONSTRUCTED_TRIALS/README.md", [HDR], "edition identifier")
p = os.path.join(OUT, "CONSTRUCTED_TRIALS", "GH-1", "GH-1_Assumptions_and_Dispositions.json"); d = json.load(open(p))
d["derived"].append(dict(id="G10-01-14", text="record-sum form on blocks of degree three and four with gains of order 3, 6 or 4: the rule is the square")); d["revised"] = "2026-11-13, edition Z11"
json.dump(d, open(p, "w"), indent=1, ensure_ascii=False); changes.append(("changed", "CONSTRUCTED_TRIALS/GH-1/GH-1_Assumptions_and_Dispositions.json", "GH-1 ledger amended"))
S4 = "REVIEW_RECORDS/Director_Z/Session_4/"
for dp_, _, fs_ in os.walk(os.path.join(SRC, "rec")):
    for f in sorted(fs_):
        rel_ = os.path.relpath(os.path.join(dp_, f), os.path.join(SRC, "rec")); put(os.path.join(dp_, f), S4 + rel_, "seventh addendum to the fourth-session record")
if PCP:
    put(os.path.join(PCP, "register.jsonl"), S4 + "register/register.jsonl", "register of the fourth session, extended by review Z11")
    nev = len(open(os.path.join(PCP, "register.jsonl")).read().strip().split("\n"))
    import re
    p4 = os.path.join(OUT, S4 + "README_SESSION_4.md"); t = open(p4).read(); m = re.search(r"The register: .*?present chain\)\.", t, re.S); assert m
    t = t.replace(m.group(0), "The register: %d events; head digest of the chain `%s`; SHA-256 of the file `%s` (edition Z11; the heads of editions Z4 to Z10 are the heads of the present chain at events 36, 52, 67, 93, 116, 145 and 188, the last being `110c00c66b8856896138a7e8fc79318cc4629d3491d22a72e961b256516a1518`; the present chain)." % (nev, os.environ.get("PCP_HEAD", "see pcpos verify"), sha(os.path.join(PCP, "register.jsonl"))))
    a_ = "findings Z-077 to Z-082 |"; assert a_ in t
    t = t.replace(a_, a_ + "\n| `ADDENDUM_EDITION_Z11.md`, `NEW_Z_SCOPED_FINDINGS_SESSION_4_ADDENDUM_7.csv`, further files in `cross_review/` | the seventh addendum: Proposition 5.10 of paper G10, the Lean files with Mathlib in `COMPUTATION/Lean/Mathlib/`, and the cross-review of Director G's papers on fixed transport and field reversal, made by two sub-agents; findings Z-083 to Z-087 |").replace("`CHANGES_Z8_TO_Z9.md`, `CHANGES_Z9_TO_Z10.md`", "`CHANGES_Z8_TO_Z9.md`, `CHANGES_Z9_TO_Z10.md`, `CHANGES_Z10_TO_Z11.md`")
    assert "CHANGES_Z10_TO_Z11.md" in t
    open(p4, "w").write(t); changes.append(("changed", S4 + "README_SESSION_4.md", "register digests; seventh addendum listed"))
for rel in ("PROGRAM/CONTRIBUTIONS.md", "PROGRAM/PAPER_INDEX.md", "PROGRAM/STANDARDS.md", "PROGRAM/CHARTER.md", "REVIEW_RECORDS/README.md", "README.md", "LEGACY/README.md", "NEGATIVE_CONTROLS/README.md"):
    extra = []
    if rel == "PROGRAM/PAPER_INDEX.md": extra = [(f"| G10 | {T10} | article | {old_pages} | {old_statements} |", f"| G10 | {T10} | article | {n10} | 14 |")]
    if rel == "README.md": extra = [(f"({637 + old_pages} assembled pages;", f"({637 + n10} assembled pages;"), (f"theorem registry ({len(reg) - 1} rows)", f"theorem registry ({len(reg)} rows)")]
    if rel == "REVIEW_RECORDS/README.md": extra = [("(commits b626c0d, 00b8e26, d4f6fea and 6bb2d14)", "(commits b626c0d, 00b8e26, d4f6fea, 6bb2d14 and 616c1d6; since merged into the default branch as the folder `Director_G/`)"), ("the cross-review of six of their results is in", "the cross-review of eight of their results is in")]
    edit(rel, [HDR] + extra, "edition identifier" + ("; paper G10 revised" if extra else ""))
shutil.copy(os.path.abspath(__file__), os.path.join(OUT, "tools", "director_z_update_11.py")); changes.append(("added", "tools/director_z_update_11.py", "the program that applied these changes"))
changes.append(("added", S4 + "CHANGES_Z10_TO_Z11.md", "this list")); changes.append(("changed", "MANIFEST.json", "edition identifier, digests"))
with open(os.path.join(OUT, S4, "CHANGES_Z10_TO_Z11.md"), "w") as f:
    f.write("# Changes from edition Z10 to edition Z11\n\n13 November 2026. Every other file is byte-identical to edition Z10.\n\n| Change | File | Reason |\n|---|---|---|\n")
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
print("edition Z11:", len(files), "files;", len(reg), "registry rows;", n10, "pages in G10;", len(changes), "changes")




