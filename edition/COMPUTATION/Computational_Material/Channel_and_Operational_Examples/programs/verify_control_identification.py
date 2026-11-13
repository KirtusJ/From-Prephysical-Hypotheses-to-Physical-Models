#!/usr/bin/env python3
"""Exact checks for calibrated two-control identification.

Fresh reanalysis of the supplied two-state example, followed by a new-to-this-
review reconstruction derivation. No empirical data, replication, or literature
novelty claim. Universal conclusions use the companion analytic argument.
"""
from __future__ import annotations
from fractions import Fraction
from itertools import product
from math import comb
from pathlib import Path
import hashlib
import json
import platform
import sympy as sp

M = sp.Matrix
R = sp.Rational
one = M([1, 1])
checks = []

def check(name, condition):
    if not bool(condition):
        raise RuntimeError(name)
    checks.append(name)

def zero(A):
    return all(sp.simplify(x) == 0 for x in A)

def encode(x):
    if isinstance(x, sp.MatrixBase):
        return [[str(x[i,j]) for j in range(x.cols)] for i in range(x.rows)]
    return str(x)

def K(a, b):
    return M([[1-a, a], [b, 1-b]])

T = [M([[6,2],[1,3]])/20, M([[4,8],[7,9]])/20]
pi = M([[R(4,9), R(5,9)]])
S = K(R(1,10), R(1,5))
Tb = [S.inv()*t*S for t in T]
pib = pi*S
Q = K(R(1,10), 0)
Tq = [Q.inv()*t*Q for t in T]
piq = pi*Q
R2 = K(1,0)
check('original row stochastic', zero((T[0]+T[1])*one-one))
check('original stationary', zero(pi*(T[0]+T[1])-pi))
for j,(ts,p) in enumerate([(Tb,pib),(Tq,piq)]):
    check(f'transform {j}: strict positivity', all(x>0 for t in ts for x in t) and all(x>0 for x in p))
    check(f'transform {j}: stochastic',zero((ts[0]+ts[1])*one-one))
    check(f'transform {j}: stationary',zero(p*(ts[0]+ts[1])-p))
H = M([[(pi*T[y]*T[z]*one)[0] for z in range(2)] for y in range(2)])
check('two-output determinant', H.det()==R(53,8100))
a,b,x,y = sp.symbols('a b x y',real=True)
C=K(a,b)
pair_difference=sp.factor((pi*C*T[0]*one-pib*C*Tb[0]*one)[0])
check('pair common-control contrast',sp.simplify(pair_difference-(2*a-b)/35)==0)
check('pair commutator criterion',zero((S*C-C*S).subs(b,2*a)))
check('reset-preserving distinct similarity',zero(Q*R2-R2*Q) and Q!=sp.eye(2))
check('second transformed T0',Tq[0]==M([[531,229],[81,279]])/1800)
check('second transformed T1',Tq[1]==M([[297,743],[567,873]])/1800)
check('reset uncertainty threshold witness', S.inv()*R2*S == M([[R(1,5),R(4,5)],[R(1,5),R(4,5)]]))
u=sp.symbols('u',real=True)
p0 = sp.factor((M([[u,1-u]])*T[0]*one)[0])
p0b=sp.factor((M([[u,1-u]])*Tb[0]*one)[0])
check('first reset-zero law',sp.simplify(p0-(1+u)/5)==0)
check('second reset-zero law',sp.simplify(p0b-(1+2*u)/7)==0)

# Two-control centralizer: S'=I+X has row sums one.
X=M([[-x,x],[y,-y]])
check('general commutator identity',zero(X*C-C*X-M([[b*x-a*y,a*y-b*x],[b*x-a*y,a*y-b*x]])))
a1,b1,a2,b2=sp.symbols('a1 b1 a2 b2',real=True)
Delta=a1*b2-a2*b1
control_pair_commutator=K(a1,b1)*K(a2,b2)-K(a2,b2)*K(a1,b1)
check('two-control noncommutativity determinant',zero(control_pair_commutator-M([[Delta,-Delta],[Delta,-Delta]])))

