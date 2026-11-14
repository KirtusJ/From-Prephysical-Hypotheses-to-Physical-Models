"""Run python -B check_parity_eraser.py NEW_OUTPUT_DIRECTORY.

For each source rail and depth 1..8 compare every physical analyzer output
to signed first-arm words. Check both normalized marker laws, named plus
and minus detectors, corrected scans and deliberately leaked/later tags.
"""
import argparse
from collections import Counter
from fractions import Fraction
from itertools import product
import json
from pathlib import Path

from check_parity_direction import marker_step, tick


def check(test, message):
    if not test:
        raise ValueError(message)


def transpose(ports, x_parity):
    """Swap (x,L) with (x+1,R) for disjoint cells starting at x."""
    result = {}
    for (y, rail), value in ports.items():
        target = y, rail
        if y % 2 == x_parity and rail == 1:
            target = y+1, 0
        elif y % 2 != x_parity and rail == 0:
            target = y-1, 1
        check(target not in result, "competing inputs on a routed port")
        result[target] = value
    return result


def word_read(t, initial, copied=1, leak=False):
    tagged = Counter()
    direct = Counter()
    for word in product((0,1), repeat=t):
        rail = initial
        sign = 1
        for step in word:
            if rail == step == 1:
                sign = -sign
            rail = step
        x = t-2*sum(word)
        b = 1-word[copied-1]
        tagged[x,rail,b] += sign
        direct[x,rail] += sign
    corrected = Counter()
    for x in range(-t,t+1,2):
        for c, s in product((0,1),repeat=2):
            a, b = (tagged[x,c,k] for k in (0,1))
            square = a*a+b*b if leak else (a+(-1)**s*b)**2
            target = (-x,c^1) if s else (x,c)
            corrected[target] += Fraction(square,2**(t+1))
    return tagged, direct, corrected


def panel(t, initial, field, onsite, nearby):
    routed = transpose(field,t%2)
    check(transpose(routed,t%2) == field, "analyzer router is involutive")
    physical = tick(routed)
    measured = [marker_step(routed,transpose(mass,t%2),r)
                for r, mass in enumerate((onsite,nearby))]
    tagged, direct, corrected = word_read(t,initial)
    rows = []
    seen = set()
    decoded = [Counter(),Counter()]
    for x in range(-t,t+1,2):
        for c, s in product((0,1),repeat=2):
            port = x+c+1-2*s,s
            check(port not in seen, "detector collision")
            seen.add(port)
            a, b = (tagged[x,c,k] for k in (0,1))
            amp = a+(-1)**s*b
            leaked = Fraction(a*a+b*b,2**(t+1))
            check(physical.get(port,0) == amp, "sum/difference orientation")
            p, q = (mass.get(port,0) for mass in measured)
            check(p == Fraction(amp*amp,2**(t+1)), "on-site word oracle")
            target = (-x,c^1) if s else (x,c)
            decoded[0][target] += p
            decoded[1][target] += q
            rows.append([*port,x,c,s,amp,str(p),str(q),str(leaked)])
    for table in (physical,*measured):
        check(all(port in seen or value == 0 for port,value in table.items()),
              "omitted reachable detector")
    check(len(rows) == 4*(t+1) and all(sum(v.values()) == 1 for v in decoded), "coverage")
    check(all(sum(m for (y,r),m in measured[0].items() if r==s) == Fraction(1,2)
              for s in (0,1)), "Walsh branches")
    for x, c in corrected:
        check(decoded[0][x,c] == corrected[x,c] == Fraction(direct[x,c]**2,2**t),
              "all-outcome decode")
    if t == 3 and initial == 0:
        for port,ordinary,rival in [((1,0),0,Fraction(3,40)),((-1,1),Fraction(1,4),Fraction(7,40))]:
            check([mass.get(port,0) for mass in measured] == [ordinary,rival], "signed-port test")
        dark_row = next(row for row in rows if tuple(row[:2]) == (1,0))
        check(Fraction(dark_row[-1]) == Fraction(1,8), "persistent-copy control")
        for column in (6,7,8):
            by_x = Counter()
            by_branch = Counter()
            for row in rows:
                by_x[row[2]] += Fraction(row[column])
                by_branch[row[4]] += Fraction(row[column])
            check([by_x[x] for x in (-3,-1,1,3)] == [Fraction(a,8) for a in (1,3,3,1)]
                  and list(by_branch.values()) == [Fraction(1,2)]*2, "coarsened readings")
    summary = [[x,c,str(decoded[0][x,c]),str(decoded[1][x,c])] for x,c in sorted(corrected)]
    record = dict(source_rail=initial,native_depth=t,slots_at_read=t+3,
                  detectors=rows,decoded=summary)
    emitted = record["detectors"]
    check(len(emitted) == len(seen) and {(r[0],r[1]) for r in emitted} == seen, "emitted ports")
    for y,rail,x,c,s,raw,ordinary,rival,persistent in emitted:
        a,b = (tagged[x,c,k] for k in (0,1))
        check(c in (0,1) and x % 2 == t % 2 and (y,rail) == (x+c+1-2*s,s)
              and raw == a+(-1)**s*b and Fraction(ordinary) == Fraction(raw*raw,2**(t+1))
              and Fraction(rival) == measured[1].get((y,rail),0)
              and Fraction(persistent) == Fraction(a*a+b*b,2**(t+1)), "emitted joint detector")
    return record


def run():
    panels = []
    for initial in (0,1):
        field = {(2,0):1,(-1,1):(-1)**initial}
        onsite = nearby = {port:Fraction(1,2) for port in field}
        for t in range(1,9):
            panels.append(panel(t,initial,field,onsite,nearby))
            onsite = marker_step(field,onsite,0)
            nearby = marker_step(field,nearby,1)
            field = tick(field)
    check([(p["source_rail"],p["native_depth"],p["slots_at_read"]) for p in panels]
          == [(r,t,t+3) for r in (0,1) for t in range(1,9)], "clock and horizon")
    controls = []
    for name, copied, leak in (("unread_copy",1,True),("second_direction",2,False)):
        for t in range(copied,9):
            _,direct,decoded = word_read(t,0,copied,leak)
            rows = [[x,c,str(Fraction(direct[x,c]**2,2**t)),str(decoded[x,c])]
                    for x,c in sorted(decoded)]
            distance = sum(abs(Fraction(a)-Fraction(b)) for _,_,a,b in rows)/2
            controls.append(dict(kind=name,t=t,TV=str(distance),records=rows))
    for name,t in (("unread_copy",3),("second_direction",4)):
        selected = [p for p in controls if p["kind"]==name and p["TV"]!="0"]
        check((selected[0]["t"],selected[0]["TV"]) == (t,"1/4"), "first control failure")
    return dict(detector_columns=["physical site","physical rail","logical site","original rail",
                                 "Walsh outcome","signed tally","on-site","radius-one","persistent copy"],
                decoded_columns=["corrected site","corrected rail","on-site","radius-one"],
                panels=panels,controls=controls)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory",type=Path)
    directory = parser.parse_args().directory
    directory.mkdir(parents=True,exist_ok=True)
    result = run()
    with (directory/"parity_eraser.json").open("x",encoding="utf8",newline="\n") as stream:
        json.dump(result,stream,separators=(",",":"))
        stream.write("\n")
