"""Exact sharp-launch rail records on two wells, with both clock exposures retained."""
import argparse
from collections import Counter
from fractions import Fraction
from itertools import product
import json
from pathlib import Path


def require(ok, message):
    if not ok:
        raise ValueError(message)


def physical_words(ticks):
    ports = {rail: [] for rail in "RL"}
    for word in product("RL", repeat=ticks):
        site = 0
        incoming = "R"
        power = 0
        sign = 1
        for outgoing in word:
            site = (site + (1 if outgoing == "R" else -1)) % 2
            if outgoing == "L":
                power += 1
                if incoming == "L":
                    sign = -sign
            incoming = outgoing
        require(site == ticks % 2, "unexpected occupied well")
        ports[incoming].append(("".join(word), power, sign))
    return ports


def coherent_probability(port, ticks, x):
    """The phases have real part x. Real autocorrelations give Chebyshev moments."""
    signed = Counter()
    for _, power, sign in port:
        signed[power] += sign
    chebyshev = [Fraction(1), x]
    for _ in range(2, ticks+1):
        chebyshev.append(2*x*chebyshev[-1]-chebyshev[-2])
    value = sum(n*k*chebyshev[abs(i-j)] for i,n in signed.items() for j,k in signed.items())
    return value / (1 << ticks)


def observation(ports, t, components, count, rail):
    port = ports[t][rail]
    fair = Fraction(len(port), 1 << t)
    return count*fair + sum(w*coherent_probability(port,t,x) for x,w in components)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_directory", type=Path)
    out = parser.parse_args().output_directory
    f = Fraction
    supports = [("pure_cubic_unit", [(-f(1,2), f(1))],f(0)),
                ("pure_trivial", [(f(1),f(1))],f(0)),
                ("pure_negative", [(f(-1),f(1))],f(0)),
                ("quarter_turn", [(f(0),f(1))],f(0)),
                ("count", [],f(1)),
                ("interior", [(f(2,7),f(1))],f(0)),
                ("symmetric_pair", [(-f(1,2),f(1,2)),(f(1,2),f(1,2))],f(0)),
                ("three_atoms", [(f(-1),f(1,8)),(f(0),f(3,4)),(f(1),f(1,8))],f(0)),
                ("count_and_phase", [(f(3,5),f(2,5)),(-f(1,3),f(1,5))],f(2,5))]
    ports = {t: physical_words(t) for t in (1,2,3)}
    cases, frequencies = [], {}
    for label, components, c in supports:
        require(c+sum(w for _,w in components)==1, "mixture normalization")
        p = {}
        for t in ports:
            r = observation(ports,t,components,c,"R")
            l = observation(ports,t,components,c,"L")
            require(l+r==1 and min(l,r)>=0, "physical probability")
            p[t]=r
        require(p[1]==f(1,2), "time-one control")
        scores = []
        for m in (-f(1),-f(1,2),f(0),f(2,7),f(1,2),f(1)):
            witness = 2*(1-p[3])-2*m*(2*p[2]-1)+m*m
            outside = sum(w*(x-m)**2 for x,w in components)
            require(witness==outside+c*(1+m*m), "centered score")
            require((witness==0)==(c==0 and all(x==m for x,w in components if w)), "zero set")
            radius = f(1,3)
            mass = sum(w for x,w in components if abs(x-m)>=radius)
            require(mass*radius**2<=witness and c*(1+m*m)<=witness, "stability bounds")
            scores.append(dict(target=str(m),score=str(witness),outside_third=str(mass)))
        frequencies[label] = [p[2],p[3]]
        cases.append(dict(model=label, count=str(c), components=[[str(x),str(w)] for x,w in components],
                          right_probabilities=list(map(str,p.values())), witnesses=scores))
    require(frequencies["pure_cubic_unit"]==[f(1,4),f(7,8)],"cubic unit")
    require(frequencies["symmetric_pair"]==frequencies["three_atoms"],"mixed alias")
    m=-f(1,2)
    early = [(f(1),(1+m)/2),(f(-1),(1-m)/2)]
    late = [(-m,f(1))]
    imitation=[observation(ports,2,early,0,"R"), observation(ports,3,late,0,"R")]
    require(imitation==frequencies["pure_cubic_unit"],"varying-source control")
    result = dict(denominator="all original launches at each clock",
                  words={str(t):p for t,p in ports.items()}, cases=cases,
                  changing_ensemble=dict(target=str(m), tick_two_endpoint_weights=list(map(str,[early[0][1],early[1][1]])),
                                         tick_three_real_part=str(-m), rates=list(map(str,imitation))))
    out.mkdir(exist_ok=True,parents=True)
    with (out/"two_well_witness.json").open("x",encoding="utf8",newline="\n") as handle:
        json.dump(result,handle,indent=2)
        handle.write("\n")


if __name__ == "__main__":
    main()
