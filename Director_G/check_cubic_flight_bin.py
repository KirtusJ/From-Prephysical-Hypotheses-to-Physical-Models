"""Exact forward Hadamard propagation with addressed cubic arrival increments."""
import argparse
from fractions import Fraction as Q
import json
from pathlib import Path


def check(condition, name):
    if not condition:
        raise ValueError(name)


# (a,b) represents a+b*omega with omega^2+omega+1=0.
def plus(x, y):
    return (x[0]+y[0], x[1]+y[1])


def minus(x, y):
    return (x[0]-y[0], x[1]-y[1])


def phase(x, j):
    for _ in range(j % 3):
        x = (-x[1], x[0]-x[1])
    return x


def norm(x):
    a,b = x
    return a*a-a*b+b*b


def source(n, port=0):
    v = [(0,0)] * (2*n)
    v[port] = (1,0)
    return v


def forward(state, ticks):
    n = len(state)//2
    for _ in range(ticks):
        out = [(0,0)] * (2*n)
        for x in range(n):
            r,l = state[2*x:2*x+2]
            out[2*((x+1)%n)] = plus(r,l)
            out[2*((x-1)%n)+1] = minus(r,l)
        state = out
    return state


def mark(state, ports, j):
    return [phase(x,j) if i in ports else x for i,x in enumerate(state)]


def full_revival(n):
    scale = 2**12
    returned = 0
    for i in range(2*n):
        state = forward(source(n,i),24)
        returned += (state[i] == (scale,0) and sum(norm(x) for x in state) == scale**2)
    return returned


def trials(word, initial, nblocks):
    # Pair ij means arrive with bin increment i, walk 21 forward, apply source j,
    # walk 3 forward. Empty slots are exactly 24 unmodified forward ticks.
    state = initial
    bin_ports = {2,3}
    for i,j in word:
        state = forward(mark(state,bin_ports,i),21)
        state = forward(mark(state,{0},j),3)
    state = forward(state,24*(nblocks-len(word)))
    counts = []
    for j in range(3):
        final = mark(state,bin_ports,j)
        site_mass = [norm(final[i])+norm(final[i+1]) for i in range(0,len(final),2)]
        total = sum(site_mass)
        check(total == 2**(3+24*nblocks), "original-launch normalization")
        # Scalar multiplication of the original marked and unmarked packets,
        # checked on each native port including previously unoccupied ports.
        for ports,ref in ((bin_ports,3),(set(range(len(final)))-bin_ports,6)):
            check(initial[ref] == (1,0), "unit reference numerator")
            for k in ports:
                check(initial[k][1] == 0 and
                      final[k] == tuple(initial[k][0]*a for a in final[ref]), "packet plane")
        q = Q(site_mass[1],total)
        alternative = Q(site_mass[1]**2,sum(m*m for m in site_mass))
        check(alternative == 3*q*q/(3*q*q+(1-q)**2), "site-law comparison")
        counts.append((q,alternative))
    check(len(set(counts))==1, "twirl phase invariance in named models")
    return dict(word=word,twirl_exponents=[0,1,2],ticks=3+24*nblocks,
                bin_mass=counts[0][0],squared_site_response=counts[0][1])


def panel(high_word, low_word, psi, p):
    nblocks = max(len(high_word),len(low_word))
    query,high,low = [trials(word,psi,nblocks) for word in ([],high_word,low_word)]
    u,l = high["bin_mass"],low["bin_mass"]
    w = (p-l)/(u-l)
    check(l<p<u and w*u+(1-w)*l==query["bin_mass"]==p, "exact barycenter")
    alt = query["squared_site_response"]-(w*high["squared_site_response"]+
                                           (1-w)*low["squared_site_response"])
    return dict(query=query,high=high,low=low,high_fraction=w,squared_site_gap=alt)


def tetrahedron(pop):
    # Axial unit vectors represented by four tetrahedron vertices or their opposites.
    # 120-degree rotations permute the three remaining vertices around a fixed one.
    # For p=1/3 source dot (+bin)=-1/3; for p=2/3 use -bin as the second vertex.
    dot = Q(2)*pop-1
    axis_sign = 1 if dot<0 else -1
    check(axis_sign*dot == -Q(1,3), "tetrahedral axes")
    return sorted({(1+axis_sign*t)/2 for t in (Q(1),-Q(1,3))})


def main():
    args=argparse.ArgumentParser(description=__doc__)
    args.add_argument("output",type=Path)
    path=args.parse_args().output
    p=Q(5,8)
    cycles={n:full_revival(n) for n in (4,8,12,16)}
    check(cycles=={4:8,8:16,12:0,16:0}, "24-step identity columns")
    psi=forward(source(8),3)
    short=panel([(1,1)],[(1,2)],psi,p)
    check((short["high"]["bin_mass"],short["low"]["bin_mass"],short["high_fraction"])==
          (Q(365,512),Q(5,512),Q(7,8)), "short weights")
    check(short["squared_site_gap"]==Q(47166975,752237689), "short competing response")
    high=[(1,2)]*3+[(2,2)]*3+[(2,1)]*3
    low=[(1,1),(2,2)]
    sharp=panel(high,low,psi,p)
    check(sharp["high"]["bin_mass"]>Q(989,1000) and sharp["low"]["bin_mass"]==Q(5,32768),
          "long bracket")
    # Direct failure polynomial for same-phase recursion with the actual cubic angle.
    fixed=[(q,(1-q)*(1-3*q)**2) for q in (Q(1,3),Q(2,3),Q(5,8),Q(9,10))]
    check(fixed[0][1]==0 and fixed[1][1]==1-Q(2,3) and fixed[-1][1]>1-Q(9,10),
          "cubic phase is not the sixth-root fixed point")
    result=dict(revival_columns_at_24=cycles,short_panel=short,sharp_panel=sharp,
                exceptional_orbit_populations={str(q):tetrahedron(q) for q in (Q(1,3),Q(2,3))},
                same_cubic_pair_input_and_unwanted_output=fixed)
    with path.open("x",encoding="utf8",newline="\n") as out:
        json.dump(result,out,indent=2,default=str)
        out.write("\n")


if __name__=="__main__":
    main()
