"""Check a three-copy count reference from signed physical ports on an eight-site ring."""

from argparse import ArgumentParser
from fractions import Fraction as Q
from itertools import product
import json
from math import comb, prod
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def walk_ports():
    # Physical order at each site is right, left; denominator after three
    # ticks is sqrt(8). The signed Hadamard precedes the conditional shift.
    state = [[0, 0] for _ in range(8)]
    state[0][0] = 1
    for step in range(3):
        after = [[0, 0] for _ in range(8)]
        for x, (r, l) in enumerate(state):
            after[(x+1) % 8][0] += r+l
            after[(x-1) % 8][1] += r-l
        state = after
        require(sum(r*r+l*l for r,l in state) == 2**(step+1), "full signed-port norm")
    require(state == [[0,0],[2,1],[0,0],[1,0],[0,0],[0,1],[0,0],[-1,0]],
            "signed site and rail output for the right launch")
    return state


def count_weights(ports):
    # Route each ordered triple of physical modes; retain the two dark rails
    # of an empty site and every other unused mode in the enumeration.
    one = [(x, a) for x, pair in enumerate(ports) for a in pair]
    layers = [0]*4
    for triple in product(one, repeat=3):
        count = sum(x == 1 for x, _ in triple)
        layers[count] += prod(a for _, a in triple)**2
    require(layers == [27,135,225,125] and sum(layers) == 512, "full three-bank count law")
    return layers


def threshold_table():
    table = {}
    for word in product((0,1), repeat=3):
        complement = tuple(1-bit for bit in word)
        passes = [int(sum(word) >= j) for j in (1,2,3)]
        table["".join(str(x) for x in word)] = passes
        for j, passed in enumerate(passes, 1):
            require(passed + int(sum(complement) >= 4-j) == 1, "word complement")
    for j in range(3):
        # XOR the threshold into an initially free bit and retain the whole
        # word. Each of the 16 basis configurations has a distinct image.
        mapped = {(w, bit ^ answers[j]) for w,answers in table.items() for bit in (0,1)}
        require(len(mapped) == 16, "threshold instrument is reversible")
    return table


def binomial_tails(m, p):
    weights = [comb(m,k)*p**k*(1-p)**(m-k) for k in range(m+1)]
    return [sum(weights[j:]) for j in range(1,m+1)]


def square_score(u):
    return u*u/(u*u + (1-u)**2)


def midpoint_ramp(u):
    return min(Q(1),max(Q(0),50*(u-Q(49,100))))


def average(xs):
    return sum(xs)/len(xs)


def maximum_monotone_average(tails):
    # For a complementary response with G(0)=0,G(1)=1, write 2G(u)-1
    # above one half as the cumulative weight of an increasing step. On
    # this finite grid one extreme step attains the largest linear average.
    # The same upper value is attainable by a continuous interpolant.
    distances = [2*x-1 for x in tails]
    cuts = sorted({abs(x) for x in distances} | {Q(1)})
    best = max(sum((x>=c)-(x<=-c) for x in distances) for c in cuts if c>0)
    return Q(1,2)+Q(best,2*len(tails))


def dispersion(weights):
    """All expectations are finite sums over independent copies of the count."""
    m = len(weights)-1
    require(m > 0 and sum(weights) == 1 and all(w>=0 for w in weights), "complete count law")
    tails = [sum(weights[j:]) for j in range(1,m+1)]
    mean = sum(Q(k,m)*w for k,w in enumerate(weights))
    var = sum((Q(k,m)-mean)**2*w for k,w in enumerate(weights))
    gap = sum(abs(k-l)*wk*wl for k,wk in enumerate(weights) for l,wl in enumerate(weights))
    threshold_var = average([s*(1-s) for s in tails])
    require(average(tails) == mean and 2*m*threshold_var == gap, "tail sum and absolute-difference identity")
    require(var <= threshold_var and 3*threshold_var**2 <= var, "two dispersion bounds")
    return dict(mean=mean, variance=var, mean_threshold_variance=threshold_var,
                expected_absolute_count_difference=gap)


def check_histogram_symmetry():
    """Compare reflected interior tails with reflected counts, including support gaps."""
    checked = symmetric = 0
    for raw in product(range(3), repeat=6):
        occupied = [k for k, w in enumerate(raw) if w]
        if not occupied:
            continue
        first, last = occupied[0], occupied[-1]
        total = sum(raw)
        tails = [sum(raw[j:]) for j in range(1, len(raw))]
        interior = sorted(s for s in tails if 0 < s < total)
        reflected = sorted(total-s for s in interior)
        symmetric_counts = all(raw[k] == raw[first+last-k] for k in range(first, last+1))
        require((interior == reflected) == symmetric_counts, "reflection about supported midrange")
        symmetric += symmetric_counts
        checked += 1
    return dict(histograms=checked, symmetric_histograms=symmetric)


