"""Measured-only (binary64) look at the asymptotic claims; no thresholds, no pass/fail.
M1 fronts eq (2): D even, D=1 mod 3, t=even nearest sqrt2*D: report p(D,R)/h^2, p(D,L)/h^2 for Re u=1 and -1/2
   (note: (4,0) and (5/2,3/2) in the limit) and (R+L)/4.
M2 interior: n=N=2D, D=4 mod 12: U_E, K_E, K_E+, gap 3K_E+, determinant; note claims liminf K_E+>0, K_E->0.
"""
import numpy as np, sys, json
import mpmath
airy=lambda x:(float(mpmath.airyai(x)),)
def line(n):
    R=np.zeros(n+2); L=np.zeros(n+2); R[0]=1.0; s=2**-0.5
    for _ in range(n):
        nR=(R+L)*s; nL=np.zeros_like(R); nL[1:]=((R-L)*s)[:-1]; R,L=nR,nL
    return R,L   # index = number of left steps; displacement y=n-2l
out={"M1":[], "M2":[]}
for D in [4,10,16,40,100,250,1000,4000,10000]:
    t=2*round(D*2**0.5/2); R,L=line(t)
    l1=(t-D)//2; l2=l1+D
    v=2**-0.5; eta=(D-v*t)*t**(-1/3); al=(4*2**0.5)**(1/3); h=al*t**(-1/3)*airy(al*eta)[0]
    row={"D":D,"t":t}
    for name,m in (("triv",1.0),("unit",-0.5)):
        pR=R[l1]**2+R[l2]**2+2*m*R[l1]*R[l2]; pL=L[l1]**2+L[l2]**2+2*m*L[l1]*L[l2]
        row[name]=[round(pR/h**2,4),round(pL/h**2,4),round((pR+pL)/(4*h*h),4)]
    out["M1"].append(row); print(row)
for D in [40,76,160,316,736,1204,2404,4804,9604,19204]:
    assert D%12==4
    n=2*D; R,_=line(n)
    xs=[x for x in range(-(-21*n//50), 11*n//25+1) if (x-n)%2==0]
    a=np.array([R[(n-x)//2] for x in xs]); b=np.array([R[(n-x)//2+D] for x in xs])
    U=float((a*a+b*b).sum()); K=float((a*b).sum()); pos=a*b>0
    Up=float((a*a+b*b)[pos].sum()); Kp=float((a*b)[pos].sum())
    row={"n":n,"wells":len(xs),"U_E":U,"K_E":K,"K_E+":Kp,"gap=3K_E+":3*Kp,"triv_E+":Up+2*Kp,"nontriv_E+":Up-Kp,"det(no C)":2*(U*Kp-Up*K),"sum|ab|":float(abs(a*b).sum())}
    out["M2"].append(row); print({k:(round(v,6) if isinstance(v,float) else v) for k,v in row.items()})
json.dump(out,open(sys.argv[1]+"/xr66_asym.json","x"),indent=1)
