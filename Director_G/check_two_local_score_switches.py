"""Generate two-packet site spectra and test mixtures without across-launch memory."""
from argparse import ArgumentParser
from collections import Counter
from fractions import Fraction as Q
from itertools import combinations_with_replacement, product
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def bank(n, k, pooled):
    # Controlled straight/turn permutations act on the known incoming rail of
    # each distinct label. Deterministic routes never erase a label.
    counts = Counter()
    for label in range(n):
        group = min(label // k, 2)
        route = ("RRLLLLLL", "RRRRLLLL", "RRRRRRRR")[group]
        x, rail = 0, "R"
        for direction in route:
            rail = direction
            x += 1 if rail == "R" else -1
        require((x, rail) == ((-4, "L"), (0, "L"), (8, "R"))[group],
                "unrouted packet")
        if group < 2 and not pooled[group] and label == group*k:
            rail = "R"
        x += 1 if rail == "R" else -1
        counts[x % 24] += 1
    table = [Q(counts[i], n) for i in range(24)]
    require(sum(table) == 1 and table[9] == Q(n-2*k, n), "spectator changed")
    return table


def rates(tables, score):
    numerators = [[score(x) for x in table] for table in tables]
    require(all(min(v) >= 0 and sum(v) > 0 for v in numerators), "invalid score")
    return [v[9]/sum(v) for v in numerators], [sum(v) for v in numerators]


def test_score(n, k, tables, score):
    u = Q(1, n)
    s = (n-2*k)*u
    r, z = rates(tables, score)
    d = score(k*u)+score(Q(0))-score((k-1)*u)-score(u)
    require(z == [z[0], z[0]+d, z[0]+d, z[0]+2*d], "packet denominator")
    contrast = r[0]-r[1]-r[2]+r[3]
    x = d/z[1]
    require(contrast == 2*score(s)*d*d/(z[0]*z[1]*z[3]), "square identity")
    require(contrast == 2*r[1]*x*x/(1-x*x), "relative contrast")
    return dict(rates=r, delta=d, contrast=contrast)


def discontinuous_half(table):
    values = []
    for h in (Q(1, 2), -Q(1, 2)):
        scores = [1/(1+h)-Q(1, 2) if w == Q(1, 2) else w for w in table]
        values.append([v/sum(scores) for v in scores])
    require([sum(col)/2 for col in zip(*values)] == list(table), "endpoint construction")
    return values[0] != list(table)


def run():
    responses = dict(ordinary=lambda w: w, squared=lambda w: w*w,
                     concave=lambda w: 2*w-w*w, pedestal=lambda w: w+Q(1, 24))
    rows = []
    for n in (8, 16, 32, 64):
        for k in range(2, n//2+1):
            tables = [bank(n, k, settings) for settings in product((False, True), repeat=2)]
            reports = {name: test_score(n, k, tables, score) for name, score in responses.items()}
            require(reports["ordinary"]["contrast"] == reports["pedestal"]["contrast"] == 0,
                    "affine score")
            expected = k < n//2
            require(all((reports[name]["contrast"] > 0) == expected
                        for name in ("squared", "concave")), "nonlinear score with empty spectator")
            base = reports["squared"]["rates"]
            alt = reports["concave"]["rates"]
            if expected:
                require((base[0]-base[1])*(alt[0]-alt[1]) < 0, "opposite one-switch errors")
                weight = (alt[0]-alt[1])/(alt[0]-alt[1]-(base[0]-base[1]))
                mixed = [weight*a+(1-weight)*b for a, b in zip(base, alt)]
                require(0 < weight < 1 and mixed[0] == mixed[1] and mixed[3] > mixed[1],
                        "one-switch false pass")
            else:
                weight = None
            nonlinear_pedestal = test_score(n, k, tables, lambda w: w*w+Q(1, 24))
            require(nonlinear_pedestal["contrast"] > 0, "positive empty spectator")
            rows.append(dict(n=n, k=k, responses=reports, cancelling_weight=weight,
                             pedestal_square_contrast=nonlinear_pedestal["contrast"]))
    witness = next(row for row in rows if row["n"] == 8 and row["k"] == 3)
    require(witness["responses"]["squared"]["contrast"] == Q(16, 693), "example")
    total, altered = 0, 0
    for t in combinations_with_replacement(range(17), 4):
        if sum(t) == 16:
            altered += discontinuous_half([Q(i, 16) for i in t])
            total += 1
    require(altered > 0, "endpoint perturbation was never exercised")
    return dict(bank_size=24, settings=["SS", "SP", "PS", "PP"], rows=rows,
                endpoint_four_site_tables=total, endpoint_tables_with_nonordinary_type=altered)


if __name__ == "__main__":
    p = ArgumentParser(description=__doc__)
    p.add_argument("output", type=Path)
    args = p.parse_args()
    results = run()
    with args.output.open("x", encoding="utf8", newline="\n") as dest:
        json.dump(results, dest, default=str, indent=2)
        dest.write("\n")
