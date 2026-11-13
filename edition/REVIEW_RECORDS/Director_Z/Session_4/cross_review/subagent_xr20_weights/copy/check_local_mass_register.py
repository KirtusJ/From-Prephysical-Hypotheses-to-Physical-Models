"""Check a bounded-speed base and cyclic mass register with a uniform external field.

Usage: python -B check_local_mass_register.py OUTPUT_DIRECTORY (NumPy required).
Signed-sheet coordinates and scalar/vector force gauges use the same real H,H
coin. Only site/rail records commute with the final change of force gauge.
"""

import argparse
import json
import math
from collections import Counter
from fractions import Fraction
from pathlib import Path

import numpy as np


def round_nearest(x):
    """Round half up, with an exact rational error of at most one half."""
    return (2*x.numerator + x.denominator) // (2*x.denominator)


def control(tick, force, tau, c=1, mu=1):
    # h/theta = f*c*tau/mu; no run-time force or particle coordinates enter.
    def target(j):
        return force*c*tau*j*(j+1)/(2*mu)
    Q = round_nearest(target(tick))
    stride = Q - round_nearest(target(tick-1))
    assert abs(Q-target(tick)) <= Fraction(1,2)
    assert abs(stride) <= abs(force*c*tau*tick/mu) + 1
    return stride, Q-target(tick)


def real_h(state):
    out=Counter()
    for (x,y,d),v in state.items():
        out[x,y,1]+=v
        out[x,y,-1]+=d*v
    return out


def local_tick(state, order, q):
    """One mass stroke, |q| vector strokes, and one spatial stroke, all unit."""
    a=real_h(state)
    a={(x,(y+d)%order,d):v for (x,y,d),v in a.items()}
    a=real_h(a)
    sign = 1 if q>0 else -1
    for _ in range(abs(q)):
        a={(x,(y-d*sign)%order,d):v for (x,y,d),v in a.items()}
    return {(x+d,y,d):v for (x,y,d),v in a.items()}


def projection(a, order, s, n):
    out=Counter()
    for (x,y,d),v in a.items():
        out[x,d]+=v*np.exp(-2j*math.pi*(s*y % order)/order)/(math.sqrt(2)*2**n)
    return out


def site_distance(y,order):
    return min(y,order-y)


def small_sheet():
    rows=[]
    for order in (7,8,13,20):
        smax=4
        for force in (Fraction(-3,2),Fraction(0),Fraction(3,2)):
            base={(0,0,1):1,(0,0,-1):1}
            psi={s:{(0,1):1/math.sqrt(2),(0,-1):1/math.sqrt(2)}
                 for s in (1,-1,smax)}
            largest=0.
            settings=[]
            for j in range(1,10):
                q,e=control(j,force,Fraction(1,10));settings.append(q)
                base=local_tick(base,order,q)
                assert sum(v*v for v in base.values())==2*4**j
                assert all(abs(x)<=j and site_distance(y,order)<=j+sum(map(abs,settings))
                           for (x,y,d), v in base.items() if v)
                for s in psi:
                    ang=math.tau*s/order
                    a=Counter()
                    for (x,d),v in psi[s].items():
                        for p in (-1,1):
                            a[x+p,p]+=v*(math.cos(ang) if p==d else -1j*math.sin(ang))*np.exp(1j*p*q*ang)
                    psi[s]=a
                    literal=projection(base,order,s,j)
                    largest=max(largest,max(abs(literal.get(k,0)-a.get(k,0)) for k in literal.keys()|a.keys()))
                assert all(abs(psi[1].get(k,0)-psi[-1].get(k,0).conjugate())<2e-12 for k in psi[1].keys()|psi[-1].keys())
            assert largest<2e-12
            rows.append(dict(M=order,force=str(force),strides=settings,all_paths_base_and_sheet_cone=True,
                             signed_integer_final_norm=sum(v*v for v in base.values()),
                             maximum_fibre_discrepancy=largest))
    return rows


def coin(spin,theta):
    a,b=spin
    C,S=math.cos(theta),-1j*math.sin(theta)
    return C*a+S*b,S*a+C*b


def stream(spin,k):
    v=np.exp(-1j*k)
    return spin[0]*v,spin[1]*np.conj(v)


