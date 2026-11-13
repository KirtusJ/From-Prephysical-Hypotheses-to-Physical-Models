"""Uninterrupted ring ports and repeated destructive reads, with exact signed counts."""

import argparse
import json
from collections import Counter
from fractions import Fraction
from itertools import product
from math import cos, pi
from pathlib import Path


DIR = (1, -1)
PORTS = [(x,c) for x in range(8) for c in DIR]


def tick(state, gains, m):
    out = Counter()
    for (x,c,y), value in state.items():
        shifted = (y+gains[x]) % m
        for d in DIR:
            out[(x+d) % len(gains),d,shifted] += -value if c==d==-1 else value
    return {key:v for key,v in out.items() if v}


def word_table(x0, c0, t, gains, m):
    """Separate direct listing of every direction word at a fixed horizon."""
    cells = Counter()
    for word in product(DIR,repeat=t):
        x = x0
        exponent = 0
        for d in word:
            exponent += gains[x]
            x = (x+d) % len(gains)
        coins = (c0,)+word
        negative = sum(a==b==-1 for a,b in zip(coins,coins[1:]))
        cells[x,coins[-1],exponent % m] += (-1)**negative
    return {key:v for key,v in cells.items() if v}


def autocorrelation(poly):
    return [sum(v*poly[(i-d)%len(poly)] for i,v in enumerate(poly)) for d in range(len(poly))]


def sector_difference(poly):
    measured = autocorrelation(poly)
    difference = measured.copy()
    for j,v in enumerate(measured):
        difference[(4*j)%15] -= v
    # Ascending coefficients of Phi_15. The port weights agree exactly iff
    # the remainder of their numerator difference is zero.
    cyclotomic = [1,-1,0,1,-1,1,0,-1,1]
    for leading in range(14,7,-1):
        value = difference[leading]
        for i,c in enumerate(cyclotomic):
            difference[leading-8+i] -= value*c
    return difference[:8]


def tomography(coefficients):
    def profile(fixed_start):
        pivots = {}
        ranks = []
        selected = []
        for t,layer in enumerate(coefficients):
            for start,end,coeff in layer:
                if fixed_start and start!=(0,1):
                    continue
                row = list(map(Fraction,coeff))
                for pivot in sorted(pivots):
                    if row[pivot]:
                        row = [a-row[pivot]*b for a,b in zip(row,pivots[pivot])]
                pivot = next((j for j,v in enumerate(row) if v),None)
                if pivot is not None:
                    pivots[pivot] = [v/row[pivot] for v in row]
                    selected.append(dict(start=start,end=end,tick=t,coefficients=coeff))
            ranks.append(len(pivots))
        return ranks,selected
    ranks_all,_ = profile(False)
    ranks_fixed,basis = profile(True)
    assert ranks_all==[1,1,1,3,3,6,8] and ranks_fixed==[1,1,1,2,2,5,8]
    # Independently invert the selected matrix by exact Gauss-Jordan elimination,
    # keeping columns in the original measurement order.
    size = len(basis)
    matrix = [list(map(Fraction,r["coefficients"])) for r in basis]
    augmented = [row+[Fraction(j==i) for j in range(size)] for i,row in enumerate(matrix)]
    for i in range(size):
        k = next(j for j in range(i,size) if augmented[j][i])
        augmented[i],augmented[k] = augmented[k],augmented[i]
        augmented[i] = [v/augmented[i][i] for v in augmented[i]]
        for j in range(size):
            if i!=j:
                augmented[j] = [a-augmented[j][i]*b for a,b in zip(augmented[j],augmented[i])]
    inverse = [row[size:] for row in augmented]
    assert all(sum(inverse[i][k]*matrix[k][j] for k in range(size))==int(i==j)
               for i in range(size) for j in range(size))
    return dict(cumulative_ranks_all_starts=ranks_all,cumulative_ranks_from_0R=ranks_fixed,
                single_start_basis=basis,inverse_coefficients=[[str(v) for v in row] for row in inverse],
                reconstruction="Multiply the eight measured probabilities by 2^tick in the listed basis order, "
                               "then multiply this vector by inverse_coefficients to get C(0)..C(7). For folded "
                               "character masses w0,w1,...,w7, C(u)=sum_k wk*cos(2*pi*k*u/15). Thus "
                               "w0=(C(0)+2*sum_{u=1}^7 C(u))/15; for k=1..7, "
                               "wk=2*(C(0)+2*sum_{u=1}^7 C(u)*cos(2*pi*k*u/15))/15. "
                               "Each setting uses its own preparation of the same sheet; no intermediate read.")


