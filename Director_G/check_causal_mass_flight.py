"""Finite-speed split Dirac flight with a real coin, an external uniform force and a prepared sheet.

Run python -B check_causal_mass_flight.py OUTPUT_DIRECTORY (NumPy required).
The exact endpoint cone, finite approximate position measurements and maintained
complex phases are compared in independent position/momentum representations.
"""

import argparse
import json
import math
from fractions import Fraction
from pathlib import Path

import numpy as np


def edge_spinor(branch):
    return np.array([1, 1j * branch]) / math.sqrt(2)


def eigenvectors(p, branch, c, mu):
    # H(p) is X-rotation of mu*Y with length E(p). This gauge is parallel.
    beta = np.arctan(c * p / mu) / 2
    v = edge_spinor(branch)
    return np.cos(beta)[:, None] * v - 1j * np.sin(beta)[:, None] * v[::-1]


def energy(p, c, mu):
    return np.hypot(c*p, mu)


def action(p, field, t, c, mu):
    if field == 0:
        return t * energy(p, c, mu)
    def primitive(x):
        return (x * energy(x, c, mu) + mu**2/c * np.arcsinh(c*x/mu)) / 2
    return (primitive(p) - primitive(p - field*t)) / field


def fit_trajectory(field, branch, t, m, c):
    ratio = field*t/(m*c)
    newton = -branch * field*t*t/(2*m)
    exact = -branch * field*t*t/(m*(1+math.hypot(1,ratio)))
    correction = abs(field)**3*t**4/(8*m**3*c**2)
    assert abs(exact-newton) <= correction + 1e-15
    assert abs(exact) <= c*t + 1e-15
    return exact, newton, correction


def on_grid(eps, tau, n, p0, field, branch, spin_source, m=1., c=1.):
    """Periodized compact momentum packet; position detector is the first circle harmonic."""
    a = c*tau
    theta = m*c*c*tau/eps
    mu = m*c*c
    width = math.sqrt(eps)
    k = 2*math.pi*np.fft.fftfreq(n)
    p = eps*k/a
    z = (p-p0)/width
    amp = np.maximum(0., 1-z*z)**3
    amp /= np.linalg.norm(amp)
    u = eigenvectors(p, branch, c, mu)
    initial_spin = u if spin_source == "eigenframe" else np.tile(edge_spinor(branch),(n,1))
    preparation_error = float(np.linalg.norm(amp[:,None]*(u-initial_spin)))
    active = amp != 0
    centre = p[active]
    spin = initial_spin[active]*amp[active,None]
    co, si = math.cos(theta), math.sin(theta)
    ticks = round(.5/tau)
    t = ticks*tau
    for j in range(1,ticks+1):
        phase = np.exp(-1j*(centre-j*field*tau)*a/eps)
        r,l = spin[:,0],spin[:,1]
        spin = np.column_stack((phase*(co*r-si*l),np.conj(phase)*(si*r+co*l)))
    ideal = amp[active,None]*eigenvectors(centre-field*t,branch,c,mu)*np.exp(
        -1j*branch*action(centre,field,t,c,mu)/eps)[:,None]
    actual_error = float(np.linalg.norm(spin-ideal))
    bound_p = abs(p0)+width+abs(field)*t
    assert bound_p*a/eps < math.pi
    continuous_error = eps*(abs(field)*c/(2*mu**2) + 7*t*field**2*c**2/(8*mu**3))
    endpoint_error = t*tau*c*abs(field)/(2*eps)
    split_error = t*tau*c*bound_p*mu/eps**2
    bound = preparation_error+continuous_error+endpoint_error+split_error
    assert actual_error <= bound+2e-13

    full = np.zeros((n,2),dtype=complex)
    full[active]=spin
    # Output Fourier components are shifted together by -f*t. Relative grid
    # phases, hence every point probability, are unchanged by ignoring that
    # common real-space modulation during this inverse transform.
    wave = np.fft.ifft(full,axis=0,norm="ortho")
    mass = np.sum(abs(wave)**2,axis=1)
    length=n*a
    xi=2*math.pi/length
    pos=np.fft.fftfreq(n)*length
    char=complex(mass@np.exp(1j*xi*pos))
    ray,newton,newton_bound=fit_trajectory(field,branch,t,m,c)
    if p0:
        # For general initial momentum, integrate v=λE′ along p0-f*t.
        ray=branch*(energy(p0,c,mu)-energy(p0-field*t,c,mu))/field if field else (
            branch*t*c*c*p0/energy(p0,c,mu))
        newton=branch*(p0*t-field*t*t/2)/m
        newton_bound=None
    return dict(epsilon=eps,tau=tau,cell=a,c=c,m=m,length=length,ticks=ticks,t=t,
                field=field,branch=branch,initial_p=p0,source=spin_source,
                momentum_modes=int(np.sum(active)),analytic_ray=float(ray),newton=float(newton),
                newton_error_upper_at_rest=newton_bound,finite_position_character=[char.real,char.imag],
                first_harmonic_distance=float(abs(char-np.exp(1j*xi*ray))),
                total=float(np.sum(mass)),max_spinor_error_bound=bound,observed_spinor_error=actual_error,
                terms=dict(initial_spin=preparation_error,continuum_band=continuous_error,
                           endpoint_time=endpoint_error,split=split_error))


