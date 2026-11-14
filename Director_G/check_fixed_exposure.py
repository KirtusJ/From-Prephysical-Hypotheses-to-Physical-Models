"""Interval Berry--Esseen bounds for repeated single-node pair likelihoods."""
from fractions import Fraction as Q
from mpmath import iv
from check_paired_exposure import cells, rates


def interval(q):
    return iv.mpf(q.numerator)/q.denominator


def moments(table, log_ratio):
    mean = sum(p*z for p,z in zip(table,log_ratio))
    sd = iv.sqrt(sum(p*(z-mean)**2 for p,z in zip(table,log_ratio)))
    third = sum(p*abs(z-mean)**3 for p,z in zip(table,log_ratio))
    return abs(mean)/sd, third/sd**3


def normal_tail(x):
    # Integrate exp(-t^2/2) termwise. Consecutive partial sums enclose the integral.
    assert 0 <= x and x < 2
    term = x
    total = term
    for k in range(1,24):
        term = -term*x*x*(2*k-1)/(2*k*(2*k+1))
        total += term
    following = -term*x*x*47/(48*49)
    enclosed = total + iv.mpf([0,1])*following
    return iv.mpf('0.5')-enclosed/iv.sqrt(2*iv.pi)


def error_bounds(law,n):
    root = iv.sqrt(n)
    return [normal_tail(root*drift)+iv.mpf([-1,1])*iv.mpf('0.475')*skew/root
            for drift,skew in law]


def main():
    iv.dps = 50
    budget = Q(1,10**8)
    laws = []
    for s,g,l in rates():
        p,q = cells(s,budget*g),cells(s,budget*l)
        if p==q:
            continue
        z = [iv.ln(interval(a/b)) for a,b in zip(p,q)]
        laws.append((s,[moments(list(map(interval,tab)),z) for tab in [p,q]]))
    # The endpoints and anchored midpoint have identical laws and error 1/2.
    lo,hi = 3_800_940_000_000_000,3_800_950_000_000_000
    target = iv.mpf('0.05')
    for s,law in laws:
        e=error_bounds(law,lo)
        assert sum(e)/2 > target,(float(s),e)
    winners=[]
    for s,law in laws:
        e=error_bounds(law,hi)
        if all(v < target for v in e):
            winners.append(s)
            print('passing node',float(s),'conditional error enclosures',*[str(v) for v in e])
        else:
            assert sum(e)/2 > target, (float(s),e)
    assert len(winners)==1
    s = winners[0]
    law=dict(laws)[s]
    print('lower endpoint conditional errors',*[str(v) for v in error_bounds(law,lo)])


if __name__=='__main__':
    main()
