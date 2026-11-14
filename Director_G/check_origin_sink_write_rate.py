"""Certify independent site-write rates against the archived continual-sink bars."""
import argparse
from collections import defaultdict
from fractions import Fraction
import json
from math import comb
from pathlib import Path

from check_origin_sink_data import band, group_by_histories

DATA = Path(__file__).with_name("results") / "origin_sink_data.json"
GRID = 10**9


def recurrence(z, stride, horizon):
    """Return 2**t times the cumulative absorbed mass with coherence factor z."""
    # A pair (x,y) holds its RR, RL, LR, LL block of the survivor density matrix.
    state = {(0, 0): [1, 0, 0, 0]}
    absorbed = {}
    for tick in range(1, horizon + 1):
        outgoing = defaultdict(lambda: [0, 0, 0, 0])
        for (x, y), (a, b, c, d) in state.items():
            rotated = (a+b+c+d, a-b+c-d, a+b-c-d, a-b-c+d)
            for rail_pair, value in enumerate(rotated):
                if not value:
                    continue
                dest_x = x + (1 if rail_pair < 2 else -1)
                dest_y = y + (1 if rail_pair % 2 == 0 else -1)
                if dest_x == 0 or dest_y == 0:
                    continue
                if tick % stride == 0 and dest_x != dest_y:
                    value *= z
                outgoing[dest_x, dest_y][rail_pair] = value
        state = outgoing
        if tick % 2 == 0:
            trace = sum(block[0]+block[3] for (x,y), block in state.items() if x == y)
            absorbed[tick] = 2**tick - trace
    return absorbed


def interpolate(values):
    """Power coefficients from exact values at consecutive integers starting at zero."""
    coefficients = [Fraction(0)] * len(values)
    basis = [Fraction(1)]
    for level in range(len(values)):
        for k, value in enumerate(basis):
            coefficients[k] += values[0] * value
        values = [b-a for a, b in zip(values, values[1:])]
        shifted = [Fraction(0)] + basis
        for k, value in enumerate(basis):
            shifted[k] -= level * value
        basis = [value/(level+1) for value in shifted]
    while len(coefficients) > 1 and coefficients[-1] == 0:
        coefficients.pop()
    assert all(a.denominator == 1 for a in coefficients)
    return [int(a) for a in coefficients]


def evaluate(coefficients, z):
    total = 0
    for value in reversed(coefficients):
        total = total * z + value
    return total


def min_derivative(coefficients, scale):
    """Lower bound on d/d(gamma) using the Bernstein basis in z=1-gamma."""
    derivative = [-i*c for i, c in enumerate(coefficients) if i]
    if not derivative:
        return Fraction(0)
    degree = len(derivative)-1
    return min(sum(Fraction(comb(j,k)*derivative[k], comb(degree,k)*scale)
                   for k in range(j+1)) for j in range(degree+1))


def rate_bracket(coefficients, scale, cap):
    """A closed rational bracket for the last admissible gamma of one monotone row."""
    def fits(numerator):
        z = 1 - Fraction(numerator, GRID)
        return evaluate(coefficients, z) <= cap * scale

    assert fits(0)
    if fits(GRID):
        return [GRID, GRID]
    lo, hi = 0, GRID
    while hi-lo > 1:
        mid = (lo+hi)//2
        if fits(mid):
            lo = mid
        else:
            hi = mid
    return [lo, hi]


def path_pair_check(tick, stride):
    """Independent paths grouped by visible site record for each eligible subset."""
    from itertools import combinations
    total = Fraction()
    for hit_time in range(2, tick+1, 2):
        eligible = range(stride, hit_time, stride)
        total += sum(group_by_histories(hit_time, writes)
                     for size in range(len(eligible)+1)
                     for writes in combinations(eligible, size)) / (2**len(eligible))
    return total


def correlated_even_writes():
    """Determine the dependence on an arbitrary schedule through tick ten."""
    from itertools import combinations
    schedule_rows = []
    for tick in (8, 10):
        eligible = range(2, tick, 2)
        for size in range(len(eligible)+1):
            for writes in combinations(eligible, size):
                observed = sum(group_by_histories(hit, writes) for hit in range(2,tick+1,2))
                a, b = int(4 in writes), int(6 in writes)
                if tick == 8:
                    expected = Fraction(81,128) + Fraction(a,32)
                else:
                    expected = Fraction(81,128) + Fraction(3*a+b+a*b,64)
                assert observed == expected
                schedule_rows.append({"tick":tick, "writes":list(writes), "return":str(observed)})
    return schedule_rows


def replay_schedule(figure, stride, check_column):
    horizon = figure[-1]["tick"]
    # Discarding the last tick's write does not alter the trace at that tick.
    degree_bound = (horizon-1)//stride
    samples = {z: recurrence(z, stride, horizon) for z in range(-1, degree_bound+1)}
    rows = []
    for observation in figure:
        t = observation["tick"]
        scale = 2**t
        degree = (t-1)//stride
        coeff = interpolate([samples[z][t] for z in range(degree+1)])
        assert all(evaluate(coeff,z) == values[t] for z, values in samples.items())
        assert Fraction(evaluate(coeff,1),scale) == Fraction(observation["coherent_continual"])
        assert Fraction(evaluate(coeff,0),scale) == Fraction(observation[check_column])
        if t <= 8:
            assert evaluate(coeff,Fraction(1,2))/scale == path_pair_check(t,stride)
        low, high = band(*observation["continual_cap_rows"])
        lower_slope = min_derivative(coeff, scale)
        if len(coeff) > 1:
            assert lower_slope > 0
        else:
            assert lower_slope == 0
        assert low <= Fraction(evaluate(coeff,1),scale) <= high
        rows.append({"tick":t, "inclusive_bar":[str(low),str(high)],
                     "scale":scale, "power_coefficients_in_z":coeff,
                     "minimum_derivative_bernstein_coefficient":str(lower_slope),
                     "upper_rate_bracket_numerators":rate_bracket(coeff,scale,high)})
    ordered = sorted(rows, key=lambda row: row["upper_rate_bracket_numerators"])
    first, second = ordered[:2]
    assert first["upper_rate_bracket_numerators"][1] < second["upper_rate_bracket_numerators"][0]
    high = Fraction(first["inclusive_bar"][1])
    raised = rate_bracket(first["power_coefficients_in_z"], first["scale"], high + Fraction(1,478))
    assert raised[0] > second["upper_rate_bracket_numerators"][1]
    return {"binding_clock":first["tick"], "runner_up_clock":second["tick"],
            "upper_rate_bracket_numerators":first["upper_rate_bracket_numerators"],
            "binding_row_one_pixel_higher_bracket":raised, "all_clocks":rows}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    figure = json.loads(DATA.read_text(encoding="utf-8"))["even_clock_rows"]
    assert [r["tick"] for r in figure] == list(range(2,37,2))
    result = {"input_figure":"Nitsche et al., Figure 4, continual origin return",
              "bracket_denominator":GRID,
              "correlated_even_schedule_controls":correlated_even_writes(),
              "each_tick":replay_schedule(figure, 1, "exact_site_each_tick"),
              "even_ticks":replay_schedule(figure, 2, "exact_site_each_even_tick")}
    with args.output.open("x", encoding="utf-8", newline="\n") as output:
        output.write(json.dumps(result,indent=2)+"\n")


if __name__ == "__main__":
    main()
