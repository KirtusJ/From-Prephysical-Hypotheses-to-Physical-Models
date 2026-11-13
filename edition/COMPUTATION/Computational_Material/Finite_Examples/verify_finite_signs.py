#!/usr/bin/env python3
"""Exact finite checks for graph-sign comparators and binary extensions.

New implementation from the displayed mathematical definitions.
No archived program is imported or executed. Unrestricted conclusions use
the accompanying proofs, not the number of predicates in this program.
"""
from collections import defaultdict
from fractions import Fraction as F
from itertools import product, combinations
from math import comb
import json
import sympy as s

checks = []
results = {}


def ck(condition, name):
    if not bool(condition):
        raise ArithmeticError(name)
    checks.append(name)


def words(n):
    return product((0, 1), repeat=n)


def p4_word(w):
    M = 2*sum(w)-4
    return F(1, 2**(M*M//4))*F(8, 81)


target = [F(1, 162), F(16, 81), F(16, 27), F(16, 81), F(1, 162)]
ck([sum(p4_word(w) for w in words(4) if sum(w) == k) for k in range(5)]
   == target, "four-sign count distribution")
ck(sum(p4_word(w)*(2*w[0]-1)*(2*w[1]-1) for w in words(4))
   == -F(5, 27), "four-sign pair correlation")


def extension_word(n, w):
    k = sum(w)
    if k in (0, n):
        return F(1, 162)
    if (n == 5 and k in (2, 3)) or (n == 6 and k == 3):
        return F(4, 81)
    return F(0)


def hypergeom(n, k, j):
    def choose(a, b):
        return comb(a, b) if 0 <= b <= a else 0
    return F(choose(k, j)*choose(n-k, 4-j), comb(n, 4))


for n in (5, 6):
    law = {w: extension_word(n, w) for w in words(n)}
    ck(sum(law.values()) == 1, "extension normalized N=%d" % n)
    for subset in combinations(range(n), 4):
        for pattern in words(4):
            actual = sum(p for w, p in law.items()
                         if tuple(w[i] for i in subset) == pattern)
            ck(actual == p4_word(pattern), "complete marginal N=%d %s %s"
               % (n, subset, pattern))
    for k in range(n+1):
        if n == 5:
            witness = k*(5-k)*(k-2)*(k-3)
            formula = 10*(hypergeom(n,k,1)+hypergeom(n,k,3))-F(20,3)*hypergeom(n,k,2)
        else:
            witness = k*(6-k)*(k-3)**2
            formula = 30*(hypergeom(n,k,1)+hypergeom(n,k,3))-20*hypergeom(n,k,2)
        ck(witness == formula and witness >= 0, "support polynomial N=%d k=%d" % (n,k))
    results["extension_%d_count_law" % n] = [
        str(sum(p for w,p in law.items() if sum(w)==k)) for k in range(n+1)]

distances = {}
for n in range(7, 31):
    m = (n+1)//2
    maximum = F(3*m*(m-1), 2*(2*m-1)*(2*m-3))
    ck(max(hypergeom(n,k,2) for k in range(n+1)) == maximum,
       "central hypergeometric maximum N=%d" % n)
    if n % 2 == 0:
        q = [hypergeom(n,m,j) for j in range(5)]
    else:
        q = [(hypergeom(n,m-1,j)+hypergeom(n,m,j))/2 for j in range(5)]
    d = sum(abs(x-y) for x,y in zip(target,q))/2
    ck(d == F(16,27)-maximum, "finite staircase attained N=%d" % n)
    distances[n] = str(d)
ck(distances[7] == str(F(74,945)) and distances[8] == str(F(74,945)),
   "seven and eight sharp distance")
fair = [F(comb(4,k),16) for k in range(5)]
ck(sum(abs(x-y) for x,y in zip(target,fair))/2 == F(47,216),
   "infinite-exchangeable sharp distance attained")
results["finite_distances"] = distances

# Exact finite-range optimum and its two dual certificates.
R = s.symbols("R", positive=True)
v = 3*R/(5*R+2)
a,b,c = s.symbols("a b c", positive=True)
expr = 12*c+2*v*(a+b)
normalized_expr = expr.subs(a,(1-10*b-20*c)/2)
ck(s.simplify(normalized_expr-v-24*(c-R*b)/(5*R+2)) == 0,
   "second action-range dual identity")
ck(s.simplify(s.Rational(16,27)+v/81-v-32/(27*(5*R+2))) == 0,
   "second action-range lower bound")
for rv in (F(1),F(2),F(8),F(78,5),F(16),F(32),F(100)):
    if rv <= F(78,5):
        aa=bb=1/(4*(5*rv+3));cc=rv*bb
        optimum=F(16,27)-3*rv/(5*rv+3)
    else:
        bb=F(20,81)/(5*rv+2);cc=rv*bb;aa=F(1,162)-bb
        optimum=F(32,27)/(5*rv+2)
    q=[aa+bb,4*(bb+cc),12*cc,4*(bb+cc),aa+bb]
    ck(min(aa,bb,cc)>0 and max(aa,bb,cc)<=rv*min(aa,bb,cc)
       and 2*aa+10*bb+20*cc==1, "action-range weights admissible R=%s"%rv)
    ck(sum(abs(x-y) for x,y in zip(target,q))/2==optimum,
       "action-range bound attained R=%s"%rv)

x = s.symbols("x", real=True)
ck(s.simplify(s.cosh(2*x)/s.cosh(x)**4-(1-s.tanh(x)**4)) == 0,
   "quadratic marginal closure identity")

# Signless action at the alternating four-cycle minimum.
cycle=s.Matrix([[0,1,0,1],[1,0,1,0],[0,1,0,1],[1,0,1,0]])
Q=2*s.eye(4)+cycle
ck(Q.eigenvals()=={0:1,2:2,4:1}, "four-cycle signless spectrum")
ck(Q*s.Matrix([1,-1,1,-1])==s.zeros(4,1), "alternating zero mode")
ck(sum((u-v)**2 for u,v in [(1,-1),(-1,1),(1,-1),(-1,1)])==16,
   "four-cycle edge variation")

# Complete graph-sign enumeration; powers of z are integer counts.
z=s.symbols("z")
graphs={
 "A5":(5,[(0,1),(1,2),(2,0),(0,3),(0,4)]),
 "B5":(5,[(0,1),(1,2),(2,0),(0,3),(3,4)]),
 "A6":(6,[(0,1),(0,5),(1,2),(1,5),(2,3),(2,4),(3,4),(4,5)]),
 "B6":(6,[(0,1),(0,4),(0,5),(1,2),(1,5),(2,3),(2,5),(3,4)]),
 "C3":(3,[(0,1),(1,2),(2,0)]),
 "C4":(4,[(0,1),(1,2),(2,3),(3,0)])}
polynomials={}
for name,(n,edges) in graphs.items():
    table=defaultdict(lambda:s.Integer(0))
    for w in product((-1,1),repeat=n):
        table[sum(w)**2]+=z**sum(w[i]==w[j] for i,j in edges)
    polynomials[name]=dict(table)
    results[name]={"magnetization_numerators":{str(k):str(s.expand(v))
                   for k,v in sorted(table.items())},
                   "partition_function":str(s.factor(sum(table.values())))}
Z5=2*z*(1+z)**2*(3+z*z)
Z6=2*z*z*(1+z)**2*(1+z*z)*(z*z-2*z+5)
for name,expected in [('A5',Z5),('B5',Z5),('A6',Z6),('B6',Z6)]:
    ck(s.expand(sum(polynomials[name].values())-expected)==0,
       "partition polynomial "+name)
diff5=s.factor((polynomials['A5'][9]-polynomials['B5'][9])/Z5)
diff6=s.factor((polynomials['A6'][4]-polynomials['B6'][4])/Z6)
ck(s.simplify(diff5-(1-z)**2/((1+z)*(3+z*z)))==0,
   "five-vertex magnetization difference")
ck(s.simplify(diff6-(1-z)**3/((1+z)*(1+z*z)*(z*z-2*z+5)))==0,
   "six-vertex magnetization difference")
ck(diff5.subs(z,s.Rational(1,2))==s.Rational(2,39)
   and diff6.subs(z,s.Rational(1,2))==s.Rational(4,255),
   "graph aliases exact total variation")
u=(1+s.I)/s.sqrt(2)
for name,target_sq in [('C3',s.Rational(145,169)),('C4',s.Rational(801,1681))]:
    polynomial=sum(polynomials[name].values())
    coherence=polynomial.subs(z,u/2)/polynomial.subs(z,s.Rational(1,2))
    ck(s.simplify(coherence*s.conjugate(coherence))==target_sq,
       "cycle coherence "+name)
conditioned=(u+s.Rational(1,4)*u**3)/s.Rational(5,4)
sq=s.simplify(conditioned*s.conjugate(conditioned))
ck(sq==s.Rational(17,25) and (1+sq)/2==s.Rational(21,25),
   "triangle eliminated-vertex conditional purity")

for p in range(1,5):
    for q in range(1,5):
        n=p+q
        adjacency=s.zeros(n)
        for i in range(p):
            for j in range(p,n):
                adjacency[i,j]=adjacency[j,i]=1
        degrees=[q]*p+[p]*q
        lap=s.diag(*degrees)-adjacency
        norm=s.eye(n)-adjacency/s.sqrt(p*q)
        expected={s.Integer(0):1,s.Integer(2):1}
        if n>2:expected[s.Integer(1)]=n-2
        ck(norm.eigenvals()==expected,"normalized complete-bipartite spectrum %d,%d"%(p,q))
        expected_lap=defaultdict(int)
        expected_lap[0]+=1;expected_lap[n]+=1
        if q>1:expected_lap[p]+=q-1
        if p>1:expected_lap[q]+=p-1
        ck(lap.eigenvals()==dict(expected_lap),"unnormalized complete-bipartite spectrum %d,%d"%(p,q))

print(json.dumps({"status":"PASS","finite_check_count":len(checks),
                  "archived_code_executed":False,"checks":checks,
                  "results":results},indent=2))