def main():
    ap = ArgumentParser(description=__doc__)
    ap.add_argument("output_file", type=Path)
    output = ap.parse_args().output_file
    ports = walk_ports()
    layers = count_weights(ports)
    table = threshold_table()
    p = Q(5,8)
    tails = [Q(sum(layers[j:]),512) for j in (1,2,3)]
    require(tails == binomial_tails(3,p) == [Q(485,512),Q(350,512),Q(125,512)], "rank tails")
    require(average(tails) == p and tails[1]+tails[2] < 1, "tail sum and ordered complements")
    require(average([midpoint_ramp(x) for x in tails]) == maximum_monotone_average(tails) == Q(2,3),
            "sharp complementary-response upper endpoint")
    base = square_score(p)
    actual = average([square_score(u) for u in tails])
    require(base == Q(25,34) and base-Q(2,3) == Q(7,102) and actual <= Q(2,3),
            "nonlinear base exceeds every possible pooled reference")

    # Sharp types at p=0 and iid types at p=4/5 form a common-mean
    # counterexample to substituting the launch mean inside a binomial tail.
    mixed_p, weight = Q(4,5), Q(25,32)
    mixed_rival = weight*average([midpoint_ramp(x) for x in binomial_tails(3,mixed_p)])
    require(weight*mixed_p == p and mixed_rival == Q(25,32) > Q(2,3), "mixture control")
    # Joint state sqrt(1-p)|000>+sqrt(p)|111> and its dephased version.
    ghz_counts = [1-p, Q(0), Q(0), p]
    ghz_tails = [sum(ghz_counts[j:]) for j in (1,2,3)]
    require(ghz_tails == [p]*3 and average([square_score(u) for u in ghz_tails]) == base,
            "correlated copies pass invariance for a nonlinear detector")
    # Even parity with uniform masses is pairwise independent and not triple iid.
    even = [w for w in product((0,1),repeat=3) if sum(w)%2==0]
    require(all(len({(w[i], w[j]) for w in even}) == 4 for i,j in [(0,1),(0,2),(1,2)]),
            "all even-parity pair marginals are uniform")
    parity_tails = [Q(sum(sum(w)>=j for w in even),4) for j in (1,2,3)]
    require(parity_tails == [Q(3,4),Q(3,4),Q(0)] and average(parity_tails) == Q(1,2),
            "pairwise independence preserves the mean but changes the three-copy thresholds")
    tails48 = binomial_tails(48,p)
    bound48 = maximum_monotone_average(tails48)
    require(average(tails48) == p and bound48 == Q(61,96) < base, "48-copy upper bound")
    special = [Q(1,2) if k in (2,8) else Q(0) for k in range(9)]
    tails8 = [sum(special[j:]) for j in range(1,9)]
    require(tails8 == [Q(1)]*2 + [Q(1,2)]*6, "two certain and six midpoint tails")
    sym = (2+6*Q(1,2))/8  # Every sharp complementary response has these two values.
    raw = average([s*s for s in tails8])
    require(sym == p and raw == Q(7,16) and p-raw == Q(3,16), "port randomization masks this drift")
    cases = dict(product_three=[Q(x,512) for x in layers], ghz_three=ghz_counts,
                 pairwise_even=[Q(1,4),Q(0),Q(3,4),Q(0)], fixed_count=[Q(0),Q(1),Q(0)],
                 two_point_eight=special)
    dispersion_checks = {name: dispersion(weights) for name,weights in cases.items()}
    require(dispersion_checks["two_point_eight"]["variance"] == Q(9,64), "unconcentrated law")
    # Positive Taylor terms lower-bound exp(n * (7/204)^2) without libm.
    blocks = 2545
    exponent = blocks * Q(7,204)**2
    lower_exp = term = Q(1)
    for order in range(1, 21):
        term *= exponent/order
        lower_exp += term
    require(lower_exp > 20 and 4*blocks == 10180, "5 percent design and bank accounting")
    data = dict(physical_right_left_numerators=ports, site=1, site_mass=p,
                threshold_truth_table=table, triple_count_weights_over_512=layers, threshold_masses=tails,
                squared_base_rate=base, squared_threshold_average=actual, monotone_upper="2/3",
                guaranteed_base_gap="7/102", mixed_type_weights=["7/32","25/32"],
                mixed_type_masses=[0,mixed_p], mixed_threshold_rate=mixed_rival,
                correlated_tails=ghz_tails, correlated_squared_rate=base, even_parity_tails=parity_tails,
                forty_eight_copy_sharp_upper=bound48, dispersion=dispersion_checks,
                two_point_thresholds=tails8, two_point_symmetric_rate=sym,
                two_point_raw_square_rate=raw, two_point_raw_shortfall=p-raw,
                reflection_check=check_histogram_symmetry(), blocks_per_arm=blocks,
                bank_launches=4*blocks, decision_threshold="7/204")
    with output.open("x", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, indent=2, default=str)
        f.write("\n")


if __name__ == "__main__":
    main()
