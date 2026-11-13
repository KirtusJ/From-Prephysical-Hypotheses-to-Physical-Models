"""Cross-review program for Director_G/Path_area_and_the_force_clock.md (own code).

Model (from the note's text): base line, sheet Z/M (or Z when no winding), coin c in {R=+1,L=-1}; one tick from
(x,c,y): choose c' with amplitude (+-1)/sqrt2, minus only for L->L; y += k*x (departure position); x += c'.
Start (0,R,y0). Read: squared coordinates. Ruler: Hadamard coined step of stride l on the sheet, fresh coin R.
PREDICATES fixed before the first run (exact Fractions unless marked float):
 Q1 marked read, 2 force ticks + 1 ruler tick: P = 1/2 if k=+-l mod M else 0, for ALL unit pairs (k,l),
    M in {3,4,5,8,12,64} and at M=67, 100 (not in the note's stored range 3..64). Hypothesis per instance: gcd(k,M)=gcd(l,M)=1.
 Q2 first horizon t with positive return mass equals d=cyclic distance of k*l^-1 from 0, with mass 2^-d; M in {5,8,9,67 (d<=12 only)}.
 Q3 two launches, 3 force ticks, same port among (1,R),(-1,L), cyclic sheet distance two: 1/16 if 2k=+-2 else 0; M in 4..12 and 67.
 Q4 equality protocol with 2-step ruler: 1/64 if 2k=+-2l and M!=4; 1/32 at M=4; else 0; M in 3..12 and 67, all unit pairs.
 Q5 seven ticks, k=1, M=5, port (3,R): 15 words; per residue 2 positive 1 negative; port mass 5/128; A=(2,..,2) weight 20/128,
    B=(0,..) weight 0; sum D_j^2 = 20,0; (sum D_j)^2 = 100,0; primitive sum of A is 0.
 Q6 A(w)=C(p,2)-C(q,2)+pq-2I for all words of length <=12; R^aL^aR and L^aR^aR give +a^2,-a^2 at (1,R), a<=6.
 Q7 v=1, k=1, sheet Z: D_n=0 for n<=6, D_7=1/16, D_8=3/32; (1,R) signed counts at y=-9..9 step 2 as in the note;
    excluded numerator 8 of 128. Float: D_32 within 5e-7 of 0.334730, D_80 within 5e-7 of 0.388233 (tolerance = the note's 6 printed digits).
 Q8 two-launch event (same port, |y1-y2|>2n): tick 7 = 5/4096, conditional 5/526; tick 80 float within 5e-8 of 0.0257322.
 Q9 (force-reference question; measured, plus two fixed predicates) (a) P_marked(u k,u l)=P_marked(k,l) for all units u [fixed];
    (b) M=8: marked read separates k=1 from k=5 at l=1, translated read Q3 does not [fixed]; table of P over l at fixed k [measured].
 MEASURED ONLY: D_9..D_12, two-launch tick 8..12, seven-tick port census at M=7.
Failed predicates are kept. Result file is not overwritten.
"""
import itertools, json, os, sys
from fractions import Fraction as Fr
from math import gcd, comb
import numpy as np
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'xr_patharea_result.json')
if os.path.exists(OUT): sys.exit('refusing to overwrite '+OUT)
res={}; 
def pred(name,ok,**kw):
    r=res.setdefault(name,dict(met=0,failed=0,failures=[]))
    if ok: r['met']+=1
    else:
        r['failed']+=1; r['failures'].append(kw)
def force(n,k,M=None,start=(0,1,0)):
    st={start:1}
    for _ in range(n):
        new={}
        for (x,c,y),a in st.items():
            for c2 in (1,-1):
                s=-a if (c==-1 and c2==-1) else a
                y2=y+k*x
                if M: y2%=M
                key=(x+c2,c2,y2); new[key]=new.get(key,0)+s
        st={q:v for q,v in new.items() if v}
    return st   # integer numerators, amplitude = v/2^(n/2)
def ruler(y,l,t,M):  # Hadamard coined walk on sheet, fresh coin R; returns {(y,coin):int}, amp/2^(t/2)
    st={(y,1):1}
    for _ in range(t):
        new={}
        for (yy,c),a in st.items():
            for c2 in (1,-1):
                s=-a if (c==-1 and c2==-1) else a
                key=((yy+c2*l)%M,c2); new[key]=new.get(key,0)+s
        st={q:v for q,v in new.items() if v}
    return st
def marked(k,l,M,t=1):
    tot=Fr(0)
    for (x,c,y),a in force(2,k,M).items():
        for (yy,c2),b in ruler(y,l,t,M).items():
            if yy==0: tot+=Fr(a*a*b*b,4*2**t)
    return tot
