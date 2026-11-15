"""Write the two call files of review Z32. Usage: mk32.py REPO_ROOT OUT_DIR"""
import json,hashlib,sys,os
R,O=sys.argv[1],sys.argv[2]
h=lambda p: hashlib.sha256(open(os.path.join(R,p),'rb').read()).hexdigest()
W="Director_Z/computation/Product_Events/four_gains/winding/"; C="Director_Z/challenger/"; PW="Director_Z/pcp_workers/"
P={"g10":"Director_Z/papers/G10_Histories_as_Events.pdf","draft":"Director_Z/papers/drafts/G10_subsection_winding_products.tex",
   "tp":W+"total_positivity/r_N5_B9.json","pc":W+"total_positivity/r_product_checks.json",
   "ctp":C+"2026-11-15b_tp/REPORT_AND_RECHECK.md","cpr":C+"2026-11-15b_products/REPORT_AND_RECHECK.md","mic":C+"2026-11-15b_micro/REPORT_AND_RECHECK.md",
   "occ":W+"builder_four_groups/run1/res2_cap11_M3to7.txt","occc":PW+"2026-11-15b_occurrence/challenger/DIRECTOR_RECHECK.md",
   "four":PW+"2026-11-15b_four_classes/FINDINGS.md","wild":PW+"2026-11-15b_wildcard_unrolled/r_coincidence_S80.json",
   "small":PW+"2026-11-15b_small_rings/PROOFS.md","lean":"Director_Z/lean/WindingCoincidence.lean"}
N={k:"z32_"+k for k in P}
a=[{"name":"acr_artifact","arguments":{"path":P[k],"name":N[k],"origin":"PRODUCED"}} for k in P]
json.dump(a,open(os.path.join(O,"c32a.json"),"w"),indent=1)
A={k:h(p) for k,p in P.items()}
ref=lambda k:{"ref":{"sha256":A[k],"t":"artifact"}}
sub=lambda kind,body:{"name":"acr_submit","arguments":{"kind":kind,"body":body}}
MODS=[{"id":"acr.mathematics","sha256":"8da02f39bd7f91a6f3768644695e6d51739ac9cd5216f606f32647eac5c03361","version":"1.0"},{"id":"acr.science","sha256":"e1a3466816fb4b57e787ed91e51dd2f1c3a67eca5fb8d033900e31f07c5b417e","version":"1.0"}]
claims=[
 {"label":"A","kind":"DERIVATION","origin":"TARGET_TEXT","text":"G10 Theorem 5.64 and Corollary 5.65: the winding counts at one site of a position product event on a ring form a totally non-negative array; their generating polynomials are real-rooted, and the associated polynomial W has no root in the open right half-plane.","criterion":"Supported in scope if the proof follows on reading, a challenger finds no defect of substance, and every profile enumerated satisfies the corollary."},
 {"label":"B","kind":"DERIVATION","origin":"TARGET_TEXT","text":"G10 Lemmas 5.66 to 5.68, Theorems 5.69 and 5.70: products of multisets in two adjacent cosets occur, a consistent rule on them is the count plus a banded form, and for three classes of winding it is the count and the two squares on all products.","criterion":"Supported in scope if each proof follows on reading, the algebraic steps are checked in Lean, and challengers find no defect of substance."},
 {"label":"C","kind":"DERIVATION","origin":"TARGET_TEXT","text":"G10 Proposition 5.73 and Corollaries 5.72, 5.74: three groups on two levels for M at least 5, and the dependent results with M at least 5.","criterion":"Supported in scope if the construction for M at least 6 follows tick by tick on reading and the table for M = 5 is exclusive in every replay."},
 {"label":"D","kind":"DERIVATION","origin":"TARGET_TEXT","text":"Total positivity is sufficient for a profile to occur, on large rings.","criterion":"Refuted in scope by an allowed profile that occurs at no site; resolved only for the rings searched."}]
