#!/usr/bin/env python3
"""New finite checks for three coverage additions; no archived imports."""
from fractions import Fraction as F
from itertools import combinations, product
from collections import defaultdict
from math import comb, factorial
import json
import sympy as s

checks=[]
def ck(ok,name):
    if not bool(ok):raise ArithmeticError(name)
    checks.append(name)

# Four-probability conditional odds on every simple labelled four-vertex graph.
n=4
edges=list(combinations(range(n),2))
for bits in product((0,1),repeat=len(edges)):
    graph=[e for e,b in zip(edges,bits) if b]
    weights={w:F(1,2)**sum(w[i]==w[j] for i,j in graph)
             for w in product((-1,1),repeat=n)}
    for i,j in edges:
        rest=[k for k in range(n) if k not in (i,j)]
        for outside in product((-1,1),repeat=len(rest)):
            p={}
            for a,b in product((-1,1),repeat=2):
                w=[0]*n;w[i]=a;w[j]=b
                for k,v in zip(rest,outside):w[k]=v
                p[a,b]=weights[tuple(w)]
            ratio=p[1,1]*p[-1,-1]/(p[1,-1]*p[-1,1])
            ck(ratio==F(1,2)**(2*((i,j) in graph)),
               "graph odds %s pair %s outside %s"%(bits,(i,j),outside))

# The finite signed example and the Legendre aliases.
t=s.symbols("t",real=True)
def sign_law(prior,m):
    result={}
    for w in product((-1,1),repeat=m):
        result[w]=sum(prob*s.prod(s.Rational(1,2)*(1+v*x) for v in w)
                      for x,prob in prior)
    return result
for eta in (s.Rational(1,4),s.Rational(1,10000)):
    A=[(s.sqrt(eta),s.Rational(1,2)),(-s.sqrt(eta),s.Rational(1,2))]
    B=[(0,1-eta),(1,eta/2),(-1,eta/2)]
    for m in range(1,5):
        pa,pb=sign_law(A,m),sign_law(B,m)
        for w in pa:
            want=0 if m<4 else eta*(1-eta)*s.prod(w)/16
            ck(s.simplify(pb[w]-pa[w]-want)==0,
               "latent three-point alias eta=%s m=%d word=%s"%(eta,m,w))
for n in (2,4,6):
    L=s.legendre(n,t)
    for j in range(n):
        ck(s.integrate(t**j*L,(t,-1,1))==0,
           "Legendre orthogonality n=%d j=%d"%(n,j))
    integral=s.integrate(t**n*L,(t,-1,1))
    exact=s.Rational(2**(n+1)*factorial(n)**2,factorial(2*n+1))
    ck(integral==exact,"Legendre leading integral n=%d"%n)
    tv=0
    for w in product((-1,1),repeat=n):
        difference=s.integrate(s.prod(1+v*t for v in w)*L/2**(n+1),(t,-1,1))
        ck(difference==exact*s.prod(w)/2**(n+1),
           "Legendre full pattern n=%d word=%s"%(n,w))
        tv+=abs(difference)/2
    ck(tv==exact/4,"Legendre full TV n=%d"%n)
    if n==4:ck(tv==s.Rational(4,315),"Legendre concrete distance")

# Partitions encoded as tuples of canonical block labels.
def canon(labels):
    lookup={}
    return tuple(lookup.setdefault(x,len(lookup)) for x in labels)
def selected_law(n,u):
    out=defaultdict(F)
    for bits in product((0,1),repeat=n):
        key=canon([("selected",) if b else ("single",i) for i,b in enumerate(bits)])
        out[key]+=u**sum(bits)*(1-u)**(n-sum(bits))
    return dict(out)
def marked_kernel(R,Q,t):
    cells=canon(list(zip(R,Q)))
    k=max(cells)+1
    out=defaultdict(F)
    for marks in product((0,1,2),repeat=k):
        prob=F(1)
        for mark in marks:prob*=t if mark<2 else 1-2*t
        if not prob:continue
        keys=[]
        for i,cell in enumerate(cells):
            mark=marks[cell]
            keys.append(("H",R[i]) if mark==0 else ("V",Q[i]) if mark==1 else ("N",cell))
        out[canon(keys)]+=prob
    return dict(out)
def tv(p,q):
    return sum(abs(p.get(x,F(0))-q.get(x,F(0))) for x in p.keys()|q.keys())/2
for n in range(2,6):
    top=(0,)*n;bottom=tuple(range(n))
    for tval in (F(1,10),F(1,3),F(1,2)):
        first=marked_kernel(top,bottom,tval)
        ck(first==selected_law(n,tval),"marked first law n=%d t=%s"%(n,tval))
        left=defaultdict(F)
        for middle,prob in first.items():
            for final,p in marked_kernel(middle,bottom,tval).items():
                left[final]+=prob*p
        ck(dict(left)==selected_law(n,tval*tval),
           "marked two-step law n=%d t=%s"%(n,tval))
        b1=[sum(F(comb(n,j))*tval**j*(1-tval)**(n-j) for j in (0,1))]
        b2=[sum(F(comb(n,j))*(tval*tval)**j*(1-tval*tval)**(n-j) for j in (0,1))]
        for j in range(2,n+1):
            b1.append(F(comb(n,j))*tval**j*(1-tval)**(n-j))
            b2.append(F(comb(n,j))*(tval*tval)**j*(1-tval*tval)**(n-j))
        ck(tv(first,dict(left))==sum(abs(a-b) for a,b in zip(b1,b2))/2,
           "marked aggregated-binomial TV n=%d t=%s"%(n,tval))

print(json.dumps({"status":"PASS","exact_predicate_count":len(checks),
 "archived_programs_executed":False,"checks":checks,
 "unrestricted_claims":"Use the displayed algebraic and limit proofs; finite checks do not establish all-size theorems."},indent=2))
