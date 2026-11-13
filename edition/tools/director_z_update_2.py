#!/usr/bin/env python3
"""Apply the Director Z changes of the second session of 12 November 2026 to a copy of edition Z1, giving edition Z2.
Arguments: build directory (manuscripts, computation, records, map, trial, director packets), copy of edition Z1.  Rewrites MANIFEST.json last."""
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
OLD, NEW = "FPHPM-BASELINE-2026-11-12-Z1", "FPHPM-BASELINE-2026-11-12-Z2"
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
PDF7 = P7 + "/G7_Transport_Holonomy_and_Monodromy_as_Bridge_Candidates_between_Classica.pdf"; PART7 = P7 + "/parts/01_G7_manuscript.pdf"
PDF8 = P8 + "/G8_Gauge_Invariant_Pair_Measures_on_Gain_Graphs_and_the_Squared_Amplitude_Rule.pdf"; PART8 = P8 + "/parts/01_G8_manuscript.pdf"
for pdf, part, pd, g, why in ((PDF7, PART7, P7, "g7", "paper G7, revised"), (PDF8, PART8, P8, "g8", "paper G8")):
    name = g.upper() + "_manuscript"
    put(os.path.join(SRC, g, name + ".pdf"), pdf, why); put(os.path.join(SRC, g, name + ".pdf"), part, why)
    for f in (name + ".tex", "body.tex", "Scientific_Preamble.tex"): put(os.path.join(SRC, g, f), pd + "/source/" + f, why)
def pages_of(pdf, labels):
    """page of the bold theorem head carrying each label"""
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
for f in sorted(os.listdir(os.path.join(SRC, "comp"))): put(os.path.join(SRC, "comp", f), ba + f, "computation cited by papers G7 and G8")
rr = os.path.join(OUT, "COMPUTATION", "RERUN_RECORD_2026-11-12.csv")
with open(rr, newline="") as f: rows = list(csv.DictReader(f))
R = lambda p, s, n: dict(program=p, status="RAN_OK", stored_output_compared="yes", stdout_equals_stored=s, note=n)
rows += [R("Baseline_Additions/verify_reconciliation_and_phase_recovery.py (fresh directory)", "result file byte-identical", "11 predicates; added in edition Z2"),
         R("Baseline_Additions/verify_galois_conjugate_embeddings.py (fresh directory)", "result file byte-identical", "7 predicates; added in edition Z2"),
         R("Baseline_Additions/verify_gain_graph_pair_measures.py (fresh directory)", "result file byte-identical", "15 predicates; added in edition Z2"),
         R("Baseline_Additions/verify_second_round_director_items.py (fresh directory, with transition_geometry_lib.py)", "result file byte-identical", "6 predicates; added in edition Z2"),
         R("REVIEW_RECORDS/Directors_A_B_G_2026-11-12: packet verifiers and verification programs of the six packets (copies, outputs redirected)", "stored results reproduced as reported by each program", "rerun for edition Z2"),
         R("verify_baseline.py on edition Z1 as received", "BASELINE_CHECK_PASS 657 files", "intake for edition Z2")]
wcsv(rr, rows); changes.append(("changed", "COMPUTATION/RERUN_RECORD_2026-11-12.csv", "six rows appended"))
ci = rd("COMPUTATION_INDEX.csv")
for r in ci:
    if r["directory"] == "COMPUTATION/Baseline_Additions": r["papers"] = "D8 G7 G8"
wcsv("COMPUTATION_INDEX.csv", ci); changes.append(("changed", "PROGRAM/registers/COMPUTATION_INDEX.csv", "paper G8 entered"))

