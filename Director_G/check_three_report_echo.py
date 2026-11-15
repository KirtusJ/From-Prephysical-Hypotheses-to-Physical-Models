"""Outward-rounded certificates for coherent echoes compared with three binary reports."""

import argparse
from fractions import Fraction
from itertools import product
import json
from pathlib import Path


GRID = 10**48
BAND = (GRID // 8, 7 * GRID // 8)


def two_tick_source():
    amplitudes = {}
    for word in product(("R", "L"), repeat=2):
        x, rail, amplitude = 0, "R", 1
        for next_rail in word:
            if rail == next_rail == "L":
                amplitude = -amplitude
            x += 1 if next_rail == "R" else -1
            rail = next_rail
        port = (x, rail)
        amplitudes[port] = amplitudes.get(port, 0) + amplitude
    total = sum(n * n for n in amplitudes.values())
    return total, amplitudes, Fraction(total - amplitudes[(0, "R")] ** 2, total)


def numerator(action, x):
    """Raw numerator of F(x / GRID) over GRID cubed."""
    if action == "D":
        return x**3
    return GRID**3 - (GRID - x)**3


def child_bounds(action, lo, hi):
    divisor = GRID**2
    return numerator(action, lo) // divisor, -(-numerator(action, hi) // divisor)


def schedule(x, depth):
    lo = hi = int(x * GRID)
    assert Fraction(lo, GRID) == x
    words = []
    for _ in range(depth):
        if 2 * hi <= GRID:
            action = "U"
        elif 2 * lo > GRID:
            action = "D"
        else:
            raise ArithmeticError("Precision insufficient to select the threshold branch")
        words.append(action)
        lo, hi = child_bounds(action, lo, hi)
        assert BAND[0] <= lo <= hi <= BAND[1]
    return "".join(words)


def lower_inverse(action, target):
    """Greatest grid point with F(x) <= target/GRID; includes exact equality."""
    lo, hi = 0, GRID
    rhs = target * GRID**2
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if numerator(action, mid) <= rhs:
            lo = mid
        else:
            hi = mid - 1
    return lo


def bracket(word, residual):
    lo, hi = BAND
    for action in reversed(word):
        left = lower_inverse(action, max(0, lo - residual))
        target = min(GRID, hi + residual)
        right = lower_inverse(action, target)
        if numerator(action, right) != target * GRID**2:
            right += 1
        lo, hi = max(BAND[0], left), min(BAND[1], right)
        if lo > hi:
            raise ArithmeticError("Empty feasible interval")
    return lo, hi


def show_bracket(interval):
    # Outward round to six decimal places for human-readable JSON.
    divisor = GRID // 10**6
    lo, hi = interval
    parts = [lo // divisor, -(-hi // divisor)]
    return [f"{units // 10**6}.{units % 10**6:06d}" for units in parts]


def report():
    total, amplitudes, x = two_tick_source()
    assert total == 4 and x == Fraction(3, 4)
    word = schedule(x, 12)
    rows = []
    for depth in (0, 1, 2, 3, 4, 6, 8, 10, 12):
        exact = bracket(word[:depth], 0)
        noisy = bracket(word[:depth], GRID // 1000)
        assert noisy[0] <= exact[0] <= x * GRID <= exact[1] <= noisy[1]
        rows.append({
            "depth": depth,
            "word": word[:depth],
            "forward_or_reverse_source_calls_in_deepest_word": 3**depth,
            "root_interval_zero_residual": show_bracket(exact),
            "root_interval_residual_at_most_0.001": show_bracket(noisy),
        })

    def rival(s):
        return s + s * (1 - s) * (2 * s - 1) / 2

    direct, after = rival(x), rival(x**3)
    assert word[0] == "D" and direct**3 != after
    # If three reports equal the same fair bit, both AND and OR are that bit.
    assert all(all([b] * 3) == any([b] * 3) == b for b in (False, True))
    return {
        "two_tick_integer_amplitudes": {f"{i},{r}": n for (i, r), n in sorted(amplitudes.items())},
        "squared_norm_denominator": total,
        "initial_nonblank_mass": str(x),
        "exact_integer_interval_grid": str(GRID),
        "required_observed_band_at_each_node": ["1/8", "7/8"],
        "certificates": rows,
        "rival": {
            "native": str(direct), "coherent_first_echo": str(after),
            "independent_three_hit_rate": str(direct**3),
            "absolute_discrepancy": str(abs(after - direct**3)),
        },
        "shared_fair_bit_control": {"native": "1/2", "AND": "1/2", "OR": "1/2"},
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    output = parser.parse_args().output
    data = json.dumps(report(), indent=2) + "\n"
    if output:
        output.write_text(data, encoding="utf-8", newline="\n")
    else:
        print(data, end="")


if __name__ == "__main__":
    main()
