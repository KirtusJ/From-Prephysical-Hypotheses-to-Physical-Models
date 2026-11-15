"""Short-horizon tests for the ideal five-site Hadamard launch-port return."""
from math import inf, nextafter
from fractions import Fraction as F
from itertools import product
import json


def require(condition, label):
    if not condition:
        raise ArithmeticError(label)


def returns(last_tick):
    amplitudes = [1] + [0] * 9
    out = []
    for t in range(last_tick + 1):
        out.append(F(amplitudes[0]**2, 2**t))
        advanced = [0] * 10
        for x in range(5):
            r, l = amplitudes[2*x:2*x+2]
            advanced[2*((x+1) % 5)] = r+l
            advanced[2*((x-1) % 5)+1] = r-l
        amplitudes = advanced
    return out


def det_mod(matrix, modulus):
    """Eliminate over the prime field, after reducing rational entries."""
    a = [[int(x.numerator) * pow(int(x.denominator), -1, modulus) % modulus
          for x in row] for row in matrix]
    det = 1
    for k in range(len(a)):
        pivot = next((i for i in range(k, len(a)) if a[i][k]), None)
        if pivot is None:
            return 0
        if pivot != k:
            a[k], a[pivot] = a[pivot], a[k]
            det = -det
        det = det * a[k][k] % modulus
        inverse = pow(a[k][k], -1, modulus)
        for i in range(k+1, len(a)):
            factor = a[i][k] * inverse % modulus
            for j in range(k+1, len(a)):
                a[i][j] = (a[i][j]-factor*a[k][j]) % modulus
    return det


def cdf(n, k, p):
    """Binomial cumulative probability through k by exact integer recurrence."""
    if k < 0:
        return F(0)
    if k >= n:
        return F(1)
    a, b = p.as_integer_ratio()
    c = b-a
    mass = c**n
    total = mass
    for j in range(k):
        mass = mass * (n-j) * a // ((j+1)*c)
        total += mass
    return F(total, b**n)


def check_chain(matrix, b, expected):
    require(all(sum(row) == 1 and min(row) >= 0 for row in matrix), "stochastic rows")
    row = [1] + [0]*(len(matrix)-1)
    for target in expected:
        require(sum(w*z for w,z in zip(row, b)) == target, "prefix realization")
        row = [sum(w*m[j] for w,m in zip(row, matrix)) for j in range(len(matrix))]


def main():
    p = returns(51)
    require(p[:6] == [1, 0, F(1, 4), 0, F(1, 16), F(1, 32)], "first six port probabilities")
    minors = []
    for h in range(1, 27):
        matrix = [[1, *p[i:i+h]] for i in range(h+1)]
        minors.append(det_mod(matrix, 1009))
    require(all(minors[:25]) and minors[25] == 0, "rank certificates")

    M = [[1, *p[i:i+3]] for i in range(4)]
    B = [[F(-2,3), 2, F(20,3), -8], [F(4,3), 4, F(-16,3), 0], [8, -8, -32, 32]]
    for i, row in enumerate(B):
        for j in range(4):
            require(sum(x*m[j] for x, m in zip(row, M)) == int(j==i+1), "inverse rows")
    norm = max(sum(abs(sum(x*y for x,y in zip(b, v))) for b in B)
               for v in product((-1,1), repeat=4))
    require(norm == 100, "inverse norm")
    a = F(1,4)
    check_chain([[1]], [1], p[:1])
    check_chain([[0,1],[a,1-a]], [1,0], p[:3])
    check_chain([[0,1,0],[a,0,1-a],[0,0,1]], [1,0,0], p[:5])
    check_chain([[0,1,0,0],[a,0,1-a,0],[0,0,0,1],[0,F(1,6),0,F(5,6)]],
                [1,0,0,0], p[:6])

    delta = F(1,100)
    ideal_reject = F(0)
    rival_accept = (1-delta)**299
    rows = []
    for t, n, lo, hi in [(2,31100,7593,7958), (4,10300,586,703), (5,5700,147,210)]:
        ideal = cdf(n,lo-1,p[t]) + 1-cdf(n,hi,p[t])
        low_rival = 1-cdf(n,lo-1,p[t]-delta)
        high_rival = cdf(n,hi,p[t]+delta)
        rows.append([t, n, lo, hi, float(ideal), float(low_rival), float(high_rival)])
        ideal_reject += ideal
        rival_accept = max(rival_accept, low_rival, high_rival)
    require(ideal_reject < F(47619,10**6) and rival_accept < F(49537,10**6), "count design")
    print(json.dumps({"first_six_probabilities": [str(x) for x in p[:6]],
                      "augmented_hankel_determinants_mod_1009_h_1_to_26": minors,
                      "inverse_operator_norm": int(norm),
                      "worst_tick_gap_lower_bound": "1/100",
                      "successive_exact_prefix_minima": [1,2,2,3,3,4],
                      "remaining_count_rows_t_n_L_U_ideal_low_high": rows,
                      "launches": 47997, "largest_tick": 5,
                      "ideal_error_upper": nextafter(float(ideal_reject), inf),
                      "rival_error_upper": nextafter(float(rival_accept), inf)}, indent=2))


if __name__ == "__main__":
    main()
