#!/usr/bin/env python3
"""Apply the Director Z changes of the fourth session (13 November 2026) to a copy of edition Z3, giving edition Z4.
Arguments: build directory (g10, comp, rec, sources), copy of edition Z3, optional directory holding the session register (.pcp).
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
OLD, NEW = "FPHPM-BASELINE-2026-11-12-Z3", "FPHPM-BASELINE-2026-11-13-Z4"
OLDH, NEWH = OLD + ", 12 November 2026", NEW + ", 13 November 2026"
changes = []
def put(src, rel, why, kind=None):
    dst = os.path.join(OUT, rel); os.makedirs(os.path.dirname(dst), exist_ok=True)
    k = kind or ("changed" if os.path.exists(dst) else "added"); shutil.copy(src, dst); changes.append((k, rel, why))
def write(rel, text, why):
    dst = os.path.join(OUT, rel); os.makedirs(os.path.dirname(dst), exist_ok=True)
    k = "changed" if os.path.exists(dst) else "added"; open(dst, "w").write(text); changes.append((k, rel, why))
predecessor_manifest = sha(os.path.join(OUT, "MANIFEST.json"))

# ---- paper G10
P7 = "PAPERS/G7_Transport_Holonomy_and_Monodromy_as_Bridge_Candidates_between_Classica"
T8 = "Gauge-Invariant Pair Measures on Gain Graphs and the Squared-Amplitude Rule"
T9 = "Reversible Steps on Gain Digraphs: Arc Structure, Complex Structure and the Ray Limit"
T10 = "Histories as Events: the Order of the Pair Rule, First-Order Weights and Forces from Gains of Bounded Order"
N10 = ("G10_" + "Histories_as_Events_the_Order_of_the_Pair_Rule_First_Order_Weights_and_Forces_from_Gains_of_Bounded_Order")[:len(os.path.basename(P7))]
P10 = "PAPERS/" + N10; PDF10 = P10 + "/" + N10 + ".pdf"; PART10 = P10 + "/parts/01_G10_manuscript.pdf"
put(os.path.join(SRC, "g10", "G10_manuscript.pdf"), PDF10, "paper G10"); put(os.path.join(SRC, "g10", "G10_manuscript.pdf"), PART10, "paper G10")
for f in ("G10_manuscript.tex", "body.tex", "Scientific_Preamble.tex"): put(os.path.join(SRC, "g10", f), P10 + "/source/" + f, "paper G10")
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

# ---- computation
ba = "COMPUTATION/Baseline_Additions/"
for f in sorted(os.listdir(os.path.join(SRC, "comp"))):
    if f.endswith(".py") or f.endswith("_Results.json"):
        if os.path.exists(os.path.join(OUT, ba + f)):
            assert sha(os.path.join(OUT, ba + f)) == sha(os.path.join(SRC, "comp", f)), f; continue      # reversible_walk_lib.py is unchanged
        put(os.path.join(SRC, "comp", f), ba + f, "computation cited by paper G10 and by the fourth-session record")
rr = os.path.join(OUT, "COMPUTATION", "RERUN_RECORD_2026-11-12.csv")
with open(rr, newline="") as f: rows = list(csv.DictReader(f))
R = lambda p, s, n: dict(program=p, status="RAN_OK", stored_output_compared="yes", stdout_equals_stored=s, note=n)
bi = "result file byte-identical"
rows += [R("Baseline_Additions/verify_continuation_selection.py (fresh directory, with reversible_walk_lib.py)", bi, "8 predicates, of which two are failed and kept (S5); added in edition Z4"),
         R("Baseline_Additions/verify_bounded_order_confinement.py (fresh directory, with reversible_walk_lib.py)", bi, "3 predicates, of which two are failed and kept (C1, C1b; the band-velocity computation is discarded as an instrument); about one minute; added in edition Z4"),
         R("Baseline_Additions/verify_modulus_rules_and_local_spectra.py (fresh directory, with reversible_walk_lib.py)", bi, "5 predicates, of which two are failed and kept (M1 through the program, L3 on the substance); added in edition Z4"),
         R("Baseline_Additions/verify_fourth_session_corrections.py (fresh directory, with reversible_walk_lib.py)", bi, "6 predicates; added in edition Z4"),
         R("Baseline_Additions/verify_ray_error_scaling.py (fresh directory, with reversible_walk_lib.py)", bi, "2 predicates, of which one is failed and kept (E1); several minutes; added in edition Z4"),
         R("Baseline_Additions/verify_ray_averaged_prediction.py (fresh directory, with reversible_walk_lib.py)", bi, "2 predicates; several minutes; added in edition Z4"),
         R("verify_baseline.py on edition Z3 as received", "BASELINE_CHECK_PASS 967 files", "intake for edition Z4"),
         R("PAPERS/G9: source rebuilt with XeLaTeX (TeX Live 2023)", "13 pages; extracted text identical to the issued PDF", "toolchain check for edition Z4"),
         R("note on platform", "numpy 2.5.3, Python 3.13.18, Linux x86_64", "the rows of edition Z4 marked byte-identical refer to the container in which edition Z4 was built")]
wcsv(rr, rows); changes.append(("changed", "COMPUTATION/RERUN_RECORD_2026-11-12.csv", "nine rows appended"))
ci = rd("COMPUTATION_INDEX.csv")
for r in ci:
    if r["directory"] == "COMPUTATION/Baseline_Additions": r["papers"] = "D8 G7 G8 G9 G10"
wcsv("COMPUTATION_INDEX.csv", ci); changes.append(("changed", "PROGRAM/registers/COMPUTATION_INDEX.csv", "paper G10 entered"))

# ---- theorem registry
reg = rd("THEOREM_REGISTRY.csv")
ST10 = [("Lemma", "3.1", "Consistency under continuation is well-definedness on the algebra of cylinder sets of histories"),
        ("Proposition", "4.1", "An additive switching-invariant rule consistent under continuation is a multiple of the number of walks"),
        ("Theorem", "5.1", "Signed line: a rule adding over end vertices a function of the modulus is consistent only for the square"),
        ("Theorem", "5.2", "Norm-preserving gain digraphs with a merging pair of walks: the only consistent power of the modulus is the second"),
        ("Proposition", "6.1", "Exact translation of the quasi-momentum holds only for the linear gain; a translation by 2 pi / n needs gains of order at least n"),
        ("Proposition", "6.2", "Local spectra: no common quasi-energy of the free step multiplied by all q-th roots of unity for q = 3 and q >= 5; four band edges for q = 4")]
n10, pg10 = pages_of(PDF10, [f"{k} {n}" for k, n, _ in ST10])
for i, (k, num, name) in enumerate(ST10, 1):
    reg.append(dict(id=f"G10-01-{i:02d}", paper="G10", part="1", part_title=T10, kind=k, number=num, name=name, status="PROOF_IN_MANUSCRIPT", paper_file_page=str(pg10[f"{k} {num}"]), part_page=str(pg10[f"{k} {num}"]), legacy_locator=""))
wcsv("THEOREM_REGISTRY.csv", reg)

# ---- paper index, crosswalk, citations, readiness
index = rd("PAPER_INDEX.csv"); g9row = [r for r in index if r["id"] == "G9"][0]
index.insert(index.index(g9row) + 1, dict(id="G10", series=g9row["series"], title=T10, kind="article", file=PDF10, pages=str(n10), parts="1", statements="6", cites_papers="G8 G9"))
wcsv("PAPER_INDEX.csv", index)
cross = rd("COMPONENT_CROSSWALK.csv")
cross.append(dict(paper="G10", part="1", title=T10, kind="new", legacy_path="", legacy_volume="", legacy_volume_pages="", legacy_sha256="", baseline_path=PART10,
                  baseline_sha256=sha(os.path.join(OUT, PART10)), pages=str(n10), change="first issued with edition Z4", editable_sources="3"))
wcsv("COMPONENT_CROSSWALK.csv", cross)
cit = rd("CITATIONS_BETWEEN_PAPERS.csv")
C = lambda a, b, t: dict(citing_paper=a, citing_part="1", cited_paper=b, cited_part="1", cited_title=t, evidence="title mention", locator="")
cit += [C("G10", "G8", T8), C("G10", "G9", T9)]
wcsv("CITATIONS_BETWEEN_PAPERS.csv", cit)
ready = rd("READINESS.csv"); g9r = [r for r in ready if r["paper"] == "G9"][0]
g9r["gaps"] += "; edition Z4: paper G10 qualifies one sentence of Section 6.2 (the bounded distance under a linear gain of small order holds over four periods; the spread is ballistic at long times) and reports the remainder of the ray position for longer periods"
ready.insert(ready.index(g9r) + 1, dict(paper="G10", title=T10, kind="article", pages=str(n10), parts="1", parts_with_editable_source="1", labelled_statements="6", independent_referee_report="none",
                                        gaps="first issued with edition Z4; proofs not independently checked; equation (7.1) is heuristic and supported by computed instances only; the reference to Li and So was not inspected (OP-30)"))
wcsv("READINESS.csv", ready)

# ---- open problems
ops = rd("OPEN_PROBLEMS.csv")
AM = {
 "OP-16": (" Edition Z4: three builds of the ACR text are in the record. Sessions 1 to 3 of Director Z pinned release fingerprint 42341ddf...41c79; the Implementation packet received for the fourth session has fingerprint 6b6d3a68...53c6 (build 19) and the plugins carry the text of build 22 (manifest 7ff72eed...4707). Builds 19 and 22 were compared by diff: build 22 adds Core Section 14.4 (Calibration), instruments, and one sentence each in Core 15.2 and 15.8. The text of the first fingerprint was not available for comparison. The mapping to PCP-2026-11-10-R13 is still not made.", None),
 "OP-19": (" Edition Z4: the second order is derived conditionally (G10-01-03, G10-01-04): if events are sets of histories, a rule that adds over end vertices a function of the modulus of the summed gains is consistent only for the square on the signed line, and only for the second power on any norm-preserving gain digraph with a merging pair of walks. The additive weighting of returning walks is excluded under the same assumption (G10-01-02). With trivial gains the count is consistent on the same carrier. Open are a reason for the event structure, for the record role of end vertices and the record-sum form, for the carrier, for the group and representation, and any construction for the first form that does not import the geometry.", "open; two items closed, one conditional construction, one conditional derivation of the order"),
 "OP-23": (" Edition Z4: the continuation requirement is equivalent to taking events to be sets of histories (G10-01-01). An exact force of size 2 pi / n needs gains of order at least n (G10-01-05); the remainder of the ray position after the connection offset falls about as the first power of the field for the packet-averaged ray in computed instances and does not fall for the ray through the central quasi-momentum (G10 Section 7). No bound, clock, composition or interaction.", None),
 "OP-24": (" Edition Z4: the fourth Director Z session kept a register with the PCP OS program (review Z4: six claims, three objections of which one is recorded open, six findings), reached through a client written in the session, so that no hook ran and no command was observed by a host. A Calibration Record under Core 14.4 was written: retrieval 9 of 9 on items the participant chose and had seen, application not measured, no finding on onboarding. The host of that session has a sub-agent facility; it was not used, the principal's instruction not having asked for it. No packet of another Director was among the inputs, so paper G10 has had no cross-review.", None),
 "OP-26": (" Edition Z4: the residual for the ray through the central quasi-momentum does not decrease with the field (0.075, 0.038, 0.038, 0.062, 0.117, 0.232 site at periods 64 to 2048; a predicate expecting a first-order decrease failed). For the ray and the connection averaged over the quasi-momentum distribution of the packet the residual is 0.0735, 0.0273, 0.0135, 0.0071, 0.0029, 0.0016 site (exponent -1.1). The corresponding theorem for Schroedinger operators is Panati, Spohn and Teufel (2003), inspected in part; no bound is proved for the step of G9.", "open; instances extended"),
 "OP-27": (" Edition Z4: a conditional reason is given. A family of measures is one function on sets of histories exactly when it is consistent under continuation (G10-01-01), and then an additive invariant rule is a multiple of the count (G10-01-02): the first-order weighting of returning walks is not a function of sets of histories. That events are sets of histories is an assumption about the event structure and is not derived.", "conditional reason given; the event structure is supplied"),
 "OP-28": (" Edition Z4: narrowed. An exact translation of the quasi-momentum needs the linear gain, hence gains of order at least 2 pi / Phi (G10-01-05). For gains of order q >= 3 wound through blocks no quasi-energy lies in the local spectrum of every block, except four band edges for q = 4 (G10-01-06). Instances: staircases of order 3, 4, 6 hold a walk within about one block for block lengths 16 and 64 up to 2048 steps, leak for block length 4 and spread ballistically for block length 1 (Cedzich et al.); an order-4 staircase reaches 0.69, 0.54, 0.16 of the mean-field displacement at block lengths 16, 64, 256. Open: a theorem on the dynamics; arrangements other than staircases (one quasi-periodic rounding was run and stayed within seven sites).", "unresolved; narrowed by two propositions; five adverse instances"),
}
for r in ops:
    if r["id"] in AM:
        r["statement"] += AM[r["id"]][0]
        if AM[r["id"]][1]: r["state"] = AM[r["id"]][1]
ops.append(dict(id="OP-30", scope="G8 G9 G10", type="foundations", statement="Event structure and carrier. Independent verification of the proofs of paper G10. A reason for taking events to be sets of histories. A classification of the rules consistent under continuation that are not sums over end vertices of a function of one modulus. A principle that selects a carrier on which a rule depending on the gains is consistent: with trivial gains the count is consistent on every digraph of constant out-degree, and the requirement that the transport be visible to the measure is a proposal without warrant. The statement of Li and So on isometries of l_p, cited from secondary sources, is to be inspected.", state="open"))
wcsv("OPEN_PROBLEMS.csv", ops)
for n, why in (("PAPER_INDEX.csv", "paper G10 entered"), ("THEOREM_REGISTRY.csv", "six G10 rows added"), ("COMPONENT_CROSSWALK.csv", "paper G10 entered"), ("CITATIONS_BETWEEN_PAPERS.csv", "two citations added"),
               ("READINESS.csv", "paper G10 entered; G9 note"), ("OPEN_PROBLEMS.csv", "OP-16, OP-19, OP-23, OP-24, OP-26, OP-27, OP-28 amended; OP-30 added")):
    changes.append(("changed", "PROGRAM/registers/" + n, why))

# ---- bridge register
bp = os.path.join(REG, "BRIDGE_CANDIDATE_REGISTER.json"); br = json.load(open(bp)); amended = 0
br["date"] = "2026-11-13"
for e in br["edges"]:
    if e["statement"].startswith("Consistency of the pair measure under continuation (the measure of an event equals"):
        e["statement"] += " Edition Z4: the requirement is equivalent to taking events to be sets of histories (G10-01-01); the event structure is the postulate."; e["locator"] += "; Paper G10, Section 3"; amended += 1
    if e["statement"].startswith("With gains of the orders 2, 3, 4, 6 a linear gain is a strong field"):
        e["statement"] += " Edition Z4: an exact translation of the quasi-momentum by 2 pi / n needs gains of order at least n (G10-01-05); for gains of order q >= 3 no quasi-energy lies in the local spectra of all blocks of a winding staircase, except four band edges for q = 4 (G10-01-06); instances at block lengths 1 to 256 confine, leak or spread, and none follows the ray of its mean field; a linear gain of small order spreads ballistically at long times."
        e["locator"] += "; Paper G10, Section 6; verify_fourth_session_corrections.py N1 to N3"; e["status"] = "two propositions PROOF_IN_MANUSCRIPT; computed instances; general statement unresolved (OP-28)"; amended += 1
assert amended == 2
E = lambda **k: br["edges"].append(k)
E(**{"from": "PRE-GAIN", "to": "PRE-ARC", "type": "exact_correspondence", "statement": "A family of set functions on walks of each length is one function on the algebra of cylinder sets of histories exactly when it is consistent under continuation.", "locator": "Paper G10, G10-01-01; Dowker-Johnston-Surya 2010 for the algebra", "status": "PROOF_IN_MANUSCRIPT; elementary"})
E(**{"from": "PRE-GAIN", "to": "GPT-CLASSICAL", "type": "exact_correspondence", "statement": "An additive switching-invariant rule that is consistent under continuation is a multiple of the number of walks: on sets of histories a first-order rule is the classical count and cannot depend on the transport; the holonomy weighting of returning walks is excluded.", "locator": "Paper G10, G10-01-02; verify_continuation_selection.py S3", "status": "PROOF_IN_MANUSCRIPT; loopless digraphs of constant out-degree"})
E(**{"from": "PRE-ARC", "to": "QMS", "type": "exact_correspondence", "statement": "Among rules that add over end vertices a function of the modulus of the summed gains, consistency under continuation admits only the square on the signed arc digraph of the line, and only the second power on any norm-preserving gain digraph with a merging pair of walks. With trivial gains the count is consistent on the same digraph.", "locator": "Paper G10, G10-01-03, G10-01-04; verify_fourth_session_corrections.py M1 and controls", "status": "PROOF_IN_MANUSCRIPT; conditional on the event structure, the record-sum form and the carrier, all supplied"})
E(**{"from": "PRE-ARC", "to": "CM-SYMP", "type": "untested_transfer", "statement": "Under a linear gain the centroid of a packet follows the ray averaged over the quasi-momentum distribution of the packet, displaced by the connection of the branch eigenvector, with a remainder of first order in the field.", "locator": "Paper G10, Section 7 and equation (7.1); verify_ray_averaged_prediction.py; Panati-Spohn-Teufel 2003 for Schroedinger operators", "status": "heuristic; computed instances (remainder 0.0735 to 0.0016 site over periods 64 to 2048); no bound"})
br["obligations_for_any_prephysical_candidate"].append("state the event structure: if events are sets of histories, a first-order rule is the count and is blind to the transport; say what selects a carrier on which a rule that depends on the transport is consistent")
br["retained_outliers"].update({
 "central_ray_residual_after_offset_sites_periods_64_to_2048": [0.0748, 0.0385, 0.0381, 0.0622, 0.1174, 0.2315],
 "averaged_ray_residual_sites_periods_64_to_2048": [0.0735, 0.0273, 0.0135, 0.0071, 0.0029, 0.0016],
 "staircase_rms_distance_after_2048_steps_orders_2_3_4_6_by_block_length_1_2_4_16_64": [[1108, 750, 403, 346, 347], [520, 520, 160, 9.3, 31], [750, 365, 102, 8.4, 34], [520, 181, 27, 11, 48]],
 "interface_transmission_for_gain_steps_pi_over_12_6_4_3_2_and_2pi_over_3_and_pi": [0.99974, 0.99944, 0.97466, 0.00254, 3.1e-13, 2.9e-13, 0.47693],
 "order4_staircase_fraction_of_mean_field_displacement_block_lengths_16_64_256": [0.686, 0.539, 0.158],
 "additive_holonomy_weight_continuation_ratios_K4_Z3": [1.5, 2.5, 4.0],
 "band_velocities_from_sorted_eigenphases_discarded_instrument_orders_2_12_24": [0.00049, 21.1, 5.46],
 "period_64_staircase_displacement_every_64_steps_sites": [3.86, -3.55, -1.17, 4.0, -2.07, -1.38, 2.45, -1.27, -0.4, 1.69, -2.05, 0.21, 1.66, -2.66, 0.12, 2.53],
 "quasiperiodic_rounded_order4_displacement_range_sites": [-6.6, 5.75]})
json.dump(br, open(bp, "w"), indent=1, ensure_ascii=False); changes.append(("changed", "PROGRAM/registers/BRIDGE_CANDIDATE_REGISTER.json", "four edges and one obligation added; two edges amended; retained values added"))

# ---- gate map
gp = os.path.join(REG, "ONTOLOGY_GATE_MAP.json"); gm = json.load(open(gp)); gm["date"] = "2026-11-13"; gm["edition"] = NEW
ADD = {
 "P1": " Edition Z4: if events are sets of histories, the measures at successive lengths are related by continuation and conversely (G10-01-01); a first-order rule is then the count, and the holonomy weighting of returning walks is not available (G10-01-02). The event structure is supplied.",
 "P5": " Edition Z4: under consistency under continuation the second order is forced among rules that add over end vertices a function of the modulus of the summed gains: only the square on the signed line, only the second power on norm-preserving gain digraphs with merging walks (G10-01-03, G10-01-04). With trivial gains the count is consistent on the same carrier, so the event structure does not select the quadratic rule. Rules outside that form are not classified.",
 "P7": " Edition Z4: the continuation requirement is the statement that events are sets of histories (G10-01-01); it is no longer a separate dynamical assumption, and it remains supplied.",
 "P9": " Edition Z4: the centroid follows the packet-averaged ray displaced by the eigenvector connection with a remainder falling about as the first power of the field in instances (0.0735 to 0.0016 site over periods 64 to 2048); for the ray through the central quasi-momentum the remainder does not fall. No bound. An exact force of size 2 pi / n needs gains of order at least n (G10-01-05).",
 "P10": " Edition Z4: for gains of order q >= 3 wound through blocks no quasi-energy lies in every local spectrum, except four band edges for q = 4 (G10-01-06); staircases of order 3, 4, 6 confine, leak or are strong fields in the instances computed, and an order-4 staircase reaches 0.69, 0.54 and 0.16 of the mean-field displacement at block lengths 16, 64, 256 (OP-28, unresolved).",
 "P12": " Edition Z4: unchanged. With history events the trials admit the classical count as well as the quadratic rule.",
}
for g in gm["gates"]:
    if g["id"] in ADD: g["evidence"] += ADD[g["id"]]
json.dump(gm, open(gp, "w"), indent=1, ensure_ascii=False); changes.append(("changed", "PROGRAM/registers/ONTOLOGY_GATE_MAP.json", "evidence of six gates amended; no state changed"))
dot = open(os.path.join(OUT, "PROGRAM", "figures", "Gate_Map_2026-11-12.dot")).read()
assert "edition Z3, 12 November 2026" in dot
dot = dot.replace("edition Z3, 12 November 2026", "edition Z4, 13 November 2026").replace("Green: open, a conditional derivation, construction or instance exists.", "Green: open, a conditional derivation, construction or instance exists.\\nEdition Z4 changes evidence under P1, P5, P7, P9, P10 and no state.")
write("PROGRAM/figures/Gate_Map_2026-11-13.dot", dot, "gate map figure source, edition Z4")
subprocess.run(["dot", "-Tpdf", os.path.join(OUT, "PROGRAM", "figures", "Gate_Map_2026-11-13.dot"), "-o", os.path.join(OUT, "PROGRAM", "figures", "Gate_Map_2026-11-13.pdf")], check=True, env=dict(os.environ, SOURCE_DATE_EPOCH="1794528000"))
changes.append(("added", "PROGRAM/figures/Gate_Map_2026-11-13.pdf", "gate map figure, edition Z4; the figure of 12 November is kept"))

# ---- constructed trials
def edit(rel, pairs, why):
    p = os.path.join(OUT, rel); s = open(p).read()
    for a, b in pairs:
        assert a in s, (rel, a[:70]); s = s.replace(a, b)
    open(p, "w").write(s); changes.append(("changed", rel, why))
edit("CONSTRUCTED_TRIALS/README.md", [(OLDH, NEWH),
  ("| dependence of an additive measure on the transport | excluded for one weight function applied to all walks; allowed for returning walks, through a class function of their gain, without interference (derived; Directors A, B, G) | G8 Lemma 3.1 |",
   "| dependence of an additive measure on the transport | excluded for one weight function applied to all walks; allowed for returning walks, through a class function of their gain, without interference (derived; Directors A, B, G); excluded altogether when events are sets of histories (derived) | G8 Lemma 3.1; G10 Proposition 4.1 |"),
  ("| second order of the rule | supplied | G8 Section 9 (1) |",
   "| second order of the rule | derived, conditional on events being sets of histories, on the record-sum form of the rule and on a branching norm-preserving carrier; otherwise supplied. With trivial gains the count is consistent on the same carrier | G8 Section 9 (1); G10 Theorems 5.1, 5.2 |"),
  ("| relation between the measures at successive lengths | absent in general (Directors A and B); see GH-2 | G8 Section 9 (5) |",
   "| relation between the measures at successive lengths | absent in general (Directors A and B); it is the statement that events are sets of histories; see GH-2 | G8 Section 9 (5); G10 Lemma 3.1 |"),
  ("| consistency under continuation | supplied; equivalent to the step matrix being a multiple of a unitary matrix on the vectors concerned | G9 Lemma 3.1 |",
   "| consistency under continuation | supplied, in the form: events are sets of histories; equivalent to the step matrix being a multiple of a unitary matrix on the vectors concerned | G9 Lemma 3.1; G10 Lemma 3.1 |"),
  ("| position equation of a ray | observed in instances over one period (deviation 0.61 to 0.65 site); no error bound | G9 Table 4 |",
   "| position equation of a ray | observed in instances over one period (deviation 0.61 to 0.65 site); with the ray and the eigenvector connection averaged over the packet the remainder is 0.0735 to 0.0016 site over the periods 64 to 2048; no error bound | G9 Table 4; G10 Section 7 |"),
  ("| weak force with gains of order 2, 3, 4 or 6 | not obtained in the instances examined (staircase of order-4 gains) | G9 Section 6.2 |",
   "| weak force with gains of order 2, 3, 4 or 6 | not obtained: an exact force of size 2 pi / n needs gains of order at least n (derived); winding gains of order 3 or more have no common local quasi-energy apart from four band edges for order 4 (derived); staircases of order 3, 4, 6 confine, leak or are strong fields (instances) | G9 Section 6.2; G10 Propositions 6.1, 6.2, Table 1 |"),
  ("A ray limit with a force for gains of bounded order: UNRESOLVED, with two adverse instances.", "A ray limit with a force for gains of bounded order: UNRESOLVED, narrowed by two propositions of paper G10, with five adverse instances. With events taken as sets of histories, as a claim that the trials yield quantum and classical mechanics: NOT_IDENTIFIED_IN_SCOPE (the count is consistent with trivial gains).")],
  "edition identifier; ledgers of GH-1 and GH-2 amended")
for name in ("GH-1", "GH-2"):
    p = os.path.join(OUT, "CONSTRUCTED_TRIALS", name, name + "_Assumptions_and_Dispositions.json"); d = json.load(open(p))
    if name == "GH-1":
        a1 = [a for a in d["assumptions"] if a["id"] == "GH1-A1"][0]
        a1["standing"] = "CONDITIONALLY_DERIVED (edition Z4); otherwise SUPPLIED"
        a1["note"] += "; edition Z4: if events are sets of histories, a rule adding over end vertices a function of the modulus of the summed gains is consistent only for the square on the signed line and only for the second power on a norm-preserving gain digraph with merging walks (G10-01-03, G10-01-04), and the first-order weighting of returning walks is excluded (G10-01-02); with trivial gains the count is consistent"
        d["assumptions"].append(dict(id="GH1-A7", text="events are sets of histories (cylinder sets of unending walks); the rule is a sum over end vertices of a function of the modulus of the summed gains", standing="SUPPLIED", note="added in edition Z4 as the assumptions under which GH1-A1 is derived (paper G10)"))
        d["derived"] += [dict(id="G10-01-02", text="an additive invariant rule consistent under continuation is a multiple of the count"), dict(id="G10-01-03", text="signed line: consistent modulus rule is the square"), dict(id="G10-01-04", text="norm-preserving digraph with merging walks: the only consistent power is the second")]
        d["dispositions"]["with events as sets of histories, a gain graph yields quantum mechanics"] = "NOT_IDENTIFIED_IN_SCOPE (the count is consistent with trivial gains)"
    else:
        a2 = [a for a in d["assumptions"] if a["id"] == "GH2-A2"][0]
        a2["note"] += "; edition Z4: equivalent to taking events to be sets of histories (G10-01-01); the event structure is what is supplied"
        d["derived"] += [dict(id="G10-01-01", text="consistency under continuation = well-definedness on cylinder sets of histories"), dict(id="G10-01-05", text="exact translation of the quasi-momentum only for the linear gain; order at least 2 pi / Phi"), dict(id="G10-01-06", text="no common local quasi-energy for winding gains of order 3 or more, except four band edges for order 4")]
        d["observed"]["edition_Z4"] = dict(programs=["verify_continuation_selection.py", "verify_bounded_order_confinement.py", "verify_modulus_rules_and_local_spectra.py", "verify_fourth_session_corrections.py", "verify_ray_error_scaling.py", "verify_ray_averaged_prediction.py"],
                                          predicates=26, passed=19, failed_and_kept="S5 (two), C1, C1b, M1 and L3 of the first modulus-rule program, E1",
                                          adverse_instances="order-4 staircase reaches 0.686, 0.539, 0.158 of the mean-field displacement at block lengths 16, 64, 256; staircases of order 3, 4, 6 confine within a block for block lengths 16, 64",
                                          ray_remainder_sites="central ray 0.0748 to 0.2315; packet-averaged ray 0.0735 to 0.0016, periods 64 to 2048")
        d["dispositions"]["a ray limit with a force for gains of bounded order"] = "UNRESOLVED; narrowed by G10-01-05 and G10-01-06; five adverse instances"
    d["revised"] = "2026-11-13, edition Z4"
    json.dump(d, open(p, "w"), indent=1, ensure_ascii=False); changes.append(("changed", os.path.relpath(p, OUT), name + " ledger amended"))

# ---- review records
S4 = "REVIEW_RECORDS/Director_Z/Session_4/"
for dp, _, fs in os.walk(os.path.join(SRC, "rec")):
    for f in sorted(fs):
        rel = os.path.relpath(os.path.join(dp, f), os.path.join(SRC, "rec")); put(os.path.join(dp, f), S4 + rel, "Director Z fourth-session record")
head = "not included in this build"
if PCP:
    put(os.path.join(PCP, "register.jsonl"), S4 + "register/register.jsonl", "register of the fourth session kept by the PCP OS program, as it stood when the review was closed")
    for f in sorted(os.listdir(os.path.join(PCP, "artifacts"))): put(os.path.join(PCP, "artifacts", f), S4 + "register/artifacts/" + f, "text kept beside the register by the program")
    lines = open(os.path.join(PCP, "register.jsonl")).read().strip().split("\n"); head = sha(os.path.join(PCP, "register.jsonl")); nev = len(lines)
SRCS = [("Dowker, Johnston, Surya. On extending the quantum measure. J. Phys. A 43:505305 (2010)", "arXiv 1007.2725", "994d1e7e3834f3437cc1cffaf2ae038f6c35293c10775dfde6bddd94793e906f", "abstract; Section 3 to equation (30); Claim 6", "the algebra of cylinder sets of finite strings and the decoherence functional of a finite unitary system on it (G10 Section 3)"),
        ("Panati, Spohn, Teufel. Effective dynamics for Bloch electrons: Peierls substitution and beyond. Comm. Math. Phys. 242, 547-578 (2003)", "arXiv math-ph/0212041", "fcb86a0dd3d51ac458aec93ffab651bec7cffb784d90b6e5f5015a8a30627d99", "abstract; introduction with equations (1) to (5); Theorem 3; Corollary 4", "first-order semiclassical equations with the Berry connection for Schroedinger operators (G10 Section 7); does not cover the step of G9"),
        ("Cedzich, Rybar, Werner, Alberti, Genske, Werner. Propagation of quantum walks in electric fields. Phys. Rev. Lett. 111, 160601 (2013)", "arXiv 1302.2081", "c903d92667cb7225b63deaf6d55bd7f5c2eade9efa070c4f30f129a3deca6ce8", "abstract; Table I; the section on the rational case", "rational fields: ballistic propagation with revivals, marked proved in their Table I (G10 Section 6)"),
        ("Grimmett, Janson, Scudo. Weak limits for quantum random walks (2003)", "arXiv quant-ph/0309135", "f614804ae3997f5202c25c090c185d584679b9c5f57bd45752a5d915d7111f2b", "abstract; Theorem 1 with equation (20)", "weak limit of position over steps (quoted in G9; applied in G10 Section 6 to a periodic cell)")]
led = "# Source ledger, Director Z fourth session\n\nRetrieved 13 November 2026, 06:58 UTC, from arxiv.org (PDF and listing page), text extracted with pdftotext. The digest is of the PDF as retrieved. Status of each: preprint with a journal reference read from the listing page (none for the fourth). Retractions, corrections and expressions of concern were not looked for. The copies are not redistributed here.\n\n| Source | Identifier | SHA-256 of the PDF | Portion read | Point supported |\n|---|---|---|---|---|\n"
for s in SRCS: led += "| " + " | ".join(s[:2]) + f" | `{s[2]}` | {s[3]} | {s[4]} |\n"
led += "\nNot inspected: C.-K. Li and W. So, Isometries of l_p-norm, Amer. Math. Monthly 101 (1994) 452-453. Its existence and the statement attributed to it were seen in search-result summaries only (13 November 2026); it is cited in paper G10 as not inspected and is not used in a proof.\n\nSearch queries were run with the host's web search; a first attempt to fetch arxiv.org failed because the host was outside the environment's network allow-list, which was then extended by arxiv.org and export.arxiv.org.\n"
write(S4 + "sources/SOURCE_LEDGER_SESSION_4.md", led, "Director Z fourth-session record")
rs4 = f"""# Director Z, fourth session | Histories as events, the order of the pair rule, forces from gains of bounded order, the remainder of the ray; paper G10

