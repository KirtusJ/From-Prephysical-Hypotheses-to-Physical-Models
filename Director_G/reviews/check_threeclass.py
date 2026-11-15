"""Exact algebraic checks for the three-coset product proof (no ring reachability assumed)."""
from collections import Counter
from math import comb



def add(x, y, r, k):
    carry, i = divmod(x[0] + y[0], 3)
    return i, (x[1] + y[1] + k * carry) % r


def multiset_product(a, b, r, k):
    c = Counter()
    for x, n in a.items():
        for y, m in b.items():
            c[add(x, y, r, k)] += n * m
    return c


def weighted(*terms):
    c = Counter()
    for n, x in terms:
        c[x] += n
    return c


def folded(coeffs, sign):
    return tuple(sum(coeffs[i] * sign ** (i // 3) for i in range(j, len(coeffs), 3))
                 for j in range(3))


def signed_counts(counts):
    return tuple(sum(n * (-1) ** j for (i, j), n in counts.items() if i == u)
                 for u in range(3))


def raw_coeffs(a, b):
    c = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i+j] += x * y
    return c


def square_basis(v, sign):
    x, y, z = v
    return x*x + y*y + z*z, x*y + y*z + sign*x*z


def require(condition, label):
    if not condition:
        raise ValueError(label)


def main():
    cases = 0
    for r in range(2, 11, 2):
        for k in range(r):
            unit, beta, eta = (0, 0), (1, 0), (0, -k % r)
            sign = (-1)**k
            e_beta = weighted((1,beta))
            eta_beta = add(eta, beta, r, k)
            factor = weighted((1,unit),(1,beta))
            a = multiset_product(weighted((4,unit),(1,eta),(1,eta_beta)), factor, r,k)
            b = multiset_product(weighted((1,unit),(2,beta)),weighted((1,unit),(2,beta),(1,eta_beta)),r,k)
            for d in range(2,33):
                require(multiset_product(e_beta, a, r,k) == b, "positive multisets disagree after translation")
                require(sum(a.values()) == sum(b.values()) == 12 * 2**(d-2), "cardinality mismatch")
                fac = [comb(d-2,j) for j in range(d-1)]
                u = raw_coeffs([4+sign,4+2*sign,sign],fac)
                v = raw_coeffs([1,4+sign,2*(2+sign)],fac)
                require(u[0]*u[-1] - v[0]*v[-1] == 2*sign-3, "top-lag separation failed")
                require(folded(u,sign) == signed_counts(a), "left product folding failed")
                require(folded(v,sign) == signed_counts(b), "right product folding failed")
                require(square_basis(folded(u,sign),sign) == square_basis(folded(v,sign),sign), "quadratic basis changed after translation")
                a,b = multiset_product(a,factor,r,k),multiset_product(b,factor,r,k)
                cases += 1
    # With the negative twist, pretending the wrap is unsigned must fail.
    sign = -1
    negative = (2, 3, -5)
    shifted = (sign*negative[2], negative[0], negative[1])
    require(square_basis(shifted, sign) == square_basis(negative, sign), "negative twist failed invariance")
    require(square_basis(shifted, +1) != square_basis(negative, +1), "incorrect twist escaped the control")
    print(f"{cases} relation/degree cases passed; wrong-wrap control detected.")


if __name__ == '__main__':
    main()
