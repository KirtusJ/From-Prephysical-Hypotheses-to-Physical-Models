"""Write the two call files of review Z31. Usage: mk31.py REPO_ROOT OUT_DIR"""
import json,hashlib,sys,os
R,O=sys.argv[1],sys.argv[2]
h=lambda p: hashlib.sha256(open(os.path.join(R,p),'rb').read()).hexdigest()
W="Director_Z/computation/Product_Events/four_gains/winding/"; D="Director_Z/papers/drafts/"
P={"g10":"Director_Z/papers/G10_Histories_as_Events.pdf","add":"Director_Z/addenda/ADDENDUM_EDITION_Z31_SESSION_4.md",
   "bp":W+"builder_three_classes/PROOFS.md","br":W+"builder_three_classes/results_run1.json","bw":W+"builder_three_classes/results_wprime1.json",
   "cp":D+"review_winding_proof/result_small_1.json","c3":D+"review_winding_three/s3_results.jsonl","c1":D+"review_winding_three/s1s2_results.jsonl",
   "pl":W+"plots/plots_record.json","p1":W+"plots/dimension_ring4_three_classes.svg","lean":"Director_Z/lean/WindingAxis.lean"}
N={"g10":"paper_G10_revision_27","add":"addendum_Z31","bp":"builder_three_proofs","br":"builder_three_result","bw":"builder_wprime_result","cp":"challenger_proof_result","c3":"challenger_three_ranks","c1":"challenger_three_walks","pl":"plots_record","p1":"plot_dimension_ring4","lean":"lean_winding_axis"}
words="Make sure to utilize the mathematics and science modules of PCP especially Graphing and Projections along your stack"
a=[{"name":"acr_artifact","arguments":{"text":words,"name":"principal_module_instruction","origin":"SUPPLIED"}}]
a+=[{"name":"acr_artifact","arguments":{"path":P[k],"name":N[k],"origin":"PRODUCED"}} for k in P if k!="lean"]
json.dump(a,open(os.path.join(O,"c31a.json"),"w"),indent=1)
A={k:h(p) for k,p in P.items()}
ref=lambda k:{"ref":{"sha256":A[k],"t":"artifact"}}
sub=lambda kind,body:{"name":"acr_submit","arguments":{"kind":kind,"body":body}}
claims=[
 {"label":"A","kind":"DERIVATION","origin":"TARGET_TEXT","text":"G10 Proposition 5.60 with its written proof (three groups on two levels, M at least 8, delta of finite order) and Theorem 5.61 (two classes of winding) without that proposition as a hypothesis.","criterion":"Supported in scope if the proof follows on reading tick by tick and a rebuild from the paper text alone meets every request examined."},
 {"label":"B","kind":"DERIVATION","origin":"TARGET_TEXT","text":"G10 Lemma 5.54(iii), Corollary 5.57, Lemma 5.59 and Theorem 5.62: the sharper winding inequality, three levels on one rail force two on the other, invariance without preparation, and for three or more classes the rule on multisets in two adjacent cosets.","criterion":"Supported in scope if each proof follows on reading, the exchanged walks satisfy every step in the range examined and exact ranks equal the statement."},
 {"label":"C","kind":"DERIVATION","origin":"TARGET_TEXT","text":"The one-gain construction deposits walks of one number of left steps at the target (used in G10 Proposition 5.58).","criterion":"Conditional unless the stage statements of the one-gain note are proved here; supported as a conditional if the inference from those statements is valid for every stage."},
 {"label":"D","kind":"DERIVATION","origin":"TARGET_TEXT","text":"For three or more classes of winding a consistent site-independent rule equals a combination of the count and the squares on the multisets that meet three cosets.","criterion":"Supported only by a proof; computations on single rings leave it unresolved."}]
