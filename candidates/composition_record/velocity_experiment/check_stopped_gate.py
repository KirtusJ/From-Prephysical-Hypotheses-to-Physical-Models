"""First block meeting both conditions: site 0 and distance from H at most 1/32.

Run: python -I -B check_stopped_gate.py
Assumes the ideal repeated 12-tick instrument. Distance is the operator norm
minimized over a global sign. Each row counts all original launches. The
initial instant is excluded. All predicates and probabilities use integers.
"""

from collections import defaultdict
from fractions import Fraction
from math import gcd
from pathlib import Path
from runpy import run_path


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def block_matrices():
    walk = run_path(str(Path(__file__).with_name("check_scalar_walk.py")))
    word = walk["ALL_SCALAR"]
    matrices = defaultdict(lambda: [0] * 4)
    for index, matrix in enumerate(walk["kernels"](word)):
        address = (2 * index - len(word)) % 16
        for entry, value in enumerate(matrix):
            matrices[address][entry] += value
    return matrices, 2 ** word.count("H")


def orthogonal_steps(matrices):
    steps = []
    for address, (a, b, c, d) in sorted(matrices.items()):
        weight = a * a + c * c
        require(weight > 0, "unexpected dark address")
        determinant = a * d - b * c
        orientation = 1 if determinant > 0 else -1
        require((b, d) == (-orientation * c, orientation * a),
                "block failed the scalar orthogonality test")
        steps.append((address, a, c, orientation, weight))
    return steps


def advance(state, step):
    """Track first-column direction and determinant sign, modulo global sign."""
    site, u, v, orientation = state
    displacement, a, b, sign, _ = step
    real, imag = a * u - b * sign * v, b * u + a * sign * v
    divisor = gcd(real, imag)
    if real < 0 or (real == 0 and imag < 0):
        divisor = -divisor
    return (site + displacement) % 16, real // divisor, imag // divisor, sign * orientation


def is_hit(state):
    site, u, v, orientation = state
    # Opposite determinant from H gives distance 2 for either global sign.
    # For a reflection, distance² = 2 - 2 |u+v| / sqrt(2(u²+v²)).
    return (site == 0 and orientation == -1 and
            2048**2 * (u + v)**2 >= 2 * 2047**2 * (u * u + v * v))


def first_hit_probabilities(steps, denominator, horizon):
    live = {(0, 1, 0, 1): 1}
    probabilities = []
    for tick in range(1, horizon + 1):
        following = defaultdict(int)
        for state, path_weight in live.items():
            for step in steps:
                successor = advance(state, step)
                if not is_hit(successor):
                    following[successor] += path_weight * step[-1]
        live = following
        probabilities.append(1 - Fraction(sum(live.values()), denominator**tick))
    return probabilities


def direct_tree(matrices, denominator, depth):
    """Enumerate complete short paths with raw 2x2 products and the H trace."""
    first_hits = [0] * depth

    def extend(tick, site, matrix, weight):
        u, v, w, z = matrix
        for displacement, (a, b, c, d) in matrices.items():
            product = (a * u + b * w, a * v + b * z, c * u + d * w, c * v + d * z)
            r, s, t, h = product
            total = weight * (a * a + c * c)
            endpoint = (site + displacement) % 16
            # trace(H^T O) = (r+s+t-h)/sqrt(2*total).
            if (endpoint == 0 and r * h - s * t < 0 and
                    2048**2 * (r + s + t - h)**2 >= 8 * 2047**2 * total):
                first_hits[tick - 1] += total
            elif tick < depth:
                extend(tick + 1, endpoint, product, total)

    extend(1, 0, (1, 0, 0, 1), 1)
    cumulative = Fraction(0)
    for tick, weight in enumerate(first_hits, start=1):
        cumulative += Fraction(weight, denominator**tick)
        yield cumulative


def main():
    matrices, denominator = block_matrices()
    steps = orthogonal_steps(matrices)
    by_address = {step[0]: step for step in steps}
    require(denominator == sum(step[-1] for step in steps) == 128, "block normalization")
    require(is_hit((0, 1, 1, -1)) and is_hit((0, -1, -1, -1)), "H or -H rejected")
    require(is_hit((0, 17, 16, -1)) and not is_hit((0, 16, 15, -1)), "angle threshold")
    require(not any(is_hit(state) for state in ((0, 1, 1, 1), (2, 1, 1, -1),
                                                 (0, 1, 0, -1))), "wrong orientation, site or angle accepted")

    path = (4, 8, 0, 12, 8)
    state, weight = (0, 1, 0, 1), 1
    for displacement in path:
        step = by_address[displacement]
        state = advance(state, step)
        weight *= step[-1]
    require(state == (0, 71, 69, -1) and is_hit(state), "five-block example")
    print(f"Example {path}: state={state}, probability={Fraction(weight, denominator**len(path))}")

    probabilities = first_hit_probabilities(steps, denominator, 12)
    require(probabilities[:5] == list(direct_tree(matrices, denominator, 5)), "raw matrix tree mismatch")
    require(probabilities[:4] == [0] * 4, "unexpected early hit")
    for tick, expected in ((5, Fraction(14703, 268435456)),
                           (8, Fraction(40869439, 274877906944)),
                           (12, Fraction(1039325527453239, 2305843009213693952))):
        require(probabilities[tick - 1] == expected, f"first hit by block {tick}")
    for tick, probability in enumerate(probabilities, start=1):
        print(f"Hit by block {tick:2d}: {probability}")


if __name__ == "__main__":
    main()
