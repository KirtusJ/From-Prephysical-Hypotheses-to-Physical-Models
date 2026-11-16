"""Exact optical bank-swap controls and a finite calibration-and-counting design."""
from fractions import Fraction as F
from pathlib import Path
from runpy import run_path
import json

previous = run_path(str(Path(__file__).with_name("check_polarization_banks.py")))
require = previous["require"]
field_size = previous["field_size"]
upper_tail = previous["clean_power"]


def optical_controls():
    # Integer powers implement the two Poisson empty probabilities exactly for
    # each selected intensity, rational pure Stokes vector, axis and swap.
    for i in range(119):
        k = 1+i%4
        den = 1+k*k
        q = F(967+i%30, 1000)
        v = i%4
        empty = both = F(0)
        for comp in (2*k, 1-k*k, 0):
            for g in (-v, v):
                a = q**((4+g)*(den+comp))
                b = q**((4-g)*(den-comp))
                empty += a*b/6
                both += (1-a)*(1-b)/6
        y = 1-q**(4*den)
        require(1-empty <= 2*y-y*y, "hidden swap occupancy")
        require(both >= F(2,3)*(1-F(v,4)**2)*y*y, "bank-imbalance double floor")

    # An aligned input and no swap can feed the higher-gain bank. This
    # violates the mean-rate occupancy bound used for the randomized design.
    q = F(4,5)
    require(1-q**3 > 1-q**2, "missing swap adverse control")
    # One dead detector makes any initially unpolarized Poisson pulse and
    # unpolarized single excitation agree whenever their live click rates match.
    live_eta = F(4,5)
    pulse = (1-F(3,5), F(0))
    require(pulse == (live_eta/2, F(0)), "dead-bank labeled imitation")


def interval_probability(n, lo, hi, p):
    return upper_tail(n, lo, p)-upper_tail(n, hi+1, p)


def main():
    optical_controls()
    eta = F(1,10)
    m = F(2,3)
    rows = []
    for eps, n, k in ((F(1,4), 2289, 206), (F(1,2), 2794, 254), (F(4,5), 5468, 511)):
        size = field_size(n, k, 0, eta, m*(1-eps**2), F(0))
        power = upper_tail(n, k, eta)
        require(size < F(".05") and power > F(".95"), "known gain interval")
        rows.append(dict(max_relative_gain_difference=str(eps), preparations=n,
                         required_occupied=k, maximum_doubles=0))

    # The two bad-gain regions are alternatives. Each uses only its nearer
    # one-sided tail. Symmetry supplies the identical bound on the other side.
    ncal, lo, hi = 512, 219, 293
    b = F(5,8)
    q = 1-upper_tail(ncal, hi+1, b)
    require(lo == ncal-hi and q < F(".008133"), "bad calibration acceptance")
    require(upper_tail(ncal, lo, 1-b) == q, "opposite bad-gain tail")
    cal_bal = interval_probability(ncal, lo, hi, F(1,2))
    require(cal_bal > F(".99909"), "balanced calibration power")
    n, k = 2494, 223
    size = field_size(n, k, 0, eta, m*(1-F(1,4)**2), F(0))
    power = upper_tail(n, k, eta)
    require(size < F(".04") and power > F(".96535"), "science error budget")
    require(cal_bal*power > F(".9644"), "joint power")
    shorter = cal_bal*upper_tail(2289, 206, eta)
    require(F(".9493") < shorter < F(".9494"), "calibration loss in shorter design")
    # With access to the real imbalance region, the intersection rule also
    # has a disjoint-case size bound, sharper than the budget sum.
    require(max(q, size) < F(".04"), "intersection size")
    print(json.dumps(dict(known_imbalance=rows,
        reference=dict(detected_events=ncal, min_labels_A=lo, max_labels_A=hi,
                       bad_calibration_acceptance_below=".008133"),
        joint_design=dict(science_preparations=n, min_occupied=k, max_doubles=0,
                          field_rejection_below=".04",
                          balanced_clean_power_above=".9644")), indent=2))


if __name__ == "__main__":
    main()