def direct_ports():
    """Update all spatial sites, including the chronological departure phase on each gate."""
    rows=[]
    for n in (64,80):
        for field in (-1.,0.,1.):
            for branch in (-1,1):
                a=tau=1/32; eps=1/4; mu=1.
                theta=mu*tau/eps; h=field*a*tau/eps
                x=np.arange(n)-n//2
                y=np.exp(-1j*h*x)
                phi=np.zeros((n,2),complex)
                # Two starts with unequal amplitudes exercise translation phases.
                phi[n//2]=edge_spinor(branch)*2/math.sqrt(5)
                phi[n//2-2]=edge_spinor(branch)/math.sqrt(5)
                k=2*math.pi*np.fft.fftfreq(n)
                amplitudes=(2+np.exp(2j*k))[:,None]*edge_spinor(branch)/math.sqrt(5*n)
                worst=0.;max_cone=0.;mass_error=0.
                for j in range(1,13):
                    v=phi*y[:,None]
                    r=math.cos(theta)*v[:,0]-math.sin(theta)*v[:,1]
                    l=math.sin(theta)*v[:,0]+math.cos(theta)*v[:,1]
                    phi=np.column_stack((np.roll(r,1),np.roll(l,-1)))
                    phase=np.exp(-1j*(k-j*h))
                    r,l=amplitudes[:,0],amplitudes[:,1]
                    amplitudes=np.column_stack((phase*(math.cos(theta)*r-math.sin(theta)*l),
                                     np.conj(phase)*(math.sin(theta)*r+math.cos(theta)*l)))
                    recovered=np.fft.fftshift(np.fft.ifft(amplitudes,axis=0,norm="ortho"),axes=0)
                    recovered*=np.exp(-1j*j*h*x)[:,None]
                    worst=max(worst,float(np.linalg.norm(phi-recovered)))
                    outside=np.minimum(np.abs(x),np.abs(x+2))>j
                    max_cone=max(max_cone,float(np.max(np.abs(phi[outside]),initial=0)))
                    mass_error=max(mass_error,abs(float(np.sum(np.abs(phi)**2))-1))
                assert max_cone==0 and worst<1e-12 and mass_error<1e-12
                rows.append(dict(sites=n,field=field,branch=branch,steps=12,cone_max=max_cone,
                                 max_full_wave_discrepancy=worst,max_norm_error=mass_error))
    return rows


def dispersion():
    rows=[]
    m=c=1.
    for ratio in (1/4,1/8,1/16,1/32):
        theta=m*c*c*ratio
        for p in (-2,-1,-.25,0,.25,1,2):
            k=c*p*ratio
            omega=math.acos(math.cos(theta)*math.cos(k))
            velocity=c*math.cos(theta)*math.sin(k)/math.sin(omega)
            assert abs(velocity)<=c
            rows.append(dict(tau_over_epsilon=ratio,p=p,energy=omega/ratio,
                             dirac_energy=math.hypot(m*c*c,c*p),velocity=velocity,
                             dirac_velocity=c*c*p/math.hypot(m*c*c,c*p)))
    return rows


def finite_speed_loop():
    # Root orders M=8a² admit an exact quarter when h=2π/M. Choose
    # ε=F c τ²/h and ε→0, τ/ε²→0 via integer dyadic a,τ schedules.
    rows=[]
    for q in (2,3,4,5):
        arm=2**(5*q)
        tau=Fraction(1,2**(6*q)); cell=tau; M=8*arm*arm
        eps_times_pi=4*arm*arm*tau*tau
        time=2*arm*tau; radius=arm*cell
        assert 2*arm*arm*Fraction(1,M)==Fraction(1,4)
        assert time*time==eps_times_pi and radius==time/2
        rows.append(dict(arm=arm,M=M,physical_cell=str(cell),tau=str(tau),epsilon_times_pi=str(eps_times_pi),
                         relative_phase_turns="1/4",continuum_speed=1,prep_time=str(time),
                         radius=str(radius),tau_over_epsilon_squared_times_inverse_pi_squared=
                         str(tau/eps_times_pi**2)))
    return rows


def main(out):
    flights=[]
    # τ=ε³/8 and L=96: the classical field is a smooth local function on
    # the covering line, while the finite momentum grid periodizes the packet.
    # Momentum samples of U are computed only on the occupied compact support.
    for eps in (.5,.25,.125):
        tau=eps**3/8
        size=round(96/tau)
        for field,branch in [(1,1),(-1,-1),(-1,1),(3,1),(0,1)]:
            flights.append(on_grid(eps,tau,size,0.,field,branch,"eigenframe"))
        flights.append(on_grid(eps,tau,size,0.,1.,1,"constant_edge"))
    for j in range(0,len(flights),6):
        a,b=flights[j:j+2]
        assert max(abs(q-v) for q,v in zip(a['finite_position_character'],b['finite_position_character']))<2e-12
    assert all(abs(r['total']-1)<3e-12 for r in flights)
    out.mkdir(parents=True,exist_ok=True)
    record=dict(external_hardware="One real onsite tunable rotation R_y(theta)=exp(-i theta sigma_y), nearest-neighbor R/L stream, preassigned uniform force phase at each site on the covering line, squared rail statistics. Fourier-character preparation is an independent resource. No dynamic interparticle force is included.",
        controls="Grouping both position rails after a fixed time; explicit compact momentum-source model on grid, Born normalization, upper/lower energy and conjugate sign settings. Main grid represents a periodicization of the line packet in the accelerating representation; the restored wave on the physical core can carry a time-dependent boundary twist. Independent compact starts have zero cone leakage at every tick.",
        characteristic_oracle="Ideal scalar action exp(-i λ integral of E(p-fs)/epsilon) and a parallel band eigenvector, with all phases retained. The supplied bound is for the full spinor. Uniform nonrelativistic error bound is for a centre launched at rest, at fixed c; it does not tend to zero just by refining the grid.",
        grids=flights,dispersion=dispersion(),spatial_control=direct_ports(),quadrature_routes=finite_speed_loop())
    (out/"causal_mass_flight.json").write_bytes((json.dumps(record,indent=2,allow_nan=False)+"\n").encode())


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_directory",type=Path)
    main(parser.parse_args().output_directory)

