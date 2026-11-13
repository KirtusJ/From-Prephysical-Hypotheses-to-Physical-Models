#!/usr/bin/env python3
"""Apply the third addendum of the fourth Director Z session (13 November 2026) to a copy of edition Z6, giving edition Z7:
paper G10 revised (Proposition 5.6 added; corrections after the cross-reading of Director G), one program, the cross-review of
Director G's results, register amendments.
Arguments: build directory (g10, comp, rec), copy of edition Z6, optional directory holding the session register (.pcp).
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
OLD, NEW = "FPHPM-BASELINE-2026-11-13-Z6", "FPHPM-BASELINE-2026-11-13-Z7"
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
for f in sorted(os.listdir(os.path.join(SRC, "comp"))): put(os.path.join(SRC, "comp", f), ba + f, "computation cited by paper G10 (Proposition 5.6)")
rr = os.path.join(OUT, "COMPUTATION", "RERUN_RECORD_2026-11-12.csv")
with open(rr, newline="") as f: rows = list(csv.DictReader(f))
R = lambda p, n: dict(program=p, status="RAN_OK", stored_output_compared="yes", stdout_equals_stored="result file byte-identical", note=n)
rows += [R("Baseline_Additions/verify_composition_selects_one_character.py (fresh directory)", "4 predicates; added in edition Z7"),
         R("REVIEW_RECORDS/Director_Z/Session_4/cross_review/crosscheck_director_g.py (fresh directory)", "6 predicates; about ten minutes; added in edition Z7"),
         dict(program="Director G, pull request 2, commit b626c0d: four checkers rerun (check_walk, check_record_selection, check_probability_selection, check_forced_envelope)", status="RAN_OK", stored_output_compared="yes", stdout_equals_stored="two exact outputs identical apart from line endings; seven floating-point outputs differ by at most 1.5e-6 relative, no predicate changed", note="reproduction on Linux of results recorded on Windows; rerun for edition Z7")]
wcsv(rr, rows); changes.append(("changed", "COMPUTATION/RERUN_RECORD_2026-11-12.csv", "three rows appended"))
reg = rd("THEOREM_REGISTRY.csv")
NEWST = [("G10-01-10", "Proposition", "5.6", "Positivity confines the weights of the conjugate rules to a cone; multiplicativity on products selects the squared modulus in one conjugate character")]
labels = [f"{r['kind']} {r['number']}" for r in reg if r["paper"] == "G10"] + [f"{k} {n}" for _, k, n, _ in NEWST]
n10, pg = pages_of(PDF10, labels)
for r in reg:
    if r["paper"] == "G10": r["paper_file_page"] = r["part_page"] = str(pg[f"{r['kind']} {r['number']}"])
for i_, k, num, name in NEWST:
    reg.append(dict(id=i_, paper="G10", part="1", part_title=T10, kind=k, number=num, name=name, status="PROOF_IN_MANUSCRIPT", paper_file_page=str(pg[f"{k} {num}"]), part_page=str(pg[f"{k} {num}"]), legacy_locator=""))
wcsv("THEOREM_REGISTRY.csv", reg); changes.append(("changed", "PROGRAM/registers/THEOREM_REGISTRY.csv", "G10 pages updated; row G10-01-10 added"))
old_statements = [r["statements"] for r in rd("PAPER_INDEX.csv") if r["id"] == "G10"][0]
index = rd("PAPER_INDEX.csv")
for r in index:
    if r["id"] == "G10": r.update(pages=str(n10), statements="10")
wcsv("PAPER_INDEX.csv", index); changes.append(("changed", "PROGRAM/registers/PAPER_INDEX.csv", "paper G10 revised"))
cross = rd("COMPONENT_CROSSWALK.csv")
for c in cross:
    if c["paper"] == "G10": c.update(baseline_sha256=sha(os.path.join(OUT, PART10)), pages=str(n10), change="first issued with edition Z4; revised in editions Z5, Z6 and Z7")
wcsv("COMPONENT_CROSSWALK.csv", cross); changes.append(("changed", "PROGRAM/registers/COMPONENT_CROSSWALK.csv", "G10 digest"))
ready = rd("READINESS.csv")
for r in ready:
    if r["paper"] == "G10": r.update(pages=str(n10), labelled_statements="10", gaps="first issued with edition Z4; revised in editions Z5 (Theorem 5.3), Z6 (Lemma 5.4, Theorem 5.5) and Z7 (Proposition 5.6; a summary sentence corrected after Director G). Proposition 4.1 and Theorems 5.1 to 5.3 were read by Director G (Codex), who reports that they hold within their hypotheses; the later statements have been read by their author only. Equation (7.1) is heuristic; the reference to Li and So was not inspected (OP-30)")
wcsv("READINESS.csv", ready); changes.append(("changed", "PROGRAM/registers/READINESS.csv", "paper G10 revised"))
ops = rd("OPEN_PROBLEMS.csv")
AM = {"OP-21": " Edition Z7: multiplicativity on products of carriers removes the combinations: a consistent multiplicative rule is the squared modulus in one conjugate character (G10-01-10). Director G (pull request 2, commit b626c0d) obtained first, from a marginal test with one balanced coin, invariance under zeta and factorization of product tables on Q(zeta, sqrt 2), that the weight is lambda(a conj a) for a field embedding lambda of the real subfield; Director Z read that proof and confirmed its linear-algebra core by an exact computation (invariant forms of dimension phi(M) for M = 3, 5, 7, 9, spanned by the embeddings). What remains is the Galois group acting on one character. Director G lists three controls that would break it (a regular real plane, an order on the real algebraic amplitudes, a calibrated preparation with a prescribed algebraic entry) and shows that a localized sheet with native operations cannot; none is derived from the carrier.",
      "OP-23": " Edition Z7: Director G (pull request 2) gives, for a packet near the band edge k = -pi/2 of the signed line walk under a linear gain, a bound on the full spinor against a constant-force Schroedinger envelope, and weak convergence of the scaled lattice position law to a Newtonian trajectory for a shrinking packet. Director Z read the proof and checked the bound by a real-space walk on a ring (three runs; see the cross-review). Conditional on the band preparation, the squared-amplitude readout, the scaling of lattice variables and gains whose order grows as the field decreases; no clock.",
      "OP-24": " Edition Z7: first cross-review of paper G10. Director G (Codex) read Proposition 4.1 and Theorems 5.1 to 5.3 in edition Z5 and reports that they hold within their hypotheses; found that a summary sentence (any branching norm-preserving carrier) is false, by the countable binary tree; and corrected the informal dimension count for order two. That error was not found by the self-check of Director Z. Director Z read two results of Director G, reran the four checkers (nine outputs reproduced; floating outputs to 1.5e-6) and checked both results by routes that import nothing from them. Two participants of different model families working from shared sources: not independent replication.",
      "OP-26": " Edition Z7: Director G's bound concerns a packet near a band edge over a compact interval of scaled time and a bounded observable; Director G states that it does not close the full-period connection-corrected criterion, which remains open.",
      "OP-30": " Edition Z7: positivity restricts the weights of the conjugate rules to a cone and composition selects one character (G10-01-10). A carrier without merging walks (the countable binary tree, Director G) makes every rule of the record-sum form the count, so merging is necessary for Theorem 5.2 and for the summary of Section 5. Open: carriers on which the growth hypothesis fails; degrees above two."}
for r in ops:
    if r["id"] in AM: r["statement"] += AM[r["id"]]
wcsv("OPEN_PROBLEMS.csv", ops); changes.append(("changed", "PROGRAM/registers/OPEN_PROBLEMS.csv", "OP-21, OP-23, OP-24, OP-26 and OP-30 amended"))
bp = os.path.join(REG, "BRIDGE_CANDIDATE_REGISTER.json"); br = json.load(open(bp)); k = 0
br["author"] += "; entries of edition Z7 marked Director G (Codex) follow the research supplements of pull request 2, commit b626c0d"
for e in br["edges"]:
    if e["statement"].startswith("Among rules that add over end vertices a function of the modulus"):
        assert "on any norm-preserving gain digraph with a merging pair of walks" in e["statement"]
        e["statement"] = e["statement"].replace("on any norm-preserving gain digraph with a merging pair of walks", "on any norm-preserving gain digraph with a merging pair of walks (merging is necessary: on the countable binary tree every such rule is the count; Director G)"); k += 1
    if e["statement"].startswith("Consistency on history events forces the order of the rule and does not select the embedding"):
        e["statement"] += " Edition Z7: positivity confines the weights to a cone; multiplicativity on products selects one conjugate character (G10-01-10; Director G's classification on Q(zeta, sqrt 2), obtained first). The Galois group on one character remains."; e["locator"] += "; G10-01-10; Director G, Probability_from_record_composition.md"; k += 1
assert k == 2
br["edges"].append({"from": "PRE-ARC", "to": "CM-SYMP", "type": "exact_correspondence", "statement": "Signed line walk under a linear gain, packet near the band edge k = -pi/2: the full spinor stays within E(t) = 2|F| t delta + t delta^2 L^4/(6 eps) + t |F| L delta^2/2 of a constant-force Schroedinger envelope, and for a shrinking packet the scaled lattice position law converges weakly to the Newtonian trajectory Y0 + p0 t - F t^2/2.", "locator": "Director G (Codex), Forced_envelope_and_classical_motion.md, pull request 2, commit b626c0d; cross-check: REVIEW_RECORDS/Director_Z/Session_4/cross_review", "status": "Director G record; proof read and bound checked by a real-space walk by Director Z; unrefereed; conditional on the band preparation, the readout, the scaling and gains of growing order"})
br["retained_outliers"]["director_g_rerun_largest_relative_difference_of_floating_outputs"] = 1.49e-06
json.dump(br, open(bp, "w"), indent=1, ensure_ascii=False); changes.append(("changed", "PROGRAM/registers/BRIDGE_CANDIDATE_REGISTER.json", "two edges amended; one edge and one retained value added"))
gp = os.path.join(REG, "ONTOLOGY_GATE_MAP.json"); gm = json.load(open(gp)); gm["edition"] = NEW
for g in gm["gates"]:
    if g["id"] == "P5": g["evidence"] += " Edition Z7: positivity gives non-negative weights; multiplicativity on products gives one conjugate character (G10-01-10; Director G's record-marginal classification, obtained first). Merging walks are necessary: on a tree every rule is the count (Director G)."
    if g["id"] == "P6": g["evidence"] += " Edition Z7: requiring the rule to be multiplicative on products of carriers selects the squared modulus of one conjugate character among the consistent rules (G10-01-10; Director G)."
    if g["id"] == "P9": g["evidence"] += " Edition Z7: near a band edge Director G bounds the spinor against a constant-force Schroedinger envelope and obtains weak convergence of the position law to a Newtonian trajectory for a shrinking packet; the bound was checked by Director Z by a real-space walk. Conditional on preparation, readout, scaling and gains of growing order."
    if g["id"] == "P10": g["evidence"] += " Edition Z7: the choice among conjugate characters is what remains after consistency and composition; Director G shows that a localized sheet with native operations cannot make it and names three controls that would."
json.dump(gm, open(gp, "w"), indent=1, ensure_ascii=False); changes.append(("changed", "PROGRAM/registers/ONTOLOGY_GATE_MAP.json", "evidence of P5, P6, P9 and P10 amended; no state changed"))
dp = os.path.join(OUT, "PROGRAM", "figures", "Gate_Map_2026-11-13.dot"); dot = open(dp).read(); assert "edition Z6, 13 November 2026" in dot
open(dp, "w").write(dot.replace("edition Z6, 13 November 2026", "edition Z7, 13 November 2026").replace("Editions Z4 to Z6 change evidence", "Editions Z4 to Z7 change evidence")); changes.append(("changed", "PROGRAM/figures/Gate_Map_2026-11-13.dot", "edition label"))
subprocess.run(["dot", "-Tpdf", dp, "-o", dp[:-4] + ".pdf"], check=True); changes.append(("changed", "PROGRAM/figures/Gate_Map_2026-11-13.pdf", "edition label"))
HDR = (OLD + ", 13 November 2026", NEW + ", 13 November 2026")
edit("CONSTRUCTED_TRIALS/README.md", [HDR, ("on the record-sum form of the rule and on a branching norm-preserving carrier; otherwise supplied.", "on the record-sum form of the rule and on a norm-preserving carrier in which walks merge (on a tree every such rule is the count: Director G); otherwise supplied."),
  ("is unique exactly for the orders 2, 4, 6 (derived) | G8 Proposition 8.1; G10 Theorem 5.5 |", "is unique exactly for the orders 2, 4, 6 (derived); multiplicativity on products leaves one conjugate character (derived; Director G) | G8 Proposition 8.1; G10 Theorem 5.5, Proposition 5.6 |")], "edition identifier; GH-1 ledger")
p = os.path.join(OUT, "CONSTRUCTED_TRIALS", "GH-1", "GH-1_Assumptions_and_Dispositions.json"); d = json.load(open(p))
d["derived"].append(dict(id="G10-01-10", text="positivity: non-negative weights; multiplicativity on products: one conjugate character")); d["revised"] = "2026-11-13, edition Z7"
a1 = [a for a in d["assumptions"] if a["id"] == "GH1-A1"][0]; a1["note"] += "; edition Z7: the carrier must have merging walks; on the countable binary tree every rule of the form is the count (Director G)"
json.dump(d, open(p, "w"), indent=1, ensure_ascii=False); changes.append(("changed", "CONSTRUCTED_TRIALS/GH-1/GH-1_Assumptions_and_Dispositions.json", "GH-1 ledger amended"))
S4 = "REVIEW_RECORDS/Director_Z/Session_4/"
for dp_, _, fs_ in os.walk(os.path.join(SRC, "rec")):
    for f in sorted(fs_):
        rel_ = os.path.relpath(os.path.join(dp_, f), os.path.join(SRC, "rec")); put(os.path.join(dp_, f), S4 + rel_, "third addendum to the fourth-session record")
if PCP:
    put(os.path.join(PCP, "register.jsonl"), S4 + "register/register.jsonl", "register of the fourth session, extended by review Z5")
    nev = len(open(os.path.join(PCP, "register.jsonl")).read().strip().split("\n"))
    import re
    p4 = os.path.join(OUT, S4 + "README_SESSION_4.md"); t = open(p4).read(); m = re.search(r"The register: .*?present chain\)\.", t, re.S); assert m
    t = t.replace(m.group(0), "The register: %d events; head digest of the chain `%s`; SHA-256 of the file `%s` (edition Z7; the heads of editions Z4, Z5 and Z6 were `ea97886d0cc8dcd7aba4d95f9844cc8c95f312e56c4796f8da0d5123e1b250d8`, `d79915e5eb5a24959bc14dd7d73a0c7567a5543bebc692eefe2ffc57410a49e6` and `6e5fe34345615733380f6e4fbc4588b9dd63e79e76a91cf5cbb8de893b48fec5`, events 36, 52 and 67 of the present chain)." % (nev, os.environ.get("PCP_HEAD", "see pcpos verify"), sha(os.path.join(PCP, "register.jsonl"))))
    a_ = "findings Z-058 to Z-060, and the record of contact with Director G |"; assert a_ in t
    t = t.replace(a_, a_ + "\n| `ADDENDUM_EDITION_Z7.md`, `NEW_Z_SCOPED_FINDINGS_SESSION_4_ADDENDUM_3.csv`, `cross_review/` | the third addendum: Proposition 5.6 of paper G10, the corrections after Director G's cross-reading, and the cross-review of two results of Director G with its program and result file; findings Z-061 to Z-066 |").replace("`CHANGES_Z4_TO_Z5.md`, `CHANGES_Z5_TO_Z6.md`", "`CHANGES_Z4_TO_Z5.md`, `CHANGES_Z5_TO_Z6.md`, `CHANGES_Z6_TO_Z7.md`")
    open(p4, "w").write(t); changes.append(("changed", S4 + "README_SESSION_4.md", "register digests; third addendum listed"))
T9 = "Reversible Steps on Gain Digraphs: Arc Structure, Complex Structure and the Ray Limit"
for rel in ("PROGRAM/CONTRIBUTIONS.md", "PROGRAM/PAPER_INDEX.md", "PROGRAM/STANDARDS.md", "PROGRAM/CHARTER.md", "REVIEW_RECORDS/README.md", "README.md", "LEGACY/README.md", "NEGATIVE_CONTROLS/README.md"):
    extra = []
    if rel == "PROGRAM/PAPER_INDEX.md": extra = [(f"| G10 | {T10} | article | {old_pages} | {old_statements} |", f"| G10 | {T10} | article | {n10} | 10 |")]
    if rel == "README.md": extra = [(f"({637 + old_pages} assembled pages;", f"({637 + n10} assembled pages;"), (f"theorem registry ({len(reg) - 1} rows)", f"theorem registry ({len(reg)} rows)")]
    if rel == "REVIEW_RECORDS/README.md": extra = [("it worked under the ACR 1.0 text of build 22, which adds Calibration (Core 14.4) to the text used before.", "it worked under the ACR 1.0 text of build 22, which adds Calibration (Core 14.4) to the text used before. In that session Director G (Codex) worked on the same repository; the research supplements of Director G are in pull request 2 of the repository (commit b626c0d) and are not copied here; the cross-review of two of their results is in `Director_Z/Session_4/cross_review/`.")]
    if rel == "PROGRAM/CONTRIBUTIONS.md": extra = [("paper G10; amendment of the ledgers of GH-1 and GH-2);", "paper G10; amendment of the ledgers of GH-1 and GH-2; cross-review of two results of Director G);"),
        ("- **Gemini (Google), Grok (SpaceXAI), DeepSeek (High-Flyer)**", "- **Director G (Codex)**, 13 November 2026: research supplements in pull request 2 of the program repository (probability rules from record composition; a constant-force envelope and classical limit of the signed walk); the cross-reading of paper G10, including the binary-tree example that corrects a summary sentence, and the classification of weights by field embeddings with which G10 Proposition 5.6 agrees.\n- **Gemini (Google), Grok (SpaceXAI), DeepSeek (High-Flyer)**")]
    edit(rel, [HDR] + extra, "edition identifier" + ("; paper G10 revised" if extra else ""))
shutil.copy(os.path.abspath(__file__), os.path.join(OUT, "tools", "director_z_update_7.py")); changes.append(("added", "tools/director_z_update_7.py", "the program that applied these changes"))
changes.append(("added", S4 + "CHANGES_Z6_TO_Z7.md", "this list")); changes.append(("changed", "MANIFEST.json", "edition identifier, digests"))
with open(os.path.join(OUT, S4, "CHANGES_Z6_TO_Z7.md"), "w") as f:
    f.write("# Changes from edition Z6 to edition Z7\n\n13 November 2026. Every other file is byte-identical to edition Z6.\n\n| Change | File | Reason |\n|---|---|---|\n")
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
print("edition Z7:", len(files), "files;", len(reg), "registry rows;", n10, "pages in G10;", len(changes), "changes")
