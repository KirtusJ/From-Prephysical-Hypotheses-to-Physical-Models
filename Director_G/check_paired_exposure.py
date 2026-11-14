"""Full binary-pair likelihoods for the two published equal-budget witnesses."""
from decimal import Decimal, localcontext, ROUND_CEILING
from fractions import Fraction as Q
from pathlib import Path
import json

from check_multigap_bias import optimum
from check_sqrt_witness import tent


def rates():
    menu = json.loads((Path(__file__).parent / "results/echo_probability_map.json").read_text())["finite_menu"]
    den = int(menu["mass_denominator"])
    x = sorted({Q(int(v["numerator"]), den) for v in menu["routed_left_half_masks"]} | {Q(1,2)})
    widths = [b-a for a,b in zip(x,x[1:])]
    cutoff = optimum(widths)[0]
    weights = [a+b for a,b in zip(widths,widths[1:])]
    nodes = x[1:-1]
    global_power = [tent(z)**2 for z in nodes]
    local_power = [Q(0) for z in nodes]
    for a,b in zip(x,x[1:]):
        h = b-a
        if h <= cutoff:
            continue
        center = (a+b)/2
        radius = min(4*h,center,Q(1,2)-center)
        probability = 2*(1-cutoff/h)
        for j,z in enumerate(nodes):
            local_power[j] += probability*max(0,radius-abs(z-center))**2
    def normalize(values):
        cost = sum(w*v for w,v in zip(weights,values))
        return [v/cost for v in values]
    return list(zip(nodes,normalize(global_power),normalize(local_power)))


def cells(s,v):
    cross = s*(1-s)-v
    table = [(1-s)**2+v,cross,cross,s*s+v]
    assert sum(table)==1 and min(table)>=0 and table[1]+table[3]==s
    return table


def evaluate(precision):
    with localcontext() as ctx:
        ctx.prec = precision
        def dec(q):
            return Decimal(q.numerator)/Decimal(q.denominator)
        budget = Q(1,10**8)
        ranked = []
        for s,g,l in rates():
            p,q = cells(s,budget*g),cells(s,budget*l)
            # Stable evaluation of 1 - sum sqrt(pq).
            loss = sum((dec(a-b)/(dec(a).sqrt()+dec(b).sqrt()))**2 for a,b in zip(p,q))/2
            direct = 1-sum(dec(a*b).sqrt() for a,b in zip(p,q))
            assert abs(loss-direct)<Decimal(10)**(2-precision)
            ranked.append((loss,s,g,l))
        ranked.sort(reverse=True)
        loss,s,g,l = ranked[0]
        exponent = -(1-loss).ln()
        ceil = lambda x: int(x.to_integral_value(rounding=ROUND_CEILING))
        necessary = ceil(-Decimal('0.19').ln()/(2*exponent))
        sufficient = ceil(Decimal(10).ln()/exponent)
        print(f"s={float(s):.12f}, g/M={float(g):.9f}, l/M={float(l):.9f}, 1-affinity={loss:.12E}")
        print(f"runner-up s={float(ranked[1][1]):.12f}, loss={ranked[1][0]:.12E}; necessary={necessary}, sufficient={sufficient}")
        return s,necessary,sufficient


if __name__ == '__main__':
    assert evaluate(60)==evaluate(90)
