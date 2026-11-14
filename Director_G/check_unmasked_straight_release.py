"""Native source/release checks. Run with NumPy: python -B check_unmasked_straight_release.py NEW_DIR."""
import argparse
import json
import math
from collections import Counter
from pathlib import Path
import numpy as np


def require(test,message):
    if not test:
        raise ValueError(message)


def source_shape(k,h,m):
    q=2*k+math.pi/2+h
    out=np.ones(k.size)
    for j in range(1,m+1):
        out*=np.sin(q+(2*j-1)*4*h)
    return out


def direct_source(n,s,m,home):
    size=4*n
    sites=np.arange(size)
    z=np.exp(-2j*math.pi*s*(sites//2)/n)
    r=np.zeros(size,dtype=complex)
    l=r.copy()
    r[2*home]=1
    for step in range(2*m):
        old=(2*(home+step))%4
        for half in range(2):
            r,l=np.roll(z*(r+l),1)/math.sqrt(2),np.roll(z*(r-l),-1)/math.sqrt(2)
            if half==0 and step%2==1:
                dx=-1 if (step//2)%2==0 else 1
                keep=(sites%4==(old+dx)%4)
                r*=keep
                l*=keep
        keep=(sites%4==(old+2)%4)
        r*=keep
        l*=keep
    h=math.pi*s/n
    k=2*math.pi*sites/size
    raw=source_shape(k,h,m)*np.exp(-1j*k*2*home)*2.**(-m) /math.sqrt(size)
    actual=np.fft.fft(r,norm="ortho")
    norm=np.linalg.norm(raw)
    require(norm>0 and np.linalg.norm(l)<1e-12,"unexpected source rail")
    phase=np.vdot(raw,actual)
    error=float(np.linalg.norm(actual-raw*(phase/abs(phase)))/norm)
    require(error<5.e-12,"endpoint gauge or source normalization error")
    return dict(N=n,s=s,m=m,home=home,norm_error=error)


def flight(n,s,lam=.25,T=1.):
    delta=(math.pi/n)**(1/3)
    h=math.pi*s/n
    m=max(2,2*round(lam/(2*delta**2)))
    ticks=round(T/delta**2)
    size=4*n
    k=2*math.pi*np.fft.fftfreq(size)
    source=source_shape(k,h,m)
    zero=source_shape(k,0,m)
    ratio=float(np.sum(source**2)/np.sum(zero**2))
    source/=np.linalg.norm(source)
    peak_offset=(2*m+.5)*h
    slow=np.abs(np.sin(k+peak_offset))>1/math.sqrt(2)
    # At an exact tile boundary sharing the single grid point would be a
    # convention. Its weight here is exponentially small in the scaling.
    r=np.stack((source,source*slow,source*(~slow))).astype(complex)
    l=np.zeros_like(r)
    er=np.exp(-1j*k)/math.sqrt(2)
    for _ in range(ticks):
        a,b=np.roll(r,-2*s,axis=1),np.roll(l,-2*s,axis=1)
        r,l=er*(a+b),er.conjugate()*(a-b)
    density=abs(np.fft.ifft(r,axis=1,norm="ortho"))**2+abs(np.fft.ifft(l,axis=1,norm="ortho"))**2
    y=np.fft.fftfreq(size)*size*delta
    window=abs(y)<=delta**(-.5)
    weights=density.sum(axis=1)
    masses=density[:,window].sum(axis=1)
    actual_lam=m*delta**2
    actual_t=ticks*delta**2
    mean=2*actual_lam*actual_t+actual_t**2/2
    variance=2*actual_lam+actual_t**2/(8*actual_lam)
    estimated=np.sum(density[1]*np.exp(1j*y))/weights[1]
    predicted=math.exp(-variance/2)*math.cos(mean)
    require(abs(weights[0]-1)<2e-11 and abs(weights[1]+weights[2]-1)<2e-11,"norm drift")
    return dict(N=n,charge=s,lambda_eff=actual_lam,time=actual_t,m=m,unmasked_ticks=ticks,
                source_ratio=ratio,predicted_source_ratio=math.exp(-16*actual_lam**3/3),
                slow_mass=float(weights[1]),fast_mass=float(weights[2]),
                window=float(masses[0]),slow_in_window=float(masses[1]),fast_in_window=float(masses[2]),
                fast_right=float(np.sum(density[2,y>0])),fast_left=float(np.sum(density[2,y<0])),
                slow_characteristic_real=float(estimated.real),slow_characteristic_imag=float(estimated.imag),
                predicted_slow_characteristic=predicted)


def alias_control():
    n=16
    live=Counter({(0,"R",0,1):1})
    sources=[]
    for t in range(1,12):
        nxt=Counter()
        for (x,r,g,s),v in live.items():
            for c,step in (("R",1),("L",-1)):
                y=(x+step)%(4*n)
                if t<=8:
                    j=(t-1)//2
                    old=2*j%4
                    if t%2==0 and y%4!=(old+2)%4:
                        continue
                    if t%2 and j%2 and y%4!=(old+(-1 if j==1 else 1))%4:
                        continue
                nxt[y,c,(g+x//2)%n,-s if r==c=="L" else s]+=v
        live=nxt
        if t==8:
            sources=list(live.items())
    chars=[]
    for s in (1,5):
        bins={}
        for (x,r,g,e),v in sources:
            bins[x,r]=bins.get((x,r),0)+v*e*np.exp(-2j*math.pi*s*g/n)
        p=sum(abs(z)**2 for z in bins.values())/2**8
        require(abs(p-1/128)<1e-13,"different logical source yields")
        chars.append((1+math.cos(2*math.pi*s/n))/8)
    sig=Counter()
    for (x,c,g,s),v in live.items():
        if (x,c)==(5,"R"):
            sig[g]+=s*v
    require(sig=={8:-1,9:-1},"alias read at chosen unmasked port")
    return dict(N=n,ticks_encoded=8,ticks_unmasked=3,port=[5,"R"],signed_residues=dict(sig),
                physical_s=[1,5],source_yields=["1/128","1/128"],conditional_port=chars)


def run():
    oracle=[direct_source(n,s,m,home) for n in (12,16,20,28) for s in (1,-1,1+n//4)
            for m in (2,4) for home in (0,2*n-1)]
    runs=[flight(n,s) for n in (256,1024,4096,16384) for s in (-1,1)]
    return dict(physical_source_oracles=oracle,unmasked_flights=runs,alias_control=alias_control(),
                scope="All probabilities in flight rows are conditional on successful encoded source.")


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory",type=Path)
    directory=parser.parse_args().directory
    out=directory/"unmasked_straight_release.json"
    if out.exists():
        parser.exit(2,f"Refusing to overwrite {out}\n")
    result=run()
    directory.mkdir(parents=True,exist_ok=True)
    with out.open("x",encoding="utf8",newline="\n") as stream:
        json.dump(result,stream,separators=(",",":"),allow_nan=False)
        stream.write("\n")
