import itertools, sympy as sp
# Z: parallelogram m=2 and (1,1,-1,-1), f=n^2 and counter f=n^4, f=|n|
rng=range(-8,9)
for name,f in [("n^2",lambda n:n*n),("n^4",lambda n:n**4),("|n|",abs)]:
    for u in [(1,-1),(1,1,-1,-1)]:
        bad=sum(1 for a in rng for b in rng if sum(f(a+z*b) for z in u)!=len(u)*(f(a)+f(b)))
        print("Z",name,u,"violations",bad)
# solve on Z: f even unknown values f(0..12), m=2 -> dimension of solution space
N=12; fs=sp.symbols('f0:%d'%(N+1)); eq=[]
for a in range(0,N+1):
    for b in range(0,N+1):
        if a+b<=N: eq.append(fs[a+b]+fs[abs(a-b)]-2*fs[a]-2*fs[b])
sol=sp.solve(eq,fs,dict=True)[0]; print("Z m=2 solution:",[sol.get(s,s) for s in fs][:6])
# Gaussian ints as (x,y); Eisenstein as (x,y) = x+y*w
def gmul(p,q): return (p[0]*q[0]-p[1]*q[1],p[0]*q[1]+p[1]*q[0])
def emul(p,q): # w^2=-1-w
    return (p[0]*q[0]-p[1]*q[1], p[0]*q[1]+p[1]*q[0]-p[1]*q[1])
def add(p,q): return (p[0]+q[0],p[1]+q[1])
gn=lambda p:p[0]**2+p[1]**2
en=lambda p:p[0]**2-p[0]*p[1]+p[1]**2
def check(mul,f,us,B):
    pts=[(x,y) for x in range(-B,B+1) for y in range(-B,B+1)]
    return sum(1 for a in pts for b in pts if sum(f(add(a,mul(u,b))) for u in us)!=len(us)*(f(a)+f(b)))
w=(0,1); w2=(-1,-1)
print("Z[w] (1,w,w2) |a|^2 viol",check(emul,en,[(1,0),w,w2],6))
print("Z[w] (1,w,w2) |a|^4 viol",check(emul,lambda p:en(p)**2,[(1,0),w,w2],6))
print("Z[w] (1,-1) |a|^2 viol",check(emul,en,[(1,0),(-1,0)],6))
print("Z[w] 6th roots (1,-w2... ) (1,-1,w,-w) viol",check(emul,en,[(1,0),(-1,0),w,(0,-1)],6))
print("Z[i] (1,-1) |a|^2 viol",check(gmul,gn,[(1,0),(-1,0)],6))
def re4(p):
    q=gmul(p,p); return gmul(q,q)[0]
print("Z[i] (1,i,-1,-i) Re a^4 viol",check(gmul,re4,[(1,0),(0,1),(-1,0),(0,-1)],6), "f(5)",re4((5,0)),"f(3+4i)",re4((3,4)))
print("Z[i] (1,-1) Re a^4 viol",check(gmul,re4,[(1,0),(-1,0)],6))
print("Z[i] (1,i,-1,-i) |a|^4 viol",check(gmul,lambda p:gn(p)**2,[(1,0),(0,1),(-1,0),(0,-1)],6))
# uniqueness on Z[w] with (1,w,w2): unknowns indexed by norm, box
B=5; pts=[(x,y) for x in range(-B,B+1) for y in range(-B,B+1)]
norms=sorted({en(p) for p in pts}); S={n:sp.Symbol('g%d'%n) for n in norms}
eq=set()
for a in pts:
    for b in pts:
        t=[add(a,emul(u,b)) for u in [(1,0),w,w2]]
        if all(en(p) in S for p in t): eq.add(sum(S[en(p)] for p in t)-3*S[en(a)]-3*S[en(b)])
M=sp.Matrix([[e.coeff(S[n]) for n in norms] for e in eq]); print("Z[w] 3-term: unknowns",len(norms),"nullity",len(norms)-M.rank())
S={n:sp.Symbol('g%d'%n) for n in sorted({gn(p) for p in pts})}; norms=sorted(S)
for us,nm in [([(1,0),(-1,0)],"(1,-1)"),([(1,0),(0,1),(-1,0),(0,-1)],"(1,i,-1,-i)")]:
    eq=set()
    for a in pts:
        for b in pts:
            t=[add(a,gmul(u,b)) for u in us]
            if all(gn(p) in S for p in t): eq.add(sum(S[gn(p)] for p in t)-len(us)*S[gn(a)]-len(us)*S[gn(b)])
    M=sp.Matrix([[e.coeff(S[n]) for n in norms] for e in eq]); print("Z[i]",nm,"unknowns",len(norms),"nullity",len(norms)-M.rank())