# ---- registers: theorem registry
reg = rd("THEOREM_REGISTRY.csv")
ST7 = [("Proposition", "3.1"), ("Proposition", "4.1"), ("Lemma", "4.2"), ("Proposition", "4.3"), ("Corollary", "4.5"), ("Theorem", "5.1"), ("Proposition", "7.1"), ("Theorem", "7.2"), ("Corollary", "7.3")]
NEW7 = [("Proposition", "4.6", "Fan of thin triangles: recovery of the Bargmann phase from holonomy determinants"),
        ("Corollary", "4.7", "Transition probabilities determine all Bargmann phases up to one conjugation"),
        ("Proposition", "5.4", "Generators and observables are equal in number exactly for complex quantum theory"),
        ("Proposition", "7.4", "Conjugate embeddings: a second invariant transition probability on the orbit of a dense group"),
        ("Proposition", "8.1", "Minimal and quantum composites of two qubits share the single-system data"),
        ("Proposition", "8.2", "Relative orientation of complex structures is fixed by the composite")]
n7, pg7 = pages_of(PDF7, [f"{k} {n}" for k, n in ST7] + [f"{k} {n}" for k, n, _ in NEW7])
for r in reg:
    if r["paper"] == "G7":
        p = pg7[f"{r['kind']} {r['number']}"]; r["paper_file_page"] = r["part_page"] = str(p)
        if r["number"] == "4.5": r["name"] = "Transition probabilities determine the Bargmann phase power up to conjugation"
for i, (k, num, name) in enumerate(NEW7, 10):
    reg.append(dict(id=f"G7-01-{i:02d}", paper="G7", part="1", part_title=T7, kind=k, number=num, name=name, status="PROOF_IN_MANUSCRIPT", paper_file_page=str(pg7[f"{k} {num}"]), part_page=str(pg7[f"{k} {num}"]), legacy_locator=""))
ST8 = [("Lemma", "3.1", "Additive switching-invariant functions on walks do not depend on the gains"),
       ("Theorem", "4.1", "Invariant pair rules are class functions of the pair holonomy; strong positivity is non-negativity of character coefficients"),
       ("Corollary", "4.2", "Squared-norm form of the extreme pair measures"),
       ("Corollary", "4.3", "Second-order interference present, third and higher orders absent"),
       ("Proposition", "5.1", "Hilbert space and transition probability of a pair measure; density under a growth condition"),
       ("Proposition", "6.1", "The product of gain graphs gives the tensor product"),
       ("Proposition", "7.1", "Walks with distinct records give the counting measure"),
       ("Proposition", "8.1", "Independence of the faithful cyclic character exactly for orders 1, 2, 3, 4, 6")]
n8, pg8 = pages_of(PDF8, [f"{k} {n}" for k, n, _ in ST8])
for i, (k, num, name) in enumerate(ST8, 1):
    reg.append(dict(id=f"G8-01-{i:02d}", paper="G8", part="1", part_title=T8, kind=k, number=num, name=name, status="PROOF_IN_MANUSCRIPT", paper_file_page=str(pg8[f"{k} {num}"]), part_page=str(pg8[f"{k} {num}"]), legacy_locator=""))
wcsv("THEOREM_REGISTRY.csv", reg)
# ---- paper index, crosswalk, citations, readiness
index = rd("PAPER_INDEX.csv"); old7 = None
for r in index:
    if r["id"] == "G7": old7 = int(r["pages"]); r.update(pages=str(n7), statements="15", cites_papers="G3 G6 G8")
g7row = [r for r in index if r["id"] == "G7"][0]
index.insert(index.index(g7row) + 1, dict(id="G8", series=g7row["series"], title=T8, kind="article", file=PDF8, pages=str(n8), parts="1", statements="8", cites_papers="G3 G6 G7"))
wcsv("PAPER_INDEX.csv", index)
cross = rd("COMPONENT_CROSSWALK.csv")
for c in cross:
    if c["paper"] == "G7": c.update(baseline_sha256=sha(os.path.join(OUT, PART7)), pages=str(n7), change="first issued with edition Z1; revised in edition Z2")
cross.append(dict(paper="G8", part="1", title=T8, kind="new", legacy_path="", legacy_volume="", legacy_volume_pages="", legacy_sha256="", baseline_path=PART8,
                  baseline_sha256=sha(os.path.join(OUT, PART8)), pages=str(n8), change="first issued with edition Z2", editable_sources="3"))
