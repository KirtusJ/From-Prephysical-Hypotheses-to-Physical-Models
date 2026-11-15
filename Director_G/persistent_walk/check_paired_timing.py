"""Exact integer bounds for independent blocks of two launches at a common time."""
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
from runpy import run_path

HERE = Path(__file__).resolve().parent
WALK = run_path(str(HERE / "check_804_timing.py"))
N, SCALE, unnormalized_step = WALK["N"], WALK["SCALE"], WALK["unnormalized_step"]
make_design = run_path(str(HERE / "check_prelaunch_time_sampling.py"))["make_design"]


NULL_CEILING = Fraction(547843, 1000000)
GRID = 1 << 80


@lru_cache(maxsize=1)
def ideal_pair_moments():
    """Outward bounds on E[s(T)] and E[s(T)^2] for the accepted signed setting."""
    thresholds = make_design(N)
    rails = [SCALE] + [0] * 9
    weight_sum = first_sum = second_sum = 0
    for lag, threshold in enumerate(thresholds):
        weight = (N - abs(lag - (N - 1))) * abs(threshold)
        click = rails[0] ** 2
        success = click if threshold >= 0 else SCALE**2 - click
        weight_sum += weight
        first_sum += weight * success
        second_sum += weight * success**2
        rails = [v // 2 for v in unnormalized_step(unnormalized_step(rails))]
    # Each two-tick roundoff has Euclidean norm <2/SCALE; exact evolution
    # preserves the norm. Squaring an amplitude with absolute error d<1
    # costs at most 3*d, as does squaring the resulting success estimate.
    first = Fraction(first_sum, weight_sum * SCALE**2)
    second = Fraction(second_sum, weight_sum * SCALE**4)
    error = Fraction(6 * (len(thresholds) - 1), SCALE)
    p_lo, p_hi = Fraction('0.62566370613899'), Fraction('0.62566370613900')
    m_lo, m_hi = Fraction('0.52966370805656'), Fraction('0.52966370805658')
    if not (p_lo <= first - error <= first + error <= p_hi and
            m_lo <= second - 3*error <= second + 3*error <= m_hi):
        raise ValueError('The ideal moment enclosures failed')
    return p_lo, p_hi, m_lo, m_hi


def null_size_upper(pairs, cutoff, tie):
    """Bound each mixture vertex 2*Bin(r,p) + Bin(2*pairs-2*r,p)."""
    a, denominator = NULL_CEILING.as_integer_ratio()
    b = denominator - a
    # Point masses rounded up on a common grid at every Bernoulli step.
    rows = [[GRID]]
    for _ in range(2*pairs):
        previous = rows[-1]
        rows.append([(b*x + a*y + denominator-1) // denominator
                     for x, y in zip(previous+[0], [0]+previous)])
    largest = 0
    at_vertex = 0
    g, h = tie.as_integer_ratio()
    for doubles in range(pairs+1):
        singles = rows[2*(pairs-doubles)]
        tails = [0] * (len(singles)+1)
        for k in range(len(singles)-1, -1, -1):
            tails[k] = tails[k+1] + singles[k]
        total = 0
        for x, mass in enumerate(rows[doubles]):
            k = cutoff - 2*x
            if k < 0:
                total += mass * h * GRID
            elif k < len(singles):
                total += mass * (h*tails[k+1] + g*singles[k])
        if total > largest:
            largest, at_vertex = total, doubles
    return Fraction(largest, h * GRID**2), at_vertex


def ideal_power_lower(pairs, cutoff, tie, moments):
    p_lo, _, m_lo, m_hi = moments
    # A stochastically smaller pair distribution increases P(0) and
    # decreases P(2). Round the parameters further onto a small common grid.
    scale = 10**10
    zero = -((-scale*(1-2*p_lo+m_hi)) // 1)
    two = (scale*m_lo) // 1
    one = scale-zero-two
    masses = [GRID]
    for _ in range(pairs):
        masses = [(zero*x + one*y + two*z) // scale for x, y, z in
                  zip(masses+[0, 0], [0]+masses+[0], [0, 0]+masses)]
    return (sum(masses[cutoff+1:]) + tie*masses[cutoff]) / GRID


def main():
    moments = ideal_pair_moments()
    source = run_path(str(HERE / "check_real_readout_bound.py"))
    if source["NULL_UPPER"] > NULL_CEILING:
        raise ValueError("The paired-design null ceiling is too small")
    for pairs, cutoff, tie, size_limit, power_floor, expected_vertex in (
            (389, 458, Fraction(0), 49624333, 950869646, 388),
            (402, 474, Fraction(1, 2), 46313539, 952523132, 402)):
        size, vertex = null_size_upper(pairs, cutoff, tie)
        power = ideal_power_lower(pairs, cutoff, tie, moments)
        if size > Fraction(1, 20) or power < Fraction(19, 20):
            raise ValueError('The paired design exceeds its error allowance')
        # Print rigorous decimal endpoints by rounding in the indicated directions.
        size_numerator = -((-size*10**9) // 1)
        power_numerator = (power*10**9) // 1
        if size_numerator > size_limit or power_numerator < power_floor or vertex != expected_vertex:
            raise ArithmeticError('reported paired bounds or extremizing vertex differ')
        print(f'{pairs} pairs, reject above {cutoff}, tie {tie}: '
              f'null <= {size_numerator}/10^9 (vertex {vertex}), '
              f'ideal >= {power_numerator}/10^9')


if __name__ == '__main__':
    main()
