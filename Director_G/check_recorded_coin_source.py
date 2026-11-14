"""Check the three recorded coins, all four late switch settings and their blind cases."""

from argparse import ArgumentParser
from fractions import Fraction as Q
from itertools import product
import json
from pathlib import Path


SETTINGS = list(product((False, True), repeat=2))  # False = split, True = pooled
WELLS = 24


def need(condition, description):
    if not condition:
        raise ValueError(description)


def route_tables(coins, initial, phase):
    """One path per protected (initial rail, output rails) label. A Gaussian
    rational amplitude is stored as a signed rational and a power of i."""
    tables = [[Q(0)] * WELLS for _ in SETTINGS]
    by_word = {}
    labels = []
    for rail0, *outgoing in product(range(2), repeat=4):
        x, rail = 0, rail0
        amplitude, ipower = initial[rail], phase * rail
        flips = []
        for tick, (next_rail, (stay, flip)) in enumerate(zip(outgoing, coins)):
            change = rail != next_rail
            flips.append(int(change))
            # D_out * [[stay, -flip], [flip, stay]] * D_in, with unit
            # diagonal phases. Each stage has the prescribed flip modulus.
            amplitude *= (-flip if rail == 1 else flip) if change else stay
            ipower += phase * ((tick + 1) * rail + (tick + 2) * next_rail)
            rail = next_rail
            x += 1 if rail == 0 else -1
        amplitude *= (1, 1, -1, -1)[ipower % 4]
        real, imaginary = (amplitude, 0) if ipower % 2 == 0 else (0, amplitude)
        mass = real * real + imaginary * imaginary
        word = tuple(flips)
        by_word[word] = by_word.get(word, 0) + mass
        prefix = word[:2]
        site = {(0, 1): -4, (1, 0): 0}.get(prefix, 4)
        final_rail = int(site != 4)
        nright = (9 + site - x) // 2
        nright_early = nright - int(final_rail == 0)
        moves = [0] * nright_early + [1] * (8 - nright_early) + [final_rail]
        need(len(moves) == 9, "routing clock")
        for desired in moves:
            if rail != desired:
                rail = 1 - rail
            x += 1 if rail == 0 else -1
        need((x, rail) == (site, final_rail), "arrival well/rail")
        label_destinations = []
        for table, (pool_a, pool_b) in zip(tables, SETTINGS):
            split = (site == -4 and not pool_a) or (site == 0 and not pool_b)
            late_rail = 1 - rail if split and flips[-1] else rail
            destination = (x + (1 if late_rail == 0 else -1)) % WELLS
            table[destination] += mass
            label_destinations.append(destination)
        labels.append((mass, label_destinations))
    return tables, by_word, labels


def product_tables(q):
    u, v = (1 - q[0]) * q[1], q[0] * (1 - q[1])
    s = 1 - u - v
    tables = []
    for pool_a, pool_b in SETTINGS:
        table = [Q(0)] * WELLS
        table[5] = s
        for site, mass, pooled in [(-4, u, pool_a), (0, v, pool_b)]:
            table[site - 1] = mass if pooled else mass * (1 - q[2])
            table[site + 1] = 0 if pooled else mass * q[2]
        tables.append(table)
    return tables, u, v, s


def spectator(tables, score):
    scores = [[score(w) for w in bank] for bank in tables]
    norms = list(map(sum, scores))
    rates = [row[5] / z for row, z in zip(scores, norms)]
    c = rates[0] - rates[1] - rates[2] + rates[3]
    z, zb, za, zab = norms
    a, b = za - z, zb - z
    need(zab == z + a + b, "additive changes to normalizer")
    need(c == scores[0][5] * a * b * (z + zab) / (z * za * zb * zab), "sign identity")
    if a * b >= 0:
        upper = max(norms)
        need(c >= 2 * scores[0][5] * abs(a * b) / upper**3, "finite-error inequality")
    return dict(rates=rates, contrast=c, gaps=[a, b])


def run():
    coins = [(Q(1), Q(0)), (Q(0), Q(1)), (Q(3, 5), Q(4, 5)), (Q(12, 13), Q(5, 13))]
    starts = [(Q(1), Q(0)), (Q(3, 5), Q(4, 5))]
    checks = active = blind = 0
    identity = lambda w: w
    square = lambda w: w * w
    concave = lambda w: 2 * w - w * w
    for triplet, initial, phase in product(product(coins, repeat=3), starts, (0, 1)):
        q = [flip * flip for _, flip in triplet]
        tables, words, labels = route_tables(triplet, initial, phase)
        expected, u, v, s = product_tables(q)
        need(tables == expected and all(sum(t) == 1 for t in tables), "exact 24-well law")
        for word, recorded in words.items():
            weight = Q(1)
            for change, flip_probability in zip(word, q):
                weight *= flip_probability if change else 1 - flip_probability
            need(recorded == weight, "flip-word mass")
        # For any positive power within a protected label, the only occupied
        # well wins. Aggregate these conditional responses with sector mass.
        for k, table in enumerate(tables):
            label_law = [Q(0)] * WELLS
            for mass, destinations in labels:
                label_law[destinations[k]] += mass
            need(label_law == table, "label-conditioned alternative")
        informative = s > 0 and u > 0 and v > 0 and 0 < q[2] < 1
        for score in (square, concave):
            result = spectator(tables, score)
            need((result["contrast"] > 0) == informative, "strict-curvature test")
            if q[0] == q[1]:
                need(result["gaps"][0] == result["gaps"][1], "matched packet")
        need(spectator(tables, identity)["contrast"] == 0, "ordinary null")
        checks += 1
        active += int(informative)
        blind += int(not informative)

    # u=1/16 and v=9/16; the first packet meets only the lower kink.
    q = [Q(3, 4), Q(1, 4), Q(1, 2)]
    tables, _, _, _ = product_tables(q)
    def mixed_curvature(w):
        return w + max(0, w-Q(1, 24)) - Q(3, 2)*max(0, w-Q(1, 4))
    negative = spectator(tables, mixed_curvature)
    need(negative["gaps"][0] > 0 > negative["gaps"][1] and negative["contrast"] < 0,
         "increasing nonconvex counterexample")
    positive = spectator(tables, square)
    mix = positive["contrast"] / (positive["contrast"] - negative["contrast"])
    need(0 < mix < 1 and mix*negative["contrast"] + (1-mix)*positive["contrast"] == 0,
         "unmatched sources admit exact mixture cancellation for unrestricted scores")
    near_dark = []
    for denominator in (4, 16, 64, 256):
        q = Q(1, denominator)
        tables, _, _, _ = product_tables((q, q, Q(1, 2)))
        near_dark.append(spectator(tables, square)["contrast"])
    need(all(a > b > 0 for a, b in zip(near_dark, near_dark[1:])), "nonuniform sensitivity")
    return dict(circuits=checks, active=active, blind=blind, settings=["SS", "SP", "PS", "PP"],
                increasing_mixed_curvature=negative, squared_same_source=positive,
                cancelling_mixed_curvature_fraction=mix, near_dark_square_contrasts=near_dark)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    result = run()
    with args.output.open("x", encoding="utf-8", newline="\n") as output:
        json.dump(result, output, default=str, indent=2)
        output.write("\n")
