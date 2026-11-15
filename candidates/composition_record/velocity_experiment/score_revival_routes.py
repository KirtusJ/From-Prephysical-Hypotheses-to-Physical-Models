"""Fixed-horizon test for a privately randomized data/revival experiment.

At each release cut draw DATA with probability 7/19 and AUDIT with 12/19,
independently of the cut state and of earlier draws. Count every launch in
the assigned arm. An invalid or missing result pays zero. Hard quotas or
choosing the stopping time from outcomes require a different analysis.

Examples from this directory:
  python -I -B score_revival_routes.py --data 375 309 --audit 644 644
  python -I -B score_revival_routes.py --check

Each pair is ATTEMPTS PAID_SUCCESSES. The null p-value uses all launches,
without conditioning on the realized arm totals. The comparison with alpha
uses exact rational arithmetic. The reported decimal is rounded.
Use --data-error and --audit-error for prespecified uniform upper bounds on
the upward error in the corresponding conditional success effects.
"""

import argparse
from decimal import Decimal, localcontext
from fractions import Fraction
from math import comb, floor


NULL_RATE = Fraction(35, 38)
SEVEN_WRITE = Fraction(226560354573, 274877906944)
IDEAL_RATE = (7*SEVEN_WRITE + 12)/19


def calibrated_rate(data_error, audit_error):
    if data_error < 0 or audit_error < 0:
        raise ValueError("upward effect error bounds must be nonnegative")
    return min(Fraction(1), NULL_RATE + (7*data_error + 12*audit_error)*Fraction(1, 19))


def binomial_upper(n, k, rate=NULL_RATE):
    """Exact P[Bin(n, rate) >= k], summing whichever tail has fewer terms."""
    if n < 0 or not 0 <= rate <= 1:
        raise ValueError("invalid binomial parameters")
    if k <= 0:
        return Fraction(1)
    if k > n or rate == 0:
        return Fraction(0)
    if rate == 1:
        return Fraction(1)
    a = rate.numerator
    b = rate.denominator - a
    denominator = rate.denominator**n

    if n-k+1 <= k:
        # Start at n successes. Neighboring integer weights have ratios
        # (n-j)b/((j+1)a), where j counts failures so far.
        term = a**n
        total = term
        for j in range(n-k):
            term = term * (n-j)*b // ((j+1)*a)
            total += term
        return Fraction(total, denominator)

    # The complement needs only success counts 0 through k-1.
    term = b**n
    total = term
    for j in range(k-1):
        term = term * (n-j)*a // ((j+1)*b)
        total += term
    return Fraction(denominator-total, denominator)


def decimal_text(value):
    with localcontext() as ctx:
        ctx.prec = 10
        return format(Decimal(value.numerator)/Decimal(value.denominator), ".9g")


def score(data, audit, alpha, data_error=0, audit_error=0):
    for name, (attempts, paid) in (("data", data), ("audit", audit)):
        if not 0 <= paid <= attempts:
            raise ValueError(f"{name} must satisfy 0 <= paid successes <= attempts")
    n = data[0] + audit[0]
    k = data[1] + audit[1]
    if not n:
        raise ValueError("the test requires at least one assigned launch")
    if not 0 < alpha < 1:
        raise ValueError("alpha must lie strictly between 0 and 1")
    rate = calibrated_rate(data_error, audit_error)
    p_value = binomial_upper(n, k, rate)
    print(f"Data paid {data[1]}/{data[0]}, audit paid {audit[1]}/{audit[0]}")
    print(f"All launches paid {k}/{n}")
    if data_error or audit_error:
        print(f"Calibrated null success cap {rate}")
    print(f"One-sided binomial null tail {decimal_text(p_value)}")
    print(f"At alpha {decimal_text(alpha)}: "
          + ("reject the measure-and-prepare null" if p_value <= alpha
             else "insufficient evidence to reject the measure-and-prepare null"))


def check(condition, message):
    if not condition:
        raise AssertionError(message)


def self_check():
    # Direct integer polynomial independently exercises both recursion branches.
    for n in range(19):
        for k in range(n+2):
            direct = sum(comb(n, j)*35**j*3**(n-j) for j in range(k, n+1))
            check(binomial_upper(n, k) == Fraction(direct, 38**n), "small binomial tail")
    check(binomial_upper(4, 1, Fraction(0)) == 0, "rate zero")
    check(binomial_upper(4, 4, Fraction(1)) == 1, "rate one")
    check(calibrated_rate(0, 0) == NULL_RATE, "zero calibration errors")
    amended = calibrated_rate(Fraction(1, 100), Fraction(1, 50))
    check(amended == Fraction(1781, 1900) and binomial_upper(3, 3, amended) == amended**3,
          "upward data and audit errors")
    saturated = calibrated_rate(0, Fraction(1, 8))
    check(saturated == calibrated_rate(1, 1) == 1 and binomial_upper(37, 37, saturated) == 1,
          "calibration cap reaches and stays at one")
    check(binomial_upper(7, 0) == 1 and binomial_upper(7, 7) == NULL_RATE**7,
          "all failures and all successes")
    check(binomial_upper(36, 36) > Fraction(1, 20) >= binomial_upper(37, 37),
          "perfect-record 5 percent threshold")

    # Expected-rate example, rounding down as stated.
    n, k = 1019, 953
    check(floor(n*IDEAL_RATE) == k, "seven-write expected successes")
    null = binomial_upper(n, k)
    check(Fraction(49504, 10**6) < null < Fraction(49505, 10**6), "1019 upper tail")
    check(binomial_upper(n, k-1) > Fraction(1, 20), "1019 critical count")
    print(f"1019 launches, 953 successes: null tail {decimal_text(null)}")

    # Independent seven-write ideal on every launch for the power calculation.
    n, k = 3596, 3339
    null = binomial_upper(n, k)
    power = binomial_upper(n, k, IDEAL_RATE)
    check(Fraction(49724, 10**6) < null < Fraction(49725, 10**6), "3596 upper tail")
    check(Fraction(950712, 10**6) < power < Fraction(950713, 10**6), "3596 ideal power")
    check(binomial_upper(n, k-1) > Fraction(1, 20), "3596 critical count")
    print(f"3596 launches, 3339 successes: null tail {decimal_text(null)}, "
          f"ideal probability of rejection {decimal_text(power)}")


def main():
    parser = argparse.ArgumentParser(description="Fixed-horizon, all-launch revival route test.")
    for arm in ("data", "audit"):
        parser.add_argument("--"+arm, type=int, nargs=2, metavar=("ATTEMPTS", "PAID_SUCCESSES"))
        parser.add_argument("--"+arm+"-error", default="0", metavar="BOUND",
                            help=f"preassigned upper bound on upward {arm} effect error, default 0")
    parser.add_argument("--alpha", default="0.05",
                        help="preassigned one-sided significance, default 0.05")
    parser.add_argument("--check", action="store_true", help="verify endpoint and planning examples")
    args = parser.parse_args()
    if args.check:
        if args.data is not None or args.audit is not None:
            parser.error("--check runs by itself")
        self_check()
        return
    if args.data is None or args.audit is None:
        parser.error("supply both --data ATTEMPTS PAID_SUCCESSES and --audit ATTEMPTS PAID_SUCCESSES")
    try:
        score(args.data, args.audit, Fraction(args.alpha),
              Fraction(args.data_error), Fraction(args.audit_error))
    except (ValueError, ZeroDivisionError) as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