wcsv("COMPONENT_CROSSWALK.csv", cross)
cit = rd("CITATIONS_BETWEEN_PAPERS.csv")
C = lambda a, b, t: dict(citing_paper=a, citing_part="1", cited_paper=b, cited_part="1", cited_title=t, evidence="title mention", locator="")
T3 = "Finite Signed Graphs and Binary Extension Constraints"; T6 = "Invariant Relational Selection and Approximate Symmetry"
cit += [C("G7", "G3", T3), C("G7", "G8", T8), C("G8", "G3", T3), C("G8", "G6", T6), C("G8", "G7", T7)]
wcsv("CITATIONS_BETWEEN_PAPERS.csv", cit)
ready = rd("READINESS.csv")
for r in ready:
    if r["paper"] == "G7": r.update(pages=str(n7), labelled_statements="15", gaps="revised in edition Z2; proofs not independently refereed; quoted inputs partly inspected in extracts and bibliographic details partly unverified (OP-17)")
g7r = [r for r in ready if r["paper"] == "G7"][0]
ready.insert(ready.index(g7r) + 1, dict(paper="G8", title=T8, kind="article", pages=str(n8), parts="1", parts_with_editable_source="1", labelled_statements="8", independent_referee_report="none",
                                        gaps="first issued with edition Z2; proofs not independently checked; growth condition of Proposition 5.1 not proved for a class of graphs; bibliographic details partly unverified (OP-25)"))
wcsv("READINESS.csv", ready)

# ---- open problems
ops = rd("OPEN_PROBLEMS.csv")
for r in ops:
    if r["id"] == "OP-10":
        r["statement"] = r["statement"].replace("leaves a cap of angular radius 10.48 degrees uncovered (G7-01-07)", "leaves a cap of angular radius arccos(59/60) = 10.475 degrees uncovered, 14.835 degrees for orbits of rotation groups (G7-01-07)")
        r["statement"] += " Edition Z2: for the second and third forms paper G8 gives a construction conditional on stated assumptions (events of unbounded walk length on a finite gain graph give, under a growth condition, a dense inhomogeneous subset of a complex or real projective space; G8-01-05); Directors A and B record inhomogeneous nets of an imported geometry. A connected group acting on the limit, and tomographic locality as a principle, are not obtained."
    if r["id"] == "OP-11":
        r["statement"] = r["statement"].replace("inside the class of single-system theories without third-order interference", "inside the class of non-classical single-system theories with classical decomposability, strong symmetry and no third-order interference")
        r["statement"] = r["statement"].replace("(the commutant of the Levi-Civita holonomy group of the transition-probability geometry, with monodromy)", "(the commutant of the Levi-Civita holonomy group of the transition-probability geometry, which for the real three-level theory requires the monodromy of a non-contractible loop; the curvatures 1 and 4 separate that theory from the qubit locally)")
        r["statement"] += " Edition Z2: the transition probabilities determine all Bargmann phases up to one conjugation (G7-01-10, G7-01-11); on a gain graph the pair measures are squared norms in a representation of real, complex or quaternionic type, all of which occur (G8-01-02, G8-01-03). No selection of the complex case."
    if r["id"] == "OP-17":
        r["statement"] += " Edition Z2: inspected in retrieved text: Gelander (journal version; the corollary is 1.3), the isotropy and holonomy of the quaternionic projective spaces and of the octonionic plane, the curvature range, the three postulates of Barnum-Mueller-Ududec, Boykin et al., Lavi, Li-Wagner-Zhang, Selinger, Baez; the classification of finite subgroups of O(3) was inspected by Directors B and G. Three statements of edition Z1 were corrected after the review of Directors A, B and G. Still from recall: the dimensions used in G7-01-12, the innerness of continuous automorphisms of SO(3), and the bibliographic details listed in the Director Z second-session disposition, section 7. The proofs remain unrefereed."
        r["state"] = "open; partly discharged in edition Z2"
    if r["id"] == "OP-18":
        r["statement"] += " Edition Z2: the symplectic form, the complex holonomy commutant, a dynamical correspondence (Alfsen-Shultz) and observability of energy are forms of one requirement, and equality of the numbers of generators and observables is necessary for it (G7-01-12). A warrant for the requirement is not identified."
    if r["id"] == "OP-19":
        r["statement"] = r["statement"].replace(" For a geodesic polygon whose vertices span the space, a transport construction of the Bargmann phase itself, beyond its (n+1)-th power, is also not given.", "")
        r["statement"] += " Edition Z2: the transport construction of the Bargmann phase itself is given (G7-01-10). Paper G8 gives a conditional construction for the second and third forms with a composition rule (G8-01-05, G8-01-06); open are a reason for the second order of the rule, for the record role of end vertices and for the group and representation, the growth condition, and any construction for the first form that does not import the geometry."
        r["state"] = "open; one item closed, one conditional construction"
