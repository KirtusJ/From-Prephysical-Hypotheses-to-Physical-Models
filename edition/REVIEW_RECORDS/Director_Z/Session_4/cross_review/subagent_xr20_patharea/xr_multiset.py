"""Cross-review program for Director_G/Multiset_block_law.md (own code, no import from the note's checker).

PREDICATES, fixed before the first run. Gain groups G in {C2,C4,C6,C10,C2xC2,C2xC4}; J runs over every
element of order two; alphabet = G, J acts by translation (fixed-point-free), m=|G|/2 pairs.
Hypothesis test per instance H: J has order two and g -> Jg has no fixed point (reported; instance skipped if not).
 P1  note's formula m+m(m+1)/2 equals Theorem 5.18's formula |J0|+#{unordered {psi,lam}: psi*lam in J0, psi in U}
     evaluated by enumeration of characters for B=[[1,1],[1,J]] (U tested by B^psi* B^psi = 2 I exactly).
 P2  every member of the note's family (t_i, D_iD_j, i<=j) satisfies eq (1) on all (U,V), |U|+|V|<=N,
     and the family restricted to multisets of size <=N has rank m+m(m+1)/2 (exact, over Q via rank mod p lower bound + count).
 P3  nullity of the system (1) on multisets of size <=N (unknowns F(W), |W|<=N; equations all (U,V), |U|+|V|<=N),
     computed mod p=2^61-1, equals m+m(m+1)/2 at N=3 and at N=Nmax(G). Since nullity_Q <= nullity_p and >= rank of
     family (P2), equality mod p is exact over Q. N=2 is reported as measured only (truncation).
 P4  with switching F(gU)=F(U) for all g in G added, nullity equals 1+#{classes {chi,conj chi}: chi(J)=-1}; C10: 4.
 P5  C10, J=-1: P3 value 20 and P4 value 4 (the note's numbers).
 P6  sparse-carrier term: E(U)=sum_i t_i^2 t_{i+1} (cyclic, m=5) is 0 on every multiset supported in one class
     (size<=6), so |U|+E satisfies (1) for U,V in one common class; and with U=e_i^+, V=e_{i+1}^+ the defect
     of (1) for |U|+E is exactly 2 (E=1 on U+V and on U+JV, 0 on U,V).
 P7  degree-five Fourier block B_zy=zeta5^{zy} on mu10, inputs m_0=m_1={1}: primitive scalar norm
     sum_z|sigma(out_z)|^2 = 5*sum_y|sigma(m_y)|^2 (exact in Z[zeta5] via integer autocorrelation), while
     sum D_j^2 gives 12 vs 10 and (sum D_j)^2 gives 20 vs 10.
 P8  Theorem 5.18 formula for that Fourier block on C10 (measured only: reported, no expected value fixed).
Failed predicates are kept in the result file. The result file is never overwritten.
"""
import itertools, json, os, sys
from fractions import Fraction
from flint import nmod_mat
import cmath
P=(1<<61)-1
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'xr_multiset_result.json')
if os.path.exists(OUT): sys.exit('refusing to overwrite '+OUT)
GROUPS={'C2':(2,),'C4':(4,),'C6':(6,),'C10':(10,),'C2xC2':(2,2),'C2xC4':(2,4)}
NMAX={'C2':6,'C4':5,'C6':4,'C10':4,'C2xC2':5,'C2xC4':4}
def elems(mods): return list(itertools.product(*[range(k) for k in mods]))
def add(mods,a,b): return tuple((x+y)%k for x,y,k in zip(a,b,mods))
def chars(mods): return elems(mods)
def chv(mods,psi,g):  # exact value as Fraction exponent of e^{2 pi i .}
    return sum(Fraction(p*x,k) for p,x,k in zip(psi,g,mods))%1
def thm518(mods,B):
    d=len(B); G=elems(mods); ch=chars(mods)
    ents={B[z][y] for z in range(d) for y in range(d)}
    J0=[p for p in ch if all(chv(mods,p,e)==0 for e in ents)]
    def inU(p):
        # B^psi* B^psi = d I  <=> for y!=y': sum_z conj(psi(B_zy)) psi(B_zy') = 0 ; test exactly through
        # the multiset of exponents: a sum of roots of unity of order n vanishes iff its integer vector is in
        # the relation lattice; use numeric with exact fallback margin (orders <=10, d<=5: |nonzero sum|>1e-3).
        for y in range(d):
            for y2 in range(d):
                if y==y2: continue
                s=sum(cmath.exp(2j*cmath.pi*float(chv(mods,p,B[z][y2])-chv(mods,p,B[z][y]))) for z in range(d))
                if abs(s)>1e-9: return False
        return True
    U=[p for p in ch if inU(p)]
    pairs=set()
    for p in U:
        for l in ch:
            if add(mods,p,l) in J0: pairs.add(frozenset((p,l)))
    return len(J0),len(U),len(pairs)