b=[sub("REVIEW_COMMISSIONED",{"arrangement":"UNARY","author":"assistant","claims":claims,"director":"principal","expectation":"NO_DIRECTIONAL_EXPECTATION","extent":"PARTIAL","label":"Z31","modules":MODS,"procedure":"FOCUSED","required_gates":["G1","G5","G6"],"target":{"sha256":A["g10"],"t":"artifact"},"title":"Twenty-seventh revision of paper G10: proofs for the hypotheses of edition Z30; three or more classes of winding"}) for MODS in [json.loads(os.environ.get("MODS",'["mathematics","science"]'))]]
ins=[("g10","the subsection on the winding (Lemma 5.53 to Remark 5.63) read line by line in the typeset paper"),("add","all of it; written by this participant"),("bp","all of it; Theorem A, Proposition N and Lemma W' read step by step"),("br","rerun by this participant in a fresh folder, byte-identical"),("bw","rerun by this participant in a fresh folder, byte-identical"),("cp","rerun by this participant in a fresh folder, byte-identical"),("c3","rerun by this participant in a fresh folder, byte-identical"),("c1","rerun by this participant in a fresh folder, byte-identical"),("pl","produced by this participant's program; the three receipts read, exit 0 each"),("p1","rendered and looked at by this participant"),("lean","rerun by this participant: exit 0, standard axioms")]
for k,e in ins: b.append(sub("INSPECTION_DECLARED",{"extent":e,"ref":{"sha256":A[k],"t":"artifact"}}))
b.append(sub("GATE_COMMITTED",{"basis":[],"gate":"G1","note":None,"review":"Z31"}))
objs=[("O38","A","Replays reach orders of delta up to 4 and M up to 20; rings with M at most 7 are open; all reviewers share the participant's model family."),
      ("O39","C","Rests on the stage statements of Director G's one-gain note, whose short stages are stated by test and are not reproved here."),
      ("O40","D","No proof on any ring; a builder's exact ranks leave one dimension undecided on rings of 3, 5 and 6 sites in searches that are sampled; the ring of 4 sites agrees to the sizes examined.")]
for i,c,t in objs: b.append(sub("OBJECTION_RAISED",{"basis":[],"claim":c,"id":i,"review":"Z31","text":t}))
for i,c,t in objs: b.append(sub("OBJECTION_RESOLVED",{"basis":[],"how":"Stands. The paper and the addendum state the limit.","id":i,"resolution":"OPEN_RECORDED"}))
rel={"author":"assistant","exposure":"NOT_OBSERVED","label":"SELF_CHECK","lineage":"SAME"}
def fin(i,c,disp,basis,cond,left):
    return sub("FINDING_RECORDED",{"basis":[ref(x) for x in basis],"claim":c,"conditions":cond,"contrary":[],"disposition":disp,"estimate":None,"execution":"REASONED","grounding":"SUPPLIED_ONLY","grounding_observed":"SUPPLIED_ONLY","id":i,"left_open":left,"noncritical":[],"relation":rel,"review":"Z31","session":1,"supersedes":None})
b+=[fin("F94","A","SUPPORTED_IN_SCOPE",["g10","cp","lean"],[],"Rings with M at most 7."),
    fin("F95","B","SUPPORTED_IN_SCOPE",["g10","bp","c3","c1"],[],"Multisets that meet three cosets."),
    fin("F96","C","CONDITIONAL",["g10"],["the stage statements of the one-gain note of Director G"],"A proof of those statements for the short stages."),
    fin("F97","D","UNRESOLVED",["br","pl"],[],"The converse on multisets that meet three cosets, on every ring.")]
b.append(sub("GATE_COMMITTED",{"basis":[],"gate":"G5","note":"Each claim has a finding; three objections are recorded open.","review":"Z31"}))
b.append(sub("GATE_COMMITTED",{"basis":[],"gate":"G6","note":"Deliverable checked: paper G10 revised a twenty-seventh time (70 pages, 63 labelled statements), programs, plots, review records, and edition Z31 assembled from edition Z30 by a program, with verify_baseline.py run before the push.","review":"Z31"}))
b.append(sub("REVIEW_CLOSED",{"examined_extent":"PARTIAL","lifecycle":"CLOSED_COMPLETE","note":None,"review":"Z31"}))
json.dump(b,open(os.path.join(O,"c31b.json"),"w"),indent=1); print(len(a),len(b))
