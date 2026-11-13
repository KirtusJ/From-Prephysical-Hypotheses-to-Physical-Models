"""Prepare rail quadrature with two signed-walk excursions and propagate the base packet."""
import argparse
import json
import math
from collections import defaultdict
from fractions import Fraction
from itertools import product
from pathlib import Path

import numpy as np

from check_walk import positive_eigenvector


def routed_step(state, gate, modulus, field=1):
    result = defaultdict(int)
    for (x, rail, y), value in state.items():
        outgoing = (-1, 1) if gate == "H" else (rail if gate == "I" else -rail,)
        for d in outgoing:
            sign = -1 if gate == "H" and d == rail == -1 else 1
            result[x+d, d, (y+field*x) % modulus] += sign * value
    return {cell: value for cell, value in result.items() if value}


def actual_routes():
    rows = []
    # Spread in the base, signs at several addresses and both input directions.
    initial = {(-3,1,3):2, (0,1,1):-3, (4,1,0):1, (0,-1,2):1, (4,-1,1):-1}
    for modulus in (3, 4, 5, 8, 13, 23):
        for a in (1, 2, 3, 7, 12):
            state = initial
            for gate in ["H"] + ["I"]*(a-1) + ["X"] + ["I"]*(a-1):
                state = routed_step(state, gate, modulus)
            wanted = defaultdict(int)
            for (x, c, y), value in initial.items():
                for d in (-1, 1):
                    # Initial R -> both first rails positive. Initial L flips
                    # the sign of the outgoing L, which returns on the R rail.
                    sign = -1 if c == -1 and d == 1 else 1
                    dest = (x, d, (y + 2*a*x - d*a*a) % modulus)
                    wanted[dest] += sign*value
            wanted = {cell: value for cell, value in wanted.items() if value}
            assert state == wanted
            assert sum(z*z for z in state.values()) == 2*sum(z*z for z in initial.values())
            rows.append(dict(M=modulus, a=a, unscaled_final_norm=sum(z*z for z in state.values()),
                             complete_output=[[*cell,v] for cell,v in sorted(state.items())]))
    return rows


def compensated_routes():
    # 4b streamed steps, a turn at 2b, and two sign changes of the field.
    rows = []
    for b in (1, 2, 3, 7):
        for modulus in (5, 13, 32, 101):
            initial = {(x,1,y):v for x,y,v in [(-3,0,1),(1,2,-1),(5,3,2)]}
            state = initial
            for t in range(4*b):
                gate = "H" if t == 0 else ("X" if t == 2*b else "I")
                state = routed_step(state, gate, modulus, 1 if b <= t < 3*b else -1)
            expected = {(x,rail,(y-rail*2*b*b)%modulus):v
                        for (x,_,y),v in initial.items() for rail in (-1,1)}
            assert state == expected
            rows.append(dict(M=modulus,b=b,gain_difference=4*b*b,
                             complete_output=[[*cell,v] for cell,v in sorted(state.items())]))
    return rows


def area_extrema():
    rows = []
    for a in range(1, 8):
        areas = {-1: set(), 1: set()}
        for word in product((-1, 1), repeat=2*a):
            if sum(word):
                continue
            x = y = 0
            for d in word:
                y += x
                x += d
            areas[d].add(y)
        gaps = {p-q for p in areas[-1] for q in areas[1]}
        assert max(gaps) == 2*a*a and min(areas[1]) == -a*a and max(areas[-1]) == a*a
        rows.append(dict(a=a, last_L=sorted(areas[-1]), last_R=sorted(areas[1]),
                         attainable_oriented_gaps=sorted(gaps)))
    return rows


