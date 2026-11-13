"""Run python -B check_finite_record_memory.py OUTPUT_DIRECTORY (standard library).

Exact projectors use Gaussian rationals. Quotients use Gaussian-integer pairs
modulo 3^h; this is a finite ring, including when 3^h is composite.
"""
import argparse
import json
from collections import defaultdict
from fractions import Fraction
from functools import lru_cache
from itertools import combinations
from pathlib import Path

from check_gauss_string import mult
from check_string_readouts import (
    IDENTITY, LABELS, PAIRS, R, SWAP, T, distance_kick, execute, inverse, rotation, squared,
)


D = len(PAIRS)
KICK = distance_kick(IDENTITY, 1)
DISJOINT = rotation(0, R) + rotation(2, R)
FIRST = DISJOINT + KICK + rotation(1, R)
# Repeat the designated read after a reset, with other branches receiving
# different analyzer words (including two choices with a nontrivial kick).
SECOND = [[], rotation(2, T), rotation(1, R) + KICK + rotation(1, R),
          inverse(FIRST), rotation(0, R), KICK + rotation(2, SWAP)]


def project(amplitudes):
    return tuple(mult(z, (x, -y)) for z in amplitudes for x, y in amplitudes)


def reduced(projector, modulus):
    def residue(x):
        return x.numerator * pow(x.denominator, -1, modulus) % modulus
    return tuple((residue(x), residue(y)) for x, y in projector)


def reduced_product(a, b, modulus):
    out = []
    for i in range(D):
        for j in range(D):
            value = [mult(a[D*i+k], b[D*k+j]) for k in range(D)]
            out.append(tuple(sum(z[t] for z in value) % modulus for t in (0, 1)))
    return tuple(out)


def adjoint(matrix):
    return tuple((matrix[D*j+i][0], -matrix[D*j+i][1]) for i in range(D) for j in range(D))


@lru_cache(maxsize=None)
def gate_matrix(gate, modulus):
    columns = [execute(pair, [gate]) for pair in PAIRS]
    return reduced(tuple(columns[j][i] for i in range(D) for j in range(D)), modulus)


def step(state, gate, modulus):
    u = gate_matrix(gate, modulus)
    return reduced_product(reduced_product(u, state, modulus), adjoint(u), modulus)


def propagate(state, word, modulus):
    for gate in word:
        state = step(state, gate, modulus)
    return state


def sharp(j, modulus):
    return reduced(project(execute(PAIRS[j], [])), modulus)


def panel():
    rows = []

    def include(label, source, word):
        z = execute(PAIRS[source], word)
        rows.append(dict(label=label, source=source, word=word, p=tuple(squared(z)), matrix=project(z)))

    for j, name in enumerate(LABELS):
        include("sharp_" + name, j, [])
    for k in range(1, 13):
        include(f"power_{k}", 0, rotation(1, R)*k)
    for j, name in enumerate(LABELS):
        include("disjoint_" + name, j, DISJOINT)
        include("backward_effect_" + name, j, inverse(FIRST))
    include("tree_first", 1, FIRST)  # sharp 02
    include("conjugated_first", 1, DISJOINT + inverse(KICK) + rotation(1, R))
    include("phase_removed", 1, DISJOINT + rotation(1, R))
    for j, name in enumerate(LABELS):
        include("reset_then_" + name, j, SECOND[j])
    return rows


def support(state):
    return tuple(any(z != (0, 0) for z in state[D*j:D*(j+1)]) for j in range(D))


def inspect_collisions(rows, modulus):
    buckets = defaultdict(dict)
    invisible = []
    for row in rows:
        key = reduced(row["matrix"], modulus)
        buckets[key].setdefault(row["matrix"], row)
        missing = [name for name, x, present in zip(LABELS, row["p"], support(key)) if x and not present]
        if missing:
            invisible.append(dict(label=row["label"], lost_positive_ports=missing))
    collisions = []
    for distinct in buckets.values():
        if len(distinct) > 1:
            cuts = list(distinct.values())
            collisions.append(dict(representatives=[r["label"] for r in cuts],
                                   unequal_record_pairs=[[a["label"], b["label"]]
                                        for a, b in combinations(cuts, 2) if a["p"] != b["p"]]))
    return dict(modulus=modulus, distinct_exact=sum(map(len, buckets.values())),
                distinct_reduced=len(buckets), collisions=collisions,
                disagreeing_pairs=sum(len(b["unequal_record_pairs"]) for b in collisions),
                positive_coordinate_losses=invisible)


