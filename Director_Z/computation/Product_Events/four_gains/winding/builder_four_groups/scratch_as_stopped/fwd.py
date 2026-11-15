"""Exploration: forward BFS in abstract packet model, counts only (r=1), WITH deletion.
state: tuple of packets, packet = tuple of counts by level (dict level->count as sorted tuple).
Report: 2-packet states (P,Q) with levels P in {0,1,2}, Q in {0,1}; is test (1,3,1 | 2,5) reached;
compare with/without deletion."""
import sys
from collections import deque
K=int(sys.argv[1]); T=int(sys.argv[2]); DEL=int(sys.argv[3])
def shift(p,d): return tuple((l+d,c) for l,c in p)
def add(p,q):
    d=dict(p)
    for l,c in q: d[l]=d.get(l,0)+c
    return tuple(sorted(d.items()))
def canon(s):
    best=None;k=len(s)
    for i in range(k):
        rot=list(s[i:])+[shift(p,-1) for p in s[:i]]
        m=min(l for p in rot for l,c in p)
        rot=tuple(shift(p,-m) for p in rot)
        if best is None or rot<best: best=rot
    return best
def tot(s): return sum(c for p in s for l,c in p)
start=canon((((0,1),),))
seen={start};dq=deque([start])
while dq:
    s=dq.popleft();k=len(s);nxt=[]
    if k<K:
        for i in range(k):
            if tot(s)+sum(c for l,c in s[i])<=T: nxt.append(s[:i+1]+(s[i],)+s[i+1:])
    if k>=2:
        for i in range(k-1): nxt.append(s[:i]+(add(s[i],s[i+1]),)+s[i+2:])
        nxt.append((add(s[0],shift(s[-1],1)),)+s[1:-1])
        if DEL:
            for i in range(k): nxt.append(s[:i]+s[i+1:])
    for t in nxt:
        c=canon(t)
        if c not in seen: seen.add(c);dq.append(c)
print('states',len(seen))
two=[s for s in seen if len(s)==2]
print('2-packet states',len(two))
target=canon((((0,1),(1,3),(2,1)),((0,2),(1,5))))
print('test reached:',target in seen)
import pickle
pickle.dump(seen,open(f'seen_K{K}_T{T}_D{DEL}.pkl','wb'))
