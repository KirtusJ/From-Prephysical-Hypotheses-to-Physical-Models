"""Compile arbitrary finite lists of (sign, residue) on two terminal rails using position masks.

Run python check_residue_mask_preparation.py OUTDIR. Uses only the standard library.
The returned schedule is in moving deficits d: physical site x=start+t-2*d mod N.
"""
import argparse
from collections import Counter
from math import gcd
import json
from pathlib import Path


def require(ok, message):
    if not ok:
        raise ValueError(message)


def compile_masks(m, size, right, left, target, start=0, timed=True, compensate=True):
    """Use a single reservoir. A slot's delay is solved from its absolute terminal gain."""
    require(m >= 3 and size > 0 and size % (2*m) == 0, "incompatible staircase period")
    require(0 <= start < size and 0 <= target < size, "invalid physical start or target")
    h = {3: 4, 4: 5}.get(m, m-1)
    require(h >= 4 and gcd(h,m) == 1, "pulse width")
    slots, rows = [], []
    for rail, items in (("R", right), ("L", left)):
        walls = {0,h} if rail == "R" else {0,h,h+2}
        for sign, residue in items:
            require(sign in (-1,1) and 0 <= residue < m, "invalid signed residue")
            # Right stock takes LLR in storage transfer; left stock takes LL at closure.
            # Each flips exactly once. Place the sole optional dwell away from both walls.
            pulse_sign = -sign if compensate else sign
            pulse = "L"*h if (-1)**(h-1) == pulse_sign else "LLR"+"L"*(h-2)
            pulse += "R"
            slots.append((len(rows), rail, sign, residue, pulse, walls))
            rows.extend([walls]*(len(pulse)+m-1))
        if rail == "R":
            rows.extend(({0,h+1}, {0,h+2}, {0,h+2}))
            transfer_end = len(rows)
    padding = (target - (start+len(rows)+3-2*(h+2))) % size
    rows.extend([{0,h,h+2}]*padding)
    rows.extend(({h,h+2}, {h+1,h+2}, {h+2}))
    horizon = len(rows)
    common_gain = sum((start+t)//2 for t in range(horizon))
    receipts = []
    for begin, rail, sign, residue, pulse, walls in slots:
        # Baseline sum of departure deficits for this one lineage with delay zero.
        d = area = 0
        offsets = []
        for step in pulse:
            area += d
            d += step == "L"
            offsets.append(d)
        end = begin + len(pulse)
        if rail == "R":
            transfer_start = transfer_end-3
            area += (transfer_start-end)*h + (3*h+3) + (horizon-transfer_end)*(h+2)
        else:
            area += (horizon-2-end)*h + 2*h+1
        baseline = (common_gain-area) % m
        delay = ((residue-baseline)*pow(h,-1,m)) % m if timed else 0
        for t, d in enumerate(offsets, begin+delay):
            rows[t] = walls | {d}
        actual_sign = (-1)**sum(a == b == "L" for a,b in zip("R"+pulse,pulse))
        require(actual_sign == (-sign if compensate else sign), "deposit pulse sign")
        receipts.append(dict(rail=rail, sign=sign, residue=residue, baseline=baseline,
                             slot_start=begin, word=pulse, pulse_sign=actual_sign, delay=delay))
    require(horizon == 6+padding+sum(len(pulse)+m-1 for _,_,_,_,pulse,_ in slots),
            "native schedule length")
    require(max(map(len, rows)) <= 4, "too many simultaneous position windows")
    return rows, dict(h=h, ticks=horizon, padding=padding, start=start, target=target,
                      max_sites=max(map(len,rows)), slots=receipts)


def physical_replay(m, size, rows, start):
    """Propagate distinct admitted paths directly on named physical wells of the actual ring."""
    paths = [(start,"R",1,0)]
    for t, deficits in enumerate(rows, 1):
        sites = {(start+t-2*d) % size for d in deficits}
        surviving = []
        for x,c,s,g in paths:
            sheet = (g+x//2) % m
            for outgoing, dx in (("R",1),("L",-1)):
                y = (x+dx) % size
                if y in sites:
                    surviving.append((y,outgoing,-s if c == outgoing == "L" else s,sheet))
        paths = surviving
    return Counter(paths)


def sparse_cells(census):
    return [[*cell, n] for cell,n in sorted(census.items())]


def trial(m, size, right, left, target, start=0, timed=True, compensate=True):
    rows, info = compile_masks(m,size,right,left,target,start,timed,compensate)
    expected = Counter((target,rail,s,g) for rail,items in (("R",right),("L",left)) for s,g in items)
    census = physical_replay(m,size,rows,start)
    require(all(cell[0] == target for cell in census), "unexpected final well")
    info.update(order=m, size=size, right_items=len(right), left_items=len(left),
                exact_match=census==expected, missing=sparse_cells(expected-census),
                extra=sparse_cells(census-expected))
    return info


def run():
    orders = (3,4,5,6,7,8,9,10,12,15,16,24)
    families = []
    for m in orders:
        size = (8 if m < 5 else 4)*m
        bins = [(s,g) for s in (-1,1) for g in range(m)]
        families_to_test = [
            ("all signed bins on both rails", bins, bins[::-1], 0, 0),
            ("duplicate and canceling bins", [(1,0),(1,0),(-1,0)], [(-1,m-1)]*2, 0, size-1),
            ("empty", [], [], 0, size-1),
            ("odd nonzero start", [(-1,0)], [(1,1),(1,1)], size-1, 0)]
        for name,right,left,start,target in families_to_test:
            info = trial(m,size,right,left,target,start)
            require(size//2 > info["h"]+3 and info["exact_match"], "unintended paths on safe ring")
            phases = sorted({item["delay"] for item in info["slots"]})
            if name == "all signed bins on both rails":
                require(len(phases) > 1, "missing phase variation")
            if m == 5 and name == "duplicate and canceling bins":
                example = info.copy()
            families.append(dict(name=name, order=m, circumference=size, h=info["h"], ticks=info["ticks"],
                                 start=start, target=target, nR=len(right), nL=len(left),
                                 max_sites=info["max_sites"], applied_delays=phases))

    failures=[]
    for m in (3,4):
        bins=[(s,g) for s in (-1,1) for g in range(m)]
        for name, right, left in (("empty",[],[]),("all",bins,bins[::-1])):
            info=trial(m,4*m,right,left,0)
            failures.append(dict(order=m, name=name, ticks=info["ticks"], exact_match=info["exact_match"],
                                 missing=info["missing"], extra=info["extra"]))
    require([f["exact_match"] for f in failures] == [False,False,True,False],
            "small-ring alias controls")

    adversaries=[]
    for name,timed,compensate in (("no phase adjustment",False,True),("no sign compensation",True,False)):
        info=trial(7,28,[(1,0),(-1,3)],[(-1,4)],27,timed=timed,compensate=compensate)
        require(not info["exact_match"], "mutated compiler escaped")
        adversaries.append(dict(name=name, missing=info["missing"], extra=info["extra"]))

    return dict(scope="One sharp right-rail launch; true cyclic wells; only whole-position masks.",
                columns=["site","rail","sign","absolute_residue","multiplicity"], verified=families,
                example=example, original_small_rings=failures, mutant_controls=adversaries)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory",type=Path)
    directory = parser.parse_args().directory
    result = run()
    directory.mkdir(parents=True,exist_ok=True)
    with (directory/"residue_mask_preparation.json").open("x",encoding="utf8",newline="\n") as out:
        json.dump(result,out,separators=(",",":"))
        out.write("\n")