13 November 2026. Research direction: Kirtus Justus. Reviewing participant: LLM Director Z, Claude (Anthropic), at the principal's direction; no endorsement by Anthropic is implied. One participant in this stack; every challenge inside it is a self-check. Root Unary Review of the program whole: G1 Grounding, OPEN, unchanged. No ontology is selected.

| File | Content |
|---|---|
| `CALIBRATION_AND_ACR_USE_LOG_SESSION_4.md` | onboarding, what was and was not established about the method, the Calibration Record, intake checks, direction of the stack, use log |
| `reports/DIRECTOR_Z_TECHNICAL_DISPOSITION_SESSION_4.md` | assessments, evidence, dispositions |
| `registers/NEW_Z_SCOPED_FINDINGS_SESSION_4.csv` | fourteen scoped findings, Z-041 to Z-054 |
| `registers/CALIBRATION_RECORD_SESSION_4.json`, `CALIBRATION_RETRIEVAL_ANSWERS_SESSION_4.json`, `CALIBRATION_RETRIEVAL_SCORES_SESSION_4.json` | the Calibration Record (Core 14.4, build 22), the committed answers and their mechanical scores |
| `sources/SOURCE_LEDGER_SESSION_4.md` | external sources retrieved, with digests and the portions read |
| `register/register.jsonl`, `register/artifacts/` | the append-only register kept for this session by the PCP OS program (`pcpos` 1.0.22), with the principal's opening message as kept by the program |
| `CHANGES_Z3_TO_Z4.md` | every file added or changed |

