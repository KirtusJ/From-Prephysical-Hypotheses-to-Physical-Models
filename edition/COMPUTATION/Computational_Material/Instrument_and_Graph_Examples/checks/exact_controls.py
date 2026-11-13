"""Exact checks of the graph, channel, and simple-law power examples."""
from decimal import Decimal, localcontext
from itertools import combinations, product
from math import comb
from fractions import Fraction
import sympy as sp


def check(condition, message):
    if not condition:
        raise ArithmeticError(message)


def graph_check():
    sites = list(product(range(4), repeat=2))
    rook = {(i, 0) for i in range(1, 4)} | {(0, i) for i in range(1, 4)}
    shrikhande = {(1, 0), (3, 0), (0, 1), (0, 3), (1, 1), (3, 3)}
    counts = []
    for directions in [rook, shrikhande]:
        def entry(i, j):
            a, b = sites[i]
            x, y = sites[j]
            return int(((x-a) % 4, (y-b) % 4) in directions)
        adj = sp.Matrix(16, 16, entry)
        lap = 6*sp.eye(16)-adj
        ranks = []
        for eig, others in [(0, (4, 8)), (4, (0, 8)), (8, (0, 4))]:
            a, b = others
            proj = (lap-a*sp.eye(16))*(lap-b*sp.eye(16))/((eig-a)*(eig-b))
            check(proj**2 == proj and lap*proj == eig*proj, 'spectral projection')
            ranks.append(proj.trace())
            for i, j in combinations(range(16), 2):
                for sign in (-1, 1):
                    v = (sp.eye(16)[:, i] + sign*sp.I*sp.eye(16)[:, j])/sp.sqrt(2)
                    check((v.H*proj*v)[0].simplify() == proj.trace()/16, 'pair weight')
        check(ranks == [1, 6, 9], 'multiplicities')
        counts.append(sum(all(adj[i, j] for i,j in combinations(v, 2)) for v in combinations(range(16), 4)))
    check(counts == [8, 0], 'four-cliques')
    print('Both graphs: 120 labelled pairs, both signs, masses (1,6,9)/16. Four-cliques: 8 and 0.')


def phase_check():
    kron=sp.kronecker_product
    X=sp.Matrix([[0,1],[1,0]])
    Z=sp.diag(1,-1)
    Y=sp.Matrix([[0,-sp.I],[sp.I,0]])
    U=sp.I*kron(Z,sp.eye(2))
    V=sp.I*kron(X,sp.eye(2))
    eye=sp.eye(4)
    kraus=([eye/2,U/2,V/sp.sqrt(2)], [(eye-U)/2,V/sp.sqrt(2)])
    def vec(k):
        return sp.Matrix(list(k))/2  # output index followed by input index
    def chan(ks, rho):
        return sum((k*rho*k.H for k in ks),sp.zeros(4)).applyfunc(sp.simplify)
    def projector(v):
        return v*v.H
    P, Q = projector(vec(eye)),projector(vec(U))
    purities=[];rates=[]; states=[]
    for ks in kraus:
        check((sum((k.H*k for k in ks),sp.zeros(4))-eye).applyfunc(sp.simplify)==sp.zeros(4),'trace preserving')
        C=sum((projector(vec(k)) for k in ks),sp.zeros(16)).applyfunc(sp.simplify)
        purities.append(sp.trace(C*C))
        for E in [P,Q]:
            check(P*E==E*P and sp.trace(E*C)==sp.Rational(1,4),'phase invariance at endpoint')
        states.append([chan(ks,projector(eye[:,j])) for j in range(4)])
        plus0=(eye[:,0]+eye[:,2])/sp.sqrt(2)
        rates.append(sp.trace(kron((sp.eye(2)+Y)/2,sp.eye(2))*chan(ks,projector(plus0))).simplify())
    check(states[0]==states[1],'complete basis outputs')
    check(purities==[sp.Rational(3,8),sp.Rational(1,2)] and rates==[sp.Rational(1,2),sp.Rational(3,4)],'coherent probe')
    print('Endpoint scan: 1/4 at all phases. Purities: 3/8, 1/2. Coherent-input Y probabilities: 1/2, 3/4.')


def risk_enclosure(n, reciprocal_rate, cutoff=65):
    # Conditional on an informative success, the null no-click probability is 1/5.
    denominator=reciprocal_rate**n
    weight=(reciprocal_rate-1)**n
    retained=0; numerator=0
    for m in range(cutoff+1):
        upper=sum(comb(m,k)*4**(m-k) for k in range(m//2+1,m+1))
        tie=comb(m,m//2)*4**(m//2) if m%2==0 else 0
        numerator+=weight*(2*upper+tie)*5**(cutoff-m)
        retained+=weight
        weight, remainder=divmod(weight*(n-m),(m+1)*(reciprocal_rate-1))
        check(remainder==0,'exact binomial recurrence')
    den=2*denominator*5**cutoff
    lo=Fraction(numerator,den)
    return lo, lo+Fraction(denominator-retained,2*denominator)


def power_check():
    for reciprocal, first in [(1000,7065),(2000,14131)]:
        for n in (first-1,first):
            lo,hi=risk_enclosure(n,reciprocal)
            check(lo>Fraction(1,20) if n<first else hi<Fraction(1,20),'threshold')
            check(hi-lo<Fraction(1,10**38),'tail width')
            with localcontext() as ctx:
                ctx.prec=35
                value=Decimal(lo.numerator)/Decimal(lo.denominator)
                print(f'Informative success 1/{reciprocal}; N={n}; risk approximately {value:.14f}; exact side of 1/20 certified.')
    # Check assignment-aware bounds in high precision, separately from the supplied verifier.
    with localcontext() as ctx:
        ctx.prec=70
        D=Decimal
        for q,expected in [('1',3837),('0.75',5116),('0.5',7675),('0.25',15350)]:
            ratio=D('.1').ln()/(1-D(q)*D('.0006')).ln()
            check(expected-1<ratio<=expected,'TV count')
        k=(D('.95')-D('.05'))*D(19).ln()
        for l,u,expected in [('.2','.8',6372),('.45','.55',264114)]:
            kl=(D(u)-D(l))*(D(u)/D(l)).ln()
            ratio=k/(D('.0005')*kl)
            check(expected-1<ratio<=expected,'KL count')
    print('Uniform four-arm necessary bounds: TV 7,675 at gap 0.6; KL 264,114 at gap 0.10.')


if __name__=='__main__':
    graph_check()
    phase_check()
    power_check()
