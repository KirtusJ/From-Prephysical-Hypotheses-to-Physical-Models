"""Run python -B check_string_readouts.py OUTPUT_DIRECTORY (standard library).

Exact physical matter/link propagation. Coordinates are all two-occupant
configurations in the open four-site vacuum Gauss sector, in lexical order.
"""
import argparse
import json
from fractions import Fraction
from itertools import combinations, permutations
from pathlib import Path

from check_gauss_string import bond, defect, launch, single_link_kicks


N = 4
PAIRS = tuple(combinations(range(N), 2))
LABELS = ["".join(map(str, pair)) for pair in PAIRS]
W = (3, -4, 5)
R = (3, 4)
T = (4, -3)
SWAP = (0, 5)
IDENTITY = tuple(range(N))
GATE_KEY = [((1 << a) | (1 << b), (1 << b) - (1 << a)) for a, b in PAIRS]
MIX_2 = Fraction(9, 25)


def inverse(word):
    """Rational real rotations and electric phases have opposite signed inverses."""
    return [(op, j, c, -s) for op, j, c, s in reversed(word)]


def rotation(j, gate):
    return [("bond", j, *gate)]


def acquired(order):
    """Signed adjacent swaps send each original mode to its position in order."""
    current = list(IDENTITY)
    word = []
    for destination, target in enumerate(order):
        j = current.index(target)
        while j > destination:
            current[j - 1], current[j] = current[j], current[j - 1]
            word.extend(rotation(j - 1, SWAP))
            j -= 1
    assert list(order) == current
    return word


def in_order(order, word):
    route = acquired(order)
    return route + word + inverse(route)


def distance_kick(order, sign):
    return in_order(order, [("field", -1, W[0], sign * W[1])])


def execute(source, word):
    """Return all six exact Gaussian-rational amplitudes, including zeros."""
    state, denominator = launch(N, *source), 1
    for operation, j, c, s in word:
        if operation == "bond":
            state = bond(state, j, c, s, 1)
            denominator *= 5
        else:
            assert operation == "field"
            state, scale = single_link_kicks(state, N, (c, s, 5))
            denominator *= scale
        assert all(defect(mask, links) == 0 for mask, links in state)
    amplitudes = [(Fraction(x, denominator), Fraction(y, denominator))
                  for x, y in (state.get(key, (0, 0)) for key in GATE_KEY)]
    assert sum(squared(amplitudes)) == 1
    return amplitudes


def squared(amplitudes):
    return [x*x + y*y for x, y in amplitudes]


def colour(amplitudes, prime):
    active = []
    for j, pair in enumerate(amplitudes):
        x, y = [z.numerator * pow(z.denominator, -1, prime) % prime for z in pair]
        # In F2 we put i=1. In F9, 1 and i are independent over F3.
        nonzero = (x + y) % 2 != 0 if prime == 2 else (x, y) != (0, 0)
        if nonzero:
            active.append(j)
    assert len(active) == 1
    return active[0]


def records(amplitudes):
    born = squared(amplitudes)
    norm4 = sum(x*x for x in born)
    a, b = (colour(amplitudes, p) for p in (2, 3))
    mixture = [MIX_2 * (j == a) + (1 - MIX_2) * (j == b) for j in range(len(PAIRS))]
    quartic = [x*x / norm4 for x in born]
    assert sum(mixture) == sum(quartic) == 1
    return dict(born=born, quartic=quartic, residue_mixture=mixture,
                labels_mod_1_plus_i_and_3=[LABELS[a], LABELS[b]])


def xy_changes(weights):
    """The algebraic conjugate controls reverse i in every amplitude and projector."""
    return [(x, -y) for x, y in weights]