def finite_flight(K,force,s):
    # Exact tau, exact angle theta=2π/M. Units c=mu=1, epsilon=tau/theta.
    tau=Fraction(1,8*8**K)
    M=50*4**K
    theta=math.tau/M; eps=float(tau)/theta
    T=Fraction(1,2); ticks=int(T/tau)
    h=theta*float(force*tau)
    step=float(tau)
    # Occupied Fourier sites of a periodized line envelope in the vector frame.
    length=16
    n=round(length/step)
    freq=math.tau*np.fft.fftfreq(n)
    p=eps*freq/step
    width=math.sqrt(eps)
    mask=np.abs(p)<width
    k=freq[mask]
    amp=(1-(p[mask]/width)**2)**3
    amp/=np.linalg.norm(amp)
    initial=(amp/math.sqrt(2),amp/math.sqrt(2))
    actual=initial; ideal=initial; naive=initial
    max_stride=0;max_r=0.;max_actual=0.;max_compensated=0.
    for j in range(1,ticks+1):
        q,res=control(j,force,tau)
        rnd=round_nearest(force*tau*j)
        max_stride=max(max_stride,abs(q));max_r=max(max_r,abs(float(res)))
        actual=stream(coin(actual,s*theta),k-s*q*theta)
        ideal=stream(coin(ideal,s*theta),k-s*j*h)
        naive=stream(coin(naive,s*theta),k-s*rnd*theta)
        delta=s*theta*float(res)
        adjusted=stream(actual,delta)
        err=float(np.linalg.norm(np.asarray(actual)-ideal))
        err2=float(np.linalg.norm(np.asarray(adjusted)-ideal))
        max_actual=max(max_actual,err);max_compensated=max(max_compensated,err2)
        step_bound=2*abs(math.sin(s*theta))*math.sin(theta/2)*j
        assert err2<=step_bound+3e-12 and err<=theta/2+step_bound+3e-12
    Y=np.fft.fftfreq(n)*length
    xi=math.tau*2/length
    def read(spin):
        z=np.zeros((2,n),complex);z[:,mask]=spin
        v=np.fft.ifft(z,axis=1,norm="ortho");w=np.sum(abs(v)**2,axis=0)
        assert abs(sum(w)-1)<5e-12
        f=np.dot(w,np.exp(1j*xi*Y))
        return [float(f.real),float(f.imag)]
    tr=float(T)
    F=float(force)
    # λ=sgn(s) selects the positive spin-X edge in the mass frame. Here |s|=1.
    ray=-F*tr**2/(1+math.hypot(1,F*tr))
    probabilities=read(actual),read(ideal),read(naive)
    drift=lambda z:abs(complex(*z)-np.exp(1j*xi*ray))
    return dict(K=K,M=M,epsilon=eps,tau=str(tau),ticks=ticks,force=str(force),sector=s,
                phi_per_tick=theta,desired_force_phase_per_tick=h,highest_register_stride=max_stride,
                largest_prefix_rounding_error_in_strokes=max_r,support_modes=len(k),
                max_spinor_error=max_actual,max_corrected_spinor_error=max_compensated,
                final_uniform_bound=theta/2+2*ticks*abs(math.sin(theta))*math.sin(theta/2),
                ideal_continuum_position=ray,physical_position_harmonic=xi,
                bounded_position_records=dict(actual=probabilities[0],unrounded=probabilities[1],naive=probabilities[2]),
                position_harmonic_distance_from_ray=[drift(z) for z in probabilities],
                sheet_pitch_if_each_edge_has_speed_one=float(tau)/(2+max_stride),
                sheet_circumference_at_that_pitch=M*float(tau)/(2+max_stride))


