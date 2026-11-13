"""Finite checks for Mathematical Supplement, 10 November 2026.

These calculations use exact rational/symbolic arithmetic. They check instances
and displayed constants; they are not proofs of unrestricted theorems or
physical experiments. Requires Python 3 and SymPy. No network or external data.
"""
from collections import Counter, defaultdict
from fractions import Fraction as F
from itertools import combinations, permutations, product
from math import comb, factorial
from pathlib import Path
import argparse
import json
import sys
import sympy as S

checks = []
values = {}

def check(name, condition):
    passed = bool(condition)
    checks.append({"name": name, "passed": passed})
    if not passed:
        raise AssertionError(name)

def equal(name, left, right):
    if isinstance(left, S.MatrixBase):
        ok = (left - right).applyfunc(S.simplify) == S.zeros(*left.shape)
    else:
        ok = S.simplify(left-right) == 0
    check(name, ok)

def td(a, b):
    eig = (a-b).eigenvals()
    return S.simplify(sum(abs(x)*m for x,m in eig.items())/2)

def canonical(seq):
    d = {}
    return tuple(d.setdefault(x,len(d)) for x in seq)

def set_partitions(n):
    if n == 0:
        yield ()
        return
    def rec(prefix, high):
        if len(prefix) == n:
            yield tuple(prefix)
            return
        for j in range(high+2):
            yield from rec(prefix+[j], max(high,j))
    yield from rec([0],0)

def exact_kernels():
    D = S.Matrix([[1,0,0,1],[0,1,-1,0],[0,-1,1,0],[1,0,0,1]])/4
    ones = S.ones(4,1)
    equal("four-alternative total normalization",(ones.T*D*ones)[0],1)
    check("four-alternative spectrum",D.eigenvals()=={S.Rational(1,2):2,S.Integer(0):2})
    v=S.Matrix([1,1,0,1])
    equal("four-alternative event score",(v.T*D*v)[0],S.Rational(5,4))
    cells=[]
    for mask in range(1,8):
        a=S.Matrix([1]+[(mask>>i)&1 for i in range(3)])
        b=ones-a
        if a==ones:
            continue
        if (a.T*D*b)[0]==0 and (a.T*D*a)[0]>0 and (b.T*D*b)[0]>0:
            cells.append(tuple(a))
    check("exactly two positive binary contexts",len(cells)==2)
    v=S.Matrix([1,S.I])/S.sqrt(2)
    d=v*v.conjugate().T
    triple=S.kronecker_product(d,d,d)
    b=S.Matrix([int(i.bit_count()==1) for i in range(8)])
    equal("three-copy event score",(b.T*triple*b)[0],S.Rational(9,8))
    t,u=S.symbols("t u",real=True)
    dt=S.Matrix([[S.Rational(1,2),S.I*t],[-S.I*t,S.Rational(1,2)]])
    du=dt.subs(t,u);b=S.Matrix([0,1,1,0])
    equal("oriented two-copy event",(b.T*S.kronecker_product(dt,du)*b)[0],S.Rational(1,2)+2*t*u)
    a=S.Matrix([1,1,0,0])/S.sqrt(2);b=S.Matrix([0,0,1,1])/S.sqrt(2)
    plus=S.eye(4)/4+(a*a.T-b*b.T)/8
    minus=S.eye(4)/4-(a*a.T-b*b.T)/8
    M=S.Matrix([[1,1,0,0],[0,0,1,1]])
    equal("aggregation input distance",td(plus,minus),S.Rational(1,4))
    equal("aggregation target distance",td(M*plus*M.T,M*minus*M.T),S.Rational(1,2))
    for i,x in enumerate([plus,minus]):
        grouped=S.diag(x[0,0]+x[1,1],x[2,2]+x[3,3])
        equal(f"aggregation attained error {i}",td(grouped,M*x*M.T),S.Rational(1,8))
        equal(f"aggregation success {i}",S.trace(M*x*M.T/2),S.Rational(1,2))
    R=S.Matrix([[1,S.Rational(3,5),S.Rational(21,100)],[S.Rational(3,5),1,S.Rational(3,5)],[S.Rational(21,100),S.Rational(3,5),1]])
    check("strict positive correlation counterexample",set(R.eigenvals())=={S.Rational(1,4),S.Rational(79,100),S.Rational(49,25)})
    check("log-distance triangle fails",R[0,2]<R[0,1]*R[1,2])

