"""Reproducible positive/adverse controls for the five-site time sampler.

No physical apparatus or random-number generator is tested.  The 64-bit
callback deliberately breaks the sampler's independent fair-bits contract.
"""
from array import array
from decimal import Decimal, ROUND_FLOOR, localcontext
from fractions import Fraction
from pathlib import Path
from runpy import run_path

_pinned = run_path(str(Path(__file__).with_name("check_prelaunch_time_sampling.py")))
ACCEPT_LEVELS = _pinned["ACCEPT_LEVELS"]
SCALE = _pinned["SCALE"]
cosine_centers = _pinned["cosine_centers"]
draw_setting = _pinned["draw_setting"]

N = 250_000
LAG = 28
WIDTH = (N - 1).bit_length()
REQUESTED = 2 * WIDTH + 32


def require(condition, reason):
    if not condition:
        raise ArithmeticError(reason)


def independent_threshold(precision):
    """Compute the lag-28 floor by an independent decimal phase recurrence."""
    with localcontext() as ctx:
        ctx.prec = precision
        root5 = Decimal(5).sqrt()
        ca = (Decimal(3) - root5) / 8
        cb = (Decimal(3) + root5) / 8
        sa = (1 - ca * ca).sqrt()
        sb = (1 - cb * cb).sqrt()
        zr, zi = ca * cb + sa * sb, sa * cb - ca * sb
        x, y = Decimal(1), Decimal(0)
        for _ in range(LAG):
            x, y = x * zr - y * zi, x * zi + y * zr
        return (int((abs(x) * ACCEPT_LEVELS).to_integral_value(
            rounding=ROUND_FLOOR)), x > 0)


def candidate(j, k, acceptance_word):
    require(0 <= j < 1 << WIDTH and 0 <= k < 1 << WIDTH,
            "candidate coordinate is outside bit field")
    return j | (k << WIDTH) | (acceptance_word << (2 * WIDTH))


def run_words(signed, words):
    stream = iter(words)
    calls = [0]

    def source(requested_bits):
        require(requested_bits == REQUESTED, "unexpected random-bit request")
        calls[0] += 1
        return next(stream)

    outcome = draw_setting(N, signed, source)
    return outcome, calls[0]


def main():
    require((WIDTH, REQUESTED) == (18, 68), "changed sampler bit layout")
    pinned_center = list(cosine_centers(LAG + 1))[-1]
    pinned_h = ACCEPT_LEVELS * abs(pinned_center) // SCALE
    exact_70 = independent_threshold(70)
    exact_100 = independent_threshold(100)
    require(exact_70 == exact_100 == (95_786_191, True),
            "independent high-precision threshold changed")
    require((pinned_h, pinned_center > 0) == exact_100,
            "pinned source and independent recurrence disagree")
    require(0 < pinned_h < 1 << 28, "adverse bit-width regime changed")

    signed = array("q", [0]) * (2 * N - 1)
    signed[LAG] = pinned_h
    accepted = candidate(LAG, 0, pinned_h - 1)
    rejected = candidate(LAG, 0, pinned_h)
    invalid_coordinate = candidate((1 << WIDTH) - 1, 0, 0)
    expected = (2 * LAG, True)
    require(run_words(signed, [accepted]) == (expected, 1),
            "positive control: valid accepted word")
    require(run_words(signed, [rejected, accepted]) == (expected, 2),
            "negative control: equality at acceptance boundary")
    require(run_words(signed, [invalid_coordinate, accepted]) == (expected, 2),
            "negative control: out-of-range coordinate")
    require(accepted < 1 << 64, "adverse word must fit a 64-bit source")
    require(run_words(signed, [accepted]) == (expected, 1),
            "adverse source must yield the same apparent assignment")

    # Conditional on the valid proposed coordinates J=28, K=0, a uniform
    # 68-bit word supplies 32 fair acceptance bits; a uniform 64-bit word
    # supplies only 28. These are exact counts, not Monte Carlo estimates.
    proper = Fraction(pinned_h, 1 << 32)
    short = Fraction(pinned_h, 1 << 28)
    require(short == 16 * proper and short < 1,
            "the width defect did not produce the expected ratio")
    print(f"PASS: pinned and independent h[{LAG}] = {pinned_h}")
    print(f"PASS: both sources can yield tick {2*LAG}, click-is-success true")
    print(f"PASS: correct 68-bit acceptance = {float(proper):.12f}")
    print(f"PASS: deficient 64-bit acceptance = {float(short):.12f}")
    print("PASS: rejection-at-threshold and invalid-coordinate controls")
    print("LIMIT: only a stipulated changed callback; no apparatus or RNG tested")


if __name__ == "__main__":
    main()
