"""One translated aperture on the permanent-field walk. Run with NumPy and a fresh directory."""

import argparse
import json
import math
from fractions import Fraction
from pathlib import Path

import numpy as np

from check_central_window_flight import density, require, sharp, stream


def schedule(order, universal):
    # Force F=1. Logarithms are natural. Both schedules use the actual rounded t.
    delta = (math.pi / order) ** .25
    H = math.log(order)
    g = math.log(H)
    D = g if universal else 1.0
    w = delta / g
    t = round(D * H / w**2)
    return delta, H, g, D, w, t


def count_interval(t, low, high):
    """Exact numerator of the fair-binomial interval by the adjacent-bin recurrence."""
    j0 = (t+low)//2
    j1 = (t+high)//2
    term = math.comb(t, j0)
    total = term
    for k in range(j0, j1):
        term = term * (t-k) // (k+1)
        total += term
    if t <= 200:
        require(total == sum(math.comb(t, k) for k in range(j0, j1+1)), "binomial sum")
    return Fraction(total, 2**t)


def trial(order, universal, s):
    delta, H, g, D, w, t = schedule(order, universal)
    v = 2*w
    lo, hi = t*(v-w), t*(v+w)
    n = round(.75 / delta**3)
    require(t+n < 2*order, "ring lift through last read")
    r, l, first = sharp(t, order, s, 0)
    rho = density(r, l)
    require(abs(rho.sum()-1) < 2e-10, "launch mass")
    x = first + 2*np.arange(len(r))
    take = (lo <= x) & (x <= hi)
    J = int(np.count_nonzero(take))
    require(J > 0, "nonempty native interval")
    first, last = int(x[take][0]), int(x[take][-1])
    pc = count_interval(t, first, last)
    upper = math.exp(-t*(v-w)**2/2)
    require(float(pc) <= upper + 1e-14, "count exponential upper bound")
    # Stirling's factorial errors give this lower bound for the least likely site.
    u = last / t
    if u < 1:
        j, k = (t+last)//2, (t-last)//2
        rate = ((1+u)*math.log1p(u)+(1-u)*math.log1p(-u))/2
        log_floor = (math.log(J)-.5*math.log(2*math.pi*j*k/t)-t*rate
                     +1/(12*t+1)-1/(12*j)-1/(12*k))
        require(log_floor <= math.log(float(pc)) + 1e-11, "local Stirling floor")
    else:
        log_floor = None
    ps = float(rho[take].sum())
    require(ps > 0, "positive square pass")
    er, el, start = stream(r[take], l[take], first, n, order, s)
    masses = density(er, el)
    require(abs(masses.sum()-ps) < 2e-10, "joint terminal mass")
    time = n*delta**3
    y = delta**2*(start+2*np.arange(len(masses)))
    cf = []
    for xi in (1., 3.):
        val = complex(np.dot(masses, np.exp(1j * xi * y))/ps)
        target = math.cos(s * xi * time**2/2)
        cf.append(dict(xi=xi, lab_CF=[val.real, val.imag], predicted=target,
                       absolute_error=abs(val-target)))
    return dict(M=order, schedule="universal" if universal else "known_fixed_weight",
                s=s, H=H, g=g, D=D, delta=delta, w=w, v=v, t=t, n=n,
                first_site=first, last_site=last, occupied_sites=J, pass_time=t*delta**3,
                leading_square=2*w/math.pi, square=ps, count_exact=str(pc),
                count=float(pc), count_upper=upper, log_stirling_floor=log_floor,
                count_posterior_equal_priors=float(pc)/(ps+float(pc)),
                unit_mean_physical_cost=t*delta**3/ps,
                leading_physical_cost=math.pi*D*H*g**3/2,
                equal_prior_physical_cost_per_pass=2*t*delta**3/(ps+float(pc)),
                scaled_window_velocity=[(v-w)/delta,(v+w)/delta],
                actual_lab_CF_given_square_pass=cf)


def asymptotic_factors(power):
    # These are algebraic parameter estimates before tick rounding, not simulated records.
    H = power*math.log(10)
    g = math.log(H)
    D = g
    logdelta = (math.log(math.pi)-H)/4
    logw = logdelta-math.log(g)
    return dict(log10_M=power, g=g, max_scaled_velocity=3/g,
                log10_count_upper_over_unit_rate_for_b1_M_inv=
                (-D*H/2 - logw + H - math.log(2/math.pi))/math.log(10),
                log10_source_field_error_factor=(1.5*logdelta + 3*math.log(D*H)
                                                  + 6.5*math.log(g))/math.log(10),
                unit_physical_clock_leading=math.pi*D*H*g**3/2)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    dest = parser.parse_args().directory
    rows = []
    for universal in (False, True):
        unit_at_2048 = None
        for order in (127, 2048, 8191, 32768):
            row = trial(order, universal, 1)
            rows.append(row)
            if order == 2048:
                unit_at_2048 = row
        minus = trial(2048, universal, -1)
        rows.extend([minus, trial(2048, universal, 0)])
        require(abs(unit_at_2048["square"]-minus["square"]) < 2e-12,
                "conjugate square passage")
        for a, b in zip(unit_at_2048["actual_lab_CF_given_square_pass"],
                        minus["actual_lab_CF_given_square_pass"]):
            require(abs(complex(*a["lab_CF"])-complex(*b["lab_CF"])) < 2e-10,
                    "conjugate flight positions")
    dest.mkdir(parents=True, exist_ok=True)
    with (dest / "rested_window_cost.json").open("x", encoding="utf8", newline="\n") as file:
        json.dump(dict(scope="Sharp physical (0,R), F=1. Native ring cone, fair exact count, "
                       "source/terminal probability totals, Stirling/Chernoff bounds and conjugation "
                       "are checked. Conditional terminal CF discrepancies are retained without "
                       "an asymptotic tolerance. Physical costs assume independent sharp launches.",
                       rows=rows, unrounded_parameter_estimates_only=[
                           asymptotic_factors(p) for p in (6, 12, 24, 48, 100)]),
                  file, indent=2, allow_nan=False)
        file.write("\n")


if __name__ == "__main__":
    main()
