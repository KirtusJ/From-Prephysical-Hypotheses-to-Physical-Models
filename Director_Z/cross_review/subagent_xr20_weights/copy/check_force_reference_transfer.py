"""Verify a post-preparation, base-only force reference on the same physical walk.

Run with a destination directory. All probabilities and correlations use integers
or fractions. No separate phase generator, right-rail reset, or sheet read.
"""

import argparse
import json
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import product
from pathlib import Path


def advance(amplitude, paths, order):
    out, counts = Counter(), Counter()
    for (x, coin, y), value in amplitude.items():
        for direction in (1, -1):
            sign = -1 if coin == direction == -1 else 1
            out[x + direction, direction, (y + x) % order] += sign * value
    for (x, coin), multiplicity in paths.items():
        for direction in (1, -1):
            counts[x + direction, direction] += multiplicity
    return out, counts


def by_port(amplitude, order):
    ports = defaultdict(lambda: [0] * order)
    for (x, coin, y), value in amplitude.items():
        ports[x, coin][y] += value
    return dict(ports)


def square_norm(vector):
    return sum(v * v for v in vector)


def realized_gram(ports, order):
    return [sum(v[i] * v[(i + h) % order] for v in ports.values()
                for i in range(order)) for h in range(order)]


def basis_paths(order, start, coin, depth):
    """Independent individual direction-word oracle, including the incoming coin."""
    ports, unsigned = defaultdict(lambda: [0] * order), Counter()
    for word in product((1, -1), repeat=depth):
        x, previous, gain, sign = start, coin, 0, 1
        for direction in word:
            gain += x
            if previous == direction == -1:
                sign *= -1
            previous = direction
            x += direction
        ports[x, previous][gain % order] += sign
        unsigned[x, previous] += 1
    return ports, unsigned


def one_left_row(order, start, coin, n):
    # The one opposite step moves through the first n ticks. Use its
    # earliest possible placement to set the origin, then advance by 2c.
    x, first_gain = start, 0
    for direction in [-coin] + [coin] * n:
        first_gain += x
        x += direction
    sign = 1 if coin == 1 or (n - 1) % 2 == 0 else -1
    row = [0] * order
    for index in range(n):
        row[(first_gain + 2 * coin * index) % order] += sign
    return row