units=lambda M:[u for u in range(1,M) if gcd(u,M)==1]
Q9tab={}
for M in (3,4,5,8,12,64,67,100):
    tab={}
    for k in units(M):
        for l in units(M):
            p=marked(k,l,M); tab[k,l]=p
            pred('Q1',p==(Fr(1,2) if (k-l)%M==0 or (k+l)%M==0 else 0),M=M,k=k,l=l,p=str(p))
    if M in (5,8,12,67):
        for u in units(M):
            for (k,l),p in tab.items(): pred('Q9a',tab[u*k%M,u*l%M]==p,M=M,u=u,k=k,l=l)
    if M==8: Q9tab={f'k={k}': {f'l={l}':str(tab[k,l]) for l in units(8)} for k in units(8)}
for M in (5,8,9,67):
    for k in units(M):
        for l in units(M):
            r=k*pow(l,-1,M)%M; d=min(r,M-r)
            if d>12: continue
            first=None
            for t in range(1,d+1):
                p=marked(k,l,M,t)
                if p>0: first=(t,p); break
            pred('Q2',first==(d,Fr(1,2**d)),M=M,k=k,l=l,d=d,first=str(first))
def cyc(a,M): a%=M; return min(a,M-a)
def twocopy(k,M):
    st=force(3,k,M); tot=Fr(0)
    for (x,c,y),a in st.items():
        for (x2,c2,y2),b in st.items():
            if (x,c)==(x2,c2) and (x,c) in ((1,1),(-1,-1)) and cyc(y-y2,M)==2: tot+=Fr(a*a*b*b,64)
    return tot
def equality(k,l,M):
    st=force(3,k,M); tot=Fr(0)
    for (x,c,y),a in st.items():
        for (x2,c2,y2),b in st.items():
            if (x,c)==(x2,c2) and (x,c) in ((1,1),(-1,-1)) and y!=y2:
                for (yy,cc),e in ruler(y,l,2,M).items():
                    if yy==y2: tot+=Fr(a*a*b*b*e*e,64*4)
    return tot
Q3vals={}
for M in list(range(3,13))+[67]:
    for k in units(M):
        if M>=4:
            p=twocopy(k,M); pred('Q3',p==(Fr(1,16) if (2*k-2)%M==0 or (2*k+2)%M==0 else 0),M=M,k=k,p=str(p))
            if M==8: Q3vals[f'k={k}']=str(p)
        for l in units(M):
            p=equality(k,l,M); rel=(2*k-2*l)%M==0 or (2*k+2*l)%M==0
            pred('Q4',p==((Fr(1,32) if M==4 else Fr(1,64)) if rel else 0),M=M,k=k,l=l,p=str(p))
pred('Q9b',marked(1,1,8)==Fr(1,2) and marked(5,1,8)==0 and twocopy(1,8)==twocopy(5,8)==Fr(1,16),
     marked=[str(marked(1,1,8)),str(marked(5,1,8))],translated=[str(twocopy(1,8)),str(twocopy(5,8))])
# Q5 by word enumeration
def words_at(n,k,port):
    out=[]
    for w in itertools.product((1,-1),repeat=n):
        x=0;c=1;g=0;s=1
        for c2 in w:
            if c==-1 and c2==-1: s=-s
            g+=k*x; x+=c2; c=c2
        if (x,c)==port: out.append((w,g,s))
    return out
W=words_at(7,1,(3,1)); pos=[0]*5; neg=[0]*5
for w,g,s in W:
    (pos if s>0 else neg)[g%5]+=1
port=[pos[j]-neg[j] for j in range(5)]
Arow=pos; Brow=[0]*5
st7=force(7,1,5)
pm=sum(Fr(a*a,128) for (x,c,y),a in st7.items() if (x,c)==(3,1))
pred('Q5',len(W)==15 and pos==[2]*5 and neg==[1]*5 and pm==Fr(5,128) and sum(a*a for a in Arow)==20 and sum(Arow)**2==100
     and len(set(Arow))==1, words=len(W),pos=pos,neg=neg,port_mass=str(pm))
cen7={}
for (w,g,s) in words_at(7,1,(3,1)):
    cen7.setdefault(g%7,[0,0])[0 if s>0 else 1]+=1
