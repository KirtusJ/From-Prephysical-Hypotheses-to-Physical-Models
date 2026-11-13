#!/usr/bin/env python3
"""Fresh exact checks of selected displayed operational examples.

This program contains no archived code and performs no empirical or universal
proof certification. SymPy rational identities and Fraction comparisons are
exact. Decimal displays are approximations for readability only.
"""
from datetime import datetime, timezone
from fractions import Fraction as F
from hashlib import sha256
from math import comb
from pathlib import Path
import json
import platform
import sympy as sp

HERE = Path(__file__).resolve().parent
MATERIALS = HERE.parents[2]
SOURCE = MATERIALS / "Related_Source_Editions/Operational_Identification_of_Records_Controls_and_Continuous_Time_Dynamics.pdf"
checks = []

def check(name, predicate, details=None):
    if not bool(predicate):
        raise AssertionError(name)
    checks.append({"name": name, "passed": True, "arithmetic": "exact", "details": details})

def matrix_equal(a, b):
    return a.shape == b.shape and all(sp.simplify(x-y) == 0 for x,y in zip(a,b))

def strings(m):
    return [[str(x) for x in row] for row in m.tolist()]

one = sp.ones(2,1)
T0 = sp.Matrix([[6,2],[1,3]])/20
T1 = sp.Matrix([[4,8],[7,9]])/20
pi = sp.Matrix([[sp.Rational(4,9), sp.Rational(5,9)]])
K1 = sp.Matrix([[sp.Rational(3,4),sp.Rational(1,4)], [sp.Rational(1,2),sp.Rational(1,2)]])
K2 = sp.Matrix([[sp.Rational(1,2),sp.Rational(1,2)], [sp.Rational(1,4),sp.Rational(3,4)]])
check("positive stationary row-stochastic model", all(x>0 for T in (T0,T1) for x in T) and (T0+T1)*one==one and pi*(T0+T1)==pi)
H = sp.Matrix(2,2,lambda i,j:(pi*[T0,T1][i]*[T0,T1][j]*one)[0])
check("two-output determinant", H.det()==sp.Rational(53,8100), {"determinant":str(H.det())})
q=(pi*T0*one)[0]
q1=(pi*K1*T0*one)[0]
q2=(pi*K2*T0*one)[0]
check("one-output probabilities", (q,q1,q2)==(sp.Rational(13,45),sp.Rational(29,90),sp.Rational(49,180)))
a1,a2,b1,b2=sp.symbols("a1 a2 b1 b2")
B=sp.Matrix([[b1,-a1-b1],[b2,-a2-b2]])
check("symbolic determinant criterion", sp.expand(B.det())==a1*b2-a2*b1)
Bn=B.subs({a1:sp.Rational(1,4),b1:sp.Rational(1,2),a2:sp.Rational(1,2),b2:sp.Rational(1,4)})
d,k=Bn.inv()*sp.Matrix([q1-q,q2-q])
check("reconstructed emission difference and preparation product", (d,k)==(sp.Rational(1,5),sp.Rational(4,45)) and Bn.det()==-sp.Rational(3,16))
e=T0*one
A=sp.Matrix.vstack(pi,pi*K1)
Fm=sp.Matrix([[1,e[0]],[1,e[1]]])
C0=A*T0*Fm
C1=A*T1*Fm
check("displayed C0 and C1", C0==sp.Matrix([[sp.Rational(13,45),sp.Rational(9,100)],[sp.Rational(29,90),sp.Rational(21,200)]]) and C1==sp.Matrix([[sp.Rational(32,45),sp.Rational(179,900)],[sp.Rational(61,90),sp.Rational(337,1800)]]), {"C0":strings(C0),"C1":strings(C1)})
check("short reconstruction returns matrices", A.inv()*C0*Fm.inv()==T0 and A.inv()*C1*Fm.inv()==T1 and k/d==pi[0])

t=sp.symbols("t",real=True)
S=sp.Matrix([[1-t,t],[2*t,1-2*t]])
N0=sp.Matrix([[6-15*t-t*t,2-5*t+t*t],[1-8*t-t*t,3-12*t+t*t]])
N1=sp.Matrix([[4-3*t-35*t*t,8-37*t+35*t*t],[7-4*t-35*t*t,9-36*t+35*t*t]])
check("symbolic similarity formulas", matrix_equal(S.inv()*T0*S,N0/(20*(1-3*t))) and matrix_equal(S.inv()*T1*S,N1/(20*(1-3*t))))
check("fixed first and perturbed second control", matrix_equal(S.inv()*K1*S,K1) and matrix_equal(S.inv()*K2*S-K2,sp.Matrix([[3*t/4,-3*t/4],[3*t/4,-3*t/4]])))
check("preparation interval formula", matrix_equal(pi*S,sp.Matrix([[(4+6*t)/9,(5-6*t)/9]])))
endpoint=sp.Rational(1,10)
lower0=sp.Matrix([[sp.Rational(449,100),sp.Rational(3,2)],[sp.Rational(19,100),sp.Rational(9,5)]])
lower1=sp.Matrix([[sp.Rational(67,20),sp.Rational(43,10)],[sp.Rational(25,4),sp.Rational(27,5)]])
for idx,(num,lower) in enumerate(((N0,lower0),(N1,lower1))):
    # Every derivative is affine; negativity at both endpoints certifies
    # monotone decrease on the full closed interval, not merely a grid test.
    decreasing=all(sp.diff(x,t).subs(t,0)<0 and sp.diff(x,t).subs(t,endpoint)<0 for x in num)
    check(f"numerator {idx} positive lower bounds on entire interval", decreasing and all(x>=y>0 for x,y in zip(num.subs(t,endpoint),lower)))