def certify_launches():
    rows = []
    for order in (3, 4, 5, 6, 8, 12):
        checked, wrap, nonzero_origin = 0, 0, 0
        for start in (-3, 0, 7):
            for coin in (1, -1):
                for n in range(1, order // (2 if order % 2 == 0 else 1) + 2):
                    depth = n + 1
                    ports, unsigned = basis_paths(order, start, coin, depth)
                    target = (start + coin * (n - 1), coin)
                    assert unsigned[target] == n
                    assert ports[target] == one_left_row(order, start, coin, n)
                    check_gram = realized_gram({target: ports[target]}, order)
                    pair_gaps = Counter((2 * (i - j)) % order
                                        for i in range(n) for j in range(n))
                    assert check_gram == [pair_gaps[h] for h in range(order)]
                    checked += 1
                    nonzero_origin += start != 0
                    wrap += square_norm(ports[target]) > n
        rows.append(dict(order=order, launches_tested=checked,
                         nonzero_origin_cases=nonzero_origin, first_wrap_cases=wrap))
    return rows


def diagnostic(order, depth_prep=5, window=None):
    # Use exact localized lift plus an initially 1/2 route-count component.
    amplitude, paths = {(0, 1, 0): 1}, {(0, 1): 1}
    for _ in range(depth_prep):
        amplitude, paths = advance(amplitude, paths, order)
    ports = by_port(amplitude, order)
    if window is not None:
        ports = {port: v for port, v in ports.items() if port == window}
        paths = {port: number for port, number in paths.items() if port == window}
    path_mass = sum(paths.values())
    coherent_mass = sum(square_norm(v) for v in ports.values())
    total = path_mass + coherent_mass
    gram = realized_gram(ports, order)
    assert gram[0] == coherent_mass and total > 0
    rows = []
    m = order // (2 if order % 2 == 0 else 1)
    for n in range(1, m + 2):
        t = n + 1
        grouped_count, grouped_coherent = 0, 0
        all_count, all_coherent = 0, 0
        for (x, coin), vec in ports.items():
            local = {(x, coin, y): val for y, val in enumerate(vec) if val}
            unsigned = {(x, coin): paths[x, coin]}
            for _ in range(t):
                local, unsigned = advance(local, unsigned, order)
            cells = by_port(local, order)
            target = (x + coin * (n - 1), coin)
            grouped_coherent += square_norm(cells.get(target, []))
            grouped_count += unsigned[target]
            all_coherent += sum(square_norm(v) for v in cells.values())
            all_count += sum(unsigned.values())
        assert all_coherent == coherent_mass * 2**t
        assert all_count == path_mass * 2**t
        predicted = n * path_mass + n * coherent_mass + 2 * sum(
            (n - lag) * gram[(2 * lag) % order] for lag in range(1, n))
        assert grouped_count == n * path_mass
        assert grouped_count + grouped_coherent == predicted
        rows.append(dict(n=n, count_raw=grouped_count, coherent_raw=grouped_coherent,
                         p=str(Fraction(predicted, total * 2**t))))
    return dict(order=order, accepted_port=window, incoming_rail_populations=[
        dict(coin=c, paths=sum(v for (x, d), v in paths.items() if d == c),
             coherent=sum(square_norm(v) for (x, d), v in ports.items() if d == c))
        for c in (1, -1)], paths=path_mass, coherent=coherent_mass,
        prior_herald_probability=str(Fraction(total, 2**(depth_prep + 1))),
        post_count_weight=str(Fraction(path_mass, total)), sheet_gram=gram, rows=rows)


def gauge_checks():
    # Difference of two area histories with common start and time is even.
    # In an even cycle, evaluating the shifted character multiplies every
    # history from start x by (-1)^(t*x+t*(t-1)/2), independent of its route.
    tests = {}
    for order in (4, 6, 8, 10, 12, 16):
        trials = 0
        for start in (-3, 0, 1):
            for t in range(1, 8):
                for word in product((1, -1), repeat=t):
                    x, area = start, 0
                    for d in word:
                        area += x
                        x += d
                    # Express the equal sign by final position x and time.
                    assert (area - (t * x + t * (t + 1) // 2)) % 2 == 0
                    for s in {0, 1, order // 2 - 1}:
                        difference = (s + order // 2) * area - s * area
                        assert difference % order == ((t*x+t*(t+1)//2)*order//2) % order
                        trials += 1
        tests[order] = trials
    return tests


def launch_rail_control():
    # Applying the (1,R) terminal score regardless of the measured incoming
    # rail would corrupt the comparison. At order five tick five is enough.
    entries = []
    for incoming in (1, -1):
        ports, _ = basis_paths(5, 0, incoming, 5)
        entries.append(dict(incoming=incoming,
                            fixed_positive_port=str(Fraction(square_norm(ports[1, 1]), 32)),
                            reflected_port=str(Fraction(square_norm(ports[incoming, incoming]), 32))))
    assert [r["fixed_positive_port"] for r in entries] == ["1/8", "1/4"]
    assert [r["reflected_port"] for r in entries] == ["1/8", "1/8"]
    return entries


def measured_shared_and_reprepared():
    # Physically generate the two outcome probabilities from a single
    # localized lift. Measure a bright three-tick output; the returned
    # physical sheet vector is the input to the second test.
    entries = []
    for m in (3, 4, 5, 6, 8, 12):
        ports, count_paths = basis_paths(m, 0, 1, 3)
        first = ports[1, 1]
        count1 = count_paths[1, 1]
        a, p = {(1, 1, y): v for y, v in enumerate(first) if v}, {(1, 1): count1}
        for _ in range(3):
            a, p = advance(a, p, m)
        retained = by_port(a, m)[2, 1]
        p1 = Fraction(square_norm(first) + count1, 2 * 2**3)
        p2 = Fraction(square_norm(retained) + p[2, 1], 2 * 2**6)
        entries.append(dict(order=m, marginal=str(p1), shared=str(p2),
                            reset_independent=str(p1*p1), difference=str(p2-p1*p1)))
    assert [r["difference"] for r in entries] == ["1/64", "1/32", "1/64",
                                                    "1/64", "1/64", "1/64"]
    return entries

def gram_controls():
    # These two full coherent states differ by an independent minus sign
    # at the occupied left rail. Their sheet marginal is the same.
    models = []
    for phase in (1, -1):
        local = {(0, 1, 0): 1, (0, -1, 0): phase}
        ports = by_port(local, 5)
        evolved, _ = advance(local, {}, 5)
        out = by_port(evolved, 5)
        p = Fraction(square_norm(out[1, 1]), 4)
        models.append(dict(relative_sign=phase, sheet_gram=realized_gram(ports, 5),
                           flight_p_right=str(p)))
    assert models[0]["sheet_gram"] == models[1]["sheet_gram"]
    assert [m["flight_p_right"] for m in models] == ["1", "0"]
    return models


def repeated_launch():
    # Use a real sheet with weights 1/5 on k=0 and 4/5 on k=±1 at M=8
    # (symmetrically on the conjugate pair). At h=2 the cosines are 1,0.
    # Include count weight 1/2 in the complete ensemble. Each bright event
    # has probability (1+cos)/4; counting gives 1/4.
    weights = [Fraction(1, 2), Fraction(1, 10), Fraction(2, 5)]
    bright = [Fraction(1, 4), Fraction(1, 2), Fraction(1, 4)]
    p = sum(w*q for w, q in zip(weights, bright))
    shared = sum(w*q*q for w, q in zip(weights, bright))
    redrawn = p*p
    assert shared > redrawn
    return dict(weights=list(map(str, weights)), categories=["count", "k=0", "k=±1"],
                bright_by_category=list(map(str, bright)), marginal=str(p),
                persistent_pair=str(shared), independently_redrawn_pair=str(redrawn),
                persistent_minus_redrawn=str(shared - redrawn))


def main(out):
    baseline = [diagnostic(m) for m in (3, 4, 5, 6, 8, 12)]
    heralds = [diagnostic(m, window=(1, 1)) for m in (3, 4, 5, 6, 8, 12)]
    assert [r["post_count_weight"] for r in heralds] == [
        "1", "3/7", "3/5", "1", "1/2", "3/5"]
    results = dict(protocol="Shared localized launch and five force ticks before arm choice. "
             "Diagnostic reads both base variables, keeps every outcome, follows its measured rail "
             "with an oriented relative terminal score; sheet never measured. Flight arm omits reset.",
             geometry="Line; integer departure x, signed Hadamard, incoming R; exact 2^t normalization. "
             "The initial ensemble gives half to persistent route counting and half to a localized physical sheet.",
             all_launches=certify_launches(), all_outcomes=baseline, conditional_herald_and_reset=heralds,
             alias_path_checks=gauge_checks(), equal_sheet_different_flight=gram_controls(),
             shared_vs_redrawn=repeated_launch(),
             physical_repeat=measured_shared_and_reprepared(), wrong_incoming=launch_rail_control())
    out.mkdir(parents=True, exist_ok=True)
    (out / "force_reference_transfer.json").write_bytes(
        (json.dumps(results, ensure_ascii=True, indent=2) + "\n").encode("utf-8"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_directory", type=Path)
    main(parser.parse_args().output_directory)

