"""Bayes risk enclosures for a capped single-mass likelihood test."""
from fractions import Fraction
from mpmath import iv
from check_paired_exposure import cells, rates
from check_sequential_exposure import dec


def clock_risk(width, time):
    # The sum is positive. Successive terms decrease at least geometrically.
    limit = 1 / (1 + iv.exp(width))
    total = limit
    for j in range(6):
        k = (2*j + 1)*iv.pi/(2*width)
        rate = k*k/2 + iv.mpf('0.125')
        term = iv.exp(-rate*time)/(4*width*rate)
        total += term
    ratio = iv.exp(-time*iv.pi**2/width**2)
    return iv.mpf([total.a, (total + term*ratio/(1-ratio)).b])


def main():
    iv.dps = 60
    rows = []
    for mass, global_rate, local_rate in rates():
        p, q = [cells(mass, Fraction(1, 10**8)*v) for v in (global_rate, local_rate)]
        z = [iv.ln(dec(a/b)) for a, b in zip(p, q)]
        mp = 2*sum(dec(w)*v for w, v in zip(p, z))
        mq = -2*sum(dec(w)*v for w, v in zip(q, z))
        rows.append((mp, mq, max(abs(v).b for v in z)))
    mp, mq, b = max(rows, key=lambda row: row[0].a)
    K = 2*b*b/(1-b)
    delta = iv.mpf('0.000040')
    original = iv.ln(19)+b
    for n, width, low, high in [
        (3800950000000000, original, '0.0676043','0.0676048'),
        (4000000000000000, iv.mpf(4), '0.0489421','0.0489427'),
    ]:
        tmin = n*min(mp.a, mq.a)
        tmax = n*max(mp.b, mq.b)
        over = iv.exp(-delta**2/(4*K*tmax+2*K*delta))
        under = iv.exp(-delta**2/(4*K*tmax))
        lo = clock_risk(width+b, tmax+delta).a-over
        hi = clock_risk(width, tmin-delta).b+under
        assert lo > iv.mpf(low) and hi < iv.mpf(high)
        print(n, float(lo.a), float(hi.b))
        if width == 4:
            error_floor = (1-iv.exp(-width))/(iv.exp(width+b)-iv.exp(-width))
            terminal_mean = width+b-(2*width+b)*error_floor
            mean_cap = 2*terminal_mean/min(mp.a, mq.a)
            print('mean pairs, each law below', float(mean_cap.b))
            assert mean_cap < 2708673000000000


if __name__ == '__main__':
    main()
