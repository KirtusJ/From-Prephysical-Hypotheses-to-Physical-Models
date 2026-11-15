"""Verify the trusted return read for the four-path heralded reference.

    python -I -B -O check_hidden_herald_return.py

Use a common signed power on the positive support of one six-cell terminal
instrument, with dark cells excluded even at negative powers.
The inverse operates on the source and its protected registers only.
The extra routing tags must be fresh; the binary return is not scored
before the six-way read. Measured counts and calibration errors would
be needed for a physical test. All bound checks below use integers or
fractions. Decimal displays of the analytic minimum are illustrative.
"""

from fractions import Fraction as F
from math import exp, log
from pathlib import Path
from runpy import run_path


def require(ok, name):
    if not ok:
        raise ArithmeticError(name)


def cut_geometry():
    lib = run_path(str(Path(__file__).with_name("check_heralded_gate_reference.py")))
    pair, capacity, _ = lib["parameters"](2)
    scale_squared = 2*capacity**2
    # Columns of W restricted to the four inputs B, before dividing all
    # amplitudes by sqrt(scale_squared). Keep every physical output row.
    sectors = [[], []]
    for a, b in pair:
        table = lib["routed_columns"](a, b, capacity)
        for flag, paths in enumerate(table):
            for path, matrix in enumerate(paths):
                sector = int(flag == path == 0)
                sectors[sector].extend(matrix[4*i:4*i+4] for i in range(4))
    fractions = []
    for rows in sectors:
        gram = [[sum(row[i]*row[j] for row in rows) for j in range(4)] for i in range(4)]
        energy = gram[0][0]
        require(gram == [[energy*int(i==j) for j in range(4)] for i in range(4)],
                "restricted sector Gram")
        # Thus the sector compression of P=W B W† is (energy/scale²)
        # times a rank-four orthogonal projector. Extra rows in each sector
        # give a nontrivial nullspace for a possible corrupted state.
        require(energy > 0 and len(rows) > 4, "room for sector corruption")
        fractions.append(F(energy, scale_squared))
    require(fractions == [F(11,16), F(5,16)], "failure/success eigenvalues")
    return fractions[1]


def routed_weights(w):
    # Four equally likely routing settings lift a rejected return to the
    # good group on one setting. Two more bits choose one of its four
    # cells. Four final path bits select the 1:15 failure subdivision.
    weights = [F(0)]*6
    for returned, mass in ((True,w), (False,1-w)):
        nascent = [0]*6
        for bypass in range(4):
            for label in range(4):
                for path in range(16):
                    cell = label if returned or bypass == 0 else 4+int(path != 0)
                    nascent[cell] += 1
        for i, n in enumerate(nascent):
            weights[i] += mass*n/256
    u = F(1,4)+3*w/4
    require(weights == [u/4]*4+[(1-u)/16,15*(1-u)/16], "six terminal masses")
    require(sum(weights) == 1, "all terminal cells included")
    return weights


def certify_sum_lower(x, k, m, nonnegative_q, fail_lower):
    """Weighted AM-GM for x^q+(15x)^q. The mean has weights k/m, 1-k/m."""
    y = 15*x
    # If (x^k y^(m-k))^q >= 1, the sum is >= exp(binary entropy(k/m)).
    ratio_n = x.numerator**k*y.numerator**(m-k)
    ratio_d = x.denominator**k*y.denominator**(m-k)
    require(ratio_n >= ratio_d if nonnegative_q else ratio_n <= ratio_d,
            "AM-GM product orientation")
    odds_sum = 4*fail_lower/(1-fail_lower)
    require((m*odds_sum.denominator)**m >
            odds_sum.numerator**m * k**k * (m-k)**(m-k), "strict rational lower bound")


def upper_power(x, numerator, denominator, precision):
    """Upper grid bound for x^(numerator/denominator) by integer comparisons."""
    target = x.numerator**numerator * precision**denominator
    factor = x.denominator**numerator
    lo, hi = 0, precision
    while hi**denominator*factor < target:
        hi *= 2
    while hi-lo > 1:
        mid = (lo+hi)//2
        if mid**denominator*factor < target:
            lo = mid
        else:
            hi = mid
    return F(hi, precision)


def minimum(x):
    # Setting t=log(15x)/log(15) makes x^t (15x)^(1-t) exactly 1.
    # Equality in weighted AM-GM holds at q=log((1-t)/t)/log(15).
    t = log(float(15*x))/log(15)
    q = log((1-t)/t)/log(15)
    pair_sum = exp(-t*log(t)-(1-t)*log(1-t))
    return q, pair_sum/(4+pair_sum)


def main():
    s = cut_geometry()
    lo = routed_weights(F(0))
    # The normalized failure-sector projection of any W B input attains
    # w=1-s. This uses the allowed change in sector populations.
    hi = routed_weights(1-s)
    ideal = routed_weights(F(1))
    require(ideal == [F(1,4)]*4+[0,0], "ideal has only four bright goods")
    x0, x1 = hi[4]/hi[0], lo[4]/lo[0]
    require((x0,x1) == (F(15,196), F(3,4)), "full range of smaller failure/good")
    require(x1 < 1 < 15*x0, "a failure is both unique minimum and unique maximum")
    # In particular both signed-infinite selectors give unit failure.
    # q>=0 selects the lower x endpoint for the worst sum; q<=0 the upper.
    # t(x0) < 1-t(x1) < 1/2, so the first entropy is strictly smaller.
    require(15*x0*x1 < 1 and 15*x1*x1 > 1, "endpoint entropy ordering")
    lower, upper = F(234157974,10**9), F(234157977,10**9)
    certify_sum_lower(x0, 430, 8439, True, lower)
    certify_sum_lower(x1, 9, 10, False, lower)
    trial = sum(upper_power(x, 27, 25, 10**11) for x in (x0,15*x0))
    require(trial/(4+trial) < upper, "near-tight finite exponent 27/25")
    # Every common monotone response assigns at least as much to one
    # failure as to a good. Monotone step responses attain the bound.
    for test in (lambda x: x >= hi[0], lambda x: x <= hi[0]):
        assigned = list(map(test, hi))
        require(F(sum(assigned[4:]), sum(assigned)) == F(1,5), "monotone sharpness")
    print(f"All six cells, both cut Grams and exact rational bracket pass: "
          f"{lower} < minimum failure < {upper}.")
    for x in (x0,x1):
        q, failure = minimum(x)
        print(f"x={x}, optimal signed q={q:.10f}, failure={failure:.12f}")
    # Fixed unperturbed sector populations give the smaller return bound
    # s²+(1-s)². A pure Lüders write without sector corruption attains it.
    kept = s*s+(1-s)**2
    weights = routed_weights(kept)
    require(kept == F(73,128) and weights[4]/weights[0] == F(165,1388),
            "Luders return")
    _, loss = minimum(F(165,1388))
    print(f"Luders write (w={kept}) has minimum failure {loss:.12f}; "
          "general monotone floor 1/5; ideal failure zero.")


if __name__ == "__main__":
    main()
