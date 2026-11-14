"""Finite-pair survival bounds for the single-mass sequential likelihood rule."""
from fractions import Fraction
from mpmath import iv
from check_paired_exposure import cells, rates
from check_sequential_exposure import dec


def survival(width, time):
    """Integrate the tilted Dirichlet kernel over (-width, width)."""
    factor = (iv.exp(width / 2) + iv.exp(-width / 2)) / width
    total = 0
    for j in range(5):
        k = (2*j + 1) * iv.pi / (2 * width)
        term = factor * k / (k*k + iv.mpf('0.25')) * iv.exp(-time * (k*k/2 + iv.mpf('0.125')))
        total += (-1)**j * term
    # The alternating terms decrease since k > 1/2 throughout.
    return iv.mpf([total.a-term.b, total.b])


def main():
    iv.dps = 60
    rows = []
    for s, g, l in rates():
        p, q = [cells(s, Fraction(1, 10**8)*v) for v in (g, l)]
        z = [iv.ln(dec(a/b)) for a, b in zip(p, q)]
        means = [2*sum(dec(w)*v for w, v in zip(p, z)),
                 -2*sum(dec(w)*v for w, v in zip(q, z))]
        rows.append((means, max(abs(v).b for v in z), s))
    means, b, s = max(rows, key=lambda row: row[0][0].a)
    assert iv.pi / (2*(iv.ln(19)+2*b)) > iv.mpf('0.5')
    width = iv.ln(19) + b
    K = 2*b*b/(1-b)
    delta = iv.mpf('0.000040')
    for n, low, high in [(3800950000000000,'0.0861824','0.0861844'),
                         (4516320000000000,'0.05','0.050002'),
                         (4516360000000000,'0.049998','0.05'),
                         (5000000000000000,'0.0346020','0.0346029'),
                         (7000000000000000,'0.0075517','0.0075520')]:
        for mean in means:
            t = n * mean
            overflow = iv.exp(-delta**2/(4*K*t+2*K*delta))
            underflow = iv.exp(-delta**2/(4*K*t))
            lo = survival(width, t+delta).a - overflow
            hi = survival(width+b, t-delta).b + underflow
            print(n, float(lo.a), float(hi.b))
            assert lo > iv.mpf(low) and hi < iv.mpf(high)


if __name__ == '__main__':
    main()
