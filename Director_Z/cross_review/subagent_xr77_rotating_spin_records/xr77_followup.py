"""Follow-up to xr77.py (result_1.json kept). Predicates fixed before run:
F1 count lattice with real-valued N in [2000,5000] step 0.01: report N* minimizing max|f*N-round(f*N)| per series,
   using filed normalized frequencies; PASS if max deviation at N* < 0.1 count (basis: 0.0005pt rounding*N/237.68 ~ 0.007
   plus scale error; 0.1 is a loose bound, the deviation itself is reported) AND a random 16-vector (seed 20261114,
   200 Dirichlet draws rounded to 0.001pt) reaches that deviation in <5% of draws (control for look-elsewhere).
F2 corrected worst-case reading bound for double flip ratio r=A/B (A: 2 heights, B: 8): (2*d*(1-r)+6*d*r)/B, d=0.0005pt; PASS if <5e-6.
F3 with reconstructed integer counts, heralded double flips agree with filed values to <2e-4 (half a count / ~1500).
"""
import json,sys,random,math
from pathlib import Path
out=Path(sys.argv[2]); 
if out.exists(): sys.exit("refuse to overwrite")
J=json.load(open(sys.argv[1])); rng=random.Random(20261114); R={}
def best(f):
    b=(9,None)
    for i in range(200000,500001):
        n=i/100; d=max(abs(x*n-round(x*n)) for x in f)
        if d<b[0]: b=(d,n)
    return b
for k in ("initially_and_finally_detected","initially_detected"):
    W=J[k]["words"]; f=[W[w]["frequency"] for w in sorted(W)]
    d,n=best(f); cnt={w:round(W[w]["frequency"]*n) for w in sorted(W)}
    hits=0
    for _ in range(200):
        g=[rng.gammavariate(3000/16,1) for _ in range(16)]; s=sum(g); g=[round(x/s*237.68,3) for x in g]; s=sum(g)
        hits+= best_d<=d if (best_d:=min(max(abs(x/s*(m/10)-round(x/s*(m/10))) for x in g) for m in range(20000,50001,1))) is not None else 0
    def dbl(r):
        den=sum(c for w,c in cnt.items() if w[0]==r); num=sum(c for w,c in cnt.items() if w[0]==r and w[1]!=r and w[2]==r); return num,den
    R[k]=dict(N_star=n,max_dev_counts=d,control_fraction_reaching=hits/200,counts=cnt,total=sum(cnt.values()),
              double_flip_counts={r:dbl(r) for r in "01"},
              double_flip_from_counts={r:dbl(r)[0]/dbl(r)[1] for r in "01"}, filed=J[k]["double_flip_given_initial_bit"])
    R[k]["F1"]= d<0.1 and hits/200<0.05
    R[k]["F3"]= all(abs(R[k]["double_flip_from_counts"][r]-R[k]["filed"][r])<2e-4 for r in "01")
    r_=J[k]["double_flip_given_initial_bit"]["0"]; B=sum(float(eval(W[w]["pdf_height"])) for w in W if w[0]=="0")
    R[k]["F2_bound"]=(2*0.0005*(1-r_)+6*0.0005*r_)/B; R[k]["F2"]=R[k]["F2_bound"]<5e-6
json.dump(R,out.open("x"),indent=1)
for k,v in R.items(): print(k,{a:b for a,b in v.items() if a!="counts"})
