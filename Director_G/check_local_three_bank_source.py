"""Three local walk records with correlated center and separated endpoints."""
from argparse import ArgumentParser
from collections import Counter
from fractions import Fraction as Q
from itertools import product
import json
from math import prod
from pathlib import Path


def require(ok, msg):
    if not ok:
        raise ValueError(msg)


def walk(steps):
    """Signed integer output amplitudes on an open line after a sharp R launch."""
    states = {(0,0):1}
    for j in range(steps):
        new = Counter()
        for (x,rail), value in states.items():
            for out,direction in ((0,1),(1,-1)):
                new[x+direction,out] += (-1 if rail == out == 1 else 1)*value
        states = new
        require(sum(a*a for a in states.values()) == 2**(j+1), "walk norm")
    return states


def tails(table):
    return [sum(mass for word,mass in table.items() if sum(word) >= j) for j in (1,2,3)]


def middle_and(p,q,c):
    table = Counter()
    for a,b,h in product((0,1),repeat=3):
        mass = prod(v if bit else 1-v for bit,v in ((a,p),(b,q),(h,c)))
        table[a,a*h,b] += mass
    return table


def native():
    left,coin,right = walk(4),walk(2),walk(4)
    data = Counter()
    for (l,a),(c,b),(r,d) in product(left.items(),coin.items(),right.items()):
        x = int(l[0] in (2,4))
        y = int(r[0] in (2,4))
        h = int(c[0] in (0,2))
        data[x,x*h,y] += Q((a*b*d)**2,2**10)
    require(data == middle_and(Q(11,16),Q(11,16),Q(3,4)), "native signed cells")
    return data


def grid_extrema():
    """Fill the center first on outer nonzero cells, then on 00 to attain the bound."""
    grid = [Q(j,8) for j in range(9)]
    yes = no = 0
    for u,v,w in product(grid,repeat=3):
        outer = {(a,b):(u if a else 1-u)*(v if b else 1-v)
                 for a,b in product((0,1),repeat=2)}
        rem = w
        joint = Counter()
        for a,b in ((1,1),(0,1),(1,0),(0,0)):
            mass = outer[a,b]
            allocated = min(mass,rem)
            joint[a,1,b] = allocated
            joint[a,0,b] = mass-allocated
            rem -= allocated
        s1,s2,s3 = tails(joint)
        require(rem == 0 and s2+s3 == min(u+v,w+u*v), "supremum attained")
        if s2+s3 > 1:
            cut = s2-Q(1,2)
            def vertex(t):
                if t >= Q(1,2)+cut:
                    return 1
                if t <= Q(1,2)-cut:
                    return 0
                return Q(1,2)
            require(Q(sum(map(vertex,(s1,s2,s3))),3) >= Q(5,6), "complementary separating curve")
            no += 1
        else:
            yes += 1
    return [yes,no]


def lightcones():
    """Backward supports for every open-line matching and schedule through depth 3."""
    n = 8
    matchings = []
    for bits in product((0,1),repeat=n-1):
        edges = [i for i,enabled in enumerate(bits) if enabled]
        if all(i+1 not in edges for i in edges):
            matchings.append(edges)
    bounds = {}
    for depth in (1,2,3):
        supports = {tuple(1 << i for i in range(n))}
        for _ in range(depth):
            next_supports = set()
            for current in supports:
                for edges in matchings:
                    new = list(current)
                    for left in edges:
                        new[left] = new[left+1] = current[left] | current[left+1]
                    next_supports.add(tuple(new))
            supports = next_supports
        maxgap = max(j-i for row in supports for i in range(n)
                     for j in range(i+1,n) if row[i] & row[j])
        require(maxgap == 2*depth-1, "matching light-cone boundary")
        bounds[depth] = {"causal_support_patterns":len(supports), "max_overlap_distance":maxgap}
    return bounds


def run():
    table = native()
    s = tails(table)
    require(s == [Q(231,256),Q(649,1024),Q(363,1024)], "three thresholds")
    require(sum(s)/3 == Q(121,192), "ordinary count versus separately chosen bank")
    p, w = Q(11,16), Q(33,64)
    square = lambda y: y*y/(y*y+(1-y)**2)
    base = (2*square(p)+square(w))/3
    require(base-Q(2,3) == Q(28247,448950), "native-to-threshold guaranteed gap")
    low,high = tails(middle_and(Q(1,8), Q(1,8), Q(3,4))), tails(middle_and(Q(7,8), Q(7,8), Q(3,4)))
    require(max(low) < Q(49,100) < Q(51,100) < min(high), "hidden-type counterexample")
    return dict(local_word_probabilities={"".join(map(str,i)):table[i] for i in product((0,1),repeat=3)},
                native_tails=s, all_bin_norm=1, ordinary_mean=sum(s, Q(0))/3, native_random_bank_square_rate=base,
                sharp_upper=Q(2,3), three_threshold_square_rate=sum(map(square,s))/3,
                shared_source_escape={"low_tails":low,"high_tails":high,"high_type_weight":Q(3,4)},
                integer_eighth_grid_caps_and_separators=grid_extrema(), lightcone_checks=lightcones())


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("output",type=Path)
    result = run()
    with parser.parse_args().output.open("x",encoding="utf8",newline="\n") as out:
        json.dump(result,out,indent=2,default=str)
        out.write("\n")