def fifteen_sheet_scan():
    gains = [0,3,0,8,0,5,0,0]
    polynomials = []
    identifiers = {}
    rows = []
    distinct = [0]*7
    coefficients = [[] for _ in distinct]
    witness = None
    for x0,c0 in PORTS:
        state = {(x0,c0,0):1}
        by_time = []
        for t in range(7):
            assert state==word_table(x0,c0,t,gains,15)
            assert sum(v*v for v in state.values())==2**t
            by_port = []
            weight_total = [0]*15
            for x,c in PORTS:
                poly = tuple(state.get((x,c,y),0) for y in range(15))
                if poly not in identifiers:
                    identifiers[poly] = len(polynomials)
                    polynomials.append([[y,n] for y,n in enumerate(poly) if n])
                by_port.append(identifiers[poly])
                remainder = sector_difference(poly)
                distinct[t] += bool(any(remainder))
                weights = autocorrelation(poly)
                folded = [weights[0]]+[weights[j]+weights[-j] for j in range(1,8)]
                coefficients[t].append(((x0,c0),(x,c),folded))
                weight_total = [a+b for a,b in zip(weight_total,weights)]
                if (x0,c0,x,c,t)==(0,1,1,-1,5):
                    ps = [sum(v*cos(2*pi*k*y/15) for y,v in enumerate(weights))/2**t for k in (1,4)]
                    witness = dict(initial=[x0,c0],port=[x,c],tick=t,signed_polynomial=polynomials[by_port[-1]],
                                   autocorrelation=[[j,n] for j,n in enumerate(weights) if n],
                                   phi15_remainder_before_normalization=remainder,probabilities_approx=ps,
                                   exact_difference="(cos(4*pi/15)-cos(14*pi/15))/16 > 0")
            assert weight_total==[2**t]+[0]*14
            by_time.append(by_port)
            if t<6:
                state = tick(state,gains,15)
        rows.append(by_time)
    assert distinct[:6]==[0,0,0,0,0,64]
    assert witness["signed_polynomial"]==[[3,1],[6,2],[11,-1]]
    assert witness["phi15_remainder_before_normalization"]==[2,-2,1,1,-2,2,0,-3]
    return dict(N=8,M=15,departure_gains=gains,characters=[1,4],ports=PORTS,polynomials=polynomials,
                polynomial_ids=rows,unequal_port_pairs_by_tick=distinct,witness=witness,
                tomography=tomography(coefficients),
                encoding="polynomial_ids[start_index][tick][end_index] indexes polynomials. Start and end "
                         "use ports in the displayed order. Each sparse [exponent,coefficient] list is P(z); "
                         "an empty list is the zero port. The unresolved-sheet, character-k probability is "
                         "|P(exp(2*pi*i*k/15))|^2/2^tick. All 1,792 port cells, including empty ones, are encoded.")


def resolved_ports(state, ticks):
    gains = [1]+[0]*7
    for _ in range(ticks):
        state = tick(state,gains,5)
    return [(x,c,[state.get((x,c,y),0) for y in range(5)]) for x,c in PORTS]


def sheet_norm(vector):
    return sum(v*v for v in vector)


def five_sheet_tree(vector, first_route):
    """Stop on a non-dark read. All routing directions and all terminal reads count."""
    norm = sheet_norm(vector)
    branches = []
    terminals = []
    one = Fraction(0)
    two = Fraction(0)
    route_totals = Counter()

    def read_node(x,c,vec,time,record,actions,dark_count):
        nonlocal one,two
        before = Fraction(sheet_norm(vec),norm*2**time)
        if not actions:
            terminals.append(dict(record=record,mass=str(before)))
            return
        route = actions[0]=="route"
        span = 1 if route else 3
        state = {(x,c,y):v for y,v in enumerate(vec) if v}
        children = []
        subtotal = Fraction(0)
        for u,d,result in resolved_ports(state,span):
            if not any(result):
                continue
            prob = Fraction(sheet_norm(result),norm*2**(time+span))
            subtotal += prob
            dark = (u,d)==((x-c)%8,-c) and not route
            key = record+[[u,d]]
            children.append(dict(port=[u,d],sheet=result,joint_mass=str(prob),dark=dark))
            if dark:
                assert u==0
                if dark_count==0:
                    one += prob
                else:
                    two += prob
            if route:
                route_totals[d] += prob
                assert prob==before/2
            if not route and not dark:
                terminals.append(dict(record=key,mass=str(prob)))
            else:
                read_node(u,d,result,time+span,key,actions[1:],dark_count+int(dark))
        assert subtotal==before
        branches.append(dict(prior_record=record,time=time+span,read="one-step route" if route else "three-tick port",
                             incoming_mass=str(before),outcomes=children))

    # The neighbor-start variant exposes first and second destructive reads at
    # times 3 and 7. The bump-start variant first records a fair one-tick route.
    # Both read both directions after the second return as well.
    schedule = ["probe","route","probe","route"]
    if first_route:
        schedule.insert(0,"route")
    read_node(0 if first_route else 1,1,vector,0,[],schedule,0)
    total = sum((Fraction(t["mass"]) for t in terminals),Fraction())
    assert total==1 and route_totals[1]==route_totals[-1]
    return dict(start=[0 if first_route else 1,1],schedule=schedule,initial_sheet_numerators=vector,
                initial_squared_norm=norm,p_one_dark=str(one),p_two_dark=str(two),
                second_dark_given_first=str(two/one),independent_fresh_sheet_joint=str(one**2),
                leaf_mass=str(total),terminal_records=terminals,branches=branches)


