"""Enumerate the address routings at a common pooled mass and read their feedback table."""
import json
from argparse import ArgumentParser
from fractions import Fraction as Q
from itertools import product
from pathlib import Path

from check_coin_uniform_masks import require, summed, transfer


def response(mass, u, a, b):
    if a < mass < b:
        return b if u < (mass-a)/(b-a) else a
    if 1-b < mass < 1-a:
        return 1-response(1-mass, u, a, b)
    return mass


def recover_weights(table, h, tail):
    f00, f10 = table[0, 0]/h**2, table[1, 0]/h**2
    f01, f11 = table[0, 1]/h**2, table[1, 1]/h**2
    return (2*f00, (f01-f00)/tail, (f10-f00)/tail, (f11-f01-f10+f00)/tail)


def survey_memory(routes, curves, quadrature, c, h):
    zero = next(i for i,r in enumerate(routes) if r[3] == 0)
    active = max(range(len(routes)), key=lambda i: routes[i][3])
    tail = routes[active][3]
    pooled = [response(c,u,c-h/2,c+h/2) for u,_ in quadrature]
    labels = (zero, active)
    receipts = []
    cases = [(Q(0),)*4, (Q(1,12), Q(1,4), Q(1,6), Q(1,3))]
    cases.extend(tuple(Q(i == mode) for i in range(4)) for mode in range(4))
    for weights in cases:
        table = {}
        for j, k in product(range(2), repeat=2):
            base = c*c + (1-c)*(1-c)
            own = (1-sum(weights))*base
            for (p_mode,s_mode), weight in zip(product(range(2),repeat=2),weights):
                x = curves[labels[j]] if p_mode else pooled
                y = curves[labels[k]] if s_mode else pooled
                own += weight*sum(w*(px*sy+(1-px)*(1-sy))
                                  for px,sy,(_,w) in zip(x,y,quadrature))
            table[j,k] = own-base
        got = recover_weights(table,h,tail)
        require(got == tuple(weights), "retention and both read modes")
        receipts.append({"weights_00_01_10_11":list(map(str,got)),
                         "gain_00_01_10_11":[str(table[key]) for key in sorted(table)]})
    return receipts


def dark_read(a_flag, b_flag, route_copy, flag_copy):
    # One site, two address arms, unwrite flag using the original XOR.
    # Environment labels persist. Sum amplitudes by the labels before squaring.
    amplitudes = {}
    for address, flag in enumerate((a_flag,b_flag)):
        label = (address if route_copy else 0, flag if flag_copy else 0)
        amplitudes[label] = amplitudes.get(label,0) + (1 if address == 0 else -1)
    return Q(sum(v*v for v in amplitudes.values()),4)


def run():
    menu = json.loads((Path(__file__).parent / "results/echo_probability_map.json").read_bytes())["finite_menu"]
    den = int(menu["mass_denominator"])
    masks = {Q(int(v["numerator"]), den): set(v["radii"]) for v in menu["routed_left_half_masks"]}
    nodes = sorted(set(masks) | {Q(1, 2)})
    a, b = max(zip(nodes, nodes[1:]), key=lambda pair: pair[1]-pair[0])
    c, h = (a+b)/2, b-a
    fixed = masks[a] & masks[b]
    changing = sorted(masks[a] ^ masks[b])
    effects = transfer(menu["ticks"])

    def mass(radii):
        rr, rl, ll = summed(effects, [x for x in effects if abs(x) in radii])
        require(rr == ll and rl == 0, "each whole-shell event must be scalar on both input rails")
        return Q(rr, den)

    total_disagreement = mass(changing)
    cells = [mass(fixed), total_disagreement, 1-mass(fixed)-total_disagreement]
    require(all(value > 0 for value in cells), "both flag outcomes and mismatch control")
    routes, cuts = [], {Q(0), Q(1,2), Q(1)}
    for bits in product((0, 1), repeat=len(changing)):
        m0, m1 = (mass(fixed | {r for r, bit in zip(changing, bits) if bit == value})
                  for value in (1, 0))
        require((m0+m1)/2 == c and max(m0,m1) < Q(1, 2), "common pooled mass and domain")
        t = max(Q(0), Q(1, 2)-abs(m0-c)/h)
        for m in (m0, m1):
            if a < m < b:
                cuts.add((m-a)/h)
        routes.append(("".join(map(str,bits)), m0, m1, t))
    cuts = sorted(cuts)
    quadrature = [((x+y)/2, y-x) for x,y in zip(cuts,cuts[1:])]
    curves = []
    for _,m0,m1,_ in routes:
        curve = [(response(m0,u,a,b)+response(m1,u,a,b))/2 for u,_ in quadrature]
        require(sum(val*w for val,(_,w) in zip(curve,quadrature)) == c, "fixed-setting mean")
        curves.append(curve)

    table = []
    for j, pilot in enumerate(curves):
        row = []
        for k, science in enumerate(curves):
            # Unconditional own-bit and independent-bit science hit probabilities.
            own = sum(w*(x*y+(1-x)*(1-y)) for x,y,(_,w) in zip(pilot,science,quadrature))
            reassigned = c*c+(1-c)*(1-c)
            delta = own-reassigned
            require(delta == h*h*min(routes[j][3],routes[k][3]), "all split-address contrasts")
            row.append(delta)
        table.append(row)
    diag = [row[i] for i,row in enumerate(table)]
    strengths = sorted(set(diag)-{Q(0)})
    require(len(routes)==32 and len(strengths)==4 and diag.count(0)==24, "survey controls")
    # det[min(d_i,d_j)] for the distinct positive diagonal strengths is the product of successive increments.
    increments = [y-x for x,y in zip([Q(0)]+strengths, strengths)]
    require(all(x>0 for x in increments), "four independent positive contrasts")
    original = "".join("1" if r in masks[a] else "0" for r in changing)
    require(dict(zip([r[0] for r in routes],diag))[original] == 0, "endpoint address split")
    receipts = survey_memory(routes,curves,quadrature,c,h)
    dark = {"unread": Q(0), "flag_dephased": total_disagreement/2, "address_dephased": Q(1, 2)}
    for word, _, _, _ in routes:
        first = fixed | {r for r,b in zip(changing,word) if b == "1"}
        second = fixed | {r for r,b in zip(changing,word) if b == "0"}
        for which, (route_copy,flag_copy) in {"unread":(False,False),"flag_dephased":(False,True),
                                             "address_dephased":(True,False)}.items():
            gram = [Q(0)]*3
            for x,values in effects.items():
                p = dark_read(abs(x) in first,abs(x) in second,route_copy,flag_copy)
                gram = [entry+p*value/den for entry,value in zip(gram,values)]
            require(gram == [dark[which],0,dark[which]], word+" dark port")
    return {"tick":menu["ticks"],"endpoints":[str(a),str(b)],"c":str(c),"changing_radii":changing,
            "original_bits":original,"pooled_model_gain":str(h*h/2),"retention_controls":receipts,
            "all_dark_probabilities":
            {k:str(v) for k,v in dark.items()}, "quadrature_intervals":len(quadrature),
            "routes":[{"bits":r[0],"mass_0":str(r[1]),"mass_1":str(r[2]),"tail":str(r[3]),
                       "diagonal_gain":str(val)} for r,val in zip(routes,diag)],
            "cross_table_by_route_index":[[str(v) for v in row] for row in table]}


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    result = run()
    with args.output.open("x",encoding="utf-8",newline="\n") as target:
        json.dump(result,target,indent=2)
        target.write("\n")
