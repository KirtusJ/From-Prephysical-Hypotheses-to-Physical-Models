"""Follow-up F1 (added after the first run; first-run file untouched). Exploratory, no pass/fail predicate:
does the three-tick 1/4 vs 1/2 split at port (1,R) persist for amplitudes L other than the note's L=3
(same N=32, m=5120, M=17, B=8 vs 16)? Records probabilities for L in {1,2,3,4,6,12,30}. Refuses to overwrite."""
import json,os,sys,importlib.util
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'own_followup_L_result.json')
if os.path.exists(OUT): sys.exit('refusing to overwrite')
src=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'own_local_check.py')).read()
ns={}
exec(src[src.index('def gain_table'):src.index('n,M,L,m=32,17,3,5120')].replace('itertools','__import__("itertools")'),ns)
from fractions import Fraction
rows=[]
for L in (1,2,3,4,6,12,30):
    g=ns['gain_table'](32,5120,L)
    r={}
    for y in (8,16):
        p=ns['three_tick'](32,17,g,y); r[y]=(str(Fraction(p[(1,1)][0],64)),str(Fraction(p.get((31,-1),[0])[0],64)))
    rows.append(dict(L=L,g14_16_18=[g[14],g[16],g[18]],g20_28=[g[k] for k in (20,22,24,26,28)],B8=r[8],B16=r[16]))
    print(rows[-1])
json.dump(rows,open(OUT,'x'),indent=1)
