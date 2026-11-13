#!/usr/bin/env python3
"""Apply the fifth addendum of the fourth Director Z session (13 November 2026) to a copy of edition Z8, giving edition Z9:
paper G10 revised (Theorem 5.8 added), two programs, the second addendum to the cross-review of Director G, register amendments.
Arguments: build directory (g10, comp, rec), copy of edition Z8, optional directory holding the session register (.pcp).
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
OLD, NEW = "FPHPM-BASELINE-2026-11-13-Z8", "FPHPM-BASELINE-2026-11-13-Z9"
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
rr = os.path.join(OUT, "COMPUTATION", "RERUN_RECORD_2026-11-12.csv")
with open(rr, newline="") as f: rows = list(csv.DictReader(f))
R = lambda p, n: dict(program=p, status="RAN_OK", stored_output_compared="yes", stdout_equals_stored="result file byte-identical", note=n)
X = "REVIEW_RECORDS/Director_Z/Session_4/cross_review/"
rows += [R("Baseline_Additions/verify_kernel_rules.py (fresh directory)", "4 predicates, 3 failed and kept; added in edition Z9"),
         R("Baseline_Additions/verify_kernel_rules_followup.py (fresh directory)", "3 predicates; added in edition Z9"),
         R(X + "crosscheck_director_g_two_rays.py (fresh directory)", "5 predicates, 1 failed and kept; added in edition Z9"),
         R(X + "crosscheck_director_g_two_rays_followup.py (fresh directory)", "3 predicates; added in edition Z9"),
         R(X + "crosscheck_director_g_sheet_filter_cost.py (fresh directory)", "3 predicates; added in edition Z9"),
         dict(program="Director G, pull request 2, commit d4f6fea: check_band_preparation.py rerun", status="RAN_OK", stored_output_compared="yes", stdout_equals_stored="six checks true; 1300 flight rows within 2.7e-13; 107 numbers of the report differ by at most 1.3e-15", note="reproduction on Linux of results recorded on Windows; rerun for edition Z9")]
wcsv(rr, rows); changes.append(("changed", "COMPUTATION/RERUN_RECORD_2026-11-12.csv", "six rows appended"))
reg = rd("THEOREM_REGISTRY.csv")
NEWST = [("G10-01-12", "Theorem", "5.8", "A switching-invariant pair rule is consistent under continuation exactly when its kernel changes sign under -1; the consistent kernels are the combinations of the characters in which -1 acts as -1")]
labels = [f"{r['kind']} {r['number']}" for r in reg if r["paper"] == "G10"] + [f"{k} {n}" for _, k, n, _ in NEWST]
n10, pg = pages_of(PDF10, labels)
for r in reg:
    if r["paper"] == "G10": r["paper_file_page"] = r["part_page"] = str(pg[f"{r['kind']} {r['number']}"])
for i_, k, num, name in NEWST:
    reg.append(dict(id=i_, paper="G10", part="1", part_title=T10, kind=k, number=num, name=name, status="PROOF_IN_MANUSCRIPT", paper_file_page=str(pg[f"{k} {num}"]), part_page=str(pg[f"{k} {num}"]), legacy_locator=""))
wcsv("THEOREM_REGISTRY.csv", reg); changes.append(("changed", "PROGRAM/registers/THEOREM_REGISTRY.csv", "G10 pages updated; row G10-01-12 added"))
old_statements = [r["statements"] for r in rd("PAPER_INDEX.csv") if r["id"] == "G10"][0]
index = rd("PAPER_INDEX.csv")
for r in index:
    if r["id"] == "G10": r.update(pages=str(n10), statements="12")
wcsv("PAPER_INDEX.csv", index); changes.append(("changed", "PROGRAM/registers/PAPER_INDEX.csv", "paper G10 revised"))
cross = rd("COMPONENT_CROSSWALK.csv")
for c in cross:
    if c["paper"] == "G10": c.update(baseline_sha256=sha(os.path.join(OUT, PART10)), pages=str(n10), change="first issued with edition Z4; revised in editions Z5, Z6, Z7, Z8 and Z9")
wcsv("COMPONENT_CROSSWALK.csv", cross); changes.append(("changed", "PROGRAM/registers/COMPONENT_CROSSWALK.csv", "G10 digest"))
ready = rd("READINESS.csv")
for r in ready:
    if r["paper"] == "G10": r.update(pages=str(n10), labelled_statements="12", gaps="first issued with edition Z4; revised in editions Z5 (Theorem 5.3), Z6 (Lemma 5.4, Theorem 5.5), Z7 (Proposition 5.6; a summary sentence corrected after Director G), Z8 (Corollary 5.7; the preparation in the five-sheet instance stated at the request of Director G) and Z9 (Theorem 5.8). Proposition 4.1 and Theorems 5.1 to 5.3 were read by Director G (Codex), who reports that they hold within their hypotheses; the later statements have been read by their author only. Equation (7.1) is heuristic; the reference to Li and So was not inspected (OP-30)")
wcsv("READINESS.csv", ready); changes.append(("changed", "PROGRAM/registers/READINESS.csv", "paper G10 revised"))
ops = rd("OPEN_PROBLEMS.csv")
AM = {"OP-21": " Edition Z9: without a choice of records beyond the end vertices, among the switching-invariant pair rules of G8 the consistent ones are exactly those whose kernel changes sign under -1: the combinations of the characters in which -1 acts as -1, a space of dimension ceil(q/4) (G10-01-12), unique only for the orders 2 and 4. The conjugate rules of G10-01-09 and the lift rule of G10-01-11 are two sections of this family. Scope of the edition Z7 statement: multiplicativity on products leaves one conjugate character among rules that are functions of the faithful amplitude; among pair rules it leaves one character in which -1 acts as -1, which need not be faithful. Faithfulness (that the whole group of gains acts) is therefore assumed and not obtained. Open, in addition to the items of edition Z8: a reason for faithfulness.",
      "OP-23": " Edition Z9: Director G (pull request 2, commit d4f6fea) shows that full site-and-direction readings leave the momentum density flat, and that a coherent projection on the direction with the sites unread, alternated every two steps, prepares a binomial packet at the two band edges; with the field on, in a stated scaling, the sheet-unresolved position law tends to equal point masses at -F t^2/2 and +F t^2/2. Director Z read the paper once, confirmed the preparation formulas to rounding in a model written for the purpose and found the limit consistent with real-space runs at five scales (masses differing by m h, centres on the ray with the preparation offset, convergence as delta^(1/2) and delta^(1/4)). Conditional on the direction instrument, a weak-field sheet plane, the squared-amplitude readout and gains of growing order; a position measurement at one time, not a joint law along a trajectory; no clock.",
      "OP-24": " Edition Z9: second cross-review of Director G by Director Z (the paper on the base preparation and two rays): eleven predicates in three programs, ten met, one failed through the reviewer's tolerance and kept; Director G's checker rerun with all six checks true. Two additions to the paper: sharper rates for the filter comparison, and a count of the cost of the assumed sheet preparation. The sheet version, the cutoffs in full rigour and the external articles were not checked. Not independent replication.",
      "OP-28": " Edition Z9: Director G's two-ray limit uses the field pi/M with the sheet order M = pi/(F delta^4) growing, as the exact translation of G10-01-05 requires; it does not concern gains of bounded order. Cost of the sheet plane it assumes, for the five-sheet word extended to M sheets (Director Z): about 0.202 M^2 records for residual 0.01 with joint probability near 2^(-s); for every instrument that leaves the sheets unread the probability is at most 2/(M(1 - eta)). Open: a native word near that bound.",
      "OP-30": " Edition Z9: one class outside the record-sum form is now classified, the pair rules with a kernel (G10-01-12); there the pair form, hence the second order, is assumed. Open as before: carriers on which the hypotheses on blocks fail (12 of 40 random carriers in the follow-up computation, each with a larger space of consistent kernels); degrees above two; rules that are neither pair rules nor of the record-sum form."}
for r in ops:
    if r["id"] in AM: r["statement"] += AM[r["id"]]
assert sum(1 for r in ops if r["id"] in AM) == 5
wcsv("OPEN_PROBLEMS.csv", ops); changes.append(("changed", "PROGRAM/registers/OPEN_PROBLEMS.csv", "OP-21, OP-23, OP-24, OP-28 and OP-30 amended"))
bp = os.path.join(REG, "BRIDGE_CANDIDATE_REGISTER.json"); br = json.load(open(bp)); k = 0
br["author"] += "; the edge of edition Z9 marked Director G (Codex) follows the supplement on the base preparation and two rays, pull request 2, commit d4f6fea"
for e in br["edges"]:
    if e["statement"].startswith("Consistency on history events forces the order of the rule and does not select the embedding"):
        e["statement"] += " Edition Z9: among switching-invariant pair rules, with no choice of records, the consistent ones are exactly those whose kernel changes sign under -1 (G10-01-12); composition then leaves one character in which -1 acts as -1, not necessarily faithful."; e["locator"] += "; G10-01-12"; k += 1
assert k == 1
br["edges"].append({"from": "PRE-ARC", "to": "CM-SYMP", "type": "exact_correspondence", "statement": "Signed line walk under a linear gain, prepared by a coherent projection on the direction with the sites unread, alternated every two steps: in the scaling eps = delta, h = F delta^4, about delta^(-5/2) blocks, the sheet-unresolved position law at scaled time t tends to equal point masses at -F t^2/2 and +F t^2/2, the two band curvatures at the two edges. Full site-and-direction readings cannot prepare the packet (flat momentum density).", "locator": "Director G (Codex), Base_preparation_and_two_rays.md, pull request 2, commit d4f6fea; cross-check: REVIEW_RECORDS/Director_Z/Session_4/cross_review/CROSS_REVIEW_OF_DIRECTOR_G_TWO_RAYS_ADDENDUM.md", "status": "Director G record; read once and checked by real-space runs at five scales by Director Z; unrefereed; conditional on the direction instrument, a weak-field sheet plane, the readout and gains of growing order; a law at one time, not a trajectory"})
br["retained_outliers"]["two_ray_mass_of_positive_half_at_delta_0p2"] = 0.5437860483779331
br["retained_outliers"]["kernel_rule_first_run_predicates_failed_of_4"] = 3
json.dump(br, open(bp, "w"), indent=1, ensure_ascii=False); changes.append(("changed", "PROGRAM/registers/BRIDGE_CANDIDATE_REGISTER.json", "one edge amended; one edge and two retained values added"))
gp = os.path.join(REG, "ONTOLOGY_GATE_MAP.json"); gm = json.load(open(gp)); gm["edition"] = NEW; k = 0
for g in gm["gates"]:
    if g["id"] == "P5": g["evidence"] += " Edition Z9: among the switching-invariant pair rules the consistent ones are exactly those whose kernel changes sign under -1, the mixtures of the characters in which -1 acts as -1 (G10-01-12); the even characters, the coincidence count on the base among them, are excluded. Unique only for the orders 2 and 4."; k += 1
    if g["id"] == "P6": g["evidence"] += " Edition Z9: among pair rules, multiplicativity on products leaves one character in which -1 acts as -1; it does not make the character faithful (G10-01-12)."; k += 1
    if g["id"] == "P9": g["evidence"] += " Edition Z9: Director G prepares, by a coherent direction projection, a packet at the two band edges and obtains in a scaling limit equal point masses at the two Newtonian positions of opposite curvature; consistent with real-space runs of Director Z at five scales. Conditional on the instrument, a weak-field sheet plane, the readout and gains of growing order; the native cost of the sheet plane is exponential in the square of the sheet order for the instrument examined."; k += 1
    if g["id"] == "P10": g["evidence"] += " Edition Z9: faithfulness of the character is a further assumption: neither consistency nor composition yields it among pair rules (G10-01-12)."; k += 1
assert k == 4
json.dump(gm, open(gp, "w"), indent=1, ensure_ascii=False); changes.append(("changed", "PROGRAM/registers/ONTOLOGY_GATE_MAP.json", "evidence of P5, P6, P9 and P10 amended; no state changed"))
dp = os.path.join(OUT, "PROGRAM", "figures", "Gate_Map_2026-11-13.dot"); dot = open(dp).read(); assert "edition Z8, 13 November 2026" in dot and "Editions Z4 to Z8 change evidence" in dot
open(dp, "w").write(dot.replace("edition Z8, 13 November 2026", "edition Z9, 13 November 2026").replace("Editions Z4 to Z8 change evidence", "Editions Z4 to Z9 change evidence")); changes.append(("changed", "PROGRAM/figures/Gate_Map_2026-11-13.dot", "edition label"))
subprocess.run(["dot", "-Tpdf", dp, "-o", dp[:-4] + ".pdf"], check=True); changes.append(("changed", "PROGRAM/figures/Gate_Map_2026-11-13.pdf", "edition label"))
HDR = (OLD + ", 13 November 2026", NEW + ", 13 November 2026")
edit("CONSTRUCTED_TRIALS/README.md", [HDR,
  ("(derived; whether the gain is a record is supplied) | G8 Proposition 8.1; G10 Theorem 5.5, Proposition 5.6, Corollary 5.7 |", "(derived; whether the gain is a record is supplied); among pair rules with a kernel the consistent ones are the mixtures of the characters in which -1 acts as -1, and faithfulness is supplied (derived) | G8 Proposition 8.1; G10 Theorem 5.5, Proposition 5.6, Corollary 5.7, Theorem 5.8 |")], "edition identifier; GH-1 ledger")
p = os.path.join(OUT, "CONSTRUCTED_TRIALS", "GH-1", "GH-1_Assumptions_and_Dispositions.json"); d = json.load(open(p))
d["derived"].append(dict(id="G10-01-12", text="pair rules with a kernel: consistent exactly when the kernel changes sign under -1; mixtures of the characters in which -1 acts as -1")); d["revised"] = "2026-11-13, edition Z9"
a1 = [a for a in d["assumptions"] if a["id"] == "GH1-A1"][0]; a1["note"] += "; edition Z9: within pair rules consistency excludes the characters in which -1 acts trivially and leaves the others; faithfulness of the character is not obtained (G10 Theorem 5.8)"
json.dump(d, open(p, "w"), indent=1, ensure_ascii=False); changes.append(("changed", "CONSTRUCTED_TRIALS/GH-1/GH-1_Assumptions_and_Dispositions.json", "GH-1 ledger amended"))
S4 = "REVIEW_RECORDS/Director_Z/Session_4/"
for dp_, _, fs_ in os.walk(os.path.join(SRC, "rec")):
    for f in sorted(fs_):
        rel_ = os.path.relpath(os.path.join(dp_, f), os.path.join(SRC, "rec")); put(os.path.join(dp_, f), S4 + rel_, "fifth addendum to the fourth-session record")
if PCP:
    put(os.path.join(PCP, "register.jsonl"), S4 + "register/register.jsonl", "register of the fourth session, extended by review Z9")
    nev = len(open(os.path.join(PCP, "register.jsonl")).read().strip().split("\n"))
    import re
    p4 = os.path.join(OUT, S4 + "README_SESSION_4.md"); t = open(p4).read(); m = re.search(r"The register: .*?present chain\)\.", t, re.S); assert m
    t = t.replace(m.group(0), "The register: %d events; head digest of the chain `%s`; SHA-256 of the file `%s` (edition Z9; the heads of editions Z4 to Z8 were `ea97886d0cc8dcd7aba4d95f9844cc8c95f312e56c4796f8da0d5123e1b250d8`, `d79915e5eb5a24959bc14dd7d73a0c7567a5543bebc692eefe2ffc57410a49e6`, `6e5fe34345615733380f6e4fbc4588b9dd63e79e76a91cf5cbb8de893b48fec5`, `f1c45a743b49e74ae70e22839fc1d9fa6edfcde87f4dcb8dfc7bd0e1b2b8011b` and `1adafcd57fccabe28b8e7109a3f15e7428a941a2bb8e14ee1e999da6fbdac4e2`, events 36, 52, 67, 93 and 116 of the present chain)." % (nev, os.environ.get("PCP_HEAD", "see pcpos verify"), sha(os.path.join(PCP, "register.jsonl"))))
    a_ = "findings Z-067 to Z-071 |"; assert a_ in t
    t = t.replace(a_, a_ + "\n| `ADDENDUM_EDITION_Z9.md`, `NEW_Z_SCOPED_FINDINGS_SESSION_4_ADDENDUM_5.csv`, seven further files in `cross_review/` | the fifth addendum: Theorem 5.8 of paper G10 (which pair rules are consistent), a scope note on the edition Z7 statement about composition, and the cross-review of Director G's paper on the base preparation and two rays with three programs and their result files; findings Z-072 to Z-076 |").replace("`CHANGES_Z6_TO_Z7.md`, `CHANGES_Z7_TO_Z8.md`", "`CHANGES_Z6_TO_Z7.md`, `CHANGES_Z7_TO_Z8.md`, `CHANGES_Z8_TO_Z9.md`")
    assert "CHANGES_Z8_TO_Z9.md" in t
    open(p4, "w").write(t); changes.append(("changed", S4 + "README_SESSION_4.md", "register digests; fifth addendum listed"))
for rel in ("PROGRAM/CONTRIBUTIONS.md", "PROGRAM/PAPER_INDEX.md", "PROGRAM/STANDARDS.md", "PROGRAM/CHARTER.md", "REVIEW_RECORDS/README.md", "README.md", "LEGACY/README.md", "NEGATIVE_CONTROLS/README.md"):
    extra = []
    if rel == "PROGRAM/PAPER_INDEX.md": extra = [(f"| G10 | {T10} | article | {old_pages} | {old_statements} |", f"| G10 | {T10} | article | {n10} | 12 |")]
    if rel == "README.md": extra = [(f"({637 + old_pages} assembled pages;", f"({637 + n10} assembled pages;"), (f"theorem registry ({len(reg) - 1} rows)", f"theorem registry ({len(reg)} rows)")]
    if rel == "REVIEW_RECORDS/README.md": extra = [("(commits b626c0d and 00b8e26)", "(commits b626c0d, 00b8e26 and d4f6fea)"), ("the cross-review of two of their results is in", "the cross-review of four of their results is in")]
    if rel == "PROGRAM/CONTRIBUTIONS.md": extra = [("and the correction of the five-sheet sentence of G10 Section 5.3.", "the correction of the five-sheet sentence of G10 Section 5.3, and the preparation of a base packet with its two-ray limit (commit d4f6fea).")]
    edit(rel, [HDR] + extra, "edition identifier" + ("; paper G10 revised" if extra else ""))
shutil.copy(os.path.abspath(__file__), os.path.join(OUT, "tools", "director_z_update_9.py")); changes.append(("added", "tools/director_z_update_9.py", "the program that applied these changes"))
changes.append(("added", S4 + "CHANGES_Z8_TO_Z9.md", "this list")); changes.append(("changed", "MANIFEST.json", "edition identifier, digests"))
with open(os.path.join(OUT, S4, "CHANGES_Z8_TO_Z9.md"), "w") as f:
    f.write("# Changes from edition Z8 to edition Z9\n\n13 November 2026. Every other file is byte-identical to edition Z8.\n\n| Change | File | Reason |\n|---|---|---|\n")
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
print("edition Z9:", len(files), "files;", len(reg), "registry rows;", n10, "pages in G10;", len(changes), "changes")


