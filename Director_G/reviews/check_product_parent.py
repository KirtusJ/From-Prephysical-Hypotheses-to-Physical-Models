"""Exact controls for the transfer and lag-coordinate steps in G10 Theorem 5.69."""
from fractions import Fraction
from itertools import product
from math import comb
import json


def require(condition, explanation):
    if not condition:
        raise ValueError(explanation)


def determinant(matrix):
    rows = [list(map(Fraction, row)) for row in matrix]
    sign = 1
    for i in range(len(rows)):
        pivot = next((j for j in range(i, len(rows)) if rows[j][i]), None)
        if pivot is None:
            return Fraction(0)
        if pivot != i:
            rows[i], rows[pivot] = rows[pivot], rows[i]
            sign = -sign
        for j in range(i + 1, len(rows)):
            multiplier = rows[j][i] / rows[i][i]
            for k in range(i, len(rows)):
                rows[j][k] -= multiplier * rows[i][k]
    result = Fraction(sign)
    for i, row in enumerate(rows):
        result *= row[i]
    return result


def multiply_linear(coefficients, constant, slope):
    result = [0] * (len(coefficients) + 1)
    for i, value in enumerate(coefficients):
        result[i] += constant * value
        result[i + 1] += slope * value
    return result


def lag_control(factors):
    polynomial, symmetric = [1], [1]
    for left, right in factors:
        polynomial = multiply_linear(polynomial, left, right)
        symmetric = multiply_linear(symmetric, left**2 + right**2, left * right)
    lags = [sum(a*b for a, b in zip(polynomial, polynomial[d:]))
            for d in range(len(polynomial))]
    predicted = [sum(comb(j, (j-d)//2) * symmetric[j]
                     for j in range(d, len(symmetric), 2))
                 for d in range(len(symmetric))]
    require(lags == predicted, ("lag basis", factors, lags, predicted))
    return lags


def main():
    # Values of (n,D,B) for an identity singleton, 1+delta, and 1+beta.
    evaluations = [(1, 1, 0), (2, 0, 0), (2, 2, 1)]
    require(determinant(evaluations) == -2, "count and the two quadratic functions are dependent")
    empty = (0, 0)
    require(lag_control((empty,)) == [0, 0], "empty factor contributes nonzero quadratic part")
    require(lag_control(((1, -1), empty)) == [0, 0, 0], "zero product contributes nonzero lag")
    # Padding by a singleton preserves the pure count product independently of lags.
    n1, n2 = 2, 3
    require(n1*n2*1 == n1*n2 and n1*n2*0 == 0, "identity/empty cardinality")
    tests = 0
    factors = ((1, 0), (0, 1), (1, -1), (2, 1), (-1, -2))
    for k in range(1, 6):
        matrix = [[comb(j, (j-d)//2) if j >= d and (j-d) % 2 == 0 else 0
                   for j in range(k + 1)] for d in range(k + 1)]
        require(determinant(matrix) == 1, "nonunit lag basis change")
        for choice in product(factors, repeat=k):
            lags = lag_control(choice)
            require(lag_control((*choice, (1, 0))) == lags + [0], "degree padding")
            tests += 1
    # A symmetric separately allowed expression, tested by transferring E=1+delta
    # between P=1 and Q=E: E*1, E versus 1, E*E.
    def mixed(p, q):
        return p[0] * q[1] + p[1] * q[0]
    e, identity, e_squared = (2, 0), (1, 1), (4, 0)
    fails_left, fails_right = mixed(e, e), mixed(identity, e_squared)
    require((fails_left, fails_right) == (0, 4), "mixed term escaped transfer control")
    print(json.dumps({"factor_tuples": tests, "max_factors": 5, "dimension_control": -2,
                      "lag_basis_determinants": [1] * 5,
                      "mixed_term_transfer": [fails_left, fails_right]}, sort_keys=True))


if __name__ == "__main__":
    main()
