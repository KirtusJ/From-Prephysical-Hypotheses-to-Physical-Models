"""Deterministic checks of conditional Choi pure-channel exclusion.

Research direction and responsibility: Kirtus Justus.
Mathematical/computational verification: ChatGPT (OpenAI).
7 November 2026, Vancouver, British Columbia, Pacific Time (UTC-7).
No laboratory data, random matrix samples, or simulated trial records.
"""
import math
from fractions import Fraction
import numpy as np
import mpmath as mp


def require(ok, message):
    if not bool(ok):
        raise ValueError(message)


def close(x, y, message, atol=3e-11):
    require(np.max(np.abs(np.asarray(x)-np.asarray(y))) < atol, message)


mp.mp.dps = 70
s = mp.mpf(131)/320
h = mp.mpf(99)/100
q = mp.mpf(81711338569043)/224995905216000
k = (mp.sqrt(s*h)-mp.sqrt(q))**2/(1-h)
d = s+k
r = 1-d
ell = mp.mpf('0.01')
f = r-ell

I = np.eye(2, dtype=complex)
X = np.array([[0,1],[1,0]],complex)
Y = np.array([[0,-1j],[1j,0]],complex)
Z = np.diag([1,-1]).astype(complex)
paulis = (I,X,Y,Z)

def ket(M):
    return np.asarray(M).reshape(16)/2

def outer(v):
    return np.outer(v,v.conj())

def trace_input(J):
    return np.trace(J.reshape(4,4,4,4),axis1=0,axis2=2)

def trace_output(J):
    return np.trace(J.reshape(4,4,4,4),axis1=1,axis2=3)

def product_output(J):
    return 4*J.reshape(4,4,4,4)[:,0,:,0]

def first_output(J):
    O=product_output(J)
    return np.trace(O.reshape(2,2,2,2),axis1=1,axis2=3)

def choi(U):
    return outer(ket(U))

def check_CPTP(J):
    close(J,J.conj().T,'J Hermitian')
    require(np.linalg.eigvalsh(J).min() > -1e-12,'J PSD')
    close(np.trace(J),1,'J normalized')
    close(trace_input(J),np.eye(4)/4,'J input marginal')

p=ket(np.eye(4)); u=ket(1j*np.kron(Z,I)); v=ket(1j*np.kron(X,I))
Pp,Pu,Pv=map(outer,(p,u,v))
Pnull=np.outer((float(mp.sqrt(k))*p+float(mp.sqrt(s))*u)/math.sqrt(float(d)),
               (float(mp.sqrt(k))*p+float(mp.sqrt(s))*u).conj()/math.sqrt(float(d)))
D=np.eye(16)-Pp-Pu-Pv
w=float(mp.sqrt(s))*p-float(mp.sqrt(k))*u
eta=w/math.sqrt(float(d))
e=float(mp.sqrt(h))*p+float(mp.sqrt(1-h))*u
E=outer(e)


def first_rates(J):
    R=first_output(J)
    return [np.trace((np.eye(2)+pauli)/2@R).real for pauli in (X,Y,Z)]


def pure_inequality(J):
    # Only intended for rank-one normalized Choi states of unitary channels.
    probs=first_rates(J)
    lam=max(np.linalg.eigvalsh(first_output(J)))
    sm=np.trace(Pp@J).real
    fm=np.trace(Pv@J).real
    qm=np.trace(E@J).real
    km=np.trace(Pu@J).real
    kmin=((math.sqrt(qm)-math.sqrt(float(h)*sm))**2)/(1-float(h))
    require(km + 1e-12 >= kmin,'Reverse-triangle sector bound')
    require(lam + 1e-12 >= 2*(sm+fm)-1,'Pure local-sector inequality')
    require(lam + 1e-12 >= 2*(sm+fm+kmin)-1,'Sharpened pure inequality')
    return lam,probs

# Directly construct the population-reference mixed normalized Choi state.
f64=float(f);d64=float(d);r64=float(r)
Jref=outer(w)+f64*Pv+(r64-f64)*D/13
check_CPTP(Jref)
close(np.trace(E@Jref),float(q),'ordinary detector rate')
close(np.trace(Pp@Jref),float(s),'match population')
close(np.trace(Pv@Jref),f64,'additional outcome')
pr=first_rates(Jref)
close(pr,[.5,.5,d64+6*.01/13],'reference triple')
lam_ref=max(np.linalg.eigvalsh(first_output(Jref)))
bare=2*(float(s)+f64)-1
sharp=2*(float(s)+float(k)+f64)-1
require(lam_ref < bare < sharp,'Exclusion ordering')

# A calibrated local subspace contains p, u, v, and iY_1 tensor identity.
local=[ket(np.kron(B,I)) for B in (I,1j*X,1j*Y,1j*Z)]
Ploc=sum(outer(t) for t in local)
close(Ploc@Ploc,Ploc,'local Choi subspace projector')
close(Ploc@p,p,'match in local sector')
close(Ploc@v,v,'extra vector in local sector')

# The two pure unitary witnesses from the source, reconstructed independently.
alpha=math.atan2(math.sqrt(float(k)),math.sqrt(float(s)))
T=np.kron(np.diag(np.exp(-0.5j*alpha*np.array([1,-1]))),I)


