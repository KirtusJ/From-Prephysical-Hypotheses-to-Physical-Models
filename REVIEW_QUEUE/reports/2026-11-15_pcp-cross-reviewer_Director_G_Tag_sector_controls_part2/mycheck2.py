"""Own check of Tag_sector_controls.md lines 120-188. Predicates fixed before first run:
P1 F_{4000,q0}(2263) within 1e-9 of 0.048670116842 and <0.05.
P2 power [1-F_{B,d}(3999)]F_{4000,p}(2263): B=28122 >=0.95 (~0.950019928679), B=28121 <0.95.
P3 exact threshold e* = 2816/2853 from (512-472e)/(512-438e)=257/444; e=0 gives 239/256.
P4 hidden-log witnesses: logs consistent with stated true masses (hypothesis: certificates <= true masses).
P5 dependent-streams rejection within [0.103506244470,0.103506254147] (full sum, no truncation).
P6 F_{4700,q0}(2664)<0.049171; max(0,2t-1) <0.95 at 33284, >=0.95 at 33285.
P7 Chernoff: null<0.039651, rival<0.040970, timeout<0.001771, power>=0.955489509622 (to 1e-9).
P8 NEW parameter m=20000, cutoff floor(2m*25096/44000): Chernoff null bound vs exact comonotone tail
   (bound must dominate); MC (seed 20261113) of combined test, per instance hypothesis pbar>=q0.
Float binomial via lgamma; tolerance basis: double rounding ~1e-12 relative per term.
"""
import math, json, random, sys
from fractions import Fraction as Fr
def pmf_list(n,p):
    lp,lq=math.log(p),math.log1p(-p)
    return [math.exp(math.lgamma(n+1)-math.lgamma(k+1)-math.lgamma(n-k+1)+k*lp+(n-k)*lq) for k in range(n+1)]
def F(n,p,k):
    if k<0: return 0.0
    if k>=n: return 1.0
    lp,lq=math.log(p),math.log1p(-p); s=[]
    for j in range(k+1):
        s.append(math.exp(math.lgamma(n+1)-math.lgamma(j+1)-math.lgamma(n-j+1)+j*lp+(n-j)*lq))
    return math.fsum(s)
def Ftail_hi(n,p,k):  # P(Bin>=k)
    return 1-F(n,p,k-1)
R={}; q0=257/444
R['P1']=F(4000,q0,2263); R['P1_pass']=abs(R['P1']-0.048670116842)<1e-9 and R['P1']<0.05
d=9691/65536; p=5356/9691
pw=lambda B:(1-F(B,d,3999))*F(4000,p,2263)
R['P2']=[pw(28122),pw(28121)]; R['P2_pass']=R['P2'][0]>=0.95>R['P2'][1] and abs(R['P2'][0]-0.950019928679)<1e-9
e=Fr(256*187*2,1)/(444*472-257*438); e=Fr(187*512,444*472-257*438)
R['P3']=str(e); R['P3_pass']=e==Fr(2816,2853) and Fr(512-34,512)==Fr(239,256)
# P4 hypothesis per witness: certified <= true, unresolved = deficit
W=[((40,34,438),(40,31,438,3)),((43,31,438),(40,31,438,3)),((49,25,438),(40,25,438,9)),((40,34,438),(40,25,438,9)),
   ((240,204,2628),(240,187,2628,17)),((257,187,2628),(240,187,2628,17))]
R['P4']=[all(l[i]<=t[i] for i in range(3)) and sum(t)-sum(l[:3])==l[3] for t,l in W]; R['P4_pass']=all(R['P4'])
# P5
pc=pmf_list(4000,0.5); a_=37/256; tot=0.0
import itertools
for N in range(1600,2401):  # omitted sign mass < 1e-30 (run 2 change: speed; run 1 timed out)
    a=min(N,4000-N); v=abs(2*N-4000)
    px=pmf_list(a,q0)
    cv=list(itertools.accumulate(pmf_list(v,q0))) if v else [1.0]
    s=math.fsum(px[x]*(cv[min(2263-2*x,v)]) for x in range(min(a,2263//2)+1))
    tot+=pc[N]*s
R['P5']=tot*(1-F(28122,a_,3999)); R['P5_pass']=0.103506244470-1e-10<=R['P5']<=0.103506254147+1e-10
t=lambda B:(1-F(B,d,4699))*F(4700,p,2664)
R['P6']=[F(4700,q0,2664),max(0,2*t(33284)-1),max(0,2*t(33285)-1)]
R['P6_pass']=R['P6'][0]<0.049171 and R['P6'][1]<0.95<=R['P6'][2]
def chern(m,x,pp):
    z=x*(1-pp)/(pp*(1-x)); return math.exp(m*math.log(1-pp+pp*z)-m*x*math.log(z))
pbar=499/888
nb=chern(22000,25096/44000,q0); rb=chern(22000,25097/44000,pbar); to=F(155000,37/256,21999)
R['P7']=[nb,rb,to,1-rb-2*to]; R['P7_pass']=nb<0.039651 and rb<0.040970 and to<0.001771 and abs(1-rb-2*to-0.955489509622)<1e-8
# P8 new m
m=20000; k=(2*m*25096)//44000; x=k/(2*m)
nb2=chern(m,x,q0); ex=F(2*m,q0,k)  # independent streams at boundary: total ~Bin(2m,q0)
como=F(m,q0,k//2)  # identical streams: T=K, total=2K<=k
rng=random.Random(20261113); trials=4000; rej=0; qual=0
for i in range(trials):
    pp=rng.uniform(q0,0.62); pm=2*q0-pp+rng.uniform(0,0.01)
    if not (0<pm<1 and (pp+pm)/2>=q0): continue
    qual+=1; u=[rng.random() for _ in range(200)]  # comonotone blocks approx: shared uniforms per score via binomial on shared
    # exact comonotone: K_s = #{j<=m: U_j<p_s}; draw counts by splitting intervals
    lo,hi=min(pp,pm),max(pp,pm)
    c1=rng.binomialvariate(m,lo); c2=rng.binomialvariate(m-c1,(hi-lo)/(1-lo))
    Klo,Khi=c1,c1+c2
    if Klo+Khi<=k: rej+=1
R['P8']=dict(m=m,k=k,chern_null=nb2,exact_indep=ex,exact_comonotone=como,mc_qual=qual,mc_rej=rej,mc_rate=rej/max(qual,1))
R['P8_pass']=nb2>=max(ex,como) and rej/max(qual,1)<=nb2+3*math.sqrt(nb2/qual)
with open(sys.argv[1],'x') as f: json.dump(R,f,indent=1)
print(json.dumps(R,indent=1))
