"""Numerical checks for transverse readout bounds and exact channel examples.
Kirtus Justus, research direction and responsibility. Vancouver, 7 November 2026.
Requires NumPy, mpmath and SciPy. No trials or simulated observations.
"""
from math import cos, pi, sin, sqrt
import numpy as np
from mpmath import iv

s, h = 131/320, .99
q = 81711338569043/224995905216000
k = (s*h-sqrt(s*h*q))**2/(s*h*(1-h))
d = s+k
r = 1-d
I = np.eye(2)
X = np.array([[0,1],[1,0]],complex)
Y = np.array([[0,-1j],[1j,0]])
Z = np.diag([1,-1])
I4 = np.eye(4)


def check(condition, reason):
    if not condition:
        raise ArithmeticError(reason)


def close(left, right, reason):
    check(np.max(np.abs(left-right))<6e-13, reason)


def ket(matrix):
    return matrix.reshape(16)/2


def outer(left, right=None):
    if right is None:
        right=left
    return np.outer(left,right.conj())


p=ket(I4)
u=ket(1j*np.kron(Z,I))
v=ket(1j*np.kron(X,I))
W=(sqrt(s)*I4-1j*sqrt(k)*np.kron(Z,I))/sqrt(d)
V=1j*np.kron(X,I)
eta=ket(W)
span=outer(eta)+outer(v)
spectators=np.eye(16)-outer(p)-outer(u)-outer(v)
e=sqrt(h)*p+sqrt(1-h)*u
xi=np.array([(sqrt(s)-1j*sqrt(k))/sqrt(d),0])
nu=np.array([0,1j])
O=outer(xi,nu)+outer(nu,xi)
# K selects reference input 00 and converts the normalized Choi block to output.
K=np.kron(I4,[[2,0,0,0]])
D=K.conj().T@np.kron(O,I)@K


def bounds(f, reading):
    ell=r-f
    tolerance=4*ell+2*sqrt(3*(1-ell)*ell)
    xlow=max(0,abs(reading)-tolerance)
    xhigh=abs(reading)+tolerance
    central=d*d+f*f
    lo=central+ell**2/13+xlow**2/2
    hi=central+min(4*d*f,xhigh*xhigh+ell*ell)/2+2*(1-ell)*ell+ell*ell
    return lo,min(hi,1.)


def output_first(state):
    full=K@state@K.conj().T
    return np.trace(full.reshape(2,2,2,2),axis1=1,axis2=3)


def check_state(state,f):
    close(state,state.conj().T,'Hermitian state')
    check(np.linalg.eigvalsh(state)[0]>-5e-13,'positive state')
    tensor=state.reshape(4,4,4,4)
    close(np.trace(tensor,axis1=0,axis2=2),I4/4,'trace preservation')
    close(np.trace(tensor,axis1=1,axis2=3),I4/4,'unitality')
    close(v.conj()@state@v,f,'orthogonal outcome')
    close(p.conj()@state@p,s,'match population')
    close(u.conj()@state@u,k,'complement population')
    close(p.conj()@state@u,-sqrt(s*k),'complex quadrature')
    gamma=eta.conj()@state@v
    reading=np.trace(D@state).real
    impurity_tol=5e-13
    check(2*abs(gamma.imag)<=r-f+impurity_tol,'imaginary coherence')
    lo,hi=bounds(f,reading)
    purity=np.trace(state@state).real
    check(lo-impurity_tol<=purity<=hi+impurity_tol,'purity enclosure')
    return purity


def construct(f):
    ell=r-f
    U=(sqrt(s)*I-1j*sqrt(k)*Z+1j*sqrt(f)*X)/sqrt(d+f)
    target=np.array([sqrt(6/13),sqrt(7/13)])
    col=U.conj().T@target
    col*=np.exp(-1j*np.angle(col[0]))
    a,b=col
    N=np.array([[a.real,b.conjugate()],[b,-a.real]])
    close(N@N,I,'Hermitian involution')
    main=sqrt(d+f)*np.kron(U,I)
    rest=1j*sqrt(ell)*np.kron(U@N,X)
    states=[]
    for sign in (1,-1):
        matrix=main+sign*rest
        close(matrix.conj().T@matrix,I4,'unitary channel')
        states.append(outer(ket(matrix)))
    return states,a.real


