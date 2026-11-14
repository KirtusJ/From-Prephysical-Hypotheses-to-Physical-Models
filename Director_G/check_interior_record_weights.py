"""Replay an inserted whole-position write by two integer constructions."""
import argparse
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import product
import json
from pathlib import Path

from check_velocity_readout import line_step


CLOCKS = {"coarse": (2, 6, 7), "fine": (2, 4, 6, 7)}
SITES = tuple(range(-7, 8, 2))
G = dict(zip(SITES, (-8, 48, -8, 1, 15, 0, -48, 0)))
H = {(0, 0, -1): 1, (0, 2, 3): 1, (-2, -4, -5): -8, (2, 4, 5): -8,
     (-2, -2, -3): 8, (2, 2, 3): 8, (-2,-4,-3): -2}
RESULT = Path(__file__).with_name("results") / "interior_record_weights.json"


def enumerate_words(clocks):
    amps = defaultdict(lambda: [0, 0])
    counts = Counter()
    for word in product((0, 1), repeat=7):
        site, rail, sign = 0, 0, 1
        history = []
        for clock, turn in enumerate(word, 1):
            sign *= -1 if rail == turn == 1 else 1
            site += 1 if turn == 0 else -1
            rail = turn
            if clock in clocks:
                history.append(site)
        key = tuple(history)
        amps[key][rail] += sign
        counts[key] += 1
    return dict(amps), counts


def iterate_writes(clocks, exponent=None):
    # Offset indexes reachable positions j as 2jâˆ’t at clock t.
    branches = {(): (0, [1], [0], Fraction(1))}
    last = 0
    for tick in clocks:
        new = {}
        for h, (offset, r, l, p) in branches.items():
            for _ in range(tick-last):
                r, l = line_step(r, l)
            weights = [a*a + b*b for a, b in zip(r,l)]
            if exponent is not None:
                den = sum(w**exponent for w in weights if w)
            for j, (a,b,w) in enumerate(zip(r,l,weights),offset):
                if not w:
                    continue
                law = p if exponent is None else p*Fraction(w**exponent,den)
                new[h+(2*j-tick,)] = (j,[a],[b],law)
        branches = new
        last = tick
    return {h: ((a[0], b[0]),p) for h,(_,a,b,p) in branches.items()}


def hscore(word):
    return H.get((word[0], word[-2], word[-1]), 0)


def report_schedule(name, clocks):
    amps, fair = enumerate_words(clocks)
    propagated = iterate_writes(clocks)
    assert {w: tuple(row) for w,row in amps.items() if any(row)} == {
            w: row for w,(row,_) in propagated.items()}
    table = []
    rows = defaultdict(Counter)
    hm = Counter()
    for word,(a,b) in sorted(amps.items()):
        weight = a*a + b*b
        table.append([list(word), a, b, weight, fair[word]])
        if weight:
            rows[weight][word[-1]] += 1
            hm[weight] += hscore(word)
    assert sum(row[3] for row in table) == sum(row[4] for row in table) == 128
    G_rows = {m: sum(G[x]*v for x,v in sites.items()) for m,sites in rows.items()}
    max_weight = max(rows)
    max_words = [w for w, weight in ((r[0],r[3]) for r in table) if weight == max_weight]
    if name == "coarse":
        assert G_rows == {1:0,4:0,16:0,36:0}
        assert len(max_words) == 1 and G[max_words[0][-1]] == 0
    else:
        assert G_rows == {1:16,4:-8,16:1} and hm == {1:32,4:-16,16:2}
        assert all(hscore(word) == 1 for word in max_words)
        assert sum(hscore(w)*n for w,n in fair.items()) == 44
        assert [w[1] for w in sorted(amps) if hscore(w)==8 and w[0]==-2 and any(amps[w])] == [-4,-2,0]
    local = {}
    for power in (0,1,2):
        laws = {w:p for w,(_,p) in iterate_writes(clocks,power).items()}
        assert sum(laws.values()) == 1
        g = sum(G[w[-1]]*p for w,p in laws.items())
        h = sum(hscore(w)*p for w,p in laws.items())
        local[str(power)] = {"G":str(g),"H":str(h)}
    if name == "fine":
        assert Fraction(2,7)*Fraction(local["0"]["G"])+Fraction(5,7)*Fraction(local["2"]["G"])==0
        assert [local[str(q)]["H"] for q in (0,1,2)] == ["1/9", "0", "2/9"]
    return {"clocks": clocks, "reachable_words": table,
            "position_multiplicity_by_mass": {str(m):[sites[x] for x in SITES] for m,sites in sorted(rows.items())},
            "G_numerator_by_mass": dict(sorted(G_rows.items())), "H_numerator_by_mass":dict(sorted(hm.items())),
            "ordinary_position_numerators": [sum(m * sites[x] for m,sites in rows.items()) for x in SITES],
            "maximum_words": max_words, "locally_normalized_position_scores": local}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--write",action="store_true",help="replace the stored replay")
    args = p.parse_args()
    result = {n: report_schedule(n, ts) for n,ts in CLOCKS.items()}
    delta = sum(abs(a-b) for a,b in zip(result["coarse"]["ordinary_position_numerators"],
                                           result["fine"]["ordinary_position_numerators"]))
    assert Fraction(delta, 256) == Fraction(13,64)
    result["reachable_word_columns"] = ["positions","right_amplitude","left_amplitude","signed_mass","fair_count"]
    data=(json.dumps(result,indent=2)+"\n").encode()
    if args.write:
        RESULT.write_bytes(data)
    else:
        assert RESULT.read_bytes()==data
        print("Replayed both schedules, including dark words, local scoring and maximum ties.")


if __name__ == "__main__":
    main()
