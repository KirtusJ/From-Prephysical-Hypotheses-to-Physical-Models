"""Global one-bit count certificates and independent full-scale likelihood calculations."""
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
from math import comb,ceil,floor,log
import json
import numpy as np
from scipy.special import roots_legendre
from scipy.integrate import simpson
from scipy.fft import rfft,irfft,next_fast_len
from scipy.stats import binom

ROOT=Path(__file__).resolve().parent
D=2**42
WORK=2**64

def require(test,message):
    if not test:raise ArithmeticError(message)

@lru_cache(maxsize=None)
def exp_minus(x):
    """Rational lower/upper bounds on exp(-x), x>=0. Range reduction, alternating Taylor, outward squaring."""
    require(x>=0,'positive input to exp_minus');steps=0
    while x>F(1,2):x/=2;steps+=1
    term=F(1);s=term
    for j in range(1,23):term*=-x/j;s+=term
    low=floor((s-term*x/23)*WORK);high=ceil(s*WORK)
    for j in range(steps):low=low*low//WORK;high=(high*high+WORK-1)//WORK
    return F(low,WORK),F(high,WORK)

@lru_cache(maxsize=None)
def prob(t,w4,w8):
    a=exp_minus(8*t);b=exp_minus(16*t)
    values=[w4*(1+8*t)*a[j]+w8*(1+16*t)*b[j] for j in [0,1]]
    return max(0,floor(values[0]*D)),min(D,ceil(values[1]*D))

def masses(N,p):
    if p==D:return [0]*N+[D**N]
    if p==0:return [D**N]+[0]*N
    out=[];term=(D-p)**N
    for k in range(N+1):
        out.append(term)
        if k<N:term=term*(N-k)*p//((k+1)*(D-p))
    return out

def twice_risk_numerator(N,p,q):
    return sum(min(a,b) for a,b in zip(masses(N,p),masses(N,q)))

def certify_all_thresholds(n,high,low,test_point):
    # For p>=q, minimum binomial risk decreases with p and increases with q.
    M=n-1;scale=D**M;stack=[(F(0),F(2))];passed=0;depth=0;lowest=2*scale
    while stack:
        a,b=stack.pop();pmax=prob(a,*high)[1];qmin=prob(b,*low)[0]
        numerator=twice_risk_numerator(M,pmax,qmin)
        if 10*numerator>2*scale:
            passed+=1;lowest=min(lowest,numerator);continue
        mid=(a+b)/2;depth=max(depth,mid.denominator.bit_length())
        require(b-a>F(1,2**28),'failed to enclose all thresholds')
        stack.extend([(a,mid),(mid,b)])
    tail=twice_risk_numerator(M,prob(F(2),*high)[1],0);require(10*tail>2*scale,'unbounded tail interval')
    pmin=prob(test_point,*high)[0];qmax=prob(test_point,*low)[1];require(pmin>qmax,'witness orientation')
    witness=twice_risk_numerator(n,pmin,qmax);require(10*witness<2*D**n,'witness fails')
    return {'minimum_trials_all_nonnegative_single_upper_thresholds':n,'N_minus_1_partitions_verified':passed+1,'uniform_lower_bound_at_N_minus_1':min(tail,lowest)/(2*scale),'witness_threshold':str(test_point),'witness_upper_risk':witness/(2*D**n)}

def transform(n0,high,low,nodes_count,dt):
    z,w=roots_legendre(nodes_count);nodes=[];quad=[]
    for a,b in zip([0,1,3,8,20],[1,3,8,20,70]):nodes.extend((a+b)/2+(b-a)*z/2);quad.extend(w*(b-a)/2)
    u=np.array(nodes);weight=np.array(quad);P=u*(high[0]*np.exp(-u)+4*high[1]*np.exp(-2*u));Q=u*(low[0]*np.exp(-u)+4*low[1]*np.exp(-2*u));ll=np.log(P/Q);times=np.arange(0,35+dt/2,dt)
    f=(1-sum(high))+np.exp(1j*times[:,None]*ll)@(np.sqrt(P*Q)*weight)
    bd=float(f[0].real);errors={str(n):float(simpson((f**n).real/(times**2+.25),x=times)/(2*np.pi)) for n in [n0-1,n0]}
    return errors,bd

