"""Exact coefficients for the finite paired-moment envelope on the tick-256 mesh."""
from fractions import Fraction as Q
import json
from math import sqrt
from pathlib import Path
from check_multigap_bias import optimum


def main():
    menu = json.loads((Path(__file__).parent / "results/echo_probability_map.json").read_text())["finite_menu"]
    den = int(menu["mass_denominator"])
    x = sorted({Q(int(v["numerator"]), den) for v in menu["routed_left_half_masks"]} | {Q(1, 2)})
    h = [b-a for a,b in zip(x,x[1:])]
    t, base, _ = optimum(h)
    W = [h[i-1]+h[i] for i in range(1,len(h))]
    q = [max(Q(0), 1-t/gap) for gap in h]
    coeff = [(a+b)/2 for a,b in zip(q,q[1:])]
    A = 1/min(W)
    C = sum(c*c/w for c,w in zip(coeff,W))
    cases = []
    for i in range(1,len(h)):
        relaxed = optimum(h[:i-1]+[h[i-1]+h[i]]+h[i+1:])[1]
        cost = W[i-1]*h[i-1]*h[i]
        cases.append(((relaxed-base)/cost, i, relaxed, cost))
    slope, i, relaxed, cost = max(cases)
    assert i == 23 and 643 < slope < 644 and sum(q) == Q(1,2)
    assert base + slope*cost == relaxed
    # The one-cell pair score equals variance of an endpoint-valued response.
    a,u,b = x[i-1:i+2]
    p = (u-a)/(b-a)
    assert (1-p)*(a-u)**2+p*(b-u)**2 == h[i-1]*h[i]
    M = Q(1,10**8)
    assert 0 < M < cost
    print(f"node={float(u):.12f}, full cost={float(cost):.12g}, slope={float(slope):.12f}")
    print(f"sqrt coefficient={sqrt(A)+sqrt(C):.12f}")
    print(f"at M={float(M):g}: attainable bias (rounded) {float(base+slope*M):.12f}, "
          f"upper bound (rounded) {float(base)+(sqrt(A)+sqrt(C))*sqrt(M):.12f}")


if __name__ == "__main__":
    main()
