"""Exact complete-rail effects for color-conditional Hadamard walks on lines and rings."""
from argparse import ArgumentParser
from collections import defaultdict
from fractions import Fraction
from itertools import combinations, product
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def step(state, ring, inverse=False):
    work = defaultdict(int)
    for (site, rail), amplitude in state.items():
        for other in (0, 1):
            move = 1 - 2 * (rail if inverse else other)
            y = site - move if inverse else site + move
            if ring:
                y %= ring
            work[y, other] += amplitude * (-1 if rail == other == 1 else 1)
    return {port: a for port, a in work.items() if a}


def flight(state, ticks, ring, inverse=False):
    for _ in range(ticks):
        state = step(state, ring, inverse)
    return state


def straight_words(site, rail, ticks, ring):
    """Signed rays classified by final rail, independent of the reverse-step routine."""
    output = defaultdict(int)
    for word in product((0, 1), repeat=ticks):
        y = site + ticks - 2 * sum(word)
        sign = (-1) ** sum(previous * current for previous, current in zip((rail,) + word, word))
        output[y % ring if ring else y, word[-1]] += sign
    return {port: a for port, a in output.items() if a}


def color(site, rule):
    if rule == "pairs":
        return (site // 2) % 2
    if rule == "thirds":
        return site % 3
    raise ValueError(rule)


def target(site, source, ticks, ring):
    shifts = (0,) if ticks == 2 else (-3, 3)
    return any(site == ((source + d) % ring if ring else source + d) for d in shifts)


def dot(left, right):
    return sum(a * right.get(port, 0) for port, a in left.items())


def evaluate(ticks, rule, ring):
    """Return first failed predicates, including failures between distinct input columns."""
    positions = range(ring) if ring else range(-7, 9)
    expected = Fraction(1, 2 if ticks == 2 else 4)
    denominator = 2**ticks
    record = dict(ticks=ticks, rule=rule, domain=ring or "line sample [-7,8]", sectors=[])
    for label in sorted({color(x, rule) for x in positions}):
        sources = [(x, r) for x in positions if color(x, rule) == label for r in (0, 1)]
        marked_columns = {}
        direct_error, gram_error, echo_error = [], [], []
        checked_amplitudes = 0
        for port in sources:
            site, rail = port
            full = flight({port: 1}, ticks, ring)
            require(full == straight_words(site, rail, ticks, ring), "signed histories disagree")
            for displacement in range(-ticks, ticks + 1, 2):
                y = (site + displacement) % ring if ring else site + displacement
                if (color(y, rule) == label) != target(y, site, ticks, ring):
                    direct_error.append([site, y])
            marked = {p: a for p, a in full.items() if color(p[0], rule) == label}
            marked_columns[port] = marked
            signed = {p: -a if p in marked else a for p, a in full.items()}
            returned = flight(signed, ticks, ring, inverse=True)
            require(dot(returned, returned) == denominator**2, "echo failed norm check")
            control = flight(full, ticks, ring, inverse=True)
            require(control == {port: denominator}, "unsigned matched inverse failed")
            sector = {p: a for p, a in returned.items() if color(p[0], rule) == label}
            tested = set(sector) | {port}
            for dest in sorted(tested):
                actual = Fraction(sector.get(dest, 0), denominator)
                wanted = (1 - 2 * expected) if dest == port else 0
                checked_amplitudes += 1
                if actual != wanted:
                    echo_error.append([port, dest, str(actual), str(wanted)])
        for i, left in enumerate(sources):
            for right in sources[i:]:
                inner = Fraction(dot(marked_columns[left], marked_columns[right]), denominator)
                wanted = expected if left == right else 0
                if inner != wanted:
                    gram_error.append([left, right, str(inner), str(wanted)])
        record["sectors"].append(dict(label=label, source_columns=len(sources),
            checked_upper_gram_entries=len(sources) * (len(sources) + 1) // 2,
            echo_coordinates_with_nonzero_or_expected_amplitude=checked_amplitudes,
            direct_mismatches=len(direct_error), gram_mismatches=len(gram_error),
            echo_mismatches=len(echo_error), first_direct_mismatch=next(iter(direct_error), None),
            first_gram_mismatch=next(iter(gram_error), None), first_echo_mismatch=next(iter(echo_error), None)))
    return record


def half_mass_same_setting():
    """One mask gives every sharp launch half, sometimes from the opposite shell."""
    record = []
    for x in range(4):
        cols = [straight_words(x, rail, 2, None) for rail in (0, 1)]
        cols = [{p: a for p, a in col.items() if color(p[0], "pairs") == 0} for col in cols]
        gram = [dot(cols[i], cols[j]) for i, j in ((0, 0), (0, 1), (1, 1))]
        require(gram == [2, 0, 2], "single fixed half mask")
        record.append(dict(source=x, accepted_shifts=[d for d in (-2, 0, 2) if color(x+d, "pairs")==0],
                           gram_numerator=gram, denominator=4))
    return record


def obstruction(ticks):
    yes = {0} if ticks == 2 else {-3, 3}
    no = set(range(-ticks, ticks + 1, 2)) - yes
    differences = sorted({a - b for a in yes for b in no} | {b - a for a in yes for b in no})
    clique = [0, 2] if ticks == 2 else [0, 2, 4]
    conflicts = []
    for x, z in combinations(clique, 2):
        marked_from_x = {x + a for a in yes} & {z + b for b in no}
        marked_from_z = {z + a for a in yes} & {x + b for b in no}
        require(marked_from_x or marked_from_z, "missing conflict edge")
        conflicts.append(dict(x=x, z=z, yes_x_no_z=sorted(marked_from_x), yes_z_no_x=sorted(marked_from_z)))
    return dict(ticks=ticks, forbidden_equal_color_offsets=differences, clique=clique, conflicts=conflicts)


def ring_clique(ticks, ring):
    """On these even rings every two even origins conflict, but paired parities can share a mask."""
    shifts = range(-ticks, ticks + 1, 2)
    yes = (0,) if ticks == 2 else (-3, 3)
    even = range(0, ring, 2)
    edges = []
    for x, z in combinations(even, 2):
        shared = {(x + d) % ring for d in shifts} & {(z + d) % ring for d in shifts}
        disagreement = sorted(y for y in shared if target(y, x, ticks, ring) != target(y, z, ticks, ring))
        require(disagreement, "claimed even clique is incomplete")
        edges.append([x, z, disagreement])
    masks = []
    for x in even:
        selected = {(source + d) % ring for source in (x, x + 1) for d in yes}
        for source in (x, x + 1):
            for d in shifts:
                y = (source + d) % ring
                require((y in selected) == target(y, source, ticks, ring), "paired origin mask disagrees")
        masks.append(dict(origins=[x, x + 1], selected=sorted(selected)))
    return dict(ticks=ticks, ring=ring, minimum_launch_labels=len(masks), conflict_edges=edges, masks=masks)


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    good = [(2, "pairs", None), (3, "thirds", None), (2, "thirds", None),
            (2, "pairs", 8), (3, "thirds", 12), (2, "thirds", 12),
            (3, "thirds", 6), (2, "pairs", 4), (3, "thirds", 3)]
    bad = [(2, "pairs", 6), (3, "thirds", 8)]
    panels = []
    for settings in good + bad:
        panel = evaluate(*settings)
        errors = sum(sector["direct_mismatches"] + sector["gram_mismatches"] + sector["echo_mismatches"]
                     for sector in panel["sectors"])
        require((errors == 0) == (settings in good), "incorrect boundary prediction")
        panels.append(panel)
    record = dict(panels=panels, label_conflicts=[obstruction(2), obstruction(3)],
                  single_fixed_half_mask=half_mass_same_setting(),
                  compact_label_minima=[ring_clique(2, 6), ring_clique(3, 8), ring_clique(3, 10)])
    with args.output.open("x", encoding="utf8", newline="\n") as out:
        json.dump(record, out, indent=2)
        out.write("\n")


if __name__ == "__main__":
    main()
