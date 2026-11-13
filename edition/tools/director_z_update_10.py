#!/usr/bin/env python3
"""Apply the sixth addendum of the fourth Director Z session (13 November 2026) to a copy of edition Z9, giving edition Z10:
paper G10 revised (Theorem 5.8 in general form, Corollary 5.9), three programs, three Lean files, a challenger report, the third
addendum to the cross-review of Director G, register amendments.
Arguments: build directory (g10, comp, lean, rec), copy of edition Z9, optional directory holding the session register (.pcp).
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
OLD, NEW = "FPHPM-BASELINE-2026-11-13-Z9", "FPHPM-BASELINE-2026-11-13-Z10"
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
for f in sorted(os.listdir(os.path.join(SRC, "comp"))): put(os.path.join(SRC, "comp", f), ba + f, "computation cited by paper G10 (Theorem 5.8)")
for f in sorted(os.listdir(os.path.join(SRC, "lean"))): put(os.path.join(SRC, "lean", f), "COMPUTATION/Lean/" + f, "Lean 4 proof cited by paper G10")
open(os.path.join(OUT, "COMPUTATION", "Lean", "README.md"), "w").write("# Lean proofs\n\nThree files for Lean 4.12.0, core library only (no Mathlib). Check each with `lean <file>`; exit code 0 and the line naming the axioms `propext` and `Quot.sound` is a pass. They prove the recursion of G10 Theorem 5.1 and G10 Lemma 5.4 with integer values. Written by a sub-agent of the fourth Director Z session and rechecked in that session. Nothing else in the collection is formalized.\n")
changes.append(("added", "COMPUTATION/Lean/README.md", "how to check the Lean files"))
rr = os.path.join(OUT, "COMPUTATION", "RERUN_RECORD_2026-11-12.csv")
with open(rr, newline="") as f: rows = list(csv.DictReader(f))
R = lambda p, n: dict(program=p, status="RAN_OK", stored_output_compared="yes", stdout_equals_stored="result file byte-identical", note=n)
X = "REVIEW_RECORDS/Director_Z/Session_4/cross_review/"
rows += [R("Baseline_Additions/verify_kernel_rules_general.py (fresh directory)", "4 predicates, 1 failed and kept; added in edition Z10"),
         R("Baseline_Additions/verify_kernel_rules_general_followup.py (fresh directory)", "3 predicates, 1 failed and kept; added in edition Z10"),
         R("Baseline_Additions/verify_kernel_rules_general_followup_2.py (fresh directory)", "3 predicates; added in edition Z10"),
         R(X + "crosscheck_director_g_relative_transport.py (fresh directory)", "4 predicates, exact integers; added in edition Z10"),
         R(X + "crosscheck_director_g_position_records.py (fresh directory)", "3 predicates; about four minutes; added in edition Z10"),
         R(X + "crosscheck_director_g_offset_free_preparation.py (fresh directory)", "3 predicates; added in edition Z10"),
         dict(program="COMPUTATION/Lean: three files checked with Lean 4.12.0", status="RAN_OK", stored_output_compared="not applicable", stdout_equals_stored="exit code 0 for each; axioms propext and Quot.sound only", note="added in edition Z10"),
         dict(program="Director G, pull request 2, commit 6bb2d14: check_relative_transport.py and check_position_records.py rerun", status="RAN_OK", stored_output_compared="yes", stdout_equals_stored="all checks true; two outputs identical apart from line endings, two within 8e-15", note="rerun for edition Z10")]
wcsv(rr, rows); changes.append(("changed", "COMPUTATION/RERUN_RECORD_2026-11-12.csv", "eight rows appended"))
reg = rd("THEOREM_REGISTRY.csv")
for r in reg:
    if r["id"] == "G10-01-12": r["name"] = "For a finite abelian gain group and any degree, a switching-invariant pair rule is consistent under continuation exactly when its kernel is a combination of the characters for which the step is norm-preserving"
NEWST = [("G10-01-13", "Corollary", "5.9", "In degree two the consistent kernels are those that change sign under the element of the block relation; for the q-th roots of unity they form a space of dimension ceil(q/4) containing the conjugate rules and the lift rule")]
labels = [f"{r['kind']} {r['number']}" for r in reg if r["paper"] == "G10"] + [f"{k} {n}" for _, k, n, _ in NEWST]
n10, pg = pages_of(PDF10, labels)
for r in reg:
    if r["paper"] == "G10": r["paper_file_page"] = r["part_page"] = str(pg[f"{r['kind']} {r['number']}"])
for i_, k, num, name in NEWST:
    reg.append(dict(id=i_, paper="G10", part="1", part_title=T10, kind=k, number=num, name=name, status="PROOF_IN_MANUSCRIPT", paper_file_page=str(pg[f"{k} {num}"]), part_page=str(pg[f"{k} {num}"]), legacy_locator=""))
wcsv("THEOREM_REGISTRY.csv", reg); changes.append(("changed", "PROGRAM/registers/THEOREM_REGISTRY.csv", "G10 pages updated; row G10-01-12 restated; row G10-01-13 added"))
old_statements = [r["statements"] for r in rd("PAPER_INDEX.csv") if r["id"] == "G10"][0]
index = rd("PAPER_INDEX.csv")
for r in index:
    if r["id"] == "G10": r.update(pages=str(n10), statements="13")
wcsv("PAPER_INDEX.csv", index); changes.append(("changed", "PROGRAM/registers/PAPER_INDEX.csv", "paper G10 revised"))
cross = rd("COMPONENT_CROSSWALK.csv")
for c in cross:
    if c["paper"] == "G10": c.update(baseline_sha256=sha(os.path.join(OUT, PART10)), pages=str(n10), change="first issued with edition Z4; revised in editions Z5 to Z10")
wcsv("COMPONENT_CROSSWALK.csv", cross); changes.append(("changed", "PROGRAM/registers/COMPONENT_CROSSWALK.csv", "G10 digest"))
ready = rd("READINESS.csv")
for r in ready:
    if r["paper"] == "G10": r.update(pages=str(n10), labelled_statements="13", gaps="first issued with edition Z4; revised in editions Z5 (Theorem 5.3), Z6 (Lemma 5.4, Theorem 5.5), Z7 (Proposition 5.6; a summary sentence corrected after Director G), Z8 (Corollary 5.7; a sentence corrected at the request of Director G), Z9 (Theorem 5.8) and Z10 (Theorem 5.8 restated for any finite abelian group and any degree after a defect of its hypothesis; Corollary 5.9). Proposition 4.1 and Theorems 5.1 to 5.3 were read by Director G (Codex), who reports that they hold within their hypotheses. Theorem 5.8 and Corollary 5.9 were examined by a challenger sub-agent of the same model family, which found four omissions in the corollary, corrected, and no counterexample. The recursion of Theorem 5.1 and Lemma 5.4 with integer values are checked in Lean 4. The other statements after Theorem 5.3 have been read by their author only. Equation (7.1) is heuristic; the reference to Li and So was not inspected (OP-30)")
wcsv("READINESS.csv", ready); changes.append(("changed", "PROGRAM/registers/READINESS.csv", "paper G10 revised"))
ops = rd("OPEN_PROBLEMS.csv")
AM = {"OP-21": " Edition Z10: the classification of consistent pair rules holds for every finite abelian gain group and every degree: the consistent kernels are the combinations of the characters for which the step is norm-preserving (G10-01-12, restated; G10-01-13 for degree two). That -1 acts as -1 is special to degree two; in degree three with gains in the sixth roots of unity the consistent characters are those faithful on the cube root, and the sign character is excluded. Director G (pull request 2, commit 6bb2d14) prepares, from two localized sheet registers on one coherent base path with selectable gains, a prescribed relation r = u s between their characters, exactly at prime order with probability 2p/8^p, and verifies it by a dark setting; a tagged reference on one register transfers to the other; the absolute embedding stays unidentified. Director Z confirmed the sheet-operator statements in exact integers. In the terms of G10 the gain switches are a layered carrier with a supplied schedule (Director Z) or a spatial arrangement of gains on a ring (Director G); neither is derived. Open: a reason for such a carrier; faithfulness; the absolute character.",
      "OP-23": " Edition Z10: Director G (commit 6bb2d14) obtains a joint law for successive coherent coarse position readings of one prepared walker: the interpolated record tends weakly to an equal mixture of the two Newtonian tracks, the first separated reading heralding the branch, also through a field reversal. Director Z followed the sequential-projection inequality and its use without finding a gap and reproduced the adverse finite reversal control at two smaller scales (limit words 0.248 and 0.289), explained by the momentum offset of the preparation; with the field sign quartered during the preparation the centres lie within 2.5 and 0.8 percent of the limit rays in two runs. The bound of the theorem is of order delta^(1/32). Conditional on a supplied pointer that records a bin, the direction instrument, the readout, a sheet plane, gains of growing order and an externally set clock.",
      "OP-24": " Edition Z10: Director G merged the branch of the fourth Director Z session into the default branch (merge commit 37efa56) on the principal's authorization. Third cross-review of Director G by Director Z (ten predicates in three programs, all met; two checkers rerun). First use of sub-agents in a Director Z session: a challenger on G10 Theorem 5.8 and Corollary 5.9 found four omissions in the corollary and no counterexample; a second wrote Lean 4 proofs of the recursion of G10 Theorem 5.1 and of G10 Lemma 5.4 with integer values, rechecked in the session. Both are of the participant's model family; reduced exposure, not independence. A defect of the hypothesis of Theorem 5.8 as printed in edition Z9 was found by the participant and corrected.",
      "OP-30": " Edition Z10: for pair rules the classification is complete for every degree and every finite abelian gain group under the hypothesis on quotients (G10-01-12). Open: rules of the record-sum form in degrees above two; carriers on which the hypothesis fails; non-abelian gain groups; rules that are neither pair rules nor of the record-sum form; infinite vertex sets were not examined by the challenger."}
for r in ops:
    if r["id"] in AM: r["statement"] += AM[r["id"]]
assert sum(1 for r in ops if r["id"] in AM) == 4
wcsv("OPEN_PROBLEMS.csv", ops); changes.append(("changed", "PROGRAM/registers/OPEN_PROBLEMS.csv", "OP-21, OP-23, OP-24 and OP-30 amended"))
bp = os.path.join(REG, "BRIDGE_CANDIDATE_REGISTER.json"); br = json.load(open(bp)); k = 0
br["author"] += "; statements of edition Z10 marked Director G (Codex) follow the supplements on relative sheet transport and sequential position records, pull request 2, commit 6bb2d14"
for e in br["edges"]:
    if e["statement"].startswith("Consistency on history events forces the order of the rule and does not select the embedding"):
        e["statement"] += " Edition Z10: for every finite abelian gain group and every degree the consistent pair rules are the mixtures over the characters for which the step is norm-preserving (G10-01-12, G10-01-13). Director G: a relation between the characters of two sheet registers can be prepared and verified natively on a carrier with selectable gains; the absolute character cannot."; e["locator"] += "; G10-01-13; Director G, Relative_sheet_transport.md"; k += 1
    if e["statement"].startswith("Signed line walk under a linear gain, prepared by a coherent projection on the direction"):
        e["statement"] += " Edition Z10: for successive coherent coarse position readings the interpolated record tends weakly to an equal mixture of the two Newtonian tracks (Director G, Sequential_position_records.md, commit 6bb2d14); read and checked at finite scales by Director Z; needs a supplied pointer and clock."; k += 1
assert k == 2
br["retained_outliers"]["reversal_control_mass_of_limit_words_at_delta_0p1_and_0p05"] = [0.24830311498196259, 0.289066365500153]
br["retained_outliers"]["two_register_carriers_with_hypothesis_first_follow_up_of_12"] = 1
json.dump(br, open(bp, "w"), indent=1, ensure_ascii=False); changes.append(("changed", "PROGRAM/registers/BRIDGE_CANDIDATE_REGISTER.json", "two edges amended; two retained values added"))
gp = os.path.join(REG, "ONTOLOGY_GATE_MAP.json"); gm = json.load(open(gp)); gm["edition"] = NEW; k = 0
for g in gm["gates"]:
    if g["id"] == "P5": g["evidence"] += " Edition Z10: the classification of consistent pair rules is general: for any finite abelian gain group and any degree they are the mixtures over the characters for which the step is norm-preserving (G10-01-12); examined by a challenger sub-agent without a counterexample."; k += 1
    if g["id"] == "P6": g["evidence"] += " Edition Z10: Director G prepares and verifies a relation between the characters of two sheet registers natively on a carrier with selectable gains and a shared base path; a tagged reference transfers; the absolute character is not identified."; k += 1
    if g["id"] == "P9": g["evidence"] += " Edition Z10: Director G obtains a joint law of successive coarse position readings converging to an equal mixture of two Newtonian tracks, with a supplied pointer and clock; the bound is of order delta^(1/32); finite controls are adverse and are explained by the preparation offset (Director Z)."; k += 1
assert k == 3
json.dump(gm, open(gp, "w"), indent=1, ensure_ascii=False); changes.append(("changed", "PROGRAM/registers/ONTOLOGY_GATE_MAP.json", "evidence of P5, P6 and P9 amended; no state changed"))
dp = os.path.join(OUT, "PROGRAM", "figures", "Gate_Map_2026-11-13.dot"); dot = open(dp).read(); assert "edition Z9, 13 November 2026" in dot and "Editions Z4 to Z9 change evidence" in dot
open(dp, "w").write(dot.replace("edition Z9, 13 November 2026", "edition Z10, 13 November 2026").replace("Editions Z4 to Z9 change evidence", "Editions Z4 to Z10 change evidence")); changes.append(("changed", "PROGRAM/figures/Gate_Map_2026-11-13.dot", "edition label"))
subprocess.run(["dot", "-Tpdf", dp, "-o", dp[:-4] + ".pdf"], check=True); changes.append(("changed", "PROGRAM/figures/Gate_Map_2026-11-13.pdf", "edition label"))
HDR = (OLD + ", 13 November 2026", NEW + ", 13 November 2026")
edit("CONSTRUCTED_TRIALS/README.md", [HDR,
  ("and faithfulness is supplied (derived) | G8 Proposition 8.1; G10 Theorem 5.5, Proposition 5.6, Corollary 5.7, Theorem 5.8 |", "and faithfulness is supplied (derived); for any finite abelian group and any degree the consistent pair rules are the mixtures over the characters for which the step is norm-preserving (derived) | G8 Proposition 8.1; G10 Theorem 5.5, Proposition 5.6, Corollary 5.7, Theorem 5.8, Corollary 5.9 |")], "edition identifier; GH-1 ledger")
p = os.path.join(OUT, "CONSTRUCTED_TRIALS", "GH-1", "GH-1_Assumptions_and_Dispositions.json"); d = json.load(open(p))
d["derived"].append(dict(id="G10-01-13", text="degree two: consistent kernels change sign under the element of the block relation; G10-01-12 restated for any finite abelian group and any degree")); d["revised"] = "2026-11-13, edition Z10"
json.dump(d, open(p, "w"), indent=1, ensure_ascii=False); changes.append(("changed", "CONSTRUCTED_TRIALS/GH-1/GH-1_Assumptions_and_Dispositions.json", "GH-1 ledger amended"))
S4 = "REVIEW_RECORDS/Director_Z/Session_4/"
for dp_, _, fs_ in os.walk(os.path.join(SRC, "rec")):
    for f in sorted(fs_):
        rel_ = os.path.relpath(os.path.join(dp_, f), os.path.join(SRC, "rec")); put(os.path.join(dp_, f), S4 + rel_, "sixth addendum to the fourth-session record")
if PCP:
    put(os.path.join(PCP, "register.jsonl"), S4 + "register/register.jsonl", "register of the fourth session, extended by review Z10")
    nev = len(open(os.path.join(PCP, "register.jsonl")).read().strip().split("\n"))
    import re
    p4 = os.path.join(OUT, S4 + "README_SESSION_4.md"); t = open(p4).read(); m = re.search(r"The register: .*?present chain\)\.", t, re.S); assert m
    t = t.replace(m.group(0), "The register: %d events; head digest of the chain `%s`; SHA-256 of the file `%s` (edition Z10; the heads of editions Z4 to Z9 were `ea97886d0cc8dcd7aba4d95f9844cc8c95f312e56c4796f8da0d5123e1b250d8`, `d79915e5eb5a24959bc14dd7d73a0c7567a5543bebc692eefe2ffc57410a49e6`, `6e5fe34345615733380f6e4fbc4588b9dd63e79e76a91cf5cbb8de893b48fec5`, `f1c45a743b49e74ae70e22839fc1d9fa6edfcde87f4dcb8dfc7bd0e1b2b8011b`, `1adafcd57fccabe28b8e7109a3f15e7428a941a2bb8e14ee1e999da6fbdac4e2` and `02fec5108f968ec623e238ea11833f042cde4fcbe4413eef8ba18da9b31efdcb`, events 36, 52, 67, 93, 116 and 145 of the present chain)." % (nev, os.environ.get("PCP_HEAD", "see pcpos verify"), sha(os.path.join(PCP, "register.jsonl"))))
    a_ = "findings Z-072 to Z-076 |"; assert a_ in t
    t = t.replace(a_, a_ + "\n| `ADDENDUM_EDITION_Z10.md`, `NEW_Z_SCOPED_FINDINGS_SESSION_4_ADDENDUM_6.csv`, `challenger/`, seven further files in `cross_review/` | the sixth addendum: Theorem 5.8 of paper G10 in general form and Corollary 5.9, the report and programs of a challenger sub-agent, the Lean proofs in `COMPUTATION/Lean/`, and the cross-review of Director G's papers on relative sheet transport and sequential position records; findings Z-077 to Z-082 |").replace("`CHANGES_Z7_TO_Z8.md`, `CHANGES_Z8_TO_Z9.md`", "`CHANGES_Z7_TO_Z8.md`, `CHANGES_Z8_TO_Z9.md`, `CHANGES_Z9_TO_Z10.md`")
    assert "CHANGES_Z9_TO_Z10.md" in t
    open(p4, "w").write(t); changes.append(("changed", S4 + "README_SESSION_4.md", "register digests; sixth addendum listed"))
for rel in ("PROGRAM/CONTRIBUTIONS.md", "PROGRAM/PAPER_INDEX.md", "PROGRAM/STANDARDS.md", "PROGRAM/CHARTER.md", "REVIEW_RECORDS/README.md", "README.md", "LEGACY/README.md", "NEGATIVE_CONTROLS/README.md"):
    extra = []
    if rel == "PROGRAM/PAPER_INDEX.md": extra = [(f"| G10 | {T10} | article | {old_pages} | {old_statements} |", f"| G10 | {T10} | article | {n10} | 13 |")]
    if rel == "README.md": extra = [(f"({637 + old_pages} assembled pages;", f"({637 + n10} assembled pages;"), (f"theorem registry ({len(reg) - 1} rows)", f"theorem registry ({len(reg)} rows)")]
    if rel == "REVIEW_RECORDS/README.md": extra = [("(commits b626c0d, 00b8e26 and d4f6fea)", "(commits b626c0d, 00b8e26, d4f6fea and 6bb2d14)"), ("the cross-review of four of their results is in", "the cross-review of six of their results is in")]
    if rel == "PROGRAM/CONTRIBUTIONS.md": extra = [("and the preparation of a base packet with its two-ray limit (commit d4f6fea).", "the preparation of a base packet with its two-ray limit (commit d4f6fea), and relative sheet transport and sequential position records (commit 6bb2d14); merged the fourth Director Z session into the default branch.")]
    edit(rel, [HDR] + extra, "edition identifier" + ("; paper G10 revised" if extra else ""))
shutil.copy(os.path.abspath(__file__), os.path.join(OUT, "tools", "director_z_update_10.py")); changes.append(("added", "tools/director_z_update_10.py", "the program that applied these changes"))
changes.append(("added", S4 + "CHANGES_Z9_TO_Z10.md", "this list")); changes.append(("changed", "MANIFEST.json", "edition identifier, digests"))
with open(os.path.join(OUT, S4, "CHANGES_Z9_TO_Z10.md"), "w") as f:
    f.write("# Changes from edition Z9 to edition Z10\n\n13 November 2026. Every other file is byte-identical to edition Z9.\n\n| Change | File | Reason |\n|---|---|---|\n")
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
print("edition Z10:", len(files), "files;", len(reg), "registry rows;", n10, "pages in G10;", len(changes), "changes")



