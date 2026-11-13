#!/usr/bin/env python3
"""Apply the ninth addendum of the fourth Director Z session (13 November 2026) to a copy of edition Z12, giving edition Z13:
paper G10 revised after the reports of the review queue, one Lean file, the queue reports, worker trials, register amendments.
Arguments: build directory (g10, mathlib, rec), copy of edition Z12, optional directory holding the session register (.pcp).
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
OLD, NEW = "FPHPM-BASELINE-2026-11-13-Z12", "FPHPM-BASELINE-2026-11-13-Z13"
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
for f in sorted(os.listdir(os.path.join(SRC, "mathlib"))): put(os.path.join(SRC, "mathlib", f), "COMPUTATION/Lean/Mathlib/" + f, "Lean 4 proof with Mathlib (termwise inequality of Theorem 5.2)")
edit("COMPUTATION/Lean/README.md", [("holds seven files for Lean 4.12.0 with Mathlib v4.12.0", "holds eight files for Lean 4.12.0 with Mathlib v4.12.0")], "one Mathlib file added")
rr = os.path.join(OUT, "COMPUTATION", "RERUN_RECORD_2026-11-12.csv")
with open(rr, newline="") as f: rows = list(csv.DictReader(f))
rows += [dict(program="COMPUTATION/Lean/Mathlib/PowerSumConvexity.lean with Mathlib v4.12.0", status="RAN_OK", stored_output_compared="not applicable", stdout_equals_stored="exit code 0; axioms propext, Classical.choice, Quot.sound", note="written by the review queue session; rerun by the director for edition Z13"),
         dict(program="Baseline_Additions/verify_continuation_selection.py", status="RAN_OK", stored_output_compared="yes", stdout_equals_stored="unchanged", note="edition Z13: the recorded column rms_width of the staircase rows is wrong at 13 samples (unwrapped centroid); it enters no predicate; file kept")]
wcsv(rr, rows); changes.append(("changed", "COMPUTATION/RERUN_RECORD_2026-11-12.csv", "two rows appended"))
reg = rd("THEOREM_REGISTRY.csv")
labels = [f"{r['kind']} {r['number']}" for r in reg if r["paper"] == "G10"]
n10, pg = pages_of(PDF10, labels)
for r in reg:
    if r["paper"] == "G10": r["paper_file_page"] = r["part_page"] = str(pg[f"{r['kind']} {r['number']}"])
wcsv("THEOREM_REGISTRY.csv", reg); changes.append(("changed", "PROGRAM/registers/THEOREM_REGISTRY.csv", "G10 pages updated"))
old_statements = [r["statements"] for r in rd("PAPER_INDEX.csv") if r["id"] == "G10"][0]
index = rd("PAPER_INDEX.csv")
for r in index:
    if r["id"] == "G10": r.update(pages=str(n10))
wcsv("PAPER_INDEX.csv", index); changes.append(("changed", "PROGRAM/registers/PAPER_INDEX.csv", "paper G10 revised"))
cross = rd("COMPONENT_CROSSWALK.csv")
for c in cross:
    if c["paper"] == "G10": c.update(baseline_sha256=sha(os.path.join(OUT, PART10)), pages=str(n10), change="first issued with edition Z4; revised in editions Z5 to Z13")
wcsv("COMPONENT_CROSSWALK.csv", cross); changes.append(("changed", "PROGRAM/registers/COMPONENT_CROSSWALK.csv", "G10 digest"))
ready = rd("READINESS.csv")
for r in ready:
    if r["paper"] == "G10":
        a_ = "The other statements after Theorem 5.3 have been read by their author only."; assert a_ in r["gaps"]
        r.update(pages=str(n10), gaps=r["gaps"].replace(a_, "Edition Z13: Lemma 3.1, Proposition 4.1, Theorems 5.2 and 5.5 and Propositions 5.6, 6.1 and 6.2 were examined by challengers of an unattended review queue (same model family, paper text only); six places of wording corrected, Lemma 3.1 given its missing hypothesis, Theorem 5.2 a shorter proof checked in Lean. Theorems 5.1 and 5.3 and Lemma 5.4 have no challenger report."))
wcsv("READINESS.csv", ready); changes.append(("changed", "PROGRAM/registers/READINESS.csv", "paper G10 revised"))
ops = rd("OPEN_PROBLEMS.csv")
AM = {"OP-24": " Edition Z13: the review stack is defined in the repository (agent definitions and a file queue) and is served by a separate session on a schedule, without the director. Its first period gave eight reports; no proof of G10 failed; Lemma 3.1 was false as worded without the sentence before it and is corrected; one instrument artefact was found in a result file. Worker trials through the ACR reference host ran a Claude worker and a local Qwen worker concurrently and nested; the local model scored 0 of 3 on bounded checks. All these reviewers except Qwen share the director's model family.",
      "OP-27": " Edition Z13: G10 Lemma 3.1 now carries its hypotheses in the statement: every vertex has an outgoing arc, and events and histories are those from one fixed starting vertex. Without the first, the identification of events with sets of histories fails at dead ends."}
for r in ops:
    if r["id"] in AM: r["statement"] += AM[r["id"]]
assert sum(1 for r in ops if r["id"] in AM) == 2
wcsv("OPEN_PROBLEMS.csv", ops); changes.append(("changed", "PROGRAM/registers/OPEN_PROBLEMS.csv", "OP-24 and OP-27 amended"))
bp = os.path.join(REG, "BRIDGE_CANDIDATE_REGISTER.json"); br = json.load(open(bp))
br["retained_outliers"]["rms_width_artefact_in_continuation_selection_staircase_rows"] = 4096.04
json.dump(br, open(bp, "w"), indent=1, ensure_ascii=False); changes.append(("changed", "PROGRAM/registers/BRIDGE_CANDIDATE_REGISTER.json", "one retained value added"))
gp = os.path.join(REG, "ONTOLOGY_GATE_MAP.json"); gm = json.load(open(gp)); gm["edition"] = NEW
json.dump(gm, open(gp, "w"), indent=1, ensure_ascii=False); changes.append(("changed", "PROGRAM/registers/ONTOLOGY_GATE_MAP.json", "edition identifier; no evidence or state changed"))
dp = os.path.join(OUT, "PROGRAM", "figures", "Gate_Map_2026-11-13.dot"); dot = open(dp).read(); assert "edition Z12, 13 November 2026" in dot
open(dp, "w").write(dot.replace("edition Z12, 13 November 2026", "edition Z13, 13 November 2026").replace("Editions Z4 to Z12 change evidence", "Editions Z4 to Z13 change evidence")); changes.append(("changed", "PROGRAM/figures/Gate_Map_2026-11-13.dot", "edition label"))
subprocess.run(["dot", "-Tpdf", dp, "-o", dp[:-4] + ".pdf"], check=True); changes.append(("changed", "PROGRAM/figures/Gate_Map_2026-11-13.pdf", "edition label"))
HDR = (OLD + ", 13 November 2026", NEW + ", 13 November 2026")
edit("CONSTRUCTED_TRIALS/README.md", [HDR], "edition identifier")
S4 = "REVIEW_RECORDS/Director_Z/Session_4/"
for dp_, _, fs_ in os.walk(os.path.join(SRC, "rec")):
    for f in sorted(fs_):
        rel_ = os.path.relpath(os.path.join(dp_, f), os.path.join(SRC, "rec")); put(os.path.join(dp_, f), S4 + rel_, "ninth addendum to the fourth-session record")
if PCP:
    put(os.path.join(PCP, "register.jsonl"), S4 + "register/register.jsonl", "register of the fourth session, extended by review Z13")
    nev = len(open(os.path.join(PCP, "register.jsonl")).read().strip().split("\n"))
    import re
    p4 = os.path.join(OUT, S4 + "README_SESSION_4.md"); t = open(p4).read(); m = re.search(r"The register: .*?present chain\)\.", t, re.S); assert m
    t = t.replace(m.group(0), "The register: %d events; head digest of the chain `%s`; SHA-256 of the file `%s` (edition Z13; earlier editions end at earlier events of the present chain)." % (nev, os.environ.get("PCP_HEAD", "see pcpos verify"), sha(os.path.join(PCP, "register.jsonl"))))
    a_ = "findings Z-088 to Z-092 |"; assert a_ in t
    t = t.replace(a_, a_ + "\n| `ADDENDUM_EDITION_Z13.md`, `NEW_Z_SCOPED_FINDINGS_SESSION_4_ADDENDUM_9.csv`, `queue_reports/`, `pcp_workers/` | the ninth addendum: the reports of the unattended review queue and what they changed in paper G10, the worker trials through the ACR reference host, and the fifth cross-review of Director G; findings Z-093 to Z-095 |").replace("`CHANGES_Z10_TO_Z11.md`, `CHANGES_Z11_TO_Z12.md`", "`CHANGES_Z10_TO_Z11.md`, `CHANGES_Z11_TO_Z12.md`, `CHANGES_Z12_TO_Z13.md`")
    assert "CHANGES_Z12_TO_Z13.md" in t
    open(p4, "w").write(t); changes.append(("changed", S4 + "README_SESSION_4.md", "register digests; ninth addendum listed"))
for rel in ("PROGRAM/CONTRIBUTIONS.md", "PROGRAM/PAPER_INDEX.md", "PROGRAM/STANDARDS.md", "PROGRAM/CHARTER.md", "REVIEW_RECORDS/README.md", "README.md", "LEGACY/README.md", "NEGATIVE_CONTROLS/README.md"):
    extra = []
    if rel == "PROGRAM/PAPER_INDEX.md" and str(old_pages) != str(n10): extra = [(f"| G10 | {T10} | article | {old_pages} | {old_statements} |", f"| G10 | {T10} | article | {n10} | {old_statements} |")]
    if rel == "README.md" and old_pages != n10: extra = [(f"({637 + old_pages} assembled pages;", f"({637 + n10} assembled pages;")]
    edit(rel, [HDR] + extra, "edition identifier")
shutil.copy(os.path.abspath(__file__), os.path.join(OUT, "tools", "director_z_update_13.py")); changes.append(("added", "tools/director_z_update_13.py", "the program that applied these changes"))
changes.append(("added", S4 + "CHANGES_Z12_TO_Z13.md", "this list")); changes.append(("changed", "MANIFEST.json", "edition identifier, digests"))
with open(os.path.join(OUT, S4, "CHANGES_Z12_TO_Z13.md"), "w") as f:
    f.write("# Changes from edition Z12 to edition Z13\n\n13 November 2026. Every other file is byte-identical to edition Z12.\n\n| Change | File | Reason |\n|---|---|---|\n")
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
print("edition Z13:", len(files), "files;", len(reg), "registry rows;", n10, "pages in G10;", len(changes), "changes")






