"""xr42 own program for Director_G/Independent_walks_and_shared_gains.md (the note that carries
the six/eight-tick claims of the pull-request summary). Written from the note text only.
Exact arithmetic: integers in Z[x]/(Phi_M); no floats in any predicate.

Walk (from the note): ring of 4M wells, start well 0, rail R, sign +, residue 0. A departure at x
adds floor(x/2) mod M. R moves +1, L moves -1; only L after L flips the sign.
Blocks at home x: C opens {x-1,x+1},{x},{x+1}; I opens {x+1},{x},{x+1} (home advances 1);
D opens {x-1,x+1},{x,x+2},{x+1},{x+2}; J opens {x+1},{x+2},{x+1},{x+2} (home advances 2).
Labels: count, folded characters s=0..floor(M/2). Scores: f_*(U)=|U|, f_s(U)=|sum eps zeta^{s j}|^2.
Law = weights on labels (nonneg, sum 1). Local numerator F_X(U)=sum_i lambda_i f_i(U).
Product independence: joint numerator F_A(U) F_B(V), denominator 4^T.

PREDICATES (fixed before first run)
 H1(M,panel)  hypothesis: the three settings (ff,ii),(ii,ff),(fi,if) have the SAME signed joint
              histogram U*V, same tick count, all words end at the same well on rail R.  Tested per M,panel.
 H2(law)      hypothesis: weights nonnegative, sum to one. Tested per law.
 P1  M=4 six ticks, A=B=half count + half s=1: numerators equal (4,4,4).
 P2  M=4 eight ticks, same law: numerators (5,5,4); 4^8 = 65536.
 P3  M=4 six ticks, A=B=half count + half s=0: numerators 10,10,9 over 4096.
 P4(M) forced purity: over ALL ordered pairs of grid laws (weights multiples of 1/n), the pair passes
       the note's prescribed test (six-tick panel if 4 does not divide M; six- and eight-tick if it does)
       IFF A=B and pure.  Count qualifying instances, passes, violations in each direction.
 P5(M) six-tick panel alone passes IFF A=B pure  (expected by the note to FAIL exactly when 4|M).
 P6(M) eight-tick panel alone passes IFF A=B pure (the note makes no such claim; measured only).
 P7(M) BB/BH/HH first row (scores computed from the multisets B*B,B*H,H*H; mask preparation NOT redone
       here) passes IFF A=B pure.
 P8(M) oriented single equality F_A(BB)F_B(HH)=F_A(BH)F_B(BH) alone passes only for A=B pure
       (the note says this FAILS: spurious pass at M=4, A=s1, B=(1/10 s0, 9/10 s2)).
"pass" = all three numerators equal as elements of Q(zeta_M) (exact).
M list: 3,4,5,6,8,12 (reported by the note) and 7,9,16,20 (not reported). Grid n=4 (n=3 for M>=16).
Failed predicates are kept in the result file. Result file opened with mode 'x'.
"""
import sys, json
from collections import Counter
from itertools import product
from pathlib import Path

def polydivmod(a,b):
    a=a[:]; q=[0]*(max(len(a)-len(b)+1,1))
    while len(a)>=len(b):
        c=a[-1]//b[-1]; assert c*b[-1]==a[-1]
        k=len(a)-len(b); q[k]=c
        for i,bi in enumerate(b): a[i+k]-=c*bi
        a.pop()
    return q,a
def cyclotomic(n,_c={}):
    if n in _c: return _c[n]
    p=[-1]+[0]*(n-1)+[1]
    for d in range(1,n):
        if n%d==0:
            p,r=polydivmod(p,cyclotomic(d)); assert not any(r)
    _c[n]=p; return p
