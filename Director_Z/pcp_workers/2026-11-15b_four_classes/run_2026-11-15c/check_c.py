#!/usr/bin/env python3
"""check_c.py OUT  -- exact check of claim (c) of Step 2 (no randomness; seed 20261113 unused).
Group G = <delta, beta>, delta of order r, beta^s = delta^k0, elements beta^i delta^n (0<=i<s, n mod r).
Multisets = dicts in N[G].  Factor P(p,q;N) = (N+p)D0+(N-p)D1 + ((N+q)D0+(N-q)D1) e_beta,
D0 = sum delta^even, D1 = delta*D0.
PREDICATES fixed before the first run:
 C1 (j=0 realisation) for the relation R2 = square of (-3+X)(1+X) == -X^2 (1+X)^2(-1+2X) mod X^4-1, which has j=0,
    the padded construction gives prod P_A == T_{delta^e} prod P_B exactly in N[G], for r in {2,4,6}, k0 in {0,2}.
 C2 (j!=0 with counts (2N,2N)) for R itself (j=2): prod P_A == T_{delta^e beta^2} prod P_B FAILS (expected: claim (c)
    as written is false for j not 0 mod s).  Kept either way.
 C3 R0: e_beta*(7D0+D0 e_b)*(D0+D0 e_b)^2 == (D0+3D0 e_b)^2*(D0+D0 e_b) holds for r in {2,4,6}, k0 in {0,2};
    and the same with e_1 in place of D0 holds for k0=0 and fails for k0=2 (r=4).
 C4 sigma=-1 control: the construction for a j=0 relation of X^4+1 (the trivial one X^4 == -1 is j=4: use
    (1+X)^4 * ... ) is not tested here (no j=0 relation known yet).
Hypothesis check per case: s=4 cosets distinct (beta^i not in <delta> for 0<i<4) -- true by construction of G.
Result file opened with mode 'x'.
"""
import sys, json
from collections import Counter
out=open(sys.argv[1],'x'); res={}
def mk(r,s,k0):
    def mul(a,b):
        i=a[0]+b[0]; n=a[1]+b[1]
        if i>=s: i-=s; n+=k0
        return (i,n%r)
    def conv(A,B):
        C=Counter()
        for g,x in A.items():
            for h,y in B.items(): C[mul(g,h)]+=x*y
        return +C
    return mul,conv
def D(r,par,i,c):  # c*D_par at coset i
    return Counter({(i,n):c for n in range(r) if n%2==par}) if c else Counter()
def P(r,p,q,N):
    A=D(r,0,0,N+p)+D(r,1,0,N-p)+D(r,0,1,N+q)+D(r,1,1,N-q); return +A
def prodl(conv,L):
    acc=Counter({(0,0):1})
    for x in L: acc=conv(acc,x)
    return acc
def T(mul,g,A): return +Counter({mul(g,h):x for h,x in A.items()})
RA=[(-3,1),(1,1)]; RB=[(1,1),(1,1),(-1,2)]   # j=2, eps=-1
R2A=RA*2; R2B=RB*2                          # j=4 -> X^4=1, eps=+1
c1=[];c2=[];c3=[]
for r in (2,4,6):
  for k0 in (0,2):
    mul,conv=mk(r,4,k0); N=3
    A=R2A+[(1,0)]*(len(R2B)-len(R2A)); B=list(R2B)
    ok=prodl(conv,[P(r,p,q,N) for p,q in A])==prodl(conv,[P(r,p,q,N) for p,q in B])
    c1.append([r,k0,ok])
    A=RA+[(1,0)]; B=RB
    ok2=prodl(conv,[P(r,p,q,N) for p,q in A])==T(mul,(2,1),prodl(conv,[P(r,p,q,N) for p,q in B]))
    ok2b=prodl(conv,[P(r,p,q,N) for p,q in A])==T(mul,(2,0),prodl(conv,[P(r,p,q,N) for p,q in B]))
    c2.append([r,k0,ok2,ok2b])
    f=lambda a,b: +(D(r,0,0,a)+D(r,0,1,b))
    ok3=T(mul,(1,0),prodl(conv,[f(7,1),f(1,1),f(1,1)]))==prodl(conv,[f(1,3),f(1,3),f(1,1)])
    c3.append([r,k0,ok3])
e=lambda a,b: +Counter({(0,0):a,(1,0):b})
for k0 in (0,2):
    mul,conv=mk(4,4,k0)
    c3.append(['e1-version r=4',k0,T(mul,(1,0),prodl(conv,[e(7,1),e(1,1),e(1,1)]))==prodl(conv,[e(1,3),e(1,3),e(1,1)])])
res=dict(argv=sys.argv,C1=c1,C1_pass=all(x[2] for x in c1),C2_rows_r_k0_shiftbeta2_shift_none=c2,
 C2_fails_as_expected=not any(x[2] for x in c2),C3=c3)
json.dump(res,out,indent=1); out.close(); print(json.dumps(res))
