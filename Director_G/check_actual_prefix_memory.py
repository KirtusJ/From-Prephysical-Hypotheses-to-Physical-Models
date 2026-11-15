"""Audit a reflecting-walk detector on the memory left by its actual prefix."""
from argparse import ArgumentParser
from collections import Counter
from fractions import Fraction
from itertools import product
import json
from pathlib import Path

from check_forward_cut import coefficients, histories, shift
from check_reflecting_path import launch, physical_step


def path_read(armed):
    """Retain all earlier read outcomes; the bit that arms the sign is the first label."""
    totals = Counter()
    routes = Counter()
    for directions in product((0, 1), repeat=8):
        x, rail, sign = 1, 0, 1
        labels = []
        for tick, d in enumerate(directions, 1):
            if rail == d == 1:
                sign *= -1
            x, rail = shift(4, x, d)
            if tick in (2, 4, 8):
                labels.append(int(x >= 2))
            if tick == 4 and armed and labels[0] and (x,rail) == (2,1):
                sign *= -1
        word = "".join(map(str,labels))
        totals[word, x, rail] += sign
        routes[word, x, rail] += 1
    return {''.join(word):sum(n*n for (w,x,r),n in totals.items() if w==''.join(word))
            for word in product('01', repeat=3)}, sum(routes.values())


def propagated(armed, word):
    state = launch(4,1)
    labels = dict(zip((2,4,8),word))
    for t in range(1,9):
        state = physical_step(state)
        if t not in labels:
            continue
        for x in range(4):
            if int(x>=2) != int(labels[t]):
                state[x] = [0,0]
        if armed and t == 4 and word[0] == '1':
            state[2][1] *= -1
    return sum(v*v for row in state for v in row)


def dark_probes(armed_fraction):
    rows = []
    for x in range(4):
        dark = shift(4,x,1)
        for k in (1,2):
            terms = coefficients(4,x,k,dark)
            from_paths = {path[k]:sgn for path,sgn in histories(4,x,3)[dark]}
            assert terms == from_paths
            for label in (0,1):
                eligible = {mode:v for mode,v in terms.items() if int(mode[0]>=2)==label}
                blank = sum(eligible.values())
                armed = blank - 2*eligible.get((2,1),0)
                qblank, qarmed = Fraction(blank*blank,8), Fraction(armed*armed,8)
                rows.append({"source":x, "read_tick":k, "label":label,
                             "dark_port":list(dark), "paths_in_label":len(eligible),
                             "fresh":str(qblank), "armed":str(qarmed),
                             "actual_prefix":str((1-armed_fraction)*qblank+armed_fraction*qarmed)})
    return rows


def entangled_error(d):
    # A projector onto the maximally entangled vector triggers a wrong flag.
    # Apply it to each product basis input, then to the unnormalized correlated
    # column sum_i |i,i>. All amplitudes in this projector are rational.
    def projected_norm(pairs):
        diagonal_sum = sum(value for (j,k),value in pairs.items() if j==k)
        entry = Fraction(diagonal_sum,d)
        return sum(entry**2 for _ in range(d))

    sharp_rates = [sum(projected_norm({(i,j):1}) for j in range(d))/d for i in range(d)]
    product_dark = sharp_rates[0]
    correlated_dark = projected_norm({(j,j):1 for j in range(d)})/d
    assert all(rate == Fraction(1,d*d) for rate in sharp_rates)
    assert correlated_dark == 1
    return {"degeneracy":d, "correlated_source_dark":str(correlated_dark),
            "separate_mode_and_mixed_memory_dark":str(product_dark),
            "ratio":str(correlated_dark/product_dark)}


def run():
    counts, nwords = path_read(False)
    actual, nwords2 = path_read(True)
    assert nwords == nwords2 == 256
    assert all(propagated(False,w)==n and propagated(True,w)==actual[w] for w,n in counts.items())
    assert sum(counts.values())==sum(actual.values())==256
    armed = Fraction(sum(n for w,n in actual.items() if w[0]=='1'),256)
    discrepancy = Fraction(sum(abs(actual[w]-n) for w,n in counts.items()),512)
    rows = dark_probes(armed)
    failures = [row for row in rows if row['paths_in_label']==2 and row['actual_prefix']!='0']
    assert [(r['source'],r['read_tick'],r['actual_prefix']) for r in failures] == [(2,2,'1/8'),(3,1,'1/8')]
    assert (armed,discrepancy) == (Fraction(1,4),Fraction(1,16))
    return {"wells":4, "cut_after_well":1, "source":[1,"R"], "read_clocks":[2,4,8],
            "word_denominator":256, "ideal_counts":counts, "actual_prefix_counts":actual,
            "armed_prefix_mass":str(armed), "terminal_word_tv":str(discrepancy),
            "all_probes_at_second_read":rows,
            "correlated_control":[entangled_error(d) for d in (2,4,8,16)]}


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("output",type=Path)
    with parser.parse_args().output.open("x",encoding="utf-8",newline="\n") as f:
        f.write(json.dumps(run(),indent=2)+"\n")
