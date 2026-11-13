import numpy as np, itertools
# d=2,q=2. vertices 0..3. block{0,1}->succ(0,2); block{2,3}->succ(1,2). rho=kappa=1.
A=np.zeros((4,4))
A[0,0]=1;A[2,0]=1;A[0,1]=1;A[2,1]=-1
A[1,2]=1;A[2,2]=1;A[1,3]=1;A[2,3]=-1
print("A*A=\n",A.T@A)
# hypothesis: counts of walks from 0 by (vertex,sign)
cnt=np.zeros((4,2),dtype=object);cnt[0,0]=1
for L in range(14):
    new=np.zeros((4,2),dtype=object)
    for x in range(4):
        for y in range(4):
            if A[y,x]!=0: new[y]+= cnt[x] if A[y,x]>0 else cnt[x][::-1]
    cnt=new
print("counts length 14 (vertex x sign):\n",cnt)
# event: both length-1 walks from 0
v=np.array([1,0,1,0.]);w=A@v
print("v",v,"Av",w,"|v|^2",v@v,"|Av|^2",w@w,"(needs 2*|v|^2)")
# general: solve consistency for phi on integers using all events of length<=7 subsets size<=3
walks=[(0,1)]
for _ in range(6): walks=[(y,g*int(A[y,x])) for (x,g) in walks for y in range(4) if A[y,x]!=0]
import random; rng=random.Random(1); rows=[]
for _ in range(20000):
    S=rng.sample(range(len(walks)),rng.choice([1,2,3,4,5,6]))
    v=np.zeros(4)
    for i in S: v[walks[i][0]]+=walks[i][1]
    w=A@v; r=np.zeros(40)
    for t in w: r[int(abs(t))]+=1
    for t in v: r[int(abs(t))]-=2
    rows.append(r)
M=np.array(rows)[:,1:]; M=M[:,(M!=0).any(0)]
s=np.linalg.svd(M,compute_uv=False); print("unknowns",M.shape[1],"nullity",int((s<1e-9*s[0]).sum()))
