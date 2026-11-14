"""Run python -B whole_cylinders.py OUTPUT_DIRECTORY. Prespecified checks:

Use the prime 5 in the four-site alternative. For all unions of the occupied
terminal bins at each t=0..8, compare ordinary and altered cylinder weights
after h=0..8 unrestricted steps; record every failure. Test the two-step
uniform routing counts from every oriented source. At t=5 choose five walks
to (1,R) and one to (1,L), in lexicographic word order; retain their signs
and both weights before and after one extension. The altered weight must
exceed 2^5 and violate continuation; the ordinary weight must double.
"""
import argparse
import json
from itertools import combinations
from pathlib import Path

from whole_ring import ORIGIN, VERTICES, counts_and_signs, extend, step, term


def propagate(bins):
    out = {}
    for p,(n,d) in bins.items():
        for letter in "LR":
            y,g = step(p,letter)
            m,e = out.get(y,(0,0))
            out[y] = m+n,e+g*d
    return out


def compare(bins):
    return sum(d*d for n,d in bins.values()), sum(term(n,d,5) for n,d in bins.values())


def verify():
    source_failures = []
    for port in VERTICES:
        bins = propagate(propagate({port:(1,1)}))
        parity_ports = {p for p in VERTICES if p[0]%2 == port[0]%2}
        if set(bins) != parity_ports or any(n != 1 for n,d in bins.values()):
            source_failures.append(port)
    full = {ORIGIN:(1,1)}
    checked, failures = 0, []
    for t in range(9):
        for size in range(len(full)+1):
            for chosen in combinations(full,size):
                bins = {p:full[p] for p in chosen}
                initial,_ = compare(bins)
                for h in range(9):
                    ordinary, altered = compare(bins)
                    checked += 1
                    if ordinary != altered or ordinary != 2**h*initial:
                        failures.append([t,chosen,h,ordinary,altered,initial])
                    bins = propagate(bins)
        full = propagate(full)
    paths = [("",ORIGIN,1)]
    for _ in range(5):
        paths = extend(paths)
    selected = [p for p in paths if p[1] == (1,"R")][:5] + [p for p in paths if p[1] == (1,"L")][:1]
    ordinary, altered = compare(counts_and_signs(selected))
    next_ordinary, next_altered = compare(counts_and_signs(extend(selected)))
    predicates = dict(two_step_uniform=not source_failures, cylinder_consistency=not failures,
                      separating_event=len(selected)==6 and altered>32 and
                      next_ordinary==2*ordinary and next_altered!=2*altered)
    return dict(predicates=predicates, cylinder_checks=checked, source_failures=source_failures,
                cylinder_failures=failures, paths=selected, ordinary=ordinary, altered=altered,
                extended_ordinary=next_ordinary, extended_altered=next_altered)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_directory", type=Path)
    directory = parser.parse_args().output_directory
    directory.mkdir(parents=True, exist_ok=True)
    output = directory/"whole_cylinders.json"
    if output.exists():
        raise SystemExit(f"refusing to overwrite {output}")
    result = verify()
    with output.open("x", encoding="utf-8", newline="\n") as f:
        json.dump(result, f, indent=2)
        f.write("\n")
    print(result["predicates"])
    raise SystemExit(int(not all(result["predicates"].values())))
