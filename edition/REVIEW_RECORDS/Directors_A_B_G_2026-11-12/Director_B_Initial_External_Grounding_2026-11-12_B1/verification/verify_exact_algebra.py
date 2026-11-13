#!/usr/bin/env python3
"""Independent exact-symbolic cross-checks (SymPy) of the report's finite witnesses.
Not a proof of Gelander's theorem, of general CP^n holonomy, or any physical model.
"""
from pathlib import Path
import json
import sympy as s
I=s.I
sqrt2=s.sqrt(2)
zero=s.Matrix([1,0]); x=s.Matrix([1,1])/sqrt2; y=s.Matrix([1,I])/sqrt2
bra=lambda a,b:(a.conjugate().T*b)[0]
B=s.simplify(bra(zero,x)*bra(x,y)*bra(y,zero))
assert s.simplify(B-(1+I)/4)==0
normalized=s.simplify(B/s.sqrt(s.conjugate(B)*B))
assert s.simplify(normalized**2-I)==0
B_conj=s.simplify(bra(zero,x)*bra(x,s.conjugate(y))*bra(s.conjugate(y),zero))
assert s.simplify(B_conj-s.conjugate(B))==0
J=s.Matrix([[0,-1],[1,0]]);R=s.diag(1,-1)
a,b,c,d=s.symbols('a b c d',real=True)
A=s.Matrix([[a,b],[c,d]])
commJ=s.solve(list(A*J-J*A),[a,b,c,d],dict=True)
assert commJ and (len(commJ[0])==2)
commBoth=s.solve(list(A*J-J*A)+list(A*R-R*A),[a,b,c,d],dict=True)
assert commBoth and commBoth[0].get(b)==0 and commBoth[0].get(c)==0
X=s.Matrix([[0,1],[1,0]]);Z=s.diag(1,-1);Id=s.eye(2)
phi=s.Matrix([1,0,0,1])/sqrt2
rho=s.simplify(phi*phi.conjugate().T)
B0=(Z+X)/sqrt2; B1=(Z-X)/sqrt2
bell=s.kronecker_product(Z,B0+B1)+s.kronecker_product(X,B0-B1)
CHSH=s.simplify(s.trace(rho*bell))
assert s.simplify(CHSH-2*sqrt2)==0
pt=s.Matrix(4,4, lambda r,c:rho[2*(r//2)+(c%2), 2*(c//2)+(r%2)])
eigs=pt.eigenvals()
assert eigs=={s.Rational(-1,2):1,s.Rational(1,2):3}
# Wilson D8 projection algebra, symbolic H^2=(u^2+b^2)I
u,m=s.symbols('u m',real=True)
H=u*X+m*Z
assert (H**2-(u*u+m*m)*Id)==s.zeros(2)
# The projector expression is meaningful for (u,m)!=(0,0)
P=(Id-H/s.sqrt(u*u+m*m))/2
assert (P**2-P).applyfunc(s.simplify)==s.zeros(2)
out={'source':'Exact SymPy algebra; definitions stipulated',
 'CP1_orthogonal_axes_B':str(B),'CP1_normalized_B_squared':str(s.expand(normalized**2).simplify()),
 'conjugate_B':str(B_conj),'RP2_SO2_commutant':str(commJ),
 'RP2_O2_commutant':str(commBoth),'Bell_exact_CHSH':str(CHSH),
 'Bell_partial_transpose_spectrum':{str(k):int(v) for k,v in eigs.items()},
 'D8_projector_idempotence':'EXACT_ZERO for symbolic real u,m not both zero',
 'checks':'PASS','limitations':'Symbolic finite witnesses, not an analytic proof of all continuum limit or emergent physics claims'}
Path(__file__).with_name('exact_algebra_results.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print('PASS_EXACT_ALGEBRA',B,CHSH,eigs)
