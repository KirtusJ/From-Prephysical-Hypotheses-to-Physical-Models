"""Exact finite checks for the release revival and four-preparation EB benchmark.

A is the incident matching-basis survival rate. p is the probability that the
trusted inverse of the coherent six-qubit preparation returns all zeros.
Run python -I -B check_revival_benchmark.py. No device records are used.
"""

from fractions import Fraction as F
from pathlib import Path
from runpy import run_path


def require(value, message):
    if not value:
        raise AssertionError(message)


def basis_flag(t):
    """Equal source labels. External basis flags proportional to (1, ±t)."""
    norm = 1 + t*t
    inner_product = (1-t*t) / norm
    revival = (1+inner_product) / 2
    # The optimal basis guess measures the flag in the ± basis.
    guess = (1+t)**2 / (2*norm)
    # Correct basis gives survival 1; wrong basis gives 1/2.
    score = guess + (1-guess)/2
    require(revival == 1/norm and score == F(3, 4) + t/(2*norm),
            "fair labels, retained coherence and measured score")
    require((score-F(3, 4))**2 == revival*(1-revival)/4,
            "sharp upper branch attained")
    return revival, score


def support_checks():
    # t > 1 is the supporting parameter for H = 2M-I. For u in [0,1],
    # these two nonnegative secant surpluses justify moving all planar norm
    # to a single axis in the ideal-state resolvent bound.
    for t in (F(9, 8), F(3, 2), F(3), F(19)):
        z = t*t
        for u in (F(0), F(1, 11), F(1, 2), F(7, 8), F(1)):
            first = (1-u)/z + u/(z-1) - 1/(z-u)
            second = u/(z-1)**2 - u/(z-u)**2
            require(first == u*(1-u)/(z*(z-1)*(z-u)) and first >= 0,
                    "resolvent secant for inverse")
            require(second == u*(1-u)*(2*z-1-u)/((z-1)**2*(z-u)**2) and second >= 0,
                    "resolvent secant for squared inverse")

        # Rational Bloch directions and a shorter output Bloch vector.
        vectors = [(1, 0), (0, -1), (F(3, 5), F(4, 5)),
                   (F(-12, 13), F(5, 13)), (F(1, 4), F(1, 4)), (0, 0)]
        support = (1/(t-1) + 1/t)/2
        for output in vectors:
            for measurement in vectors:
                value = sum((t+r*n)/(z-n*n) for r, n in zip(measurement, output))/2
                require(value <= support, "EB resolvent support")
        require((t+1)/(2*(z-1)) + t/(2*z) == support, "axis attains support")

    for n in range(13):
        t = F(n, 12)
        p, score = basis_flag(t)
        if t == 0:
            require((p, score) == (1, F(3, 4)), "indistinguishable basis flags")
        elif t == 1:
            require((p, score) == (F(1, 2), 1), "orthogonal basis flags")
        else:
            # Optimal support v = 2t_resolvent-1 = sqrt(p/(1-p)).
            v = 1/t
            require(2*score-1 == (1+(1-p)*v+p/v)/2, "support attained")

    # With orthogonal flags the EB device learns the basis exactly.
    # One private sign branch per basis gets a phase exp(i phi). Projection
    # onto the ideal preparation sums the two branch amplitudes in each flag.
    for cosine, sine in [(-1, 0), (F(-3, 5), F(4, 5)), (0, 1),
                         (F(3, 5), F(4, 5)), (1, 0)]:
        require(cosine**2 + sine**2 == 1, "unit phase")
        flag_amplitude = F(1+cosine, 4), F(sine, 4)
        revival = 2*sum(x*x for x in flag_amplitude)
        require(revival == F(1+cosine, 4), "unit-score lower branch")


def main():
    support_checks()
    walk = run_path(str(Path(__file__).with_name("check_four_state_alphabet.py")))
    steps = walk["record"]["read_steps"]()
    score = walk["exact_four"](steps, 7)
    require(score == F(226560354573, 274877906944), "seven-write score")
    radicand = 1-16*(score-F(3, 4))**2
    require(radicand == F(4306127965074464560471, 4722366482869645213696),
            "critical revival squared root")
    # p_crit = (1+sqrt(radicand))/2. Open rational interval, no float.
    lower = F(977456297837, 10**12)
    upper = F(977456297838, 10**12)
    require((2*lower-1)**2 < radicand < (2*upper-1)**2, "critical revival bracket")
    print(f"Seven-write ideal survival {score}.")
    print("Critical revival lies strictly between 0.977456297837 and 0.977456297838.")
    print("Fair pure basis flags attain the upper curve; orthogonal flags give p=1/2, A=1.")


if __name__ == "__main__":
    main()