O = lambda i, sc, ty, st, state: dict(id=i, scope=sc, type=ty, statement=st, state=state)
ops += [O("OP-20", "G7 G8", "foundations", "Orientation. The transition probabilities leave one conjugation per system undetermined (G7-01-11); conjugating a whole model changes no outcome probability (Director B, B2); a composite fixes the relative orientations of its parts, which form a balanced signing (G7-01-15). What fixes the relative orientations in a structure specified without quantum data, and which equivalence relation a candidate is required to respect, are not identified.", "not identified"),
        O("OP-21", "G7 G8", "foundations", "Ordering of values. Algebraic generating data determine transition probabilities only up to field automorphisms (G7-01-13); for cyclic phases the pair measure is independent of the faithful character only for orders 1, 2, 3, 4, 6 (G8-01-08). A principle that supplies the ordering of the values of a probability, or that confines the data to the rational, Gaussian or Eisenstein fields, is not given. A directed three-cycle yields the Eisenstein field and equally a classical simplex (Director A, A2).", "not identified"),
        O("OP-22", "G7 G8", "foundations", "Composition. Single-system data are shared by the minimal composite, the quantum composite and the interpolated family K_t (G7-01-14; Directors B and G); the uniform four-system extension of K_t fails closure under parallel preparation by t(1-t)/4 (Director G); closure under local unitaries and a controlled-not forces the quantum composite once a complex representation is given (Director G; rerun, not reproved). The product of gain graphs gives the full tensor product with a common step count (G8-01-06). A principle selecting the composite, multipartite closure, and the origin of entangling operations are not derived.", "open"),
        O("OP-23", "program", "foundations", "Dynamics, clock and classical limit. Static transition-probability geometry selects no generator and no clock (Director A). In the constructed trial GH-1 walk length is not a unitary evolution and only the counting measure of recorded walks is obtained on the classical side (paper G8, Section 9). No reversible dynamics, calibrated time or classical Hamiltonian mechanics has been obtained from any structure of the program.", "open"),
        O("OP-24", "REVIEW_RECORDS", "method", "No Director session has had a sub-agent facility; every review inside a stack is a self-check. Directors A, B and G (GPT-6) and Director Z (Claude) worked from shared sources. Three errors of edition Z1 were found by the other Directors and not by the self-check of Director Z; this is one observation, not a measurement of the method. The ACR packet was not among the inputs of the second Director Z session. Independent review by qualified mathematicians and physicists is outstanding for every paper.", "open"),
        O("OP-25", "G8", "manuscript", "Independent verification of the proofs of paper G8; a proof of the growth condition of G8-01-05 for a stated class of gain graphs; verification of the bibliographic details written from memory (Zaslavsky, Huang, Sinha et al., Boes-Navascues, Serre, authorship of arXiv 2111.12428).", "open")]
