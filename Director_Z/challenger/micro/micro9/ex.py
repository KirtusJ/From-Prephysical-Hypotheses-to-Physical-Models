import numpy as np
# vertices 0,1,2 ; arcs y->z gain in {+1,-1}; A[z,y]
arcs={(0,1):1,(0,2):1,(1,1):1,(1,2):-1,(2,0):1,(2,2):1}
A=np.zeros((3,3),int)
for (y,z),g in arcs.items(): A[z,y]=g
print("A^T A=\n",A.T@A)
B=A[np.ix_([1,2],[0,1])]; print("B^T B=\n",B.T@B)
# walk counts by gain: P[z,y] plus-count, M minus-count
P=(A==1).astype(object); Mi=(A==-1).astype(object)
for s in range(3):
    p=np.zeros(3,object); m=np.zeros(3,object); p[s]=1
    for n in range(1,13):
        p,m=P@p+Mi@m, P@m+Mi@p
        if n in(4,8,12): print("start",s,"len",n,"min count over (vertex,gain)",min(list(p)+list(m)))
