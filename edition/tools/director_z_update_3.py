#!/usr/bin/env python3
"""Apply the Director Z changes of the third session of 12 November 2026 to a copy of edition Z2, giving edition Z3.
Arguments: build directory (g7, g8, g9, comp, rec, map, trial, directors), copy of edition Z2.  Rewrites MANIFEST.json last."""
import csv, hashlib, json, os, shutil, sys
import pymupdf
SRC, OUT = sys.argv[1], sys.argv[2]
REG = os.path.join(OUT, "PROGRAM", "registers")
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
def rd(n):
    with open(os.path.join(REG, n), newline="") as f: return list(csv.DictReader(f))
def wcsv(n, rows):
    with open(os.path.join(REG, n) if not os.path.isabs(n) else n, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
OLD, NEW = "FPHPM-BASELINE-2026-11-12-Z2", "FPHPM-BASELINE-2026-11-12-Z3"
changes = []
def put(src, rel, why, kind=None):
    dst = os.path.join(OUT, rel); os.makedirs(os.path.dirname(dst), exist_ok=True)
    k = kind or ("changed" if os.path.exists(dst) else "added"); shutil.copy(src, dst); changes.append((k, rel, why))
predecessor_manifest = sha(os.path.join(OUT, "MANIFEST.json"))

# ---- papers
T7 = "Transport, Holonomy and Monodromy as Bridge Candidates between Classical and Quantum Models"
P7 = "PAPERS/G7_Transport_Holonomy_and_Monodromy_as_Bridge_Candidates_between_Classica"
T8 = "Gauge-Invariant Pair Measures on Gain Graphs and the Squared-Amplitude Rule"
P8 = "PAPERS/G8_Gauge_Invariant_Pair_Measures_on_Gain_Graphs_and_the_Squared_Amplitude_Rule"
T9 = "Reversible Steps on Gain Digraphs: Arc Structure, Complex Structure and the Ray Limit"
N9 = ("G9_" + "Reversible_Steps_on_Gain_Digraphs_Arc_Structure_Complex_Structure_and_the_Ray_Limit")[:len(os.path.basename(P7))]
P9 = "PAPERS/" + N9
PDF = {"g7": P7 + "/" + os.path.basename(P7) + ".pdf", "g8": P8 + "/" + os.path.basename(P8) + ".pdf", "g9": P9 + "/" + N9 + ".pdf"}
PART = {"g7": P7 + "/parts/01_G7_manuscript.pdf", "g8": P8 + "/parts/01_G8_manuscript.pdf", "g9": P9 + "/parts/01_G9_manuscript.pdf"}
PD = {"g7": P7, "g8": P8, "g9": P9}
for g, why in (("g7", "paper G7, revised"), ("g8", "paper G8, revised"), ("g9", "paper G9")):
    name = g.upper() + "_manuscript"
    put(os.path.join(SRC, g, name + ".pdf"), PDF[g], why); put(os.path.join(SRC, g, name + ".pdf"), PART[g], why)
    for f in (name + ".tex", "body.tex", "Scientific_Preamble.tex"): put(os.path.join(SRC, g, f), PD[g] + "/source/" + f, why)
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
    if f.endswith(".py") or f.endswith("_Results.json"): put(os.path.join(SRC, "comp", f), ba + f, "computation cited by papers G7, G8 and G9 and by the third-session record")
rr = os.path.join(OUT, "COMPUTATION", "RERUN_RECORD_2026-11-12.csv")
with open(rr, newline="") as f: rows = list(csv.DictReader(f))
R = lambda p, s, n: dict(program=p, status="RAN_OK", stored_output_compared="yes", stdout_equals_stored=s, note=n)
rows += [R("Baseline_Additions/verify_third_round_director_items.py (fresh directory)", "result file byte-identical", "25 predicates; added in edition Z3"),
         R("Baseline_Additions/verify_fourth_round_director_items.py (fresh directory)", "result file byte-identical", "16 predicates; added in edition Z3"),
         R("Baseline_Additions/verify_gain_graph_covers_and_growth.py (fresh directory)", "result file byte-identical", "5 predicates; added in edition Z3"),
         R("Baseline_Additions/verify_reversible_gain_digraphs.py (fresh directory, with reversible_walk_lib.py)", "result file byte-identical", "21 predicates; about four minutes; added in edition Z3"),
         R("Baseline_Additions/verify_reversible_walk_rays.py (fresh directory, with reversible_walk_lib.py)", "result file byte-identical", "7 predicates, of which one is failed and kept (criterion 0.02 site not met); added in edition Z3"),
         R("REVIEW_RECORDS/Directors_A_B_G_2026-11-12: packet verifiers and verification programs of the packets A3, B3, G3, A4, B4, G4 (copies, outputs redirected)", "stored results reproduced as reported by each program; floating residuals differ at rounding level", "rerun for edition Z3"),
         R("verify_baseline.py on edition Z2 as received", "BASELINE_CHECK_PASS 791 files", "intake for edition Z3"),
         R("note on the rows of edition Z2 marked byte-identical", "refers to the container in which edition Z2 was built", "Directors A, B and G report seven last-place floating-point differences for verify_gain_graph_pair_measures.py and 29 for verify_reconciliation_and_phase_recovery.py on their platforms, with all predicates passing")]
wcsv(rr, rows); changes.append(("changed", "COMPUTATION/RERUN_RECORD_2026-11-12.csv", "eight rows appended"))
ci = rd("COMPUTATION_INDEX.csv")
for r in ci:
    if r["directory"] == "COMPUTATION/Baseline_Additions": r["papers"] = "D8 G7 G8 G9"
wcsv("COMPUTATION_INDEX.csv", ci); changes.append(("changed", "PROGRAM/registers/COMPUTATION_INDEX.csv", "paper G9 entered"))

# ---- registers: theorem registry
reg = rd("THEOREM_REGISTRY.csv")
n7, pg7 = pages_of(PDF["g7"], [f"{r['kind']} {r['number']}" for r in reg if r["paper"] == "G7"])
ST8NEW = [("Proposition", "4.4", "The identity-indicator measure is the coincidence count on the derived covering graph and the dimension-weighted mean of the irreducible measures"),
          ("Proposition", "5.2", "Growth: gains reached at a given length form a coset; the growth condition holds exactly when closed walks of even length realize every group element")]
n8, pg8 = pages_of(PDF["g8"], [f"{r['kind']} {r['number']}" for r in reg if r["paper"] == "G8"] + [f"{k} {n}" for k, n, _ in ST8NEW])
for r in reg:
    if r["paper"] == "G7": r["paper_file_page"] = r["part_page"] = str(pg7[f"{r['kind']} {r['number']}"])
    if r["paper"] == "G8":
        r["paper_file_page"] = r["part_page"] = str(pg8[f"{r['kind']} {r['number']}"])
        if r["number"] == "3.1": r["name"] = "Additive switching-invariant functions on walks: constant weight on open walks, class function of the gain on closed walks"
        if r["number"] == "6.1": r["name"] = "The product of gain graphs gives the tensor product at each walk length"
for i, (k, num, name) in enumerate(ST8NEW, 9):
    reg.append(dict(id=f"G8-01-{i:02d}", paper="G8", part="1", part_title=T8, kind=k, number=num, name=name, status="PROOF_IN_MANUSCRIPT", paper_file_page=str(pg8[f"{k} {num}"]), part_page=str(pg8[f"{k} {num}"]), legacy_locator=""))
ST9 = [("Lemma", "3.1", "Consistency of the pair measure under continuation is norm preservation of the step matrix", "PROOF_IN_MANUSCRIPT"),
       ("Proposition", "4.1", "With trivial gains a norm-preserving step is a permutation", "PROOF_IN_MANUSCRIPT"),
       ("Proposition", "4.2", "On an undirected gain graph a norm-preserving step is an involution after normalization", "PROOF_IN_MANUSCRIPT"),
       ("Theorem", "4.3", "Out-degree two: arc digraph of a digraph with two arcs into and out of every node; zigzag gain -1", "PROOF_IN_MANUSCRIPT"),
       ("Proposition", "5.1", "Polar complex structure of a real orthogonal step: uniqueness under a positive generator; reversal", "PROOF_IN_MANUSCRIPT"),
       ("Proposition", "5.3", "Only real scalars commute with the step and the vertex projections", "PROOF_IN_MANUSCRIPT"),
       ("Lemma", "6.1", "Dispersion and group velocity of the signed arc digraph of a ring", "PROOF_IN_MANUSCRIPT"),
       ("Theorem", "6.2", "Grimmett, Janson and Scudo", "RESTATEMENT"),
       ("Proposition", "6.3", "A linear gain translates the quasi-momentum by a fixed amount per step", "PROOF_IN_MANUSCRIPT"),
       ("Proposition", "6.4", "Group velocity as derivative of the eigenphase with respect to the holonomy round the ring", "PROOF_IN_MANUSCRIPT"),
       ("Proposition", "7.1", "Ladder transport of a rectagraph has trivial holonomy exactly for Cayley graphs of elementary abelian 2-groups", "PROOF_IN_MANUSCRIPT"),
       ("Proposition", "7.2", "Norm-preserving signings are the anticommuting ones; central complex structure exactly for k = 3 modulo 4", "PROOF_IN_MANUSCRIPT")]
n9, pg9 = pages_of(PDF["g9"], [f"{k} {n}" for k, n, _, _ in ST9])
for i, (k, num, name, st) in enumerate(ST9, 1):
    reg.append(dict(id=f"G9-01-{i:02d}", paper="G9", part="1", part_title=T9, kind=k, number=num, name=name, status=st, paper_file_page=str(pg9[f"{k} {num}"]), part_page=str(pg9[f"{k} {num}"]), legacy_locator=""))
wcsv("THEOREM_REGISTRY.csv", reg)

# ---- paper index, crosswalk, citations, readiness
index = rd("PAPER_INDEX.csv"); oldp = {}
for r in index:
    if r["id"] == "G7": oldp["G7"] = int(r["pages"]); r.update(pages=str(n7), cites_papers="G3 G6 G8 G9")
    if r["id"] == "G8": oldp["G8"] = int(r["pages"]); r.update(pages=str(n8), statements="10", cites_papers="G3 G6 G7 G9")
g8row = [r for r in index if r["id"] == "G8"][0]
index.insert(index.index(g8row) + 1, dict(id="G9", series=g8row["series"], title=T9, kind="article", file=PDF["g9"], pages=str(n9), parts="1", statements="12", cites_papers="G3 G7 G8"))
wcsv("PAPER_INDEX.csv", index)
cross = rd("COMPONENT_CROSSWALK.csv")
for c in cross:
    if c["paper"] == "G7": c.update(baseline_sha256=sha(os.path.join(OUT, PART["g7"])), pages=str(n7), change="first issued with edition Z1; revised in editions Z2 and Z3")
    if c["paper"] == "G8": c.update(baseline_sha256=sha(os.path.join(OUT, PART["g8"])), pages=str(n8), change="first issued with edition Z2; revised in edition Z3")
cross.append(dict(paper="G9", part="1", title=T9, kind="new", legacy_path="", legacy_volume="", legacy_volume_pages="", legacy_sha256="", baseline_path=PART["g9"],
                  baseline_sha256=sha(os.path.join(OUT, PART["g9"])), pages=str(n9), change="first issued with edition Z3", editable_sources="3"))
wcsv("COMPONENT_CROSSWALK.csv", cross)
cit = rd("CITATIONS_BETWEEN_PAPERS.csv")
C = lambda a, b, t: dict(citing_paper=a, citing_part="1", cited_paper=b, cited_part="1", cited_title=t, evidence="title mention", locator="")
T3 = "Finite Signed Graphs and Binary Extension Constraints"
cit += [C("G7", "G9", T9), C("G8", "G9", T9), C("G9", "G3", T3), C("G9", "G7", T7), C("G9", "G8", T8)]
wcsv("CITATIONS_BETWEEN_PAPERS.csv", cit)
ready = rd("READINESS.csv")
for r in ready:
    if r["paper"] == "G7": r.update(pages=str(n7), gaps="revised in editions Z2 and Z3; proofs not independently refereed; quoted inputs partly inspected in extracts and bibliographic details partly unverified (OP-17)")
    if r["paper"] == "G8": r.update(pages=str(n8), labelled_statements="10", gaps="revised in edition Z3 (Lemma 3.1 completed after the review of Directors A, B and G; Propositions 4.4 and 5.2 added); proofs not independently checked; bibliographic details partly unverified (OP-25)")
g8r = [r for r in ready if r["paper"] == "G8"][0]
ready.insert(ready.index(g8r) + 1, dict(paper="G9", title=T9, kind="article", pages=str(n9), parts="1", parts_with_editable_source="1", labelled_statements="12", independent_referee_report="none",
                                        gaps="first issued with edition Z3; proofs not independently checked; Theorem 6.2 quoted; the ray position equation is supported by computed instances only; bibliographic details partly unverified (OP-26)"))
wcsv("READINESS.csv", ready)

# ---- open problems
ops = rd("OPEN_PROBLEMS.csv")
AM = {
 "OP-18": (" Edition Z3: a real reversible step has a complex structure of its own, unique under positivity of the generator and reversed with the step (G9-01-05); Stueckelberg (1960) and Moretti-Oppio (2017, for Poincare symmetry) are the corresponding results in the literature. In the model of G9 the record projections do not commute with it and the commutant of step and records is real (G9-01-06). This route gives a warrant only if the observables are those generated by the dynamics, which is the requirement in another form. On signed Cayley rectagraphs a central complex structure exists exactly for k = 3 mod 4 direction classes, with k supplied (G9-01-12). A warrant is not identified.", None),
 "OP-19": (" Edition Z3: the growth condition is settled (G8-01-10): it holds exactly when the closed walks of even length realize every group element, and the type of the limit space follows the group they realize. A representation-free form of the rule is the coincidence count on the covering graph (G8-01-09). Open are a reason for the second order (an additive weighting of returning walks exists: G8-01-01), for the record role of end vertices, for the group and representation, and any construction for the first form that does not import the geometry.", "open; two items closed, one conditional construction"),
 "OP-20": (" Edition Z3: where a reversible real step defines a complex structure, its orientation is the direction of the step (G9-01-05); on a signed cube it is the orientation of the three direction classes (G9-01-12). Neither is a structure that the records of the model respect, and neither fixes relative orientations of several systems.", None),
 "OP-21": (" Edition Z3: in the constructed trial GH-2 a weak force requires a linear gain in a cyclic group of large order, for which the measure depends on the character; with orders 2, 3, 4, 6 the field is strong, and a staircase of order-4 gains does not follow the ray of its mean field (G9 Section 6.2; OP-28).", None),
 "OP-22": (" Edition Z3: the interpolated family K_t is not closed under selective local filters (Directors A, B); no four-party weight repairs it (Director A); a matching-generated hierarchy is closed under parallel preparation, discarding and unconditioned one-site channels and excludes GHZ (Director A); one pure entangled seed with local unitaries and local filters gives all two-qubit states (Directors A, B). All within the imported quantum formalism; recomputed. The product of gain graphs gives the tensor product at each length and can reach fewer end-vertex pairs over all lengths (Director G; G8 Section 6). Which selective operations are available is a further obligation.", None),
 "OP-23": (" Edition Z3: requiring consistency of the pair measure under continuation makes the step unitary up to a factor (G9-01-01); this admits permutations without transport, involutions on undirected gain graphs, and for out-degree two the arc digraph of a 2-in 2-out digraph with a sign -1 (G9-01-02 to G9-01-04). For the signed arc digraph of a ring the position over steps has the distribution of a group velocity (quoted), a linear gain translates the quasi-momentum exactly (G9-01-09) and packets follow the rays of w(k) + Phi x over one period in instances. Supplied: the requirement, the ring, the step count, the gain order for a weak force. Not obtained: a clock with a unit, a generator other than a choice of logarithm, an error bound for the position equation, interaction, composition, more than one dimension, and classical Hamiltonian mechanics beyond the rays of a given dispersion function.", "open; one conditional construction (GH-2)"),
 "OP-24": (" Edition Z3: the ACR 1.0 packet was among the inputs of the third Director Z session; the kernel and six Core clauses were fetched. One error of edition Z2 was found by Directors A, B and G and not by the self-check of Director Z; one erratum proposed by Directors A and B was not upheld (an overline lost in text extraction of the PDF). No sub-agent facility in any stack.", None),
 "OP-25": (" Edition Z3: the growth condition is proved with a criterion (G8-01-10); Lemma 3.1 was completed after the review of Directors A, B and G. Open: independent verification of the proofs, including the two new propositions; the bibliographic details; the name 'derived graph' and the Perron-Frobenius statement are used from recall.", "open; one item closed"),
}
for r in ops:
    if r["id"] in AM:
        r["statement"] += AM[r["id"]][0]
        if AM[r["id"]][1]: r["state"] = AM[r["id"]][1]
O = lambda i, sc, ty, st, state: dict(id=i, scope=sc, type=ty, statement=st, state=state)
ops += [O("OP-26", "G9", "manuscript", "Independent verification of the proofs of paper G9. An error bound for the position equation of the rays under a linear gain (adiabatic estimate with the connection of the branch eigenvector; the computed residual after the connection offset is 0.075 and 0.038 site at periods 64 and 256, above the criterion 0.02 set in advance). Line-by-line check of the hypotheses of the quoted weak-limit theorem. Bibliographic details from recall: journal references of Grimmett-Janson-Scudo and Sanyal-Sottile-Sturmfels, the volume of Moretti-Oppio.", "open"),
        O("OP-27", "G8 G9", "foundations", "Relation between walk lengths and order of the rule. Consistency of the pair measure under continuation is a requirement that a generic gain graph violates (Directors A, B; G9-01-01); a reason for it, or an alternative relation between the measures at different lengths, is not given. An additive weighting of returning walks by a class function of their holonomy is switching invariant (G8-01-01); a reason for excluding it, if the second-order rule is intended, is not given.", "not identified"),
        O("OP-28", "G8 G9", "foundations", "Force and gain order. Decide whether gains of bounded order (in particular the orders 2, 3, 4, 6 for which the pair measure is independent of the character) can produce the rays of a weak force in a controlled limit, by some encoding other than the staircase tried in G9 Section 6.2, or prove that they cannot. Related: the long-time behaviour under a linear gain depends on the arithmetic of the field (Cedzich et al. 2013).", "unresolved; two adverse instances"),
        O("OP-29", "G7", "foundations", "Admitted tests. The cubic Veronese model (Director G) has the qubit table on a designated family of pure tests; with those tests only it is the qubit, with all affine effects it is a different theory in which pure states at Bloch angle 60 degrees are perfectly distinguishable. A candidate has to state which tests are admitted and why, before a pure-state transition geometry can be attributed to it; a derivation of tomographic completeness of the designated tests is not given.", "not identified")]
wcsv("OPEN_PROBLEMS.csv", ops)
for n, why in (("PAPER_INDEX.csv", "papers G7 and G8 revised; paper G9 entered"), ("THEOREM_REGISTRY.csv", "G7 and G8 pages updated, two G8 rows renamed, two G8 rows and twelve G9 rows added"), ("COMPONENT_CROSSWALK.csv", "G7 and G8 digests; paper G9 entered"),
               ("CITATIONS_BETWEEN_PAPERS.csv", "five citations added"), ("READINESS.csv", "papers G7 and G8 revised; paper G9 entered"), ("OPEN_PROBLEMS.csv", "OP-18 to OP-25 amended; OP-26 to OP-29 added")):
    changes.append(("changed", "PROGRAM/registers/" + n, why))

# ---- bridge register
bp = os.path.join(REG, "BRIDGE_CANDIDATE_REGISTER.json"); br = json.load(open(bp))
br["nodes"]["PRE-ARC"] = "norm-preserving gain digraphs: a group element on each arc of a finite digraph with step matrix a multiple of a unitary matrix; for out-degree two, arc digraphs of 2-in 2-out digraphs with a sign -1 [paper G9; Severini 2003]"
br["nodes"]["GPT-VERONESE"] = "convex hulls of the tensors n x ... x n (odd degree) with projective and higher-degree affine tests [Director G; Sanyal-Sottile-Sturmfels 2009 for the convex bodies]"
n_before = len(br["edges"]); replaced = 0
for e in br["edges"]:
    if e["statement"].startswith("Two unexamined proposals"):
        e.update({"from": "PRE-REL", "to": "PRE-GAIN", "type": "exact_correspondence",
                  "statement": "A rectagraph carries a transport of its own: an edge is carried across the quadrilateral it spans with the edge travelled (discrete Schild's ladder). Its holonomy is trivial exactly for Cayley graphs of elementary abelian 2-groups; on the incidence graph of the 7-point biplane it is the symmetric group S_4. Its permutation representation contains the trivial one. On the Cayley rectagraphs the signings with norm-preserving step are those with every quadrilateral negative, i.e. anticommuting class matrices; their ordered product is a central complex structure exactly for k = 3 mod 4.",
                  "locator": "Paper G9, G9-01-11, G9-01-12; verify_reversible_gain_digraphs.py R10; Huang 2019; Mathews 2019; Alon-Zheng 2020",
                  "status": "PROOF_IN_MANUSCRIPT; examined in the third Director Z session (was: untested transfer); selects nothing: the number of classes is supplied"}); replaced += 1
    if e["statement"].startswith("Walk length is not a unitary evolution"):
        e["statement"] += " Edition Z3: the measures at successive lengths are not related by continuation (Directors A, B); on an undirected gain graph a norm-preserving step is an involution (G9-01-03; Director B)."
    if e["statement"].startswith("A directed three-cycle gives"):
        e["statement"] += " Edition Z3: for every odd directed cycle the polar factor of P - P^T is a complex structure on the zero-sum space, reversed by reversal (Directors B, G); it is the case of a permutation of the polar structure of any real orthogonal map (G9-01-05), and the vertex projections do not commute with it."
    if e["statement"].startswith("A switching-invariant additive function on walks is a multiple of the count"):
        e["statement"] = "A switching-invariant additive function on walks has a constant weight on open walks and a class function of the gain on closed walks; with one weight function for all walks it is a multiple of the count. Walks that leave distinct records have the counting measure under any pair rule. (Sentence of edition Z2 corrected after Directors A, B, G.)"
        e["locator"] = "Paper G8, G8-01-01 (revised), G8-01-07; verify_fourth_round_director_items.py G2"
assert replaced == 1
E = lambda **k: br["edges"].append(k)
E(**{"from": "PRE-GAIN", "to": "PRE-ARC", "type": "postulate", "statement": "Consistency of the pair measure under continuation (the measure of an event equals, up to a fixed factor, that of all its continuations); gains of modulus one; out-degree two.", "locator": "Paper G9, Sections 3, 8; CONSTRUCTED_TRIALS/GH-2", "status": "supplied, not derived; violated by a generic gain graph (Directors A, B)"})
E(**{"from": "PRE-GAIN", "to": "PRE-ARC", "type": "exact_correspondence", "statement": "Consistency under continuation is norm preservation of the step matrix. With trivial gains it admits permutations only; on undirected gain graphs involutions only; for out-degree two and unit gains exactly the arc digraphs of 2-in 2-out digraphs with zigzag gain -1 in every block: the two continuations of a pair of walks interfere with opposite signs.", "locator": "Paper G9, G9-01-01 to G9-01-04; verify_reversible_gain_digraphs.py R1, R2", "status": "PROOF_IN_MANUSCRIPT; exhaustive on at most six vertices"})
E(**{"from": "PRE-ARC", "to": "GPT-REALQT", "type": "obstruction", "statement": "A real reversible step has a complex structure of its own (unique under a positive generator, reversed with the step), but only real scalars commute with the step and the vertex records: the model with its records is a real theory and the complex structure is not a structure of it.", "locator": "Paper G9, G9-01-05, G9-01-06; Stueckelberg 1960; Moretti-Oppio 2017; verify_reversible_gain_digraphs.py R3, R5", "status": "PROOF_IN_MANUSCRIPT; no warrant for complex amplitudes (OP-18)"})
E(**{"from": "PRE-ARC", "to": "CM-SYMP", "type": "conditional_derivation" if "conditional_derivation" in br.get("edge_types", {}) else "exact_correspondence", "statement": "Signed arc digraph of a ring: two branches of opposite group velocity; position over steps converges in law to the group-velocity distribution (quoted); a gain linear in position translates the quasi-momentum by a fixed amount per step exactly, and exchanged steps have a uniform pair gain; packets follow the rays of w(k) + Phi x over one period in instances; the velocity is the response of the eigenphase to the holonomy round the ring.", "locator": "Paper G9, G9-01-07 to G9-01-10; verify_reversible_walk_rays.py", "status": "conditional on the ring, the step count and the requirement; position equation in instances only (deviation 0.61 to 0.65 site); one predicate failed and kept"})
E(**{"from": "PRE-ARC", "to": "CM-SYMP", "type": "obstruction", "statement": "With gains of the orders 2, 3, 4, 6 a linear gain is a strong field and a walk stays within about six sites over four periods; a staircase of order-4 gains with weak mean slope does not follow the ray of the mean field (3.80 against 5.53 sites, 12.00 against 22.26). A weak force was obtained only with gains whose order grows, where the pair measure depends on the character. The long-time behaviour under a linear gain depends on the arithmetic of the field.", "locator": "Paper G9, Section 6.2; G8-01-08; Cedzich et al. 2013; verify_reversible_walk_rays.py R8", "status": "computed instances; general statement unresolved (OP-28)"})
E(**{"from": "PRE-GAIN", "to": "QMS", "type": "exact_correspondence", "statement": "The pair measure of the identity indicator is the count of coincidences of lifted walks on the derived covering graph and the dimension-weighted mean of the irreducible measures; a covering supplies its group but not the choice of representation. The gains reached at a given length form a coset of the holonomy group of the gain augmented by length parity, and the density statement of G8-01-05 holds with the limit space determined by the gains of closed walks of even length.", "locator": "Paper G8, G8-01-09, G8-01-10; verify_gain_graph_covers_and_growth.py; witnesses of Directors A, B, G", "status": "PROOF_IN_MANUSCRIPT"})
E(**{"from": "QT", "to": "GPT-VERONESE", "type": "obstruction", "statement": "A designated family of pure tests with the qubit table does not determine the convex set of states: the cubic Veronese model has dimension 10 and a cubic effect separating mixtures with equal Bloch contraction (1/2 against 5/8). With the designated tests only the model is the qubit; with all affine effects pure states at Bloch angle 60 degrees are perfectly distinguishable, so the model does not carry the qubit transition-probability geometry.", "locator": "Director G, G3 (Operational Veroneses and Quantum Nonselection); Paper G7, Section 5; verify_third_round_director_items.py H7, H8", "status": "Director G record; recomputed; second reading added by Director Z"})
E(**{"from": "QT", "to": "COMPOSITES", "type": "obstruction", "statement": "Selective local filters take every interior member of the family K_t outside itself; no four-party weight makes the affine family closed under parallel preparation and discarding; a matching-generated hierarchy is closed under weaker operations and excludes GHZ; one pure entangled seed with local unitaries and filters gives all two-qubit states. Which selective operations are available has to be supplied.", "locator": "Director A, A3; Director B, B3; Director G, G4; verify_third_round_director_items.py H1 to H5", "status": "Director records within the imported quantum formalism; recomputed"})
E(**{"from": "PRE-GAIN", "to": "QT", "type": "untested_transfer", "statement": "Not examined: exp(-isH) on an undirected gain graph as a dynamics (Director G; imports the imaginary unit and a continuous parameter); arc digraphs of degree three with blocks in Z_3; composition of two norm-preserving digraphs with interaction as gains on the product.", "locator": "Director Z third-session disposition, section 5", "status": "background; no construction"})
assert len(br["edges"]) == n_before + 9
br["obligations_for_any_prephysical_candidate"] += [
    "state how the measures at different lengths or times are related, and why",
    "state which tests are admitted, before attributing a transition-probability geometry",
    "if a force is to arise from a transport of bounded order, exhibit the limit; if from a transport of growing order, supply the ordering of values"]
br["retained_outliers"].update({"rays_residual_after_connection_offset_sites_periods_64_256": [0.0747, 0.0380], "staircase_order4_displacement_vs_linear_gain_sites": [[3.796, 5.535], [11.998, 22.256]],
    "strong_field_return_probability_order3_after_3_and_6_steps": [0.0, 0.7656], "veronese_infimum_at_20_40_60_degrees": [0.704, 0.207, 0.0], "three_cycle_commutator_of_vertex_projection_with_J": "2 sqrt 2/3",
    "consistent_signings_of_K4": 0, "biplane_ladder_holonomy_group_order": 24})
json.dump(br, open(bp, "w"), indent=1, ensure_ascii=False); changes.append(("changed", "PROGRAM/registers/BRIDGE_CANDIDATE_REGISTER.json", "two nodes, nine edges, three obligations added; one edge replaced; three edges amended"))
put(os.path.join(SRC, "map", "ONTOLOGY_GATE_MAP.json"), "PROGRAM/registers/ONTOLOGY_GATE_MAP.json", "gate map")
put(os.path.join(SRC, "map", "Gate_Map_2026-11-12.pdf"), "PROGRAM/figures/Gate_Map_2026-11-12.pdf", "gate map figure")
put(os.path.join(SRC, "map", "gate_map.dot"), "PROGRAM/figures/Gate_Map_2026-11-12.dot", "gate map figure source")

# ---- constructed trials, review records
put(os.path.join(SRC, "trial", "README.md"), "CONSTRUCTED_TRIALS/README.md", "GH-1 ledger amended; constructed trial GH-2")
put(os.path.join(SRC, "trial", "GH-1_Assumptions_and_Dispositions.json"), "CONSTRUCTED_TRIALS/GH-1/GH-1_Assumptions_and_Dispositions.json", "GH-1 ledger amended")
put(os.path.join(SRC, "trial", "GH-2_Assumptions_and_Dispositions.json"), "CONSTRUCTED_TRIALS/GH-2/GH-2_Assumptions_and_Dispositions.json", "constructed trial GH-2")
for dp, _, fs in os.walk(os.path.join(SRC, "directors")):
    for f in sorted(fs):
        if "__pycache__" in dp: continue
        rel = os.path.relpath(os.path.join(dp, f), os.path.join(SRC, "directors"))
        put(os.path.join(dp, f), "REVIEW_RECORDS/Directors_A_B_G_2026-11-12/" + rel, "packet of Director A, B or G, as received")
for dp, _, fs in os.walk(os.path.join(SRC, "rec")):
    for f in sorted(fs):
        rel = os.path.relpath(os.path.join(dp, f), os.path.join(SRC, "rec"))
        put(os.path.join(dp, f), "REVIEW_RECORDS/Director_Z/Session_3/" + rel, "Director Z third-session record")

# ---- program documents
def edit(rel, pairs, why):
    p = os.path.join(OUT, rel); s = open(p).read()
    for a, b in pairs:
        assert a in s, (rel, a[:70]); s = s.replace(a, b)
    open(p, "w").write(s); changes.append(("changed", rel, why))
total_old = 621; total_new = total_old - oldp["G7"] - oldp["G8"] + n7 + n8 + n9
for rel in ("PROGRAM/CONTRIBUTIONS.md", "PROGRAM/PAPER_INDEX.md", "PROGRAM/STANDARDS.md", "PROGRAM/CHARTER.md", "REVIEW_RECORDS/README.md", "README.md", "LEGACY/README.md", "NEGATIVE_CONTROLS/README.md"):
    extra = []
    if rel == "PROGRAM/PAPER_INDEX.md":
        extra = [(f"| G8 | {T8} | article | {oldp['G8']} | 8 |", f"| G8 | {T8} | article | {n8} | 10 |\n| G9 | {T9} | article | {n9} | 12 |")]
    if rel == "PROGRAM/CONTRIBUTIONS.md":
        extra = [("constructed trial GH-1, gate map); the reconciliation", "constructed trial GH-1, gate map); the third Director Z session (cross-review of the third and fourth rounds of Directors A, B and G, revision of papers G7 and G8, paper G9, constructed trial GH-2); the reconciliation"),
                 ("whole-model conjugation, and the gate list used in the gate map. Points used in papers G7 and G8 are attributed there.", "whole-model conjugation, and the gate list used in the gate map; in the third and fourth rounds the selective-filter exclusions and the pure-seed closure, the matching hierarchy, the odd-cycle complex structures, the cubic Veronese model, the correction of the additive statement of paper G8, the failure of continuation between walk lengths, the growth witnesses, and the restriction of synchronized products. Points used in papers G7, G8 and G9 are attributed there.")]
    if rel == "REVIEW_RECORDS/README.md":
        extra = [("the second Director Z session is in `Director_Z/Session_2/`.", "the second Director Z session is in `Director_Z/Session_2/`. Six further packets (A3, B3, G3, A4, B4, G4) are kept as received in the same folder; the third Director Z session is in `Director_Z/Session_3/`. The file named G9 inside packet B4 is a Director B submission and is not paper G9 of the program.")]
    if rel == "README.md":
        extra = [("by 39 papers in seven series (621 assembled pages;", f"by 40 papers in seven series ({total_new} assembled pages;"), ("theorem registry (367 rows)", f"theorem registry ({len(reg)} rows)")]
    if rel == "PROGRAM/CHARTER.md":
        extra = [("The work is divided into 39 papers", "The work is divided into 40 papers"),
                 ("GH-1, a pair measure on a finite gain graph, is the subject of paper G8.", "GH-1, a pair measure on a finite gain graph, is the subject of paper G8; GH-2, a norm-preserving step on a gain digraph, is the subject of paper G9.")]
    edit(rel, [(OLD + ",", NEW + ",")] + extra, "edition identifier" + ("; third session" if extra else ""))

shutil.copy(os.path.abspath(__file__), os.path.join(OUT, "tools", "director_z_update_3.py")); changes.append(("added", "tools/director_z_update_3.py", "the program that applied these changes"))
changes.append(("added", "REVIEW_RECORDS/Director_Z/Session_3/CHANGES_Z2_TO_Z3.md", "this list")); changes.append(("changed", "MANIFEST.json", "edition identifier, digests"))
with open(os.path.join(OUT, "REVIEW_RECORDS", "Director_Z", "Session_3", "CHANGES_Z2_TO_Z3.md"), "w") as f:
    f.write("# Changes from edition Z2 to edition Z3\n\n12 November 2026. Every other file is byte-identical to edition Z2.\n\n| Change | File | Reason |\n|---|---|---|\n")
    for c in changes: f.write(f"| {c[0]} | `{c[1]}` | {c[2]} |\n")
man = json.load(open(os.path.join(OUT, "MANIFEST.json")))
man["baseline"] = NEW; man["predecessor"] = OLD; man["predecessor_manifest_sha256"] = predecessor_manifest
files = {}
for dp, _, fs in os.walk(OUT):
    for f in sorted(fs):
        rel = os.path.relpath(os.path.join(dp, f), OUT)
        if rel == "MANIFEST.json" or "__pycache__" in rel: continue
        files[rel] = dict(sha256=sha(os.path.join(OUT, rel)), size=os.path.getsize(os.path.join(OUT, rel)))
man["files"] = dict(sorted(files.items()))
json.dump(man, open(os.path.join(OUT, "MANIFEST.json"), "w"), indent=1, ensure_ascii=False)
print("edition Z3:", len(files), "files;", len(reg), "registry rows;", n7, n8, n9, "pages in G7, G8, G9;", total_new, "assembled pages")
