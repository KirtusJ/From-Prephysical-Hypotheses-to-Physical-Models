"""Exploration (abstract packet model, not walks). Reverse search:
state = cyclic sequence of packets; packet = multiset of (level, exp mod r).
Reverse moves: un-copy adjacent packets equal up to delta-shift; split a packet in two adjacent.
Question: is target reducible to a single walk with at most K packets at any time?"""
import sys, itertools
from functools import lru_cache
sys.setrecursionlimit(100000)
def norm_packet(p, r):
    best=None
    for e in range(r):
        q=tuple(sorted((l,(x+e)%r) for l,x in p))
        if best is None or q<best: best=q
    return best
def canon(state, r):
    k=len(state); best=None
    for i in range(k):
        rot=list(state[i:])+[tuple((l-1,x) for l,x in p) for p in state[:i]]
        m=min(l for p in rot for l,x in p)
        rot=tuple(norm_packet(tuple((l-m,x) for l,x in p),r) for p in rot)
        if best is None or rot<best: best=rot
    return best
def splits(p):
    n=len(p); seen=set()
    for mask in range(1,2**n-1):
        a=tuple(p[i] for i in range(n) if mask>>i&1); b=tuple(p[i] for i in range(n) if not mask>>i&1)
        if (a,b) not in seen:
            seen.add((a,b)); yield a,b
def solve(target, r, K):
    memo={}
    def rec(s):
        if s in memo: return memo[s]
        memo[s]=False  # cycle guard
        if sum(len(p) for p in s)==1:
            memo[s]=True; return True
        k=len(s)
        # un-copy
        ext=list(s)+[tuple((l-1,x) for l,x in s[0])]
        for i in range(k):
            if k==1: break
            if norm_packet(ext[i],r)==norm_packet(ext[i+1],r) :
                t=canon(tuple(s[j] for j in range(k) if j!=i), r)
                if rec(t): memo[s]=('uncopy',i,t); return True
        if k<K:
            for i in range(k):
                if len(s[i])<2: continue
                for a,b in splits(s[i]):
                    t=canon(s[:i]+(a,b)+s[i+1:], r)
                    if rec(t): memo[s]=('split',i,t); return True
        return False
    c=canon(target,r); ok=rec(c)
    path=[]
    if ok:
        s=c
        while memo[s] is not True:
            path.append((s,memo[s][:2])); s=memo[s][2]
        path.append((s,'base'))
    return ok,path,len(memo)
if __name__=="__main__":
    def P(*terms):  # (level,exp,count)
        return tuple(sorted((l,x) for l,x,c in terms for _ in range(c)))
    r=int(sys.argv[1]); K=int(sys.argv[2])
    tests={
     'test_r1': (P((0,0,1),(1,0,3),(2,0,1)), P((0,0,2),(1,0,5))),
     '131_alone': (P((0,0,1),(1,0,3),(2,0,1)),),
     '1221':(P((0,0,1),(1,0,2)),P((0,0,2),(1,0,1))),
     '3,2,5,3':(P((0,0,3),(1,0,2)),P((0,0,5),(1,0,3))),
    }
    if r==2:
        tests['test_r2']=(P((0,0,1),(1,0,3),(2,0,1)), P((0,0,1),(0,1,1),(1,0,3),(1,1,2)))
        tests['test_r2b']=(P((0,0,1),(1,0,3),(2,0,1)), P((0,0,1),(0,1,1),(1,0,2),(1,1,3)))
    for name,t in tests.items():
        ok,path,n=solve(t,r,K)
        print(name,ok,n)
        for s,m in path: print('   ',m,s)
