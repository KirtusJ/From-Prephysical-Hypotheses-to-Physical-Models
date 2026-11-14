"""CHAOS test 2: program mutants. Predictions in the table are fixed before the run. Scratch copies only."""
import os, subprocess, hashlib, json, shutil, sys
W=os.path.dirname(os.path.abspath(__file__)); S=os.path.join(W,'prog_BASE_stored')
V=os.path.join(S,'Vertex_Law'); E=os.path.join(S,'edge_record_walk')
M=[
("P1","edge",'after[(x-1) % n][1] = r-l','after[(x-1) % n][1] = r+l',"sign flipped in the walk step","program asserts (norm, brute words)","CAUGHT by assert"),
("P2","edge",'range(min(10, limit+2)+1)','range(min(10, limit+2))',"off-by-one: brute-word loop one depth short","byte comparison","passes, file differs"),
("P3","edge",'assert not any(r["failed_sites"] for r in results["square"])','assert not all(r["failed_sites"] for r in results["square"])',"predicate weakened any -> all","nothing but the source digest","passes, identical file (hole)"),
("P4","periodic",'SEED = 20261113','SEED = 20261114',"seed changed","byte comparison","passes, file differs"),
("P5","periodic",'if n == 400: break','if n == 40: break',"early break: P2 walks to length 40, docstring says 400","nothing if all realizations are below 40","passes, identical file (hole)"),
("P6","periodic",'P["P3"] = dim == len(vals)','P["P3"] = dim <= len(vals)',"predicate weakened == -> <=","nothing but the source digest","passes, identical file (hole)"),
("P7","return",'for t in range(1, T + 1):','for t in range(1, T):',"off-by-one: last length T not tested","byte comparison only if t = T is extremal","passes, identical file (hole)"),
("P8","return",'Rt = a * cr + (1 - a) * coh','Rt = a * cr - (1 - a) * coh',"sign flipped in the rule R_t","byte comparison (bound still holds)","passes, file differs"),
]
cfg={"edge":(E,["check_edge_records.py"],["python3","-B","check_edge_records.py","out"],"out/edge_records.json",os.path.join(E,"edge_records.json")),
"periodic":(V,["verify_periodic.py","explore_periodic.py"],["python3","-B","verify_periodic.py"],"verify_periodic_result.json",os.path.join(V,"verify_periodic_result.json")),
"return":(V,["verify_return_weight.py"],["python3","-B","verify_return_weight.py"],"Return_Weight_Results.json",os.path.join(V,"Return_Weight_Results.json"))}
out=[]
for i,k,a,b,desc,check,pred in M:
    src,files,cmd,res,stored=cfg[k]; d=os.path.join(W,f"MUTANT_{i}_{k}"); os.makedirs(d)
    for f in files: shutil.copy(os.path.join(src,f),d)
    p=os.path.join(d,files[0]); t=open(p).read(); assert t.count(a)==1,(i,t.count(a))
    od=hashlib.sha256(t.encode()).hexdigest()
    open(p,'w').write(f"# MUTANT {i}: {desc}\n"+t.replace(a,b))
    r=subprocess.run(cmd,cwd=d,capture_output=True,text=True)
    rp=os.path.join(d,res); same=os.path.exists(rp) and open(rp,'rb').read()==open(stored,'rb').read()
    o="CAUGHT (program fails)" if r.returncode else ("SURVIVED (pass, identical result file)" if same else "CAUGHT only by byte comparison (program passes)")
    rec=dict(id=i,program=files[0],original_sha256=od,change=f"{a!r} -> {b!r}",desc=desc,check=check,prediction=pred,exit=r.returncode,identical=same,outcome=o,tail=(r.stderr.strip().split("\n")[-1:] or [""])[0][:200])
    out.append(rec); print(json.dumps(rec)); sys.stdout.flush()
json.dump(out,open(os.path.join(W,'program_mutants_result.json'),'x'),indent=1)
