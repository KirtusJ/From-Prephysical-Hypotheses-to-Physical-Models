"""Cross-review program for Director G's note "Can a local walk produce the two-body force?".
Written from the note's definitions. Seed 20261113. Refuses to overwrite its result file.

PREDICATES (fixed before the first run; failures are kept in the result file):
P1  Newton enclosure. r''=-2 sin r, r(0)=-pi/2, r'(0)=0, q_A=(r+pi/2)/2 (zero total momentum).
    For t in {1/8,1/4,1/2,3/4,1}: t^2/2 - t^6/60 <= q_A(t) <= t^2/2.
    Integrator RK4 with h=1e-4 and h=5e-5; tolerance = measured |difference of the two|; the
    predicate passes only if the margin on each side exceeds 10x that measured difference
    (otherwise recorded UNDECIDED = failed).
P2  Bin. For c in {0,1,5,50} (5 and 50 are not in the note's numerical control) and
    t in {tmax, tmax/2}, tmax=min(1,pi/(8(1+c))): hypothesis t<=tmax tested per instance;
    (a) trial I centre q_A(t) > t^2/4; (b) trial II centre 0 inside; (c) t^2/4+c t < pi/2 (distance from
    bin centre 0 to nearer B centre). Also record II-instability: r(0)=pi-w, w=1e-3, deviation of q_A at t.
P3  Three-tick walk, own enumeration (16 coin words per walker, sign -1 when incoming and outgoing
    directions are both left; gain read at departure, offset (x-y) mod N; sheet localized at 0 and summed
    incoherently at readout together with B's endpoint). Gain table rebuilt: C_d = d-th entry after m=5120
    applications of (1,2,1) circular convolution, g(d)=round_half_up(2L(C_0-C_d)/(C_0-C_{N/2})), L=3.
    (a) g(20,22,24,26,28)=(5,4,3,2,1); (b) the entries used at the second departure for B=16 are all 6;
    (c) P[(1,R)] = 1/4 (B=8), 1/2 (B=16); (d) P[(31,L)] = 1/4, 0; (e) remaining reachable ports equal in
    the two trials and exactly four of them; (f) character k: P=(1+cos(2 pi k/17))/4 at B=8 and 1/2 at
    B=16 for all k (exact Laurent coefficients 16,8,8 and 32).
    Unreported parameters: B in {12,24}, and M in {2,3,5,13}: recorded, no predicate (exploratory).
P4  Cone, exhaustive part (point 2). Ring N=16, cells in {0,1}; inputs: single 1 at site 8 vs single 1
    at site 16-? -- precisely sites 4 and 8 (receiver cell 0; nearest changed cell at distance 4).
    ALL 256 translation-invariant radius-1 rules f:{0,1}^3->{0,1}, applied D=1,2,3 layers, plus ALL
    256^2 ordered pairs of rules for D=2 (layer 1 rule, layer 2 rule) and all 256 rules repeated D=3:
    predicted number of circuits whose receiver cell (and whose whole patch {-(3-D)..(3-D)}) differs
    between the inputs: 0. Positive control: D=4 gives >0 differing rules.
    Sampled part: 20000 site-dependent random radius-1 ternary maps, D=3, same prediction.
    Quantum sampled part: 8 qubits, brickwork Haar 2-qubit gates (even bonds then odd bonds = 2 layers of
    range 1), inputs |1> at qubit 3 vs qubit 5 (qubit 0 = receiver; ring distances 3 and 3... see code:
    inputs at 3 and 4, nearest distance 3), depth 2 layers; reduced state of qubit 0 equal.
    No threshold: report max deviation inside cone-exclusion and min deviation in the positive control
    (depth 4 layers), i.e. a measured separation.
P5  Point 3, static pre-installed field. Field f_y(x)=g((x-y0) mod N) stored on site, A adds f at its own
    site at departure (range 0). (a) number of sites in the radius-3 neighbourhood of port site 1
    (sites -2..4) where f_8 != f_16 is > 0 [field carries the choice]; (b) record port probabilities of
    the frozen-field walk and whether they equal the target 1/4, 1/2.
P6  Point 3, courier. Empty track: token for B=y is at y+t with counter t. (a) with empty track and
    emission at round 0, no token inside radius-3 neighbourhood of site 1 during rounds 0..3 for either
    y in {8,16}; first arrival round at A=0 is (0-y) mod 32 = 24, 16. (b) for a pre-propagated token
    (t0 rounds before the clock starts), count t0 in 0..31 for which the token delivers the kick within
    3 rounds; for each such t0 the token must lie inside the radius-3 neighbourhood of A's site at
    clock start (then the initial cone state differs from vacuum and encodes y through its counter).
P7  Phase sector. N=8q, q in {1,2,3,5,7}; (q=7, N=56 unreported). <X>_y by explicit 2-mode state;
    TV of binary laws = |cos(pi/sqrt2)| = 0.605699867...; relative phases -pi/sqrt2, pi(1/sqrt2-1).
    Tolerance 1e-12 = 1e4 x binary64 epsilon for O(1) trigonometric quantities.
P8  Trace distance formula (|p-q|+sqrt((p+q)^2-4|<u,v>|^2))/2 against eigenvalues of the full
    (vacuum + one-particle) difference matrix; 500 random complex u,v of dimension 2..12 with
    ||u||,||v||<=1 (hypothesis tested per instance). Report max deviation (no threshold; compare to 1e-12).
P9  Stored-file arithmetic: at N=256 bin 1, TV-cone = excess, excess/2 = 0.0329505 (7 digits);
    count of (size,bin) pairs with positive excess among primary and exploratory sizes.
"""
import json, sys, os, math, itertools, random
from fractions import Fraction
import numpy as np
SEED=20261113
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'own_local_result.json')
if os.path.exists(OUT): sys.exit('refusing to overwrite '+OUT)
rng=np.random.default_rng(SEED); random.seed(SEED)
res={'seed':SEED,'predicates':{},'failed':[]}
def rec(name,ok,**kw):
    res['predicates'][name]=dict(passed=bool(ok),**kw)
    if not ok: res['failed'].append(name)

