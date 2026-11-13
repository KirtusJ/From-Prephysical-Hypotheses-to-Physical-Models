"""Channel witnesses and product-readout purity bound. No trial records.
Research direction and responsibility: Kirtus Justus, Vancouver, 7 November 2026.
Python 3, NumPy and mpmath. Interval arithmetic certifies phase signs;
matrix calculations check the separate analytical identities.
"""
from fractions import Fraction
from math import cos, pi, sin, sqrt
from mpmath import iv
import numpy as np

s=131/320
h=.99
q=81711338569043/224995905216000


def require(test,message):
    if not test:
        raise ArithmeticError(message)


def near(left,right,message):
    require(np.max(np.abs(left-right))<2e-12,message)


def phase_witness():
    iv.dps=65
    si=iv.mpf(131)/320
    hi=iv.mpf(99)/100
    qi=iv.mpf(81711338569043)/224995905216000
    ai=si*hi
    t=ai-qi
    z4=iv.mpc(iv.mpf(112)/113,iv.mpf(15)/113)
    H=4*iv.sqrt(si)-z4
    length=abs(H)
    v=(length**2-3)/(2*length)
    z1=(v+1j*iv.sqrt(1-v**2))*H/length
    z2=(H-z1)/2
    alpha_A=(2*z1-2*z2)/iv.sqrt(6)
    alpha_B=(-z1-2*z2+3*z4)/iv.sqrt(12)
    def alpha(y):
        return (alpha_A+y*alpha_B)/(2*iv.sqrt(1+y*y))
    def ordinary_error(y):
        return abs(iv.sqrt(ai)+iv.sqrt(1-hi)*alpha(y))**2-qi
    left='-0.014452126001853375'
    right='-0.014452126001853374'
    require(ordinary_error(iv.mpf(left)).b<0 and ordinary_error(iv.mpf(right)).a>0,
            'ordinary rate not bracketed')
    w=alpha(iv.mpf([left,right]))
    b=(1-hi)*abs(w)**2
    z=2*iv.sqrt(ai*(1-hi))*w.imag
    def contrast(degrees):
        angle=iv.mpf(degrees)*iv.pi/180
        return 100*((1+iv.cos(angle))*(t+b)-iv.sin(angle)*z)
    for angle,lo,upper in [('60','.11820700','.11820701'),('61','-.02364943','-.02364942')]:
        val=contrast(angle)
        require(val.a>iv.mpf(lo) and val.b<iv.mpf(upper),'contrast enclosure')
        print(f'Balanced +/-{angle} deg, strict witness interval ({lo},{upper}) pp')
    require(contrast('60.83257915540').a>0 and contrast('60.83257915542').b<0,
            'witness zero not bracketed')
    print('Witness crossing in (60.83257915540,60.83257915542) degrees')
    # Direct matrix check at a rounded root; the sign brackets above certify an exact root.
    entries=np.array([complex(float(z.real.mid),float(z.imag.mid)) for z in (z1,z2,z2,z4)])
    y=float(left)
    axis=(np.array([2,-1,-1,0])/sqrt(6)+y*np.array([-1,-1,-1,3])/sqrt(12))/sqrt(1+y*y)
    p=np.eye(4).reshape(16)/2
    u=np.diag(axis).reshape(16)
    e=sqrt(h)*p+sqrt(1-h)*u
    P=np.outer(p,p.conj())
    near(abs(entries),1,'unitary entries')
    near(np.vdot(p,e),sqrt(h),'reference response')
    for deg in (60,61):
        gains=[]
        for sign in (-1,1):
            entries_signed=entries if sign==-1 else entries.conj()
            psi=np.diag(entries_signed).reshape(16)/2
            rho=np.outer(psi,psi.conj())
            near(np.trace(rho.reshape(4,4,4,4),axis1=0,axis2=2),np.eye(4)/4,'TP Choi marginal')
            near(abs(np.vdot(p,psi))**2,s,'match probability')
            near(abs(np.vdot(e,psi))**2,q,'ordinary probability')
            gate=P+np.exp(1j*(pi+sign*deg*pi/180))*(np.eye(16)-P)
            gains.append(100*(abs(np.vdot(e,gate@psi))**2-q))
        near(gains[0],gains[1],'balanced gains')
        near(gains[0],float(contrast(str(deg)).mid),'Born contrast')


