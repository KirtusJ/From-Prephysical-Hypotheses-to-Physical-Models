"""Replay all positions for the unread contact loop and two-body phase synthesis."""
import argparse
from collections import defaultdict
from fractions import Fraction
from itertools import product
import json
from math import ceil, cos, pi, sin, sqrt
from pathlib import Path


def contact(state, dr, dl, prime):
    r, l, z = state
    shift = pow(2, -1, prime)*(r*dl-l*dr)
    return (r+dr) % prime, (l+dl) % prime, (z+shift) % prime


def loop(state, a, b, prime):
    for dr, dl in ((a,0),(0,b),(-a,0),(0,-b)):
        state = contact(state, dr, dl, prime)
    return state


def routes(bit, ticks):
    # |0> is the right-moving port at +1. Clear flags at both endpoints.
    start = 1-2*bit
    state = {(start, start): 1}
    for _ in range(ticks):
        after = defaultdict(int)
        for (x, rail), amplitude in state.items():
            for outgoing in (1, -1):
                sign = -1 if rail == outgoing == -1 else 1
                after[x+outgoing, outgoing] += sign*amplitude
        state = after
    return state


def pair_counts(mode, ticks):
    amplitudes = defaultdict(int)
    for a, b in product(range(2), repeat=2):
        r, l, z = loop((0, 0, 0), a, b, 5)
        assert (r, l, z) == (0, 0, a*b)
        memory = {"loop": z, "commuting": 0, "copied_routes": (a,b),
                  "tally": (a+b) % 5}[mode]
        for (x, u), m in routes(a, ticks).items():
            for (y, v), n in routes(b, ticks).items():
                amplitudes[x, u, y, v, memory] += m*n
    counts = defaultdict(int)
    for (x, _, y, _, _), value in amplitudes.items():
        counts[x,y] += value**2
    assert sum(counts.values()) == 4*4**ticks
    return counts


def est_x(x):
    return 2 if x in (-3, 1) else -2


def est_z(x):
    return {-3:-4, -1:0, 1:0, 3:4}[x]


def score(x, y):
    a, b = est_x(x), est_x(y)
    z, w = est_z(x), est_z(y)
    return (1-Fraction((1+a)*(1+b), 4) + Fraction(z*(1-b)+w*(1-a)+z*w, 2))


def position_test():
    sites = (-3,-1,1,3)
    xs = [[score(x,y) for y in sites] for x in sites]
    width = max(map(max,xs))-min(map(min,xs))
    models = {}
    for mode in ("loop", "commuting", "copied_routes", "tally"):
        c = pair_counts(mode, 2)
        total = sum(c.values())
        mean = sum(score(x,y)*c[x,y] for x,y in product(sites, repeat=2))/total
        models[mode] = {"counts": [[c[x,y] for y in sites] for x in sites],
                        "denominator": total, "mean": str(mean)}
    assert models["loop"]["mean"] == "-1/8"
    assert all(Fraction(v["mean"]) >= 0 for k,v in models.items() if k != "loop")
    for t in (0,1):
        assert pair_counts("loop",t) == pair_counts("copied_routes",t)
    return {"sites": sites, "scores": [[str(v) for v in row] for row in xs],
            "models": models, "score_range": str(width),
            "sufficient_tv_error": str(Fraction(1,8)/width)}


def force_test():
    # Fixed-action and shrinking-action spacings of the earlier two-body theorem.
    # Choose order and amplitude directly. No use of a primality approximation in checks.
    rows = []
    for sites, prime in ((8,101),(16,1009),(32,10009),(64,100003),(96,1000003)):
        assert all(prime % n for n in range(2, int(sqrt(prime))+1))
        for classical in (False, True):
            spacing = 2*pi/sites
            delta = sqrt(spacing) if classical else spacing
            eps = delta if classical else 1.0
            amplitude = sqrt(prime*delta*delta/(4*pi))
            rounded_cos = [round(amplitude*cos(j*spacing)) for j in range(sites)]
            rounded_sin = [round(amplitude*sin(j*spacing)) for j in range(sites)]
            bound = (4*pi/prime)*(sqrt(2)*amplitude+0.5)
            worst, symmetry = 0.0, 0
            for x,y in product(range(sites), repeat=2):
                cx, cy = rounded_cos[x], rounded_cos[y]
                sx, sy = rounded_sin[x], rounded_sin[y]
                label = loop(loop((3,5,2), -cx, cy, prime), -sx, sy, prime)
                exact = -cx*cy-sx*sy
                assert label == (3,5,(2+exact) % prime)
                phase = 4*pi*exact/prime
                target = -delta**2*cos(spacing*(x-y))
                worst = max(worst, abs(phase-target))
                xp, yp = (x+1)%sites, (y+1)%sites
                translated = -rounded_cos[xp]*rounded_cos[yp]-rounded_sin[xp]*rounded_sin[yp]
                symmetry = max(symmetry, abs(exact-translated))
            assert worst <= bound+1e-14
            rows.append({"sites": sites, "prime": prime, "epsilon": eps, "delta": delta,
                         "amplitude": amplitude, "worst_angle_error": worst,
                         "uniform_bound": bound, "max_change_one_simultaneous_site_shift": symmetry,
                         "padded_generator_slots_per_potential": 8*ceil(amplitude+0.5),
                         "one_unit_time_accumulated_bound": bound/(eps*delta**2)})
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="compare with retained results")
    args = parser.parse_args()
    result = {"positions":position_test(),"force":force_test()}
    encoded = json.dumps(result, indent=2, allow_nan=False)
    if args.check:
        path = Path(__file__).with_name("unread_loop_results.json")
        assert json.loads(path.read_text(encoding="utf-8")) == json.loads(encoded)
        print("All position counts and 10 local-force comparisons verified.")
    else:
        print(encoded)


if __name__ == "__main__":
    main()
