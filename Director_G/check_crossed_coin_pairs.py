"""Replay matched and crossed three-tick contact experiments using exact arithmetic."""
from argparse import ArgumentParser
from fractions import Fraction
from itertools import product
import json
from pathlib import Path

from check_two_coin_contact import YY, check, path_effects, scaled, score, score_sum


def shift_partner(n, shift):
    return tuple((i + shift) % n for i in range(n))


def sharp_bias(n):
    """Multiply the absolute difference by n^2*(n-1) to keep vertex tests integral."""
    signs = tuple(product((-1, 1), repeat=n))
    worst = 0
    for a in signs:
        for b in signs:
            dot = sum(x * y for x, y in zip(a, b))
            all_products = sum(a) * sum(b)
            crossed = all_products - dot
            numerator = n * crossed - (n - 1) * all_products
            worst = max(worst, abs(numerator))
    check(worst == 4 * ((n * n) // 4), "sharp vertex bound")
    return str(Fraction(worst, n * n * (n - 1)))


def bell_amplitudes(n):
    """Integer amplitudes of a product of Phi-minus pairs, before normalization."""
    entries = {}
    for bits in product((0, 1), repeat=n):
        word = sum((3 * b) << (2 * i) for i, b in enumerate(bits))
        entries[word] = (-1) ** sum(bits)
    return entries


def selected_moment(amplitudes, permutation, mask):
    """Apply the product of signed spin operators directly to computational basis kets."""
    sites = 0
    for i, j in enumerate(permutation):
        if mask & (1 << i):
            sites |= (1 << (2 * i)) | (1 << (2 * j + 1))
    count = mask.bit_count()
    numerator = 0
    for word, amplitude in amplitudes.items():
        phase = (-1) ** (count + (sites & word).bit_count())
        numerator += phase * amplitude * amplitudes.get(word ^ sites, 0)
    return Fraction(numerator, len(amplitudes)) * Fraction(-1, 4) ** count


def bell_panel(n, shift):
    permutation = shift_partner(n, shift)
    amplitudes = bell_amplitudes(n)
    moments = []
    for mask in range(1 << n):
        selected = {i for i in range(n) if mask & (1 << i)}
        invariant = {permutation[i] for i in selected} == selected
        moment = selected_moment(amplitudes, permutation, mask)
        expected = Fraction(-1, 4) ** len(selected) if invariant else 0
        check(moment == expected, "Bell moment versus permutation cycles")
        moments.append(moment)

    probabilities = {}
    for bits in product((0, 1), repeat=n):
        negatives = sum(b << i for i, b in enumerate(bits))
        probability = sum(
            value * (-1) ** (negatives & mask).bit_count()
            for mask, value in enumerate(moments)
        ) / (1 << n)
        check(probability >= 0, "negative transcript probability")
        probabilities["".join("-" if b else "+" for b in bits)] = probability
    check(sum(probabilities.values()) == 1, "total transcript probability")
    marginals = [
        sum(p for word, p in probabilities.items() if word[i] == "+") for i in range(n)
    ]
    check(marginals == [Fraction(3, 8) if shift == 0 else Fraction(1, 2)] * n,
          "one routed observer")
    if n == 2 and shift == 1:
        check(list(probabilities.values()) == [Fraction(k, 64) for k in (17, 15, 15, 17)],
              "two-pair covariance control")
    return {word: str(p) for word, p in probabilities.items()}


def dependence_controls():
    # Distribution over *classical preparation settings*, with coins prepared as
    # Y eigenstates conditional on the settings. No such representation is used for Bell pairs.
    rows = [(2, (1, -1, 1), (-1, 1, 1)), (3, (-1, -1, 1), (1, -1, -1))]
    n = 3
    total = sum(weight for weight, _, _ in rows)
    a = [sum(Fraction(w * x[i], total) for w, x, _ in rows) for i in range(n)]
    b = [sum(Fraction(w * y[i], total) for w, _, y in rows) for i in range(n)]
    q = [[sum(Fraction(w * x[i] * y[j], total) for w, x, y in rows)
          for j in range(n)] for i in range(n)]
    a_mean, b_mean = sum(a) / n, sum(b) / n
    covariance = sum((x - a_mean) * (y - b_mean) for x, y in zip(a, b)) / n
    diag = sum(q[i][i] for i in range(n)) / n
    off = sum(q[i][j] for i in range(n) for j in range(n) if i != j) / (n * (n - 1))
    c_off = sum(q[i][j] - a[i] * b[j] for i in range(n) for j in range(n) if i != j)
    c_off /= n * (n - 1)
    c_diag = sum(q[i][i] - a[i] * b[i] for i in range(n)) / n
    check(off == a_mean * b_mean - covariance / (n - 1) + c_off, "cross-pair identity")
    check(diag - off == n * covariance / (n - 1) + c_diag - c_off, "partner difference")
    check(c_off and c_diag and covariance, "test all terms away from zero")
    separate = sum(x * y for x in a for y in b) / (n * n)
    check(separate == a_mean * b_mean, "all ordered choices from independent banks")

    signs = (1, 1, -1, -1)
    shifts = [
        Fraction(sum(signs[i] * signs[j] for i, j in enumerate(shift_partner(4, k))), 4)
        for k in (1, 2, 3)
    ]
    check(shifts == [0, -1, 0], "a single fixed shift can bias the crossed estimate")
    return {
        "three_pair_mixed_source": {key: str(value) for key, value in
            [("matched", diag), ("crossed", off), ("label_covariance", covariance),
             ("matched_connected", c_diag), ("crossed_connected", c_off),
             ("independent_banks", separate)]},
        "balanced_four_nonzero_shifts": [str(x) for x in shifts],
    }


def conjugation_control(n):
    # The normalized projector entry for the all-plus-Y bank is i^(|u|-|v|)/2^(2n).
    # Retain integer real and imaginary coefficients with the common denominator suppressed.
    quarters = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    dimension = 1 << (2 * n)
    real_only = imaginary_only = 0
    for u in range(dimension):
        for v in range(dimension):
            power = u.bit_count() - v.bit_count()
            re, im = quarters[power % 4]
            re_conjugate, im_conjugate = quarters[-power % 4]
            check((re + re_conjugate, im + im_conjugate) == (2 * re, 0),
                  "global mixture equals the real symmetric part")
            real_only += abs(re)
            imaginary_only += abs(im)
    return {"dimension": dimension, "real_entries": real_only, "imaginary_entries": imaginary_only}


def run():
    effects = path_effects(2, {1, 2, 3}, 3)
    signed = score_sum(effects, {key: score(*key) for key in effects})
    check(len(effects) == 16 and signed == scaled(-16, YY), "native contact spin effect /64")
    return {
        "position_score_numerator_over_64": signed,
        "max_abs_crossed_product_bias_at_vertices": {str(n): sharp_bias(n) for n in range(2, 8)},
        "controls": dependence_controls(),
        "pure_bell_transcripts_by_n_and_cyclic_shift": {
            str(n): {str(k): bell_panel(n, k) for k in range(n)} for n in range(2, 6)
        },
        "shared_conjugate_sign_state": {str(n): conjugation_control(n) for n in range(1, 5)},
    }


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    data = run()
    with args.output.open("x", encoding="utf-8", newline="\n") as output:
        json.dump(data, output, indent=2)
        output.write("\n")
