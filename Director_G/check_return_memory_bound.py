"""Run python -B check_return_memory_bound.py OUTPUT_DIRECTORY (standard library).

Compare fresh terminal reads after k copies of one dressed hop. Every bound,
read and recurrence residual uses exact rational arithmetic.
"""
import argparse
import json
from fractions import Fraction
from pathlib import Path

from check_string_readouts import PAIRS, R, execute, rotation, squared


MAX_STATES = 12
Z_REAL, Z_IMAG = Fraction(-7, 25), Fraction(24, 25)


def native_returns(last):
    word = rotation(1, R)
    x, y = Fraction(1), Fraction(0)
    values, chords = [], []
    for k in range(last + 1):
        q = squared(execute(PAIRS[0], word * k))[0]
        assert q == (1 + x) / 2
        values.append(q)
        chords.append((1 - x)**2 + y**2)
        assert chords[-1] == 4 * (1 - q)
        x, y = Z_REAL*x - Z_IMAG*y, Z_IMAG*x + Z_REAL*y
    # H(x)=(x-1)(x²+14x/25+1). The sequence starts at k=0.
    for k in range(last - 2):
        assert 25 * (values[k+3] - values[k]) == 11 * (values[k+2] - values[k+1])
    return values, chords


def bound_row(m, native, chords):
    closest = min(chords[1:m+1])
    eta = closest / (8*m)
    assert eta == (1 - max(native[1:m+1])) / (2*m) and eta > 0
    # The squared constant is |1-z|²(1-|Re z|)/2; both factors are positive.
    assert Fraction(24, 25)**2 == chords[1] * (1-abs(Z_REAL))/2
    error = Fraction(24, 25) * eta**(m-1) / 2**(m+1)
    return dict(states=m, last_read=m+1, minimum_chord_squared=closest,
                minimizing_powers=[r for r in range(1, m+1) if chords[r] == closest],
                eigenvalue_distance_bound=eta, probability_error_bound=error)


def example(name, matrix, initial, emissions, chi, native, bounds):
    m = len(initial)
    assert len(matrix) == len(emissions) == m and len(chi) == m+1
    assert all(len(r) == m and min(r) >= 0 and sum(r) == 1 for r in matrix)
    assert min(initial) >= 0 and sum(initial) == 1 and all(0 <= b <= 1 for b in emissions)
    assert sum(chi) == 0 and chi[-1] == 1 and sum(map(abs, chi)) <= 2**m
    state, predictions = initial, []
    for k in range(m+2):
        predictions.append(sum(a*b for a, b in zip(state, emissions)))
        state = [sum(a*r[j] for a, r in zip(state, matrix)) for j in range(m)]
    target_residuals = []
    for k in (0, 1):
        assert sum(c*predictions[k+j] for j, c in enumerate(chi)) == 0
        target_residuals.append(sum(c*native[k+j] for j, c in enumerate(chi)))
    errors = [abs(p-q) for p, q in zip(predictions, native)]
    assert max(errors) >= bounds[m-1]["probability_error_bound"]
    assert any(target_residuals)
    return dict(name=name, transition=matrix, initial=initial, emission=emissions,
                characteristic_low_to_high=chi, predictions=predictions, absolute_errors=errors,
                ordinary_recurrence_residuals=target_residuals)


def calculate():
    native, chords = native_returns(MAX_STATES+1)
    bounds = [bound_row(m, native, chords) for m in range(1, MAX_STATES+1)]
    f = Fraction(779, 900)
    examples = [
        example("one static state", [[1]], [1], [1], [-1, 1], native, bounds),
        example("two-state absorbing transition", [[native[1], 1-native[1]], [0, 1]],
                [1, 0], [1, 0], [native[1], -1-native[1], 1], native, bounds),
        example("three-state calibrated prefix",
                [[0, 1, 0], [0, 0, 1], [f, 0, 1-f]], [1, 0, 0], native[:3],
                [-f, 0, f-1, 1], native, bounds),
        example("four-state deterministic cycle",
                [[0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1], [1, 0, 0, 0]],
                [1, 0, 0, 0], native[:4], [-1, 0, 0, 0, 1], native, bounds),
    ]
    # Exact equality cases for the two- and three-state examples above.
    assert examples[1]["predictions"][:3] == [1, native[1], native[1]**2]
    assert native[1]**2 - native[2] == Fraction(32, 625)
    witness = examples[2]["predictions"]
    assert witness[:4] == native[:4] and witness[4] == Fraction(167729, 390625)
    assert native[4] - witness[4] == Fraction(176, 625)
    return dict(source="Four-site vacuum Gauss sector, localized pair 01, repeated real rotation R on bond 12.",
                time_order="Fresh terminal return probabilities from k=0 upward.",
                ordinary=native, bounds=bounds, examples=examples,
                scope="The examples are exact instances. The universal bound uses the eigenvector and recurrence proof.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_directory", type=Path)
    directory = parser.parse_args().output_directory
    directory.mkdir(parents=True, exist_ok=True)
    data = calculate()
    (directory/"return_memory_bound.json").write_bytes(
        (json.dumps(data, default=str, indent=2) + "\n").encode("utf-8"))
    print("Verified 14 return times, bounds for 1–12 states and four stochastic examples.")
