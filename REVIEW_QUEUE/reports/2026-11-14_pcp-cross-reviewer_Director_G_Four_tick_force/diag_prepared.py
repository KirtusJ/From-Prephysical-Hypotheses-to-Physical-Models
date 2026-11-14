"""Diagnostic follow-up to G1 (observables only, prints; no result file).
Why do F=+1 and F=-1 both move the conditional MEAN toward the launch side at p0=+-1?
Prints the decoded scalar momentum distribution of the accepted state and the mean/median
position for each force. Median and quartiles are robust to the sharp-window momentum tails."""
import numpy as np, sys
def tick(R,L): return np.roll(R+L,1)/np.sqrt(2), np.roll(R-L,-1)/np.sqrt(2)
def quant(Y,w,qs):
    o=np.argsort(Y); c=np.cumsum(w[o]); return [float(Y[o][np.searchsorted(c,q)]) for q in qs]
for inv,p0 in ((14,1),(14,-1),(14,0),(20,1)):
    d=1/inv; eps=d**.9; a=eps*d; tau=eps*d*d; J=round(d**-2.8); M=round(.8/(4*tau)); T=4*M*tau; w=d**1.1
    N=1<<(2*(J+4*M)+4).bit_length(); i=np.arange(N); x=np.where(i<N//2,i,i-N)
    R=np.zeros(N);L=np.zeros(N);R[0]=1
    for _ in range(J): R,L=tick(R,L)
    take=np.abs(x/J-d*p0)<=w; yes=(R*R+L*L)[take].sum()
    R0=np.where(take,R,0)/np.sqrt(yes); L0=np.where(take,L,0)/np.sqrt(yes)
    par=J%2; sub=(i%2==par)
    z=(1j**(x%4))*(R0+1j*L0); zs=z[sub]; c=np.fft.fft(zs)/np.sqrt(len(zs)); m=np.fft.fftfreq(len(zs),1/len(zs)); q=2*np.pi*m/N
    # sublattice offset only multiplies c by a q-dependent phase; |c|^2 unaffected
    P2=abs(c)**2; p=q/d
    print(f"inv={inv} p0={p0} J={J} M={M} T={T:.4f} acc={yes:.4f} mean_p={float(P2@p):.3f} mass|p|<=2:{P2[abs(p)<=2].sum():.4f} |p|<=4:{P2[abs(p)<=4].sum():.4f} mass p<0:{P2[p<0].sum():.4f} mass|q|>1:{P2[abs(q)>1].sum():.4f}")
    Y=a*x; base=None
    for F in (0,1,-1):
        ang=-4*F*eps*d**3*x; cs,sn=np.cos(ang),np.sin(ang); r,l=R0.copy(),L0.copy()
        for _ in range(M):
            r,l=cs*r-sn*l,sn*r+cs*l
            for _ in range(4): r,l=tick(r,l)
        wt=r*r+l*l; q1,q2,q3=quant(Y,wt,(.25,.5,.75))
        if F==0: base=(float(Y@wt),q2)
        print(f"   F={F:+d} mean={float(Y@wt):.4f} (shift {float(Y@wt)-base[0]:+.4f})  median={q2:.4f} (shift {q2-base[1]:+.4f}) quartiles=({q1:.3f},{q3:.3f}) ideal shift={-F*T*T/2:+.4f}")
