"""Directed fixed-sample checks for a random subset of gates with two live banks."""
from fractions import Fraction as F
from math import ceil, comb, factorial
from pathlib import Path
from runpy import run_path
import json

occupancy = run_path(str(Path(__file__).with_name("check_complementary_shutters.py")))
sqrt_interval = occupancy["sqrt_interval"]
power_interval = occupancy["power_interval"]
require = occupancy["require"]
H = F(49, 100) * F(51, 100)


def field_weights(eta, f):
    """Field bound for a hard veto or an effective fraction f*(1-r)."""
    weight = 1 / (1 - 2*f*H*eta)
    return weight, 1 + (weight-1)*eta/4


def mixed_affinity(eta, f):
    lo, hi = occupancy["affinity"](eta)
    root_lo, root_hi = sqrt_interval(1-eta)
    d_lo = (eta/(1+root_hi))**2
    d_hi = (eta/(1+root_lo))**2
    # Rationalize the deficit before subtracting it from the occupancy affinity.
    penalty_lo = d_lo/(1 + sqrt_interval(1-d_lo/eta)[1])
    penalty_hi = d_hi/(1 + sqrt_interval(1-d_hi/eta)[0])
    return lo - f*penalty_hi/2, hi - f*penalty_lo/2


def necessary_bound(eta, f):
    rho_lo, rho_hi = mixed_affinity(eta, f)
    target = F(19, 100)
    low, high = 0, 1
    while power_interval(rho_hi, 2*high)[1] > target:
        high *= 2
    while high-low > 1:
        mid = (low+high)//2
        if power_interval(rho_hi, 2*mid)[1] > target:
            low = mid
        else:
            high = mid
    require(power_interval(rho_lo, 2*(high-1))[0] > target, "lower endpoint")
    require(power_interval(rho_hi, 2*high)[1] <= target, "upper endpoint")
    return high


def check_design(eta, f, n):
    weight, field = field_weights(eta, f)
    k = ceil(3*n*eta/8)
    size_bound = power_interval(field, n)[1] / power_interval(weight, k)[0]
    require(size_bound <= F(1, 20), "field rejection exceeds budget")
    if n*eta < 192:
        # Exact lower binomial tail when the simple exponential bound is loose.
        p = eta/2
        num, den = p.as_integer_ratio()
        miss = F(
            sum(comb(n,j)*num**j*(den-num)**(n-j) for j in range(k)), den**n)
        require(miss <= F(1, 20), "single-excitation miss exceeds budget")
    else:
        # exp(-n*eta/64) <= exp(-3) < 1/20.
        require(sum(F(3**i, factorial(i)) for i in range(9)) > 20, "Chernoff constant")
    for t in (F(0), eta/2, eta, F(1)):
        relaxed = 1 + (weight-1)*t/2 - f*weight*H*t**2/2
        require(field-relaxed == f*weight*H*(t-eta)**2/2, "quadratic field maximum")
    return k


if __name__ == "__main__":
    cases = [
        (".05", ".01", 1918270), (".05", ".10", 192039), (".05", "1", 19430),
        (".10", ".01", 479623), (".10", ".10", 48067), (".10", "1", 4925),
        (".62", ".01", 12488), (".62", ".10", 1262), (".62", "1", 159),
    ]
    # The complete table of optical outcomes gives the same affinity as the
    # rationalized deficit. Choose a square rational arm-empty probability.
    for arm_empty in (F(1, 4), F(3, 4), F(99, 100)):
        eta = 1-arm_empty**2
        click = 1-arm_empty
        for f in (F(0), F(1, 10), F(1)):
            rho_lo, rho_hi = mixed_affinity(eta, f)
            single = [sqrt_interval(eta*click/2),
                      sqrt_interval((1-eta/2)*arm_empty)]
            only_one = sqrt_interval(eta*click*arm_empty/2)
            direct = [(single[0][j]+single[1][j]+1-f+
                       f*(1-eta+2*only_one[j]))/2 for j in (0, 1)]
            require(max(rho_lo, direct[0]) <= min(rho_hi, direct[1]), "outcome affinity")
    # A shared first-hit register can hide every double even for a bright field.
    # Its expected weight at full occupancy one exceeds the supposed field bound.
    weight, field = field_weights(F(1, 10), F(1, 10))
    require(1+(weight-1)/2 > field, "shared-dead-time adverse control")
    rows = []
    for efficiency, fraction, n in cases:
        eta, f = F(efficiency), F(fraction)
        k = check_design(eta, f, n)
        rows.append(dict(efficiency=efficiency, audited_fraction_of_full=fraction,
                         necessary_at_least=necessary_bound(eta, f), sufficient=n,
                         minimum_full_clicks=k, maximum_confirmed_doubles=0))
    eta, f, r, delta = F(".1"), F(".1"), F(".5"), F(".0002")
    n, k, allowed_doubles = 320000, 12000, 10
    weight, field = field_weights(eta, f*(1-r))
    for t in (F(0), eta, 2*eta, F(1)):
        relaxed = 1 + (weight-1)*t/2 - f*(1-r)*weight*H*t**2/2
        require(field-relaxed == f*(1-r)*weight*H*(t-eta)**2/2, "soft field maximum")
    size = power_interval(field, n)[1] / (power_interval(weight, k)[0]*r**allowed_doubles)
    require(size < F(".047236"), "bounded-double field certificate")
    double_tail = comb(n, allowed_doubles+1)*(f*delta/2)**(allowed_doubles+1)
    require(double_tail < F(".0090245"), "double-count factorial moment")
    require(k == 3*n*eta/8 and n*eta/64 >= 20, "full occupancy Chernoff bound")
    require(2**20 > 10**6 and double_tail + F(1, 10**6) < F(".01"),
            "sum of miss bounds")
    noisy = dict(efficiency_at_least=str(eta), audited_fraction_of_full=str(f),
                 full_double_probability_at_most=str(delta), preparations=n,
                 minimum_full_clicks=k, maximum_confirmed_doubles=allowed_doubles,
                 field_size_below=".047236", power_above=".99")
    print(json.dumps(dict(clean_designs=rows, bounded_double_design=noisy), indent=2))
