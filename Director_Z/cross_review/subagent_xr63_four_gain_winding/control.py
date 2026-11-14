"""Control: predicates fixed first.
C1: port (-1,L) length 3: exactly 2 walks, gains sum 0.
C2: port (1,R) length 3: exactly 2 walks, gains sum 2.
Gain: -1 for each L step immediately following an L step, +1 otherwise (product along the walk)."""
from itertools import product
import json
res={}
for w in product("RL",repeat=3):
    x=0;rail="R";g=1
    for s in w:
        if s=="L" and rail=="L": g*=-1
        x+=1 if s=="R" else -1; rail=s
    res.setdefault((x,rail),[]).append(("".join(w),g))
out={"C1":[res[(-1,"L")],len(res[(-1,"L")])==2 and sum(g for _,g in res[(-1,"L")])==0],
     "C2":[res[(1,"R")],len(res[(1,"R")])==2 and sum(g for _,g in res[(1,"R")])==2]}
json.dump(out,open("control_result.json","x"),indent=1); print(out)
