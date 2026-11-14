"""Exact unfiltered ring records near the first meeting of the two Hadamard wavefronts.

Run with Python 3: python -B check_unfiltered_winding.py NEW_DIRECTORY.
Take g of order three and z of order two. The four gains (RR, RL, LR, LL)
are (1, g, 1, zg). The two norm-preserving characters both send z to -1.
"""
import argparse
import json
from collections import Counter
from fractions import Fraction
from math import gamma, isqrt
from pathlib import Path


def check(condition, message):
    if not condition:
        raise ValueError(message)


def nearest_front_tick(d):
    """Nearest even integer to sqrt(2)*d, using an exact midpoint comparison."""
    lower = isqrt(d*d//2)
    return 2*(lower + (2*d*d > (2*lower+1)**2))


def line_states(times):
    """Integer signed amplitudes on the line, indexed by the number of L steps."""
    right, left = [1], [0]
    for t in range(1, max(times)+1):
        right, left = ([a+b for a, b in zip(right, left)] + [0],
                       [0] + [a-b for a, b in zip(right, left)])
        if t in times:
            yield t, right, left


def omega_norm(coeff):
    """Squared modulus of a+b*omega+c*omega^2, with omega^2+omega+1=0."""
    a, b, c = coeff
    return a*a + b*b + c*c - a*b - a*c - b*c


def folded_ports(d, t, right, left):
    """Take the ring image of each line endpoint, keeping its character phase."""
    size = 2*d
    coeffs = [[[0]*3 for _ in range(2)] for _ in range(size)]
    counts = [[0, 0] for _ in range(size)]
    # Counts ending on R or L after t>=1 are the two daughters of the
    # unweighted line distribution at t-1. Binomial recurrence is exact.
    binomial = 1
    for j in range(t+1):
        x = (t-2*j) % size
        coeffs[x][0][j % 3] += right[j]
        coeffs[x][1][j % 3] += left[j]
        if j < t:
            counts[x][0] += binomial
            counts[(x-2) % size][1] += binomial
            binomial = binomial*(t-1-j)//(j+1)
    ports = []
    for x in range(size):
        row = []
        for rail in range(2):
            coeff = coeffs[x][rail]
            row.append([sum(coeff)**2, omega_norm(coeff), counts[x][rail]])
        ports.append(row)
    return ports


def direct_ring(d, times):
    """Grow ordinary unsigned words on the real six-sheet cover before reading phases."""
    size = 2*d
    state = Counter({(0, 0, 0, 0): 1})
    for t in range(1, max(times)+1):
        later = Counter()
        for (site, previous_rail, sign_bit, g), number in state.items():
            later[(site+1) % size, 0, sign_bit, g] += number
            later[(site-1) % size, 1, sign_bit ^ previous_rail, (g+1) % 3] += number
        state = later
        if t not in times:
            continue
        rows = []
        for x in range(size):
            row = []
            for r in range(2):
                coeff = [state[x,r,0,k]-state[x,r,1,k] for k in range(3)]
                check(omega_norm(coeff) == omega_norm([coeff[0], coeff[2], coeff[1]]),
                      "conjugate characters")
                count = sum(state[x,r,0,k]+state[x,r,1,k] for k in range(3))
                row.append([sum(coeff)**2, omega_norm(coeff), count])
            rows.append(row)
        yield t, rows


def selected(rows, sites, rails):
    return [sum(rows[x][r][h] for x in sites for r in rails) for h in range(3)]


def accept_record(nums, den):
    """All numerators share the per-original-launch denominator 2^t."""
    p0, p1, pc = (v/den for v in nums)
    return dict(numerators=nums, probabilities=[p0, p1, pc],
                difference=(nums[0]-nums[1])/den,
                two_sample_variance=p0*(1-p0)+p1*(1-p1))


def sign_read(ports, den, site_only):
    if site_only:
        bins = [[sum(x[rail][h] for rail in range(2)) for h in range(3)] for x in ports]
    else:
        bins = [row for x in ports for row in x]
    plus = [row for row in bins if row[0] > row[1]]
    tie = [row for row in bins if row[0] == row[1]]
    masses = [sum(row[h] for row in plus) for h in range(3)]
    ties = [sum(row[h] for row in tie) for h in range(3)]
    tv = masses[0]-masses[1]
    check(2*tv == sum(abs(row[0]-row[1]) for row in bins), "TV sign convention")
    sharp = accept_record(masses, den)
    fair = accept_record([2*m+t for m,t in zip(masses,ties)], 2*den)
    check(fair["numerators"][0]-fair["numerators"][1] == 2*tv, "half-tie contrast")
    return dict(positive_bins=len(plus), tied_bins=len(tie), tied_mass=ties[0]/den,
                total_variation_numerator=tv, total_variation=tv/den,
                sharp_positive=sharp, half_tie=fair)


def panel(d, t, label, right, left, physical):
    size = 2*d
    den = 1 << t
    rows = folded_ports(d, t, right, left)
    for h in range(3):
        check(sum(cell[h] for row in rows for cell in row) == den, "original mass")
    if physical is not None:
        check(rows == physical, "direct native ring/line disagreement")
    strip = [x for x in range(size) if 8*abs(x-d)**3 <= t]
    antipode, window = {}, {}
    for rails, key in (([0],"R"),([1],"L"),([0,1],"site")):
        antipode[key] = accept_record(selected(rows,[d],rails),den)
        window[key] = accept_record(selected(rows,strip,rails),den)
    sources = [(j, right[j], left[j]) for j in range(t+1) if (t-2*j) % size == d]
    if t < 3*d and (t-d)%2 == 0 and t >= d:
        check(len(sources) == 2, "two image condition")
        u, v = sources
        factor = 0 if d % 3 == 0 else 3
        for i, rail in ((1,"R"),(2,"L")):
            n = antipode[rail]["numerators"]
            check(n[0]-n[1] == factor*u[i]*v[i], "two winding cross term")
    site_sign = sign_read(rows, den, True)
    rail_sign = sign_read(rows, den, False)
    if d % 3 == 0 or t < d:
        check(rail_sign["total_variation"] == 0, "blind full distribution")
    if (t-d) % 2:
        check(antipode["site"]["numerators"] == [0,0,0], "unoccupied parity")
    k = t**(1/3)
    return dict(D=d, N=size, ticks=t, clock=label, denominator_power_of_two=t,
                direct_physical_oracle=physical is not None,
                antipode_lifts=[dict(x=t-2*j, left_steps=j, R_amplitude=r, L_amplitude=l)
                                for j,r,l in sources],
                antipode=antipode, window_sites=strip, window=window,
                scaled_antipode_contrast=[antipode[r]["difference"]*k*k for r in ("R","L","site")],
                scaled_window_contrast=[window[r]["difference"]*k for r in ("R","L","site")],
                sign_test_site_only=site_sign, sign_test_site_and_rail=rail_sign)


def mixture_inverse():
    """Two unfiltered native records recover the three folded weights with known gains."""
    # Two inversion records and three holdouts at distinct circumferences.
    settings = [(4,3,7,1),(4,6,4,0),(3,5,3,1),(5,9,5,0),(8,12,8,1)]
    observations = []
    for d,t,x,r in settings:
        rows = dict(direct_ring(d,{t}))[t]
        s0,s1,count = rows[x][r]
        observations.append([Fraction(v, 1<<t) for v in (s0,s1,s1,count)])
    check(observations[0] == [0,0,0,Fraction(1,4)], "count anchor")
    check(observations[1] == [Fraction(v,64) for v in (36,21,21,6)], "winding anchor")
    cases = []
    for units in [(1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1),(2,3,5,7),(2,5,3,7)]:
        weights = [Fraction(n,sum(units)) for n in units]
        readings = [sum(w*p for w,p in zip(weights,model)) for model in observations]
        count = 4*readings[0]
        trivial = (64*readings[1]-21+15*count)/15
        pair = 1-count-trivial
        check([trivial,pair,count] == [weights[0],weights[1]+weights[2],weights[3]],
              "folded inversion")
        for (s0,s1,_,c), actual in zip(observations[2:],readings[2:]):
            check(trivial*s0+pair*s1+count*c == actual, "common-mixture prediction")
        cases.append(dict(weight_units=units, probabilities=list(map(str,readings)),
                          recovered_folded=list(map(str,[trivial,pair,count]))))
    check(cases[-1]["probabilities"] == cases[-2]["probabilities"], "conjugate exchange")
    return dict(weight_order=["chi0","chi1","chi2","count"],
                settings=[dict(D=d,t=t,x=x,rail=("R","L")[r],
                               probabilities=list(map(str,model)))
                          for (d,t,x,r),model in zip(settings,observations)],
                inversion="For fixed weights, c=4*p0 and w0=(64*p1-21+15*c)/15. "
                          "The complement 1-c-w0 is the conjugate-pair weight.",
                cases=cases)


def run():
    # The visible progression is fixed before inspecting the comparisons; check
    # blind and opposite-winding residue classes at both small and large orders.
    visible = [4,16,28,40,64,100,124,256,508,1024]
    control = [8,12,20,24,36,128,252]
    rows = []
    for d in sorted(visible+control):
        front = nearest_front_tick(d)
        clocks = {"before_two_images":d-2, "first_two_images":d,
                  "front_earlier":front-2, "front":front, "front_later":front+2,
                  "wrong_antipode_parity":front+1, "late_overlap":2*d-2}
        times = set(clocks.values())
        physical = dict(direct_ring(d,times)) if d<=40 else {}
        for t,r,l in line_states(times):
            for label in (name for name,time in clocks.items() if time==t):
                rows.append(panel(d,t,label,r,l,physical.get(t)))
    ai0 = 1/(3**(2/3)*gamma(2/3))
    alpha = (4*2**0.5)**(1/3)
    contrast = 1.5*(alpha*ai0)**2
    return dict(scope="N=2D, sharp (0,R), unfiltered; each probability per original launch. "
                      "RR=LR=1, RL=g, LL=zg in C2 x C3. Ordered models: "
                      "(z,g)=(-1,1), (-1,exp(2*pi*i/3)), fair count.",
                setup=dict(visible_D=visible, controls_D=control,
                           window="8*abs(x-D)^3 <= t on physical representatives 0..2D-1",
                           front="nearest even integer to sqrt(2)*D",
                           sign="Positive bins have chi0 probability larger than chi1. Sharp reads "
                                "reject ties. An independent fair bit decides ties for half_tie, "
                                "whose numerators have denominator 2^(t+1).",
                           variance="For N fresh launches in each arm, variance of the difference "
                                    "of empirical Bernoulli means is this two-sample variance / N.",
                           zero_rates="All parity zeros, blind orders and early misses retained."),
                limiting_front=dict(Airy_at_zero=ai0, alpha=alpha,
                                    predicted_scaled_R_L_site=[contrast,-contrast,0.0]),
                native_mixture_inverse=mixture_inverse(),
                rows=rows)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_directory", type=Path)
    directory = parser.parse_args().output_directory
    result = run()
    directory.mkdir(parents=True, exist_ok=True)
    with (directory/"unfiltered_winding.json").open("x", encoding="utf8", newline="\n") as out:
        json.dump(result, out, indent=2, allow_nan=False)
        out.write("\n")