# ---------- P1/P2
def flow(r0,t,h):
    n=max(1,int(round(t/h))); h=t/n; r,v=r0,0.0
    f=lambda r:-2*math.sin(r)
    for _ in range(n):
        k1r,k1v=v,f(r); k2r,k2v=v+h/2*k1v,f(r+h/2*k1r)
        k3r,k3v=v+h/2*k2v,f(r+h/2*k2r); k4r,k4v=v+h*k3v,f(r+h*k3r)
        r+=h/6*(k1r+2*k2r+2*k3r+k4r); v+=h/6*(k1v+2*k2v+2*k3v+k4v)
    return r
def qA(t,h=1e-4,r0=-math.pi/2): return (flow(r0,t,h)-r0)/2
rows=[];ok=True
for t in (0.125,0.25,0.5,0.75,1.0):
    a,b=qA(t),qA(t,5e-5); tol=abs(a-b)
    lo,hi=t*t/2-t**6/60,t*t/2
    m_lo,m_hi=b-lo,hi-b
    good=m_lo>10*tol and m_hi>10*tol
    ok&=good; rows.append(dict(t=t,qA=b,lower=lo,upper=hi,margin_low=m_lo,margin_up=m_hi,integrator_diff=tol,passed=good))
rec('P1_newton_enclosure',ok,rows=rows)
rows=[];ok=True
for c in (0,1,5,50):
    tmax=min(1,math.pi/(8*(1+c)))
    for t in (tmax,tmax/2):
        hyp=0<t<=tmax
        q=qA(t,t/20000)
        a_=q>t*t/4; b_=0<t*t/4; c_=t*t/4+c*t<math.pi/2
        dev=abs((flow(math.pi-1e-3,t,t/20000)-(math.pi-1e-3))/2)
        good=hyp and a_ and b_ and c_; ok&=good
        rows.append(dict(c=c,t=t,hypothesis=hyp,qA_I=q,bin_half_width=t*t/4,I_outside_margin=q-t*t/4,
                         enlarged_half_width=t*t/4+c*t,gap_to_B_pi_over_2=math.pi/2-(t*t/4+c*t),
                         II_drift_w_0p001=dev,passed=good))
rec('P2_bin',ok,qualifying=sum(r['hypothesis'] for r in rows),instances=len(rows),rows=rows)

