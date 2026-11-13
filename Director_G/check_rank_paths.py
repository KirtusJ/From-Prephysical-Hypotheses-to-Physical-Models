"""Run python -B check_rank_paths.py NEW_DIRECTORY; uses exact finite arithmetic.

At each depth 1..10 recover every local rank and oriented port using one bit
per tick. Compare with a signed-word oracle. At depth four compare all
two-time position cells under two silent markers and a projective record.
Include empty ports, all launches, both input rails and parity/ring controls.
"""
import argparse
from collections import Counter
from fractions import Fraction
from itertools import product
import json
from pathlib import Path

from check_parity_direction import tick


def require(test, meaning):
    if not test:
        raise ValueError(meaning)


def signed_words(t, source):
    field = Counter()
    for word in product((0,1), repeat=t):
        previous, x, sign = source, 0, 1
        for c in word:
            x += 1-2*c
            sign *= -1 if previous == c == 1 else 1
            previous = c
        field[x,previous] += sign
    return field


def rank_bins(field, t):
    offset = 0
    starts = {}
    for x in range(-t,t+1,2):
        starts[x] = offset
        offset += sum(field.get((x,c),0)**2 for c in (0,1))
    require(offset == 2**t, "signed word normalization")
    return starts


def trajectories(source):
    field = {(0,source):1}
    states = [(0,source,0)]  # Global binary prefixes in numerical order.
    previous_sites = []
    panels = []
    for t in range(1,11):
        future = tick(field)
        oracle = signed_words(t,source)
        starts = rank_bins(oracle,t)
        states_new = []
        for x, _, slot in states:
            u,v = (field.get((x,c),0) for c in (0,1))
            for bit in (0,1):
                z = 2*slot+bit
                left = (u-v)**2
                if z < left:
                    y,c = x-1,1
                    new_slot = future.get((y,0),0)**2+z
                else:
                    y,c = x+1,0
                    new_slot = z-left
                require(starts[y]+new_slot == len(states_new), "preserved rank prefix")
                states_new.append((y,c,new_slot))
        field = future
        states = states_new
        visits = Counter((x,c) for x,c,_ in states)
        rows = []
        for x in range(-t,t+1,2):
            for c in (0,1):
                amp = oracle[x,c]
                require(amp == field.get((x,c),0) and visits[x,c] == amp**2,
                        "rank path vs signed port")
                rows.append([x,c,amp,visits[x,c]])
        require(len(states)==2**t and sum(row[3] for row in rows)==2**t,"all prefixes")
        panels.append(dict(t=t,denominator=2**t,ports=rows))
        previous_sites.append([x for x,_,_ in states])
    return panels,previous_sites


def two_time(source, ranks):
    middle = signed_words(2,source)
    rows = []
    for x in (-2,0,2):
        selected = {p:n for p,n in middle.items() if p[0]==x}
        marked = {x:Fraction(sum(n*n for n in selected.values()),4)}
        bare = middle
        for _ in range(2):
            future = Counter()
            for site,mass in marked.items():
                if not mass:
                    continue
                u,v = (bare.get((site,c),0) for c in (0,1))
                right = Fraction((u+v)**2,2*(u*u+v*v))
                future[site+1] += mass*right
                future[site-1] += mass*(1-right)
            marked = future
            selected, bare = tick(selected),tick(bare)
        for y in range(-4,5,2):
            fixed = Fraction(sum(ranks[1][k//4]==x and ranks[3][k]==y for k in range(16)),16)
            active = Fraction(sum(selected.get((y,c),0)**2 for c in (0,1)),16)
            rows.append([x,y,str(fixed),str(marked[y]),str(active)])
    require(all(sum(Fraction(r[c]) for r in rows)==1 for c in (2,3,4)), "all event mass")
    if source == 0:
        require([r for r in rows if r[:2] == [2,0]] == [[2,0,"0","1/80","1/16"]],
                "silent vs measured event")
    return rows


def run():
    launches = []
    for source in (0,1):
        panels,ranks = trajectories(source)
        joint = two_time(source,ranks)
        require(len(joint)==15 and [p["t"] for p in panels]==list(range(1,11)),"coverage")
        launches.append(dict(initial_rail=source,panels=panels,joint=joint))
    mixed = {(0,0):1,(0,1):1,(1,0):1,(1,1):-1}
    mixed_result = tick(mixed)
    mixed_rows = [[x,c,mixed_result[x,c]] for x,c in sorted(mixed_result,reverse=True)]
    require(mixed_rows==[[1,0,2],[0,1,2]], "mixed-parity exact crossing")
    ring = [[[x,(x+d)%4] for x in (0,2)] for d in (-1,1)]
    require(ring[0]!=ring[1] and all(sorted(y for _,y in edges)==[1,3] for edges in ring),
            "periodic flow ambiguity")
    return dict(ports=["site","rail (0=R)","signed tally","number of prefixes"],
                joint_columns=["site at 2","site at 4","rank","fresh site split","position read at 2"],
                launches=launches,mixed_parity_after=mixed_rows,ring_flows=ring)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory",type=Path)
    directory = parser.parse_args().directory
    result = run()
    directory.mkdir(parents=True,exist_ok=True)
    with (directory/"rank_paths.json").open("x",encoding="utf8",newline="\n") as stream:
        json.dump(result,stream,separators=(",",":"))
        stream.write("\n")
