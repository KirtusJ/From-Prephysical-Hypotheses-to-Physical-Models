"""P8b follow-up: P8 failed from my own bug (axis used tr(M^dag P M)=tr P). Predicate unchanged:
axes of observable (G^n)^dag Z G^n, n=0,1,2 = (0,0,1),(-1,0,0),(0,sqrt3/2,1/2); also note's control masses (7/32,1/32)."""
import numpy as np,json
w=np.exp(-2j*np.pi/3);H=np.array([[1,1],[1,-1]])/np.sqrt(2);X=np.array([[0,1],[1,0]]);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1])
G=X@np.diag([w,1/w])@H
ax=[[round(float(np.real(np.trace(np.linalg.matrix_power(G,n).conj().T@Z@np.linalg.matrix_power(G,n)@P))/2),12) for P in (X,Y,Z)] for n in range(3)]
v=G@np.array([1,0]); out=(G@G@v)*0.5  # two successful G, each prob 1/2 (k=1: 2^{-1})
m=[abs(out[0])**2,abs(out[1])**2]
r=dict(axes=ax,ok=bool(np.allclose(ax,[[0,0,1],[-1,0,0],[0,np.sqrt(3)/2,.5]])),success_masses_RL=m)
open('p8b_results.json','x').write(json.dumps(r));print(r)
