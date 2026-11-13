"""Run python -B check_folded_free_field.py OUTPUT_DIRECTORY (NumPy).

Check the local real-linear rule and site masses exactly on four ticks from
each site parity. Compare direct signed-rail and folded spectral evolution;
test a narrow scalar plane wave, both signs of a localized packet, a broad
tail, and a shrinking binary flight window using independent physical rails.
"""
import argparse
import json
from pathlib import Path

import numpy as np


def add(a,b):
    return a[0]+b[0], a[1]+b[1]


def mul(a,b):
    return a[0]*b[0]-a[1]*b[1], a[0]*b[1]+a[1]*b[0]


def rotate(z,n):
    return mul(z, ((1,0),(0,1),(-1,0),(0,-1))[n%4])


def exact_trace(s):
    N = 16
    state = [(0,0)]*N
    state[s],state[s+2],state[s+4] = (2,-1),(-3,2),(1,4)
    initial_mass = sum(r*r+l*l for r,l in state)
    previous = None
    rows = []
    factor = (1,0)
    for t in range(5):
        # (1-i)^t i^x times raw signed rails equals 2^t times the field.
        field = [mul(factor,rotate(rails,x)) for x,rails in enumerate(state)]
        assert all(r*r+l*l == (2**t)*(a*a+b*b)
                   for (r,l),(a,b) in zip(field,state))
        assert sum(r*r+l*l for r,l in field) == 4**t * initial_mass
        if previous is not None:
            for x,z in enumerate(field):
                left,right = previous[x-1],previous[(x+1)%N]
                conjugate_difference = left[0]-right[0],right[1]-left[1]
                assert z == add(add(left,right),rotate(conjugate_difference,t+2*s))
        rows.append(dict(tick=t, scaled_field=field))
        state = [(sum(state[x-1]),state[(x+1)%N][0]-state[(x+1)%N][1]) for x in range(N)]
        previous,factor = field,mul(factor,(1,-1))
    return dict(origin_parity=s, initial_mass=initial_mass, field_denominator="2^tick", rows=rows)


class PeriodicWalk:
    def __init__(self,N):
        assert N%4 == 0
        self.N = N
        self.x = np.arange(N)
        self.carrier = (1j)**(self.x%4)
        self.k = 2*np.pi*np.fft.fftfreq(N)
        self.q = (self.k+np.pi/2)%np.pi-np.pi/2
        self.omega = np.arcsin(np.sin(self.k)/np.sqrt(2))
        self.plus = np.exp(-1j*self.omega)
        self.minus = -np.exp(1j*self.omega)
        H = np.array([[1,1],[1,-1]])/np.sqrt(2)
        U = np.exp(np.stack([-1j*self.k,1j*self.k],axis=1))[:,:,None]*H
        self.projector = (U-self.minus[:,None,None]*np.eye(2))/(self.plus-self.minus)[:,None,None]

    def encode(self,rails,t):
        return self.carrier*np.exp(-1j*t*np.pi/4)*(rails[:,0]+1j*rails[:,1])

    def decode(self,field,t):
        z = self.carrier.conj()*np.exp(1j*t*np.pi/4)*field
        return np.column_stack((z.real,z.imag))

    def fly(self,rails,n):
        freq = np.fft.fft(rails,axis=0)
        a = np.einsum("nij,nj->ni",self.projector,freq)
        freq = self.plus[:,None]**n*a+self.minus[:,None]**n*(freq-a)
        flight = np.fft.ifft(freq,axis=0)
        assert np.max(abs(flight.imag)) < 2e-11
        return flight.real

    def direct(self,rails,n):
        for _ in range(n):
            r,l = rails.T
            rails = np.column_stack((np.roll(r+l,1),np.roll(r-l,-1)))/np.sqrt(2)
        return rails

    def scalar(self,field,n):
        # The second Fourier copy receives (-1)^n as occupied parity advances.
        in_primary_chart = (self.k >= -np.pi/2) & (self.k < np.pi/2)
        replica = np.where(in_primary_chart,1,(-1)**n)
        return np.fft.ifft(np.fft.fft(field)*replica*np.exp(-0.5j*n*self.q**2))

    def energy(self,field,mask):
        power = abs(np.fft.fft(field))**2
        return float(sum(power[mask])/sum(power))

    def compare(self,field,t,n,Q):
        field = field / np.linalg.norm(field)
        rails = self.decode(field,t)
        actual = self.encode(self.fly(rails,n),t+n)
        approx = self.scalar(field,n)
        cut = np.abs(self.q) <= Q
        tail = np.sqrt(self.energy(field,~cut))
        # ||P_-(k)-P_-(k*)|| <= |q|, ||ell||=sqrt(2), two unit phases.
        bound = 2*np.sqrt(2)*Q + n*Q**4/6 + 2*tail
        err = float(np.linalg.norm(actual-approx))
        assert err <= bound+1e-10
        assert abs(np.linalg.norm(actual)-1)<1e-10
        return dict(ticks=n,Q=Q,scalar_tail_norm=float(tail),error=err,bound=float(bound))


