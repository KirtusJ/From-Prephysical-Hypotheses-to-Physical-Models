"""Diagnostic 2 (prints only). inv=14, eps=delta^0.9.
(a) smooth Gaussian scalar packet, mean p0=1, sigma_p=0.3, on even sites: forced-minus-free mean Y.
(b) accepted sharp-launch state p0=1: trajectory of mean Y and decoded mean p for F=-1,0,+1 at quarter times."""
import numpy as np
def tick(R,L): return np.roll(R+L,1)/np.sqrt(2), np.roll(R-L,-1)/np.sqrt(2)
inv=14; d=1/inv; eps=d**.9; a=eps*d; tau=eps*d*d; J=round(d**-2.8); M=round(.8/(4*tau)); T=4*M*tau; w=d**1.1
N=1<<15; i=np.arange(N); x=np.where(i<N//2,i,i-N); Y=a*x
def meanp(r,l,par):
    z=(1j**(x%4))*(r+1j*l); zs=z[i%2==par]; c=np.fft.fft(zs); m=np.fft.fftfreq(len(zs),1/len(zs)); p=2*np.pi*m/N/d; P2=abs(c)**2; return float(P2@p/P2.sum())
def run(R0,L0,par,label):
    for F in (0,1,-1):
        ang=-4*F*eps*d**3*x; cs,sn=np.cos(ang),np.sin(ang); r,l=R0.copy(),L0.copy(); out=[]
        for b in range(M):
            r,l=cs*r-sn*l,sn*r+cs*l
            for _ in range(4): r,l=tick(r,l)
            if (b+1)%(M//4)==0: wt=r*r+l*l; out.append((round(float(Y@wt),3),round(meanp(r,l,par),3)))
        print(label,f"F={F:+d}",out)
# (a) Gaussian
for p0,sig in ((1,0.3),(1,0.77),(-1,0.3)):
    Ys=a*x; env=np.exp(-(Ys*sig/eps)**2/1.0)  # sigma_Y = eps/(sqrt2 sig)
    z=np.where(i%2==0, env*np.exp(1j*d*p0*x),0); z/=np.linalg.norm(z)
    rails=np.conj(1j**(x%4))*z
    run(rails.real.copy(),rails.imag.copy(),0,f"gauss p0={p0} sig={sig}")
R=np.zeros(N);L=np.zeros(N);R[0]=1
for _ in range(J): R,L=tick(R,L)
take=np.abs(x/J-d*1)<=w; yes=(R*R+L*L)[take].sum()
run(np.where(take,R,0)/np.sqrt(yes),np.where(take,L,0)/np.sqrt(yes),J%2,"accepted p0=1")
print("ideal: T/4 steps; free dY per quarter",T/4,"forced shift at T",T*T/2)
