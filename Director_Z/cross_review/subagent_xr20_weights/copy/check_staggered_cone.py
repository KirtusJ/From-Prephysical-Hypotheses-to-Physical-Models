"""Check the finite-speed continuum chart of a staggered occupation walk.

Run python -B check_staggered_cone.py OUTPUT_DIRECTORY (NumPy).
"""

import argparse
import json
import math
from fractions import Fraction
from pathlib import Path

import numpy as np


I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.diag([1., -1.])
S, C = 4 / 5, 3 / 5
A = S * Z - C * Y


def norm(matrix):
    return float(np.linalg.norm(matrix, 2))


def rational_gap(u):
    # Approximate tan(u/2) to O(u²), using only a finite rational
    # chart in the applied gates. The comparison target u sets the clock.
    denominator = math.ceil(u**-2)
    t = Fraction(round(denominator * math.tan(u / 2)), denominator)
    cos_g = (1 - t*t) / (1 + t*t)
    sin_g = 2*t / (1 + t*t)
    assert cos_g*cos_g + sin_g*sin_g == 1
    cos_b = Fraction(3, 5) * cos_g + Fraction(4, 5) * sin_g
    sin_b = Fraction(4, 5) * cos_g - Fraction(3, 5) * sin_g
    assert cos_b*cos_b + sin_b*sin_b == 1
    return t, cos_b, sin_b


def step(k, cos_b, sin_b):
    shifted = math.cos(k)*X + math.sin(k)*Y
    return (float(cos_b)*I + 1j*float(sin_b)*shifted) @ (C*I - 1j*S*X)


def reference(energy_mass, p, elapsed, action):
    hamiltonian = energy_mass * X + p * A  # c=1
    e = math.hypot(energy_mass, p)
    phase = elapsed * e / action
    if not e:
        return I
    return math.cos(phase)*I - 1j*math.sin(phase)*hamiltonian/e


def reflected_bond(triple, input_index):
    """One rational orthogonal reflection, from actual Walsh selector labels."""
    a, b, c = triple
    width = 1 << (abs(a)+abs(b)-1).bit_length()
    assert a*a+b*b == c*c and width >= c
    state = [0]*(4*width)  # two physical modes, two values of the junk flag
    for label in range(width):
        site, sign, junk = input_index, 1, 0
        if label < abs(a):
            sign = (1 if a>=0 else -1)*(1-2*site)
        elif label < abs(a)+abs(b):
            site ^= 1
            sign = 1 if b>=0 else -1
        else:
            junk = 1
        state[(2*junk+site)*width+label] = sign
    # Starting from the implicitly prepared uniform selector, apply its
    # inverse Walsh transform. The common denominator is width.
    half = 1
    while half < width:
        for start in range(0, len(state), 2*half):
            for i in range(start,start+half):
                v,w = state[i],state[i+half]
                state[i],state[i+half] = v+w,v-w
        half *= 2
    assert sum(x*x for x in state)==width**2
    return width,[state[0],state[width]]


def compiled_bond_clock():
    # The extra Z acts AFTER the reflection to give the oriented real rotation.
    for a,b,c in ((3,4,5),(4,3,5),(3,-4,5)):
        for j in (0,1):
            width,col = reflected_bond((a,b,c),j)
            rotated = [col[0],-col[1]]
            assert rotated == ([a,-b] if j==0 else [b,a])
            assert width==8
    p = Fraction(25,64)
    rows = []
    for bonds in (1,2,8,32):
        for layers in (1,10):
            for retry in (0,2,6):
                f = (1-p)*(1-2*p*(1-p))**retry
                all_pass = (1-f)**(bonds*layers)
                rows.append(dict(bonds=bonds, layers=layers, retry_pairs=retry,
                                 timeout_one=str(f), all_pass=float(all_pass),
                                 any_timeout=float(1-all_pass)))
    return dict(single_input_success=str(p), sample_deadlines=rows)


