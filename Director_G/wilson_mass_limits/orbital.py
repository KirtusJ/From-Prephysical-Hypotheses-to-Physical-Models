"""Exact constants and numerical checks of the normalized cell-constant spinor."""
from fractions import Fraction as F
from math import cos, exp, hypot, log, pi, sin, sqrt


def require(condition, message):
    if not condition:
        raise ValueError(message)


def check_constants():
    # (23/24)^2*25/(216 sqrt(3)) > 1/20, with no floating square roots.
    lhs = 20*25*F(23,24)**2
    require(lhs**2 > 3*216**2, "squared occupation constant is too small")
    require(1-F(1,6) == F(5,6), "first Taylor constant differs")
    require(1-F(1,24) == F(23,24), "second Taylor constant differs")
    require(F(2,20**2) == F(1,200), "entropy lower-bound coefficient differs")
    require(F(6,200) == F(3,100), "relative-law comparison coefficient differs")
    print("Squared rational comparisons for the occupation and entropy constants passed.")

def check_interval(L):
    from scipy.integrate import quad
    mu = 1/L
    m = mu/L
    cuts = sorted(set([0,m,1/L,pi] + [2*pi*j/L for j in range(1,L//2+1)]))
    def fejer(k):
        return (sin(L*k/2)/sin(k/2))**2/L if k else L
    def direct(k):
        x=2*sin(k/2)**2
        z=(m+x)/sqrt(m*m+2*(1+m)*x)
        return fejer(k)*(z-sin(k/2))/(2*pi)
    occupancy=sum(quad(direct,left,right,epsabs=1e-14)[0] for left,right in zip(cuts,cuts[1:]))
    # Separate integral over only the favorable band, calculated from d_s Z_s.
    def band(logk):
        k=exp(logk)
        def deriv(t):
            s=m*t
            e2=s*s+4*(1+s)*sin(k/2)**2
            return m*sin(k)**2/e2**1.5
        return k*fejer(k)*quad(deriv,0,1,epsabs=1e-14)[0]/(2*pi)
    positive_band=quad(band,log(m),log(1/L),epsabs=1e-14)[0]
    lower=mu*log(1/mu)/(20*pi)
    require(occupancy>=positive_band>=lower, "positive-band integral violates the occupation bounds")
    print(f"L={L}, mu=1/L: delta={occupancy:.12g}, positive band={positive_band:.12g}, "
          f"rigorous delta floor={lower:.12g}")

def compare(length, mass):
    from scipy.integrate import quad
    bare = mass / length

    def defect(k):
        if k == 0.0:
            return 1.0
        sine = sin(k)
        z = 2 * sin(k / 2) ** 2
        e0 = 2 * sin(k / 2)
        em = hypot(sine, z + bare)
        # Rationalized difference of the two z components avoids loss at small m.
        return bare * (2*z + bare) * sine**2 / (e0*em*((z+bare)*e0 + z*em))

    def fejer(k):
        return (sin(length*k/2)/sin(k/2))**2 / length if k else length

    def integral(fun):
        points = [0, bare, 1/length, pi]
        return sum(quad(fun, a, b, epsabs=3e-14*mass, epsrel=3e-12, limit=800)[0]
                   for a, b in zip(points, points[1:])) / (2*pi)

    mode = integral(lambda k: fejer(k)*defect(k))
    # Form the scalar Toeplitz displacement diagonals separately.
    matrix = integral(defect)
    for r in range(1, length):
        matrix += 2*(length-r)/length * integral(lambda k: cos(r*k)*defect(k))
    require(abs(mode-matrix) <= 2e-12*abs(mode), "Fejér integral and Toeplitz mean disagree")
    bound = mass*log(1/mass)/(20*pi)
    require(mode >= bound, "full occupation shift falls below the analytical bound")
    return mode, matrix, 2*pi*mode/mass - log(1/mass), mode/bound


if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--quadrature", action="store_true", help="run the optional SciPy quadratures")
    options = parser.parse_args()
    check_constants()
    if options.quadrature:
        for length in (2, 8, 32, 128):
            check_interval(length)
        print("L    mu          spectral integral     Toeplitz mean        2pi*d/mu - log(1/mu)    d/floor")
        for length, mass in [(1,.25), (8,.03125), (32,1/1024), (16,1e-8)]:
            values = compare(length, mass)
            print(f"{length:2} {mass:10g}  " + "  ".join(f"{v:.12g}" for v in values))
