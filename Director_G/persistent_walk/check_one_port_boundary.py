"""Exact binomial boundary calculation for the pinned five-site score bounds."""
from fractions import Fraction as F
from math import ceil, comb, floor


def boundary_probabilities(n, k, p):
    """Return P(X>k), P(X=k) for X binomial(n,p), as exact fractions."""
    a, d = p.as_integer_ratio()
    b = d - a
    point = comb(n, k) * a**k * b**(n-k)
    term, tail = point, 0
    for j in range(k, n):
        term, rem = divmod(term * (n-j) * a, (j+1) * b)
        if rem:
            raise ArithmeticError('nonintegral binomial mass numerator')
        tail += term
    return F(tail, d**n), F(point, d**n)


def main():
    p0 = F(1,2) + F(1369,31250)/F(636615,10**6) + F(1,10**9)
    p1 = F(1,2) + F(20699999689,258750000000)/F(636625,10**6) - F(1,10**9)
    alpha = F(1,20)
    coin = F(115, 1024)
    print(f'Finite-bit null success <= {ceil(p0 * 10**12) / 10**12:.12f}, '
          f'target success >= {floor(p1 * 10**12) / 10**12:.12f}')
    for n in (803, 804):
        null_tail, null_point = boundary_probabilities(n, 480, p0)
        target_tail, target_point = boundary_probabilities(n, 480, p1)
        if n == 803:
            optimal = (alpha-null_tail) / null_point
            power = target_tail + optimal * target_point
            if not (0 <= optimal <= 1 and power < 1-alpha):
                raise ArithmeticError('803 endpoint ceiling')
            print(f'803: maximum endpoint power at size .05 <= {ceil(power * 10**12) / 10**12:.12f}')
        else:
            size = null_tail + coin * null_point
            power = target_tail + coin * target_point
            if not (size < alpha and power > 1-alpha):
                raise ArithmeticError('804 boundary rule')
            print(f'804: size <= {ceil(size * 10**12) / 10**12:.12f}, power >= {floor(power * 10**12) / 10**12:.12f}')


if __name__ == '__main__':
    main()
