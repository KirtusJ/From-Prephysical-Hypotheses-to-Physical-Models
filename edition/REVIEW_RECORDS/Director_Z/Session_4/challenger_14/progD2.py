"""Follow-up to failed predicate D2 at B=1 (kept in resultAD.txt).
PREDICATES
 D3: line window W=4,5, B=3: restricted dimension to (|x|<=1, box [0..3]^2) == 5.
 D4: at B=1 the sixth solution is a truncation artefact: with unknowns to 2B=2 and U,V in [0..1]^2, the restricted
     dimension to (|x|<=1, box [0..1]^2) stays 6, but restricted to the same inner set while equations use U,V in [0..2]^2
     (i.e. the B=2 system) it is 5.  [measured: dimension of B=2 solutions restricted to box 1]
Result file resultD2.txt, mode 'x'.
"""
import importlib.util,sys,io,os
src=open('progAD.py').read().split("out=open('resultAD.txt','x')")[0]
exec(src)
out=open('resultD2.txt','x')
def W_(s):
    print(s); out.write(s+'\n'); out.flush()
for Wd in (4,5):
    sites=list(range(-Wd,Wd+1)); eqs=list(range(-Wd+1,Wd))
    A,idx=build(sites,eqs,3,lambda x:(x+1,x-1))
    res=restricted(A,idx,lambda k: abs(k[0])<=1 and k[2][0]<=3 and k[2][1]<=3)
    W_(f'D3 W={Wd} B=3 unknowns {A.shape[1]} eqs {A.shape[0]} {res} {"MET" if all(r[1]==5 for r in res) else "FAILED"}')
for Wd in (4,5):
    sites=list(range(-Wd,Wd+1)); eqs=list(range(-Wd+1,Wd))
    A,idx=build(sites,eqs,2,lambda x:(x+1,x-1))
    res=restricted(A,idx,lambda k: abs(k[0])<=1 and k[2][0]<=1 and k[2][1]<=1)
    W_(f'D4 W={Wd}: B=2 system restricted to box 1: {res} {"MET" if all(r[1]==5 for r in res) else "FAILED"}')
out.close()
