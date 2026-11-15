"""Audit repeated 12-tick HHHIIHIHHIIH site writes on the 16-site ring.

Usage: python -I -B analyze_scalar_records.py counts.json --h 0.5 --alpha 0.05

Input uses chronological ABSOLUTE 3-bit left-step codes as integers 0..7 or
null for an unreadable code. Initial absolute code is zero. This schema example
contains invented software-test input, not hardware observations:

  {"schema":"scalar-walk-abs3-v1","provenance":"synthetic","writes":3,
   "attempts":5,"records":[{"codes":[6,4,2],"count":2},
                            {"codes":[null,1,0],"count":1}]}

Unlisted attempts have no readable codes. A missing intermediate code makes
its incoming and outgoing displacements unknown; later adjacent readable codes
are used again. Format provenance: ideal, synthetic, simulator or hardware.
The reader does not correct an incorrectly assigned but present code.

Let theta=log(5)/log(29). Score = 128 times the usual three-level AM-GM
score: 32(1-theta) at either weight-2 site, -16/5 at each weight-10 site,
128 theta/58 at the weight-58 site, and 0 at the weight-26 site. Its ordinary
mean is zero and it is nonnegative in expectation for each power q. For this
state-independent block the ordinary displacement law repeats independently
of the recorded past. A whole-word escort at fixed q factors into the same
per-write escort. Sequential powers may be redrawn before each outcome.
The one-sided bounds permit arbitrary within-launch correlations across clocks
and arbitrary missingness. They assume independent incident launches, correct
matched readout, and intact localized inputs to the 12-tick block. Ideal
histograms are descriptive only. Decimal strings preserve rounded endpoints.
"""
import argparse
import json
from decimal import Context, Decimal as D, DecimalException, ROUND_CEILING, ROUND_FLOOR
from pathlib import Path
from runpy import run_path


HELPERS = run_path(str(Path(__file__).with_name("analyze_counts.py")))
integer = HELPERS["integer"]
DOWN = Context(prec=60, rounding=ROUND_FLOOR)
UP = Context(prec=60, rounding=ROUND_CEILING)
NEAR = Context(prec=60)
ZERO, ONE = D(0), D(1)
WEIGHTS = (58, 10, 2, 10, 26, 10, 2, 10)  # Indexed by (physical displacement // 2).


def ln_enclosure(x):
    value = NEAR.ln(D(x))
    return NEAR.next_minus(value), NEAR.next_plus(value)


def lower_exp(x):
    return max(ZERO, NEAR.next_minus(NEAR.exp(x)))


def outside_gap(h):
    """Uniform positive lower bound for all real |q-1|>=h and both infinities.

    For q>=1+h, divide the score numerator by 58^(q-1). With t=q-1 it
    becomes F_+(t)=theta+(1-theta)29^(-t)-(5/29)^t. For q<=1-h
    divide by 2^(q-1) and set t=1-q: F_-(t)=1-theta+theta*29^(-t)-5^(-t).
    Both increase: their derivatives are respectively log(29/5) times
    ((5/29)^t-29^(-t)) and log(5) times (5^(-t)-29^(-t)).
    Z_q=sum w^q. For q>=1, Z_q<=128*58^(q-1); for q<=1,
    Z_q<=128*2^(q-1). The score scale 128 cancels these constants.
    Thus min(F_+(h),F_-(h)) suffices (including q=0 and negative q).
    To avoid small-gap cancellation, integrate the derivative on [h/2,h]:
    log(B)*(B^-h)*(1-(B/29)^(h/2))*h/2, B=29/5 or 5.
    Below we take the better of this and a direct outward-rounded F bound.
    """
    log5_lo, log5_hi = ln_enclosure(5)
    log29_lo, log29_hi = ln_enclosure(29)
    theta_lo = DOWN.divide(log5_lo, log29_hi)
    theta_hi = UP.divide(log5_hi, log29_lo)
    half_h = DOWN.divide(h, D(2))
    common = lower_exp(DOWN.multiply(h.copy_negate(), log29_hi))
    bounds = []
    for b_lo, b_hi, baseline, factor in (
        (DOWN.subtract(log29_lo, log5_hi), UP.subtract(log29_hi, log5_lo),
         theta_lo, DOWN.subtract(ONE, theta_hi)),
        (log5_lo, log5_hi, DOWN.subtract(ONE, theta_hi), theta_lo),
    ):
        decay_hi = NEAR.next_plus(NEAR.exp(UP.multiply(h.copy_negate(), b_lo)))
        direct = DOWN.subtract(DOWN.add(baseline, DOWN.multiply(factor, common)), decay_hi)
        # 1-exp(-x) >= x/(1+x) for x>=0; this avoids subtracting two near-ones.
        x = DOWN.multiply(half_h, DOWN.subtract(log29_lo, b_hi))
        exp_difference = DOWN.divide(x, UP.add(ONE, x))
        integral = DOWN.multiply(DOWN.multiply(half_h, b_lo), exp_difference)
        integral = DOWN.multiply(integral, lower_exp(DOWN.multiply(h.copy_negate(), b_hi)))
        bounds.append(max(direct, integral))
    gap = min(bounds)
    if gap <= 0:
        raise ValueError("h is too extreme for a positive separation at this numerical precision")
    return gap, theta_lo, theta_hi


