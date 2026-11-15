"""Exact lower bounds for a 55-state return witness on short time grids.

Python 3 standard library. Every interval endpoint is an integer divided by
2**240. The circuit uses only arithmetic and outward-rounded square roots.
"""
from fractions import Fraction
from math import isqrt
import json

SCALE = 1 << 240


def require(condition, label):
    if not condition:
        raise ArithmeticError(label)


def point(value):
    return value * SCALE, value * SCALE


def add(a, b):
    return a[0] + b[0], a[1] + b[1]


def neg(a):
    return -a[1], -a[0]


def sub(a, b):
    return add(a, neg(b))


def mul(a, b):
    bounds = [x*y for x in a for y in b]
    return min(bounds) // SCALE, -(-max(bounds) // SCALE)


def div(a, b):
    require(b[0] > 0, "denominator crosses zero")
    inverse = SCALE**2 // b[1], -(-SCALE**2 // b[0])
    return mul(a, inverse)


def sqrt(a):
    require(a[0] >= 0, "negative radicand")
    return isqrt(a[0]*SCALE), isqrt(a[1]*SCALE) + 1


def cmul(z, w):
    return sub(mul(z[0], w[0]), mul(z[1], w[1])), add(mul(z[0], w[1]), mul(z[1], w[0]))


def conjugate(z):
    return z[0], neg(z[1])


def power(z, n):
    result = point(1), point(0)
    factor = z if n >= 0 else conjugate(z)
    for _ in range(abs(n)):
        result = cmul(result, factor)
    return result


def squared_distance(z, w):
    # For unit nodes the dot-product formula avoids interval squaring near zero.
    return sub(point(2), mul(point(2), cmul(z, conjugate(w))[0]))


def mode(cos_k):
    sin_omega = sqrt(div(sub(point(1), mul(cos_k, cos_k)), point(2)))
    cos_omega = sqrt(sub(point(1), mul(sin_omega, sin_omega)))
    weight = div(add(point(1), div(cos_k, mul(sqrt(point(2)), cos_omega))), point(10))
    return (cos_omega, sin_omega), weight


def path_probabilities():
    state = [1] + [0]*9
    probabilities = []
    for t in range(56):
        probabilities.append(Fraction(state[0]**2, 2**t))
        out = [0]*10
        for j in range(5):
            right, left = state[2*j:2*j+2]
            out[2*((j+1) % 5)] = right + left
            out[2*((j-1) % 5)+1] = right - left
        state = out
    return probabilities


def coefficient_table(e1, e2, w1, w2):
    # A mode label (s,i,j) stands for (-1)^s e1^i e2^j. The
    # five spatial Fourier blocks give ten individual projector weights.
    block_mass = div(point(1), point(5))
    zero_imbalance = div(point(1), sqrt(point(2)))
    ten = point(10)
    modes = [((0, 0, 0), div(add(point(1), zero_imbalance), ten)),
             ((1, 0, 0), div(sub(point(1), zero_imbalance), ten))]
    for axis, weight in enumerate((w1, w2)):
        for orientation in (1, -1):
            i, j = (orientation, 0) if axis == 0 else (0, orientation)
            modes.extend([((0, i, j), weight),
                          ((1, -i, -j), sub(block_mass, weight))])
    weights = {}
    for (s, i, j), a in modes:
        for (t, k, l), b in modes:
            label = ((s-t) % 2, i-k, j-l)
            weights[label] = add(weights.get(label, point(0)), mul(a, b))
    nodes = {}
    for (s, i, j), weight in weights.items():
        node = cmul(power(e1, i), power(e2, j))
        nodes[s, i, j] = (tuple(neg(x) for x in node) if s else node, weight)
    return nodes


def certify_grid(nodes, retained, inverse_c, derivative_floor, exponent):
    # Reciprocal partial fractions bound the product of distances from
    # each eigenvalue to all non-torsion nodes. All distances are rounded down.
    one = point(1), point(0)
    reciprocal_sum = Fraction(0)
    positive_count = len(nodes)
    for key, (node, weight) in nodes.items():
        require(Fraction(weight[0], SCALE) > Fraction(1, 100), "spectral weight")
        derivative = Fraction(1)
        for other_key, (other, _) in nodes.items():
            if key != other_key:
                derivative *= Fraction(sqrt(squared_distance(node, other))[0], SCALE)
        d_squared = min(Fraction(squared_distance(power(node, k), one)[0], SCALE)
                        for k in range(1, 56))
        require(derivative > 0 and d_squared > 0, "node collision")
        reciprocal_sum += 440 / (derivative * d_squared)
        interpolation_denominator = derivative
        for other in retained:
            interpolation_denominator *= Fraction(sqrt(squared_distance(node, other))[0], SCALE)
        require(interpolation_denominator > derivative_floor, "interpolation denominator")
    require(reciprocal_sum < inverse_c, "uniform reciprocal sum")
    m = positive_count + len(retained)
    prefactor = Fraction(derivative_floor, 100 * 2**(55 + m - 1))
    # Remove the positive_count-th root by raising both sides to that power.
    require(prefactor**positive_count / inverse_c**55 > Fraction(1, 10**exponent)**positive_count,
            "uniform prefix error")


def main():
    root5 = sqrt(point(5))
    e1, w1 = mode(div(sub(root5, point(1)), point(4)))
    e2, w2 = mode(div(sub(point(-1), root5), point(4)))
    nodes = coefficient_table(e1, e2, w1, w2)
    require(len(nodes) == 26, "distinct full-clock labels")
    nodes.pop((0, 0, 0))
    minus_one, _ = nodes.pop((1, 0, 0))
    certify_grid(nodes, [minus_one], 6_000_000, 6, 41)
    even = {}
    for (s, i, j), (node, weight) in nodes.items():
        if (i, j) not in even:
            even[i, j] = (power(node, 2), point(0))
        squared, other_weight = even[i, j]
        even[i, j] = squared, add(other_weight, weight)
    require(len(even) == 12, "distinct even-clock labels")
    certify_grid(even, [], 3_000_000, 5, 51)

    p = path_probabilities()
    alpha = [Fraction(1)] + [Fraction(0)]*54
    for t in range(56):
        require(sum(m*v for m, v in zip(alpha, p[:55])) == p[t], "55-state interpolation")
        last = alpha[-1]
        alpha = [last*p[55], alpha[0]+last*(1-p[55]), *alpha[1:-1]]
    print(json.dumps({"prefix_fit_through_tick": 55, "last_row_probability_to_state_0": str(p[55]),
                      "even_settings": 67, "even_latest_tick": 132, "even_gap_greater_than": "1e-51",
                      "full_settings": 80, "full_latest_tick": 79, "full_gap_greater_than": "1e-41",
                      "dimension_bound": 55}))


if __name__ == "__main__":
    main()
