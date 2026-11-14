"""Outward bounds on the mean number of pairs at the four-quadrillion deadline."""
from fractions import Fraction
from mpmath import iv
from check_paired_exposure import cells, rates
from check_sequential_exposure import dec


def expected_clock(width, time):
    # Subtract the integrated survival beyond the deadline from the full exit mean.
    exp_width = iv.exp(width)
    full = 2*width*(exp_width-1)/(exp_width+1)
    factor = (iv.exp(width/2)+iv.exp(-width/2))/width
    residual = 0
    for j in range(6):
        k = (2*j+1)*iv.pi/(2*width)
        rate = k*k/2 + iv.mpf('0.125')
        term = factor*k*iv.exp(-rate*time)/((k*k+iv.mpf('0.25'))*rate)
        residual += (-1)**j * term
    # From the second mode onward all factors decrease with k.
    assert 3*iv.pi/(2*width) > iv.mpf('0.5')
    return full - iv.mpf([residual.a, (residual+term).b])


def main():
    iv.dps = 60
    rows = []
    for mass, g, l in rates():
        p, q = [cells(mass, Fraction(1, 10**8)*v) for v in (g, l)]
        z = [iv.ln(dec(a/c)) for a, c in zip(p, q)]
        mp = 2*sum(dec(w)*v for w, v in zip(p, z))
        mq = -2*sum(dec(w)*v for w, v in zip(q, z))
        rows.append((mp, mq, max(abs(v).b for v in z)))
    mp, mq, b = max(rows, key=lambda row: row[0].a)
    K = 2*b*b/(1-b)
    for mean in (mp, mq):
        time = 4_000_000_000_000_000 * mean
        deviation = iv.sqrt(2*K*time)/2
        width = iv.mpf(4)
        lo = (expected_clock(width, time).a-deviation)/mean
        hi = (expected_clock(width+b, time).b+deviation)/mean
        assert lo > 2390881440000000 and hi < 2390882700000000
        print(float(lo.a), float(hi.b))


if __name__ == '__main__':
    main()