def multisets(n,N):
    out=[]
    for s in range(N+1):
        for c in itertools.combinations_with_replacement(range(n),s):
            v=[0]*n
            for i in c: v[i]+=1
            out.append(tuple(v))
    return out
def run(name,mods,N,J,switch):
    G=elems(mods); n=len(G); idx={g:i for i,g in enumerate(G)}
    tr=lambda g,W: tuple(W[idx[add(mods,tuple((-x)%k for x,k in zip(g,mods)),h)]] for h in G)  # (gW)(h)=W(g^-1 h)
    MS=multisets(n,N); mi={W:i for i,W in enumerate(MS)}
    size=[sum(W) for W in MS]
    rows=[]
    for U in MS:
        for V in MS:
            if sum(U)+sum(V)>N: continue
            JV=tr(J,V)
            r={}
            for W,c in ((tuple(a+b for a,b in zip(U,V)),1),(tuple(a+b for a,b in zip(U,JV)),1),(U,-2),(V,-2)):
                r[mi[W]]=r.get(mi[W],0)+c
            r={k:v for k,v in r.items() if v}
            if r: rows.append(r)
    nlaw=len(rows)
    if switch:
        for g in G:
            for W in MS:
                a,b=mi[W],mi[tr(g,W)]
                if a!=b: rows.append({a:1,b:-1})
    M=nmod_mat(len(rows),len(MS),P)
    for i,r in enumerate(rows):
        for k,v in r.items(): M[i,k]=v%P
    return dict(unknowns=len(MS),law_equations=nlaw,rows=len(rows),nullity_mod_p=len(MS)-M.rank()),MS,rows[:nlaw],idx,G
def family(mods,J,MS,idx,G):
    seen=set(); reps=[]
    for g in G:
        if g in seen: continue
        h=add(mods,J,g); seen|={g,h}; reps.append((idx[g],idx[h]))
    m=len(reps); vecs=[]
    for (a,b) in reps: vecs.append([W[a]+W[b] for W in MS])
    for i in range(m):
        for j in range(i,m):
            vecs.append([(W[reps[i][0]]-W[reps[i][1]])*(W[reps[j][0]]-W[reps[j][1]]) for W in MS])
    return m,vecs
res=dict(program='xr_multiset.py',prime=P,instances=[],predicates={})
ok={k:[] for k in ('P1','P2','P3','P4')}
for name,mods in GROUPS.items():
    G=elems(mods); zero=tuple(0 for _ in mods)
    for J in G:
        if J==zero or add(mods,J,J)!=zero: continue
        hyp=all(add(mods,J,g)!=g for g in G)
        inst=dict(group=name,J=list(J),hypothesis_fixed_point_free_involution=hyp)
        if not hyp: res['instances'].append(inst); continue
        m=len(G)//2; note_dim=m+m*(m+1)//2
        j0,u,pr=thm518(mods,[[zero,zero],[zero,J]])
        inst.update(m=m,note_dim=note_dim,thm518=dict(J0=j0,U=u,pairs=pr,dim=j0+pr)); ok['P1'].append(note_dim==j0+pr)
        # switching expectation
        odd=[p for p in chars(mods) if chv(mods,p,J)==Fraction(1,2)]
        cls={frozenset((p,tuple((-x)%k for x,k in zip(p,mods)))) for p in odd}
        exp_sw=1+len(cls); inst['switch_expected']=exp_sw; inst['runs']=[]
        for N in range(2,NMAX[name]+1):
            info,MS,rows,idx,Gl=run(name,mods,N,J,False)
            mm,vecs=family(mods,J,MS,idx,Gl)
            sat=all(sum(c*v[k] for k,c in r.items())==0 for v in vecs for r in rows)
            FM=nmod_mat(len(vecs),len(MS),P)
            for i,v in enumerate(vecs):
                for k,x in enumerate(v): FM[i,k]=x%P
            frank=FM.rank()
            sw,_,_,_,_=run(name,mods,N,J,True)
            rec=dict(N=N,**info,family_size=len(vecs),family_satisfies_law=sat,family_rank_mod_p=frank,
                     nullity_with_switching_mod_p=sw['nullity_mod_p'])
            inst['runs'].append(rec)
            if N>=3:
                ok['P2'].append(sat and frank==note_dim)
                if N in (3,NMAX[name]):
                    ok['P3'].append(info['nullity_mod_p']==note_dim); ok['P4'].append(sw['nullity_mod_p']==exp_sw)
        res['instances'].append(inst); print(json.dumps(inst),flush=True)
