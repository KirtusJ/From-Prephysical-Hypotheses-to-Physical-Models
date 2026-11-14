"""Exact small-budget coefficient for a specified family of gap-local perturbations."""
import json
from fractions import Fraction as Q
from math import sqrt
from pathlib import Path
from check_multigap_bias import optimum


def main():
    menu = json.loads((Path(__file__).parent / "results/echo_probability_map.json").read_text())["finite_menu"]
    den = int(menu["mass_denominator"])
    x = sorted({Q(int(v["numerator"]), den) for v in menu["routed_left_half_masks"]} | {Q(1,2)})
    h = [b-a for a,b in zip(x,x[1:])]
    weights = [h[j-1]+h[j] for j in range(1,len(h))]
    t, base, _ = optimum(h)
    terms = []
    for a,b in zip(x,x[1:]):
        width = b-a
        if width <= t:
            continue
        center = (a+b)/2
        radius = min(4*width, center, Q(1,2)-center)
        def tent(z):
            return max(0,radius-abs(z-center))
        p = 2*(1-t/width)
        # At either winning crossing, |Z-center| = D-width/2.
        mean_d = (t+width)/2
        assert radius >= width/2
        gain = radius+width/2-2*mean_d
        # Independent edge-strip integral (the tent is affine on each strip).
        mean_f = (tent(a)+tent(b-t)+tent(a+t)+tent(b))/4
        assert gain == mean_f-mean_d and gain > 0
        H = sum(w*tent(z)**2 for w,z in zip(weights,x[1:-1]))
        terms.append((p,gain,H,[tent(z) for z in x]))
    gain = sum(p*g for p,g,H,f in terms)
    cost = sum(p*H for p,g,H,f in terms)
    M = Q(1,10**8)
    assert M < cost and sum(p for p,*_ in terms)==1
    C2 = gain**2/cost
    rates = [sum(p*f[j]**2 for p,g,H,f in terms)/cost for j in range(len(x))]
    assert sum(w*r for w,r in zip(weights,rates[1:-1]))==1
    j = max(range(len(x)), key=rates.__getitem__)
    assert Q(1956,1000)**2 < C2 < Q(1957,1000)**2
    print(f"coefficient={sqrt(C2):.12f}, budget limit={float(cost):.12g}")
    print(f"at M=1e-8: bias={float(base)+sqrt(M*C2):.12f}")
    print(f"peak node={float(x[j]):.12f}, score/M={float(rates[j]):.12f}, nonzero lower nodes={sum(r>0 for r in rates)}")
    zero = next(k for k in range(1,len(x)-1) if rates[k]==0)
    print(f"zero score at interior mass {float(x[zero]):.12f}")


if __name__ == "__main__":
    main()
