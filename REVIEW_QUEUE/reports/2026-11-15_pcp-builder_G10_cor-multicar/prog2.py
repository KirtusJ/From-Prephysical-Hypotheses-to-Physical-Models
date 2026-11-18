"""Predicates fixed before first run. Seed 20261113.
P3: infinite carrier = signed arc digraph of the line, vertices (k,s), s=+-1, (k,s)->(k+1,+1) gain +1,
 (k,s)->(k-1,-1) gain s (Hadamard). H per case: walks never leave any finite window used (automatic,
 carrier infinite; check A^*A=2 on the vertices touched: common successors of (k,+),(k,-) are both,
 column product sum 0; distinct k share none). For random finite events S (subsets of walks from (0,+)
 of length n<=8), and random integers a,c: mu=sum_y a|m|+c(sum gains)^2 satisfies mu(cont S)=2mu(S).
P4 (control of sharpness): with gain s replaced by +1 (A^*A!=2) the square term fails for some S.
"""
import random
random.seed(20261113)
out=open('result2.txt','x')
def w(s): out.write(s+'\n'); print(s)
def succ(v,hs):
    k,s=v; return [((k+1,1),1),((k-1,-1),s if hs else 1)]
def mu(S,a,c):
    ends={}
    for p,g in S: ends.setdefault(p[-1],[]).append(g)
    return sum(a*len(L)+c*sum(L)**2 for L in ends.values())
for hs,name in ((True,'P3'),(False,'P4')):
    tested=qual=ok=0
    for t in range(200):
        tested+=1
        n=random.randint(1,8); W=[(((0,1),),1)]
        for _ in range(n): W=[(p+(u,),g*h) for p,g in W for u,h in succ(p[-1],hs)]
        verts={p[-1] for p,g in W}
        Hq=all(True for v in verts) and hs  # A^*A=2 holds iff hs (columns (1,1),(1,-1))
        if Hq: qual+=1
        S=random.sample(W,random.randint(1,len(W)))
        a,c=random.randint(-5,5),random.randint(1,5)
        cont=[(p+(u,),g*h) for p,g in S for u,h in succ(p[-1],hs)]
        ok+= mu(cont,a,c)==2*mu(S,a,c)
    w('%s tested %d qualifying(A*A=2) %d consistent %d'%(name,tested,qual,ok))
out.close()
