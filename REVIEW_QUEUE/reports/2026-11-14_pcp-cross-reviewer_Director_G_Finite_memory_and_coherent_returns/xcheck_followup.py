"""Follow-up to xcheck_memory.py (run1 kept unchanged; B2 and D2 stay recorded as failed there).
B2b: B2 failed in run1 because MY swap type was mis-encoded (two_state(0,0,1,0,1) starts in the clicking
     state, triple (1,0,1), not the note's 'starts dark and swaps', triple (0,1,0)). Same predicate, same
     points generator and seed, swap type = start in state 1 (dark), state 0 clicks, x=0, y=1.
D2b: D2 failed in run1 because I fixed the reading 'rows of the panel with a loss' (28,18,6,0). Second
     reading fixed here: number of lost (entry, port) pairs = 66,25,6,0. Both readings reported.
Refuses to overwrite its result file.
"""
import sys, json, random
from fractions import Fraction as F
from pathlib import Path
rnd = random.Random(20261113)
def run(P,a,b,n=3):
    v,p=list(b),[]
    for _ in range(n):
        p.append(sum(x*y for x,y in zip(a,v))); v=[sum(P[i][j]*v[j] for j in range(2)) for i in range(2)]
    return p
def ts(a,x,y,b0,b1): return run([[x,1-x],[y,1-y]],[a,1-a],[b0,b1])
def L(t,s): return F(0) if t==0 else max(F(0),t+s-1)**2/t
def rfrac():
    u=rnd.random()
    if u<0.15: return F(0)
    if u<0.3: return F(1)
    d=rnd.randint(2,40); return F(rnd.randint(0,d),d)
SWAP=ts(F(0),F(0),F(1),F(1),F(0)); assert SWAP==[0,1,0]
def lower(t,s):
    if s<=1-t: parts=[(t,ts(F(1),F(0),F(0),F(1),F(0))),(s,SWAP),(1-t-s,ts(F(1),F(1),F(0),F(0),F(0)))]
    else:
        x=(s+t-1)/t; assert 0<=x<=1
        parts=[(t,ts(F(1),x,F(0),F(1),F(0))),(1-t,SWAP)]
    assert sum(w for w,_ in parts)==1 and all(w>=0 for w,_ in parts)
    return [sum(w*tr[k] for w,tr in parts) for k in range(3)]
pts=[(F(i,7),F(j,7)) for i in range(8) for j in range(8)]+[(rfrac(),rfrac()) for _ in range(3000)]
bad=[]
for t,s in pts:
    if lower(t,s)!=[t,s,L(t,s)]: bad.append(("lower",str(t),str(s)))
    if [1-v for v in lower(1-t,1-s)]!=[t,s,1-L(1-t,1-s)]: bad.append(("upper",str(t),str(s)))
    if not L(t,s)<=1-L(1-t,1-s): bad.append(("order",str(t),str(s)))
run1=json.loads((Path(sys.argv[1])/"xcheck_memory.json").read_text())["predicates"]["D2"]["recount"]
ports=[run1[m]["lost_ports"] for m in ("3","9","27","81")]; rows=[run1[m]["rows_with_loss"] for m in ("3","9","27","81")]
out=dict(B2b=dict(passed=not bad,points=len(pts),bad=bad[:20],n_bad=len(bad),
                  boundary_points_t0_or_t1=sum(1 for t,s in pts if t in (0,1))),
         D2b=dict(passed=ports==[66,25,6,0],lost_entry_port_pairs=ports,panel_entries_with_a_loss=rows))
dest=Path(sys.argv[1])/"xcheck_followup.json"
if dest.exists(): sys.exit("refusing to overwrite")
dest.write_text(json.dumps(out,indent=1)+"\n"); print(json.dumps(out))