wcsv("OPEN_PROBLEMS.csv", ops)
for n, why in (("PAPER_INDEX.csv", "paper G7 revised; paper G8 entered"), ("THEOREM_REGISTRY.csv", "G7 pages updated, six G7 rows and eight G8 rows added"), ("COMPONENT_CROSSWALK.csv", "G7 digest; paper G8 entered"),
               ("CITATIONS_BETWEEN_PAPERS.csv", "five citations added"), ("READINESS.csv", "paper G7 revised; paper G8 entered"), ("OPEN_PROBLEMS.csv", "OP-10, OP-11, OP-17, OP-18, OP-19 amended; OP-20 to OP-25 added")):
    changes.append(("changed", "PROGRAM/registers/" + n, why))

# ---- bridge register
bp = os.path.join(REG, "BRIDGE_CANDIDATE_REGISTER.json"); br = json.load(open(bp))
br["author"] = "LLM Director D (Claude, Anthropic) and LLM Director Z (Claude, Anthropic) at the direction of Kirtus Justus; entries marked Director A, B or G follow review records prepared with GPT-6 (OpenAI)"
br["nodes"]["PRE-GAIN"] = "finite gain graphs: a group element on each oriented edge of a finite graph, up to switching; signed graphs are the case of the group of order two [Zaslavsky; papers G3, G8]"
br["nodes"]["QMS"] = "quantum measure systems: a strongly positive bi-additive function on events, with its Hilbert space [Sorkin 1994; Dowker–Johnston–Sorkin 2010]"
br["nodes"]["COMPOSITES"] = "candidate composites of two systems with given single-system theory: minimal, interpolated K_t, quantum [Director B; Director G; paper G7 Section 8]"
br["nodes"]["GPT-NO-I3"] += " Director A reports, from Barnum–Hilgert 2020, that spectrality and strong symmetry already give this list; not inspected by Director Z."
for e in br["edges"]:
    if e["statement"].startswith("Sorkin third-order interference"):
        e["status"] += "; the exclusion of PR-box and pentagon correlations is a result for quantum logics with unique conditional probabilities and further postulates (Niestegge), not for arbitrary theories (Director A, A-11)"
    if e["statement"].startswith("The commutant of the Levi-Civita holonomy group"):
        e["statement"] += " The metrics are not locally isometric: curvature 1 for RP^2 and 4 for the qubit with d = arccos sqrt p (Directors A, B, G; G7 Remark 5.2). The numbers of generators and of observables modulo constants agree exactly for the complex theories (G7-01-12)."
        e["status"] = "holonomy and isotropy groups of HP^n and OP^2 inspected in extracts; RP^m for m >= 3 quoted; presupposes the transition-probability geometry"
    if e["statement"].startswith("Finite carriers with a transitive symmetry group"):
        e["statement"] = e["statement"].replace("leaves a cap of radius arccos(59/60) uncovered", "leaves a cap of radius arccos(59/60) = 10.475 degrees uncovered (arccos(29/30) = 14.835 degrees for rotation orbits; Director G)")
        e["locator"] = "Paper G7, G7-01-07 to G7-01-09; Turing, Ann. Math. 39 (1938) 105; Gelander, L'Enseignement Math. 59 (2013) 195, Theorem 1.1 and Corollary 1.3"
    if e["statement"].startswith("Forms of a finite-to-continuum limit"):
        e["status"] = "the trial imports its generators; a conditional construction for the second and third forms is in paper G8"
