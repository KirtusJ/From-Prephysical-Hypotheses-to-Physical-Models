"""Reconstruct the routed staircase experiment from port and sheet coordinates.

Run python -B check_routed_sheet_filter.py OUTDIR. The archive must be new.
"""
import argparse
import json
from collections import Counter, defaultdict
from fractions import Fraction as Q
from itertools import product
from math import gcd, isqrt
from pathlib import Path


def require(condition, explanation):
    if not condition:
        raise ValueError(explanation)


def complement(s):
    return "".join("L" if i == "R" else "R" for i in s)


def build_arm(m, lag):
    ceiling = max(4, 1+isqrt(m-2))
    a = ceiling + (ceiling-lag) % 2
    pairs = (a*a-lag)//2
    full, rest = divmod(pairs, a-1)
    inversions = [a-1]*full + ([rest] if rest else [])
    inversions += [0]*(a-1-len(inversions))
    middle = []
    rights = 0
    for n in inversions:
        new = (a-1)-n-rights
        require(new >= 0, "misordered inversion counts")
        middle.extend("R"*new+"L")
        rights += new
    middle.extend("R"*(a-1-rights))
    return "R"+"".join(middle)+"L"


def lifted(word, home):
    x, gain, area = home, 0, 0
    for i in word:
        gain += x//2
        area += x-home
        x += 1 if i == "R" else -1
    return x, gain, area


