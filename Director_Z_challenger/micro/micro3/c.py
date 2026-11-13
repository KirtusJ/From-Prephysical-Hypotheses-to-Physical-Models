import sympy as sp, random, cmath, math
from sympy import totient
print({q:(sp.Rational(totient(q),2)) for q in range(2,13)})
# 7
k=sp.Symbol('k'); names=['a','b','-b','a+b','a-b','a+kb','a+(k+1)b']
F={n:sp.Symbol('f_'+str(i)) for i,n in enumerate(names)}
def M(x_minus,x_k,x_a,x_b): return k*F[x_minus]+F[x_k]-(k+1)*F[x_a]-k*(k+1)*F[x_b]
lhs=(k+1)*M('a-b','a+kb','a','b')-k*M('a','a+(k+1)b','a+b','b')+M('a+(k+1)b','a','a+kb','-b')
rhs=k*(k+1)*(F['a+b']+F['a-b']-2*F['a']-F['b']-F['-b'])
print('id7',sp.expand(lhs-rhs))
# 6 and conj-rule consistency
random.seed(1)
def test(d,q,j=1):
    z=cmath.exp(2j*math.pi/q)
    def el(): 
        c=[random.randint(-9,9) for _ in range(q)]
        return c
    def ev(c,j): return sum(ci*z**(j*i) for i,ci in enumerate(c))
    worst=0;wc=0
    for _ in range(200):
        a,b=el(),el()
        for jj in [j for j in range(1,q) if math.gcd(j,q)==1]:
            w=z**(jj*q//d); A,B=ev(a,jj),ev(b,jj)
            out=sorted(abs(sum(w**(zz*y)*(A if y==0 else B) for y in range(d))) for zz in range(d))
            exp=sorted([abs(A+(d-1)*B)]+[abs(A-B)]*(d-1))
            worst=max(worst,max(abs(x-y) for x,y in zip(out,exp)))
            beta=[ev(el(),jj) for _ in range(d)]
            s=sum(abs(sum(w**(zz*y)*beta[y] for y in range(d)))**2 for zz in range(d))
            wc=max(wc,abs(s-d*sum(abs(x)**2 for x in beta)))
    return worst,wc
for d,q in [(2,2),(3,3),(5,5),(4,4),(2,4),(3,6),(5,10),(3,9),(3,12)]: print(d,q,test(d,q))
# -1 as nonneg comb for odd q
for q in (3,5,7,9): print(q, abs(sum(cmath.exp(2j*math.pi*i/q) for i in range(1,q))+1))
# eigen-pairing: lambda*mu=1 only for conjugates, all units j
for q in range(2,13):
    U=[j for j in range(1,q) if math.gcd(j,q)==1]
    bad=[(i,j) for i in U for j in U if (i+j)%q==0 and j!=(q-i)%q]
    print(q,len(set(U)),bad,[j for j in U if (2*j)%q==0])