E = lambda **k: br["edges"].append(k)
E(**{"from": "QT", "to": "QT", "type": "exact_correspondence", "statement": "The transition probabilities of CP^n determine every Bargmann phase up to one conjugation common to all polygons: the phase is the product over a fan of thin triangles of the roots nearest 1 of their holonomy determinants. Three overlaps alone do not determine a triple phase in CP^2 (Director A), and the determinant of one loop loses a root of unity (Director B, B2).", "locator": "Paper G7, G7-01-10, G7-01-11; verify_reconciliation_and_phase_recovery.py B; verify_second_round_director_items.py F3", "status": "PROOF_IN_MANUSCRIPT; executed; uniqueness also follows from Wigner's theorem"})
E(**{"from": "PRE-REL", "to": "QT", "type": "obstruction", "statement": "Algebraic generating data do not determine the transition probability: the group generated by H and T carries on its orbit both p and its image under the field automorphism zeta -> zeta^3, with the same completion and no uniformly continuous identification. An ordering of the values has to be supplied.", "locator": "Paper G7, G7-01-13; verify_galois_conjugate_embeddings.py", "status": "PROOF_IN_MANUSCRIPT; exact arithmetic; density of the group quoted"})
E(**{"from": "QT", "to": "COMPOSITES", "type": "obstruction", "statement": "Single-system transition probabilities, holonomies and reversible transformations are shared by the minimal composite, the family K_t = (1-t) Sep + t Q and the quantum composite; the uniform four-system extension of K_t fails closure under parallel preparation by t(1-t)/4. A composite fixes the relative orientation of the complex structures of its parts; relative orientations form a balanced signing.", "locator": "Paper G7, G7-01-14, G7-01-15; Director B (B-COMP-05); Director G (DG-COMP-01 to 03); verify_second_round_director_items.py F4", "status": "PROOF_IN_MANUSCRIPT for G7; Director G statements recomputed for the gap and the bounds"})
E(**{"from": "PRE-GAIN", "to": "GPT-CLASSICAL", "type": "exact_correspondence", "statement": "A switching-invariant additive function on walks is a multiple of the count; walks that leave distinct records have the counting measure under any pair rule.", "locator": "Paper G8, G8-01-01, G8-01-07", "status": "PROOF_IN_MANUSCRIPT; counting measure only, no Hamiltonian mechanics"})
E(**{"from": "PRE-GAIN", "to": "QMS", "type": "exact_correspondence", "statement": "A pair rule on walks with a common end vertex is switching invariant exactly when it is a class function of the pair holonomy, and strongly positive exactly when its character coefficients are non-negative; the extreme measures are squared norms of summed representation matrices; third-order interference is absent.", "locator": "Paper G8, G8-01-02 to G8-01-04; verify_gain_graph_pair_measures.py E1 to E3", "status": "PROOF_IN_MANUSCRIPT; conditional on the postulates of the next edge"})
E(**{"from": "PRE-GAIN", "to": "QMS", "type": "postulate", "statement": "Second order of the rule; end vertices as records; one rule for all graphs; strong positivity; the gain group and its irreducible representation; step count.", "locator": "Paper G8, Section 9; CONSTRUCTED_TRIALS/GH-1", "status": "supplied, not derived; real, complex and quaternionic types all occur"})
E(**{"from": "QMS", "to": "QT", "type": "exact_correspondence", "statement": "The Dowker–Johnston–Sorkin construction gives a Hilbert space and a transition probability on classes of events; for cyclic gains of order at least 3 and under a growth condition the rays of events of unbounded walk length are dense in CP^(m-1). The product of gain graphs gives the tensor product.", "locator": "Paper G8, G8-01-05, G8-01-06", "status": "PROOF_IN_MANUSCRIPT; growth condition unproved for a class of graphs; common step count assumed; no operational meaning of the transition probability"})
E(**{"from": "PRE-GAIN", "to": "QT", "type": "obstruction", "statement": "Walk length is not a unitary evolution; long walks converge to one eigenvector; the measure depends on the faithful character unless the cyclic order is 1, 2, 3, 4 or 6. No reversible dynamics, clock or classical Hamiltonian limit.", "locator": "Paper G8, Section 9 and G8-01-08; verify_gain_graph_pair_measures.py E5, E6", "status": "computed instances and one proposition"})
E(**{"from": "PRE-REL", "to": "QT", "type": "obstruction", "statement": "A directed three-cycle gives C = P - P^T with C^2 = -3 on the zero-sum plane, hence the Eisenstein field without a choice of root of unity; the same input supports the classical simplex of three outcomes. Complex-type algebra does not select quantum theory.", "locator": "Director A, A2 (Finite-Cycle Complex Structure and Selection Boundaries); identity recomputed in verify_second_round_director_items.py F1", "status": "Director A record; identity recomputed"})
E(**{"from": "PRE-GAIN", "to": "CM-SYMP", "type": "untested_transfer", "statement": "Two unexamined proposals: gains derived from a graph alone by a discrete Schild's ladder (transport of edge directions across quadrilaterals); stationarity of the holonomy between neighbouring walks as a discrete stationary-phase condition for a classical limit.", "locator": "Director Z second-session disposition, section 5", "status": "speculation; no construction"})
br["obligations_for_any_prephysical_candidate"] += [
    "state which equivalence relation the candidate respects: conjugation of a whole model is unobservable, relative orientation of systems is not",
    "supply the ordering of probability values, or use data whose only field automorphism is complex conjugation",
    "supply a composite closed under parallel preparation for every number of systems, and the origin of entangling operations",
    "supply a reason for the second order of the probability rule and for what counts as a record"]