def difference_oracle(vector):
    # Translation and overall sign depend on the route and drop out of the norm.
    first = [v-vector[(j-1)%5] for j,v in enumerate(vector)]
    second = [v-first[(j-1)%5] for j,v in enumerate(first)]
    return [Fraction(sheet_norm(first),8*sheet_norm(vector)),Fraction(sheet_norm(second),64*sheet_norm(vector))]


def run():
    m15 = fifteen_sheet_scan()
    prepared = resolved_ports({(6,1,0):1},4)
    herald_vector = next(v for x,c,v in prepared if (x,c)==(0,1))
    herald = Fraction(sheet_norm(herald_vector),16)
    assert herald_vector==[2,1,0,0,0] and herald==Fraction(5,16) and sum(sheet_norm(v) for _,_,v in prepared)==16
    joint = [herald*p for p in difference_oracle(herald_vector)]
    assert joint==[Fraction(3,64),Fraction(7,512)]
    cases = []
    for label,vector,expected in [("coherent",[2,1,0,0,0],[Fraction(3,20),Fraction(7,160)]),
                                  ("localized",[1,0,0,0,0],[Fraction(1,4),Fraction(3,32)])]:
        oracle = difference_oracle(vector)
        assert oracle==expected
        schedules = [five_sheet_tree(vector,first_route) for first_route in (False,True)]
        assert all([Fraction(s["p_one_dark"]),Fraction(s["p_two_dark"])]==oracle for s in schedules)
        cases.append(dict(input=label,difference_norm_oracle=[str(p) for p in oracle],trees=schedules))
    return dict(fifteen_sheet_uninterrupted=m15,
                five_sheet_repeated_record=dict(N=8,M=5,departure_gains=[1,0,0,0,0,0,0,0],inputs=cases,
                    native_preparation=dict(start=[6,1],initial_sheet=0,ticks=4,herald_port=[0,1],
                                            sheet_numerators=herald_vector,
                                            herald_probability=str(herald),herald_and_one_dark=str(joint[0]),
                                            herald_and_two_dark=str(joint[1])),
                    conventions="Coin +1=R, -1=L; only L->L has negative sign. A three-tick probe is "
                                "unmeasured until its position and direction port is read. Dark is (x-c,-c) "
                                "from (x,c). Each one-tick route measures the position and direction and "
                                "retains either outcome. A non-dark probe ends the branch. Terminal leaves "
                                "exhaust the instrument. Child vectors are exact integer amplitudes over "
                                "sqrt(initial_squared_norm * 2^elapsed_ticks). A fresh-sheet product is a control."),
                checks=dict(complete_six_tick_scan=True,first_distinction_at_tick_five=True,
                            single_start_tomography_rank_and_inverse=True,path_words_equal_incremental_propagation=True,
                            four_tick_native_herald=True,
                            single_and_double_dark_match_sheet_difference_norms=True,all_record_mass_exact=True,
                            both_routing_directions_at_each_return=True))


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output",type=Path)
    args = parser.parse_args()
    result = run()
    args.output.mkdir(parents=True,exist_ok=True)
    destination = args.output/"native_gain_ports.json"
    destination.write_text(json.dumps(result,separators=(",",":"),allow_nan=False)+"\n",encoding="utf8")
    print(result["checks"])
