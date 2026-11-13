"""Distance-constrained balanced readout. No trial data.
Research direction and responsibility: Kirtus Justus. Vancouver, 7 November 2026.
Uses NumPy and mpmath. Interval and matrix diagnostics are distinct.
"""
from math import cos, pi, sin, sqrt
import numpy as np
from mpmath import iv

s=131/320
h=.99
q=81711338569043/224995905216000
a=s*h
t=a-q
g=sqrt(h*(1-h))
b0=(1-h)*(1-s)
z0=sqrt(4*a*b0-(t+b0)**2)
center=a+q
radius=2*sqrt(a*q)


def require(test,reason):
    if not test:
        raise ArithmeticError(reason)


def near(x,y,reason):
    require(np.max(np.abs(x-y))<7e-13,reason)


def optimal_pair(angle,cap):
    z=min(g*cap,z0,radius*sin(angle/2))
    b=center-sqrt(radius**2-z**2)
    delta=(1+cos(angle))*(t+b)-sin(angle)*z
    return b,z,delta


def direct_check(angle,cap):
    b,z,goal=optimal_pair(angle,cap)
    e=np.array([sqrt(h),sqrt(1-h),0])
    groups=[]
    clicks=[]
    for sign in (-1,1):
        c=complex(-(t+b),sign*z)/2
        k=b/(1-h)
        rho=np.array([[s,c/g,0],[c.conjugate()/g,k,0],[0,0,1-s-k]],complex)
        near(np.trace(rho),1,'trace')
        require(np.linalg.eigvalsh(rho)[0]>=-4e-13,'state positivity')
        near(e@rho@e,q,'ordinary rate')
        U=np.diag([1,np.exp(1j*(pi+sign*angle)),np.exp(1j*(pi+sign*angle))])
        clicks.append((e@U@rho@U.conj().T@e).real-q)
        groups.append(rho)
    D=np.abs(np.linalg.eigvalsh(groups[1]-groups[0])).sum()/2
    near(D,z/g,'trace distance')
    require(D<=cap+1e-13,'distance cap')
    near(np.mean(clicks),goal,'Born contrast')
    return goal


def certify_thresholds():
    iv.dps=65
    si=iv.mpf(131)/320
    hi=iv.mpf(99)/100
    qi=iv.mpf(81711338569043)/224995905216000
    ai=si*hi;ti=ai-qi;gi=iv.sqrt(hi*(1-hi))
    bc=(1-hi)*(1-si)
    b=(ai-2*ti-iv.sqrt(ai*(ai-4*ti)))/2
    threshold=iv.sqrt(3)*(ti+b)/gi
    require(b.a>0 and b.b<bc.a, 'zero on first disk branch')
    require(threshold.a>iv.mpf('.8309705985874090') and
            threshold.b<iv.mpf('.8309705985874091'),'sharp distance enclosure')
    simple=3*(ai-iv.sqrt(ai*qi))/(iv.sqrt(3)*gi/2)
    require(simple.a>iv.mpf('.753198530485523') and simple.b<iv.mpf('.753198530485525'),
            'linear threshold')
    def polynomial(x):
        v=iv.mpf(x)
        return (b/(1-hi))*v*v-(ti+b)*v/gi-(1-si)
    require(polynomial('-.684').a>0 and polynomial('1.537').a>0
            and polynomial('0').b<0,'spectral bounds')
    maxsq=(2*684**2+1537**2+169**2)/(4*1000**2)
    require(maxsq<.832,'four-eigenvalue bound')
    print('Critical general-state cap lies between .8309705985874090 and .8309705985874091.')
    print('Enlarged spectral box has maximum mean square',maxsq)


def pooled_control():
    # One common projection, unequal group populations and ordinary responses.
    p=np.array([1,0,0,0]);e=np.array([sqrt(h),sqrt(1-h),0,0])
    E=np.outer(e,e);E[2,2]=1
    R=np.eye(4)-np.outer(p,p)
    coords=np.arange(1,17).reshape(4,4)
    for trial in range(1,33):
        groups=[]
        for group in (1,2):
            F=np.sin(coords*(.27+trial/17))+1j*np.cos((coords.T+group)*(.41+group*trial/11))
            mat=F@F.conj().T
            groups.append(mat/mat.trace())
        avg=(groups[0]+groups[1])/2
        pop=float(avg[0,0].real); b=np.trace(E@R@avg@R).real
        c=[np.trace(E@np.outer(p,p)@rho@R) for rho in groups]
        reflected=(c[0]+c[1].conjugate())/2
        D=np.abs(np.linalg.eigvalsh(groups[0]-groups[1])).sum()/2
        require(abs(reflected)**2<=min(h*pop*b,(1-h)*pop*(1-pop-b))+2e-14,'pooled disks')
        require(abs(2*reflected.imag)<=g*D+2e-14,'distance inequality')


def calibrate_y():
    ell=.01
    k=(a-sqrt(a*q))**2/(s*h*(1-h))
    d=s+k;f=1-d-ell
    N00=abs((sqrt(s)+1j*sqrt(k))*sqrt(6/13)-1j*sqrt(f)*sqrt(7/13))/sqrt(d+f)
    for mix in (-1,-.41,0,.76,1):
        y=2*N00*mix*sqrt(ell*(1-ell))
        purity=(1-ell)**2+ell*ell+2*mix**2*ell*(1-ell)
        near(purity,(1-ell)**2+ell*ell+y*y/(2*N00*N00),'second-qubit Y')
    print('Two-sign Y endpoint magnitude',f'{2*N00*sqrt(ell*(1-ell)):.12f}')


if __name__=='__main__':
    certify_thresholds()
    for degrees in (0,10,30,60,61,90,130,180):
        for cap in (0,.2,.5,.753198530485524,.8,.83,.84,.85,.9,1):
            direct_check(degrees*pi/180,cap)
    for cap in (0,.5,.753198530485524,.8,.83,.84,.856874052566415):
        print(f'cap {cap:.12f}, sharp minimum at 60 degrees {100*direct_check(pi/3,cap):.10f} pp')
    pooled_control()
    calibrate_y()