def channel_controls():
    rel=W.conj().T@V/1j
    probe=np.kron(I4,rel.T)
    close(rel,rel.conj().T,'Hermitian input observable')
    close(probe@eta,-1j*v,'invariant reference subspace')
    close(probe@v,1j*eta,'invariant reference subspace')
    cross=span@D@(np.eye(16)-span)
    close(cross@cross.conj().T,3*span,'transverse norm')
    for ell in (0.,.0001,.01,r/2,r):
        f=r-ell
        (plus,minus),a=construct(f)
        uniform=d*outer(eta)+f*outer(v)+ell*spectators/13
        minimum=d*d+f*f+ell**2/13
        close(check_state(uniform,f),minimum,'sharp lower witness')
        local=output_first(plus)
        close(local,output_first(minus),'all first-qubit data')
        close(local[0,0],d+6*ell/13,'specified product Z rate')
        for weight in (0.,.2,.5,.83,1.):
            state=weight*plus+(1-weight)*minus
            purity=check_state(state,f)
            full=K@state@K.conj().T
            measured_y=np.trace(np.kron(I,Y)@full)
            close(measured_y,2*a*(2*weight-1)*sqrt(ell*(1-ell)),
                  'second-output sign')
            expected=(1-ell)**2+ell**2+2*(2*weight-1)**2*ell*(1-ell)
            close(purity,expected,'invisible sign interpolation')
            # Spectator direction in the pure unitary is arbitrary within that subspace.
            mixture=(1-weight)*uniform+weight*plus
            close(check_state(mixture,f),minimum+(1-minimum)*weight**2,
                  'full interval on the named Z line')
        print('residual',f'{ell:.8f}','unseen purity width',f'{2*ell*(1-ell):.10f}')
    # The trace-preserving marginal bound on imaginary coherence can saturate.
    ell=.01
    f=r-ell
    for sign in (-1,1):
        gamma=sign*1j*ell/2
        hidden=ket(W@np.kron(I,X)@(I4-sign*rel)/sqrt(2))
        close(hidden.conj()@hidden,1.,'hidden population')
        state=(d*outer(eta)+f*outer(v)+gamma*outer(eta,v)
               +gamma.conjugate()*outer(v,eta)+ell*outer(hidden))
        check_state(state,f)
        close(eta.conj()@state@v,gamma,'imaginary saturation')
    # Coherence with a residual direction can affect a local transverse reading.
    U=(sqrt(s)*I-1j*sqrt(k)*Z+1j*sqrt(f)*X)/sqrt(d+f)
    visible=sqrt(d+f)*np.kron(U,I)
    for sign in (-1,1):
        unitary=visible+sign*1j*sqrt(ell)*np.kron(U@Y,Z)
        close(unitary.conj().T@unitary,I4,'controlled unitary')
        state=outer(ket(unitary))
        check_state(state,f)
        discrepancy=abs(np.trace(D@state)-2*(eta.conj()@state@v).real)
        check(discrepancy>1e-4,'interior transverse contamination control')
    for gamma in (-sqrt(d*r),.25,0.,sqrt(d*r)):
        state=d*outer(eta)+r*outer(v)+gamma*(outer(eta,v)+outer(v,eta))
        close(check_state(state,r),d*d+r*r+2*gamma*gamma,'boundary identity')
        close(np.trace(D@state),2*gamma,'signed transverse response')
    print('Example f=r-0.0001 and transverse reading 0.5:',bounds(r-.0001,.5))


def angular_controls():
    from scipy.optimize import minimize_scalar
    iv.dps=60
    si=iv.mpf(131)/320
    hi=iv.mpf(99)/100
    qi=iv.mpf(81711338569043)/224995905216000
    a=si*hi; g=si*(1-hi); t=a-qi
    b0=(1-si)*(1-hi)
    z0=iv.sqrt(4*a*b0-(t+b0)**2)
    c2=-t-2*g; r2=2*iv.sqrt(g*(1-qi))
    angle=iv.pi/6
    low=100*((1+iv.cos(angle))*(t+b0)-iv.sin(angle)*z0)
    high=100*(4*iv.sqrt(g*(1-qi))*iv.cos(angle/2)-4*g*iv.cos(angle/2)**2)
    check(low.a>iv.mpf('4.69764481') and low.b<iv.mpf('4.69764482'),'30 degree lower rounding')
    check(high.a>iv.mpf('18.19990865') and high.b<iv.mpf('18.19990866'),'30 degree upper rounding')
    for delta,sign in [('113.20968269065',1),('113.20968269067',-1)]:
        diff=c2+r2*iv.cos(iv.pi*iv.mpf(delta)/360)-b0
        check(diff*sign>0,'upper-branch switch bracket')
    # Independent numerical diagnostic, separate from the analytic supporting-disk proof.
    a=s*h; g=s*(1-h); t=a-q; b0=(1-s)*(1-h)
    z0=sqrt(4*a*b0-(t+b0)**2)
    c1=a+q; r1=2*sqrt(a*q); c2=-t-2*g; r2=2*sqrt(g*(1-q))
    left,right=c1-r1,c2+r2
    for degrees in (0,10,30,58,110,120,150,180):
        delta=degrees*pi/180
        ax,az=1+cos(delta),abs(sin(delta))
        for direction in (-1,1):
            def objective(b):
                height=sqrt(max(0,min(4*a*b,4*g*(1-s-b))-(t+b)**2))
                return direction*ax*(t+b)-az*height
            cuts=(left,b0,right)
            samples=[objective(x) for x in cuts]
            for u0,u1 in zip(cuts,cuts[1:]):
                fit=minimize_scalar(objective,bounds=(u0,u1),method='bounded',
                                    options={'xatol':1e-15})
                samples.append(fit.fun)
            norm=2*cos(delta/2)
            if direction==1 and c1-r1*cos(delta/2)<=b0:
                exact=ax*(t+c1)-r1*norm
            elif direction==-1 and c2+r2*cos(delta/2)>=b0:
                exact=-ax*(t+c2)-r2*norm
            else:
                exact=direction*ax*(t+b0)-az*z0
            check(abs(min(samples)-exact)<1e-9,'scalar search diagnostic')
    print('30 degree outer interval [4.69764481,18.19990866] pp; full-circle supports checked')


if __name__=='__main__':
    angular_controls()
    channel_controls()
