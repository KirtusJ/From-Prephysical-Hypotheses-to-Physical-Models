import itertools, sympy as sp
def run(ns,B,S):
    G=list(itertools.product(*[range(n) for n in ns])); d=len(B)
    add=lambda a,b:tuple((x+y)%n for x,y,n in zip(a,b,ns))
    chars=G
    def psi(j,h): return sp.exp(2*sp.pi*sp.I*sum(sp.Rational(a*b,n) for a,b,n in zip(j,h,ns)))
    J0=[j for j in chars if all(sp.simplify(psi(j,B[z][y])-1)==0 for z in range(d) for y in range(d))]
    U=[]
    for j in chars:
        P=sp.Matrix(d,d,lambda z,y:psi(j,B[z][y]))
        if sp.simplify(P.H*P-d*sp.eye(d))==sp.zeros(d): U.append(j)
    neg=lambda j:tuple((-x)%n for x,n in zip(j,ns))
    J0s=set(J0); pairs=set()
    for p in U:
        for l in chars:
            if tuple((a+b)%n for a,b,n in zip(p,l,ns)) in J0s: pairs.add(frozenset([p,l]))
    formula=len(J0)+len(pairs)
    # multisets as sorted tuples of elements
    ms=[()]+[c for s in range(1,S+1) for c in itertools.combinations_with_replacement(G,s)]
    idx={m:i for i,m in enumerate(ms)}
    rows=[]
    def comps(tot):
        for sizes in itertools.product(range(tot+1),repeat=d):
            if sum(sizes)<=tot: yield sizes
    for sizes in comps(S):
        for tup in itertools.product(*[list(itertools.combinations_with_replacement(G,s)) for s in sizes]):
            r=[0]*len(ms)
            for z in range(d):
                w=tuple(sorted(add(B[z][y],h) for y in range(d) for h in tup[y])); r[idx[w]]+=1
            for y in range(d): r[idx[tup[y]]]-=d
            if any(r): rows.append(r)
    M=sp.Matrix(rows); null=len(ms)-M.rank()
    print(ns,B,"S=",S,"|J0|=",len(J0),"U=",U,"formula=",formula,"nullity=",null,"PASS" if null==formula else "FAIL")
e=(0,0);a=(1,0);b=(0,1);ab=(1,1)
# control
print("CONTROL chars of C2xC4:",len(list(itertools.product(range(2),range(4)))))
for S in (3,):
  run((2,2),[[e,e,e,e],[e,a,b,ab],[e,b,ab,a],[e,ab,a,b]],S)
  run((2,2),[[e,e,e,e],[e,e,a,a],[e,a,e,a],[e,a,a,b]],S)
  run((2,2),[[e,e],[e,a]],S)
g=(0,1);t=(1,0)
for S in (3,4):
  run((2,4),[[e,e],[e,(0,2)]],S)
  run((2,4),[[e,e],[e,(1,2)]],S)
  run((2,4),[[e,g],[t,(1,1)]],S)