# Universal two-state reconstruction from q=P(0), qj=P(Kj then 0).
r,e1,e2=sp.symbols('r e1 e2',real=True)
P=M([[r,1-r]])
e=M([e1,e2]); d=e1-e2; k=r*d
q=(P*e)[0]
v1=sp.expand((P*K(a1,b1)*e)[0]-q)
v2=sp.expand((P*K(a2,b2)*e)[0]-q)
B=M([[b1,-(a1+b1)],[b2,-(a2+b2)]])
check('linear reconstruction determinant',sp.factor(B.det())==Delta)
check('probability contrasts linear in d and rd',zero(B*M([d,k])-M([v1,v2])))
recovered=sp.simplify(B.inv()*M([v1,v2]))
check('symbolic emission contrast recovered',sp.simplify(recovered[0]-d)==0)
check('symbolic weighted contrast recovered',sp.simplify(recovered[1]-k)==0)
check('initial distribution recovered',sp.simplify(recovered[1]/recovered[0]-r)==0)
check('second emission recovered',sp.simplify(q-recovered[1]-e2)==0)
check('first emission recovered',sp.simplify(q-recovered[1]+recovered[0]-e1)==0)
q1,q2=sp.symbols('q1 q2')
general_solution=B.inv()*M([q1-sp.Symbol('q'),q2-sp.Symbol('q')])

# Strictly positive calibrated controls, neither a reset nor a permutation.
C1=K(R(1,4),R(1,2)); C2=K(R(1,2),R(1,4))
qval=(pi*T[0]*one)[0]
qj=[(pi*c*T[0]*one)[0] for c in (C1,C2)]
delta_val=R(1,4)*R(1,4)-R(1,2)*R(1,2)
coeff=M([[R(1,2),-R(3,4)],[R(1,4),-R(3,4)]])
dr=coeff.inv()*M([z-qval for z in qj])
rr=dr[1]/dr[0]
erec=M([qval-dr[1]+dr[0],qval-dr[1]])
pirec=M([[rr,1-rr]])
check('concrete probability data', [qval,*qj]==[R(13,45),R(29,90),R(49,180)])
check('concrete preparation recovery',pirec==pi)
check('concrete emission recovery',erec==T[0]*one)
left=pi.col_join(pi*C1)
right=one.row_join(erec)
check('concrete left inverse exists',left.det()==-R(1,6))
check('concrete right inverse exists',right.det()==-R(1,5))
Crecords=[]
for z in range(2):
    obs=M([[(pi*T[z]*one)[0],(pi*T[z]*T[0]*one)[0]],[(pi*C1*T[z]*one)[0],(pi*C1*T[z]*T[0]*one)[0]]])
    check(f'concrete complete T{z} reconstruction',left.inv()*obs*right.inv()==T[z])
    Crecords.append(obs)

# Adverse control pair: proportional (a,b), hence no removal of the gauge.
D1=K(R(1,4),R(1,2)); D2=K(R(1,8),R(1,4))
check('adverse pair commutes',zero(D1*D2-D2*D1))
check('adverse pair retains original similarity',zero(S*D1-D1*S) and zero(S*D2-D2*S))

# Calibration exactness is essential: if both controls may transform with S,
# the controls themselves can remain strictly positive for this witness.
for i,c in enumerate((C1,C2)):
    cb=S.inv()*c*S
    check(f'co-transformed control {i} strictly positive',all(z>0 for z in cb))
    check(f'co-transformed control {i} stochastic',zero(cb*one-one))
    check(f'co-transformed control {i} law agrees',zero(pi*c*T[0]*one-pib*cb*Tb[0]*one))

# A sharper calibration witness: C1 remains exactly fixed, while C2 moves by
# row total variation 3t/4. All output matrices stay strictly positive for
# 0 <= t <= 1/10, as certified by elementary polynomial lower bounds.
t=sp.symbols('t',real=True)
St=K(t,2*t)
Tt=[(St.inv()*z*St).applyfunc(sp.factor) for z in T]
check('local calibration witness fixes first control',zero(St.inv()*C1*St-C1))
check('local second-control variation is exact',zero(St.inv()*C2*St-C2-M([[3*t/4,-3*t/4],[3*t/4,-3*t/4]])))
check('local preparation formula',zero(pi*St-M([[(4+6*t)/9,(5-6*t)/9]])))
positive_lower_bounds=[]
for j,mat in enumerate(Tt):
    for i,z in enumerate(mat):
        numerator=sp.Poly(sp.cancel(z*20*(1-3*t)),t)
        lower=sp.Rational(0)
        for (degree,),coefficient in numerator.terms():
            lower += coefficient if degree==0 else (coefficient*R(1,10)**degree if coefficient<0 else 0)
        check(f'calibration witness strict positivity T{j} entry {i}',lower>0)
        positive_lower_bounds.append(str(lower))

