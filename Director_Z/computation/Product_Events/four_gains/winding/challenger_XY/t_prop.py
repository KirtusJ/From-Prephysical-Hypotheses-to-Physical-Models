"""Proposition T replayed from the text of PROOFS.md only. Usage: python3 t_prop.py RESULT.json SEED
State: counts indexed by (lambda unwrapped, last step, gain exponent mod q); site = t-2*lambda mod N; start (0,R), exponent 0.
A mask given as relative residues E means the SITE set {t-2(s+e) mod N: e in E}, s = unwrapped deficit of the source
(frozen after KILL); a continued walk survives iff its new site is in that set. L after L multiplies by delta.
PREDICATES (fixed before first run); hypothesis M>=8 tested per case, qualifying cases counted; M<8 cases are run as
'subbound' observations (the text says the construction fails for M in {3,5,6,7}).
 T1: terminal field (all walks, all sites) == request exactly: mode (i) R:G2@l, L:G3@l, G1@l+M; mode (ii) R:G3@l, G1@l+M, L:G2@l+M;
     l = s+4 (i), s+2 (ii), s = 2*#ADV; site T-2l mod N == x.
 T2: every mask has <= 5 sites.
Requests: q=1..3, all (G1,G2,G3) with at most one item each, plus 40 random requests per (N,q) with 0..3 items each.
Sites: all x for N=16; x in {0,1,N-1} for other N.
Resolutions of ambiguity are listed in NOTES.md.
"""
import sys, json, random, itertools
from collections import Counter
def run(N,q,mode,G1,G2,G3,x):
    M=N//2 if N%2==0 else N
    st=Counter({(0,0,0):1}); env={'t':0,'s':0,'r':0,'adv':0,'maxmask':0,'src':True}
    pos={}
    def tick(E):
        env['t']+=1; t=env['t']
        sm={(t-2*(env['s']+e))%N for e in E}; env['maxmask']=max(env['maxmask'],len(sm))
        new=Counter()
        for (lam,last,e),c in st.items():
            if (t-2*lam)%N in sm: new[(lam,0,e)]+=c
            if (t-2*(lam+1))%N in sm: new[(lam+1,1,(e+(last==1))%q)]+=c
        st.clear(); st.update(new)
    stocks=lambda: set(pos.values())
    occ=lambda: stocks()|({0} if env['src'] else set())
    def ADV():
        ks=stocks()
        tick({1}|{k+1 for k in ks}); tick({2}|{k+1 for k in ks}); tick({2}|{k+2 for k in ks}); tick({2}|{k+2 for k in ks})
        env['s']+=2; env['r']+=1; env['adv']+=1
    def DEP(name):
        ks=stocks(); tick({0,1,2}|ks); tick({0,2}|ks); tick({0,2}|ks); pos[name]=2
    def RUN(name,target):
        while pos[name]<target:
            k=pos[name]; oth=occ()-{k}
            tick(oth|{k+1}); tick(oth|{k+1}); pos[name]=k+1
    def slot(name,c,items):
        r0=env['r']
        for j in sorted(items,key=lambda j:(j-c-r0)%q):
            while (env['r']+c-j)%q: ADV()
            DEP(name)
    cA,cB,cC=(3,1,2) if mode==1 else (2,2,1)
    slot('A',cA,G1)
    if 'A' in pos: RUN('A',6)
    slot('B',cB,G2)
    if 'B' in pos: RUN('B',4)
    slot('C',cC,G3)
    tick(stocks()); env['src']=False   # KILL
    if 'A' in pos:
        RUN('A',M); k=M
        oth=occ()-{k}; tick(oth|{k+1}); tick(oth|{k+2}); pos['A']=k+2; tick(occ())
    if mode==2 and 'B' in pos: RUN('B',M)
    s=env['s']; l=s+4 if mode==1 else s+2
    for _ in range((x-env['t']-2+2*l)%N): tick(occ())
    p=4 if mode==1 else 2
    tick({p-1,p}); tick({p})
    exp=Counter()
    if mode==1:
        for j in G2: exp[(l,0,j)]+=1
        for j in G3: exp[(l,1,j)]+=1
        for j in G1: exp[(l+M,1,j)]+=1
    else:
        for j in G3: exp[(l,0,j)]+=1
        for j in G1: exp[(l+M,0,j)]+=1
        for j in G2: exp[(l+M,1,j)]+=1
    ok=(+st==+exp) and all((env['t']-2*lam)%N==x for lam,_,_ in st)
    return ok,env['maxmask'],env['t'],dict(st),dict(exp)
if __name__=='__main__':
    out=open(sys.argv[1],'x'); seed=int(sys.argv[2]); rng=random.Random(seed)
    summary={}; fails=[]
    for N in (16,9,11,17,18,13,32,7,14,3,5,6,10,12,4,8):
        M=N//2 if N%2==0 else N
        xs=range(N) if N==16 else sorted({0,1,N-1})
        for q in (1,2,3):
            opts=[()]+[(j,) for j in range(q)]
            reqs=list(itertools.product(opts,repeat=3))
            for _ in range(40): reqs.append(tuple(tuple(rng.randrange(q) for _ in range(rng.randint(0,3))) for _ in range(3)))
            for mode in (1,2):
                key='N%d_M%d_q%d_mode%d_%s'%(N,M,q,mode,'qualifies' if M>=8 else 'subbound')
                c={'cases':0,'T1_fail':0,'T2_fail':0,'maxmask':0}
                for G1,G2,G3 in reqs:
                    for x in xs:
                        ok,mm,T,st,ex=run(N,q,mode,G1,G2,G3,x)
                        c['cases']+=1; c['maxmask']=max(c['maxmask'],mm)
                        if mm>5: c['T2_fail']+=1
                        if not ok:
                            c['T1_fail']+=1
                            if len([f for f in fails if f[0]==N])<4: fails.append([N,q,mode,G1,G2,G3,x,T,sorted(map(str,st.items())),sorted(map(str,ex.items()))])
                summary[key]=c; print(key,c,flush=True)
    json.dump({'seed':seed,'summary':summary,'first_failures':fails},out,indent=1); out.close()
