"""Exact scalar shells of a Hadamard walk and operator brackets with broken reflection."""

from argparse import ArgumentParser
from fractions import Fraction as Q
from itertools import product
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def transfer(ticks, defect=False):
    # Rows are output rails and columns are the two independent input rails.
    blocks = {0: ((1, 0), (0, 1))}
    for tick in range(1, ticks+1):
        updated = {}
        for x, ((a, b), (c, d)) in blocks.items():
            right = (a+c, b+d)
            left = (a-c, b-d)
            if defect and tick == 4 and x == 1:
                right, left = left, right  # a known, addressed rail exchange after the coin
            updated.setdefault(x+1, [(0,0), (0,0)])[0] = right
            updated.setdefault(x-1, [(0,0), (0,0)])[1] = left
        blocks = updated
    # Numerators of the 2x2 effects, in order RR, RL, LL.
    return {x:(a*a+c*c, a*b+c*d, b*b+d*d) for x,((a,b),(c,d)) in sorted(blocks.items())}


def summed(effects, sites):
    return tuple(sum(effects[x][i] for x in sites) for i in range(3))


def scalar_shells(effects, den):
    shell = []
    for x in sorted(effects):
        a,b,c = effects[x]
        require(effects[-x] == (c,-b,a), "reflection on every effect")
        if x >= 0:
            sites = [x,-x] if x else [0]
            v,off,h = summed(effects, sites)
            require(v == h and off == 0, "scalar on all input coins")
            shell.append((v,x))
    require(sum(v for v,_ in shell) == den, "whole source retained")
    return sorted(shell)


def coverage(shell):
    total = 0
    best, index = 0, None
    for i,(v,_) in enumerate(shell):
        if v-total > best:
            best, index = v-total, i
        total += v
    return best, index


def from_below(shell, target):
    # At each plane choose the translated lower cover when the target reaches it.
    chosen, residual = [], target
    for mass, radius in reversed(shell):
        if mass <= residual:
            chosen.append(radius)
            residual -= mass
    return sorted(chosen), target-residual


def shell_panel(ticks):
    den = 2**ticks
    effects = transfer(ticks)
    shell = scalar_shells(effects,den)
    width, index = coverage(shell)
    prior = sum(v for v,_ in shell[:index])
    if ticks <= 16:
        sums = {0}
        for v,_ in shell:
            sums |= {x+v for x in sums}
        values = sorted(sums)
        require(max(b-a for a,b in zip(values,values[1:])) == width, "exact mesh by enumeration")
    panels = {}
    for q in map(Q, ("1/10", "1/3", "1/2", "5/8", "7/9")):
        low, lo = from_below(shell, q*den)
        out, excluded = from_below(shell,(1-q)*den)
        high = sorted(set(r for _,r in shell)-set(out))
        hi = den-excluded
        require(lo <= q*den <= hi and max(q*den-lo,hi-q*den) <= width,
                "constructive one-sided guarantees")
        for mask,mass in [(low,lo),(high,hi)]:
            require(summed(effects,[x for x in effects if abs(x) in mask]) == (mass,0,mass),
                    "actual two-input transfer of each mask")
        panels[str(q)] = dict(low_radii=low,high_radii=high,low_mass=str(lo/den),high_mass=str(hi/den))
    return dict(ticks=ticks, denominator=den, radius_weights=[[r,v] for v,r in shell],
                largest_radial_prefix_gap=Q(max(v for v,_ in shell),den),
                exact_sorted_menu_gap=Q(width,den), unfilled_gap=[Q(prior,den),Q(prior+width,den)],
                masks=panels)


def null_direction(cols):
    """One exact rational dependence of four real symmetric two-rail effects."""
    rows = [[Q(v) for v in row] for row in zip(*cols)]
    pivots = []
    for j in range(len(cols)):
        i = len(pivots)
        pivot = next((k for k in range(i,3) if rows[k][j]),None)
        if pivot is None:
            continue
        rows[i],rows[pivot] = rows[pivot],rows[i]
        scale = rows[i][j]
        rows[i] = [v/scale for v in rows[i]]
        for k in range(3):
            if i != k:
                c = rows[k][j]
                rows[k] = [v-c*w for v,w in zip(rows[k],rows[i])]
        pivots.append(j)
        if len(pivots) == 3:
            break
    free = next(j for j in range(len(cols)) if j not in pivots)
    d = [Q(0)]*len(cols)
    d[free] = Q(1)
    for i,j in enumerate(pivots):
        d[j] = -rows[i][free]
    require(all(sum(c[k]*h for c,h in zip(cols,d)) == 0 for k in range(3)), "null direction")
    return d