def spectral_checks():
    walk = PeriodicWalk(128)
    f = np.zeros(128,dtype=complex)
    f[1],f[3],f[7] = 2-1j,-3+2j,1+4j
    rails = walk.decode(f,0)
    for n in (1,2,3,4,7,16):
        assert np.max(abs(walk.fly(rails,n)-walk.direct(rails,n))) < 2e-13
    # A mode exactly at the half-open chart boundary must switch parity as well.
    at_edge = (walk.x % 2 == 0) * (1j)**(walk.x % 4)
    across_edge = walk.scalar(at_edge,1)
    assert np.max(abs(across_edge[::2])) < 1e-13
    assert abs(np.linalg.norm(across_edge[1::2])-np.linalg.norm(at_edge)) < 1e-12
    advanced = lambda h: walk.encode(walk.fly(walk.decode(h,0),1),1)
    anti = float(np.linalg.norm(advanced(1j*f)-1j*advanced(f))/np.linalg.norm(f))
    assert anti>1
    # A restored position representative then changes the encoder sign.
    seams = []
    for N in (126,130):
        factor = (1j)**(N % 4)
        assert factor == -1
        seams.append(dict(N=N,factor=[int(factor.real),int(factor.imag)]))
    rule = []
    for N in (128,256,512):
        grid = PeriodicWalk(N)
        q = 4*np.pi/N
        for sign in (-1,1):
            field = np.exp(1j*sign*q*grid.x)*(grid.x%2==1)
            narrow = grid.compare(field,1,round(1/q**2),q+1e-14)
            broad = field + .25*(grid.x%2==1)*np.exp(1j*np.pi*grid.x/4)
            rule.append(dict(N=N,sign=sign,narrow=narrow,
                             broad=grid.compare(broad,1,round(1/q**2),q+1e-14)))
    return dict(direct_fft_ticks=[1,2,3,4,7,16], odd_source_relative_antilinearity=anti,
                chart_boundary_wrong_parity_norm=float(np.linalg.norm(across_edge[::2])),
                periodic_seam=seams, cases=rule)


def signed_packet_and_filter():
    grid = PeriodicWalk(2048)
    y = grid.x-grid.N//2
    rows = []
    for sign in (-1,1):
        f = (grid.x%2==0)*np.exp(-y*y/(4*24**2)+1j*sign*.18*y)
        f /= np.linalg.norm(f)
        out = grid.encode(grid.fly(grid.decode(f,0),96),96)
        mean = float(np.sum(y*abs(out)**2))
        assert mean*sign>0
        rows.append(dict(sign=sign,mean_at_96=mean,
                         initial_right_momentum_fraction=grid.energy(f,grid.q>0)))
    windows = []
    for ticks,v,w in ((512,.16,.035),(1024,.12,.026)):
        grid = PeriodicWalk(4*ticks)
        y = grid.x-grid.N//2
        sharp = np.zeros((grid.N,2))
        sharp[grid.N//2,0]=1
        free = grid.fly(sharp,ticks)
        for sign in (-1,1):
            selected = free*(abs(y/ticks-sign*v)<=w)[:,None]
            p = float(np.linalg.norm(selected)**2)
            f = grid.encode(selected/np.sqrt(p),ticks)
            correct = grid.energy(f,grid.q*sign>0)
            further = grid.fly(selected/np.sqrt(p),256)
            drift = float(np.sum(y*(np.sum(further*further,axis=1)-abs(f)**2))/256)
            assert p>0 and drift*sign>0 and correct>.5
            windows.append(dict(ticks=ticks,center=sign*v,half_width=w,p_yes=p,
                p_no=1-p,asymptotic_leading=2*w/np.pi,correct_momentum_sign_fraction=correct,
                other_sign_or_zero_fraction=1-correct,mean_drift_per_tick=drift))
    return dict(localized_packets=rows, finite_apertures=windows)


if __name__ == "__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_directory",type=Path)
    dest=parser.parse_args().output_directory
    dest.mkdir(exist_ok=True,parents=True)
    result=dict(encoding="i^x exp(-i pi t/4)(R+iL). Fold q into [-pi/2,pi/2).",
                exact=[exact_trace(s) for s in (0,1)],
                spectral=spectral_checks(),preparations=signed_packet_and_filter())
    (dest/"folded_free_field.json").write_bytes((json.dumps(result,indent=2)+"\n").encode())
    print("Verified the local signed rule, folded bounds and opposite free packet/window drifts.")