def sharp_tree(rows, read, modulus):
    first = read(propagate(sharp(1, modulus), FIRST, modulus))
    ideal_first = squared(execute(PAIRS[1], FIRST))
    assert tuple(ideal_first) == first and all(x > 0 for x in first)
    lookup = {r["label"]: r for r in rows}
    result = []
    for j, probability in enumerate(first):
        prepared = sharp(j, modulus)
        assert read(prepared)[j] == 1
        next_read = read(propagate(prepared, SECOND[j], modulus))
        exact = lookup["reset_then_" + LABELS[j]]["p"]
        assert next_read == exact
        result.append([probability*x for x in next_read])
    assert sum(map(sum, result)) == 1
    return result


def main():
    rows = panel()
    audits = []
    modulus = 1
    while not audits or audits[-1]["collisions"] or audits[-1]["positive_coordinate_losses"]:
        modulus *= 3
        audits.append(inspect_collisions(rows, modulus))
    table = {reduced(row["matrix"], modulus): row["p"] for row in rows}
    def read(state):
        if state in table:
            return table[state]
        active = support(state)
        assert any(active)  # The reduced projector has trace one.
        return tuple(Fraction(int(present), sum(active)) for present in active)

    inventory = []
    for row in rows:
        reached = propagate(sharp(row["source"], modulus), row["word"], modulus)
        assert reached == reduced(row["matrix"], modulus)
        assert read(reached) == row["p"] and sum(read(reached)) == 1
        assert support(reached) == tuple(x != 0 for x in row["p"])
        inventory.append(dict(label=row["label"], source=LABELS[row["source"]], word=row["word"],
                              probabilities=row["p"], reduced_projector=list(reached)))
    branch = sharp_tree(rows, read, modulus)
    labels = {row["label"]: row for row in rows}
    assert labels["tree_first"]["matrix"] != labels["conjugated_first"]["matrix"]
    assert labels["tree_first"]["p"] == labels["conjugated_first"]["p"]
    assert labels["tree_first"]["matrix"] != labels["phase_removed"]["matrix"]

    gate, = rotation(1, R)
    origin = sharp(0, modulus)
    state = step(origin, gate, modulus)
    period = 1
    while state != origin:
        state = step(state, gate, modulus)
        period += 1
    assert period > 12
    power_word = [gate] * period
    ordinary = squared(execute(PAIRS[0], power_word))
    assert 0 < ordinary[0] < 1 and read(state)[0] == 1 and ordinary[1] > 0 and read(state)[1] == 0
    # This genuine native state was omitted deliberately and exercises the
    # common, globally normalized fallback rather than a row added to the table.
    outside_word = rotation(1, R) + rotation(2, T) + KICK
    outside = propagate(origin, outside_word, modulus)
    outside_read = read(outside)
    assert outside not in table and outside_read == (Fraction(1, 3),)*3 + (Fraction(0),)*3
    assert any(y != 0 for x, y in outside)
    return dict(pair_order=LABELS, row_major_projectors="Pairs of real and imaginary residues, including diagonal and zeros.",
                model="Gate sends P to U P U* in the finite ring Z[i]/3^h. Each sharp coordinate read draws from "
                      "one probability vector indexed by P, using the uniform vector on nonzero matrix rows off the table. "
                      "Every ideal zero coordinate has a zero row after reduction. Pinned rows were tested for loss of "
                      "positive coordinates, so the table never awards mass to a zero row. Outside the panel a nonzero "
                      "ideal coordinate can reduce to a zero row, as at the first projector return. "
                      "Outcome j resets the finite state to E_j. Global normalization holds on all native words. "
                      "Arbitrary completions of an effect can give distinct probabilities outside the panel.",
                collision_checks=audits, first_injective_modulus=modulus, rows=inventory,
                adaptive_from_02=dict(intermediate_then_final_joint=branch, second_words=SECOND),
                unwritten_state=dict(source="01", word=outside_word, quotient_probabilities=outside_read,
                                     ordinary_probabilities=squared(execute(PAIRS[0], outside_word))),
                first_projector_return=dict(source="01", repeated_gate=gate, period=period,
                                            quotient_probabilities=read(state), ordinary_probabilities=ordinary))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    directory = parser.parse_args().output
    data = main()
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "finite_record_memory.json").write_bytes(
        (json.dumps(data, default=str, separators=(",", ":")) + "\n").encode())
    print("Verified", len(data["rows"]), "panel rows and 36 joint bins modulo", data["first_injective_modulus"])
