"""Check the polarization-axis optical designs with outward rational bounds."""
from fractions import Fraction as F
from pathlib import Path
from runpy import run_path
import json

shared = run_path(str(Path(__file__).with_name("check_complementary_shutters.py")))
power_interval = shared["power_interval"]
sqrt_interval = shared["sqrt_interval"]
require = shared["require"]


def clean_power(n, k, eta):
    """Exact upper binomial tail as one minus an integer lower tail."""
    a, b = eta.as_integer_ratio()
    atom = (b-a)**n
    lower = atom
    for j in range(1, k):
        atom, rem = divmod(atom*(n-j+1)*a, j*(b-a))
        require(rem == 0, "binomial atom")
        lower += atom
    return 1-F(lower, b**n)


def necessary(n_min, eta, m):
    lo, hi = sqrt_interval((1-eta)*(1-m*eta))
    y_lo, y_hi = eta/(1+hi), eta/(1+lo)
    survive_lo, survive_hi = 1-m*y_hi**2, 1-m*y_lo**2
    require(19*power_interval(survive_lo, n_min-1)[0] > 1, "necessary bound")
    require(19*power_interval(survive_hi, n_min)[1] <= 1, "necessary endpoint")


def field_size(n, k, j, eta, m, r):
    beta = m*(1-r)
    y0 = eta/2
    w = (1-y0)/(1-(1+beta)*y0)
    A = 1+(w-1)*y0
    # With y=1-sqrt(1-t) the relaxed expected weight is quadratic.
    for y in (F(0), y0, F(1)):
        value = 1+(w-1)*(2*y-y*y)-beta*w*y*y
        require(A-value == (w-1+beta*w)*(y-y0)**2, "quadratic maximum")
    return power_interval(A, n)[1]/(power_interval(w, k)[0]*r**j)


def check_stokes_outputs():
    # For q=exp[-lambda/(2*den)], both bank empty probabilities are
    # integer powers of q. Vectors are generated on the unit circle.
    for k in range(1, 6):
        den = 1+k*k
        parts = [2*k, 1-k*k, 0]
        require(sum(x*x for x in parts) == den*den, "unit Stokes vector")
        for L in (2, 3):
            m = 1-F(1, L)
            for q in (F(1, 4), F(9, 10), F(99, 100)):
                rates = [(1-q**(den+x))*(1-q**(den-x)) for x in parts[:L]]
                floor = m*(1-q**den)**2
                require(sum(rates)/L >= floor, "pure polarization bound")
                if k == 1:
                    require(sum(rates)/L == floor, "axis-aligned equality")
    # The conditional model can match full bank labels after discarding doubles.
    for L in (2, 3):
        m = 1-F(1, L)
        y = F(1, 20)
        empty = (1-y)**2
        # For each measured axis, mix all 2L oriented input eigenaxes.
        left = ((1-empty)/2+(L-1)*y*(1-y))/L
        both = m*y*y
        eta = (1-empty-both)/(1-both)
        require((empty, left, left) == tuple((1-both)*x for x in (1-eta, eta/2, eta/2)),
                "full labeled subdistribution")
    # If the source receives the basis in advance, it may aim into one bank.
    eta = F(1, 10)
    empty = 1-eta
    table = [F(0)]*4
    for u, v in ((empty, F(1)), (F(1), empty)):
        for j, mass in enumerate((u*v, (1-u)*v, u*(1-v), (1-u)*(1-v))):
            table[j] += mass/2
    require(table == [1-eta, eta/2, eta/2, 0], "setting-aware imitation")
    # The average Stokes vector of random signed eigenaxes vanishes, yet this
    # mixture has fewer doubles than inserting that mean into the Poisson law.
    y = F(1, 2)
    aligned_mixture = (0+y*y+y*y)/3
    require(aligned_mixture < y*y, "averaging-order control")


def main():
    check_stokes_outputs()
    cases = [(2, ".05", 9070, 10836, 505), (3, ".05", 6774, 8299, 383),
             (2, ".10", 2180, 2794, 254), (3, ".10", 1621, 2164, 194),
             (2, ".62", 34, 65, 34), (3, ".62", 24, 53, 27)]
    rows = []
    for L, text, lower, n, k in cases:
        eta = F(text)
        m = 1-F(1, L)
        necessary(lower, eta, m)
        size = field_size(n, k, 0, eta, m, F(0))
        power = clean_power(n, k, eta)
        require(size < F(1, 20) and power > F(19, 20), "clean test")
        rows.append(dict(axes=L, efficiency=text, necessary=lower, sufficient=n,
                         minimum_occupied=k, maximum_doubles=0))
    n, k, j = 9000, 819, 5
    size = field_size(n, k, j, F(".1"), F(2, 3), F(1, 2))
    miss = 1-clean_power(n, k, F(".1")) + clean_power(n, j+1, F(".0002"))
    require(size < F(".05") and miss < F(".0123"), "source with occasional doubles")
    # Triad with pairwise absolute dot products <= 0.05, by the Gram row-sum bound.
    m_cal = 1-(1+2*F(".05"))/3
    require(m_cal == F(19, 30), "calibrated geometry")
    alignment_size = field_size(2400, 216, 0, F(".1"), m_cal, F(0))
    alignment_power = clean_power(2400, 216, F(".1"))
    require(alignment_size < F(".05") and alignment_power > F(".95"), "calibrated triad")
    print(json.dumps(dict(clean_designs=rows,
        bounded_doubles=dict(axes=3, efficiency_at_least=".10", double_probability_at_most=".0002",
            preparations=n, minimum_occupied=k, maximum_doubles=j, power_above=".9877"),
        calibrated_triad=dict(maximum_absolute_dot_product=".05", efficiency=".10",
            preparations=2400, minimum_occupied=216, maximum_doubles=0)), indent=2))


if __name__ == "__main__":
    main()
