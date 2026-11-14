"""Run python -B check_four_tick_force.py OUTPUT_DIRECTORY (NumPy).

Check integer matched rotation and idle cells, exact norm through two blocks,
loss of the signed interference if every plate path is permanently tagged,
the common-depth binary sum-of-two-squares obstruction through depth 16,
and the four-tick field phase against the forced continuum characteristic.
Keep every signed force, parity, scale and block observation specified below.
"""
import argparse
from fractions import Fraction
import json
import math
from pathlib import Path

import numpy as np

from check_folded_free_field import PeriodicWalk, add, mul
from check_rational_bypass import walsh


def gauss_power(z, exponent):
    acc = (1,0)
    while exponent:
        if exponent%2:
            acc = mul(acc,z)
        z = mul(z,z)
        exponent //= 2
    return acc


def integer_cells():
    # These two parent-local input columns are kept coherent down to the
    # same named terminal rails; the idle padding also has 25 paths per input.
    def column(a,b):
        entries = [(0,1 if a>0 else -1)]*abs(a)+[(1,1 if b>0 else -1)]*abs(b)
        return entries+[(0,1),(0,-1)]*((25-len(entries))//2)
    cells = {}
    for name,u,v in (("positive",3,4),("negative",3,-4),("idle",5,0)):
        cols = [column(u,v),column(-v,u)]
        raw = [[sum(sign for rail,sign in col if rail==output) for col in cols] for output in (0,1)]
        assert all(len(col)==25 for col in cols)
        assert raw==[[u,-v],[v,u]] and u*u+v*v==25
        cells[name] = dict(raw=raw, path_counts=[[sum(r==rail for r,_ in col) for rail in (0,1)] for col in cols])
    # Matched integer scales while positions are signed and cross zero.
    B=11
    state = {-2:(2,-1),0:(1,3),2:(-2,2)}
    norm0 = sum(a*a+b*b for a,b in state.values())
    scale=1
    records=[]
    for block in (1,2):
        after={}
        for x,z in state.items():
            assert abs(x)<=B
            rotor=gauss_power((3,-4 if x>=0 else 4),abs(x))
            after[x]=mul(z, (rotor[0]*5**(B-abs(x)),rotor[1]*5**(B-abs(x))))
        scale *= 5**B
        for _ in range(4):
            state={}
            for x,(r,l) in after.items():
                state[x+1]=add(state.get(x+1,(0,0)),(r+l,0))
                state[x-1]=add(state.get(x-1,(0,0)),(0,r-l))
            after=state
        scale *= 4
        norm=sum(a*a+b*b for a,b in state.values())
        assert norm==norm0*scale**2
        records.append(dict(block=block,scale=scale,raw=sorted(state.items()),norm=norm))
    obstruction = []
    for depth in range(17):
        den=2**depth
        sols=[(a,math.isqrt(den-a*a)) for a in range(math.isqrt(den)+1)
              if math.isqrt(den-a*a)**2==den-a*a]
        assert all(a*b==0 if depth%2==0 else a==b for a,b in sols)
        obstruction.append(dict(depth=depth,nonnegative_solutions=sols))
    return dict(columns=cells, distinguished_path_control=Fraction(cells["positive"]["path_counts"][0][0],25),
                coherent_R_return=Fraction(9,25), exact_norm_rows=records, binary_solutions=obstruction)


def compilation_trial():
    # An explicit finite-cone tolerance example, retaining the true compiler depth.
    h=.032
    B=12
    blocks=3
    budget=.005
    w=complex(3,4)/5
    k=0
    u=1+0j
    while abs(u-np.exp(-1j*h))>budget/B:
        k+=1
        u*=w
        if k==1_000_000:
            raise RuntimeError("no compiler witness in the predeclared search")
    errors=[abs(u**x-np.exp(-1j*h*x)) for x in range(-B,B+1)]
    assert max(errors)<=budget
    return dict(slope=h, cone=B, per_plate_budget=budget, power=k, padded_primitive_calls=k*B,
                site_errors=errors, three_plate_bound=blocks*max(errors))


def binary_selector():
    # Pythagorean columns include two signs, an idle site and a true quarter turn.
    rows = []
    for D, columns in ((5,[(3,4),(3,-4),(5,0),(0,-5)]),
                       (13,[(-12,5),(5,-12),(13,0),(0,13)])):
        K=1
        while K*K < 8*D*D:
            K*=2
        assert K*K < 32*D*D
        tables=[]
        for a,b in columns:
            assert a*a+b*b==D*D
            table=[(1 if a>=0 else -1,0)]*(2*abs(a))
            table += [(0,1 if b>=0 else -1)]*(2*abs(b))
            table += [(1,0),(-1,0)]*((K-len(table))//2)
            assert len(table)==K
            tables.append(table)

        def transform(state, reverse=False):
            state=state.copy()
            walsh(state,K)
            for x,table in enumerate(tables):
                for j,(c,s) in enumerate(table):
                    u=(2*x)*K+j
                    state[u],state[u+K]=mul((c,-s if reverse else s),
                                           (state[u],state[u+K]))
            walsh(state,K)
            return state

        raw=[2,-1,-3,4,1,2,3,-2]
        start=[0]*(len(raw)*K)
        start[::K]=raw
        full=transform(start)
        rotated=[v for x,(a,b) in enumerate(columns) for v in mul((2*a,2*b),raw[2*x:2*x+2])]
        assert full[::K]==rotated
        assert transform(full,True)==[K*K*v for v in start]
        mass=sum(v*v for v in start)
        p=Fraction(4*D*D,K*K)
        assert Fraction(1,8)<p<=Fraction(1,2)
        assert sum(v*v for v in full)==K*K*mass
        # Read only zero/nonzero. Resolve neither the site nor individual failure addresses.
        fail=full.copy()
        fail[::K]=[0]*len(raw)
        recovered=transform(fail,True)
        reset=recovered.copy()
        reset[::K]=[0]*len(raw)
        clear=[v-r for v,r in zip(recovered,reset)]
        retry_mass=0
        for branch in (clear,reset):
            repaired=transform(branch)
            accepted=repaired[::K]
            pivot=next(i for i,v in enumerate(rotated) if v)
            assert accepted[pivot]!=0 and all(u*rotated[pivot]==v*accepted[pivot]
                                               for u,v in zip(accepted,rotated))
            retry_mass+=sum(v*v for v in accepted)
        assert Fraction(retry_mass,mass*K**6)==(1-p)*2*p*(1-p)
        rows.append(dict(D=D,K=K,columns=columns,source=raw,raw_accepted=rotated,
                         index_zero_probability=p,nonzero_probability=1-p,
                         joint_retry_success=Fraction(retry_mass,mass*K**6),
                         unconditioned_index_scores=[sum(v*v for v in full[j::K]) for j in range(K)],
                         joint_denominator=mass*K*K))
    return rows


def trial(N,F,s):
    grid=PeriodicWalk(N)
    delta=(2*np.pi/(4*N))**(1/3)
    dt=4*delta**2
    blocks=max(1,round(.8/dt))
    P=.85
    # Two folded Fourier replicas are required for one occupied parity.
    p=grid.q/delta
    profile=np.maximum(0,1-(p/P)**2)**3*np.exp(1j*(.4*p+.13*p*p))
    primary=(grid.k>=-np.pi/2)&(grid.k<np.pi/2)
    profile=np.where(primary,profile,(-1)**s*profile)
    initial=np.fft.ifft(profile)
    initial/=np.linalg.norm(initial)
    initial_fft=np.fft.fft(initial)
    rails=grid.decode(initial,0)
    h=F*4*delta**3
    plate=np.exp(-1j*h*grid.x)
    split=initial_fft.copy()
    rows=[]
    for j in range(1,blocks+1):
        z=(rails[:,0]+1j*rails[:,1])*plate
        rails=grid.direct(np.column_stack((z.real,z.imag)),4)
        observed=grid.encode(rails,4*j)
        # h is exactly F grid units; multiplication by exp(-ihx)
        # maps the input q to q-h before the four free ticks.
        split=np.roll(split,-F)*np.exp(-2j*grid.q**2)
        T=j*dt
        L=P+abs(F)*T
        Q=delta*L
        assert Q<1
        phase=T*p*p/2-F*T*T*p/2+F*F*T**3/6
        exact=np.fft.ifft(np.roll(initial_fft*np.exp(-1j*phase),-F*j))
        splitfield=np.fft.ifft(split)
        pure_error=float(np.linalg.norm(observed-splitfield))
        quad_error=float(np.linalg.norm(splitfield-exact))
        error=float(np.linalg.norm(observed-exact))
        free_bound=j*(4*np.sqrt(2)*Q**3+2*Q**4/3)
        quad_bound=T*dt*abs(F)*L/2
        assert pure_error<=free_bound+2e-12 and quad_error<=quad_bound+2e-12
        assert error<=free_bound+quad_bound+2e-12
        assert abs(np.linalg.norm(observed)-1)<2e-12
        bare_p=np.sum(abs(initial_fft)**2*p)/sum(abs(initial_fft)**2)
        out_fft=np.fft.fft(observed)
        mean_p=float(np.sum(abs(out_fft)**2*p)/sum(abs(out_fft)**2))
        rows.append(dict(block=j,T=T,Q=Q,field_error=error,free_error=pure_error,
                    quadrature_error=quad_error,free_bound=free_bound,
                    quadrature_bound=quad_bound,measured_folded_mean_p=mean_p,
                    reference_mean_p=float(bare_p-F*T),
                    mass_outside_reference_cut=grid.energy(observed,abs(grid.q)>Q)))
    return dict(N=N,force_slope=F,origin_parity=s,delta=delta,blocks=blocks,
                tick_units="epsilon=1, four native ticks per block",rows=rows)


def main():
    return dict(integer=integer_cells(), compiler=compilation_trial(),binary_selector=binary_selector(),
                numerical=[trial(N,F,s) for N in (256,512,1024,2048,4096)
                           for F in (-1,0,1) for s in (0,1)],
                scope="Numerical Fourier-grid tests are commensurate periodic instances. "
                      "The analytic continuum result concerns the line; a finite cone is needed for an exact integer compiler.")


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_directory",type=Path)
    dest=parser.parse_args().output_directory
    data=main()
    dest.mkdir(parents=True,exist_ok=True)
    (dest/"four_tick_force.json").write_bytes((json.dumps(data,default=str,indent=1)+"\n").encode())
    print("Verified matched integer cells, two exact flights and all periodic four-tick trial rows.")