def histogram_bounds(N,high,low,step=1/65536):
    # Map P's exact one-step law into bins of log(P/Q). Round each likelihood down and up.
    # Convolution is binary64 FFT. Bounds have analytic rounding slack but no certified floating error budget.
    a,b=high;c,d=low;floor_index=floor(log((a+4*b)/(c+4*d))/step);last=ceil(log(a/c)/step)
    indexes=np.arange(floor_index,last+1);levels=np.exp(indexes*step)
    U=np.full(len(levels),np.inf);mid=(levels>(a+4*b)/(c+4*d))&(levels<a/c);U[levels<=(a+4*b)/(c+4*d)]=0
    U[mid]=-np.log((a-levels[mid]*c)/(4*(levels[mid]*d-b)))
    def survival(x):
        result=np.zeros_like(x);m=np.isfinite(x);y=x[m];result[m]=a*(1+y)*np.exp(-y)+b*(1+2*y)*np.exp(-2*y);return result
    sf=survival(U);hist=sf[:-1]-sf[1:];hist[-1]+=sf[-1];hist[-floor_index]+=1-a-b
    require(abs(hist.sum()-1)<1e-12 and hist.min()>-1e-12,'histogram normalization')
    size=N*(len(hist)-1)+1;length=next_fast_len(size,real=True);spectrum=rfft(hist,n=length);density=irfft(spectrum**N,n=length)[:size]
    position=(N*floor_index+np.arange(size))*step
    result=[float(.5*(density@np.exp(-np.maximum(position+shift,0)))) for shift in [N*step,0]]
    require(abs(density.sum()-1)<1e-10,'convolution normalization');return result

def secondary():
    def mg(theta,w):return sum(v*(F(a)/(a-theta))**2 for v,a in zip(w,[8,16]))
    h=F(1711,10000);bounds=[]
    for tilt,w in [(F(79656,100000),(F(1,4),F(3,4))),(-F(77603,100000),(F(1,2),F(1,2)))]:
        arg=tilt*h
        upper=exp_minus(arg)[1] if arg>=0 else 1/exp_minus(-arg)[0]
        coeff=mg(tilt,w)*upper
        require(10*coeff**375<1,'Chernoff certificate fails');bounds.append(float(coeff**375))
    source=json.loads((ROOT/'reconciliation_results.json').read_text())['fifth_moment_control']
    v1,v2,delta=map(F,[source['variance_original'],source['variance_alternative'],source['m4_difference']]);n=57291466
    def sufficient(M):
        remainder=M*delta**2/9-v1-v2
        return remainder>=0 and remainder**2>=4*v1*v2
    require(sufficient(n) and not sufficient(n-1),'Cantelli integer crossing');return {'sample_mean_sufficient':375,'rational_threshold':str(h),'chernoff_tail_upper_bounds':bounds,'Cantelli_sufficient':n,'CLT_normal_approximation':1.2815515655446004**2*(float(v1)**.5+float(v2)**.5)**2/float(delta)**2}

def main():
    results={}
    for name,hi,lo,n,n_full,time in [('equal_phase',(F(1,2),F(3,8)),(F(1,4),F(5,8)),165,117,F(22943,100000)),('antisymmetric',(F(1,2),F(1,2)),(F(1,4),F(3,4)),173,127,F(23077,100000))]:
        cert=certify_all_thresholds(n,hi,lo,time);hi=tuple(map(float,hi));lo=tuple(map(float,lo));e1,bc=transform(n_full,hi,lo,90,.04);e2,_=transform(n_full,hi,lo,145,.025)
        require(max(abs(e1[s]-e2[s]) for s in e1)<1e-11,'quadrature drift')
        brackets={str(N):histogram_bounds(N,hi,lo) for N in [n_full-1,n_full]}
        for k,(l,u) in brackets.items():require(l<=e2[k]<=u,'transform outside histogram bounds')
        require(brackets[str(n_full-1)][0]>.1 and brackets[str(n_full)][1]<.1,'inconclusive crossing')
        results[name]={'global_bit':cert,'full_likelihood_quadrature_risks':e2,'full_likelihood_FFT_binning_brackets':brackets,'full_count_status':'numerically resolved by two routes; no outward-rounded FFT proof', 'single_trial_Bhattacharyya':bc,'Bhattacharyya_sufficient':ceil(log(.2)/log(bc)),'Hellinger_necessary':ceil(log(.36)/(2*log(bc)))}
        print(name,cert,e2,brackets,flush=True)
    results['sample_mean_and_fifth']=secondary();ROOT.joinpath('sampling_results.json').write_text(json.dumps(results,indent=2,sort_keys=True)+'\n');print(results['sample_mean_and_fifth'])

if __name__=='__main__':main()
