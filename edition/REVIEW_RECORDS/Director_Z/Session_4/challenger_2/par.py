# Solve (Mk) on Z as linear system: unknown f(n), |n|<=M, all instances with every argument in range; f even imposed? no: see what nullspace is
import numpy as np, itertools
for k in range(1,7):
    M=4*k+8
    idx=lambda n:n+M
    rows=[]
    for a in range(-M,M+1):
        for b in range(-M,M+1):
            if abs(a-b)<=M and abs(a+k*b)<=M:
                v=np.zeros(2*M+1); v[idx(a-b)]+=k; v[idx(a+k*b)]+=1; v[idx(a)]-=(k+1); v[idx(b)]-=k*(k+1); rows.append(v)
    A=np.array(rows); s=np.linalg.svd(A,compute_uv=False)
    print(k,M,'nullity',int((s<1e-8*s[0]).sum()))
