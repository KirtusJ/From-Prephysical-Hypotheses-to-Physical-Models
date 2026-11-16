"""Certify three fixed terminal measurements for the five-site timing sampler."""

from fractions import Fraction as Q
from math import comb
from pathlib import Path
from runpy import run_path

WALK = Path(__file__).resolve().parents[2] / "Director_G" / "persistent_walk"
N = 250_000
P0 = Q("0.547842242")
ALPHA = Q(1, 20)
TARGET = 1 - ALPHA
DIRECT = (0, 1, 7)
PAIRS = ((2, 4), (3, 5), (6, 8))
A = (-4, 0, 1, 0, 1, 0, 1, 0, 1, 0)
B = (0, -16, 1, 2, -9, -2, 9, 16, -1, 0)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def signed_matrix():
    sampler = run_path(str(WALK / "check_prelaunch_time_sampling.py"))
    walk = run_path(str(WALK / "check_804_timing.py"))
    step, scale = walk["unnormalized_step"], walk["SCALE"]
    rails = [scale] + [0] * 9
    matrix = [[0] * 10 for _ in range(10)]
    total = negative = mode_sum = 0
    aa, bb = dot(A, A), dot(B, B)
    require((aa, bb, dot(A, B)) == (20, 684, 0), "mode geometry")
    for lag, threshold in enumerate(sampler["make_design"](N)):
        weight = (N - abs(lag - (N - 1))) * threshold
        total += abs(weight)
        negative += max(-weight, 0)
        for i, r in enumerate(rails):
            factor = weight * r
            for j in range(i + 1):
                matrix[i][j] += factor * rails[j]
        # Direct projection on this lag independently checks the trace contraction.
        mode_sum += weight * (bb * dot(A, rails)**2 + aa * dot(B, rails)**2)
        rails = [r // 2 for r in step(step(rails))]
    den = total * scale**2
    matrix = [[Q(matrix[max(i, j)][min(i, j)], den) for j in range(10)]
              for i in range(10)]
    error = Q(6 * (2 * N - 2), scale)
    return matrix, Q(negative, total), error, Q(mode_sum, aa * bb * den)


def mode_gain(matrix, mode):
    return sum(x * dot(row, mode) for x, row in zip(mode, matrix)) / dot(mode, mode)


def below_shift(matrix, shift):
    """Count eigenvalues below shift using symmetric rational elimination."""
    m = [[x - shift if i == j else x for j, x in enumerate(row)]
         for i, row in enumerate(matrix)]
    count = 0
    for k, row in enumerate(m):
        pivot = row[k]
        require(pivot != 0, "zero pivot at the selected shift")
        count += int(pivot < 0)
        for i in range(k + 1, len(m)):
            ratio = m[i][k] / pivot
            for j in range(i, len(m)):
                m[i][j] -= ratio * row[j]
                m[j][i] = m[i][j]
    return count


def binomial_mass(n, p):
    a, d = p.as_integer_ratio()
    return [Q(comb(n, k) * a**k * (d-a)**(n-k), d**n) for k in range(n+1)]


def rejection(n, p, boundary, tie):
    mass = binomial_mass(n, p)
    return sum(mass[boundary+1:]) + tie * mass[boundary]


def most_powerful(n, alternative):
    null = binomial_mass(n, P0)
    remaining = ALPHA
    for k in range(n, -1, -1):
        if remaining <= null[k]:
            return rejection(n, alternative, k, remaining / null[k])
        remaining -= null[k]
    raise ValueError("level not reached")


def main():
    m, neg, error, direct_contraction = signed_matrix()
    direct = neg + sum(m[i][i] for i in DIRECT)
    paired = direct + sum((m[i][i] + m[j][j] + 2*m[i][j])/2 for i, j in PAIRS)
    coherent = neg + mode_gain(m, A) + mode_gain(m, B)
    require(coherent == neg + direct_contraction, "per-lag and matrix scores differ")
    controls = [
        ("direct", direct, Q("0.730021733918"), 74, 48, Q(243, 256)),
        ("balanced pairs", paired, Q("0.774482413923"), 46, 31, Q(191, 256)),
        ("two modes", coherent, Q("0.814150670081"), 31, 22, Q(1)),
    ]
    print("readout | ideal score (estimate) | n | size at null bound | power at lower bound")
    for name, estimate, lower, n, boundary, tie in controls:
        require(lower <= estimate-error and estimate+error <= lower+Q(1, 10**12),
                f"{name} score enclosure")
        size = rejection(n, P0, boundary, tie)
        power = rejection(n, lower, boundary, tie)
        require(size <= ALPHA and power >= TARGET, f"{name} error targets")
        print(f"{name} | {float(estimate):.12f} | {n} | {float(size):.12f} | {float(power):.12f}")
    small, large = Q("0.000000000020"), Q("0.157079632800")
    inertia = below_shift(m, small), below_shift(m, large)
    require(inertia == (8, 10), "signed-matrix inertia")
    upper = neg + 8*small + 2*large + error
    require(upper < Q("0.814159265724"), "universal effect bound")
    best = most_powerful(30, Q("0.814159265724"))
    require(best < Q("0.93819744414"), "30-launch optimal power ceiling")
    print(f"inertia {inertia}; 30-launch power ceiling {float(best):.12f}")
    dephased = neg + sum(m[i][i] * (Q(A[i]**2, 20) + Q(B[i]**2, 684))
                         for i in range(10))
    upper_dephased = Q("0.628214404755")
    require(Q("0.628214404754") < dephased-error and dephased+error < upper_dephased,
            "dephased score enclosure")
    require(rejection(31, upper_dephased, 22, Q(1)) < Q("0.228244"), "dephased power")
    required = Q("0.813378364430")
    require(rejection(31, required-Q(1, 10**12), 22, Q(1)) < TARGET
            <= rejection(31, required, 22, Q(1)), "power threshold")
    visibility = Q("0.995847")
    require(visibility*coherent + (1-visibility)*dephased - error >= required,
            "visibility threshold")
    require(coherent-error-Q("0.000772305651") >= required, "effect tolerance")
    print(f"dephased score {float(dephased):.12f}; power < 0.228244")
    print("sufficient visibility 0.995847; sufficient effect tolerance 0.000772305651")


if __name__ == "__main__":
    main()
