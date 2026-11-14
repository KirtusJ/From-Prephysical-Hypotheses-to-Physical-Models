"""Exact small-ring audit of phase averaging and position reporting after flight."""
import argparse
from fractions import Fraction as Q
import json
import math
from pathlib import Path


def require(condition, why):
    if not condition:
        raise ArithmeticError(why)


def read_bin(site, rail):
    # A two-mode Hadamard in the detector itself. Several ports share a reported well.
    return (3 * site + rail) % 16 if (site + 2*rail) % 5 else None


def output_fields(psi, skip):
    """Fourier-independent detector: mix disjoint pairs at distance skip, then bin."""
    out = {}
    for base in range(0,16,2*skip):
        for offset in range(skip):
            i, j = base + offset, base + offset + skip
            for rail in (0,1):
                a,b = psi.get((i,rail),0), psi.get((j,rail),0)
                # All amplitudes here are Gaussian integers of small magnitude.
                out[i,rail] = a+b
                out[j,rail] = a-b
    return out


def report(psi, shift, skip):
    out = [0]*17
    for (site, rail), amp in output_fields(psi,skip).items():
        b = read_bin(site,rail)
        dest = 16 if b is None else (b-shift)%16
        ar, ai = int(amp.real), int(amp.imag)
        require(amp == complex(ar,ai), "exact integer arithmetic")
        out[dest] += ar*ar + ai*ai
    denom=sum(out)
    return [Q(x,denom) for x in out]


def direct(psi, charge, skip, shifts=range(16), scramble=True):
    final = [Q(0)]*17
    repeats=0
    for a in shifts:
        for j in (range(4) if scramble else (0,)):
            for exchange in (0,1):
                for sign in (0,1):
                    state={}
                    for (x,c),v in psi.items():
                        s=(x+a)%16
                        ipow=(charge*j*(s//2))%4
                        state[s,c^exchange]=v*((1j)**ipow)*((-1)**(sign*c))
                    final=[p+q for p,q in zip(final,report(state,a,skip))]
                    repeats+=1
    return [p/repeats for p in final]


def predicted(psi, kernel):
    mass=[0]*16
    for (x,_),v in psi.items():
        mass[x]+=int(v.real)**2+int(v.imag)**2
    n=sum(mass)
    return [sum(Q(mass[x],n)*kernel[(d-x)%16] for x in range(16))
            for d in range(16)]+[kernel[16]]


def panel(label, psi, charge, skip, expected):
    kernel=direct({(0,0):1},charge,skip)
    seen=direct(psi,charge,skip)
    inferred=predicted(psi,kernel)
    tv=sum(abs(p-q) for p,q in zip(seen,inferred))/2
    require((tv==0)==expected, label)
    return dict(label=label,charge=charge,detector_pair_distance=skip,kernel=kernel,
                seen=seen,convolved=inferred,total_variation=tv)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output",type=Path)
    args=parser.parse_args()
    two={(0,0):1+1j,(2,0):2,(2,1):1j,(4,0):1,(4,1):2j}
    edge={(0,0):1,(8,0):1}
    rows=[panel("unit",two,1,2,True), panel("conjugate",two,3,2,True),
          panel("zero winding",two,0,2,False),
          panel("diameter reaches the antipode",edge,1,8,False),
          panel("nonprimitive aliases", {(0,1):1,(4,1):1},2,4,False)]
    # A single-live-site detector has spatial mean efficiency 1/N. With N increasing,
    # it is an exact sparse position read, and independent extra clicks can still dominate.
    rare=[]
    for n in (16,64,256,1024):
        detector_yield=Q(1,n)
        bad=Q(1,n)
        retained=bad/(bad+(1-bad)*detector_yield)
        require(retained>Q(1,2),"vanishing efficiency")
        rare.append(dict(sites=n,good_yield=detector_yield,bad_prior=bad,bad_posterior=retained))
    # Momentum-band shift on one parity. Use finite DFT solely for this numerical panel.
    # Momentum eigenvalues are phases; no amplitude clipping or histogram threshold.
    import cmath
    band_rows=[]
    for n,b in ((16,2),(32,3),(64,4),(128,5)):
        d=n//4
        band=tuple(range(-b,b+1))
        phase=lambda j:cmath.exp(-2j*math.pi*j*d/n)
        sharp_return=abs((n-len(band)+sum(phase(j) for j in band))/n)**2
        old=lambda x:sum(cmath.exp(2j*math.pi*j*x/n) for j in band)/math.sqrt(len(band)*n)
        new=lambda x:sum(phase(j)*cmath.exp(2j*math.pi*j*x/n) for j in band)/math.sqrt(len(band)*n)
        shift_error=max(abs(new(x)-old(x-d)) for x in range(n))
        require(shift_error<1e-12 and 1-sharp_return<=4*len(band)/n,"band shift")
        band_rows.append(dict(sites=n,band_modes=len(band),shift=d,
                              sharp_offsite=1-sharp_return,max_amplitude_shift_error=shift_error))
    result=dict(direct_panels=rows,rare_click_counterexamples=rare,frequency_window_controls=band_rows)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    with args.output.open("x",encoding="utf8",newline="\n") as f:
        json.dump(result,f,indent=2,default=str)
        f.write("\n")


if __name__=="__main__":
    main()
