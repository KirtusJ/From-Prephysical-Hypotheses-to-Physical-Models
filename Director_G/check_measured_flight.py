"""Compare squared joint-read transitions to full projective histories at eight ticks.

Use exact rotations ((3+4i)/5)^x or the identity to check the plate sign on
each incoming rail, every path and joint endpoint, and the one-tick coupling
cost. Test the full free second-moment law. Includes endpoints of zero mass.
Run python -B check_measured_flight.py NEW_DIRECTORY.
"""
import argparse
from collections import Counter
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path


def require(condition, what):
    if not condition:
        raise ValueError(what)


def rotation(x):
    c,s = F(1),F(0)
    k = 4 if x >= 0 else -4
    for _ in range(abs(x)):
        c,s = (3*c-k*s)/5,(k*c+3*s)/5
    require(c*c+s*s == 1,"plate normalization")
    return c,s


def signal(t,x,rail,enabled):
    if t % 4 != 0 or not enabled:
        return F(0)
    c,s = rotation(x)
    return (2*rail-1)*2*c*s


def histories(start, rail, enabled):
    rows = []
    masses = {(start,rail):F(1)}
    for t in range(1,9):
        future = Counter()
        for (x,incoming),m in masses.items():
            mean = signal(t-1,x,incoming,enabled)
            right = (1+mean)/2
            require(abs(right-F(1,2)) == abs(mean)/2, "shared-uniform mismatch")
            future[x+1,0] += m*right
            future[x-1,1] += m*(1-right)
        explicit = Counter()
        for word in product((0,1),repeat=t):
            x,c = start,rail
            path = F(1)
            for j,direction in enumerate(word):
                co,si = rotation(x) if enabled and j%4==0 else (F(1),F(0))
                u,v = (co,-si) if c==0 else (si,co)
                path *= (u+(-1)**direction*v)**2/2
                c = direction
                x += 1-2*c
            explicit[x,c] += path
        require(explicit == future and sum(future.values()) == 1, "all projective histories")
        if not enabled:
            require(sum((x-start)*m for (x,_),m in future.items()) == 0 and
                    sum((x-start)**2*m for (x,_),m in future.items()) == t,"fair variance")
        ports = [[x,c,str(future[x,c])] for x,c in product(range(start-t,start+t+1,2),(0,1))]
        require(sum(F(row[2]) for row in ports) == 1 and len(ports)==2*(t+1),"complete panel")
        rows.append(dict(t=t,ports=ports))
        masses = future
    if enabled and start==1:
        expected = F(1,50) if rail==0 else F(49,50)
        require(rows[0]["ports"][2] == [2,0,str(expected)],"named right daughter")
    return dict(origin=start,rail=rail,plate=enabled,panels=rows)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory",type=Path)
    dest = parser.parse_args().directory
    runs = [histories(x,c,on) for x,c,on in product((-1,0,1),(0,1),(False,True))]
    dest.mkdir(parents=True,exist_ok=True)
    with (dest/"measured_flight.json").open("x",encoding="utf8",newline="\n") as stream:
        json.dump(runs,stream,separators=(",",":"))
        stream.write("\n")