def source_controls():
    fs,fh,fq=Fraction(131,320),Fraction(99,100),Fraction(81711338569043,224995905216000)
    a=fs*fh
    corner=(1-fs)*(1-fh)
    t=a-fq
    forced=(t+corner)**2/((1-fs)**2*fh*(1-fh))
    possible={Fraction((4-2*j)**2,j*(4-j)) for j in (1,2,3)}
    require(forced not in possible and possible=={0,Fraction(4,3)},'multiplicity exclusion')
    zsq=4*a*corner-(t+corner)**2
    require(0<zsq<a*fq/16,'curvature comparison')
    z0=sqrt(float(zsq))
    angle=pi/3
    upper=lambda offset: 4*sqrt(s*(1-h)*(1-q))*cos(offset/2)-4*s*(1-h)*cos(offset/2)**2
    lower=(float(t+corner)*(1+cos(angle))-z0*sin(angle))
    near(100*lower,-.18064212209155,'density lower')
    require(abs(100*upper(angle)-16.459262144)<1e-8,'density upper')
    require(abs(75*upper(0)-14.089601593)<1e-8,'shared upper')
    require(abs(75*4*(float(a)-sqrt(float(a*fq)))-6.490194215)<1e-8,'shared lower')
    print('Forced squared root sum',f'{float(forced):.12f}','variance modulus',f'{z0:.12f}')


def purity_projection():
    ket=lambda op: op.reshape(16)/2
    def project(x):
        return np.outer(x,x.conj())
    def partial_out(x):
        return np.trace(x.reshape(4,4,4,4),axis1=0,axis2=2)
    p=ket(np.eye(4))
    u=ket(1j*np.diag([1,1,-1,-1]))
    v=ket(1j*np.kron([[0,1],[1,0]],np.eye(2)))
    a=s*h; k=(a-sqrt(a*q))**2/(s*h*(1-h)); d=s+k; r=1-d
    eta=(sqrt(s)*p-sqrt(k)*u)/sqrt(d)
    theta=(sqrt(k)*p+sqrt(s)*u)/sqrt(d)
    D=np.eye(16)-project(p)-project(u)-project(v)
    B=np.eye(16)-project(theta)
    pick=np.diag([1,0,0,0]); obs=4*np.kron(np.diag([1,1,0,0]),pick)
    perpendicular=B@obs@B-project(eta)-6*D/13
    residual=partial_out(perpendicular)
    near(residual,6*(pick-np.eye(4)/4),'reference residual')
    sharp=perpendicular-(2/7)*B@np.kron(np.eye(4),residual)@B
    near(partial_out(sharp),np.zeros((4,4)),'TP tangent')
    near(np.trace(perpendicular@perpendicular),276/13,'population-only norm')
    near(np.trace(sharp@sharp),1230/91,'projected norm')
    for f in (r/14,r/2):
        minimum=d*project(eta)+f*project(v)+(r-f)*D/13
        J=d*d+f*f+(r-f)**2/13
        base=d+6*(r-f)/13
        for change in (-.01,0,.01):
            state=minimum+change*(91/1230)*sharp
            near(partial_out(state),np.eye(4)/4,'channel marginal')
            require(np.linalg.eigvalsh(state)[0]>=-2e-13,'positive channel')
            near(np.vdot(v,state@v),f,'orthogonal outcome')
            near(np.vdot(eta,state@eta),d,'visible population')
            near(state@theta,0,'phase compression')
            near(np.trace(state@obs),base+change,'product-input rate')
            near(np.trace(state@state),J+91/1230*change**2,'attained bound')
    print('Projection norm squared 1230/91; locally sharp coefficient 91/1230')


if __name__=='__main__':
    source_controls()
    phase_witness()
    purity_projection()