class Field:
    def __init__(s,M):
        s.M=M; s.phi=cyclotomic(M); s.deg=len(s.phi)-1
    def red(s,v):
        v=list(v)
        while len(v)>s.deg:
            c=v.pop()
            if c:
                k=len(v)-s.deg
                for i in range(s.deg): v[i+k]-=c*s.phi[i]
        return tuple(v+[0]*(s.deg-len(v)))
    def mul(s,a,b):
        out=[0]*(2*s.deg-1)
        for i,x in enumerate(a):
            if x:
                for j,y in enumerate(b): out[i+j]+=x*y
        return s.red(out)
    def const(s,c): return s.red([c])
    def add(s,a,b): return tuple(x+y for x,y in zip(a,b))
    def scale(s,c,a): return tuple(c*x for x in a)
    def score(s,U,label):
        if label=="count": return s.const(sum(U.values()))
        M=s.M; p=[0]*M; pc=[0]*M
        for (e,j),n in U.items():
            p[(label*j)%M]+=e*n; pc[(-label*j)%M]+=e*n
        out=[0]*(2*M-1)
        for i,x in enumerate(p):
            if x:
                for j,y in enumerate(pc): out[i+j]+=x*y
        return s.red(out)

def words(M,key,start=0):
    N=4*M; rows=[]; home=start
    for b in key:
        if b=="C": rows+=[{home-1,home+1},{home},{home+1}]; home+=1
        elif b=="I": rows+=[{home+1},{home},{home+1}]; home+=1
        elif b=="D": rows+=[{home-1,home+1},{home,home+2},{home+1},{home+2}]; home+=2
        elif b=="J": rows+=[{home+1},{home+2},{home+1},{home+2}]; home+=2
    rows=[{x%N for x in r} for r in rows]
    U=Counter(); ends=set()
    for seq in product("RL",repeat=len(rows)):
        x,r,s,g=start,"R",1,0; ok=True
        for c,mask in zip(seq,rows):
            g=(g+x//2)%M
            x=(x+(1 if c=="R" else -1))%N
            if r=="L" and c=="L": s=-s
            r=c
            if x not in mask: ok=False;break
        if ok: U[s,g]+=1; ends.add((x,r))
    return U,ends,len(rows)
def conv(a,b,M):
    o=Counter()
    for (s,j),n in a.items():
        for (r,k),u in b.items(): o[s*r,(j+k)%M]+=n*u
    return o
def compositions(n,k):
    if k==1: yield (n,); return
    for i in range(n+1):
        for rest in compositions(n-i,k-1): yield (i,)+rest

def run(M,n):
    K=Field(M); labels=["count"]+list(range(M//2+1)); out=dict(M=M,grid=n,labels=len(labels))
    panels={}
    for name,f,i in (("six","C","I"),("eight","D","J")):
        loc={}; ends=set(); ticks=set()
        for key in (f+f,i+i,f+i,i+f):
            loc[key],e,t=words(M,key); ends|=e; ticks.add(t)
        pairs=((f+f,i+i),(i+i,f+f),(f+i,i+f))
        joint=[conv(loc[a],loc[b],M) for a,b in pairs]
        H1=(joint[0]==joint[1]==joint[2]) and len(ends)==1 and len(ticks)==1 and all(r=="R" for _,r in ends)
        panels[name]=dict(H1=H1,pairs=pairs,sc={k:[K.score(U,l) for l in labels] for k,U in loc.items()},
                          ticks=ticks.pop(),joint=sorted([s,j,c] for (s,j),c in joint[0].items()))
        out["H1_"+name]=H1; out["joint_"+name]=panels[name]["joint"]; out["ticks_"+name]=panels[name]["ticks"]
    B=Counter({(1,0):5}); H=Counter({(1,0):3,(-1,0):1,(1,1):1})
    big={"BB":conv(B,B,M),"BH":conv(B,H,M),"HH":conv(H,H,M)}
    j3=[conv(big[a],big[b],M) for a,b in (("BB","HH"),("HH","BB"),("BH","BH"))]
    out["H1_BH"]=(j3[0]==j3[1]==j3[2]) and sum(j3[0].values())==625
    bigsc={k:[K.score(U,l) for l in labels] for k,U in big.items()}
    laws=list(compositions(n,len(labels)))
    out["laws"]=len(laws); out["H2_all_laws"]=all(min(w)>=0 and sum(w)==n for w in laws)
    def mix(scs,w):
        acc=K.const(0)
        for c,sc in zip(w,scs):
            if c: acc=K.add(acc,K.scale(c,sc))
        return acc
    pm={name:{k:[mix(v,w) for w in laws] for k,v in p["sc"].items()} for name,p in panels.items()}
    bm={k:[mix(v,w) for w in laws] for k,v in bigsc.items()}
    def nums(name,a,b):
        return [K.mul(pm[name][x][a],pm[name][y][b]) for x,y in panels[name]["pairs"]]
    def passes(name,a,b):
        v=nums(name,a,b); return v[0]==v[1]==v[2]
    pure=[max(w)==n for w in laws]
    stats={k:dict(qualify=0,passes=0,pure_equal_pass=0,pure_equal_fail=0,other_pass=0,examples=[])
           for k in ("P4","P5","P6","P7","P8")}
    for a in range(len(laws)):
        for b in range(len(laws)):
            pe=(a==b and pure[a])
            six=passes("six",a,b); eight=passes("eight",a,b)
            r=[K.mul(bm["BB"][a],bm["HH"][b]),K.mul(bm["HH"][a],bm["BB"][b]),K.mul(bm["BH"][a],bm["BH"][b])]
            res=dict(P4=(six and eight) if M%4==0 else six,P5=six,P6=eight,P7=r[0]==r[1]==r[2],P8=r[0]==r[2])
            hyp=dict(P4=out["H1_six"] and (out["H1_eight"] or M%4),P5=out["H1_six"],P6=out["H1_eight"],
                     P7=out["H1_BH"],P8=out["H1_BH"])
            for k,v in res.items():
                st=stats[k]
                if not hyp[k]: continue
                st["qualify"]+=1
                if v: st["passes"]+=1
                if pe and v: st["pure_equal_pass"]+=1
                if pe and not v: st["pure_equal_fail"]+=1
                if v and not pe:
                    st["other_pass"]+=1
                    if len(st["examples"])<4: st["examples"].append([list(laws[a]),list(laws[b])])
    for k,st in stats.items():
        st["predicate_met"]=(st["pure_equal_fail"]==0 and st["other_pass"]==0 and st["qualify"]>0)
    out.update(stats)
    if M==4:
        idx={w:i for i,w in enumerate(laws)}
        h=lambda *on: idx[tuple(n//2 if l in on else 0 for l in labels)]
        q=h("count",1); t=h("count",0)
        toint=lambda v: v[0] if not any(v[1:]) else list(v)
        s6=[toint(x) for x in nums("six",q,q)]; s8=[toint(x) for x in nums("eight",q,q)]; t6=[toint(x) for x in nums("six",t,t)]
        d=n*n
        out["P1"]=dict(numerators=[x//d for x in s6],met=[x//d for x in s6]==[4,4,4] and all(x%d==0 for x in s6))
        out["P2"]=dict(numerators=[x//d for x in s8],denominator=4**panels["eight"]["ticks"],
                       met=[x//d for x in s8]==[5,5,4] and 4**panels["eight"]["ticks"]==65536)
        out["P3"]=dict(numerators=[x//d for x in t6],denominator=4**panels["six"]["ticks"],
                       met=[x//d for x in t6]==[10,10,9] and 4**panels["six"]["ticks"]==4096)
    return out

if __name__=="__main__":
    target=Path(sys.argv[1])
    res=[run(M,4 if M<16 else 3) for M in (3,4,5,6,7,8,9,12,16,20)]
    with target.open("x") as f:
        json.dump(res,f,indent=1)
    for r in res:
        print(r["M"],r["laws"],r["H1_six"],r["H1_eight"],r["H1_BH"],
              {k:(r[k]["qualify"],r[k]["passes"],r[k]["other_pass"],r[k]["pure_equal_fail"],r[k]["predicate_met"]) for k in ("P4","P5","P6","P7","P8")})
        for k in ("P1","P2","P3"):
            if k in r: print(k,r[k])
