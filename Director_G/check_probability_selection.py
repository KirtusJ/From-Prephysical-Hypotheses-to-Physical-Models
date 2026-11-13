"""Exact five-sheet walk checks. Run with one argument, the output directory."""

import argparse
import csv
import itertools
import json
import math
from collections import defaultdict
from pathlib import Path


# Integral polynomials in z modulo 1 + z + z^2 + z^3 + z^4.
ZERO = (0, 0, 0, 0)
ONE = (1, 0, 0, 0)


def reduce_terms(terms):
    raw = [0] * 5
    for exponent, coefficient in terms:
        raw[exponent % 5] += coefficient
    return tuple(a - raw[4] for a in raw[:4])


def plus(a, b):
    return tuple(x + y for x, y in zip(a, b))


def scale(n, a):
    return tuple(n * v for v in a)


def times(a, b):
    return reduce_terms((i + j, x * y) for i, x in enumerate(a) for j, y in enumerate(b))


def conjugate_by(a, unit):
    return reduce_terms((unit * j, c) for j, c in enumerate(a))


def norm_square(a):
    return times(a, conjugate_by(a, -1))


def physical_paths(steps, initial):
    """Direct path enumeration on the real lift with its Hadamard denominator removed."""
    grouped = defaultdict(lambda: [0] * 5)
    for directions in itertools.product((1, -1), repeat=steps):
        x, y, coin, sign = 0, 0, initial, 1
        for d in directions:
            y = (y + x) % 5
            if coin == d == -1:
                sign = -sign
            x += d
            coin = d
        grouped[x, coin][y] += sign
    return grouped


def advance_sector(state, r):
    """Independent recursion on a tagged character, with denominator removed."""
    next_state = defaultdict(lambda: ZERO)
    for (x, coin), amplitude in state.items():
        transported = reduce_terms((j - r * x, c) for j, c in enumerate(amplitude))
        for d in (1, -1):
            gain = -1 if coin == d == -1 else 1
            key = (x + d, d)
            next_state[key] = plus(next_state[key], scale(gain, transported))
    return next_state


def walk_trials():
    rows = []
    tests = dict.fromkeys(("character_recursion", "tag_permutation", "localized_sheet_parseval",
                           "total_mass", "three_step_witness", "conjugate_orientation"), True)
    for initial in (1, -1):
        states = [{(0, initial): ONE} for _ in range(5)]
        for t in range(9):
            counts = physical_paths(t, initial)
            denominator = 2**t
            total = [ZERO] * 5
            for (x, coin), sheet in sorted(counts.items()):
                norm = [norm_square(state[x, coin]) for state in states]
                localized = sum(c * c for c in sheet)
                tests["localized_sheet_parseval"] &= sum_vectors(norm) == scale(5 * localized, ONE)
                for r, state in enumerate(states):
                    raw = reduce_terms((-r * y, c) for y, c in enumerate(sheet))
                    tests["character_recursion"] &= state[x, coin] == raw
                    tests["conjugate_orientation"] &= norm[r] == norm[-r % 5]
                    total[r] = plus(total[r], norm[r])
                    for u in (1, 2, 3, 4):
                        transformed = conjugate_by(norm[r], u)
                        tests["tag_permutation"] &= transformed == norm[(u * r) % 5]
                        rows.append((initial, t, x, coin, r, u, denominator, *transformed, localized))
                if (initial, t, x, coin) == (1, 3, 1, 1):
                    # Exact squared numerator is 2 + z^(2r) + z^(-2r).
                    tests["three_step_witness"] &= norm[2] == (1, 0, -1, -1)
                    tests["three_step_witness"] &= norm[4] == (2, 0, 1, 1)
            tests["total_mass"] &= all(w == scale(denominator, ONE) for w in total)
            if t < 8:
                states = [advance_sector(state, r) for r, state in enumerate(states)]
    return rows, tests


def sum_vectors(vectors):
    return tuple(map(sum, zip(*vectors)))


def field_controls():
    # Exhaust every pair in this predetermined alphabet.
    alphabet = list(itertools.product((-1, 0, 1), repeat=4))
    result = {}
    for u in (1, 2, 3, 4):
        failures = []
        for a, b in itertools.product(alphabet, repeat=2):
            wa = conjugate_by(norm_square(a), u)
            wb = conjugate_by(norm_square(b), u)
            wa_plus_b = conjugate_by(norm_square(plus(a, b)), u)
            wa_minus_b = conjugate_by(norm_square(plus(a, scale(-1, b))), u)
            residuals = {
                "balanced_mixing": plus(plus(wa_plus_b, wa_minus_b), scale(-2, plus(wa, wb))),
                "tensor_product": plus(conjugate_by(norm_square(times(a, b)), u), scale(-1, times(wa, wb))),
            }
            for name, residual in residuals.items():
                if residual != ZERO:
                    failures.append([name, a, b, residual])
        result[u] = dict(pairs=len(alphabet)**2, failures=failures)
    return result


