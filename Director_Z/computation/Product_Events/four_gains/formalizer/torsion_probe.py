"""Probe (not a proof): is 2-torsion-freeness of the value group needed for Q1(d) undivided,
P(s+s',t) = P(s,t) + P(s',t), P(s,t) = g(s+t) - g(s-t)?
Predicate fixed before the run: for D = Z/n (n = 2..6) and Z/2 x Z/2, Z/2 x Z/4, V = Z/2, Z/4,
enumerate every g : D -> V satisfying g(s+t)+g(s-t) = 2g(s)+2g(t); count those with P non-additive.
Reports the number of g that qualify (satisfy the law) per case."""
import itertools
def run(Dmods, m):
    els = list(itertools.product(*[range(k) for k in Dmods]))
    add = lambda a,b: tuple((x+y)%k for x,y,k in zip(a,b,Dmods))
    sub = lambda a,b: tuple((x-y)%k for x,y,k in zip(a,b,Dmods))
    qual = bad = 0; ex = None
    for vals in itertools.product(range(m), repeat=len(els)):
        g = dict(zip(els, vals))
        if any((g[add(s,t)]+g[sub(s,t)]-2*g[s]-2*g[t])%m for s in els for t in els): continue
        qual += 1
        P = lambda s,t: (g[add(s,t)]-g[sub(s,t)])%m
        if any((P(add(s,s2),t)-P(s,t)-P(s2,t))%m for s in els for s2 in els for t in els):
            bad += 1
            if ex is None: ex = vals
    print(Dmods, "V=Z/%d"%m, "qualify", qual, "P non-additive", bad, "example", ex)
for Dm in [(2,),(3,),(4,),(5,),(6,),(2,2),(2,4)]:
    for m in (2,4):
        run(Dm, m)
