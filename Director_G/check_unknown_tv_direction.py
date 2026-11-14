"""Uniform conditional TV robustness and a menu-wide finite-cap converse."""
from fractions import Fraction as Q
from mpmath import iv
from check_fixed_exposure import interval, moments, error_bounds, normal_tail
from check_paired_exposure import cells, rates
from check_adaptive_contamination import CAP


def shifted_tables(p, q, radius):
    # Move P mass from its highest to lowest score and reverse the move for Q.
    # Nominal ties have interchangeable cells only when their shifted ratios
    # are kept equal. Share each transfer proportionally within a tied group.
    ratios = [a/b for a,b in zip(p,q)]
    low = [i for i,r in enumerate(ratios) if r == min(ratios)]
    high = [i for i,r in enumerate(ratios) if r == max(ratios)]
    left, right = list(p), list(q)
    for group, direction in [(low,1),(high,-1)]:
        total = sum(q[i] for i in group)
        for i in group:
            move = direction*radius*q[i]/total
            left[i] += move
            right[i] -= move
    if min(left+right)>0:
        shifted = [a/b for a,b in zip(left,right)]
        if all(shifted[i]==min(shifted) for i in low) and all(shifted[i]==max(shifted) for i in high):
            return left,right,True
    # An admissible overlapping or cross-mixture witness suffices for the converse.
    gap = sum(abs(a-b) for a,b in zip(p,q))/2
    f = min(Q(1,2),radius/gap)
    return [(1-f)*a+f*b for a,b in zip(p,q)], [f*a+(1-f)*b for a,b in zip(p,q)], False


def evaluate(radius):
    largest_clock = iv.mpf(0)
    jump = iv.mpf('4.82e-7')
    best = (iv.mpf(1), None)
    for s,g,l in rates():
        p,q = [cells(s,Q(1,10**8)*v) for v in (g,l)]
        if p==q:
            continue
        left,right,ordered = shifted_tables(p,q,radius)
        for nominal, shifted in [(p,left),(q,right)]:
            assert sum(shifted)==1 and min(shifted)>0
            assert sum(abs(a-b) for a,b in zip(nominal,shifted))<=2*radius
        if left==right:
            continue
        z = [iv.ln(interval(a/b)) for a,b in zip(left,right)]
        assert all(abs(v)<jump for v in z)
        upper = []
        for table,sign in [(left,1),(right,-1)]:
            w = list(map(interval,table))
            mean = sign*sum(a*v for a,v in zip(w,z))
            assert mean>0
            largest_clock = max(largest_clock,(2*mean).b)
            if ordered:
                upper.append(error_bounds([moments(w,z)],CAP)[0].b)
        if ordered and max(upper)<best[0]:
            best = max(upper),s
    mu = CAP*largest_clock
    d = iv.mpf('0.000020')
    K = 2*jump**2/(1-jump)
    overflow = iv.exp(-d*d/(4*K*mu+2*K*d))
    lower = normal_tail(iv.sqrt(mu+d)/2)-overflow
    print(float(radius),float(best[1]),float(best[0].b),float(lower.a))
    return best[0].b,lower.a


def main():
    iv.dps = 70
    target = iv.mpf('0.05')
    assert evaluate(Q(829577,10**16))[0] < target
    assert evaluate(Q(829617,10**16))[1] > target


if __name__ == '__main__':
    main()