def partition_checks():
    expected=[F(1,324),F(39,668168),F(125,556592256),F(4869,30891577600000)]
    for m in range(3,7):
        groups=[[a+1 for a in range(2**m) if a.bit_count()%2==b]for b in (0,1)]
        total=sum(groups[0])
        check(f"power-sum equal total {m}",total==sum(groups[1]))
        for j in range(m):
            check(f"matched power {m},{j}",sum(a**j for a in groups[0])==sum(a**j for a in groups[1]))
        delta=abs(F(sum(a**m for a in groups[0])-sum(a**m for a in groups[1]),(2*total)**m))
        check(f"first moment gap {m}",delta==F(factorial(m),2**(m*(m-1)//2)*(2**m+1)**m))
        stir=Counter(max(p)+1 for p in set_partitions(m))
        tv=delta*sum(count*factorial(b-1)for b,count in stir.items())/2
        check(f"complete pattern distance {m}",tv==expected[m-3])
        values[f"partition_distance_order_{m}"]=str(tv)
    A=[[1,2,3,4],[2,3,4,1],[3,4,1,2],[4,1,2,3]]
    B=[[1,2,3,4],[2,1,4,3],[3,4,1,2],[4,3,2,1]]
    laws=[]
    for mat in [A,B]:
        counts=defaultdict(int)
        event=0
        for cells in product(range(16),repeat=4):
            xs=[x//4 for x in cells];ys=[x%4 for x in cells]
            w=1
            for x,y in zip(xs,ys):w*=mat[x][y]
            counts[(canonical(xs),canonical(ys))]+=w
            if xs[0]==xs[1] and xs[2]==xs[3] and xs[0]!=xs[2] and ys[0]==ys[2] and ys[1]==ys[3] and ys[0]!=ys[1]:
                event+=w
        check("aligned law normalization",sum(counts.values())==40**4)
        laws.append(counts)
        values.setdefault("aligned_event_numerators",[]).append(event)
    tv=F(sum(abs(laws[0][k]-laws[1][k])for k in set(laws[0])|set(laws[1])),2*40**4)
    check("aligned four-position distance",tv==F(3,1250))
    check("aligned event gap",values["aligned_event_numerators"]==[4360,4488])
    check("zero-size repeated event sufficient",F(973,1000)**110<=F(1,20))
    check("zero-size preceding event insufficient",F(973,1000)**109>F(1,20))
    p={1:F(1)}
    for n in range(2,9):
        p[n]=1-sum(F(k,n*comb(n,k))*p[k] for k in range(1,n))
    for n in range(1,5):
        allperm=list(permutations(range(n)));connected=0;sep=0
        for a in allperm:
            for b in allperm:
                parent=list(range(n))
                def find(i):
                    while parent[i]!=i:i=parent[i]
                    return i
                for q in [a,b]:
                    for i,j in enumerate(q):parent[find(i)]=find(j)
                connected+=len({find(i)for i in range(n)})==1
                if n>1:sep+=find(0)!=find(1)
        den=factorial(n)**2
        check(f"permutation transitivity recurrence {n}",F(connected,den)==p[n])
        if n>1:
            formula=sum(F(k*(n-k),n*(n-1)*comb(n,k))*p[k]for k in range(1,n))
            check(f"permutation fixed pair recurrence {n}",F(sep,den)==formula)
    values["permutation_transitivity"]={str(n):str(x)for n,x in p.items()}

def moments(core,m):
    return sum(F(a,36)**m for a in core)+F(1,2**m*(2**m-1))

def variance(core,n):
    s={m:moments(core,m)for m in (3,4,5)}
    return F(9*(n-3)*(n-4),n*(n-1)*(n-2))*(s[5]-s[3]**2)+F(18*(n-3),n*(n-1)*(n-2))*(s[4]-s[3]**2)+F(6,n*(n-1)*(n-2))*(s[3]-s[3]**2)

def sampling_checks():
    cores=[[1,4,6,7],[2,3,5,8]]
    mus=[moments(c,3)for c in cores]
    check("triple means",mus==[F(425,13608),F(439,13608)])
    delta=mus[1]-mus[0]
    def feasible(n):
        a,b=[19*variance(c,n)for c in cores]
        z=delta**2-a-b
        return z>=0 and z*z>=4*a*b
    check("variance certificate sufficient 329180",feasible(329180))
    check("variance certificate insufficient 329179",not feasible(329179))
    for i,c in enumerate(cores):
        v=variance(c,365450)
        check(f"midpoint certificate {i}",v/(v+F(1,1944)**2)<=F(1,20))
    errs=[]
    for i,c in enumerate(cores):
        mu=mus[i];b=F(3,20000);threshold=F(99179,3125000)
        a=variance(c,2000000)+(mu+b)/10000000
        d=(threshold-mu-b)if i==0 else(mu-threshold-b)
        errs.append(a/(a+d*d))
    check("sparse exact alpha",errs[0]==F(25032226015092744528840625,634998927977903024107964257))
    check("sparse exact beta",errs[1]==F(27900695463010851341340625,699384194430517969365104257))
    values["sparse_errors"]=[str(x)for x in errs]
    check("whole procedure size",errs[0]+F(47,5000)<F(1,20))
    check("whole procedure power",1-errs[1]-F(29,20000)>F(19,20))
    # Integer comparisons avoid decimal or exponent-rounding decisions.
    check("quality bad-pass bound",pow(49997,200000)*pow(5,8)*5000 < pow(50000,200000)*pow(2,8)*47)
    check("quality good-fail bound",pow(200007,200000)*pow(2,9)*20000 < pow(200000,200000)*pow(9,9)*29)
    check("zero-error reference bound",pow(9999,46050)*100<pow(10000,46050))
    M=comb(2000000,2);E=M//10000
    def hyper0(e,r):return F(comb(M-e,r),comb(M,r))
    def hyper1(e,r):return F(e*comb(M-e,r-1),comb(M,r))
    for r in [105,106]:
        g=hyper0(E,r);b0=hyper0(E+1,r);b1=hyper1(E+1,r)
        gamma=1-F(1,20)/g;bound=1-b0-b1+gamma*b1
        check(f"adjacent-count boundary {r}",(bound<F(1,100))==(r==105))
        values[f"adjacent_count_omitted_{r}"]={"minimum_bad_acceptance":str(bound),"decimal_for_reading":float(bound)}
        if r==105:
            check("simple randomized good acceptance",1-g+F(19,20)*g>=F(19,20))
            check("simple randomized bad acceptance",1-b0-b1+F(19,20)*b1<=F(1,100))
    values["minimum_query_cap"]=M-105
    # Independently enumerate small labelled experiments to check the variance.
    weights=[F(1,2),F(1,3),F(1,6)]
    for n in [3,4,5]:
        mean=F(0);second=F(0)
        for x in product(range(3),repeat=n):
            prob=F(1)
            for v in x:prob*=weights[v]
            u=F(sum(len({x[i]for i in subset})==1 for subset in combinations(range(n),3)),comb(n,3))
            mean+=prob*u;second+=prob*u*u
        sm={j:sum(w**j for w in weights)for j in (3,4,5)}
        v=sum(F(comb(3,r)*comb(n-3,3-r),comb(n,3))*(sm[6-r]-sm[3]**2)for r in range(1,4)if 0<=3-r<=n-3)
        check(f"enumerated U variance {n}",second-mean**2==v)
    # Every binary report graph through five positions and every clean partition.
    for n in range(2,6):
        edges=list(combinations(range(n),2));index={e:i for i,e in enumerate(edges)}
        for k in range(2,n+1):
            subsets=list(combinations(range(n),k))
            subset_edges=[[index[e]for e in combinations(subset,2)]for subset in subsets]
            scores=[]
            for mask in range(1<<len(edges)):
                scores.append(sum(max(F(0),1-F(sum(not(mask>>i&1)for i in inds),k-1))for inds in subset_edges)/len(subsets))
            sharp=F(k,n*(n-1))
            check(f"report extension sensitivity n{n} k{k}",all(abs(scores[x]-scores[x^(1<<i)])<=sharp for x in range(len(scores))for i in range(len(edges))))
            check(f"report extension sharp witness n{n} k{k}",scores[-1]-scores[-2]==sharp)
            for part in set_partitions(n):
                mask=sum((1<<j)for j,(a,b)in enumerate(edges)if part[a]==part[b])
                clean=F(sum(len({part[i]for i in sub})==1 for sub in subsets),len(subsets))
                check(f"clean agreement n{n} k{k} {part}",scores[mask]==clean)
    # Adjacent-count TV, separately from the enormous numerical example.
    for M in range(2,10):
        for e in range(M):
            for n in range(1,M+1):
                def pmf(E,k):
                    return F(comb(E,k)*comb(M-E,n-k),comb(M,n))if 0<=k<=E and 0<=n-k<=M-E else F(0)
                dist=sum(abs(pmf(e+1,k)-pmf(e,k))for k in range(n+1))/2
                h=[F(comb(e,k)*comb(M-1-e,n-1-k),comb(M-1,n-1))for k in range(n)if k<=e and 0<=n-1-k<=M-1-e]
                check(f"adjacent hypergeometric TV {M},{e},{n}",dist==F(n,M)*max(h))

def quantum_checks():
    I=S.eye(2);X=S.Matrix([[0,1],[1,0]]);Y=S.Matrix([[0,-S.I],[S.I,0]]);Z=S.diag(1,-1)
    kron=S.kronecker_product
    def pt(rho):
        return S.Matrix(4,4,lambda i,j:rho[2*(i//2)+j%2,2*(j//2)+i%2])
    def partial(rho):
        return S.Matrix(2,2,lambda i,j:sum(rho[2*i+b,2*j+b]for b in range(2)))
    for r in [S.Rational(1,2),S.Rational(3,5)]:
        c=S.sqrt(1-r*r);rs=[(I+c*X+t*Z)/2 for t in [r,-r]]
        omega=sum([kron(x,x)for x in rs],S.zeros(4))/2
        U=S.diag(S.exp(S.I*S.pi/4),S.exp(-S.I*S.pi/4),S.exp(-S.I*S.pi/4),S.exp(S.I*S.pi/4))
        pairs=[(U*kron(x,x)*U.conjugate().T).applyfunc(S.simplify)for x in rs]
        rho=(pairs[0]+pairs[1])/2
        explicit=(S.eye(4)-c*(kron(Y,Z)+kron(Z,Y))+c*c*kron(X,X)+r*r*kron(Z,Z))/4
        equal(f"phase Pauli expansion {r}",rho,explicit)
        neg=sum(-v*mul for v,mul in pt(rho).eigenvals().items()if v<0)
        equal(f"phase pair negativity {r}",neg,c*c/2)
        tau=[partial(x)for x in pairs]
        for t,tt in zip([r,-r],tau):equal(f"phase odd factor {t}",tt,(I-c*t*Y+t*Z)/2)
        cross=(kron(tau[0],tau[0])+kron(tau[1],tau[1]))/2
        equal(f"phase cross pair distance {r}",td(rho,cross),(1-r*r)*(3-r*r)/4)
        equal(f"shared independent distance {r}",td(omega,kron((rs[0]+rs[1])/2,(rs[0]+rs[1])/2)),r*r/2)
        J2=S.Rational(3,2)*S.eye(4)+(kron(X,X)+kron(Y,Y)+kron(Z,Z))/2
        equal(f"phase pair Casimir {r}",S.trace(rho*J2),2)
    for N in [2,3,4]:
        dim=2**N;H=S.zeros(dim)
        for pauli in [X,Y,Z]:
            J=S.zeros(dim)
            for i in range(N):J+=kron(*[pauli if j==i else I for j in range(N)])/2
            H+=J*J
        expected={2:{0:1,2:3},3:{S.Rational(3,4):4,S.Rational(15,4):4},4:{0:2,2:9,6:5}}[N]
        check(f"collective spin spectrum {N}",H.eigenvals()==expected)
    x=S.symbols("x",positive=True)
    equal("Gibbs difference factorization",1/(1+3*x*x)-1/(2*(1+x**3)),(1-x)**2*(1+2*x)/(2*(1+3*x*x)*(1+x**3)))
    equal("Gibbs distance log two",1/(1+3*S.Rational(1,4))-1/(2*(1+S.Rational(1,8))),S.Rational(8,63))
    rays=[S.Matrix([1,0]),S.Matrix([-S.Rational(1,2),S.sqrt(3)/2]),S.Matrix([-S.Rational(1,2),-S.sqrt(3)/2])]
    eta=[v*v.T for v in rays]
    equal("trine average",sum(eta,S.zeros(2))/3,I/2)
    common=sum([kron(e,e)for e in eta],S.zeros(4))/3
    equal("shared independent trine distance",td(common,S.eye(4)/4),S.Rational(1,4))
    for m in range(2,12):
        minsum=min(F(3*(a*a+b*b+(m-a-b)**2)+m*m-4*m,8)for a in range(m+1)for b in range(m-a+1))
        check(f"matching alphabet packing {m}",minsum==F(m*(m-2),4)+(F(0)if m%3==0 else F(1,4)))
    for sign in [1,-1]:
        states=[(I+X)/2,(I+sign*Y)/2,(I+Z)/2]
        equal(f"oriented triple {sign}",S.im(S.trace(states[0]*states[1]*states[2])),S.Rational(sign,4))
        equal(f"anonymized calibrated Y {sign}",sum(S.trace((I+Y)*rho/2)for rho in states)/3,S.Rational(1,2)+S.Rational(sign,6))
    r=S.Rational(1,2);L=23
    err=sum(S.binomial(L,k)*((1+r)/2)**k*((1-r)/2)**(L-k)for k in range((L-1)//2+1))
    values["tail_majority_error_L23_r_half"]=str(err)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",default="Mathematical_Examples_Exact_Checks.json")
    args=parser.parse_args()
    exact_kernels()
    partition_checks()
    sampling_checks()
    quantum_checks()
    result={"title":"Exact finite checks for the Mathematical Supplement","date":"2026-11-10",
            "scope":"Rational and symbolic finite examples and displayed constants; no physical measurements; no claim of independent replication.",
            "python":sys.version.split()[0],"sympy":S.__version__,"check_count":len(checks),
            "all_passed":all(c["passed"]for c in checks),"values":values,"checks":checks}
    Path(args.output).write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"all_passed":result["all_passed"],"checks":len(checks),"output":args.output}))

if __name__=="__main__":
    main()