The register: {('%d events; head digest of the chain `%s`; SHA-256 of the file `%s`.' % (nev, os.environ.get('PCP_HEAD', 'see pcpos verify'), head)) if PCP else head} Check it with `pcpos verify register/register.jsonl`, which prints the head digest of the chain and replays the guards. A pass is a fact about those bytes. The adoption in it is recorded as relayed by the participant, because the program was reached through a client written in the session and no host hook observed the principal's message; its status therefore carries one standing attention item asking the person to confirm. The checks in it are the participant's reports.

The manuscript produced is paper G10 (`PAPERS/{N10}`). Papers G7, G8 and G9 are unchanged.
"""
write(S4 + "README_SESSION_4.md", rs4, "Director Z fourth-session record")

# ---- program documents
total_new = 637 + n10
for rel in ("PROGRAM/CONTRIBUTIONS.md", "PROGRAM/PAPER_INDEX.md", "PROGRAM/STANDARDS.md", "PROGRAM/CHARTER.md", "REVIEW_RECORDS/README.md", "README.md", "LEGACY/README.md", "NEGATIVE_CONTROLS/README.md"):
    extra = []
    if rel == "PROGRAM/PAPER_INDEX.md": extra = [(f"| G9 | {T9} | article | 13 | 12 |", f"| G9 | {T9} | article | 13 | 12 |\n| G10 | {T10} | article | {n10} | 6 |")]
    if rel == "PROGRAM/CONTRIBUTIONS.md":
        extra = [("paper G9, constructed trial GH-2); the reconciliation", "paper G9, constructed trial GH-2); the fourth Director Z session (the continuation requirement as an event structure, the order of the pair rule, the exclusion of first-order weights, forces from gains of bounded order, the remainder of the ray position; paper G10; amendment of the ledgers of GH-1 and GH-2); the reconciliation")]
    if rel == "REVIEW_RECORDS/README.md":
        extra = [("the third Director Z session is in `Director_Z/Session_3/`.", "the third Director Z session is in `Director_Z/Session_3/`. The fourth Director Z session is in `Director_Z/Session_4/`, with the register kept for it by the PCP OS program; it worked under the ACR 1.0 text of build 22, which adds Calibration (Core 14.4) to the text used before.")]
    if rel == "README.md":
        extra = [("by 40 papers in seven series (637 assembled pages;", f"by 41 papers in seven series ({total_new} assembled pages;"), ("theorem registry (381 rows)", f"theorem registry ({len(reg)} rows)")]
    if rel == "PROGRAM/CHARTER.md":
        extra = [("The work is divided into 40 papers", "The work is divided into 41 papers"),
                 ("GH-2, a norm-preserving step on a gain digraph, is the subject of paper G9.", "GH-2, a norm-preserving step on a gain digraph, is the subject of paper G9; paper G10 examines what the continuation requirement of GH-2 decides about the rule of GH-1.")]
    edit(rel, [(OLDH, NEWH)] + extra, "edition identifier" + ("; fourth session" if extra else ""))

shutil.copy(os.path.abspath(__file__), os.path.join(OUT, "tools", "director_z_update_4.py")); changes.append(("added", "tools/director_z_update_4.py", "the program that applied these changes"))
changes.append(("added", S4 + "CHANGES_Z3_TO_Z4.md", "this list")); changes.append(("changed", "MANIFEST.json", "edition identifier, date, digests"))
with open(os.path.join(OUT, S4, "CHANGES_Z3_TO_Z4.md"), "w") as f:
    f.write("# Changes from edition Z3 to edition Z4\n\n13 November 2026. Every other file is byte-identical to edition Z3.\n\n| Change | File | Reason |\n|---|---|---|\n")
    for c in changes: f.write(f"| {c[0]} | `{c[1]}` | {c[2]} |\n")
man = json.load(open(os.path.join(OUT, "MANIFEST.json")))
man["baseline"] = NEW; man["date"] = "13 November 2026"; man["predecessor"] = OLD; man["predecessor_manifest_sha256"] = predecessor_manifest
files = {}
for dp, _, fs in os.walk(OUT):
    for f in sorted(fs):
        rel = os.path.relpath(os.path.join(dp, f), OUT)
        if rel == "MANIFEST.json" or "__pycache__" in rel: continue
        files[rel] = dict(sha256=sha(os.path.join(OUT, rel)), size=os.path.getsize(os.path.join(OUT, rel)))
man["files"] = dict(sorted(files.items()))
json.dump(man, open(os.path.join(OUT, "MANIFEST.json"), "w"), indent=1, ensure_ascii=False)
print("edition Z4:", len(files), "files;", len(reg), "registry rows;", n10, "pages in G10;", total_new, "assembled pages;", len(changes), "changes")