def exact_routing():
    """Compare the path-matching invariant with the physical source and output labels."""
    other = (4, 3)
    for pair in PAIRS:
        for j in range(N - 1):
            transpose = {j: j + 1, j + 1: j}
            swapped = tuple(sorted(transpose.get(x, x) for x in pair))
            for gate, expected in [(R, (pair, swapped)), (other, (swapped, pair))]:
                amplitudes = execute(pair, rotation(j, gate))
                actual = tuple(PAIRS[colour(amplitudes, p)] for p in (2, 3))
                assert actual == expected
            two_tilts = execute(pair, rotation(j, R) + rotation(j, other))
            assert two_tilts == execute(pair, rotation(j, SWAP))
        phased = execute(pair, [("field", -1, W[0], W[1])])
        assert all(PAIRS[colour(phased, p)] == pair for p in (2, 3))

    counts = []
    for n in range(3, 13):
        # The occupancies of all adjacent-bond components, plus the isolated
        # endpoint in the other matching, already identify each pair.
        labels = list(combinations(range(n), 2))
        signatures = set()
        for pair in labels:
            occupations = [int(j in pair) + int(j + 1 in pair) for j in range(n - 1)]
            signatures.add((int(0 in pair), *occupations))
        assert len(signatures) == len(labels)
        counts.append([n, len(signatures)])
    return dict(path_sites_and_distinct_pair_signatures=counts,
                four_site_source_bond_checks=len(PAIRS)*(N-1),
                both_positive_tilts_equal_signed_quarter_turn=True)


def context_test():
    source = (0, 1)
    base = rotation(1, R) + distance_kick(IDENTITY, 1)
    analyzers = [[], rotation(0, R)]
    readings = []
    for analyzer in analyzers:
        word = base + analyzer
        amps = execute(source, word)
        conjugate_word = [(op, j, c, -s if op == "field" else s) for op, j, c, s in word]
        conjugate = execute(source, conjugate_word)
        assert conjugate == xy_changes(amps) and records(conjugate) == records(amps)
        # The added analyzer fixes the entire protected port as an effect.
        for j, pair in enumerate(PAIRS):
            assert execute(pair, analyzer)[0] == (int(j == 0), 0)
        readings.append(dict(gates=word, amplitudes=amps, **records(amps)))
    assert [row["born"][0] for row in readings] == [MIX_2, MIX_2]
    assert [row["quartic"][0] for row in readings] == [Fraction(81, 337), Fraction(50625, 136897)]
    return readings


def single_and_joint():
    single = {}
    for gate in (R, T):
        rows = []
        for bond_index in range(N-1):
            word = rotation(bond_index, gate)
            for source in PAIRS:
                row = records(execute(source, word))
                assert row["residue_mixture"] == row["born"]
                rows.append(dict(bond=bond_index, source=LABELS[PAIRS.index(source)], **row))
        single[str(gate)] = rows

    word = rotation(1, R)
    columns = [execute(pair, word) for pair in PAIRS]
    outcomes = [records(col) for col in columns]
    joint_born, joint_fresh, joint_retained = [], [], []
    for mid in range(len(PAIRS)):
        for final in range(len(PAIRS)):
            joint_born.append(outcomes[0]["born"][mid] * outcomes[mid]["born"][final])
            joint_fresh.append(outcomes[0]["residue_mixture"][mid] *
                               outcomes[mid]["residue_mixture"][final])
            total = 0
            for p, mass in ((2, MIX_2), (3, 1 - MIX_2)):
                if colour(columns[0], p) == mid and colour(columns[mid], p) == final:
                    total += mass
            joint_retained.append(total)
    assert joint_born == joint_fresh
    assert all(sum(row) == 1 for row in (joint_born, joint_fresh, joint_retained))
    assert joint_born[0] == MIX_2**2 and joint_retained[0] == MIX_2
    assert all(x == 0 for j, x in enumerate(joint_retained) if j % len(PAIRS) != 0)
    twice = records(execute((0, 1), word + word))
    assert twice["born"][0] == Fraction(49, 625) and twice["residue_mixture"][0] == 1
    return dict(single_gate_all_sources=single, double_gate_no_intermediate_read=twice,
                read_between_gates=dict(source="01", bond=1, tilt=R,
                                        order="row-major intermediate then final, using pair_order",
                                        born=joint_born, fresh_prime_at_each_read=joint_fresh,
                                        retained_prime=joint_retained))


