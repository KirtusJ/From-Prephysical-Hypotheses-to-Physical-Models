"""Allowed-but-unreachable profiles. Predicates fixed before first run:
 A(w): cor:tp (ii) and (iii) hold, tested numerically with mpmath polyroots at 60 digits; the smallest |Re| of a
   root of W and the smallest |Im| of u,v roots are reported, so the separation is measured, not assumed.
 Candidates: all w with w[0]+w[1]>0... precisely: length L<=6, entries >=0, first nonzero at index 0 or 1, last entry
   nonzero, total <= K.  Hypothesis per case: candidate counted as allowed iff A(w).
 Output: allowed count, reachable count (from a res2 file, given M), list of allowed and not reachable, and
   reachable-not-allowed (must be empty: thm:tp).
Usage: python3 allowed.py RESFILE M K OUT"""
import sys, ast, itertools, mpmath
mpmath.mp.dps=60
res,M,K,out=sys.argv[1],int(sys.argv[2]),int(sys.argv[3]),open(sys.argv[4],'x')
reach=None
for l in open(res):
    if l.startswith('PROFILES %d '%M): reach=set(ast.literal_eval(l.split(' ',2)[2]))
def roots(c):  # c ascending
    while c and c[-1]==0: c=c[:-1]
    z=0
    while c and c[0]==0: c=c[1:]; z+=1
    if len(c)<=1: return [0]*z
    return [mpmath.mpf(0)]*z+list(mpmath.polyroots(c[::-1],maxsteps=4000,extraprec=400))
minre=mpmath.inf; minim=mpmath.inf
def A(w):
    global minre,minim
    v=list(w[0::2]); u=list(w[1::2])
    Wc=[0]*(len(w)); 
    for i,x in enumerate(w): Wc[i]=x
    rW=roots(Wc)
    ok=True
    for r in rW:
        if abs(mpmath.re(r))>mpmath.mpf(10)**-40: minre=min(minre,abs(mpmath.re(r)))
        if mpmath.re(r)>mpmath.mpf(10)**-40: ok=False
    for p in (u,v):
        for r in roots(p):
            if abs(mpmath.im(r))>mpmath.mpf(10)**-40: minim=min(minim,abs(mpmath.im(r))); ok=False
            elif mpmath.re(r)>mpmath.mpf(10)**-40: ok=False
    return ok
cands=[]
for L in range(1,7):
    for w in itertools.product(range(K+1),repeat=L):
        if sum(w)>K or w[-1]==0 or (w[0]==0 and (L==1 or w[1]==0)): continue
        cands.append(w)
allowed=[w for w in cands if A(w)]
al=set(allowed); rk={w for w in reach if sum(w)<=K and len(w)<=6}
print(f'K={K} M={M} candidates={len(cands)} allowed={len(al)} reachable(len<=6)={len(rk)} min|Re| nonzero={mpmath.nstr(minre,5)} min|Im| nonzero={mpmath.nstr(minim,5)}',file=out)
print('reachable not allowed:',sorted(rk-al),file=out)
bad=sorted(al-rk,key=lambda w:(sum(w),w))
print('allowed not reachable',len(bad),file=out)
for w in bad: print(sum(w),w,file=out)
