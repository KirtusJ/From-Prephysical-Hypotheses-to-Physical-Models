"""Uniform Brownian-clock risk bound for adaptive mass selection at M=10^-8."""
from fractions import Fraction as Q
from mpmath import iv
from check_fixed_exposure import interval, normal_tail
from check_paired_exposure import cells, rates


def main():
    iv.dps = 60
    budget = Q(1, 10**8)
    # Conservative bounds on leaf displacement and one-step mean clock.
    b = iv.mpf('0.000000482')
    mean_cap = iv.mpf('0')
    for s,g,l in rates():
        p,q = cells(s,budget*g), cells(s,budget*l)
        z = [iv.ln(interval(a/c)) for a,c in zip(p,q)]
        assert all(abs(v)<b for v in z)
        for table, sign in [(p,1),(q,-1)]:
            kl = sign*sum(interval(a)*v for a,v in zip(table,z))
            mean_cap = max(mean_cap,(2*kl).b)
    # A 4-leaf balanced tree takes at most two exits.
    K = 2*b*b/(1-b)
    N = 3_800_930_000_000_000
    mu = N*mean_cap
    delta = iv.mpf('0.000020')
    horizon = mu+delta
    overflow = iv.exp(-delta**2/(4*K*mu+2*K*delta))
    risk = normal_tail(iv.sqrt(horizon)/2)-overflow
    print('clock mean cap',float(mean_cap),'horizon',float(horizon.b),'overflow upper',float(overflow.b),'risk lower',float(risk.a))
    assert risk > iv.mpf('0.05')


if __name__=='__main__':
    main()
