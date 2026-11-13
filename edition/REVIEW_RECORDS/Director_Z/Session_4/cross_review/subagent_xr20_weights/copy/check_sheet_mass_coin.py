"""An onsite coin from balanced signs and cyclic translations, with an explicit base light cone."""
import argparse
import cmath
import json
import math
from collections import defaultdict
from pathlib import Path


def shift_sheet(state, M, base_phase=0, plus=0, minus=0):
    return {(x,d,(y+base_phase*x+(plus if d==1 else minus))%M):v
            for (x,d,y),v in state.items()}


def balanced(state):
    out = defaultdict(int)
    for (x,d,y),v in state.items():
        out[x,1,y] += v
        out[x,-1,y] += d*v
    return {cell:v for cell,v in out.items() if v}


def named_cycle(state, M, stride, force):
    q = M//4
    state = shift_sheet(state,M,base_phase=force)
    state = shift_sheet(state,M,minus=-q)
    state = balanced(state)
    state = shift_sheet(state,M,plus=stride,minus=-stride)
    state = balanced(state)
    state = shift_sheet(state,M,minus=q)
    return {(x+d,d,y):v for (x,d,y),v in state.items()}


def overlap(state, M, k):
    out=defaultdict(complex)
    for (x,d,y),v in state.items():
        out[x,d] += v*cmath.exp(-1j*math.tau*(k*y%M)/M)
    return out


def expected_cycle(state, M, k, stride, force):
    # With z=e^(-i*2*pi*k/M), D=diag(1,z^(M/4)).
    # D exp(-i*angle*X) D†. Do not replace D by a quadrature
    # unless its phase really is ±i on the character being measured.
    out=defaultdict(complex)
    phase=cmath.exp(-1j*math.pi*(k%4)/2)
    angle=math.tau*(k*stride%M)/M
    for (x,d),v in state.items():
        v *= cmath.exp(-1j*math.tau*(force*k*x%M)/M)
        out[x+d,d] += math.cos(angle)*v
        out[x-d,-d] += -1j*math.sin(angle)*(phase if d==1 else phase.conjugate())*v
    return out


def literal_tests():
    cases=[]
    for M in (4,8,12,20,32):
        for j in (0,1,-1,M//4,M//2):
            initial={(0,1,0):1,(0,-1,1):2,(2,-1,M-1):-1}
            state=initial
            sectors={k:overlap(state,M,k) for k in range(M)}
            largest=0.
            cones=[]
            oracles=[]
            for n,force in enumerate((1,-1,0,1),1):
                state=named_cycle(state,M,j,force)
                assert sum(v*v for v in state.values()) == 6*4**n
                assert all(-n<=x<=2+n for x,d,y in state)
                for k in range(M):
                    sectors[k]=expected_cycle(sectors[k],M,k,j,force)
                    observed=overlap(state,M,k)
                    for cell in observed.keys() | sectors[k].keys():
                        residual=abs(observed.get(cell,0)/2**n-sectors[k].get(cell,0))
                        largest=max(largest,residual)
                # Before each R or L output, a one-sided basis launch tests the
                # actual sign. Between the two conjugates the coin is real and equal.
                theta=-math.tau*j/M
                for k in (1,M-1):
                    src={(0,1):1+0j}
                    out=expected_cycle(src,M,k,j,0)
                    assert abs(out[-1,-1]-math.sin(theta))<2e-14
                    assert abs(out[1,1]-math.cos(theta))<2e-14
                cones.append([min(x for x,d,y in state),max(x for x,d,y in state)])
                oracles.append(sum(v*v for v in state.values()))
            assert largest<3e-13
            cases.append(dict(M=M,j=j,sector_count=M,largest_complex_residual=largest,
                              reachable_extent=cones,complete_integer_norms=oracles))
    return cases


def packet_moments(K,tau,c=1.):
    # Probability weights of the exact incoming binomial preparation. It is
    # translated in momentum from ±pi/2 to 0 and pi by an onsite gain.
    eps=2.**-K
    m=2*round((eps/tau**2)/2)
    W=c*tau
    a=round(math.sqrt(math.pi*eps/(4*c*tau**2)))
    return dict(epsilon=eps,tau=tau,spacing=W,force=1,cap_steps=m,
                position_rms=W*m/math.sqrt(2*m-1),
                upper_momentum_rms=math.pi*eps/(2*W*math.sqrt(2*m+2)),
                native_input_preparation_time=2*m*tau,
                pulse_quadrature_duration=2*a*tau,
                pulse_max_physical_radius=a*W,
                pulse_momentum_kick=2*a*tau)


def finite_scaling():
    rows=[]
    # Choose c=m_phys=F=1, exact M=2pi/(h)=2pi*eps/tau²,
    # with M divisible by 4 and j nearest -1/tau.
    for K in range(2,7):
        eps=2.**-K
        for power in (2,3):
            target=eps**power
            M=4*round(math.tau*eps/target**2/4)
            tau=math.sqrt(math.tau*eps/M)
            theta=tau/eps
            h=math.tau/M
            j=-round(theta/h)
            theta_actual=-h*j
            norm_coin=2*abs(math.sin((theta_actual-theta)/2))
            n=int(1/tau)
            assert n*norm_coin<=n*h/2+3e-14
            rows.append(dict(M=M,power=power,stride=j,desired_mass_angle=theta,
                             realized_mass_angle=theta_actual,exact_force_angle=h,
                             accumulated_coin_error_bound=n*norm_coin,
                             quarter_sheet_unit_hops=M//4, **packet_moments(K,tau)))
    return rows


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output",type=Path)
    directory=parser.parse_args().output
    directory.mkdir(parents=True,exist_ok=True)
    result=dict(physical_cycles=literal_tests(),scales=finite_scaling(),
                assumptions="Two normalized onsite Hadamards, conditional cyclic sheet permutations "
                "and the scalar force act between single nearest-site streams. Base propagation "
                "has speed spacing/tau. A conditional shift by M/4 may be nonlocal in a physical "
                "sheet metric. Its clock and any hardware must be accounted for separately.",
                adverse="An even character need not see a real y-axis mass coin. An initial unshifted "
                "DO packet peaks at ±pi/2 rather than near momentum zero, and an arbitrary signed "
                "unknown input need not have its phases correlated with its force orientation.")
    (directory/"sheet_mass_coin.json").write_bytes((json.dumps(result,indent=2)+"\n").encode())