br["retained_outliers"].update({"icosahedral_full_group_covering_radius_deg_exact_circumradius": 18.7125, "phase_recovery_n4_k5_root_of_whole_polygon_vs_phase": [0.202307, 2.715582],
    "conjugate_embedding_extreme_element_p_and_pconj": [0.9953, 0.0672], "gain_graph_first_draw_I4_of_fourth_order_rule": 0.0,
    "Q8_non_class_weight_change_of_single_set_measure": 0.0, "random_Z4_gain_graph_max_singular_value_ratio": 0.4236})
json.dump(br, open(bp, "w"), indent=1, ensure_ascii=False); changes.append(("changed", "PROGRAM/registers/BRIDGE_CANDIDATE_REGISTER.json", "three nodes, ten edges, four obligations added; four edges amended"))
put(os.path.join(SRC, "map", "ONTOLOGY_GATE_MAP.json"), "PROGRAM/registers/ONTOLOGY_GATE_MAP.json", "gate map")
put(os.path.join(SRC, "map", "Gate_Map_2026-11-12.pdf"), "PROGRAM/figures/Gate_Map_2026-11-12.pdf", "gate map figure")
put(os.path.join(SRC, "map", "gate_map.dot"), "PROGRAM/figures/Gate_Map_2026-11-12.dot", "gate map figure source")

# ---- constructed trial, review records
put(os.path.join(SRC, "trial", "README.md"), "CONSTRUCTED_TRIALS/README.md", "constructed trial GH-1")
put(os.path.join(SRC, "trial", "GH-1_Assumptions_and_Dispositions.json"), "CONSTRUCTED_TRIALS/GH-1/GH-1_Assumptions_and_Dispositions.json", "constructed trial GH-1")
for dp, _, fs in os.walk(os.path.join(SRC, "directors")):
    for f in sorted(fs):
        if "__pycache__" in dp: continue
        rel = os.path.relpath(os.path.join(dp, f), os.path.join(SRC, "directors"))
        put(os.path.join(dp, f), "REVIEW_RECORDS/Directors_A_B_G_2026-11-12/" + rel, "packet of Director A, B or G, as received")
for dp, _, fs in os.walk(os.path.join(SRC, "rec")):
    for f in sorted(fs):
        rel = os.path.relpath(os.path.join(dp, f), os.path.join(SRC, "rec"))
        put(os.path.join(dp, f), "REVIEW_RECORDS/Director_Z/Session_2/" + rel, "Director Z second-session record")

# ---- program documents
def edit(rel, pairs, why):
    p = os.path.join(OUT, rel); s = open(p).read()
    for a, b in pairs:
        assert a in s, (rel, a[:70]); s = s.replace(a, b)
    open(p, "w").write(s); changes.append(("changed", rel, why))
