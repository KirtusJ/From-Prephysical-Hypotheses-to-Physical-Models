"""Compare consecutive transport probes using integer path counts on two sheet registers."""

import argparse
import csv
import json
from collections import defaultdict
from fractions import Fraction
from itertools import product
from math import gcd
from pathlib import Path


def block(state, order, link, first_gain=1):
    for _ in range(3):
        out = defaultdict(int)
        for (x, incoming, y, z), value in state.items():
            for direction in (1, -1):
                destination = (x+direction, direction, (y+first_gain*x) % order, (z+link*x) % order)
                sign = -1 if incoming == direction == -1 else 1
                out[destination] += sign*value
        state = out
    return state


def record(state, site, direction):
    return {key: val for key, val in state.items() if key[:2] == (site, direction) and val}


def mass(state):
    return sum(value**2 for value in state.values())


def switched_block(state, order, first_gain, second_gain):
    """Literal three-step destructive record, including site-dependent translations."""
    (site, channel) = next(iter(state))[:2]
    return record(block(state, order, second_gain, first_gain), site-channel, -channel)


def relation_word(prime, target):
    state = {(0, 1, 0, 0): 1}
    state = switched_block(state, prime, 0, 1)
    for probe in range(prime):
        if probe != target:
            state = switched_block(state, prime, 1, -probe)
    before = mass(state)
    cosets = defaultdict(list)
    pos, direction = next(iter(state))[:2]
    for y, z in product(range(prime), repeat=2):
        cosets[(target*y+z) % prime].append(state.get((pos, direction, y, z), 0))
    constants = all(len(set(values)) == 1 for values in cosets.values())
    profile = [cosets[j][0] for j in range(prime)]
    support = [j for j in range(prime) if profile[j]]
    profiles_ok = (constants and sorted(profile) == [-1]+[0]*(prime-2)+[1]
                   and (support[1]-support[0]) % prime in (2, prime-2))
    rows = []
    for probe in range(prime):
        numerator = mass(switched_block(state, prime, 1, -probe))
        observed = Fraction(numerator, 8*before)
        difference = (target-probe) % prime
        predicted = (Fraction(0) if difference == 0 else
                     Fraction(3,8) if difference in (1, prime-1) else Fraction(1,4))
        rows.append(dict(probe=probe, count=numerator, conditional=str(observed),
                         predicted=str(predicted), agrees=(observed == predicted)))
    return dict(order=prime, target=target, blocks=prime, squared_count=before,
                success=str(Fraction(before, 8**prime)), translated_coset_profile=profile,
                cosets_match=profiles_ok, probes=rows)


def main(output):
    output.mkdir(parents=True, exist_ok=True)
    cases = 0
    checks = dict(destructive_preparation=True, complete_second_block=True,
                  all_joint_counts=True, common_relabelling=True, tagged_nulls=True)
    tag_rows = {}
    with (output/"relative_transport.csv").open("w", encoding="utf8", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(("M", "first_link", "second_link", "second_displacement",
                         "second_channel", "joint_numerator", "joint_denominator", "conditional"))
        for order in (3, 5, 7, 9, 11, 15):
            counts = {}
            units = [j for j in range(order) if gcd(j, order) == 1]
            # Rational-coefficient representation: a root is one iff its exponent is 0 mod M.
            nulls = {f"{a},{b}": [u for u in units if (2*(a-u*b)) % order == 0]
                     for a, b in product(units, repeat=2)}
            checks["tagged_nulls"] &= all(nulls[f"{a},{b}"] == [a*pow(b, -1, order) % order]
                                          for a, b in product(units, repeat=2))
            tag_rows[str(order)] = nulls
            for first in range(order):
                prepared = record(block({(0, 1, 0, 0): 1}, order, first), -1, -1)
                checks["destructive_preparation"] &= mass(prepared) == 2
                for second in range(order):
                    out = block(prepared, order, second)
                    checks["complete_second_block"] &= mass(out) == 16
                    for dx, channel in ((3,1), (1,-1), (1,1), (-1,-1), (-1,1), (-3,-1)):
                        value = mass(record(out, -1+dx, channel))
                        # Incoming L gives constructive (-1,L), destructive (+1,R).
                        expected = 2
                        if (dx, channel) == (-1, -1):
                            expected = 2 if first == second else 4
                        if (dx, channel) == (1, 1):
                            expected = 6 if first == second else 4
                        checks["all_joint_counts"] &= value == expected
                        counts[first, second, dx, channel] = value
                        writer.writerow((order, first, second, dx, channel, value, 64, str(Fraction(value, 16))))
                        cases += 1
            checks["common_relabelling"] &= all(
                value == counts[g*a % order, g*b % order, dx, channel]
                for (a,b,dx,channel), value in counts.items() for g in units)
    words = [relation_word(prime, target) for prime in (3,5,7,11,13,17,19)
             for target in range(1, prime)]
    checks["finite_relation_words"] = all(w["squared_count"] == 2*w["order"] and
                                         w["cosets_match"] for w in words)
    checks["all_followup_probes"] = all(p["agrees"] for w in words for p in w["probes"])
    report = dict(checks=checks, native_outcome_rows=cases, tagged_nulls_by_order=tag_rows,
                  exact_relation_words=words,
                  scope="Two shared-coin transport probes. Each tagged null list is exact modular arithmetic.")
    (output/"relative_transport.json").write_text(json.dumps(report, indent=2)+"\n", encoding="utf8")
    print(checks)
    if not all(checks.values()):
        raise SystemExit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    main(parser.parse_args().output)
