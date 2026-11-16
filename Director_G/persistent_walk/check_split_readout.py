"""Check the two count rules when a five-site walk is read in two detector banks."""
from fractions import Fraction
from math import comb
from pathlib import Path
import json

Q = Fraction
HERE = Path(__file__).resolve().parent
UNIT = 10**12


def require(test, reason):
    if not test:
        raise ValueError(reason)


def outward(lower, upper):
    return [int(lower * UNIT // 1), int(-(-upper * UNIT // 1))]


def counts(n, p):
    a, d = p.as_integer_ratio()
    return [comb(n, k) * a**k * (d-a)**(n-k) for k in range(n+1)], d**n


def rejection(n, p, boundary, coin):
    row, den = counts(n, p)
    return (sum(row[boundary+1:]) + coin * row[boundary]) / den


def joint(n, eta, exclusive_min, time_boundary, time_coin, ideal_score, miss_score):
    # A detected photon supplies an exclusive-bank outcome and the usual signed trial.
    # A lost photon registers neither bank. Its signed score succeeds at negative settings.
    # Conditional on the number detected, fresh timings in the two groups are independent.
    detections, den = counts(n, eta)
    result = Q(0)
    for seen in range(exclusive_min, n+1):
        observed, a = counts(seen, ideal_score)
        lost, b = counts(n-seen, miss_score)
        above = at = 0
        for i, weight in enumerate(observed):
            first = max(0, time_boundary+1-i)
            above += weight * sum(lost[first:])
            k = time_boundary-i
            if 0 <= k < len(lost):
                at += weight * lost[k]
        result += Q(detections[seen], den) * (above + time_coin*at) / (a*b)
    return result


def main():
    program = json.loads((HERE / 'single_port_timing_output.json').read_text())[0]
    require(program['max_ticks'] == 3_999_996, 'wrong time law')
    pinned = Q(program['ideal_floor'])
    # The source rounds its ideal lower bound to 10^-12. Its fixed-point intensity
    # allowance is 780*1,999,998/2^128. Double that allowance fits inside another 10^-15.
    high = pinned + Q(1001, 10**15)
    minus = 1 - Q(program['always_click'])
    cap = Q('.528152948')
    # At derivative root (1+sqrt(7))/6 the exclusivity probability is (10+7sqrt(7))/54.
    require(54*cap > 10 and (54*cap-10)**2 > 343, 'invalid twofold-imbalance cap')
    require((54*(cap-Q(1,10**9))-10)**2 < 343, 'unexpected loose cap')
    require(Q(1,2)==2*Q(1,2)*(1-Q(1,2)), 'balanced classical equality witness')
    # Bright pulses into a common live-time lock, which suppresses one of two
    # reported bank clicks, can create a spurious exclusivity rate above the cap.
    require(1-Q(1,100)**2 > cap, 'shared live-time adverse control')

    results = []
    for n,b,k,tie,etas in [
        (57,37,38,Q(33,64),('.99962','.99963')),
        (61,40,40,Q(0),('.97665','.97666','.98'))]:
        null_time = rejection(n,Q(program['null_ceiling']),k,tie)
        null_banks = rejection(n,cap,b-1,Q(0))
        require(max(null_time,null_banks)<Q('.05'), 'one null size exceeds 5 percent')
        row=dict(launches=n,at_least_exclusive=b,timing_size=outward(null_time,null_time),
                 bank_size_ceiling=outward(null_banks,null_banks)[1],power={})
        for label in etas:
            eta=Q(label)
            low=joint(n,eta,b,k,tie,pinned,minus)
            hi=joint(n,eta,b,k,tie,high,minus)
            # Independently bracket the joint tail from the two marginal tests.
            marg_lo=rejection(n,minus+eta*(pinned-minus),k,tie)
            marg_hi=rejection(n,minus+eta*(high-minus),k,tie)
            bank=rejection(n,eta,b-1,Q(0))
            require(low>=marg_lo-(1-bank) and hi<=min(bank,marg_hi),'invalid joint tail')
            row['power'][label]=outward(low,hi)
        require(row['power'][etas[0]][1]<950_000_000_000<row['power'][etas[1]][0],
                'the efficiencies do not bracket the design target')
        results.append(row)
    print(json.dumps(dict(integer_scale=UNIT,designs=results),indent=2))


if __name__ == '__main__':
    main()