def raw_gauge():
    # Physical force at site x compared with exact vector phase; initial spin
    # occupies both spatial parities so this is not a parity-only identity.
    length=41;tau=1/20;theta=math.tau/32
    x=np.arange(length)-length//2
    rows=[]
    for s in (1,-1):
        for f in (-1,0,2):
            h=s*f*tau*theta
            start=np.zeros((2,length),complex)
            start[:,length//2]=np.array([2.,1j])/math.sqrt(7)
            start[1,length//2-1]=-1/math.sqrt(7)
            start[0,length//2+2]=1/math.sqrt(7)
            scalar=start.copy(); vector=start.copy();worst=0.
            for j in range(1,9):
                u,v=coin(scalar*np.exp(-1j*h*x),s*theta)
                scalar=np.stack((np.roll(u,1),np.roll(v,-1)))
                u,v=coin(vector,s*theta)
                vector=np.stack((np.roll(u,1)*np.exp(1j*j*h),np.roll(v,-1)*np.exp(-1j*j*h)))
                corrected=vector*np.exp(-1j*j*h*x)
                worst=max(worst,float(np.linalg.norm(corrected-scalar)))
            assert worst<3e-12
            rows.append(dict(s=s,f=f,full_spinor_residual_after_gauge=worst,
                             uncorrected_spinor_distance=float(np.linalg.norm(vector-scalar))))
    return rows


def integer_clock():
    # Nearest cumulative triangular numbers have an exact local schedule for
    # f*c*tau/mu=A/B. This controller doubles its denominator to round ties up.
    out=[]
    for ratio in (Fraction(-3,7),Fraction(1,9),Fraction(3,10),Fraction(0)):
        den=ratio.denominator
        num=ratio.numerator
        phase=den  # remainder for A_0+1/2
        offset=0
        strides=[]
        for j in range(1,21):
            offset+=2*num
            stride,phase=divmod(phase+offset,2*den)
            Q=round_nearest(ratio*j*(j+1)/2)
            old=round_nearest(ratio*(j-1)*j/2)
            assert stride==Q-old
            assert 0<=phase<2*den
            strides.append(stride)
        out.append(dict(slope=str(ratio),tick_count=len(strides),strides=strides,
                        final_remainder=phase,integer_offset=offset,denominator_doubled=2*den))
    return out


def reference_lower_cost():
    # Every real vector in the selected cos/sin plane is invisible to the
    # quadrature index orientation. In a short arc A, maximal possible plane
    # mass from any normalized vector supported on A equals lambda_max of
    # its 2x2 restricted projector Gram matrix.
    rows=[]
    for M in (17,32,63,128):
        for size in (1,M//8,M//4,M//2,M):
            idx=np.arange(size)
            basis=np.vstack((np.cos(math.tau*idx/M),np.sin(math.tau*idx/M)))*math.sqrt(2/M)
            max_mass=float(np.linalg.eigvalsh(basis@basis.T)[-1])
            trace_bound=min(1.,2*size/M)
            assert max_mass<=trace_bound+2e-14
            if size==M:
                assert abs(max_mass-1)<2e-14
            rows.append(dict(M=M,occupied_consecutive_sheet_sites=size,
                             maximum_target_pair_mass=max_mass,rank_two_trace_ceiling=trace_bound))
    return rows


def main(out):
    flights=[finite_flight(k,f,s) for k in (1,2,3)
             for f,s in ((Fraction(1,2),1),(Fraction(1,2),-1),(Fraction(-1,2),1),
                         (Fraction(0),1),(Fraction(3),1))]
    for j in range(0,len(flights),5):
        a,b=flights[j:j+2]
        assert np.max(np.abs(np.array(a['bounded_position_records']['actual'])-
                             b['bounded_position_records']['actual']))<2e-12
    result=dict(protocol="At each flight tick, H, a unit rail-controlled mass translation, H, "
                "a programmed compensating unit-stroke sequence on the same ring, and one site stream. "
                "Use C_s=exp(-i*s*theta*sigma_x) in the mass frame. Real H at launch prepares +X. "
                "Native position and rail reads ignore the diagonal change of spin and force frames.",
                hardware="Two-dimensional cylinder (x,y) with a finite rail, nearest-neighbour base +/-1 and local sheet ±1 permutations; local H and real signed readout. "
                "At horizon T, force vector stride bound Qmax=ceil(|f|cT/mu)+1. Allocate subslots, including padding for different q. "
                "If base pitch is c*tau, retain base speed c per full tick. When moves occupy distinct clock subslots the strict microstep propagation bound is larger by a FIXED factor; "
                "to use a single speed cap v include fixed subslot overhead or allow simultaneous base/sheet shifts with bounded product-metric velocity. "
                "Site placement, a distinct physical sheet coordinate per local base mode, joint phase preparation and synchronized translated programs are required. "
                "Ring circumference at sheet pitch O(tau) is O(epsilon); a fixed circumference has a different physical resource cost.",
                comparison="The scalar uniform force and the exact vector representation agree up to exp(-i*n*h*x) at the output. "
                "Between the rounded and exact vector flights, pending z rotation s*theta*(Q_n-h*n(n+1)/(2*theta)) cancels the incremental vector-phase discrepancy. "
                "Conjugating the small mass coin by the pending phase costs <=2*abs(sin(s*theta)*sin(r)). "
                "For |s|=1 the uniform operator norm error is <=theta/2+2*n*abs(sin(theta))*sin(theta/2); tau=o(epsilon²) suffices. "
                "Per-tick rounding without accumulating the phase remainder need not converge; small force max |f|T<mu/(2c) rounds every desired stroke to zero.",
                limitations="The selected character pair is an input, and a localized physical sheet does not have this purity. "
                "Uniform field is preprogrammed as a common time-dependent local phase; scalar-force address transport, an unknown remote force source, spin tomography in a fixed transverse basis, and nonlocal spatial-coherence reads are distinct tasks. "
                "Finite M and bounded transfer O(1) strokes require a specifiable finite field range and horizon or new clock controls.",
                finite_controller=integer_clock(),initial_sheet_arc_controls=reference_lower_cost(),
                resource_counts="For physical base interval of width L_x, about (L_x/(c*tau))*M cylinder sites carry the rails. "
                "Given a rational h/theta, exact integer schedules can be preloaded identically at each base site or generated with a clock and remainder. "
                "Counter bit operations are not instantaneous nearest-neighbour primitives: a table of O(T/tau) settings, or a clockwork and its cycle time, is a supplied resource. "
                "The real folded character projector has diagonal 2/M, so a sheet state supported on A sites has pair mass at most 2*A/M even with unresolved ancillas. "
                "A bounded-speed preparation from one site needs order M*sheet_pitch time for near purity; this is a lower bound and not a construction from only synchronized Hadamards.",
                literal=small_sheet(),scalar_vector=raw_gauge(),flights=flights)
    out.mkdir(parents=True,exist_ok=True)
    (out/"local_mass_register.json").write_bytes((json.dumps(result,indent=2,allow_nan=False)+"\n").encode())


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_directory",type=Path)
    main(parser.parse_args().output_directory)

