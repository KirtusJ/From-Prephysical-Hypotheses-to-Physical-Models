"""One physical rail word and a terminal position read on the staircase walk.

With NumPy: python -B check_same_flight_sheet_selection.py NEW_DIRECTORY
All finite-order charges in the census are included via exact sign conjugacy.
"""
import argparse
from collections import defaultdict
from fractions import Fraction
import json
import math
from pathlib import Path

import numpy as np

from check_field_on_renewal import free_success, product_prefixes


def require(condition, message):
    if not condition:
        raise ValueError(message)


def even_nearest(x):
    return 2 * max(1, math.floor(x / 2 + 0.5))


def parameters(order):
    delta = (math.pi / order) ** 0.25
    m = even_nearest(0.5 * order ** (2 / 3))
    n = even_nearest(1 / delta**3)
    elapsed = n * delta**3
    return delta, m, n, elapsed


def pass_tubes(x, delta, elapsed):
    center = elapsed**2 / 2
    return abs(abs(x * delta**2) - center) <= center / 4


def physical_ports(order, charge, m, n, home=0, rail=1):
    """Literal site/direction propagation, unnormalised after each projector."""
    radius = 2 * m + n
    require(radius < 2 * order, "wrapped light cone")
    x = np.arange(-radius, radius + 1)
    # A 4M-ring representative and its lift give the same departure gain.
    gain = ((x + home) // 2 * charge) % order
    kick = np.exp(-2j * math.pi * gain / order) / math.sqrt(2)
    right = np.zeros(x.size, dtype=complex)
    left = np.zeros_like(right)
    (right if rail == 1 else left)[radius] = 1
    failure = []
    keep = rail
    for tick in range(1, radius + 1):
        outgoing_r = (right + left) * kick
        outgoing_l = (right - left) * kick
        right[1:] = outgoing_r[:-1]
        left[:-1] = outgoing_l[1:]
        right[0] = left[-1] = 0
        if tick <= 2 * m and tick % 2 == 0:
            keep = -keep
            rejected = left if keep == 1 else right
            failure.append(float(np.vdot(rejected, rejected).real))
            rejected.fill(0)
    ports = np.stack((abs(right)**2, abs(left)**2))
    return x, ports, failure


def one_row(order, charge, m, n, delta, elapsed, oracle):
    x, ports, first_fail = physical_ports(order, charge, m, n)
    density = ports.sum(axis=0)
    survival = float(density.sum())
    tube = pass_tubes(x, delta, elapsed)
    joint = float(density[tube].sum())
    r = min(charge, abs(order / 2 - charge), order - charge)
    # Magnitudes and their squared norm refer to the full sheet Fourier grid.
    if oracle:
        _, _, prefixes = product_prefixes(order, charge, m)
        prefix_error = max(abs(a-b-c) for a, b, c in zip(prefixes, prefixes[1:], first_fail))
        require(prefix_error < 1e-10 and abs(survival - prefixes[-1]) < 1e-10,
                "projected coordinate histories disagree with Fourier product")
    else:
        prefix_error = None
    total_error = abs(1 - survival - sum(first_fail))
    require(total_error < 2e-10, "incomplete first-fail/terminal outcomes")
    require(survival > 0, "selected finite panel underflowed")
    ratio = survival / free_success(m)
    return dict(charge=charge, multiplicity=1 if (2*charge) % order == 0 else 2,
                offset_from_nearest_ladder=r, survival=survival,
                survival_over_zero=ratio, fixed_offset_limit=math.exp(-math.pi**2 * 0.5**3 * r*r / 3),
                first_fail=first_fail, pass_and_inside_unit_tubes=joint,
                pass_and_outside_unit_tubes=survival-joint, inside_given_pass=joint/survival,
                ballistic_half_speed_band_given_pass=float(density[abs(abs(x/n)-0.5) <= 0.125].sum()/survival),
                total_mass_error=total_error, fourier_prefix_error=prefix_error)


def panel(order, requested=None):
    delta, m, n, elapsed = parameters(order)
    charges = list(range(order//2+1)) if requested is None else sorted(set(requested))
    rows = [one_row(order,k,m,n,delta,elapsed,requested is None) for k in charges]
    result = dict(M=order, delta=delta, m=m, n=n, preparation_time=2*m*delta**3,
                  flight_time=elapsed, tube_centers=[-elapsed**2/2,elapsed**2/2],
                  tube_radius=elapsed**2/8, all_folded_charges=requested is None, rows=rows)
    if requested is None:
        require(sum(row["multiplicity"] for row in rows) == order, "wrong Fourier prior")
        joint = sum(row["multiplicity"]*row["pass_and_inside_unit_tubes"] for row in rows)/order
        survived = sum(row["multiplicity"]*row["survival"] for row in rows)/order
        true = 2*rows[1]["pass_and_inside_unit_tubes"]/order
        result.update(total_sheet_word=survived,total_sheet_word_and_tube=joint,
                      prior_unit=2/order, true_joint=true,
                      unit_given_word=2*rows[1]["survival"]/order/survived,
                      unit_given_word_and_tube=true/joint if joint else None,
                      true_joint_asymptotic=(2/order)*free_success(m)*math.exp(-math.pi**2/24))
    return result


def integer_sheet(order, m, n):
    """Full signed path counts in the localized sheet basis, without Fourier sectors."""
    state = {(0,1,0):1}
    failures = []
    for tick in range(1,2*m+n+1):
        new = defaultdict(int)
        for (x,rail,y), value in state.items():
            target = (y+x//2) % order
            new[x+1,1,target] += value
            new[x-1,-1,target] += value if rail == 1 else -value
        if tick <= 2*m and tick % 2 == 0:
            keep = (-1)**(tick//2)
            failures.append(Fraction(sum(z*z for (_,c,_),z in new.items() if c != keep),2**tick))
            new = {key:z for key,z in new.items() if key[1] == keep and z}
        state = new
    den = 2**(2*m+n)
    ports = defaultdict(int)
    for (x,c,_),z in state.items():
        ports[x,c] += z*z
    x, reference, _ = physical_ports(order,0,m,n)
    sector_sum = np.zeros_like(reference)
    fail_sum = np.zeros(m)
    for k in range(order):
        _, field, first_fail = physical_ports(order,k,m,n)
        sector_sum += field / order
        fail_sum += np.asarray(first_fail)/order
    exact = np.array([[ports[int(j),c]/den for j in x] for c in (1,-1)])
    error = float(np.max(abs(exact-sector_sum)))
    fail_error = float(np.max(abs(fail_sum-np.asarray(failures,dtype=float))))
    require(max(error,fail_error)<1e-12 and sum(failures)+Fraction(sum(ports.values()),den)==1,
            "localized-sheet signed path counts disagree with Fourier decomposition")
    return dict(M=order,m=m,n=n,denominator=den,x=x.tolist(),
                numerators_R_L=[[ports[int(j),c] for j in x] for c in (1,-1)],
                first_fail=[str(f) for f in failures],max_port_error=error,
                max_first_fail_error=fail_error)


def floquet(q,h):
    coin = np.array([[1,1],[1,-1]])/math.sqrt(2)
    def tick(k):
        return np.diag([np.exp(-1j*k),np.exp(1j*k)]) @ coin
    return tick(q) @ tick(q+h)


def controls():
    traces = []
    for h in (-math.pi/2, math.pi/2, math.pi/2+math.pi/65):
        err = 0.
        for q in np.linspace(-math.pi,math.pi,31):
            a=floquet(q,h)
            err=max(err,abs(np.trace(a)-math.cos(2*q+h)-math.cos(h)),abs(np.linalg.det(a)-1))
        diff=1e-5
        def theta(q):
            return math.acos(np.trace(floquet(q,h)).real / 2)
        v=(theta(diff)-theta(-diff))/(4*diff)
        exact_v=math.sin(h)/(2*math.sqrt(1-math.cos(h)**2))
        require(err < 2e-14 and abs(v-exact_v)<1e-9,"two-step dispersion and velocity")
        traces.append(dict(h=h,max_trace_or_determinant_error=float(err),
                           derivative_speed_per_tick=v,predicted_speed=exact_v))
    aliases=[]
    for order in (32,64,128):
        _,m,n,_=parameters(order)
        for k in (0,1,2):
            _,a,f=physical_ports(order,k,m,n)
            _,b,g=physical_ports(order,k+order//2,m,n)
            prefix_error=max(abs(i-j) for i,j in zip(f,g))
            require(prefix_error<1e-13,"half-order survival alias")
            aliases.append(dict(M=order,charge=k,survival_alias=k+order//2,
                                first_fail_difference=prefix_error,
                                conditional_terminal_TV=float(np.sum(abs(a/a.sum()-b/b.sum()))/2)))
    reflected=[]
    for order, k in ((32,1),(33,16),(65,2)):
        _,m,n,_=parameters(order)
        _,a,_=physical_ports(order,k,m,n)
        _,b,_=physical_ports(order,-k,m,n,home=1,rail=1)
        _,c,_=physical_ports(order,k,m,n,home=-1,rail=-1)
        e=max(float(np.max(abs(a-b))),float(np.max(abs(a-c[::-1,::-1]))))
        require(e<2e-13,"conjugation, translation or launch-rail reflection")
        reflected.append(dict(M=order,charge=k,max_unnormalized_port_error=e))
    return dict(two_tick=traces,half_alias=aliases,reflections=reflected)


def run():
    return dict(settings=dict(force=1,lambda_value=0.5,target_time=1,
                              even_rounding="nearest even, upward at ties",
                              tube_radius_fraction_of_center=0.25,
                              pass_definition="2m ticks, opposite rail every second tick, then n uninterrupted ticks; binary terminal union",
                              numerical_tests="mass, Fourier prefixes, localized-sheet exact integers, symmetries and two-tick dispersion; no finite success threshold"),
                exact_lift=[integer_sheet(q,2,4) for q in (5,6,9)],
                controls=controls(),
                census=[panel(q) for q in (32,33,64,65,128,129,256,257,512,513)],
                selected_higher_orders=[panel(q,[0,1,2,3,q//2-1,q//2]) for q in (2048,2049,16384,16385)])


if __name__ == "__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("destination",type=Path)
    out=ap.parse_args().destination/"same_flight_sheet_selection.json"
    if out.exists():
        raise FileExistsError(out)
    result = run()
    out.parent.mkdir(parents=True,exist_ok=True)
    with out.open("x",encoding="utf-8",newline="\n") as handle:
        json.dump(result,handle,indent=2,allow_nan=False)
        handle.write("\n")
