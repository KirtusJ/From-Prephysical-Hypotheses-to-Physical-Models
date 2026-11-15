"""Finite-cap contamination limits across the routed mass menu."""
from fractions import Fraction as Q
from mpmath import iv
from check_fixed_exposure import interval, moments, error_bounds, normal_tail
from check_paired_exposure import cells, rates

CAP = 4_000_000_000_000_000


def evaluate(fraction, radius=None):
    max_clock = iv.mpf(0)
    max_shift = Q(0)
    max_jump = iv.mpf('4.82e-7')
    achievable = iv.mpf(1)
    for s, g, l in rates():
        p,q = [cells(s, Q(1,10**8)*v) for v in (g,l)]
        gap = sum(abs(a-b) for a,b in zip(p,q))/2
        if gap == 0:
            continue
        f = min(fraction, radius/gap) if radius is not None else fraction
        max_shift = max(max_shift, f*gap)
        left = [(1-f)*a+f*b for a,b in zip(p,q)]
        right = [f*a+(1-f)*b for a,b in zip(p,q)]
        z = [iv.ln(interval(a/b)) for a,b in zip(left,right)]
        assert all(abs(v) < max_jump for v in z)
        conditional = []
        for table, sign in [(left,1),(right,-1)]:
            weights = list(map(interval,table))
            mean = sign*sum(w*v for w,v in zip(weights,z))
            max_clock = max(max_clock, (2*mean).b)
            conditional.append(error_bounds([moments(weights,z)],CAP)[0].b)
        achievable = min(achievable,max(conditional))
    mu = CAP*max_clock
    padding = iv.mpf('0.000020')
    K = 2*max_jump**2/(1-max_jump)
    overflow = iv.exp(-padding**2/(4*K*mu+2*K*padding))
    lower = normal_tail(iv.sqrt(mu+padding)/2)-overflow
    print('mix',float(fraction),'max TV',float(max_shift),
          'adaptive lower',float(lower.a),'fixed conditional upper',float(achievable.b))
    return lower.a, achievable.b, max_shift


def main():
    iv.dps = 70
    target = iv.mpf('0.05')
    lo, hi, _ = evaluate(Q(13,1000))
    assert lo > iv.mpf('0.05013928') and hi < iv.mpf('0.05013950')
    assert evaluate(Q(125996,10**7))[1] < target
    assert evaluate(Q(126003,10**7))[0] > target
    radius = Q(14534,10**14)
    lo, _, shift = evaluate(Q(13,1000),radius)
    assert shift == radius and lo > iv.mpf('0.05000011')


if __name__ == '__main__':
    main()
