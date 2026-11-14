"""Follow-up to failed B1 (kept). Fixed question: which direction fails? List assignments that are
rail-normalised at t=1,2,3 from (0,R) but not unitary, and those unitary but not normalised; for the
first kind, test normalisation at t=4,5 and whether rates equal (1/4,7/8)."""
import sys,json
sys.argv=['x','/dev/null']
src=open('xr67_check.py').read().split('res={')[0]
exec(src)
out=dict(norm_not_unit=0,unit_not_norm=0,examples=[],norm_to_5=0,target_rates=[])
for n in range(1,13):
    for a,b,c,d in product(range(n),repeat=4):
        for sd in (1,-1):
            g={'RR':(a,1),'RL':(b,1),'LR':(c,1),'LL':(d,sd)}
            unit=iszero(add(mono(a-c,n),mono(b-d,n,sd)),n)
            def nt(t):
                o,_=walk(g,n,t); return iszero(add(add(norm2(o['R'],n),norm2(o['L'],n)),const(-2**t,n)),n), norm2(o['R'],n)
            normed=all(nt(t)[0] for t in (1,2,3))
            if unit and not normed: out['unit_not_norm']+=1
            if normed and not unit:
                out['norm_not_unit']+=1
                n5=nt(4)[0] and nt(5)[0]
                out['norm_to_5']+=n5
                hit=iszero(add(nt(2)[1],const(-1,n)),n) and iszero(add(nt(3)[1],const(-7,n)),n)
                if len(out['examples'])<6: out['examples'].append((n,a,b,c,d,sd,bool(n5)))
                if hit: out['target_rates'].append((n,a,b,c,d,sd,bool(n5)))
json.dump(out,open('b1_followup.json','x'),indent=1); print(out['norm_not_unit'],out['unit_not_norm'],out['norm_to_5'],out['examples'],len(out['target_rates']),out['target_rates'][:10])