def check_pure_witness(Urot, expected_f):
    U=T@Urot@T
    close(U.conj().T@U,np.eye(4),'unitary witness')
    J=choi(U)
    check_CPTP(J)
    close(np.trace(Pp@J),float(s),'s witness')
    close(np.trace(E@J),float(q),'q witness')
    close(np.trace(Pv@J),expected_f,'f witness')
    close(np.trace(Pnull@J),0,'null direction witness')
    lam,probs=pure_inequality(J)
    close(probs[0:2],[.5,.5],'transverse reference witness')
    close(probs[2],d64+6*(r64-expected_f)/13,'Z reference witness')
    return lam

c0=math.sqrt(d64+6*r64/13)
c1=2*math.sqrt(d64)-c0
U0=np.diag([c0,c1,c1,c0]).astype(complex)
for j,kidx,co in [(0,3,c0),(1,2,c1)]:
    U0[j,kidx]=U0[kidx,j]=1j*math.sqrt(1-co*co)
lam0=check_pure_witness(U0,0)

fi=mp.findroot(lambda t:d*t-mp.mpf(42)/169*(r-t)**2,(mp.mpf('.07'),mp.mpf('.08')))
fil=float(fi); lfil=r64-fil
Q=(math.sqrt(d64)*I+1j*math.sqrt(fil)*X)/math.sqrt(d64+fil)
target=np.array([math.sqrt(6/13),-1j*math.sqrt(7/13)])
col=Q.conj().T@target
col*=np.exp(-1j*np.angle(col[0]))
N=np.array([[col[0].real,np.conj(col[1])],[col[1],-col[0].real]])
close(N@N,I,'Hermitian involution')
Ui=np.kron(Q,I)@(math.sqrt(d64+fil)*np.eye(4)+1j*math.sqrt(lfil)*np.kron(N,X))
lami=check_pure_witness(Ui,fil)

# Independently compute projected Gram matrices on all three support faces.
def inn(A,B):
    return np.trace(A@B).real

def projected_gram(sectors):
    B=sum(sectors)
    def center(M):
        V=B@M@B
        return V-sum(inn(W,V)*W/np.trace(W).real for W in sectors)
    marginal_basis=[np.kron(A,C)/2 for A in paulis for C in paulis][1:]
    marginal_tangents=[center(np.kron(np.eye(4),H)) for H in marginal_basis]
    ref=np.diag([1,0,0,0]); 
    obs=[center(4*np.kron(np.kron((I+S)/2,I),ref)) for S in (Z,X,Y)]
    QQ=np.array([[inn(A,B) for B in marginal_tangents] for A in marginal_tangents])
    CC=np.array([[inn(A,B) for B in obs] for A in marginal_tangents])
    correction=np.linalg.pinv(QQ,rcond=1e-10)@CC
    residual=[obs[j]-sum(correction[i,j]*marginal_tangents[i] for i in range(15)) for j in range(3)]
    for A in residual:
        close(trace_input(A),np.zeros((4,4)),'TP tangent')
    return np.array([[inn(A,B) for B in residual] for A in residual])

Gint=projected_gram([Pp,Pv,D])
Gzero=projected_gram([Pp,D])
Gmax=projected_gram([Pp,Pv])
close(Gint,np.diag([1230/91,97/7,97/7]),'Interior Gram',atol=4e-9)
close(Gzero,np.diag([159/13,25/2,254/21]),'f=0 Gram',atol=4e-9)
close(Gmax,np.diag([0,0,.5]),'f=r Gram',atol=4e-9)

# Pure exclusion is robust without an exact phase support equation if populations
# s and f and all three output probabilities have a simultaneous error box.
bz=2*pr[2]-1

def maxlambda(eps):
    return (1+math.sqrt((bz+2*eps)**2+8*eps*eps))/2

def minpurebound(eps):
    return bare-4*eps

low,high=0,.1
for _ in range(100):
    mid=(low+high)/2
    if minpurebound(mid)>maxlambda(mid): low=mid
    else:high=mid
critical=(low+high)/2
require(.039901950420 < critical < .039901950423,'robust threshold')
require(minpurebound(.03)>maxlambda(.03),'3-point population box excludes pure')

print('Source parameters: s',mp.nstr(s,22),'k_min',mp.nstr(k,22),
      'd',mp.nstr(d,22),'r',mp.nstr(r,22))
print('Reference at ell=.01: pZ',format(pr[2],'.15f'),
      'lambda_max',format(lam_ref,'.15f'))
print('Pure-channel necessary lambda, two populations:',format(bare,'.15f'))
print('Pure-channel necessary lambda, with ordinary detector rate:',format(sharp,'.15f'))
print('Pure reference exclusion gaps:',format(bare-lam_ref,'.15f'),format(sharp-lam_ref,'.15f'))
print('Pure unitary reference witnesses: f=0 lambda',format(lam0,'.15f'),
      'f=interior',mp.nstr(fi,19),'lambda',format(lami,'.15f'))
print('Gram diagonals: interior',np.diag(Gint).round(12).tolist(),
      'f=0',np.diag(Gzero).round(12).tolist(),
      'f=r',np.diag(Gmax).round(12).tolist())
print('Five-population uniform absolute-error threshold:',format(critical,'.15f'))
print('At 0.03 probability error: pure lower',format(minpurebound(.03),'.15f'),
      'observed eigenvalue upper',format(maxlambda(.03),'.15f'))
print('All deterministic calculations passed. No apparatus trials were used.')