b=[sub("REVIEW_COMMISSIONED",{"arrangement":"UNARY","author":"assistant","claims":claims,"director":"principal","expectation":"NO_DIRECTIONAL_EXPECTATION","extent":"PARTIAL","label":"Z32","modules":MODS,"procedure":"FOCUSED","required_gates":["G1","G5","G6"],"target":{"sha256":A["g10"],"t":"artifact"},"title":"Twenty-eighth revision of paper G10: total positivity of the winding, products of multisets, three groups for M at least 5"})]
ins=[("g10","the new subsection (Theorem 5.64 to Corollary 5.74) read in the typeset paper"),("draft","all of it; written by this participant"),("tp","produced and read by this participant"),("pc","produced and read by this participant"),("ctp","the challenger's report and the participant's recheck; program rerun byte-identical"),("cpr","the challenger's report and the participant's recheck; program rerun, equal except timing"),("mic","the micro-review and the participant's recheck by hand"),("occ","rerun by this participant in a fresh folder, byte-identical"),("occc","the second program's result for M = 5 rerun, byte-identical"),("four","read; its three Lean files rerun, exit 0"),("wild","rerun by this participant at both sizes, byte-identical"),("small","Theorem A read tick by tick by this participant; Theorem B's programs rerun, exit 0"),("lean","run by this participant, exit 0")]
for k,e in ins: b.append(sub("INSPECTION_DECLARED",{"extent":e,"ref":ref(k)["ref"]}))
b.append(sub("GATE_COMMITTED",{"basis":[],"gate":"G1","note":None,"review":"Z32"}))
objs=[("O41","A","Part (iii) of the corollary rests on a theorem of Holtz and Tyaglov read only through a secondary account; all reviewers share the participant's model family."),
      ("O42","B","Products only; the rule on multisets that occur and are not products is open; four to six classes computed, seven and more open."),
      ("O43","C","The case M = 5 is a finite table found by search; the dependent results are checked to cite only the statement of the proposition; no reviewer outside the model family has yet read it."),
      ("O44","D","Refuted only for M from 3 to 8 and totals up to 13; larger rings open.")]
for i,c,t in objs: b.append(sub("OBJECTION_RAISED",{"basis":[],"claim":c,"id":i,"review":"Z32","text":t}))
for i,c,t in objs: b.append(sub("OBJECTION_RESOLVED",{"basis":[],"how":"Stands. The paper states the limit.","id":i,"resolution":"OPEN_RECORDED"}))
rel={"author":"assistant","exposure":"NOT_OBSERVED","label":"SELF_CHECK","lineage":"SAME"}
def fin(i,c,disp,basis,left,ex="EXECUTED"):
    return sub("FINDING_RECORDED",{"basis":[ref(x) for x in basis],"claim":c,"conditions":[],"contrary":[],"disposition":disp,"estimate":None,"execution":ex,"grounding":"SUPPLIED_ONLY","grounding_observed":"SUPPLIED_ONLY","id":i,"left_open":left,"noncritical":[],"relation":rel,"review":"Z32","session":1,"supersedes":None})
b+=[fin("F98","A","SUPPORTED_IN_SCOPE",["g10","ctp","tp"],"The quoted half-plane theorem."),
    fin("F99","B","SUPPORTED_IN_SCOPE",["g10","cpr","mic","pc","lean"],"Multisets that are not products; s at least 4 in the paper."),
    fin("F100","C","SUPPORTED_IN_SCOPE",["g10","small"],"Reading of the M = 5 table by a reviewer outside the model family."),
    fin("F101","D","REFUTED_IN_SCOPE",["occ","occc"],"Rings with M at least 9.")]
b.append(sub("GATE_COMMITTED",{"basis":[],"gate":"G5","note":"Each claim has a finding; four objections are recorded open.","review":"Z32"}))
b.append(sub("GATE_COMMITTED",{"basis":[],"gate":"G6","note":"Deliverable checked: paper G10 revised a twenty-eighth time, programs, Lean files and review records; edition Z32 assembled from Z31 by a program, verify_baseline.py run before the push.","review":"Z32"}))
b.append(sub("REVIEW_CLOSED",{"examined_extent":"PARTIAL","lifecycle":"CLOSED_COMPLETE","note":None,"review":"Z32"}))
json.dump(b,open(os.path.join(O,"c32b.json"),"w"),indent=1); print(len(a),len(b))