def positive(mat):
    a,b,c = mat
    return a >= 0 and c >= 0 and a*c >= b*b


def operator_panel(ticks,q):
    den = 2**ticks
    effects = transfer(ticks,defect=True)
    require(summed(effects,effects) == (den,0,den), "defect remains unitary")
    require(any(effects[-x] != (c,-b,a) for x,(a,b,c) in effects.items()), "broken reflection")
    z = {x:q for x in effects}
    moves = 0
    while len(frac := [x for x,h in z.items() if 0 < h < 1]) > 3:
        group = frac[:4]
        d = null_direction([effects[x] for x in group])
        step = min((1-z[x])/v if v > 0 else -z[x]/v for x,v in zip(group,d) if v)
        for x,v in zip(group,d):
            z[x] += step*v
        moves += 1
    require(all(0 <= h <= 1 for h in z.values()), "feasible coordinates")
    target = (q*den,Q(0),q*den)
    require(all(sum(z[x]*v[k] for x,v in effects.items()) == target[k] for k in range(3)),
            "matrix target survives every floating step")
    low=[x for x in effects if z[x] == 1]
    high=[x for x in effects if z[x] > 0]
    lo,hi=summed(effects,low),summed(effects,high)
    require(positive(tuple(t-a for t,a in zip(target,lo))) and
            positive(tuple(a-t for a,t in zip(hi,target))), "matrix brackets")
    return dict(ticks=ticks, q=str(q), denominator=den, low_sites=low, high_sites=high,
                fractional={x:str(z[x]) for x in frac}, moves=moves,
                lower_effect=lo, upper_effect=hi,
                width_trace_bound=Q(hi[0]-lo[0]+hi[2]-lo[2],den))


def amplitude_words(ticks):
    """Direct signed words independent of the transfer-block recurrence."""
    paths = {}
    for rail in (0,1):
        for word in product((0,1),repeat=ticks):
            loc = ticks-2*sum(word)
            sign = (-1)**sum(a*b for a,b in zip((rail,)+word,word))
            key = (loc,word[-1],rail)
            paths[key] = paths.get(key,0)+sign
    result = {}
    for loc in range(-ticks,ticks+1,2):
        col = [[paths.get((loc,out,rail),0) for out in (0,1)] for rail in (0,1)]
        result[loc] = tuple(sum(a*b for a,b in zip(col[i],col[j])) for i,j in [(0,0),(0,1),(1,1)])
    return result


def main():
    parser=ArgumentParser(description=__doc__)
    parser.add_argument("output",type=Path)
    path=parser.parse_args().output
    require(all(amplitude_words(t) == transfer(t) for t in (2,3,5,8)), "all signed path contributions")
    biased_site=transfer(3)[1]
    require(biased_site == (5,1,1), "actual target with type-dependent mass")
    def tilt(s):
        return s*(1-s)*(2*s-1)
    p,v=Q(5,8),Q(1,8)
    ordinary=(p+v)/2
    reported=(p+tilt(p)+v-tilt(v))/2
    require(reported-ordinary == Q(9,128), "hidden increasing responses pass every scalar comparison")
    out=dict(bare=[shell_panel(t) for t in (3,8,16,32,64,128,256)],
             broken=[operator_panel(t,q) for t in (8,32,64) for q in (Q(1,3),Q(5,8))],
             hidden_target=dict(site=1,tick=3,effect_numerators=biased_site,
                                ordinary=ordinary,reported=reported,excess=reported-ordinary))
    with path.open("x",encoding="utf8",newline="\n") as dest:
        json.dump(out,dest,indent=2,default=str)
        dest.write("\n")


if __name__ == "__main__":
    main()