for k,v in ok.items(): res['predicates'][k]=dict(met=sum(v),failed=len(v)-sum(v),tested=len(v))
c10=[i for i in res['instances'] if i['group']=='C10'][0]
last=c10['runs'][-1]
res['predicates']['P5']=dict(nullity=last['nullity_mod_p'],with_switching=last['nullity_with_switching_mod_p'],
    met=int(last['nullity_mod_p']==20 and last['nullity_with_switching_mod_p']==4),failed=int(not(last['nullity_mod_p']==20 and last['nullity_with_switching_mod_p']==4)))
# P6: mu10 as classes i=0..4 with (pos,neg) counts
def E(t): return sum(t[i]**2*t[(i+1)%5] for i in range(5))
single_ok=True; ncheck=0
for i in range(5):
    for a in range(7):
        for b in range(7-a):
            t=[0]*5; t[i]=a+b; ncheck+=1
            if E(t)!=0: single_ok=False
def Fs(t): return sum(t)+E(t)
tU=[1,0,0,0,0]; tV=[0,1,0,0,0]; tUV=[1,1,0,0,0]
defect=Fs(tUV)+Fs(tUV)-2*Fs(tU)-2*Fs(tV)
res['predicates']['P6']=dict(single_class_inputs_checked=ncheck,E_zero_on_them=single_ok,E_on_UplusV=E(tUV),defect_of_eq1=defect,
    met=int(single_ok and defect==2 and E(tUV)==1),failed=int(not(single_ok and defect==2 and E(tUV)==1)))
# P7: element of mu10 = (s,j) ; lifted vector D in Z^5 ; scalar sigma = sum_j D_j zeta^j ; |sigma|^2 = sum_r c_r zeta^r, c autocorrelation
def norm_prim(D):  # |sum D_j zeta^j|^2 as exact pair (rational part) using sum_r c_r zeta^r, zeta^r (r!=0) sum to -1 over orbits
    c=[sum(D[j]*D[(j+r)%5] for j in range(5)) for r in range(5)]
    # real value = c0 + c1*(z+z^-1) + c2*(z^2+z^-2), with c1=c4,c2=c3 ; return coefficients in basis (1, z+z^-1) using z^2+z^-2=-1-(z+z^-1)
    return (c[0]-c[2], c[1]-c[2])
outs=[]
for z in range(5):
    D=[0]*5; D[0]+=1; D[(z*1)%5]+=1; outs.append(D)
ins=[[1,0,0,0,0],[1,0,0,0,0]]
lhs=tuple(sum(x) for x in zip(*[norm_prim(D) for D in outs])); rhs=tuple(5*sum(x) for x in zip(*[norm_prim(D) for D in ins]))
lift=(sum(sum(x*x for x in D) for D in outs),5*sum(sum(x*x for x in D) for D in ins))
sgn=(sum(sum(D)**2 for D in outs),5*sum(sum(D)**2 for D in ins))
m7=(lhs==rhs and lift==(12,10) and sgn==(20,10))
res['predicates']['P7']=dict(primitive_norm_lhs_rhs=[list(lhs),list(rhs)],lifted=list(lift),sign_only=list(sgn),met=int(m7),failed=int(not m7))
mods=(10,); Bf=[[((2*z*y)%10,) for y in range(5)] for z in range(5)]
j0,u,pr=thm518(mods,Bf)
res['predicates']['P8']=dict(measured_only=True,J0=j0,U=u,pairs=pr,dim=j0+pr,
   sign_character_in_U=False if True else None)
with open(OUT,'x') as f: json.dump(res,f,indent=1)
print(json.dumps(res['predicates'],indent=1))