# ---------- P3
def gain_table(n,m,L):
    row=[1]+[0]*(n-1)
    for _ in range(m): row=[row[(d-1)%n]+2*row[d]+row[(d+1)%n] for d in range(n)]
    norm=row[0]-row[n//2]
    return [(4*L*(row[0]-c)+norm)//(2*norm) for c in row]   # floor(x+1/2): ties upward
def three_tick(n,M,g,yB,ticks=3,field=None):
    """returns dict port-> list of Laurent coefficients (index = sheet difference mod M) numerators over 4^ticks.
    amplitude table amp[(xA,cA,yB,cB)][sheet]; port norm for localized sheet = sum of squares;
    autocorrelation coefficient k = sum_s amp[s]amp[s-k]."""
    amp={}
    for wa in itertools.product((1,-1),repeat=ticks):
        for wb in itertools.product((1,-1),repeat=ticks):
            x,y,ca,cb,s,sg=0,yB,1,1,0,1
            for da,db in zip(wa,wb):
                s=(s+(g[(x-y)%n] if field is None else field[x%n]))%M
                if ca==-1 and da==-1: sg=-sg
                if cb==-1 and db==-1: sg=-sg
                x,y,ca,cb=(x+da)%n,(y+db)%n,da,db
            amp.setdefault((x,ca,y,cb),{}); amp[(x,ca,y,cb)][s]=amp[(x,ca,y,cb)].get(s,0)+sg
    ports={}
    for (x,ca,y,cb),d in amp.items():
        co=ports.setdefault((x,ca),[0]*M)
        for s1,v1 in d.items():
            for s2,v2 in d.items(): co[(s1-s2)%M]+=v1*v2
    return ports
n,M,L,m=32,17,3,5120
g=gain_table(n,m,L)
res['gain_table']=g
pa=(g[20],g[22],g[24],g[26],g[28])==(5,4,3,2,1)
# second departure for B=16: A at +-1, B at 15 or 17 -> offsets (x-y) mod 32
offs=sorted({(x-y)%n for x in (1,-1) for y in (15,17)})
pb=all(g[o]==6 for o in offs)
P8_=three_tick(n,M,g,8); P16=three_tick(n,M,g,16)
F=lambda v:str(Fraction(v,64))
pc=(P8_[(1,1)][0],P16[(1,1)][0])==(16,32)
pd=(P8_.get((31,-1),[0])[0],P16.get((31,-1),[0])[0])==(16,0)
others=sorted(set(P8_)|set(P16)); others=[p for p in others if p not in((1,1),(31,-1))]
eq=[p for p in others if P8_.get(p,[0])[0]==P16.get(p,[0])[0] and P8_.get(p,[0])[0]>0]
pe=len(eq)==len([p for p in others if P8_.get(p,[0])[0]>0 or P16.get(p,[0])[0]>0])==4
exp8=[0]*M; exp8[0]=16; exp8[1]=exp8[-1]=8; exp16=[0]*M; exp16[0]=32
pf=P8_[(1,1)]==exp8 and P16[(1,1)]==exp16
chars=[(k,sum(c*math.cos(2*math.pi*k*j/M) for j,c in enumerate(P8_[(1,1)]))/64,(1+math.cos(2*math.pi*k/M))/4) for k in range(M)]
rec('P3a_linear_entries',pa,values=[g[20],g[22],g[24],g[26],g[28]])
rec('P3b_flat_entries_B16',pb,offsets=offs,values=[g[o] for o in offs])
rec('P3c_port_1R',pc,B8=F(P8_[(1,1)][0]),B16=F(P16[(1,1)][0]))
rec('P3d_port_31L',pd,B8=F(P8_.get((31,-1),[0])[0]),B16=F(P16.get((31,-1),[0])[0]))
rec('P3e_other_ports',pe,ports={str(p):[F(P8_.get(p,[0])[0]),F(P16.get(p,[0])[0])] for p in others})
rec('P3f_laurent',pf,B8=P8_[(1,1)],B16=P16[(1,1)],max_char_dev=max(abs(a-b) for _,a,b in chars),trivial_char=chars[0][1])
expl={}
for yb in (4,8,12,16,20,24,28):
    for MM in (2,3,5,13,17):
        p=three_tick(n,MM,[x%MM for x in g],yb)
        expl['B=%d,M=%d'%(yb,MM)]=dict(p1R=F(p[(1,1)][0]),p31L=F(p.get((31,-1),[0])[0]),hyp_distance_ge_4=min(abs(yb-1),n-abs(yb-1))>3)
res['P3_exploratory_unreported']=expl

# ---------- P4
N=16
def run_eca(rules,init):
    s=list(init)
    for r in rules: s=[(r>>(4*s[(i-1)%N]+2*s[i]+s[(i+1)%N]))&1 for i in range(N)]
    return s
def onehot(j): return [1 if i==j else 0 for i in range(N)]
A_,B_=onehot(4),onehot(8)
cnt={}
def differs(sa,sb,D): return any(sa[i%N]!=sb[i%N] for i in range(-(3-D),(3-D)+1)) if D<=3 else sa[0]!=sb[0]
for D in (1,2,3,4):
    cnt['same_rule_D%d'%D]=sum(differs(run_eca([r]*D,A_),run_eca([r]*D,B_),D) for r in range(256))
# all ordered pairs D=2 (vectorised cheaply: precompute layer-1 outputs)
l1=[(run_eca([r],A_),run_eca([r],B_)) for r in range(256)]
c2=0
for r1 in range(256):
    sa,sb=l1[r1]
    for r2 in range(256):
        if differs(run_eca([r2],sa),run_eca([r2],sb),2): c2+=1
cnt['all_ordered_pairs_D2_of_65536']=c2
# sampled site-dependent ternary
c3=0;c4=0
for trial in range(20000):
    tabs=rng.integers(0,3,size=(4,N,27))
    def run(init,D):
        s=np.array(init)
        for d in range(D): s=tabs[d,np.arange(N),9*np.roll(s,1)+3*s+np.roll(s,-1)]
        return s
    c3+=int(run(A_,3)[0]!=run(B_,3)[0]); c4+=int(run(A_,4)[0]!=run(B_,4)[0])
cnt['sampled_ternary_site_dependent_D3_of_20000']=c3; cnt['sampled_ternary_D4_positive_control_of_20000']=c4
# quantum
def haar(d):
    z=(rng.normal(size=(d,d))+1j*rng.normal(size=(d,d)))/math.sqrt(2); q,r=np.linalg.qr(z); return q*(np.diag(r)/abs(np.diag(r)))
nq=8
def apply2(psi,U,i,j):
    psi=np.moveaxis(psi,(i,j),(0,1)); sh=psi.shape; psi=(U@psi.reshape(4,-1)).reshape(sh); return np.moveaxis(psi,(0,1),(i,j))
def basis(j):
    psi=np.zeros((2,)*nq,complex); idx=[0]*nq; idx[j]=1; psi[tuple(idx)]=1; return psi
def rho0(psi):
    v=psi.reshape(2,-1); return v@v.conj().T
mx_in=0;mn_out=1e9
for trial in range(300):
    layers=[[haar(4) for _ in range(nq//2)] for _ in range(4)]
    def ev(psi,D):
        for d in range(D):
            for b in range(nq//2):
                i=(2*b+d%2)%nq; psi=apply2(psi,layers[d][b],i,(i+1)%nq)
        return psi
    # inputs at qubits 3 and 4: ring distances from qubit 0 are 3 and 4
    mx_in=max(mx_in,np.abs(rho0(ev(basis(3),2))-rho0(ev(basis(4),2))).max())
    mn_out=min(mn_out,np.abs(rho0(ev(basis(3),4))-rho0(ev(basis(4),4))).max())
cnt['quantum_max_dev_depth2_300_circuits']=float(mx_in); cnt['quantum_min_dev_depth4_positive_control']=float(mn_out)
ok=cnt['same_rule_D1']==cnt['same_rule_D2']==cnt['same_rule_D3']==0 and c2==0 and c3==0 and cnt['same_rule_D4']>0 and c4>0
rec('P4_cone_enumeration',ok,**cnt)

# ---------- P5
cone=[(1+k)%n for k in range(-3,4)]
f8=[g[(x-8)%n] for x in range(n)]; f16=[g[(x-16)%n] for x in range(n)]
ndiff=sum(f8[x]!=f16[x] for x in cone)
q8=three_tick(n,M,g,8,field=f8); q16=three_tick(n,M,g,16,field=f16)
rec('P5a_static_field_carries_choice',ndiff>0,cone_sites=cone,f_B8=[f8[x] for x in cone],f_B16=[f16[x] for x in cone],differing_sites=ndiff)
res['P5b_frozen_field_walk']=dict(p1R_B8=F(q8[(1,1)][0]),p1R_B16=F(q16[(1,1)][0]),p31L_B8=F(q8.get((31,-1),[0])[0]),p31L_B16=F(q16.get((31,-1),[0])[0]),
     equals_target=(q8[(1,1)][0],q16[(1,1)][0])==(16,32),
     note='range-0 lookup of a field frozen at the initial B position; TV between the two trials recorded, B motion ignored by the field')
# ---------- P6
def inside(site,centre,rad): d=(site-centre)%n; return min(d,n-d)<=rad
rows=[];ok=True
for y in (8,16):
    emp=[inside((y+t)%n,1,3) for t in range(4)]
    arrive=(0-y)%n
    good=not any(emp) and arrive>3; ok&=good
    rows.append(dict(B=y,token_in_port_cone_rounds_0_3=emp,first_contact_round_at_A=arrive))
pre=[];okb=True
for y in (8,16):
    for t0 in range(n):
        remaining=((0-y)%n-t0)%n   # rounds until contact at A=0 after clock start
        delivers=remaining<=3-1    # contact must occur in rounds 0,1,2 of a three-round budget
        site=(y+t0)%n
        near=inside(site,0,3)
        if delivers:
            pre.append(dict(B=y,t0=t0,token_site=site,counter=t0,within_radius3_of_A=near)); okb&=near
rec('P6a_empty_track_no_early_signal',ok,rows=rows)
rec('P6b_prepropagated_token_is_in_cone',okb,delivering_cases=pre,
    distinct_cone_states={str((p['token_site'],p['counter'])):p['B'] for p in pre})
# ---------- P7
rows=[];ok=True;target=abs(math.cos(math.pi/math.sqrt(2)))
for q in (1,2,3,5,7):
    Nn=8*q; phi=lambda x,y:math.pi*(1-math.cos(2*math.pi*(x-y)/Nn))
    ex=[];ph=[]
    for y in (2*q,4*q):
        psi=np.array([np.exp(-1j*phi(0,y)),np.exp(-1j*phi(q,y))])/math.sqrt(2)
        X=np.array([[0,1],[1,0]]); ex.append(float((psi.conj()@X@psi).real)); ph.append(phi(q,y)-phi(0,y))
    tv=abs(ex[0]-ex[1])/2
    good=abs(tv-target)<1e-12 and abs(ph[0]+math.pi/math.sqrt(2))<1e-12 and abs(ph[1]-math.pi*(1/math.sqrt(2)-1))<1e-12
    ok&=good; rows.append(dict(N=Nn,X=ex,phases=ph,tv=tv,dev=abs(tv-target),passed=good))
rec('P7_phase_sector',ok,target=target,rows=rows)
# ---------- P8
mx=0;qual=0
for _ in range(500):
    d=int(rng.integers(2,13)); u=rng.normal(size=d)+1j*rng.normal(size=d); v=rng.normal(size=d)+1j*rng.normal(size=d)
    u*=math.sqrt(rng.uniform(0,1))/np.linalg.norm(u); v*=math.sqrt(rng.uniform(0,1))/np.linalg.norm(v)
    p,qq=np.vdot(u,u).real,np.vdot(v,v).real
    if not(p<=1 and qq<=1): continue
    qual+=1
    Dm=np.zeros((d+1,d+1),complex); Dm[0,0]=(1-p)-(1-qq); Dm[1:,1:]=np.outer(u,u.conj())-np.outer(v,v.conj())
    td=np.abs(np.linalg.eigvalsh(Dm)).sum()/2
    f=(abs(p-qq)+math.sqrt(max(0,(p+qq)**2-4*abs(np.vdot(u,v))**2)))/2
    mx=max(mx,abs(td-f))
rec('P8_trace_distance_formula',mx<1e-12,qualifying=qual,instances=500,max_dev=float(mx),tolerance_basis='1e-12 ~ 5e3 eps for <=13x13 Hermitian eigenproblem with O(1) entries')
# ---------- P9
st=json.load(open(sys.argv[1]))
pos=[];allp=[]
for r in st['sizes']:
    for c in r['comparisons']:
        if c['kappa']==1:
            allp.append((r['N'],c['bin_index'],c['binary_total_variation'],c['excess_over_speed_one_cone_trace_bound']))
            if c['excess_over_speed_one_cone_trace_bound']>0: pos.append((r['N'],c['bin_index']))
r=st['sizes'][-1]; c=[c for c in r['comparisons'] if c['kappa']==1 and c['bin_index']==1][0]
td=r['bins'][1]['initial_cone']['trace_distance']
okk=round(c['binary_total_variation'],7)==0.1604391 and round(td,7)==0.0945381 and round((c['binary_total_variation']-td)/2,7)==0.0329505
rec('P9_stored_arithmetic',okk,tv=c['binary_total_variation'],cone_td=td,half_excess=(c['binary_total_variation']-td)/2,
    positive_excess_pairs=pos,all_pairs=allp,primary_pairs_with_positive_excess=sum(1 for p in pos if p[0] in st['primary_sizes']),
    cone_B_mass_pi_over_2=r['bins'][1]['initial_cone']['B_mass_pi_over_2'])
json.dump(res,open(OUT,'x'),indent=1)
print('failed:',res['failed'])
for k,v in res['predicates'].items(): print(k,v['passed'])