def decode(data):
    if not isinstance(data, dict) or data.get("schema") != "scalar-walk-abs3-v1":
        raise ValueError("expected schema scalar-walk-abs3-v1")
    if data.get("provenance") not in ("ideal", "synthetic", "simulator", "hardware"):
        raise ValueError("declare ideal, synthetic, simulator or hardware provenance")
    writes, attempts = integer(data["writes"]), integer(data["attempts"])
    if not writes or not attempts or not isinstance(data["records"], list):
        raise ValueError("positive writes and attempts and a records array are required")
    bins = [[0]*8 for _ in range(writes)]
    recorded = 0
    for record in data["records"]:
        if not isinstance(record, dict):
            raise ValueError("each records entry must be an object containing codes and count")
        count = integer(record["count"])
        codes = record["codes"]
        if not isinstance(codes, list) or len(codes) != writes:
            raise ValueError("each codes array must contain exactly one entry per write")
        recorded += count
        if recorded > attempts:
            raise ValueError("record multiplicities exceed attempted launches")
        previous = 0
        for bucket, code in zip(bins, codes):
            if code is not None and (type(code) is not int or not 0 <= code < 8):
                raise ValueError("position codes must be null or integers 0..7")
            if code is not None and previous is not None:
                displacement = (12 - 2*((code-previous) % 8)) % 16
                bucket[displacement//2] += count
            previous = code
    return attempts, recorded, bins


def analyze(data, h, alpha):
    if not h.is_finite() or h <= 0 or not alpha.is_finite() or not ZERO < alpha < ONE:
        raise ValueError("require a finite h>0 and 0<alpha<1")
    attempts, recorded, bins = decode(data)
    gap, theta_lo, theta_hi = outside_gap(h)
    low = (DOWN.multiply(D(32), DOWN.subtract(ONE, theta_hi)),
           UP.multiply(D(32), UP.subtract(ONE, theta_lo)))
    high = (DOWN.divide(DOWN.multiply(D(128), theta_lo), D(58)),
            UP.divide(UP.multiply(D(128), theta_hi), D(58)))
    coeffs = {2: low, 10: (D("-3.2"), D("-3.2")), 26: (ZERO, ZERO), 58: high}
    smallest = min(lo for lo, _ in coeffs.values())
    largest = max(hi for _, hi in coeffs.values())
    n = D(attempts)
    sampled = data["provenance"] != "ideal"
    if sampled:
        log_upper = ln_enclosure(UP.divide(D(len(bins)), alpha))[1]
        radicand = UP.divide(log_upper, D(2*attempts))
        radius = UP.multiply(UP.subtract(largest, smallest), NEAR.next_plus(NEAR.sqrt(radicand)))
    rows = []
    for clock, counts in enumerate(bins, start=1):
        missing = attempts-sum(counts)
        lo = DOWN.multiply(D(missing), smallest)
        hi = UP.multiply(D(missing), largest)
        for count, weight in zip(counts, WEIGHTS):
            lower, upper = coeffs[weight]
            lo = DOWN.add(lo, DOWN.multiply(D(count), lower))
            hi = UP.add(hi, UP.multiply(D(count), upper))
        lo, hi = DOWN.divide(lo, n), UP.divide(hi, n)
        row = {"tick": 12*clock, "counts_dx_0_to_14_step_2": counts,
               "known": attempts-missing, "unknown": missing,
               "possible_incident_sample_mean": [str(lo), str(hi)]}
        if sampled:
            upper = min(largest, UP.add(hi, radius))
            row["familywise_one_sided_mean_upper"] = str(upper)
            if upper < 0:
                row["model_status"] = "Upper limit below the model minimum of zero."
            else:
                row["bad_incident_fraction_upper"] = str(min(ONE, UP.divide(upper, gap)))
        rows.append(row)
    return {"schema": data["schema"], "provenance": data["provenance"], "attempts": attempts,
            "listed_attempts": recorded, "unlisted_attempts": attempts-recorded,
            "h": str(h), "bad_event": "|q-1| >= h, including either infinite power",
            "separation_lower_bound": str(gap),
            "score_range_enclosure": [str(smallest), str(largest)],
            "family_error_probability_if_sampled": str(alpha) if sampled else None,
            "one_sided_radius_if_sampled": str(radius) if sampled else None, "writes": rows}


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    cli.add_argument("counts", type=Path)
    cli.add_argument("--h", type=D, required=True, help="positive distance from exponent one")
    cli.add_argument("--alpha", type=D, default=D("0.05"), help="family error probability")
    args = cli.parse_args()
    try:
        data = json.loads(args.counts.read_bytes(), object_pairs_hook=HELPERS["object_with_unique_keys"])
        print(json.dumps(analyze(data, args.h, args.alpha), indent=2))
    except (KeyError, TypeError, ValueError, OSError, DecimalException) as exc:
        cli.exit(2, f"{cli.prog}: {exc}\n")
