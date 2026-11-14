"""Reproduce free-ring interior records with integer counts. Python 3, no packages."""
import argparse
import json
from collections import defaultdict
from math import acos, asin, comb, cos, pi, sin, sqrt
from pathlib import Path


def require(truth, message):
    if not truth:
        raise ValueError(message)


def signed_lines(clocks):
    """Integer counts on the line indexed by left-step count, from a sharp R."""
    right, left = [1], [0]
    for n in range(1, max(clocks) + 1):
        right, left = ([a + b for a, b in zip(right, left)] + [0],
                       [0] + [a - b for a, b in zip(right, left)])
        if n in clocks:
            require(sum(a*a + b*b for a, b in zip(right, left)) == 1 << n,
                    f"line norm at clock {n}")
            yield n, right


def direct_ring(size, n):
    """Propagate on physical sites by last rail and g exponent; signed and fair."""
    state = {(0, 0, 0): (1, 1)}
    for _ in range(n):
        later = defaultdict(lambda: [0, 0])
        for (x, old_left, power), (signed, fair) in state.items():
            r = later[(x + 1) % size, 0, power]
            r[0] += signed
            r[1] += fair
            l = later[(x - 1) % size, 1, (power + 1) % 3]
            l[0] += -signed if old_left else signed
            l[1] += fair
        state = later
    ports = {}
    for x in range(size):
        for rail in (0, 1):
            terms = [state.get((x, rail, j), (0, 0)) for j in range(3)]
            a, b, c = [s for s, _ in terms]
            ports[x, rail] = ((a + b + c)**2, a*a + b*b + c*c - a*b - b*c - c*a,
                              sum(f for _, f in terms))
    for i in range(3):
        require(sum(row[i] for row in ports.values()) == 1 << n, "direct ring norm")
    return ports


def leading(n, y):
    u = abs(y) / n
    k = acos(u / sqrt(1 - u*u))
    phase = asin(sin(k) / sqrt(2)) - u*k
    curvature = sin(k) / (1 + cos(k)**2)**1.5
    weight = (1 + y / n) / 2
    parity = (-1)**n if y < 0 else 1
    return parity * 4 * weight * cos(n*phase - pi/4) / sqrt(2*pi*n*curvature)


def panel(size, n, line, crosscheck):
    """The two lifts are present at the band used for every listed panel."""
    d = size // 2
    two_cos = 2 if d % 3 == 0 else -1
    denominator = 1 << n
    # The normalization below avoids converting exponentially large integers to floats.
    def amplitude(integer):
        return (integer / (1 << (n // 2))) / (sqrt(2) if n % 2 else 1)

    ports = direct_ring(size, n) if crosscheck else None
    rows, errors = [], []
    # Values in each group are U, K and fair numerator over the same denominator.
    groups = {key: [0, 0, 0] for key in ("band", "positive", "negative", "zero")}
    for x in range((21 * n + 49) // 50, 11*n // 25 + 1):
        if (x - n) % 2:
            if crosscheck:
                require(ports[x, 0] == (0, 0, 0), "parity")
            continue
        lifts = [y for y in range(-n, n + 1, 2) if y % size == x]
        require(lifts == [x - size, x], "incorrect lift set")
        i, j = (n - x) // 2, (n - x + size) // 2
        a, b = line[i], line[j]
        u, k = a*a + b*b, a*b
        fair = comb(n-1, i) + comb(n-1, j)
        if crosscheck:
            require(ports[x, 0] == (u + 2*k, u + two_cos*k, fair),
                    f"direct ring disagrees at {(size,n,x)}")
        which = "positive" if k > 0 else "negative" if k < 0 else "zero"
        for key in ("band", which):
            for h, increment in enumerate((u, k, fair)):
                groups[key][h] += increment
        # The signed amplitudes are exact with denominator sqrt(2^n).
        rows.append([x, str(a), str(b), str(fair)])
        errors.extend(abs(amplitude(z) - leading(n, y)) for z, y in ((a, x), (b, x-size)))

    ub, kb, cb = groups["band"]
    up, kp, cp = groups["positive"]
    # Three-law response matrix in (coherent fraction, coherent cosine moment).
    determinant_numerator = 2*((ub - cb)*kp - (up - cp)*kb)
    return dict(size=size, clock=n, D=d, two_cosine_nontrivial=two_cos,
                direct_physical_crosscheck=crosscheck,
                cells_x_signed_upper_signed_lower_fair=rows,
                group_fields=["diagonal_U", "cross_K", "fair"],
                group_numerators={key: [str(v) for v in vs] for key, vs in groups.items()},
                positive_chi0=(up + 2*kp)/denominator,
                positive_chi1=(up + two_cos*kp)/denominator,
                positive_fair=cp/denominator, band_fair=cb/denominator,
                determinant_numerator_over_2_to_2n=str(determinant_numerator),
                determinant=determinant_numerator/(denominator**2),
                max_abs_leading_amplitude_error=max(errors, default=None))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_directory", type=Path)
    opts = parser.parse_args()
    ds = (4, 16, 28, 36, 40, 72, 76, 160, 316, 736, 1204)
    panels = {2*d: [(2*d, 2*d <= 152)] for d in ds}
    # Adjacent odd-clock probes test the native (-1)^n and opposite spatial parity.
    for d in (40, 76, 316):
        panels[2*d + 1] = [(2*d, d <= 76)]
    results = [panel(size, n, line, direct)
               for n, line in signed_lines(panels)
               for size, direct in panels[n]]
    output = dict(protocol="I=[21/50,11/25], terminal right rail, sharp (0,R), no masks",
                  odds="Odd clocks and D=0 mod 3 are controls; theorem uses n=2D, D=4 mod 12.",
                  normalization="Per original launch. Each group numerator is divided by 2^clock.",
                  exact_cells="x, signed upper and lower line numerators over sqrt(2^clock), "
                              "fair combined word count over 2^clock. All reachable band cells retained.",
                  panels=results)
    opts.output_directory.mkdir(parents=True, exist_ok=True)
    out = opts.output_directory / "interior_winding.json"
    with out.open("x", encoding="utf-8", newline="\n") as handle:
        json.dump(output, handle, indent=2)
        handle.write("\n")


if __name__ == "__main__":
    main()