def selective_word():
    # Distances obey (boundary - boundary swap) - (interior - interior swap)
    # = 2(P02 - P23); each order is original labels in physical left-to-right order.
    terms = [((0, 3, 2, 1), 1), ((3, 0, 2, 1), -1),
             ((2, 0, 3, 1), -1), ((2, 3, 0, 1), 1)]
    phase_plate = []
    for order, sign in terms:
        phase_plate.extend(distance_kick(order, sign))
    r03 = in_order((0, 3, 2, 1), rotation(0, R))
    word = inverse(r03) + phase_plate + r03
    target = {PAIRS.index((0, 2)): 2, PAIRS.index((2, 3)): -2}
    columns = []
    for j, pair in enumerate(PAIRS):
        exponent = sum(sign * abs(order.index(pair[0]) - order.index(pair[1]))
                       for order, sign in terms)
        assert exponent == target.get(j, 0)
        phase_col = execute(pair, phase_plate)
        if exponent:
            angle = (Fraction(-7, 25), Fraction(-24 if exponent > 0 else 24, 25))
        else:
            angle = (1, 0)
        assert phase_col == [angle if i == j else (0, 0) for i in range(len(PAIRS))]
        col = execute(pair, word)
        if j not in target:
            assert col == [(int(j == k), 0) for k in range(len(PAIRS))]
        else:
            assert {k for k, z in enumerate(col) if z != (0, 0)} == target.keys()
        columns.append(dict(source=LABELS[j], phase_exponent=exponent, amplitudes=col, **records(col)))
    off_diagonal = columns[PAIRS.index((0, 2))]["born"][PAIRS.index((2, 3))]
    assert off_diagonal == Fraction(576**2, 625**2)
    # Across all orders, each pair receives the same accumulated exponent.
    # Omit the identity-order word to realize D^{-1} projectively with positive kicks.
    orders = list(permutations(IDENTITY))
    full = [sum(abs(o.index(a) - o.index(b)) for o in orders) for a, b in PAIRS]
    assert full == [40] * len(PAIRS)
    forward_inverses = []
    for pair in PAIRS:
        positive = []
        for order in orders:
            if order != IDENTITY:
                positive.extend(distance_kick(order, 1))
        # Follow the proposed inverse by D and check the actual uniform phase, not only its exponent.
        forward_inverses.append(execute(pair, positive + distance_kick(IDENTITY, 1))[PAIRS.index(pair)])
    assert len(set(forward_inverses)) == 1
    return dict(terms=terms, schedule=word, columns=columns, protected="01", active=["02", "23"],
                transition_probability=off_diagonal, omitted_positive_kick_orders=len(orders)-1,
                all_permuted_positive_kicks_by_pair=full,
                all_permuted_positive_kicks_common_phase=forward_inverses[0])


def main():
    return dict(pair_order=LABELS, physical_sector="Four ordered sites, vacuum Gauss boundary, two occupants.",
                gates="bond records (bond,left,c,s) use real rotation [[c,-s],[s,c]]/5, determinant 1, dressed hops. "
                      "field records (field,-1,x,y) apply (x+iy)/5 independently on all energized links.",
                colour_scope="Exact rational words in the specified tilts, signed adjacent swaps and uniform field. "
                             "For pure native preparation and analyzer, the two reduced projectors have a diagonal "
                             "unit at their physical label; monomial reduction makes equality of labels a frame law.",
                probabilities="Exact rational strings. The mixture uses mass 9/25 on the 1+i color and 16/25 on the 3 color. "
                              "No shots or sampling. Fractions for the two read times are joint, including all zero bins.",
                same_port_contexts=context_test(), residue_controls=single_and_joint(),
                dressed_selective_rotation=selective_word(), exact_routing=exact_routing())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    folder = parser.parse_args().output
    data = main()
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / "string_readouts.json"
    path.write_bytes((json.dumps(data, default=str, separators=(",", ":")) + "\n").encode())
    print("Verified all six source labels, both tilt residues, 36 joint bins and the routed selective rotation.")