total_old = 606; total_new = total_old - old7 + n7 + n8
for rel in ("PROGRAM/CONTRIBUTIONS.md", "PROGRAM/PAPER_INDEX.md", "PROGRAM/STANDARDS.md", "PROGRAM/CHARTER.md", "REVIEW_RECORDS/README.md", "README.md", "LEGACY/README.md", "NEGATIVE_CONTROLS/README.md"):
    extra = []
    if rel == "PROGRAM/PAPER_INDEX.md":
        extra = [(f"| G7 | {T7} | article | {old7} | 9 |", f"| G7 | {T7} | article | {n7} | 15 |\n| G8 | {T8} | article | {n8} | 8 |")]
    if rel == "PROGRAM/CONTRIBUTIONS.md":
        extra = [("with paper G7; the reconciliation", "with paper G7; the second Director Z session (cross-review of Directors A, B and G, revision of paper G7, paper G8, constructed trial GH-1, gate map); the reconciliation"),
                 ("- **Gemini (Google)", "- **GPT-6 (OpenAI) as LLM Directors A, B and G**: the review records in `REVIEW_RECORDS/Directors_A_B_G_2026-11-12`, including the curvature comparison of the real three-level theory and the qubit, the conjugate triple and the Gram family, the classical-spin scope example, the bound for rotation orbits, the minimal-composite witness, the interpolated composites and their four-system closure failure, the directed three-cycle construction, whole-model conjugation, and the gate list used in the gate map. Points used in papers G7 and G8 are attributed there.\n- **Gemini (Google)")]
    if rel == "REVIEW_RECORDS/README.md":
        extra = [("Directors D and Z under ACR 1.0.", "Directors D and Z under ACR 1.0; Directors A, B and G (12 November 2026, GPT-6) report working under ACR 1.0 as absorbed text. The six packets of Directors A, B and G are kept as received in `Directors_A_B_G_2026-11-12/`; the second Director Z session is in `Director_Z/Session_2/`.")]
    if rel == "README.md":
        extra = [("by 38 papers in seven series (606 assembled pages;", f"by 39 papers in seven series ({total_new} assembled pages;"), ("theorem registry (353 rows)", f"theorem registry ({len(reg)} rows)"),
                 ("component crosswalk, bridge-candidate map.", "component crosswalk, bridge-candidate map, gate map."),
                 ("| `NEGATIVE_CONTROLS/` | withdrawn and stipulated constructions kept as counterexamples |", "| `NEGATIVE_CONTROLS/` | withdrawn and stipulated constructions kept as counterexamples |\n| `CONSTRUCTED_TRIALS/` | models built from stated primitives as test objects, with their assumption ledgers |")]
    if rel == "PROGRAM/CHARTER.md":
        extra = [("The work is divided into 38 papers", "The work is divided into 39 papers"),
                 ("| `COMPUTATION_INDEX.csv` | computation directories against papers |", "| `COMPUTATION_INDEX.csv` | computation directories against papers |\n| `ONTOLOGY_GATE_MAP.json` | the obligations a candidate would have to meet, with the evidence bearing on each; no gate is passed |"),
                 ("They are retained as counterexamples and test objects.", "They are retained as counterexamples and test objects. `CONSTRUCTED_TRIALS/` holds models built from stated primitives to test which parts of the target follow from them; GH-1, a pair measure on a finite gain graph, is the subject of paper G8. A constructed trial is not a candidate ontology.")]
    edit(rel, [(OLD + ",", NEW + ",")] + extra, "edition identifier" + ("; second session" if extra else ""))

shutil.copy(os.path.abspath(__file__), os.path.join(OUT, "tools", "director_z_update_2.py")); changes.append(("added", "tools/director_z_update_2.py", "the program that applied these changes"))
changes.append(("added", "REVIEW_RECORDS/Director_Z/Session_2/CHANGES_Z1_TO_Z2.md", "this list")); changes.append(("changed", "MANIFEST.json", "edition identifier, digests"))
with open(os.path.join(OUT, "REVIEW_RECORDS", "Director_Z", "Session_2", "CHANGES_Z1_TO_Z2.md"), "w") as f:
    f.write("# Changes from edition Z1 to edition Z2\n\n12 November 2026. Every other file is byte-identical to edition Z1.\n\n| Change | File | Reason |\n|---|---|---|\n")
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
print("edition Z2:", len(files), "files;", len(reg), "registry rows;", n7, "pages in G7;", n8, "pages in G8;", total_new, "assembled pages")
