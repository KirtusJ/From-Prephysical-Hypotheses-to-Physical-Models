#!/usr/bin/env python3
"""Exact identities and numerical controls for a conditional Markov embedding witness.

The analytic proof is in the accompanying report. Finite checks do not prove
all-time or adaptive-policy statements, physical clock emergence, or novelty.
No random simulation or physical data are used. Python 3 + sympy + mpmath.
"""
import json
import platform
import sys
import sympy as sp
import mpmath as mp

checks = []

def require(name, truth):
    ok = bool(truth)
    checks.append({"name": name, "passed": ok})
    if not ok:
        raise RuntimeError(name)

def zero(M):
    return all(sp.simplify(x) == 0 for x in M)

I = sp.eye(3)
C = sp.Matrix([[0, 1, 0], [0, 0, 1], [1, 0, 0]])
Pi = sp.ones(3)/3
R = I-Pi
A = C-C**2
omega = 2*sp.pi/sp.sqrt(3)
Q0 = -12*R
Q1 = Q0+omega*A
t = sp.Symbol('t', real=True)
P0 = Pi+sp.exp(-12*t)*R
P1 = Pi+sp.exp(-12*t)*(sp.cos(2*sp.pi*t)*R+sp.sin(2*sp.pi*t)*A/sp.sqrt(3))
require('cycle order three', C**3 == I)
require('stationary projection idempotent', Pi**2 == Pi)
require('complement projection idempotent', R**2 == R)
require('skew generator annihilates stationary projection', A*Pi == sp.zeros(3) and Pi*A == sp.zeros(3))
require('rotation square on complement', A**2 == -3*R)
require('rotation and decay commute', Q0*A == A*Q0)
require('generators have zero row sums', Q0*sp.ones(3,1) == sp.zeros(3,1) and Q1*sp.ones(3,1) == sp.zeros(3,1))
require('uniform distribution stationary', sp.ones(1,3)*Q0 == sp.zeros(1,3) and sp.ones(1,3)*Q1 == sp.zeros(1,3))
# pi < 22/7 and (22/7)^2 < 12 imply pi < 2 sqrt(3), hence all rates positive.
require('rational upper bound square below twelve', sp.Rational(22,7)**2 < 12)
require('symbolic minimum rate positive', bool((4-omega).is_positive))
require('first semigroup starts at identity', P0.subs(t,0) == I)
require('second semigroup starts at identity', P1.subs(t,0) == I)
require('first semigroup solves matrix ODE', zero(sp.diff(P0,t)-P0*Q0))
require('second semigroup solves matrix ODE', zero(sp.diff(P1,t)-P1*Q1))
require('first generator reversible with uniform stationary law', Q0 == Q0.T)
require('second generator violates uniform detailed balance', Q1 != Q1.T)
x=sp.Symbol('x')
require('first characteristic polynomial', sp.expand(Q0.charpoly(x).as_expr()-x*(x+12)**2) == 0)
require('second characteristic polynomial', sp.simplify(Q1.charpoly(x).as_expr()-x*((x+12)**2+4*sp.pi**2)) == 0)
for n in range(13):
    require('sampled equality at integer '+str(n), zero(P1.subs(t,n)-P0.subs(t,n)))
require('quarter-interval oriented contrast', sp.simplify((P1[0,1]-P1[0,2]).subs(t,sp.Rational(1,4))-2*sp.exp(-3)/sp.sqrt(3)) == 0)
require('symmetric oriented contrast zero', sp.simplify(P0[0,1]-P0[0,2]) == 0)
require('exact one-interval matrix', zero(P1.subs(t,1)-(Pi+sp.exp(-12)*R)))
require('known two-state positive control', sp.exp(sp.Matrix([[-1,1],[1,-1]])) == sp.Matrix([[(1+sp.exp(-2))/2,(1-sp.exp(-2))/2],[(1-sp.exp(-2))/2,(1+sp.exp(-2))/2]]))

# Separately implemented high-precision matrix exponential, not the analytic formula.
mp.mp.dps=70
def mp_matrix(M):
    return mp.matrix([[mp.mpf(str(sp.N(M[i,j],75))) for j in range(M.cols)] for i in range(M.rows)])
mq0=mp_matrix(Q0); mq1=mp_matrix(Q1)
num=[]
for value in [mp.mpf(0),mp.mpf(1)/4,mp.mpf(1)/2,mp.mpf(1),mp.mpf(2),mp.sqrt(2)]:
    e0=mp.expm(value*mq0); e1=mp.expm(value*mq1)
    target0=mp_matrix(P0.subs(t,sp.Float(str(value),75)))
    target1=mp_matrix(P1.subs(t,sp.Float(str(value),75)))
    error=max(abs(e0[i,j]-target0[i,j]) for i in range(3) for j in range(3))
    error=max(error,max(abs(e1[i,j]-target1[i,j]) for i in range(3) for j in range(3)))
    require('independent matrix exponential at '+mp.nstr(value,8), error<mp.mpf('1e-60'))
    require('stochastic nonnegativity at '+mp.nstr(value,8), min(e1)>=-mp.mpf('1e-60'))
    require('stochastic row sums at '+mp.nstr(value,8), max(abs(sum(e1[i,j] for j in range(3))-1) for i in range(3))<mp.mpf('1e-60'))
    num.append({'t':mp.nstr(value,30),'maximum_formula_error':mp.nstr(error,12),'maximum_entry_difference':mp.nstr(max(abs(e0[i,j]-e1[i,j]) for i in range(3) for j in range(3)),25)})

# All discrete experiments telescope through the same P. As a finite concrete
# control, include three output instruments and several arbitrary stochastic controls.
P=Pi+sp.Symbol('rho',real=True)*R
controls=[sp.eye(3),C,sp.ones(3,1)*sp.Matrix([[sp.Rational(1,2),sp.Rational(1,3),sp.Rational(1,6)]])]
effects=[sp.diag(1,0,0),sp.diag(0,1,0),sp.diag(0,0,1)]
start=sp.Matrix([[sp.Rational(1,2),sp.Rational(1,3),sp.Rational(1,6)]])
for i,K in enumerate(controls):
    require('control row sums '+str(i),K*sp.ones(3,1)==sp.ones(3,1))
    require('complete controlled two-output probabilities sum to one '+str(i),sp.simplify(sum((start*P*E*K*P*F*sp.ones(3,1))[0] for E in effects for F in effects)-1)==0)

result={
    'kind':'fresh internal exact symbolic checks and separate high-precision numerical controls',
    'python':platform.python_version(),'sympy':sp.__version__,'mpmath':mp.__version__,
    'checks':checks,'check_count':len(checks),'failed':sum(not c['passed'] for c in checks),
    'Q0':str(Q0),'Q1':str(Q1),'sampled_matrix':'Pi + exp(-12)*(I-Pi)',
    'quarter_oriented_contrast_exact':'2*exp(-3)/sqrt(3)',
    'quarter_oriented_contrast_decimal':str(sp.N(2*sp.exp(-3)/sp.sqrt(3),35)),
    'numerical_controls':num,
    'analytic_only':['All-integer equality from closed semigroup formula','All adaptive boundary-only policies from common conditional kernels','Two incommensurate exact intervals identify any finite matrix generator by dense additive subgroup and continuity','No uniform finite-precision stability on an unbounded generator class'],
    'limits':['No empirical data','No physical clock derived','Known embedding obstruction; no novelty claim','Finite predicates are implementation controls, not a theorem count','Two-interval uniqueness assumes exact full labelled matrices and a shared time-homogeneous semigroup']
}
print(json.dumps(result,indent=2,sort_keys=True))
