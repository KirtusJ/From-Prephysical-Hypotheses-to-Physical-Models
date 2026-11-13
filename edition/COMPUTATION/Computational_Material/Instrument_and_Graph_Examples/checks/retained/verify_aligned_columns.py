"""Exact arithmetic checks of a four-input two-qubit branch and its optional-stopping score."""
from fractions import Fraction as Q
from math import acos,cos,pi,sin
import numpy as np

def verify(condition,message):
    if not condition:
        raise ArithmeticError(message)

def paired_columns(amplitudes, remaining, assignment):
    # Branch vectors in (environment, first output, second output, input) order.
    cols = [{} for _ in range(4)]
    for i,amps in enumerate(amplitudes):
        for y,v in enumerate(amps):
            cols[i][(y,y,i)]=v
    for i,v in enumerate(remaining,2):
        cols[i][(2,0,i%2)]=v
    def inner(i,j):
        return sum(v*cols[j].get(key,0) for key,v in cols[i].items())
    s=[inner(i,i) for i in range(4)]
    verify(all(0<=z<=1 for z in s) and sum(s)>0,'Raw successes')
    verify(all(inner(i,j)==0 for i in range(4) for j in range(i)),'Trace nonincrease')
    # Squared norm of the Hilbert-Schmidt projection onto V⊗I.
    projected=Q(0)
    for e in range(3):
        for out in range(2):
            for first in range(2):
                left=cols[2*first].get((e,out,0),0)
                right=cols[2*first+1].get((e,out,1),0)
                projected+=Q(1,2)*(left+right)**2
    w=projected/sum(s)
    d=sum((x-y)**2 for x,y in zip(*amplitudes))
    d_other=(remaining[0]-remaining[1])**2
    verify(d+d_other==2*sum(s)*(1-w),'Exact Choi projection')
    # Finite maximizing dual slopes for these positive entries.
    ratios=[y/x for x,y in zip(*amplitudes)]+[remaining[1]/remaining[0]]
    eps=1-w
    verify(sum(assignment)==1 and min(assignment)>0,'Assignment vector')
    mean=Q(0)
    for i in range(4):
        events=[v*v for v in amplitudes[i]] if i<2 else [s[i]]
        for j,raw in enumerate(events):
            ratio=ratios[j] if i<2 else ratios[-1]
            coefficient=1-ratio if i%2==0 else 1-1/ratio
            score=(coefficient-2*eps)/assignment[i]
            mean+=assignment[i]*raw*score
    verify(mean==0,'Boundary conditional expectation')
    return s,d,d_other,w

def control_scores():
    rates=((Q(9,100),Q(4,100)),(Q(4,100),Q(9,100)))
    probs=(Q(3,8),Q(3,8),Q(1,8),Q(1,8))
    slopes=(Q(2,3),Q(3,2))
    penalty=Q(1,113)
    contributions=[sum(r*((1-t if i==0 else 1-1/t)-penalty)
                       for r,t in zip(row,slopes)) for i,row in enumerate(rates)]
    contributions.extend([-penalty,-penalty])
    weighted=sum(p*(v/p) for p,v in zip(probs,contributions))
    unweighted=sum(p*v for p,v in zip(probs,contributions))
    verify((weighted,unweighted)==(0,Q(1,226)),'Unequal assignment means')
    total=2*Q(1,2)+1+Q(1,4)
    cap=1-(1-Q(1,2))**2/(2*total)
    verify(cap==Q(17,18),'Resolved-success ceiling')
    identity=np.eye(4)
    second_click=np.kron(np.eye(2),np.diag([0,1]))
    second_rates=[(identity[:,i]@second_click@identity[:,i]) for i in (0,1)]
    verify(second_rates==[0.,1.] and sum((x-y)**2 for x,y in zip((1,0),(0,1)))==2,
            'Second-qubit example')
    print('Unequal-assignment expected scores:',weighted,unweighted)
    print('Maximum four-input weight:',cap,'; identity with second-qubit readout gives D=2.')

def density(angle):
    v=np.array([cos(angle/2),sin(angle/2)])
    return np.outer(v,v)

def root_fidelity(x,y):
    def psqrt(matrix):
        vals,basis=np.linalg.eigh(matrix)
        return (basis*np.sqrt(np.maximum(vals,0)))@basis.T
    return float(np.linalg.svd(psqrt(x)@psqrt(y),compute_uv=False).sum())

def check_angles():
    low, high=.2,.8
    for c in [0.,.5,.96,1.]:
        for theta in [0.,pi/6,pi/2,pi]:
            tau=min(acos(c),(pi-theta)/2)
            # Angles are relative to the z axis; bisector is z and perpendicular axis x.
            rho0=density(pi/2-tau);rho1=density(pi/2+tau)
            e0=low*np.eye(2)+(high-low)*density(theta/2)
            e1=low*np.eye(2)+(high-low)*density(-theta/2)
            prob0=np.trace(e0@rho0);prob1=np.trace(e1@rho1)
            sharp=(high-low)*sin(min(pi/2,theta/2+acos(c)))
            verify(abs(prob0-prob1-sharp)<1e-12 and root_fidelity(rho0,rho1)>=c-2e-12,
                    'Angle bound and feasible extremizer')
    # Evaluate mixed pairs independently through fidelity and explicit effects.
    for k in [0.,.25,.8,1.]:
        for m in [0.,.33,1.]:
            a=k*density(.8)+(1-k)*np.eye(2)/2; b=m*density(-.5)+(1-m)*np.eye(2)/2
            c=min(1.,root_fidelity(a,b))
            for theta in [0.,.2,1.,pi]:
                e0=low*np.eye(2)+(high-low)*density(0.)
                e1=low*np.eye(2)+(high-low)*density(theta)
                bound=(high-low)*sin(min(pi/2,theta/2+acos(c)))
                verify(abs(np.trace(e0@a)-np.trace(e1@b)) <= bound+2e-12,'Mixed-state bound')
    print('Common-effect and rotated-effect contrast endpoints attained, including identical successful states at c=1.')

if __name__=='__main__':
    a=((Q(3,10),Q(1,5)),(Q(1,5),Q(3,10)))
    uniform=(Q(1,4),)*4
    uneven=(Q(1,10),Q(2,10),Q(3,10),Q(4,10))
    for assignment in (uniform,uneven):
        s,d,pooled,w=paired_columns(a,(Q(1),Q(1)),assignment)
        verify((d,pooled,w)==(Q(1,50),0,Q(225,226)),'Reported boundary')
        s,d,extra,w=paired_columns(a,(Q(1,2),Q(1,4)),assignment)
        verify(extra==Q(1,16),'Difference of successes on the remaining pair')
        print('Assignment',*assignment,'; sharp unequal-success check:',d,extra,w)
    print('Both projection identities and the exact score means passed.')
    control_scores()
    check_angles()
