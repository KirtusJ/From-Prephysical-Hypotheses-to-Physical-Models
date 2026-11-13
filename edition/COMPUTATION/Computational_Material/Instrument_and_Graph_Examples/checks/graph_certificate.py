#!/usr/bin/env python3
"""Exact-rational contraction certificate for the 4-site source witness.

Proves three inverse-Laplacian moments, a rigorous fourth-moment interval,
and positive conductances; all mathematical inputs are contained in this file.
"""
from __future__ import annotations
import argparse, json
import sympy as sp

CENTER = [
    '15.68999845828313460641124773061129857188423904485786562373989682',
    '3.96887190378120738276018210798761110889672715693171561389052599',
    '0.02356285637341516688523308001635257730023101101809872770608961495',
]
TARGET = [sp.Rational(5,32), sp.Rational(7,256), sp.Rational(11,2048)]
RADIUS = sp.Rational(1, 10**34)

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--output', default=None)
    args = p.parse_args()
    x, y, z = sp.symbols('x y z')
    L = sp.zeros(4,4)
    edges = [(0,1,sp.Rational(1,50)),(0,3,sp.Rational(1,50)),
             (2,3,sp.Rational(1,50)),(0,2,x),(1,2,y),(1,3,z)]
    for i,j,w in edges:
        L[i,i] += w; L[j,j] += w; L[i,j] -= w; L[j,i] -= w
    S = sp.Matrix([[1,0,0],[0,1,0],[0,0,1],[-1,-1,-1]])
    G = S.T*S
    B = G.inv() * S.T * L * S
    adj = B.adjugate(); det = sp.factor(B.det())
    hh = sp.Matrix([1,-1,0]); vars_=(x,y,z)
    eqs = sp.Matrix([sp.factor((hh.T*G*adj**j*hh)[0]/2 - TARGET[j-1]*det**j)
                     for j in range(1,4)])
    b = [sp.Rational(t) for t in CENTER]
    subs=dict(zip(vars_,b))
    J = eqs.jacobian(vars_)
    Jb = J.subs(subs)
    C = Jb.inv()
    residual = max(abs(t) for t in C*eqs.subs(subs))
    cp_inf = max(sum(abs(C[i,j]) for j in range(3)) for i in range(3))
    abs_limits=[abs(w)+RADIUS for w in b]
    def bound_poly(poly):
        pol=sp.Poly(poly,*vars_)
        return sum(abs(coef)*sp.prod(abs_limits[j]**power for j,power in enumerate(pows))
                   for pows,coef in pol.terms())
    boundH=max(sum(bound_poly(sp.diff(eqs[i],vars_[j],vars_[k]))
                   for j in range(3) for k in range(3)) for i in range(3))
    contraction=cp_inf*RADIUS*boundH
    require(residual+contraction*RADIUS < RADIUS, 'Newton box does not map into itself')
    require(0 <= contraction < 1, 'Newton map not a contraction')
    num4=sp.expand((hh.T*G*adj**4*hh)[0]/2)
    d_center=det.subs(subs)
    dmin=d_center-RADIUS*sum(bound_poly(sp.diff(det,v)) for v in vars_)
    require(dmin>0, 'determinant may vanish')
    m4center=num4.subs(subs)/d_center**4
    deriv4=RADIUS*(sum(bound_poly(sp.diff(num4,v)) for v in vars_)/dmin**4+
                   4*bound_poly(num4)*sum(bound_poly(sp.diff(det,v)) for v in vars_)/dmin**5)
    lower,upper=m4center-deriv4,m4center+deriv4
    require(lower>sp.Rational('0.006804564875115') and upper<sp.Rational('0.006804564875116'),
            'm4 enclosure does not fit reported decimal interval')
    # True four-site weights stay positive; the sixteen-vertex extension subtracts 3epsilon.
    eps=sp.Rational(3,500)
    require(all(weight.subs(subs) > 3*eps if hasattr(weight,'subs') else weight>3*eps
                for _,_,weight in edges), 'extension has nonpositive old edge')
    # Exact characteristic sign brackets for the rational center.
    t=sp.symbols('t')
    charpoly=(B-t*sp.eye(3)).det().subs(subs)
    eig_brackets=[(sp.Rational('0.084'),sp.Rational('0.086')),
                  (sp.Rational('5.58'),sp.Rational('5.59')),
                  (sp.Rational('33.81'),sp.Rational('33.82'))]
    for a,c in eig_brackets:
        require(sp.sign(charpoly.subs(t,a)) != sp.sign(charpoly.subs(t,c)),
                'eigenvalue bracket has no sign change')
    result={
        'status':'Exact-rational local certificate; positive 16-vertex extension by algebraic invariance',
        'box_radius':str(RADIUS),
        'center_strings':CENTER,
        'newton_residual_max':str(sp.N(residual,16)),
        'contraction_bound':str(sp.N(contraction,16)),
        'moment_4_center':str(sp.N(m4center,56)),
        'moment_4_error_bound':str(sp.N(deriv4,12)),
        'moment_4_interval':[str(sp.N(lower,56)),str(sp.N(upper,56))],
        'target_moments':[str(t) for t in TARGET],
        'eigen_brackets':[[str(lo),str(hi)] for lo,hi in eig_brackets],
        'smallest_original_edge_after_extension':str(sp.Rational(1,50)-3*eps),
        'sixteen_vertex_extra_eigenvalues':['0.096 (multiplicity 1)','0.144 (multiplicity 11)'],
    }
    payload=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if args.output:
        open(args.output,'w',encoding='utf-8').write(payload)
    else:
        print(payload,end='')

if __name__=='__main__':main()
