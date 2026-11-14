"""Exact arc and terminal-response controls for the two-well common-clock witness."""
import argparse
from collections import Counter
from fractions import Fraction
from itertools import product
import json
from pathlib import Path


def check(condition, note):
    if not condition:
        raise ValueError(note)


def arc_histories(switches, start):
    records = {"R": Counter(), "L": Counter()}
    fair = Counter()
    for word in product("RL", repeat=len(switches)):
        sign, gain, well, incoming = 1, 0, 0, start
        for switched, rail in zip(switches, word):
            if incoming == rail == "L":
                sign = -sign
            if rail == "L" and switched:
                gain += 1
            well = (well + (1 if rail == "R" else -1)) % 2
            incoming = rail
        check(well == len(switches) % 2, "unoccupied well")
        records[incoming][gain] += sign
        fair[incoming] += 1
    return records, fair


def probability(signed, ticks, x):
    cos = [Fraction(1), x]
    for _ in range(2, ticks + 1):
        cos.append(2*x*cos[-1] - cos[-2])
    return sum(v*w*cos[abs(i-j)] for i,v in signed.items() for j,w in signed.items())/(1 << ticks)


def program(switches, start, nodes):
    records, fair = arc_histories(switches, start)
    t = len(switches)
    check(fair["R"] == fair["L"] == 1 << (t-1), "unbalanced count")
    rates = []
    for x in nodes:
        right = probability(records["R"],t,x)
        left = probability(records["L"],t,x)
        check(0 <= right <= 1 and right+left == 1, "normalization")
        if t == 1:
            pred = Fraction(1,2)
        elif t == 2:
            pred = (1+x)/2 if switches[0] else Fraction(1)
        elif t == 3:
            pred = 1-x*x/2 if all(switches[:2]) else Fraction(1,2)
        elif not switches[1]:
            h = switches[0]+switches[2]
            pred = (1+[1,x,2*x*x-1][h])/2 if h else Fraction(1)
        else:
            pred = None
        if pred is not None:
            check(right == (pred if start == "R" else 1-pred), "schedule formula")
        rates.append(str(right))
    return dict(switch="".join(map(str,switches)), start=start,
                signed_output={r:dict(sorted(v.items())) for r,v in records.items()},
                right_over_original_launches=rates, fair_numerators=dict(fair),
                denominator=1 << t)


def mixture_programs(distribution, count):
    check(sum(w for x,w in distribution)+count == 1, "mixture normalization")
    histories = [arc_histories(word,"R")[0]["R"] for word in ((0,0,0,0),(1,0,0,0),(1,0,1,0))]
    return [count/2 + sum(w*probability(signed,4,x) for x,w in distribution) for signed in histories]


def detector_reports(rates, right, left):
    return [[[p*r+(1-p)*l for r,l in zip(right,left)] for p in (rate,1-rate)] for rate in rates]


def pointwise(first, second, f):
    return [f(x,y) for x,y in zip(first,second)]


def detector_case():
    f=Fraction
    m=-f(1,2)
    total=f(2,3)
    right=[f(3,4), f(1,8), f(1,8)]
    left=[f(1,8), f(1,2), f(3,8)]
    rates=mixture_programs([(m,total)],1-total)
    actual=detector_reports(rates,right,left)
    b=pointwise(*actual[0],lambda p,n:(p+n)/2)
    e=[pointwise(p,n,lambda x,y:x-y) for p,n in actual]
    lower=max(abs(v)/(2*x) for v,x in zip(e[0],b) if x)
    check(lower==f(10,21),"count bound")
    possible=[]
    for trial in [lower, total, f(1)]:
        kr=pointwise(b,e[0],lambda x,v:x+v/(2*trial))
        kl=pointwise(b,e[0],lambda x,v:x-v/(2*trial))
        check(sum(kr)==sum(kl)==1 and min(kr+kl)>=0,"trial response")
        moved=mixture_programs([(m,trial)],1-trial)
        check(detector_reports(moved,kr,kl)==actual,"all report channels agree")
        possible.append(dict(T=str(trial),R=list(map(str,kr)),L=list(map(str,kl))))
    for col in range(3):
        j1,j2 = e[1][col]/e[0][col],e[2][col]/e[0][col]
        check((1+j2)/2-2*m*j1+m*m==0,"normalized witness")
    # A blind bank with nonzero misses gives exactly the same reads for target and count.
    check(detector_reports(rates,b,b)==detector_reports([f(1,2)]*3,b,b),"zero visibility")
    # Tick three: target 0 and impostor 1/2. Off schedules have zero bias.
    k0=[f(5,8),f(3,8)]
    k1=[f(2,3),f(1,3)]
    reports0=detector_reports([f(1),f(1,2)],k0,k0[::-1])
    reports1=detector_reports([f(7,8),f(1,2)],k1,k1[::-1])
    check(reports0==reports1,"unknown response confounds the zero-cosine target at tick 3")
    # If visibility is correlated with phase, a nontrivial mixture can hide a phase.
    hidden_p=mixture_programs([(f(1), f(1))],f(0))
    hidden_q=detector_reports(hidden_p,b,b)
    true_q=detector_reports(mixture_programs([(m,f(1))],f(0)),right,left)
    combined=[[[total*z+(1-total)*w for z,w in zip(zz,ww)] for zz,ww in zip(u,v)]
              for u,v in zip(true_q,hidden_q)]
    check(combined==actual,"label-dependent zero-visibility phase imitates count")
    return dict(outcomes=["report A","report B","no click"], lower=str(lower),
                midpoint=list(map(str,b)), compatible=possible,
                all_reports=[[[str(x) for x in row] for row in case] for case in actual],
                blind_response_equal=True, three_tick_unknown_response_alias=True,
                correlated_blind_phase="mass 1/3 at x=+1 with uninformative bank B")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    directory=parser.parse_args().directory
    f=Fraction
    nodes=[-f(1),-f(1,2),f(0),f(2,7),f(1)]
    schedules=[program(s,start,nodes) for t in (1,2,3,4)
               for s in product(range(2),repeat=t) for start in "RL"]
    models=[("cubic",[(-f(1,2),f(1))],f(0)),
            ("quarter",[(f(0),f(1))],f(0)),("count",[],f(1)),
            ("dense_control",[(f(1),f(1,7)),(-f(3,8),f(4,7))],f(2,7)),
            ("mean_alias_early",[(f(1),f(1,4)),(-f(1),f(3,4))],f(0))]
    cases=[]
    for name,dist,c in models:
        p=mixture_programs(dist,c)
        scores=[]
        for m in nodes:
            score=f(1,2)+m*m-2*m*(2*p[1]-1)+(2*p[2]-1)/2
            check(score==sum(w*(x-m)**2 for x,w in dist)+c*(f(1,2)+m*m),"physical witness")
            check((score==0)==(not c and all(x==m for x,w in dist if w)),"zero criterion")
            scores.append(str(score))
        cases.append(dict(model=name,weights=[[str(x),str(w)] for x,w in dist],count=str(c),
                          right_rates=list(map(str,p)),witnesses=scores))
    result=dict(nodes=list(map(str,nodes)),schedules=schedules,models=cases,detector=detector_case())
    directory.mkdir(parents=True,exist_ok=True)
    with (directory/"common_clock_witness.json").open("x",encoding="utf8",newline="\n") as out:
        json.dump(result,out,indent=2)
        out.write("\n")


if __name__=="__main__":
    main()