def run_flight(order, sign, mode, T=1.5, reference_scale=1, flight_scale=1, detector=1):
    h0 = math.tau/order
    delta = h0**0.25
    h = sign*h0
    reference_h = h*reference_scale
    flight_h = h*flight_scale
    m = 2*max(1, round(0.5*delta**-2.5))
    n = round(T/delta**3)
    a = max(1, round(math.sqrt(math.pi/(4*h0))))
    depth = 0 if mode == "no_loop" else a
    if mode == "zero_drift":
        depth = 2*max(1,round(math.sqrt(math.pi/(8*h0))))
    pulse_area = depth**2//2 if mode == "zero_drift" else depth**2
    pulse_shift = 0 if mode == "zero_drift" else 2*depth*reference_h
    # Even alternating blocks finish with field sign minus and a R rail.
    # After the loop, A_out(k)=A_alt(k+2ah); A_alt(k)=A_zero(k-h)
    # up to a global phase. The wave is real apart from linear phases.
    size = 1 << (2*(m+n+2)).bit_length()
    freq = math.tau*np.fft.fftfreq(size)
    amp = np.abs(np.sin(freq + pulse_shift - h))**m
    amp /= np.linalg.norm(amp)
    phase = np.exp(-2j*reference_h*pulse_area)
    if mode == "no_loop":
        inputs = [(1., (1., 0.))]
    elif mode == "tagged":
        inputs = [(.5, (1., 0.)), (.5, (0., 1.))]
    else:
        inputs = [(1., (1/math.sqrt(2), phase/math.sqrt(2)))]
    Y = np.fft.fftfreq(size)*size*delta**2
    total = np.zeros(size)
    target_band_mass = 0.
    u = positive_eigenvector(freq)
    # Follow curvature sign b=sign(h_ref) at -pi/2, complement at +pi/2.
    target_plus = np.sin(freq)*np.sign(reference_h) < 0
    chart_boundary = np.zeros(size, dtype=bool)
    chart_boundary[[0, size//2]] = True
    for weight, rail in inputs:
        spin = amp[:,None]*np.asarray(rail, dtype=complex)[None,:]
        pplus = np.abs(np.sum(np.conj(u)*spin,axis=1))**2
        band_weight = np.where(target_plus,pplus,amp*amp-pplus)
        # These two grid points are equidistant from the two dispersion edges.
        # Split their diagnostic weight equally and record its full size.
        band_weight[chart_boundary] = amp[chart_boundary]**2/2
        target_band_mass += weight*float(np.sum(band_weight))
        for j in range(1,n+1):
            momentum = freq-j*flight_h
            left, right = spin[:,0], spin[:,1]
            spin = np.column_stack([(left+right)*np.exp(-1j*momentum),
                                    (left-right)*np.exp(1j*momentum)])/math.sqrt(2)
        wave = np.fft.ifft(spin,axis=0,norm="ortho")
        total += weight*np.sum(np.abs(wave)**2,axis=1)
    assert abs(sum(total)-1) < 3e-12
    t = n*delta**3
    target = -np.sign(reference_h)*sign*flight_scale*t*t/2
    return dict(M=order, sign=sign, mode=mode, delta=delta, m=m, a=depth, n=n,
                reference_scale=reference_scale, flight_scale=flight_scale,
                time=t, angular_error=2*abs(reference_h)*pulse_area-math.pi/2,
                loop_duration=2*depth*delta**3, maximum_relative_excursion=depth*delta**2,
                scaled_momentum_shift=-pulse_shift/delta, target_curvature_mass=target_band_mass,
                chart_boundary_mass=float(np.sum(amp[chart_boundary]**2)),
                prediction=target, mean=float(Y@total), rms_from_ray=float(np.sqrt(((Y-target)**2)@total)),
                negative_half_mass=float(np.sum(total[Y<0])), origin_mass=float(total[0]),
                bounded_characteristic={"xi":detector, "real":float(total@np.cos(detector*Y)),
                                       "imag":float(total@np.sin(detector*Y))},
                total=float(np.sum(total)))


def main(directory):
    flights = [run_flight(M,s,label) for M in (111,128,307,512,2048,8192,32768)
               for label in ("closed_loop","zero_drift","no_loop","tagged") for s in (-1,1)]
    for left,right in zip(flights[::2],flights[1::2],strict=True):
        for ky in ("negative_half_mass","mean","rms_from_ray","target_curvature_mass","origin_mass"):
            assert abs(left[ky]-right[ky]) < 1e-10
    # M=8 a^2 gives an exact quarter period for the relative trajectories at a=1.
    assert Fraction(2*1**2,8)==Fraction(1,4)
    controls = [run_flight(2048, 1, "closed_loop", reference_scale=r, flight_scale=f)
                for r,f in ((1,1),(1,-1),(-1,-1),(1,0),(1,3),(3,3))]
    assert controls[0]["mean"] < 0 < controls[1]["mean"]
    assert controls[2]["mean"] < 0 and controls[-1]["mean"] > 0
    result = dict(convention="Incoming R, relative phase L/R=exp(-2i h a^2), "
                  "field on departure exp(-i h x), U(k)=diag(exp(-ik),exp(ik)) H. "
                  "Each half uses the stream every tick; H, I, X are supplied controls. "
                  "Initial base width comes from an even, alternating-sign direction-only herald. "
                  "Flight clock excludes herald and loop; table reports loop time and excursion.",
                  route_rows=actual_routes(), compensated_routes=compensated_routes(),
                  all_return_area_rows=area_extrema(),
                  cases=flights, reference_and_flight_controls=controls,
                  first_chart_diagnostic="At M=111 an initial tie assignment at k=0,pi made "
                  "the curvature-mass diagnostic differ by 1.274700520692562e-7 between conjugates. "
                  "All physical position summaries agreed. Both dispersion-chart boundaries are "
                  "now shared equally and their total mass is reported for every case.",
                  control_target="The prediction field is the single ideal ray if curvature sign equals "
                  "sign(h_ref) at -pi/2. The last r=f=3 mistuning deliberately prepares its opposite.",
                  controls="No loop leaves a single rail with both curvatures. "
                  "Tagged loop retains orthogonal labels, so no rail coherence survives a tag-blind read. "
                  "All initial base/coin modes are retained in physical route checks. Conditional FFT "
                  "flights use no quantum trajectories or Monte Carlo samples.")
    directory.mkdir(parents=True,exist_ok=True)
    (directory/"loop_coin_flight.json").write_bytes((json.dumps(result,indent=2,allow_nan=False)+"\n").encode())


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory",type=Path)
    main(parser.parse_args().directory)
