"""Exact one-panel and paired original-launch probabilities for latent site scores."""
import argparse
from collections import Counter
from fractions import Fraction as F
from itertools import combinations_with_replacement, product
import json
from pathlib import Path

from check_dyadic_site_score import experiment


def require(ok, message):
    if not ok:
        raise ValueError(message)


def bump(w):
    if w <= F(1, 2):
        return F(0)
    z = 2*w - 1
    return z*(1-z)/4


def spike(w):
    return F(1, 2) if w == F(5, 8) else F(0)


def distribution(masses, sign, profile):
    scores = [1/(1 + sign*profile(w)) - (1-w) if w > F(1, 2) else w
              for w in masses]
    total = sum(scores)
    require(total > 0 and min(scores) >= 0, "invalid score normalizer")
    return [v/total for v in scores]


def single_table_audit():
    counts = Counter()
    deviations = Counter()
    for n in (8, 16):
        for integers in combinations_with_replacement(range(n+1), 4):
            if sum(integers) != n:
                continue
            table = [F(i, n) for i in integers]
            for profile in (bump, spike):
                plus, minus = (distribution(table, s, profile) for s in (1, -1))
                require([(a+b)/2 for a, b in zip(plus, minus)] == table,
                        "entire single-launch table")
                key = f"N{n}_{profile.__name__}"
                counts[key] += 1
                deviations[key] += int(plus != table)
    require(min(deviations.values()) > 0, "no adverse type on a tested grid")
    return dict(table_counts=counts, individually_nonordinary=deviations)


def three_tick_positions():
    by_rail = Counter()
    for path in product((0, 1), repeat=3):
        rail, site, sign = 0, 0, 1
        for daughter in path:
            if rail == daughter == 1:
                sign = -sign
            site = (site + 1-2*daughter) % 8
            rail = daughter
        by_rail[site, rail] += sign
    return [F(sum(by_rail[x, r]**2 for r in (0, 1)), 8) for x in range(8)]


def paired_contrast(rates):
    joints = {}
    for i, name in enumerate(("A", "B")):
        for j, other in enumerate(("A", "B")):
            joints[name+other] = sum(r[i]*r[j] for r in rates)/len(rates)
    contrast = joints["AA"] - joints["AB"] - joints["BA"] + joints["BB"]
    require(contrast == sum((a-b)**2 for a, b in rates)/len(rates),
            "conditional-product pair contrast")
    return dict(joints=joints, contrast=contrast)


def routed_pairs():
    rows = []
    for k in range(2, 8):
        panels = [experiment(3, k, split, copy)
                  for split, copy in ((False, False), (True, False),
                                      (False, True), (True, True))]
        rates = [[distribution(panel, sign, spike)[2] for panel in panels]
                 for sign in (1, -1)]
        require(all(r[2] == r[3] for r in rates), "copy bridge per type")
        require(all(sum(r[j] for r in rates)/2 == F(8-k, 8) for j in range(4)),
                "every one-launch spectator rate is ordinary")
        blank = paired_contrast([r[:2] for r in rates])
        late = [paired_contrast([(r[i], r[i+2]) for r in rates])["contrast"]
                for i in (0, 1)]
        rows.append(dict(k=k, conditional_spectator_rates=rates, blank=blank,
                         late_choice_contrasts=late))
    require([r["k"] for r in rows if r["blank"]["contrast"]] == [5, 6],
            "changed blank contrasts on the full eight-cell preparation grid")
    return rows


def report():
    table = three_tick_positions()
    require(sorted(table) == [0]*4 + [F(1, 8)]*3 + [F(5, 8)], "three-tick walk")
    p = sum(w for w in table if w < F(1, 2))
    pairs = {}
    for profile in (bump, spike):
        conditional = []
        for sign in (1, -1):
            dist = distribution(table, sign, profile)
            conditional.append(sum(v for w, v in zip(table, dist) if w < F(1, 2)))
        retained = sum(v**2 for v in conditional)/2
        refreshed = (sum(conditional)/2)**2
        require(refreshed == p*p and retained-refreshed == (p*profile(max(table)))**2,
                "persistence and refresh")
        pairs[profile.__name__] = dict(rates=conditional, retained=retained,
                                      refreshed=refreshed, excess=retained-refreshed)
    require(pairs["spike"]["retained"] == F(45, 256), "three-tick double hit")

    joint = F(1, 16)
    dependent = [[joint, r-joint, r-joint, 1-2*r+joint] for r in (F(1, 8), F(3, 8))]
    require(all(min(t) >= 0 and sum(t) == 1 for t in dependent), "joint table validity")
    require([sum(col)/2 for col in zip(*dependent)] == [F(i, 16) for i in (1, 3, 3, 9)],
            "dependent types with an ordinary full two-trial table")
    return dict(single_tables=single_table_audit(), three_tick=table, paired_minor_bin=pairs,
                persistent_dependent_tables=dependent, routed=routed_pairs())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    data = report()
    with args.output.open("x", encoding="utf-8", newline="\n") as out:
        json.dump(data, out, default=str, indent=2)
        out.write("\n")