# Q6
for n in range(1,13):
    for w in itertools.product((1,-1),repeat=n):
        x=0;A=0
        for c2 in w: A+=x; x+=c2
        p=w.count(1); q=n-p; I=sum(1 for i in range(n) for j in range(i+1,n) if w[i]==-1 and w[j]==1)
        if A!=comb(p,2)-comb(q,2)+p*q-2*I: pred('Q6',False,w=w); break
    else: pred('Q6',True)
for a in range(1,7):
    vals=[]
    for w in ((1,)*a+(-1,)*a+(1,),(-1,)*a+(1,)*a+(1,)):
        x=0;A=0
        for c2 in w: A+=x; x+=c2
        vals.append((A,x))
    pred('Q6',vals==[(a*a,1),(-a*a,1)],a=a,vals=vals)
# Q7,Q8 exact
def D_exact(n):
    st=force(n,1); ports={}
    for (x,c,y),a in st.items(): ports.setdefault((x,c),{})[y]=a*a
    D=Fr(0); ev=Fr(0); match=Fr(0)
    for b,dist in ports.items():
        tot=sum(dist.values()); ys=sorted(dist); best=0
        for s in ys: best=max(best,sum(v for y,v in dist.items() if s<=y<=s+2*n))
        D+=Fr(tot-best,2**n); match+=Fr(tot*tot,4**n)
        ev+=Fr(sum(v*v2 for y,v in dist.items() for y2,v2 in dist.items() if abs(y-y2)>2*n),4**n)
    return D,ev,match,st
meas={}
for n in range(1,13):
    D,ev,match,st=D_exact(n)
    if n<=6: pred('Q7',D==0,n=n,D=str(D))
    elif n==7:
        row=[st.get((1,1,y),0) for y in range(-9,10,2)]
        pred('Q7',D==Fr(1,16),n=7,D=str(D)); pred('Q7',row==[1,-1,-2,1,-1,-1,1,-2,-1,1],row=row)
        pred('Q7',D*128==8,excl=str(D*128))
        pred('Q8',ev==Fr(5,4096) and ev/match==Fr(5,526),ev=str(ev),match=str(match))
    elif n==8: pred('Q7',D==Fr(3,32),n=8,D=str(D))
    meas[n]=dict(D=str(D),two_launch=str(ev),match=str(match))
# float propagation
def D_float(n):
    Y=n*(n-1)//2; W=2*Y+1; amp=np.zeros((2*n+3,2,W)); amp[n+1,0,Y]=1.0; r=2**-0.5
    for t in range(n):
        new=np.zeros_like(amp)
        for xi in range(1,2*n+2):
            x=xi-n-1; R=amp[xi,0]; L=amp[xi,1]
            if not (R.any() or L.any()): continue
            new[xi+1,0]+=np.roll(R+L,x)*r; new[xi-1,1]+=np.roll(R-L,x)*r
        amp=new
    P=amp**2; D=0.0; ev=0.0
    for xi in range(2*n+3):
        for c in range(2):
            p=P[xi,c]; tot=p.sum()
            if tot==0: continue
            cs=np.concatenate(([0],np.cumsum(p))); w=2*n+1
            win=cs[w:]-cs[:-w] if W>w else np.array([tot])
            D+=tot-win.max()
            # pairs with |y1-y2|>2n : tot^2 - sum_y p(y)*sum_{|y'-y|<=2n} p(y')
            lo=np.clip(np.arange(W)-2*n,0,W); hi=np.clip(np.arange(W)+2*n+1,0,W)
            ev+=tot*tot-float((p*(cs[hi]-cs[lo])).sum())
    return D,ev
fl={}
for n in (7,8,32,80):
    D,ev=D_float(n); fl[n]=dict(D=D,two_launch=ev)
pred('Q7',abs(fl[7]['D']-1/16)<1e-12 and abs(fl[8]['D']-3/32)<1e-12,float_vs_exact=[fl[7]['D'],fl[8]['D']])
pred('Q7',abs(fl[32]['D']-0.334730)<5e-7,D32=fl[32]['D']); pred('Q7',abs(fl[80]['D']-0.388233)<5e-7,D80=fl[80]['D'])
pred('Q8',abs(fl[80]['two_launch']-0.0257322)<5e-8,ev80=fl[80]['two_launch'])
res['measured_only']=dict(exact_by_tick=meas,float=fl,M8_marked_table=Q9tab,M8_translated=Q3vals,
    seven_tick_port_3R_at_M7_pos_neg_by_residue=cen7)
with open(OUT,'x') as f: json.dump(res,f,indent=1,default=str)
print(json.dumps({k:(dict(met=v['met'],failed=v['failed'],failures=v['failures'][:3]) if 'met' in v else v) for k,v in res.items()},default=str)[:5000])
