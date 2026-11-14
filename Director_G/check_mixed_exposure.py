"""Uniform finite-sample certificate over nonadaptive schedules at M=10^-8."""
from fractions import Fraction as Q
from mpmath import iv
from check_fixed_exposure import interval, normal_tail
from check_paired_exposure import cells, rates


def main():
    iv.dps = 60
    budget = Q(1,10**8)
    count = 3_800_938_000_000_000
    variance_floor = iv.mpf(6)
    # If either total variance is small, both transcript laws have high affinity.
    affinity_error = (1-iv.sqrt(1-iv.exp(-2*variance_floor*iv.mpf('0.126'))))/2
    assert affinity_error > iv.mpf('0.05')
    for null in (0,1):
        drift_max, third_max = 0,0
        for s,g,l in rates():
            p,q = cells(s,budget*g), cells(s,budget*l)
            if p==q:
                continue
            table = list(map(interval,(p,q)[null]))
            logs = [iv.ln(interval(a/b)) for a,b in zip(p,q)]
            mean = sum(prob*z for prob,z in zip(table,logs))
            variance = sum(prob*(z-mean)**2 for prob,z in zip(table,logs))
            third = sum(prob*abs(z-mean)**3 for prob,z in zip(table,logs))
            rho = sum(iv.sqrt(interval(a*b)) for a,b in zip(p,q))
            assert -iv.ln(rho)/variance < iv.mpf('0.126')
            drift_max = max(drift_max,(abs(mean)/iv.sqrt(variance)).b)
            third_max = max(third_max,(third/variance).b)
        gaussian = normal_tail(iv.sqrt(count)*drift_max)
        penalty = iv.mpf('0.56')*third_max/iv.sqrt(variance_floor)
        lower = gaussian-penalty
        print(null,'Gaussian tail',float(gaussian.a),'penalty',float(penalty.b),'lower',float(lower.a))
        assert lower > iv.mpf('0.05')


if __name__=='__main__':
    main()
