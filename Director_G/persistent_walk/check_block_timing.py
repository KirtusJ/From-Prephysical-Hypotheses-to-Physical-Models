"""Finite-bit controller and two error certificates for repeated timing settings."""
from array import array
from fractions import Fraction as F
from math import ceil, floor
from pathlib import Path
from runpy import run_path

N = 250_000
GRID = 1 << 32
HERE = Path(__file__).resolve().parent
TIMING = run_path(str(HERE / 'check_prelaunch_time_sampling.py'))
WALK = run_path(str(HERE / 'check_804_timing.py'))
REAL = run_path(str(HERE / 'check_real_readout_bound.py'))


def build_thresholds(signed, tolerance):
    """Return thinning and score cutoffs c(t) in units of 2^-32."""
    scale = WALK['SCALE']
    step = WALK['unnormalized_step']
    rails = [scale] + [0] * 9
    a, b = tolerance.as_integer_ratio()
    denominator = b * scale**2
    thresholds = array('Q')
    for lag, signed_weight in enumerate(signed):
        raw = rails[0]**2 if signed_weight > 0 else scale**2 - rails[0]**2
        lower = raw - 6 * lag * scale
        cutoff = GRID * (b * lower - a * scale**2) // denominator
        thresholds.append(max(0, min(GRID, cutoff)))
        rails = [v // 2 for v in step(step(rails))]
    return thresholds


def draw_block(signed, thresholds, randbits):
    """Call before preparing the block. Return (tick, click_is_success, h)."""
    while True:
        tick, click_is_success = TIMING['draw_setting'](N, signed, randbits)
        h = thresholds[tick // 2]
        if randbits(32) < h:
            return tick, click_is_success, h


def check(signed, tolerance, blocks, launches, risk_limit_ppm, power_floor_ppm):
    thresholds = build_thresholds(signed, tolerance)
    # Force one rejected proposal followed by an accepted one at lag zero.
    words = iter([0, GRID - 1, 0, 0])
    if draw_block(signed, thresholds, lambda bits: next(words)) != (0, True, thresholds[0]):
        raise ArithmeticError('prelaunch thinning control')
    # The triangular proposal counts the ordered pairs with sum equal to lag.
    total = accepted = 0
    for lag, (v, h) in enumerate(zip(signed, thresholds)):
        weight = (N - abs(lag - (N - 1))) * abs(v)
        accepted += weight * h
        total += weight
    mass = F(accepted, total * GRID)
    # Check also against the analytic lower bound from pointwise rounding.
    allowance = F(12 * (len(signed) - 1), WALK['SCALE']) + F(1, GRID)
    if mass < REAL['IDEAL_LOWER'] - tolerance - allowance:
        raise ArithmeticError('thinning mass below rounded ideal lower bound')
    size = (REAL['NULL_UPPER'] / mass)**blocks
    # Taylor partial sum is a rational lower bound for exp(x), x >= 0.
    x = 2 * launches * tolerance**2
    term = series = F(1)
    for k in range(1, 41):
        term *= x / k
        series += term
    miss = blocks / series
    if max(size, miss) >= F(1, 20):
        raise ArithmeticError('an error bound exceeds five percent')
    # Output size and power rounded outwards using integers.
    risk_ppm = ceil(size * 1_000_000)
    power_ppm = floor((1 - miss) * 1_000_000)
    if risk_ppm > risk_limit_ppm or power_ppm < power_floor_ppm:
        raise ArithmeticError('reported block bounds failed')
    print(f'{blocks} settings; {launches} launches/setting; {blocks*launches} total; '
          f'size <= {risk_ppm}/1000000; power >= {power_ppm}/1000000')
    print(f'Exact thinning probability {mass}')


if __name__ == '__main__':
    REAL['check_geometry']()
    signed = TIMING['make_design'](N)
    check(signed, F(3, 125), 32, 5650, 47025, 952311)
    check(signed, F(51, 1000), 64, 1400, 32089, 956015)
