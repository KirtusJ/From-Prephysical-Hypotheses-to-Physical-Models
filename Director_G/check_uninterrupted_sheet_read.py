"""Uninterrupted signed Hadamard site-and-rail reads from one sharp R rail.

Run python -B check_uninterrupted_sheet_read.py OUTPUT_DIRECTORY. Standard library.
"""
import argparse
from collections import Counter, defaultdict
from itertools import product
import cmath
import json
import math
from pathlib import Path
import sys


def require(ok, explanation):
    if not ok:
        raise ValueError(explanation)


def square(z):
    return z.real*z.real + z.imag*z.imag


def snapshots(m, s, ticks):
    end = max(ticks)
    require(2*end < 4*m, "light cone no longer embeds in ring")
    norm = 1/math.sqrt(2)
    phases = [norm*cmath.exp(2j*math.pi*s*j/m) for j in range(-end, end+1)]
    right, left = [1], [0]
    for t in range(end):
        # Index j denotes departure x=2j-t. Its daughter indices are j+1,j.
        if s:
            kick = phases[end-(t+1)//2:end-(t+1)//2+t+1]
            right, left = ([0]+[(r+l)*d for r,l,d in zip(right, left, kick)],
                           [(r-l)*d for r,l,d in zip(right, left, kick)]+[0])
        else:
            right, left = ([0]+[(r+l)*norm for r,l in zip(right, left)],
                           [(r-l)*norm for r,l in zip(right, left)]+[0])
        if t+1 in ticks:
            yield t+1, list(map(square, right)), list(map(square, left))


def audit_words():
    rows = []
    for m in (3, 5, 8, 11):
        zs = [cmath.exp(2j*math.pi*y/m) for y in range(m)]
        ticks = set(range(1, min(10, 2*m)))
        for s in (0, 1, -1):
            worst = 0
            for t, r, l in snapshots(m, s, ticks):
                ports = defaultdict(Counter)
                for word in product("RL", repeat=t):
                    x, y, rail, sign = 0, 0, "R", 1
                    for out in word:
                        if rail == out == "L":
                            sign = -sign
                        y = (y+x//2) % m
                        x = (x+(1 if out == "R" else -1)) % (4*m)
                        rail = out
                    ports[x, rail][y] += sign
                for j in range(t+1):
                    x = (2*j-t) % (4*m)
                    for rail, calculated in (("R", r[j]), ("L", l[j])):
                        tally = ports[x, rail]
                        expected = square(sum(a*zs[(s*y) % m] for y, a in tally.items()))/2**t
                        worst = max(worst, abs(expected-calculated))
                # A conservative roundoff allowance grows with the number of
                # signed integer words evaluated, including cancellation at a zero.
                require(worst <= 32*sys.float_info.epsilon*2**t, "integer coordinate oracle")
            rows.append(dict(order=m, s=s, maximum_ticks=max(ticks),
                             max_port_discrepancy=worst))
    return rows


def matched_statistic(t, m, r1, r0, first=0, second=1):
    observed = []
    stationary = []
    errors = []
    for j in range(t+1):
        x = 2*j-t
        if 4*x < t or 2*x > t:
            continue
        v = x/t
        k = math.acos(v/math.sqrt(1-v*v))
        omega = math.asin(math.sin(k)/math.sqrt(2))
        curvature = (1-v*v)*math.sqrt(1-2*v*v)
        rail_weight = (1+v)/2
        phase = 2*x*k-2*t*omega+math.pi/2
        delta = math.pi**2*t*(t*t-1)*curvature/(12*m*m)
        low, high = first**2*delta, second**2*delta
        score = math.sin(phase+(low+high)/2)
        diff = r1[j]-r0[j]
        prediction = 4*rail_weight**2/(math.pi*t*curvature)*(
            math.cos(phase+high)-math.cos(phase+low))
        observed.append(diff*score)
        stationary.append(prediction*score)
        errors.append(abs(prediction-diff))
    return dict(mean_difference=math.fsum(observed),
                stationary_pair_sum=math.fsum(stationary),
                total_abs_point_difference_from_leading_stationary_term=math.fsum(errors),
                right_port_cells=len(observed))


def panel(b):
    m = b**3
    low = math.isqrt(m)
    if m-low*low > (low+1)**2-m:
        low += 1
    times = sorted({low, b*b-1, b*b, b*b+1, 2*b*b})
    small = set(times)
    result = []
    for base, forced in zip(snapshots(m, 0, small), snapshots(m, 1, small)):
        t, r0, l0 = base
        t1, r1, l1 = forced
        require(t1 == t, "comparison clock")
        dr = [r-h for r,h in zip(r1,r0)]
        dl = [r-h for r,h in zip(l1,l0)]
        totals = [math.fsum(r)+math.fsum(l) for r,l in ((r1,l1),(r0,l0))]
        require(all(abs(a-1) <= 32*(t+1)*sys.float_info.epsilon for a in totals),
                "probability normalization")
        result.append(dict(ticks=t, time_parity=t % 2, t_cubed_over_order_squared=t**3/m**2,
                           full_site_rail_TV=(math.fsum(map(abs,dr))+math.fsum(map(abs,dl)))/2,
                           position_only_TV=math.fsum(abs(a+b) for a,b in zip(dr,dl))/2,
                           rail_only_TV=(abs(math.fsum(dr))+abs(math.fsum(dl)))/2,
                           normalized_masses_s1_s0=totals,
                           matched=matched_statistic(t,m,r1,r0)))
    return dict(b=b, order=m, folded_labels=[0,1], rows=result)


def adjacent_nonzero(b):
    m, t = b**3, b*b
    _, r1, l1 = next(snapshots(m, 1, {t}))
    _, r2, l2 = next(snapshots(m, 2, {t}))
    variation = math.fsum(abs(x-y) for a, d in ((r1,r2),(l1,l2)) for x,y in zip(a,d))/2
    return dict(order=m, ticks=t, folded_labels=[1,2], full_site_rail_TV=variation,
                matched=matched_statistic(t,m,r2,r1,1,2))


def integral(steps, square_gap=1):
    def f(v):
        c = (1-v*v)*math.sqrt(1-2*v*v)
        return (2/math.pi)*((1+v)/2)**2/c*math.sin(square_gap*math.pi**2*c/24)
    return math.fsum(f(1/4+(j+0.5)/(4*steps)) for j in range(steps))/(4*steps)


def run():
    return dict(scope="Model calculations, one uninterrupted sharp R launch, "
                      "unread sheet. The tables are conditional on sector s. "
                      "No intermediate reads. Opposite parities retained. "
                      "A localized sheet has all M sector weights 1/M.",
                signed_history_audit=audit_words(),
                critical_limit_integral_midpoint=[dict(subintervals=n, value=integral(n),
                                                        labels_one_two=integral(n,3))
                                                  for n in (100, 1000, 10000)],
                adjacent_nonzero_labels=[adjacent_nonzero(b) for b in (4,8,16,32)],
                cube_panels=[panel(b) for b in (4,5,6,7,8,9,10,12,16,20,24,32)])


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("directory", type=Path)
    target = cli.parse_args().directory/"uninterrupted_sheet_read.json"
    data = run()
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("x", encoding="utf8", newline="\n") as f:
        json.dump(data, f, sort_keys=True, separators=(",", ":"))
        f.write("\n")
