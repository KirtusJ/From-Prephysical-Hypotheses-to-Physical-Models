"""Check a four-input witness for the fixed terminal effect using rational arithmetic."""
from fractions import Fraction as Q
from math import comb
from pathlib import Path
from runpy import run_path

design = run_path(str(Path(__file__).with_name("check_terminal_readouts.py")))
A, B = design["A"], design["B"]
V = (0, -46, 3, 6, -26, -6, 26, 46, -3, 0)
C = (0, 0, 1, 0, -1, 0, -1, 0, 1, 0)
W = (0, 34, 49, 98, -32, -98, 32, -34, -49, 0)
PROBES = (A, V, C, W)
SIGNS = (1, 1, -1, -1)
WEIGHT = Q("0.1570796327")
RESIDUAL = Q("0.000000079")
REQUIRED_SCORE = Q("0.813378364430")
CAL_BOUND = Q("0.998757285")
IDEAL_CAL_LOWER = Q("0.999986292")


def projector_entry(v, i, j):
    return Q(v[i] * v[j], sum(x*x for x in v))


def calibration_tail(n, allowed_misses, q):
    """Probability of at most the given number of misses."""
    a, d = q.as_integer_ratio()
    return Q(sum(comb(n, k) * (d-a)**k * a**(n-k)
                 for k in range(allowed_misses+1)), d**n)


def positive(condition, message):
    if not condition:
        raise ValueError(message)


def check_matrix(m, negative, error):
    square_norm = Q(0)
    for i, row in enumerate(m):
        for j, cell in enumerate(row):
            witness = sum(s * projector_entry(v, i, j) for s, v in zip(SIGNS, PROBES))
            square_norm += (cell - WEIGHT*witness)**2
    positive(10*square_norm < RESIDUAL**2, "Frobenius residual")
    positive(negative + WEIGHT*(4*CAL_BOUND-2) - RESIDUAL - error >= REQUIRED_SCORE,
             "soundness boundary")
    q = Q(1, 2)
    for sign, v in zip(SIGNS, PROBES):
        click = sum(Q(design["dot"](u, v)**2, design["dot"](u, u)*design["dot"](v, v))
                    for u in (A, B))
        q += sign*click/4
    positive(IDEAL_CAL_LOWER < q < Q("0.999986293"), "ideal analyzer probe rate")
    # Input rail 1 acquires a phase of pi only in the analyzer.
    flipped_b = tuple(-x if i == 1 else x for i, x in enumerate(B))
    flip = lambda v: tuple(-x if i == 1 else x for i, x in enumerate(v))
    for v in PROBES:
        for u in (A, B):
            positive(design["dot"](u, v) == design["dot"](flip(u), flip(v)),
                     "common phase flip changed a calibration overlap")
    wrong = negative + design["mode_gain"](m, A) + design["mode_gain"](m, flipped_b)
    positive(Q("0.657918768") <= wrong-error and wrong+error < Q("0.657918770"),
             "misregistered phase score")
    positive(design["rejection"](31, Q("0.657918770"), 22, Q(1)) < Q("0.344480"),
             "phase-flip power")
    return q


def main():
    m, negative, error, _ = design["signed_matrix"]()
    q = check_matrix(m, negative, error)
    print(f"ideal four-input pass probability {float(q):.12f}")
    print(f"uniform signed-score residual below {float(RESIDUAL):.9f} plus propagation error")
    for n, cutoff, walks, threshold, source_error in [
        (2410, 0, 42, 29, Q(0)), (5065, 2, 31, 22, Q(0)),
        (5508, 2, 31, 22, Q("0.0001")),
    ]:
        false_certificate = calibration_tail(n, cutoff, CAL_BOUND+source_error)
        ideal_pass = calibration_tail(n, cutoff, IDEAL_CAL_LOWER)
        size = design["rejection"](walks, design["P0"], threshold, Q(1))
        walk_power = design["rejection"](walks, Q("0.814150670081"), threshold, Q(1))
        positive(false_certificate < Q(1, 20), "bad detector accepted too often")
        positive(size < Q(1, 20) and ideal_pass*walk_power > Q(19, 20),
                 "joint ideal and null targets")
        print(f"{n} probes, <= {cutoff} errors; {walks} walks, >= {threshold} successes; "
              f"false certificate <= {float(false_certificate):.12f}; "
              f"joint ideal power >= {float(ideal_pass*walk_power):.12f}")
    print("common phase flip on source probes and analyzer: calibration statistics identical")
    print("analyzer-only rail-1 phase flip: walk score in [0.657918768, 0.657918770]")


if __name__ == "__main__":
    main()
