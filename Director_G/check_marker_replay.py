"""Run python -B check_marker_replay.py OUTPUT_DIRECTORY (standard library).

Retain 144 exact integer rail pairs on the ballistic sequence, their observed
directions, asymptotic residuals and angular gaps. Independently recover the
marker kernel from adjacent blank terminal panels; use that table alone on a
three-tick tagged flight. Compare every port to explicit signed path words.
"""
import argparse
from fractions import Fraction
import json
import math
from pathlib import Path


def advance(sites):
    out = {}
    for x, (u, v) in sites.items():
        if u + v:
            out.setdefault(x + 1, [0, 0])[0] = u + v
        if u - v:
            out.setdefault(x - 1, [0, 0])[1] = u - v
    return out


def right_probability(pair):
    u, v = pair
    return Fraction((u + v)**2, 2*(u*u + v*v))


def blank_records():
    k = math.acos(1 / math.sqrt(3))
    curvature = 3 * math.sqrt(2) / 8
    sites = {0: [1, 0]}
    table, rows = {}, []
    for t in range(4 * 144 + 1):
        future = advance(sites)
        if t < 20:
            for x, pair in sorted(sites.items()):
                right = future.get(x + 1, [0, 0])[0]
                observed = Fraction(right*right, 2*sum(z*z for z in pair))
                if observed != right_probability(pair):
                    raise ArithmeticError("adjacent blank panels disagree")
                table.setdefault(tuple(pair), [t, x, observed])
        if t and t % 4 == 0:
            n, x = t // 4, t // 2
            u, v = sites.get(x, [0, 0])
            phase = 6*n*k + math.pi/4
            factor = 4 / math.sqrt(2*math.pi*t*curvature)
            expected = (factor*0.75*math.cos(phase),
                        factor*(math.cos(phase)/4 - math.sin(phase)/(2*math.sqrt(2))))
            normed = (u/2**(t//2), v/2**(t//2))
            angle = math.atan2(v, u) if u or v else None
            rows.append(dict(n=n, raw=[u, v], angle=angle,
                             parent_probability=str(Fraction(u*u+v*v, 2**t)),
                             right_given_parent=str(right_probability((u,v))) if u or v else None,
                             approx=expected, residual=math.dist(normed, expected)))
        sites = future
    gaps = {}
    for n in (12, 36, 72, 144):
        angles = sorted(row["angle"] for row in rows[:n] if row["angle"] is not None)
        gaps[n] = max(b-a for a,b in zip(angles, angles[1:]+[angles[0]+2*math.pi]))
    return table, rows, gaps


def tagged_flight(table):
    sites = {0: [1, 0]}
    for _ in range(3):
        sites = advance(sites)
    states = [{x:z for x,z in sites.items() if int(x >= 0) == bit} for bit in (0,1)]
    masses = [{(x,rail): Fraction(z*z, 8) for x,pair in st.items()
               for rail,z in enumerate(pair) if z} for st in states]
    # A competing marker keeps the copied tag and changes its split only in tag 1.
    rival = [dict(row) for row in masses]
    witnessed, panels = [], []
    for tick in range(3, 6):
        for tag, st in enumerate(states):
            new, alt = {}, {}
            for x, pair in sorted(st.items()):
                ref_t, ref_x, h = table[tuple(pair)]
                witnessed.append(dict(tick=tick, tag=tag, site=x, pair=pair, reference=[ref_t,ref_x],
                                      right_fraction=str(h)))
                total = sum(masses[tag].get((x,r), 0) for r in (0,1))
                rival_total = sum(rival[tag].get((x,r), 0) for r in (0,1))
                for key, weight, other in [((x+1,0),h,Fraction(1,2) if tag else h),
                                           ((x-1,1),1-h,Fraction(1,2) if tag else 1-h)]:
                    new[key] = total*weight
                    alt[key] = rival_total*other
            # The tag-sensitive fair marker may occupy a dark site at later times.
            if tag:
                remaining = {x for x,_ in rival[tag]} - set(st)
                for x in remaining:
                    mass = sum(rival[tag].get((x,r),0) for r in (0,1))
                    alt[x+1,0] = alt[x-1,1] = mass / 2
            masses[tag], rival[tag] = new, alt
            states[tag] = advance(st)
        paths = {}
        elapsed = tick+1
        for word in range(2**elapsed):
            x, rail, sign, tag = 0, 0, 1, 0
            for j in range(elapsed):
                nxt = (word >> j) & 1
                if nxt == rail == 1:
                    sign = -sign
                x += 1-2*nxt
                rail = nxt
                if j == 2:
                    tag = int(x >= 0)
            key = tag, x, rail
            paths[key] = paths.get(key,0) + sign
        cells = []
        for tag in (0,1):
            for x in range(-elapsed,elapsed+1):
                for rail in (0,1):
                    raw = paths.get((tag,x,rail),0)
                    value = masses[tag].get((x,rail),0)
                    if value != Fraction(raw*raw,2**elapsed):
                        raise ArithmeticError("replayed marker and path words disagree")
                    cells.append([tag,x,rail,raw,str(value),str(rival[tag].get((x,rail),0))])
            if sum(masses[tag].values()) != sum(rival[tag].values()):
                raise ArithmeticError("rival changed the persistent tag marginal")
        panels.append(dict(tick=elapsed, cells=cells))
    return dict(witnesses=witnessed, panels=panels,
                columns=["bit","site","rail (0 = right)","signed words","replay mass","rival mass"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory",type=Path)
    dest = parser.parse_args().directory
    dest.mkdir(parents=True,exist_ok=True)
    output = dest/"marker_replay.json"
    if output.exists():
        parser.exit(2, f"Refusing to overwrite {output}\n")
    table, rows, gaps = blank_records()
    result = dict(ballistic=rows, max_angle_gaps_radians=gaps, tag_replay=tagged_flight(table))
    with output.open("x",encoding="utf-8",newline="\n") as f:
        json.dump(result,f,indent=1,allow_nan=False)
        f.write("\n")


if __name__ == "__main__":
    main()