check("one-percent calibration witness", sp.Rational(3,4)*sp.Rational(1,75)==sp.Rational(1,100) and (pi*S)[0].subs(t,sp.Rational(1,75))==sp.Rational(34,75) and sp.Rational(34,75)-pi[0]==sp.Rational(2,225))
a,b,u=sp.symbols("a b u",real=True)
K=sp.Matrix([[1-a,a],[b,1-b]])
St=S.subs(t,sp.Rational(1,10))
T0p=St.inv()*T0*St
pip=pi*St
contrast=sp.simplify((pi*K*T0*one)[0]-(pip*K*T0p*one)[0])
check("common-control pair contrast, original minus primed", contrast==(2*a-b)/35)
reset=sp.ones(2,1)*sp.Matrix([[u,1-u]])
check("reset probability functions", sp.simplify((pi*reset*T0*one)[0]-(1+u)/5)==0 and sp.simplify((pip*reset*T0p*one)[0]-(1+2*u)/7)==0)
check("endpoint reset similarity", St.inv()*reset.subs(u,0)*St==reset.subs(u,sp.Rational(1,5)))

E=sp.Matrix([9,12,12,16])/25
G=sp.Matrix([9,12,12,-16])/25
XI=sp.kronecker_product(sp.Matrix([[0,1],[1,0]]),sp.eye(2))
pE=(1+(E.T*XI*E)[0])/2
pG=(1+(G.T*XI*G)[0])/2
check("environment vectors normalized and determinant contrast", (E.T*E)[0]==1 and (G.T*G)[0]==1 and sp.Matrix(2,2,list(E)).det()==0 and sp.Matrix(2,2,list(G)).det()==-sp.Rational(288,625))
check("environment readout probability gap", (pE,pG,pE-pG)==(sp.Rational(49,50),sp.Rational(457,1250),sp.Rational(384,625)))
C=sp.Matrix([[0,1,0],[0,0,1],[1,0,0]])
Pi=sp.ones(3,3)/3
R=sp.eye(3)-Pi
Ac=C-C*C
check("cycle exponential algebra", Ac*Pi==sp.zeros(3) and Pi*Ac==sp.zeros(3) and Ac*Ac==-3*R and R*R==R and R*Ac==Ac and Ac*R==Ac)
check("generator rate equivalence", -12*R==4*(C+C*C-2*sp.eye(3)))

def randomized_np(n):
    # Under p0=1/7 and p1=1/5 the likelihood ratio increases in S.
    # Exact size alpha is obtained by rejecting S>k and randomizing at k.
    pmf0=[F(comb(n,j)*6**(n-j),7**n) for j in range(n+1)]
    pmf1=[F(comb(n,j)*4**(n-j),5**n) for j in range(n+1)]
    alpha=F(1,20)
    tail0=F(0)
    tail1=F(0)
    for k in range(n,-1,-1):
        if tail0<=alpha<=tail0+pmf0[k]:
            gamma=(alpha-tail0)/pmf0[k]
            power=tail1+gamma*pmf1[k]
            check(f"NP exact size and feasible randomization N={n}", 0<=gamma<=1 and tail0+gamma*pmf0[k]==alpha)
            return {"n":n,"boundary_count":k,"randomization_approx":float(gamma),"power_approx":float(power),"power_at_least_19_over_20":power>=F(19,20),"power_fraction":str(power)}
        tail0+=pmf0[k]
        tail1+=pmf1[k]
    raise AssertionError("boundary not found")

np_results=[randomized_np(n) for n in (467,468)]
check("exact fixed-horizon minimum 468", not np_results[0]["power_at_least_19_over_20"] and np_results[1]["power_at_least_19_over_20"], {"minimality_reason":"Neyman-Pearson monotone likelihood ratio gives the optimum for each N; optimal power cannot decrease with N because one may ignore added observations. Exact failure at 467 and success at 468 therefore certify this simple iid randomized fixed-horizon boundary."})
for r in np_results:
    # Retain the exact fraction in the local report; no enormous console dump.
    pass
result={
    "schema":"selected_operational_exact_checks_v1",
    "created_at":datetime.now(timezone.utc).isoformat(),
    "time_convention":"UTC execution timestamp",
    "source_pdf":{"path":str(SOURCE.relative_to(MATERIALS)),"relative_to":"Review_Materials","sha256":sha256(SOURCE.read_bytes()).hexdigest(),"physical_pdf_pages":[5,6,7,8,9,10]},
    "program":{"path":str(Path(__file__).resolve()),"sha256":sha256(Path(__file__).read_bytes()).hexdigest(),"python":platform.python_version(),"sympy":sp.__version__},
    "scope":"Fresh exact arithmetic on selected displayed witnesses. No archived code executed. Universal identification and observational-equivalence claims remain supported by their stated analytic proofs and premises, not by these finite checks. No empirical, independent-replication, or novelty claim.",
    "checks":checks,"all_passed":all(c["passed"] for c in checks),"exact_check_count":len(checks),
    "np_boundary":np_results,
}
out=HERE/"Supplied_Operational_Exact_Checks.json"
out.write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps({"report":str(out),"sha256":sha256(out.read_bytes()).hexdigest(),"exact_check_count":len(checks),"all_passed":result["all_passed"],"np_summary":[{k:v for k,v in r.items() if k!="power_fraction"} for r in np_results]},indent=2))