def stream(field, m, coin):
    after = defaultdict(Counter)
    for (x, rail), state in field.items():
        outputs = ("RL" if coin == "H" else
                   (rail if coin == "I" else complement(rail)))
        for y in outputs:
            sign = -1 if coin == "H" and rail == y == "L" else 1
            dst = after[(x+(1 if y == "R" else -1)) % (4*m), y]
            for g, value in state.items():
                dst[(g+x//2) % m] += sign*value
    return {port: Counter({g: a for g, a in vals.items() if a})
            for port, vals in after.items() if any(vals.values())}


def cyclic_correlations(poly, m):
    result = Counter()
    for j, a in poly.items():
        for k, b in poly.items():
            result[(j-k) % m] += a*b
    return {k: v for k, v in result.items() if v}


def probe(m, lag, home, source):
    word = build_arm(m, lag)
    direct, reflected = lifted(word, home), lifted(complement(word), home)
    require(direct[0] == reflected[0] == home and direct[2] == lag and
            direct[1]-reflected[1] == lag, "incorrect area, endpoint or sheet gap")
    field = stream({(home, source): {0: 1}}, m, "H")
    for u, v in zip(word, word[1:]):
        field = stream(field, m, "I" if u == v else "X")
    require(set(field) == {(home, "R"), (home, "L")}, "route did not refocus")
    observed = stream(field, m, "H")
    for out in "RL":
        x = (home+(1 if out == "R" else -1)) % (4*m)
        selected = {(x, out): observed[x, out]} if (x, out) in observed else {}
        reset = stream(selected, m, "X")
        require(all(pos == (home, complement(out)) for pos in reset), "wrong reset")
        corr = cyclic_correlations(reset.get((home, complement(out)), {}), m)
        sign = 1 if source == out else -1
        expected = Counter({0: 2})
        expected[lag % m] += sign
        expected[-lag % m] += sign
        require(corr == {j: v for j, v in expected.items() if v},
                "wrong signed analyzer probability polynomial")
    return dict(word=word, mirror=complement(word), ticks=len(word)+2,
                arm_departure_gains=[direct[1], reflected[1]])


def native_census():
    rows = []
    samples = []
    for m in (3, 4, 5, 6, 7, 8, 9, 12, 16, 17, 21, 31, 32, 63, 64, 101, 128):
        homes = (0, 1, 4*m-1)
        total = max_ticks = 0
        for lag, home, source in product(range(m), homes, "RL"):
            data = probe(m, lag, home, source)
            if m in (5, 12, 31) and home == 4*m-1 and source == "L" and lag in (0, 1, m-1):
                samples.append(dict(order=m, home=home, source=source, lag=lag, **data))
            max_ticks = max(max_ticks, data["ticks"])
            total += 1
        # The cosine decoder's means follow from complete root sums; the
        # rational decoder below uses exact integer differences of its table.
        means = [Q(int((s-1) % m == 0)+int((s+1) % m == 0), 2) for s in range(m)]
        require([s for s, mu in enumerate(means) if mu] == [1, m-1]
                and sum(means) == 1, "character projection alias")
        units = [s for s in range(m) if gcd(s, m) == 1]
        # In a routed unit or anti-unit arm, exact outcome zeros occur at
        # s*lag == 0 (difference) or 2*s*lag == M modulo 2M (sum).
        for lag in range(m):
            support = {((s*lag) % m != 0, (2*s*lag-m) % (2*m) != 0) for s in units}
            require(len(support) == 1, "primitive exact-zero discrimination")
        f = [m-4*min(j, m-j) for j in range(m)]
        diffs = {j: 2*f[j]-f[j-1]-f[(j+1)%m] for j in range(m)}
        sparse = {j: a for j, a in diffs.items() if a}
        m2 = m//2
        expected = {0: 8, m2: -8} if m % 2 == 0 else {0: 8, m2: -4, m2+1: -4}
        require(sparse == expected and sum(f) == m % 2, "triangle DFT numerators")
        rows.append(dict(M=m, homes=homes, tested_source_rails=["R", "L"],
                         physical_probes=total, all_lags=m, maximum_streams=max_ticks,
                         integer_triangle_laplacian=sparse,
                         triangle_DC=str(Q(sum(f), m*m)),
                         nonzero_character_score_means=[[1, "1/2"], [m-1, "1/2"]],
                         primitive_sector_count=len(units)))
    return dict(census=rows, explicit_routes=samples)


def acceptance_probability(one, repetitions):
    tally = {0: Q(1)}
    for _ in range(repetitions):
        next_tally = Counter()
        for x, p in tally.items():
            for z, weight in one.items():
                next_tally[x + z] += p * weight
        tally = next_tally
    require(sum(tally.values()) == 1, "probability lost in repeated probes")
    return sum((p for x, p in tally.items() if 4 * x >= repetitions), Q(0))


def exact_uniform_test_4(repetitions):
    # For order four cos(l*pi/2) is 1,0,-1,0. Testing mean Z>=1/4
    # has an exactly enumerable law under every sector and both input rails.
    cos4 = (1, 0, -1, 0)
    result = []
    accepted = []
    for s in range(4):
        one = Counter()
        for lag, y in product(range(4), (-1, 1)):
            one[y*cos4[lag]] += Q(1+y*cos4[(s*lag) % 4], 8)
        p_acc = acceptance_probability(one, repetitions)
        mean = sum(q*z for z, q in one.items())
        require(mean == (Q(1, 2) if s in (1, 3) else 0), "mean score")
        result.append(dict(s=s, accept=str(p_acc), reject=str(1-p_acc),
                           single_score_law={str(j): str(q) for j, q in sorted(one.items())}))
        accepted.append(p_acc)
    # Each fixed setting has a fair output under both rivals. The memory
    # rival chooses one fair sign for the whole sequence, including ties.
    count_scores = Counter()
    memory_scores = {bit: Counter() for bit in (-1, 1)}
    for lag, f in enumerate(cos4):
        for y in (-1, 1):
            count_scores[y * f] += Q(1, 8)
        lag_sign = 1 if f >= 0 else -1
        require({bit * lag_sign for bit in memory_scores} == {-1, 1},
                f"memory rival changed a single-probe marginal at lag {lag}")
        for bit, one in memory_scores.items():
            one[bit * lag_sign * f] += Q(1, 4)
    count_accept = acceptance_probability(count_scores, repetitions)
    memory_accept = sum(acceptance_probability(one, repetitions)
                        for one in memory_scores.values()) / 2
    require(count_accept == accepted[0] and memory_accept == accepted[1] / 2,
            "independent and persistent-rail controls at order four")
    return dict(order=4, repeats=repetitions, sectors=result,
                conditional_fair_count_accept=str(count_accept),
                same_marginal_hidden_bit_accept=str(memory_accept),
                original_launch_acceptance=str(sum(accepted)/4),
                original_launch_rejection=str(1-sum(accepted)/4),
                target_posterior=str((accepted[1]+accepted[3])/sum(accepted)))


def rejection_sampler():
    result = []
    for m, batches in ((3, 2), (4, 2), (5, 3), (17, 3), (32, 1)):
        width = (m-1).bit_length()
        match = Q(m, 2**width)
        fail = (1-match)**batches
        success_per_lag = sum((1-match)**i for i in range(batches))/2**width
        require(m*success_per_lag+fail == 1, "finite sampler normalization")
        result.append(dict(order=m, batches=batches, bits=width,
                           timeout=str(fail), unconditional_each_lag=str(success_per_lag),
                           max_sampler_ticks=2*width*batches))
    # A native fair rail read does not filter the sheet conditional on either
    # result. The polynomial after the X return must be a single signed monomial.
    for m, rail, home in product((3, 5, 8), "RL", (0, 1)):
        first = stream({(home, rail): {0: 1}}, m, "H")
        for port, poly in first.items():
            back = stream({port: poly}, m, "X")
            require(set(back) == {(home, complement(port[1]))} and
                    list(map(abs, next(iter(back.values())).values())) == [1],
                    "native random bit biased by sheet")
    return result


def controls():
    # At M=5, an identically zero lag and a copied, unerased arm separately
    # destroy statistical identifiability. At lag one, the ideal coherent
    # cross-numerator is z+z^-1; neither classical relabeling nor reading
    # which arm and pooling the two cases recreates it.
    word = build_arm(5, 1)
    top, low = lifted(word, 0)[1], lifted(complement(word), 0)[1]
    tagged = Counter(cyclic_correlations({top % 5: 1}, 5))
    tagged.update(cyclic_correlations({low % 5: 1}, 5))
    coherent = cyclic_correlations({top % 5: 1, low % 5: 1}, 5)
    require(dict(tagged) == {0: 2} and coherent == {0: 2, 1: 1, 4: 1},
            "recorded arm lost its control")
    n = len(word)
    # All H projection onto the two prescribed paths requires rail-relative
    # checks, a separate apparatus; success before the last H is 2^(1-n).
    return dict(tagged_arm_lag1_numerator=dict(tagged), coherent_lag1_numerator=coherent,
                both_analyzer_denominator=4, fixed_lag_zero_score_all_sectors=1,
                fixed_H_two_word_port_success_before_analyzer=str(Q(2, 2**n)),
                example_order=5, selected_word=word)


def run():
    return dict(native=native_census(), exact_full_launch_example=exact_uniform_test_4(16),
                rational_decoder=dict(score="Y*(1-4*fold(lag,M)/M)",
                                      target_lower="2/5", rival_upper="1/9", threshold="1/4",
                                      minimum_margin="5/36", Hoeffding_exponent_per_probe="25/2592"),
                native_randbelow=rejection_sampler(), failure_controls=controls())


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("directory", type=Path)
    target = cli.parse_args().directory/"routed_sheet_filter.json"
    result = run()
    target.parent.mkdir(exist_ok=True, parents=True)
    with target.open("x", encoding="utf8", newline="\n") as f:
        json.dump(result, f, sort_keys=True, separators=(",", ":"))
        f.write("\n")