# General finite-state constructive pair: cycle and a pure reset. This checks
# n=2..6. The proof for all n is in the accompanying derivation.
for n in range(2,7):
    cyc=sp.zeros(n)
    for i in range(n): cyc[i,(i+1)%n]=1
    reset=sp.zeros(n)
    for i in range(n): reset[i,0]=1
    for i in range(n):
        target=sp.zeros(n)
        for j in range(n): target[j,i]=1
        check(f'cycle-reset preparation n={n}, state={i}', reset*cyc**i==target)

def exact_power(n):
    alpha=Fraction(1,20)
    p0=[Fraction(comb(n,j)*6**(n-j),7**n) for j in range(n+1)]
    p1=[Fraction(comb(n,j)*4**(n-j),5**n) for j in range(n+1)]
    size=Fraction(0); power=Fraction(0)
    for j in range(n,-1,-1):
        if size+p0[j]>=alpha:
            gamma=(alpha-size)/p0[j]
            return j,gamma,power+gamma*p1[j]
        size+=p0[j];power+=p1[j]
    raise RuntimeError('unreachable')

trial={}
for n in (467,468):
    boundary,gamma,power=exact_power(n)
    check(f'binomial boundary n={n}',boundary=={467:79,468:80}[n])
    check(f'binomial 95 percent relation n={n}',(power>=Fraction(19,20))==(n==468))
    trial[str(n)]={'boundary':boundary,'gamma':str(gamma),'power':str(power),'power_decimal':float(power)}

source=Path(__file__).resolve().parents[1]/'source'/'Operational_Identification_of_Records_Controls_and_Continuous_Time_Dynamics.tex'
result={
 'status':'PASS','provenance':'Exact checks of the companion mathematical study within the same research program; no independent empirical replication.',
 'python':platform.python_version(),'sympy':sp.__version__,
 'source':{'path':'source/'+source.name,'sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'sections':[4,5]},
 'checked_properties':checks,'property_count':len(checks),
 'pair_contrast':str(pair_difference),'first_reset_law':str(p0),'second_reset_law':str(p0b),
 'two_control_theorem':{'condition':'Delta=a1*b2-a2*b1 != 0','contrast_equation':'(q_j-q)=b_j*d-(a_j+b_j)*k; d=e1-e2; k=r*d','reconstruction':[str(sp.factor(z)) for z in general_solution]},
 'example':{'control_1':encode(C1),'control_2':encode(C2),'Delta':str(delta_val),'q':str(qval),'q1':str(qj[0]),'q2':str(qj[1]),'recovered_pi':encode(pirec),'recovered_e':encode(erec),'data_C0':encode(Crecords[0]),'data_C1':encode(Crecords[1]),'T0':encode(T[0]),'T1':encode(T[1])},
 'calibration_countercontrol':{'S_t':encode(St),'t_range':'0 < t <= 1/10','first_control':'unchanged exactly','second_control_row_TV':'3*t/4','transformed_pi':encode(pi*St),'positive_numerator_lower_bounds':positive_lower_bounds,'choice_for_any_error_epsilon':'t=min(1/10, epsilon) gives row-TV=3t/4 < epsilon for every epsilon > 0.','claim':'For any positive error allowance in the second control, an observationally equivalent non-permutation realization remains even with the first control exact.'},
 'binomial_boundaries':trial,
 'limits':['Every control is independently anchored in the same hidden coordinate basis; co-transforming controls restores equivalence.','Same two-state Mealy class, binary alphabet, strictly positive and linearly minimal for the necessity result; outcome-only rank-two implies e1 != e2.','Population-probability reconstruction, not a finite-sample stability or physical calibration theorem.','Noncommuting controls provide class identification but no prephysical interpretation.','General n-state cycle/reset sufficiency is analytic; finite checks n=2..6 are controls, not the universal proof.'],
}
out=Path(__file__).resolve().parents[1]/'results'/'Control_Identification_Results.json'
out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':result['status'],'properties':len(checks),'example':result['example'],'binomial_power':{n:v['power_decimal'] for n,v in trial.items()},'output':str(out)},indent=2))