def collision_trial(contact):
    """Two common-sheet steps followed by an optional independently timed Bob step."""
    state = {(0, 1, 0, 1): ONE}
    for _ in range(2):
        target = defaultdict(lambda: ZERO)
        for (x, a, y, b), v in state.items():
            displacement = x + y + contact * (x == y)
            shifted = reduce_terms((j - 2 * displacement, c) for j, c in enumerate(v))
            for c, d in itertools.product((1, -1), repeat=2):
                sign = (-1)**(int(a == c == -1) + int(b == d == -1))
                key = (x + c, c, y + d, d)
                target[key] = plus(target[key], scale(sign, shifted))
        state = target
    mixed = defaultdict(lambda: ZERO)
    for (x, a, y, b), v in state.items():
        shifted = reduce_terms((j - 2*y, c) for j, c in enumerate(v))
        for d in (1, -1):
            key = (x, a, y + d, d)
            mixed[key] = plus(mixed[key], scale(-1 if b == d == -1 else 1, shifted))
    result = []
    for p in (2, 4):
        row_masses = []
        totals = []
        for output in (state, mixed):
            weights = defaultdict(lambda: ZERO)
            for (x, a, y, b), value in output.items():
                w = norm_square(value)
                weights[x, a] = plus(weights[x, a], w if p == 2 else times(w, w))
            row_masses.append(weights)
            totals.append(sum_vectors(weights.values()))
        for key in sorted(row_masses[0]):
            m, n = (weights[key] for weights in row_masses)
            unchanged = times(m, totals[1]) == times(n, totals[0])
            result.append(dict(contact=contact, p=p, alice_site=key[0], alice_coin=key[1], unchanged=unchanged,
                               before_ratio=[m, totals[0]], after_ratio=[n, totals[1]]))
    return result


def main(out):
    out.mkdir(parents=True, exist_ok=True)
    rows, checks = walk_trials()
    field = field_controls()
    checks["all_algebraic_pairs"] = all(not d["failures"] for d in field.values())
    collision = collision_trial(0) + collision_trial(1)
    checks["collision_and_free_controls"] = all(row["unchanged"] == (row["p"] == 2 or row["contact"] == 0)
                                                for row in collision)
    with (out / "probability_walk_trials.csv").open("w", encoding="utf8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(("initial_direction", "steps", "x", "direction", "character", "embedding_unit",
                         "denominator", "constant", "z", "z_squared", "z_cubed", "localized_numerator"))
        writer.writerows(rows)
    q = (math.sqrt(5) - 1) / 2
    conjugate_q = -(math.sqrt(5) + 1) / 2
    stress = []
    for n in range(17):
        w, other = q**(2*n), conjugate_q**(2*n)
        stress.append(dict(power=n, weight=w, other_weight=other, binary_record=w/(1+w),
                           other_binary_record=other/(1+other)))
    escorts = []
    for p in (0.5, 1, 1.5, 2, 3, 4):
        after = 2**p / (2**p + 2)
        amplitude = math.sqrt(2)
        mixed_weights = (amplitude**p, 2 * (1/amplitude)**p)
        direct = mixed_weights[0] / sum(mixed_weights)
        escorts.append(dict(p=p, before=2/3, after=after, after_from_amplitudes=direct))
    checks["flag_witness"] = all(abs(d["after"] - d["after_from_amplitudes"]) < 1e-14 for d in escorts)
    checks["opposite_convergence"] = all(a["weight"] > b["weight"] and a["other_weight"] < b["other_weight"]
                                          for a, b in zip(stress, stress[1:]))
    dilation = []
    for real_q in (q, conjugate_q):
        for root_two in (math.sqrt(2), -math.sqrt(2)):
            entry = real_q + root_two - 2
            dilation.append(dict(q=real_q, root_two=root_two, proposed_entry=entry,
                                 necessary_residual_weight=1-entry**2))
    checks["five_sheet_dilation_selector"] = [d["necessary_residual_weight"] > 0 for d in dilation] == [
        True, False, False, False]
    report = dict(checks=checks, native_endpoint_rows=len(rows), field_controls=field, collision_rows=collision,
                  flag_power_controls=escorts, ordered_embedding_stress=stress, dilation_selector=dilation,
                  constructive_tag_r2=(3+math.sqrt(5))/16, constructive_tag_r2_under_u2=(3-math.sqrt(5))/16,
                  numerical_scope="Exact integer polynomial trials. Power, closed-form and convergence illustrations use binary64.")
    (out / "probability_selection.json").write_text(json.dumps(report, indent=2, allow_nan=False)+"\n", encoding="utf8")
    print(checks, len(rows))
    if not all(checks.values()):
        raise SystemExit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    main(parser.parse_args().output)
