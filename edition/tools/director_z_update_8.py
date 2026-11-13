#!/usr/bin/env python3
"""Apply the fourth addendum of the fourth Director Z session (13 November 2026) to a copy of edition Z7, giving edition Z8:
paper G10 revised (Corollary 5.7 added; one sentence corrected at the request of Director G), one program, the addendum to the
cross-review of Director G, register amendments.
Arguments: build directory (g10, comp, rec), copy of edition Z7, optional directory holding the session register (.pcp).
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
OLD, NEW = "FPHPM-BASELINE-2026-11-13-Z7", "FPHPM-BASELINE-2026-11-13-Z8"
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
for f in sorted(os.listdir(os.path.join(SRC, "comp"))): put(os.path.join(SRC, "comp", f), ba + f, "computation cited by paper G10 (Corollary 5.7)")
rr = os.path.join(OUT, "COMPUTATION", "RERUN_RECORD_2026-11-12.csv")
with open(rr, newline="") as f: rows = list(csv.DictReader(f))
R = lambda p, n: dict(program=p, status="RAN_OK", stored_output_compared="yes", stdout_equals_stored="result file byte-identical", note=n)
rows += [R("Baseline_Additions/verify_signed_lift_rule.py (fresh directory)", "5 predicates; added in edition Z8"),
         R("REVIEW_RECORDS/Director_Z/Session_4/cross_review/crosscheck_director_g_native.py (fresh directory)", "5 predicates, exact arithmetic; added in edition Z8")]
wcsv(rr, rows); changes.append(("changed", "COMPUTATION/RERUN_RECORD_2026-11-12.csv", "two rows appended"))
reg = rd("THEOREM_REGISTRY.csv")
NEWST = [("G10-01-11", "Corollary", "5.7", "On the signed lift the consistent rule of the record-sum form is unique, the square of the integer amplitude; it is the equal-weight mean of the squared-modulus rules over the characters in which -1 acts as -1")]
labels = [f"{r['kind']} {r['number']}" for r in reg if r["paper"] == "G10"] + [f"{k} {n}" for _, k, n, _ in NEWST]
n10, pg = pages_of(PDF10, labels)
for r in reg:
    if r["paper"] == "G10": r["paper_file_page"] = r["part_page"] = str(pg[f"{r['kind']} {r['number']}"])
for i_, k, num, name in NEWST:
    reg.append(dict(id=i_, paper="G10", part="1", part_title=T10, kind=k, number=num, name=name, status="PROOF_IN_MANUSCRIPT", paper_file_page=str(pg[f"{k} {num}"]), part_page=str(pg[f"{k} {num}"]), legacy_locator=""))
wcsv("THEOREM_REGISTRY.csv", reg); changes.append(("changed", "PROGRAM/registers/THEOREM_REGISTRY.csv", "G10 pages updated; row G10-01-11 added"))
old_statements = [r["statements"] for r in rd("PAPER_INDEX.csv") if r["id"] == "G10"][0]
index = rd("PAPER_INDEX.csv")
for r in index:
    if r["id"] == "G10": r.update(pages=str(n10), statements="11")
wcsv("PAPER_INDEX.csv", index); changes.append(("changed", "PROGRAM/registers/PAPER_INDEX.csv", "paper G10 revised"))
cross = rd("COMPONENT_CROSSWALK.csv")
for c in cross:
    if c["paper"] == "G10": c.update(baseline_sha256=sha(os.path.join(OUT, PART10)), pages=str(n10), change="first issued with edition Z4; revised in editions Z5, Z6, Z7 and Z8")
wcsv("COMPONENT_CROSSWALK.csv", cross); changes.append(("changed", "PROGRAM/registers/COMPONENT_CROSSWALK.csv", "G10 digest"))
ready = rd("READINESS.csv")
for r in ready:
    if r["paper"] == "G10": r.update(pages=str(n10), labelled_statements="11", gaps="first issued with edition Z4; revised in editions Z5 (Theorem 5.3), Z6 (Lemma 5.4, Theorem 5.5), Z7 (Proposition 5.6; a summary sentence corrected after Director G) and Z8 (Corollary 5.7; the preparation in the five-sheet instance stated at the request of Director G). Proposition 4.1 and Theorems 5.1 to 5.3 were read by Director G (Codex), who reports that they hold within their hypotheses; the later statements have been read by their author only. Equation (7.1) is heuristic; the reference to Li and So was not inspected (OP-30)")
wcsv("READINESS.csv", ready); changes.append(("changed", "PROGRAM/registers/READINESS.csv", "paper G10 revised"))
ops = rd("OPEN_PROBLEMS.csv")
AM = {"OP-21": " Edition Z8: the obligation divides by an assumption about records. (a) If the gain of a walk is a record, the carrier is the signed lift (one sheet for each pair of opposite gains): the consistent rule of the record-sum form is unique for every even order, the square of the integer amplitude, equal to the equal-weight mean of the squared-modulus rules over the characters in which -1 acts as -1, faithful or not (G10-01-11). Nothing is then to be selected; no single-character rule is of the record-sum form for orders from 6 on, and a single character is not a system. Director G obtained first (pull request 2, commit 00b8e26), from other premises, that from a localized sheet every protocol of steps and coordinate records has the same rational law under each embedding law, and that an integer branch vector is not supported in one faithful plane when phi(h) > 2; a repeated native filter approaches (3 + sqrt 5)/16 under every embedding law, the laws differing only in the label of the selected plane. (b) If the gain is not a record, the edition Z7 statement stands: the choice among conjugate characters is not made by consistency, composition or native records. Open: a reason for or against the gain being a record; the warrant for an externally tagged character; whether a composite with a tagged system fixes a relative embedding (with Director G); records of the sheet modulo a divisor.",
      "OP-24": " Edition Z8: Director G pointed out that a sentence of G10 Section 5.3 in edition Z7 left the preparation of the five-sheet instance implicit; corrected. A statement of Director Z on the review thread (no real norm-preserving step of degree three) was wrong as a general statement and was withdrawn after a self-check of the citation; 1 + A is such a step for a skew signed A of degree two. Director Z read Director G's paper on native preparations once and confirmed five instances in exact arithmetic; the section on countably many rounds was not checked.",
      "OP-30": " Edition Z8: with the pairs of a vertex and a sheet as records, the form of the rule is the record-sum form on the signed lift and the rule is unique for every order (G10-01-11); the dependence of the classification on what counts as a record is thereby explicit. Open as before: carriers on which the growth hypothesis fails; degrees above two; rules outside the record-sum form."}
for r in ops:
    if r["id"] in AM: r["statement"] += AM[r["id"]]
assert sum(1 for r in ops if r["id"] in AM) == 3
wcsv("OPEN_PROBLEMS.csv", ops); changes.append(("changed", "PROGRAM/registers/OPEN_PROBLEMS.csv", "OP-21, OP-24 and OP-30 amended"))
bp = os.path.join(REG, "BRIDGE_CANDIDATE_REGISTER.json"); br = json.load(open(bp)); k = 0
br["author"] += "; entries of edition Z8 marked Director G (Codex) follow the supplement on native preparations, pull request 2, commit 00b8e26"
for e in br["edges"]:
    if e["statement"].startswith("Consistency on history events forces the order of the rule and does not select the embedding"):
        e["statement"] += " Edition Z8: if the gain of a walk is a record (signed lift) the rule is unique for every order and is the equal-weight mean over the characters in which -1 acts as -1 (G10-01-11); the choice of an embedding belongs to the reduction by a character. Director G: native records from a localized sheet have one rational law under every embedding law (obtained first)."; e["locator"] += "; G10-01-11; Director G, Native_preparations_and_probability_embeddings.md"; k += 1
assert k == 1
br["retained_outliers"]["signed_lifts_with_two_connected_components_of_30"] = 2
json.dump(br, open(bp, "w"), indent=1, ensure_ascii=False); changes.append(("changed", "PROGRAM/registers/BRIDGE_CANDIDATE_REGISTER.json", "one edge amended; one retained value added"))
gp = os.path.join(REG, "ONTOLOGY_GATE_MAP.json"); gm = json.load(open(gp)); gm["edition"] = NEW; k = 0
for g in gm["gates"]:
    if g["id"] == "P5": g["evidence"] += " Edition Z8: what counts as a record enters the rule. With the gain of a walk recorded (signed lift) the consistent record-sum rule is unique for every order and integer-valued (G10-01-11); with only the end vertex recorded the conjugate rules remain. Director G: every native protocol from a localized sheet has the same rational law under each embedding law."; k += 1
    if g["id"] == "P10": g["evidence"] += " Edition Z8: the selection of an embedding is required only after reduction by a character; on the signed lift the rule is real, unique and the mean over the characters (G10-01-11; Director G's native-preparation theorem, obtained first). Not obtained: a reason for or against the gain being a record, and a warrant for treating one character as a system."; k += 1
assert k == 2
json.dump(gm, open(gp, "w"), indent=1, ensure_ascii=False); changes.append(("changed", "PROGRAM/registers/ONTOLOGY_GATE_MAP.json", "evidence of P5 and P10 amended; no state changed"))
dp = os.path.join(OUT, "PROGRAM", "figures", "Gate_Map_2026-11-13.dot"); dot = open(dp).read(); assert "edition Z7, 13 November 2026" in dot and "Editions Z4 to Z7 change evidence" in dot
open(dp, "w").write(dot.replace("edition Z7, 13 November 2026", "edition Z8, 13 November 2026").replace("Editions Z4 to Z7 change evidence", "Editions Z4 to Z8 change evidence")); changes.append(("changed", "PROGRAM/figures/Gate_Map_2026-11-13.dot", "edition label"))
subprocess.run(["dot", "-Tpdf", dp, "-o", dp[:-4] + ".pdf"], check=True); changes.append(("changed", "PROGRAM/figures/Gate_Map_2026-11-13.pdf", "edition label"))
HDR = (OLD + ", 13 November 2026", NEW + ", 13 November 2026")
edit("CONSTRUCTED_TRIALS/README.md", [HDR,
  ("multiplicativity on products leaves one conjugate character (derived; Director G) | G8 Proposition 8.1; G10 Theorem 5.5, Proposition 5.6 |", "multiplicativity on products leaves one conjugate character (derived; Director G); if the gain of a walk is itself a record (signed lift) the rule is unique for every order and no character is chosen (derived; whether the gain is a record is supplied) | G8 Proposition 8.1; G10 Theorem 5.5, Proposition 5.6, Corollary 5.7 |")], "edition identifier; GH-1 ledger")
p = os.path.join(OUT, "CONSTRUCTED_TRIALS", "GH-1", "GH-1_Assumptions_and_Dispositions.json"); d = json.load(open(p))
d["derived"].append(dict(id="G10-01-11", text="signed lift: with the gain recorded the record-sum rule is unique for every order, the mean over the characters in which -1 acts as -1")); d["revised"] = "2026-11-13, edition Z8"
a1 = [a for a in d["assumptions"] if a["id"] == "GH1-A1"][0]; a1["note"] += "; edition Z8: which objects are records (end vertex only, or end vertex and gain) is part of this assumption and changes the classification (G10 Corollary 5.7)"
json.dump(d, open(p, "w"), indent=1, ensure_ascii=False); changes.append(("changed", "CONSTRUCTED_TRIALS/GH-1/GH-1_Assumptions_and_Dispositions.json", "GH-1 ledger amended"))
S4 = "REVIEW_RECORDS/Director_Z/Session_4/"
for dp_, _, fs_ in os.walk(os.path.join(SRC, "rec")):
    for f in sorted(fs_):
        rel_ = os.path.relpath(os.path.join(dp_, f), os.path.join(SRC, "rec")); put(os.path.join(dp_, f), S4 + rel_, "fourth addendum to the fourth-session record")
if PCP:
    put(os.path.join(PCP, "register.jsonl"), S4 + "register/register.jsonl", "register of the fourth session, extended by review Z8")
    nev = len(open(os.path.join(PCP, "register.jsonl")).read().strip().split("\n"))
    import re
    p4 = os.path.join(OUT, S4 + "README_SESSION_4.md"); t = open(p4).read(); m = re.search(r"The register: .*?present chain\)\.", t, re.S); assert m
    t = t.replace(m.group(0), "The register: %d events; head digest of the chain `%s`; SHA-256 of the file `%s` (edition Z8; the heads of editions Z4, Z5, Z6 and Z7 were `ea97886d0cc8dcd7aba4d95f9844cc8c95f312e56c4796f8da0d5123e1b250d8`, `d79915e5eb5a24959bc14dd7d73a0c7567a5543bebc692eefe2ffc57410a49e6`, `6e5fe34345615733380f6e4fbc4588b9dd63e79e76a91cf5cbb8de893b48fec5` and `f1c45a743b49e74ae70e22839fc1d9fa6edfcde87f4dcb8dfc7bd0e1b2b8011b`, events 36, 52, 67 and 93 of the present chain)." % (nev, os.environ.get("PCP_HEAD", "see pcpos verify"), sha(os.path.join(PCP, "register.jsonl"))))
    a_ = "findings Z-061 to Z-066 |"; assert a_ in t
    t = t.replace(a_, a_ + "\n| `ADDENDUM_EDITION_Z8.md`, `NEW_Z_SCOPED_FINDINGS_SESSION_4_ADDENDUM_4.csv`, three further files in `cross_review/` | the fourth addendum: Corollary 5.7 of paper G10 (the rule on the signed lift), a sentence corrected at the request of Director G, a statement on the review thread withdrawn, and the cross-review of Director G's paper on native preparations with its program and result file; findings Z-067 to Z-071 |").replace("`CHANGES_Z5_TO_Z6.md`, `CHANGES_Z6_TO_Z7.md`", "`CHANGES_Z5_TO_Z6.md`, `CHANGES_Z6_TO_Z7.md`, `CHANGES_Z7_TO_Z8.md`")
    assert "CHANGES_Z7_TO_Z8.md" in t
    open(p4, "w").write(t); changes.append(("changed", S4 + "README_SESSION_4.md", "register digests; fourth addendum listed"))
for rel in ("PROGRAM/CONTRIBUTIONS.md", "PROGRAM/PAPER_INDEX.md", "PROGRAM/STANDARDS.md", "PROGRAM/CHARTER.md", "REVIEW_RECORDS/README.md", "README.md", "LEGACY/README.md", "NEGATIVE_CONTROLS/README.md"):
    extra = []
    if rel == "PROGRAM/PAPER_INDEX.md": extra = [(f"| G10 | {T10} | article | {old_pages} | {old_statements} |", f"| G10 | {T10} | article | {n10} | 11 |")]
    if rel == "README.md": extra = [(f"({637 + old_pages} assembled pages;", f"({637 + n10} assembled pages;"), (f"theorem registry ({len(reg) - 1} rows)", f"theorem registry ({len(reg)} rows)")]
    if rel == "REVIEW_RECORDS/README.md": extra = [("the research supplements of Director G are in pull request 2 of the repository (commit b626c0d)", "the research supplements of Director G are in pull request 2 of the repository (commits b626c0d and 00b8e26)")]
    if rel == "PROGRAM/CONTRIBUTIONS.md": extra = [("and the classification of weights by field embeddings with which G10 Proposition 5.6 agrees.", "the classification of weights by field embeddings with which G10 Proposition 5.6 agrees, the law of native records from a localized sheet with which G10 Corollary 5.7 agrees, and the correction of the five-sheet sentence of G10 Section 5.3.")]
    edit(rel, [HDR] + extra, "edition identifier" + ("; paper G10 revised" if extra else ""))
shutil.copy(os.path.abspath(__file__), os.path.join(OUT, "tools", "director_z_update_8.py")); changes.append(("added", "tools/director_z_update_8.py", "the program that applied these changes"))
changes.append(("added", S4 + "CHANGES_Z7_TO_Z8.md", "this list")); changes.append(("changed", "MANIFEST.json", "edition identifier, digests"))
with open(os.path.join(OUT, S4, "CHANGES_Z7_TO_Z8.md"), "w") as f:
    f.write("# Changes from edition Z7 to edition Z8\n\n13 November 2026. Every other file is byte-identical to edition Z7.\n\n| Change | File | Reason |\n|---|---|---|\n")
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
print("edition Z8:", len(files), "files;", len(reg), "registry rows;", n10, "pages in G10;", len(changes), "changes")