def chart(action, tau, total_time, gap_kind):
    # Units c=mu=m=1. Two disjoint bond layers cost one cycle.
    u = tau / action
    a = tau / S
    t, cos_b, sin_b = rational_gap(u)
    if gap_kind == "zero":
        cos_b, sin_b = Fraction(3, 5), Fraction(4, 5)
    elif gap_kind == "reversed":
        t = -t
        cg, sg = (1-t*t)/(1+t*t), 2*t/(1+t*t)
        cos_b = Fraction(3,5)*cg + Fraction(4,5)*sg
        sin_b = Fraction(4,5)*cg - Fraction(3,5)*sg
    actual_gap = math.atan2(S*float(cos_b)-C*float(sin_b),
                            C*float(cos_b)+S*float(sin_b))
    n = round(total_time / tau)
    elapsed = n*tau
    ports = []
    for p in (-.75, -.25, 0., .25, .75):
        k = a*p/action
        w = step(k, cos_b, sin_b)
        assert norm(w.conj().T@w-I) < 1e-14
        trace = C*float(cos_b)+S*float(sin_b)*math.cos(k)
        assert abs(np.trace(w)/2-trace)<1e-14
        stepped = np.linalg.matrix_power(w, n)
        expected = reference(1., p, elapsed, action)
        one_tick_error = norm(w-reference(1.,p,tau,action))
        error = norm(stepped-expected)
        assert error <= n*one_tick_error + 2e-10
        # Analytic sine/cosine form of the positive band velocity; at a
        # gapless degeneracy velocity is a cone, not a single derivative.
        sin_omega = math.sqrt(max(0.,(1-trace)*(1+trace)))
        velocity = (float(sin_b)*math.sin(k)/sin_omega if sin_omega>1e-12 else None)
        ports.append(dict(p=p, k=k, step_norm_error=one_tick_error,
                          full_norm_error=error, telescope=n*one_tick_error,
                          flip_probability=float(abs(stepped[1,0])**2),
                          Dirac_flip_probability=float(abs(expected[1,0])**2),
                          band_velocity=velocity, target_velocity=p/math.hypot(1,p),
                          newtonian_velocity=p))
    return dict(action=action, tau=tau, a=a, ticks=n, actual_time=elapsed,
                max_microscopic_speed=a/tau, gap_kind=gap_kind,
                applied_beta=[str(cos_b),str(sin_b)],
                gap_error=actual_gap-u, ports=ports)


def main():
    assert norm(A@A-I)<1e-15 and norm(A@X+X@A)<1e-15
    # Sign convention checked by a derivative of the full matrix, including
    # the intracell gate whose cross term contributes its Z component.
    h = 1e-6
    derivative = (step(h,C,S)-step(-h,C,S))/(2*h)
    assert norm(derivative+1j*S*A)<2e-12
    cases = [chart(.25,2.**(-j),.5,"tuned") for j in range(5,10)]
    cases += [chart(2.**(-r),2.**(-3*r),.5,"tuned") for r in range(2,5)]
    cases += [chart(.25,1/256,.5,tag) for tag in ("zero","reversed")]
    for row in cases:
        if row["gap_kind"]=="tuned":
            assert abs(row["gap_error"])<= (row["tau"]/row["action"])**2+1e-14
    order_control = step(math.pi/3,Fraction(4,5),Fraction(3,5))
    first,second = C*I-1j*S*X, .8*I+1j*.6*(.5*X+math.sqrt(3)/2*Y)
    assert norm(order_control-second@first)<1e-14
    return dict(scope="Uniform two-layer gate and full two-component spinor at specified momenta. No fermionic statistics or interaction is inferred from this comparison.",
                units="c=mu=m=1, cell pitch a=tau/sin(alpha), half-cell bond pitch a/2 and half-cycle layer duration tau/2.",
                signed_gate_control=compiled_bond_clock(),
                order_reversal_at_pi_over_three=dict(
                    trace_difference=abs(complex(np.trace(first@second-order_control))),
                    norm_difference=norm(first@second-order_control)),
                cases=cases)


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("directory",type=Path)
    out=parser.parse_args().directory
    out.mkdir(exist_ok=True,parents=True)
    (out/"staggered_cone.json").write_bytes((json.dumps(main(),indent=2)+"\n").encode())
