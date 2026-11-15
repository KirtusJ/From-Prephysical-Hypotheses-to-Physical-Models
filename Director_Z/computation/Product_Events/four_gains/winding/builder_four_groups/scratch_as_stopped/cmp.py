"""Exploration: compare model-reachable 2-packet count states (total<=9) with Hurwitz-TN sequences (minors up to order 4)."""
import pickle, itertools, sys
from fractions import Fraction
seen=pickle.load(open('seen_K6_T13_D1.pkl','rb'))
def wseq(s):
    A=dict(s[0]);B=dict(s[1]);L=max(list(A)+list(B))
    w=[]
    for l in range(L+1): w+= [A.get(l,0),B.get(l,0)]
    while w and w[-1]==0: w.pop()
    while w and w[0]==0: w.pop(0)
    return tuple(w)
model=set()
for s in seen:
    if len(s)==2:
        w=wseq(s)
        if sum(w)<=9: model.add(w)
def det(m):
    n=len(m); m=[[Fraction(x) for x in r] for r in m]; d=Fraction(1)
    for i in range(n):
        p=next((j for j in range(i,n) if m[j][i]!=0),None)
        if p is None: return 0
        if p!=i: m[i],m[p]=m[p],m[i]; d=-d
        d*=m[i][i]
        for j in range(i+1,n):
            f=m[j][i]/m[i][i]
            for k in range(i,n): m[j][k]-=f*m[i][k]
    return d
def tn(w):
    n=len(w); g=lambda j: w[j] if 0<=j<n else 0
    rows=range(-1,(n+1)//2+2); cols=range(-2,n+3)
    for k in (2,3,4):
        for I in itertools.combinations(rows,k):
            for C in itertools.combinations(cols,k):
                if det([[g(c-2*i) for c in C] for i in I])<0: return False
    return True
def comps(total,maxlen):
    for n in range(1,maxlen+1):
        def rec(pos,rem,cur):
            if pos==n:
                if cur[0]>0 and cur[-1]>0: yield tuple(cur)
                return
            for c in range(0,rem+1):
                yield from rec(pos+1,rem-c,cur+[c])
        for t in range(1,total+1):
            for w in rec(0,t,[]):
                if sum(w)==t: yield w
allowed=set(w for w in comps(9,6) if tn(w))
al=set(w for w in allowed)
print('TN-allowed (len<=6,total<=9):',len(al),' model:',len([w for w in model if len(w)<=6]))
print('model not allowed:',sorted(w for w in model if len(w)<=6 and w not in al)[:10])
miss=sorted(w for w in al if w not in model)
print('allowed not in model:',len(miss),miss[:40])
miss2=[w for w in miss if any(w[i] for i in range(0,len(w),2)) and any(w[i] for i in range(1,len(w),2))]
print('genuine misses:',len(miss2),miss2)
