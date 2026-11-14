"""Exact checks for validating the source from serial, independent herald attempts.

Run python Director_G/check_stopped_heralds.py to print the reference JSON.
"""
import json
from fractions import Fraction as F
from itertools import product
from math import comb, prod


def require(ok, message):
    if not ok:
        raise ValueError(message)


def binomial_tail(trials, successes, p):
    return sum(comb(trials, j) * p**j * (1-p)**(trials-j)
               for j in range(successes, trials+1))


def hit_time(flags, target):
    count = 0
    for t, flag in enumerate(flags, 1):
        count += flag
        if count == target:
            return t
    return None


def certificate_example():
    alpha, tolerance, risk = F(1, 100), F(1, 10), F(1, 20)
    threshold = alpha / (alpha + (1-alpha)*tolerance)
    at_four = binomial_tail(4, 2, threshold)
    at_five = binomial_tail(5, 2, threshold)
    require(threshold == F(10, 109) and risk < threshold, "first herald cannot certify")
    require(at_four == F(6286600, 141158161) and at_four < risk < at_five,
            "second-herald terminal time boundary")
    # Tail strictly increases in p. These endpoints enclose L_2(4).
    lo, hi = F(976114, 10**7), F(976115, 10**7)
    require(binomial_tail(4, 2, lo) < risk < binomial_tail(4, 2, hi), "root enclosure")
    wrong_upper = alpha*(1-lo)/((1-alpha)*lo)
    return dict(false_pass_max=alpha, requested_wrong_fraction=tolerance, risk=risk,
                required_rate=threshold, best_first_herald_lower=risk,
                best_first_herald_wrong_upper=alpha*(1-risk)/((1-alpha)*risk),
                second_herald_test_at_four=at_four, second_herald_test_at_five=at_five,
                second_by_four_lower_enclosure=[lo, hi], wrong_upper_from_lower_end=wrong_upper)


def flag_checks():
    # Enumerate every flag string. For a fixed target, compare every rejection
    # probability at a finite deadline to its prespecified error budget.
    risk = F(1, 20)
    cases = 0
    for n in range(1, 9):
        for p in (F(0), F(1, 25), F(1, 3), F(1, 2), F(1)):
            words = [(w, p**sum(w)*(1-p)**(n-sum(w))) for w in product((0,1), repeat=n)]
            for k in range(1, n+1):
                by_time = [F(0)]*(n+1)
                for w, weight in words:
                    t = hit_time(w, k)
                    if t is not None:
                        by_time[t] += weight
                cdf, error = F(0), F(0)
                for t in range(k, n+1):
                    cdf += by_time[t]
                    require(cdf == binomial_tail(t, k, p), "stopping-time / count identity")
                    if cdf < risk:  # Exactly the event L_k(t) > p.
                        error += by_time[t]
                require(error <= risk, "fixed-target coverage with timeout at zero")
                cases += 1

    # Same flag law, but choose the target after seeing the first launch.
    p, n = F(1, 25), 9
    require(binomial_tail(n, 2, p) < risk < binomial_tail(n+1, 2, p),
            "last second-herald time that undercovers")
    failure = F(0)
    for flags in product((0,1), repeat=n):
        k = 1 if flags[0] else 2
        t = hit_time(flags, k)
        if t is not None and binomial_tail(t, k, p) < risk:
            failure += p**sum(flags)*(1-p)**(n-sum(flags))
    require(failure == p+(1-p)*binomial_tail(n-1, 2, p) == F(292287211993, 3814697265625)
            and failure > risk, "adaptive target counterexample")

    # Conditional reporting can lose coverage even with a fixed target.
    p = F(1, 25)
    completed = p  # target and deadline both one
    require(completed < risk, "undercoverage on every completed one-launch run")
    return dict(fixed_target_cases=cases, switched_target_failure=failure,
                switched_target_nominal_risk=risk, one_launch_completion_probability=completed,
                one_launch_conditional_failure=F(1))


def marks_check():
    # A fresh launch has one of three outcomes: miss, genuine herald, rival herald.
    weights = (F(1, 2), F(2, 5), F(1, 10))
    p = weights[1]+weights[2]
    totals, wrong = [F(0)]*6, [F(0)]*6
    for word in product(range(3), repeat=5):
        t = hit_time([kind != 0 for kind in word], 2)
        if t is not None:
            mass = prod(weights[kind] for kind in word)
            totals[t] += mass
            if word[t-1] == 2:
                wrong[t] += mass
    rows = []
    for t in range(2, 6):
        prefix = (t-1)*p*(1-p)**(t-2)  # exactly one flag among t-1 launches
        require((totals[t], wrong[t]) == (prefix*p, prefix*weights[2]), "marked stopping law")
        rows.append(dict(t=t, hit=totals[t], wrong_and_hit=wrong[t],
                         wrong_given_hit=wrong[t]/totals[t]))
    return rows


if __name__ == "__main__":
    result = dict(scope="Prospective calibration examples; no measured heralds",
                  purity=certificate_example(), coverage=flag_checks(), marked_launches=marks_check())
    print(json.dumps(result, indent=2, default=str))
