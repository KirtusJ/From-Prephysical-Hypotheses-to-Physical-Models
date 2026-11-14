"""Robustness to error in the four-cell law at the single selected mass."""
from fractions import Fraction as Q
from mpmath import iv
from check_paired_exposure import cells, rates
from check_fixed_exposure import error_bounds, moments
from check_sequential_exposure import dec


def binary_kl(a,b):
    return a*iv.ln(a/b)+(1-a)*iv.ln((1-a)/(1-b))


def main():
    iv.dps = 85
    menu = []
    for mass,g,l in rates():
        p,q = [cells(mass, Q(1,10**8)*v) for v in (g,l)]
        score = sum(dec(a)*iv.ln(dec(a/b)) for a,b in zip(p,q))
        menu.append((score,p,q))
    _,p,q = max(menu, key=lambda row: row[0].a)
    half_gap = sum(abs(a-b) for a,b in zip(p,q))/4
    threshold = binary_kl(iv.mpf('0.04999529'),iv.mpf('0.05'))
    nmean = 2255410570000000
    for table in (p,q):
        small, second = sorted(map(dec,table), key=lambda cell:cell.a)[:2]
        limit = iv.sqrt(2*threshold/(nmean*(1/small+1/second)))
        delta = iv.mpf('5.2527e-14')
        # Inflate the quadratic bound on -log(1+x)+x at |x| <= delta/min(p).
        bound = nmean*(delta**2/2)*(1/small+1/second)/(1-delta/small)**2
        print('quadratic scale',float(limit.a),'KL ratio at chosen radius',float((bound/threshold).b))
        assert bound < threshold

    fraction = Q(13,1000)
    left = [(1-fraction)*a+fraction*b for a,b in zip(p,q)]
    right = [fraction*a+(1-fraction)*b for a,b in zip(p,q)]
    z = [iv.ln(dec(a/b)) for a,b in zip(left,right)]
    lower = []
    for table in (left,right):
        interval = error_bounds([moments(list(map(dec,table)), z)],4_000_000_000_000_000)[0]
        lower.append(interval.a)
    risk = sum(lower)/2
    print('shift TV',float(2*fraction*half_gap),'best cap risk lower',float(risk.a),
          'midpoint TV',float(half_gap))
    assert risk > iv.mpf('0.0501394')
    assert 2*fraction*half_gap < Q(15,10**11)
    assert Q(57671871,10**16) < half_gap < Q(57671872,10**16)


if __name__ == '__main__':
    main()
