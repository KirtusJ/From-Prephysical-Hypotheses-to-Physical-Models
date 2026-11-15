"""Robust radius for conditional joint laws with both binary margins fixed."""
from fractions import Fraction as Q
from mpmath import iv
from check_unknown_tv_direction import evaluate


def inward_endpoints(p, q, radius):
    direction = (1,-1,-1,1)
    assert all(a-b == sign*(p[0]-q[0]) for a,b,sign in zip(p,q,direction))
    step = min(radius/2, abs(p[0]-q[0])/2)
    signed_step = step if p[0]>q[0] else -step
    left = [a-signed_step*v for a,v in zip(p,direction)]
    right = [b+signed_step*v for b,v in zip(q,direction)]
    if left==right:
        return left,right,False

    # Verify the derivative of each lower-score CDF in the direction
    # from the Q-side endpoint to the P-side endpoint.
    ratios = [a/b for a,b in zip(left,right)]
    orientation = 1 if p[0]>q[0] else -1
    for cutoff in set(ratios):
        slope = sum(v for v,r in zip(direction,ratios) if r<=cutoff)
        assert orientation*slope <= 0
    return left,right,True


def main():
    iv.dps = 70
    target = iv.mpf('0.05')
    assert evaluate(Q(14532909,10**17),inward_endpoints)[0] < target
    assert evaluate(Q(14533604,10**17),inward_endpoints)[1] > target


if __name__ == '__main__':
    main()
