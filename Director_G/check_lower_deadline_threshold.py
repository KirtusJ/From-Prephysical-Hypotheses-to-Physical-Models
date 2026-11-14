"""Certify a lower threshold and exclude a range of faster thresholds."""
from fractions import Fraction
from mpmath import iv
from check_paired_exposure import cells, rates
from check_sequential_exposure import dec
from check_deadline_decision import clock_risk
from check_capped_mean import expected_clock


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
    width = iv.mpf('3.867')
    tmin = count*min(mp.a, mq.a)
    tmax = count*max(mp.b, mq.b)
    delta = iv.mpf('0.000020')
    time = tmax+delta
    K = 2*b*b/(1-b)
    over = iv.exp(-delta**2/(4*K*tmax+2*K*delta))
    under = iv.exp(-delta**2/(4*K*tmax))
    upper = clock_risk(width, tmin-delta).b + under
    lower = clock_risk(width+b, time).a - over
    h = iv.mpf('0.003')
    cutoff = iv.ln((1+h)/(1-h))
    assert cutoff < width
    density = iv.exp(-time/8+cutoff/2)/iv.sqrt(2*iv.pi*time)
    # Bound the slope over the shifted decision interval and integrate a triangle.
    gain = (1+h)*iv.exp(cutoff)*cutoff**2*density/4
    imbalance = (upper-lower+gain)/h
    lo, hi = lower-imbalance, upper+imbalance
    print('half difference below', float(imbalance.b))
    print('each error inside', float(lo.a), float(hi.b))
    assert lo > iv.mpf('0.0496484') and hi < iv.mpf('0.0499902')
    failed = clock_risk(iv.mpf('3.842')+b, time).a - over
    assert failed > iv.mpf('0.0500070')
    for mean in (mp, mq):
        horizon = count*mean
        deviation = iv.sqrt(2*K*horizon)/2
        low = (expected_clock(width, horizon).a-deviation)/mean
        high = (expected_clock(width+b, horizon).b+deviation)/mean
        print('mean pairs', float(low.a), float(high.b))
        assert low > 2320413930000000 and high < 2320415200000000
        floor = (expected_clock(iv.mpf('3.842'), horizon).a-deviation)/mean
        print('feasible mean floor', float(floor.a))
        assert floor > 2306918910000000


if __name__ == '__main__':
    main()
