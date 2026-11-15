"""Bound each model's error using two nearby priors as proof devices."""
from fractions import Fraction
from mpmath import iv
from check_paired_exposure import cells, rates
from check_sequential_exposure import dec
from check_deadline_decision import clock_risk


def main():
    iv.dps = 60
    clocks = []
    for mass, g, l in rates():
        p, q = [cells(mass, Fraction(1, 10**8)*v) for v in (g, l)]
        z = [iv.ln(dec(a/c)) for a, c in zip(p, q)]
        mp = 2*sum(dec(w)*v for w, v in zip(p, z))
        mq = -2*sum(dec(w)*v for w, v in zip(q, z))
        clocks.append((mp, mq, max(abs(v).b for v in z)))
    mp, mq, b = max(clocks, key=lambda row: row[0].a)
    count = 4_000_000_000_000_000
    width = iv.mpf(4)
    tmin = count*min(mp.a, mq.a)
    tmax = count*max(mp.b, mq.b)
    delta = iv.mpf('0.000040')
    time = tmax+delta
    K = 2*b*b/(1-b)
    over = iv.exp(-delta**2/(4*K*tmax+2*K*delta))
    under = iv.exp(-delta**2/(4*K*tmax))
    upper = clock_risk(width, tmin-delta).b + under
    lower = clock_risk(width+b, time).a - over
    h = iv.mpf('0.004')
    cutoff = iv.ln((1+h)/(1-h))
    assert cutoff < width
    density = iv.exp(-time/8+cutoff/2)/iv.sqrt(2*iv.pi*time)
    # The pointwise loss improvement has maximum h at zero.
    gain = h*cutoff*density
    imbalance = (upper-lower+gain)/h
    lo, hi = lower-imbalance, upper+imbalance
    print('half difference below', float(imbalance.b))
    print('each error inside', float(lo.a), float(hi.b))
    assert lo > iv.mpf('0.0485860') and hi < iv.mpf('0.0492988')


if __name__ == '__main__':
    main()
