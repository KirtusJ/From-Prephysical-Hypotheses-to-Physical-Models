"""Write the call files of review Z33. Usage: mk33.py REPO_ROOT OUT_DIR"""
import json,hashlib,sys,os
R,O=sys.argv[1],sys.argv[2]
h=lambda p: hashlib.sha256(open(os.path.join(R,p),'rb').read()).hexdigest()
P={"g10":"Director_Z/papers/G10_Histories_as_Events.pdf","draft":"Director_Z/papers/drafts/G10_subsection_winding_products.tex",
   "four":"Director_Z/pcp_workers/2026-11-15b_four_classes/FINDINGS.md","lean":"Director_Z/pcp_workers/2026-11-15b_four_classes/run_2026-11-15c/Bezout2.lean",
   "gxr":"Director_Z/cross_review/2026-11-15_G_on_Z32/RECHECK.md"}
a=[{"name":"acr_artifact","arguments":{"path":P[k],"name":"z33_"+k,"origin":"PRODUCED"}} for k in P]
json.dump(a,open(os.path.join(O,"c33a.json"),"w"),indent=1)
A={k:h(p) for k,p in P.items()}
ref=lambda k:{"ref":{"sha256":A[k],"t":"artifact"}}
sub=lambda kind,body:{"name":"acr_submit","arguments":{"kind":kind,"body":body}}
MODS=[{"id":"acr.mathematics","sha256":"8da02f39bd7f91a6f3768644695e6d51739ac9cd5216f606f32647eac5c03361","version":"1.0"},{"id":"acr.science","sha256":"e1a3466816fb4b57e787ed91e51dd2f1c3a67eca5fb8d033900e31f07c5b417e","version":"1.0"}]
claims=[{"label":"A","kind":"DERIVATION","origin":"TARGET_TEXT","text":"G10 Proposition 5.73 (the schema): coincidences of products whose polynomials h_t have greatest common divisor m force a consistent rule on products to be the count and the squares.","criterion":"Supported in scope if the proof follows on reading and a reviewer outside the author's model family finds no defect of substance."},
 {"label":"B","kind":"DERIVATION","origin":"TARGET_TEXT","text":"G10 Theorem 5.74: four, five and six classes of winding, both twists, on products.","criterion":"Supported in scope if the schema holds and the coincidences, the polynomials h_t and a Bezout relation are checked in Lean."},
 {"label":"C","kind":"DERIVATION","origin":"TARGET_TEXT","text":"Corrections to Corollary 5.65 from the cross-reviews of edition Z32 (pooled totals as a sum of four minors; Hurwitz indexing; empty root list).","criterion":"Supported in scope if each corrected sentence is true on reading and on the reviewers' examples."}]
b=[sub("REVIEW_COMMISSIONED",{"arrangement":"UNARY","author":"assistant","claims":claims,"director":"principal","expectation":"NO_DIRECTIONAL_EXPECTATION","extent":"PARTIAL","label":"Z33","modules":MODS,"procedure":"FOCUSED","required_gates":["G1","G5","G6"],"target":{"sha256":A["g10"],"t":"artifact"},"title":"Twenty-ninth revision of paper G10: the schema, four to six classes on products, corrections from cross-review"})]
ins=[("g10","Proposition 5.73, Theorem 5.74 and Corollary 5.65 read in the typeset paper"),("draft","all of it; written by this participant"),("four","read; the worker's schema and pairs"),("lean","rerun by this participant, exit 0"),("gxr","written by this participant; Director G's checkers rerun")]
for k,e in ins: b.append(sub("INSPECTION_DECLARED",{"extent":e,"ref":ref(k)["ref"]}))
b.append(sub("GATE_COMMITTED",{"basis":[],"gate":"G1","note":None,"review":"Z33"}))
objs=[("O45","A","Reviewed outside the model family by Director G (Codex) and Session B (GPT-6) on the PR thread; their records are not in this register."),
      ("O46","B","Seven and more classes open; multisets that are not products open.")]
for i,c,t in objs: b.append(sub("OBJECTION_RAISED",{"basis":[],"claim":c,"id":i,"review":"Z33","text":t}))
for i,c,t in objs: b.append(sub("OBJECTION_RESOLVED",{"basis":[],"how":"Stands. The paper states the limit.","id":i,"resolution":"OPEN_RECORDED"}))
rel={"author":"assistant","exposure":"NOT_OBSERVED","label":"SELF_CHECK","lineage":"SAME"}
def fin(i,c,basis,left):
    return sub("FINDING_RECORDED",{"basis":[ref(x) for x in basis],"claim":c,"conditions":[],"contrary":[],"disposition":"SUPPORTED_IN_SCOPE","estimate":None,"execution":"EXECUTED","grounding":"SUPPLIED_ONLY","grounding_observed":"SUPPLIED_ONLY","id":i,"left_open":left,"noncritical":[],"relation":rel,"review":"Z33","session":1,"supersedes":None})
b+=[fin("F102","A",["g10","draft"],"Records of the outside reviewers are on the PR thread only."),fin("F103","B",["g10","four","lean"],"Seven and more classes."),fin("F104","C",["g10","gxr"],"None.")]
b.append(sub("GATE_COMMITTED",{"basis":[],"gate":"G5","note":"Each claim has a finding; two objections recorded open.","review":"Z33"}))
b.append(sub("GATE_COMMITTED",{"basis":[],"gate":"G6","note":"Deliverable checked: G10 revised a twenty-ninth time; edition Z33 assembled from Z32 by a program; verify_baseline.py run before the push.","review":"Z33"}))
b.append(sub("REVIEW_CLOSED",{"examined_extent":"PARTIAL","lifecycle":"CLOSED_COMPLETE","note":None,"review":"Z33"}))
json.dump(b,open(os.path.join(O,"c33b.json"),"w"),indent=1); print(len(a),len(b))
