"""Run python -B check_residue_frames.py OUTPUT_DIRECTORY (standard library).

One four-site chain, two occupied sites and the three dressed Gauss links.
All gates here are real. The pair order also indexes the six physical link strings.
"""
import argparse
import json
from fractions import Fraction as F
from itertools import combinations, permutations, product
from pathlib import Path

from check_gauss_string import bond, defect, launch
from check_string_readouts import (
    GATE_KEY, LABELS, PAIRS, R, SWAP, T, colour, execute, inverse, rotation,
)


SOURCE = (0, 2)
SOURCE_INDEX = PAIRS.index(SOURCE)
MIXED = ["03", "12"]
TILTS = {"R": R, "T": T}
PRIME_MASS = F(9, 25)


def real_column(source, word):
    column = execute(source, word)
    assert all(y == 0 for x, y in column)
    return [x for x, y in column]


def frame(word):
    """Read the actual inverse effects and verify their transpose and both projectors."""
    columns = [real_column(pair, word) for pair in PAIRS]
    rows = []
    shared = []
    for index, pair in enumerate(PAIRS):
        effect = execute(pair, inverse(word))
        v = [x for x, y in effect]
        assert effect == [(col[index], 0) for col in columns]
        labels = []
        for prime in (2, 3):
            selected = colour(effect, prime)
            # On these real entries reduction mod (1+i) is reduction mod 2.
            residues = [x.numerator * pow(x.denominator, -1, prime) % prime for x in v]
            assert all(a * b % prime == int(i == j == selected)
                       for i, a in enumerate(residues) for j, b in enumerate(residues))
            labels.append(LABELS[selected])
        rows.append(dict(port=LABELS[index], inverse_effect_amplitudes=v,
                         reduced_projector_labels=labels))
        shared.append(sum((m for m, label in zip((PRIME_MASS, 1-PRIME_MASS), labels)
                           if label == LABELS[SOURCE_INDEX]), F(0)))
    source_output = columns[SOURCE_INDEX]
    assert sum(shared) == 1
    return dict(chronological_bonds=word, effects=rows, launch_amplitudes=source_output,
                squared_coordinate=[x*x for x in source_output], shared_prime=shared)


def check_routes():
    # R has phase (3+4i)/5 and T has phase (4-3i)/5 on a single occupied bond.
    cases = []
    for j in range(3):
        direct = rotation(j, SWAP)
        rt = rotation(j, R) + inverse(rotation(j, T))
        plus = rotation(j, R) + rotation(j, (4, 3))
        for pair in PAIRS:
            expected = execute(pair, direct)
            assert execute(pair, rt) == execute(pair, plus) == expected
            assert execute(pair, inverse(rt)) == execute(pair, direct * 3)
            assert execute(pair, rt + inverse(rt)) == execute(pair, [])
        cases.append(dict(bond=j, direct=direct, from_R_and_reciprocal_T=rt,
                          from_R_and_positive_complement=plus, signed_inverse=direct*3))
    return cases


def tagged_output(pair, input_bit, left, right, early):
    """A local occupancy-to-pointer XOR, with literal matter/link updates per bit."""
    tagged = [{}, {}]
    tagged[input_bit] = launch(4, *pair)
    ops = ["left", "copy", "right"] if early else ["left", "right", "copy"]
    for op in ops:
        if op == "copy":
            after = [{}, {}]
            for bit, branch in enumerate(tagged):
                for (mask, links), z in branch.items():
                    new_bit = bit ^ ((mask >> 1) & 1)
                    assert (mask, links) not in after[new_bit]
                    after[new_bit][mask, links] = z
            tagged = after
        else:
            j, (c, s) = (0, left) if op == "left" else (2, right)
            tagged = [bond(branch, j, c, s, 1) for branch in tagged]
        assert all(defect(mask, links) == 0 for branch in tagged for mask, links in branch)
    assert all(y == 0 for branch in tagged for x, y in branch.values())
    output = [[F(branch.get(key, (0, 0))[0], 25) for key in GATE_KEY] for branch in tagged]
    assert sum(x*x for branch in output for x in branch) == 1
    return output


def marginal_joint(left_stay, right_stay, both_stay):
    """The complete four-cell joint distribution at fixed one-bond marginals."""
    r, s, u = left_stay, right_stay, both_stay
    return [F(0), u, r-u, s-u, 1-r-s+u, F(0)]


def coupling_checks(r, s, shared):
    low, high = max(F(0), r+s-1), min(r, s)
    rows = []
    values = [("lower", low), ("midpoint", (low+high)/2), ("upper", high),
              ("conditional_calibration", r*s), ("retained_shared_prime", shared[SOURCE_INDEX])]
    for label, u in values:
        joint = marginal_joint(r, s, u)
        assert min(joint) >= 0 and sum(joint) == 1
        assert joint[1]+joint[2] == r and joint[1]+joint[3] == s
        if label == "retained_shared_prime":
            assert joint == shared
        rows.append(dict(choice=label, both_stay=u, port_masses=joint,
                         mixed_total=joint[2]+joint[3]))
    return dict(left_stay=r, right_stay=s, both_stay_interval=[low, high], checks=rows)


def frame_response(first, second, t):
    """Two prime labels at one port, with fixed sharp source 02, q=9/25."""
    if first == second == SOURCE:
        return F(1)
    if first == SOURCE:
        return PRIME_MASS if set(second).intersection(SOURCE) else t
    if second == SOURCE:
        return 1-PRIME_MASS if set(first).intersection(SOURCE) else 1-t
    return F(0)


def permutation_frames():
    # Reindex port rows by the first prime image. The second is then an arbitrary
    # relative site permutation on two-element subsets, not an arbitrary S_d.
    summaries = []
    t_values = [F(0), PRIME_MASS, F(1, 2), F(1)]
    for n in range(3, 7):
        pairs = list(combinations(range(n), 2))
        counts = [0, 0, 0]
        for perm in permutations(range(n)):
            images = [tuple(sorted((perm[a], perm[b]))) for a, b in pairs]
            next_pair = images[pairs.index(SOURCE)]
            prev_pair = pairs[images.index(SOURCE)]
            overlap = len(set(SOURCE).intersection(next_pair))
            assert overlap == len(set(SOURCE).intersection(prev_pair))
            counts[overlap] += 1
            for t in t_values:
                weights = [frame_response(a, b, t) for a, b in zip(pairs, images)]
                assert min(weights) >= 0 and sum(weights) == 1
        summaries.append(dict(sites=n, pairs=len(pairs), site_permutations=sum(counts),
                              relative_image_disjoint_adjacent_identical=counts,
                              parameter_visible=bool(counts[0])))
    return dict(anchor="02", q=PRIME_MASS, checked_t=t_values,
                formula="F(s,s)=1; F(s,a)=q and F(a,s)=1-q for adjacent a; F(s,a)=t and F(a,s)=1-t for disjoint a; F=0 if both labels differ from s.",
                finite_permutations=summaries,
                normalization="The relative permutation and its inverse send s to pairs with equal overlap with s. Either one row has mass one, or the two supported rows have complementary weights. At n=3 there is no disjoint pair.")


def check_pair(left_name, right_name):
    left, right = TILTS[left_name], TILTS[right_name]
    split = rotation(0, left) + rotation(2, right)
    route = rotation(1, R) + inverse(rotation(1, T))
    crossed = route + split + inverse(route)
    direct = frame(split)
    routed = frame(crossed)
    assert routed["launch_amplitudes"] == [F(pair == SOURCE) for pair in PAIRS]
    direct_route = rotation(1, SWAP)
    for pair in PAIRS:
        assert execute(pair, crossed) == execute(pair, direct_route + split + inverse(direct_route))
    equal = [a["port"] for a, b in zip(direct["effects"], routed["effects"])
             if a["reduced_projector_labels"] == b["reduced_projector_labels"]]
    assert equal == (MIXED if left == right else [])
    for port in equal:
        idx = LABELS.index(port)
        assert direct["squared_coordinate"][idx] == F(144, 625)
        assert routed["squared_coordinate"][idx] == direct["shared_prime"][idx] == 0

    for pair, bit in product(PAIRS, (0, 1)):
        assert tagged_output(pair, bit, left, right, True) == tagged_output(pair, bit, left, right, False)
    tagged = tagged_output(SOURCE, 0, left, right, True)
    r, s = F(left[0]**2, 25), F(right[0]**2, 25)
    first = real_column(SOURCE, rotation(0, left))
    assert [x*x for x in first] == [0, r, 0, 1-r, 0, 0]
    conditional = []
    for branch in [SOURCE, (1, 2)]:
        amplitudes = real_column(branch, rotation(2, right))
        masses = [x*x for x in amplitudes]
        assert masses[PAIRS.index(branch)] == s
        assert masses[PAIRS.index((branch[0], 3))] == 1-s
        conditional.append(dict(localized_source=branch, right_only_amplitudes=amplitudes,
                                right_only_squared_coordinates=masses))
    product_law = marginal_joint(r, s, r*s)
    for bit, branch in enumerate(tagged):
        for i, pair in enumerate(PAIRS):
            expected = direct["launch_amplitudes"][i] if int(1 in pair) == bit else 0
            assert branch[i] == expected
    assert product_law == direct["squared_coordinate"]
    coupling = coupling_checks(r, s, direct["shared_prime"])
    parameter_checks = []
    for t in [F(0), PRIME_MASS, F(1, 2), F(1)]:
        frame_weights = []
        for apparatus in (direct, routed):
            weights = []
            for effect in apparatus["effects"]:
                first, second = (PAIRS[LABELS.index(label)] for label in effect["reduced_projector_labels"])
                weights.append(frame_response(first, second, t))
            assert sum(weights) == 1
            if t == PRIME_MASS:
                assert weights == apparatus["shared_prime"]
            frame_weights.append(weights)
        untagged, protected = frame_weights
        assert protected == routed["squared_coordinate"]
        local_marginals = [untagged[1]+untagged[2], untagged[1]+untagged[3]]
        assert (local_marginals == [r, s]) == (t == PRIME_MASS)
        parameter_checks.append(dict(t=t, split_weights=untagged, sharp_routed_weights=protected,
                                     split_left_right_stay_marginals=local_marginals))
    offsets = parameter_checks[0]["split_left_right_stay_marginals"]
    slopes = [v-b for v, b in zip(parameter_checks[-1]["split_left_right_stay_marginals"], offsets)]
    assert all(abs(m) == 1 for m in slopes)
    assert [(p-b)/m for p, b, m in zip((r, s), offsets, slopes)] == [PRIME_MASS]*2
    return dict(tilts=[left_name, right_name], split=direct, routed=routed,
                identical_reduced_effects_at_same_named_port=equal,
                pointer=dict(local_read="XOR occupancy of site 1 into the bit, with the other bond at sites 2 and 3",
                             early_equals_deferred_basis_inputs=2*len(PAIRS), clean_launch_tagged_amplitudes=tagged,
                             left_only_amplitudes=first, right_only_calibration_by_left_click=conditional,
                             conditional_right_stay_given_each_left_click=[s, s],
                             left_record_masses=[r, 1-r], joint_from_conditional_calibrations=product_law),
                joint_freedom=coupling, reduced_frame_family=parameter_checks,
                split_local_marginals_affine_in_t=dict(intercepts=offsets, slopes=slopes,
                                                       forced_t_from_either_marginal=PRIME_MASS))


def main():
    cases = [check_pair(a, b) for a, b in product(TILTS, repeat=2)]
    return dict(pair_order=LABELS, sharp_launch="02", prime_order=["1+i", "3"],
                layout="Four open sites, vacuum Gauss sector. Each pair has one physical matter mask and link string.",
                coordinate_encoding="All signed amplitudes are real rational strings. Each inverse effect is a ray column in pair_order.",
                chronological_bond_encoding="[bond,left,c,s] applies [[c,-s],[s,c]]/5 on a single occupation and identity on 00,11.",
                route_synthesis_all_six_inputs=check_routes(), normalized_frame_family=permutation_frames(),
                cases=cases,
                joint_freedom_formula="With local stay marginals r,s and u=P(02), the active cells 02,03,12,13 have masses u,r-u,s-u,1-r-s+u. Both calibrated conditional probabilities P(right stay | left click)=s force u=r*s.",
                logical_scope=[
                    "For a fixed preparation, any named-port response factoring through its two reduced projectors must agree wherever the two frames have equal labels at that port. Sharp routed detection forces zero for both mixed cells in the same-tilt split.",
                    "The local pointer can be deferred past the other dressed tilt as an exact operator identity. Using the conditional-calibration joint law for the untagged terminal read also requires agreement of these terminal marginals with the experiment carrying the pointer. Merely matching the two one-bond marginals permits the full displayed interval.",
                    "The squared-coordinate law is separately evaluated for comparison. No detector data were sampled. Comparing frequencies directly across the two settings tests the factorization premise.",
                    "An addressed signed quarter turn can be supplied directly or synthesized from R and reciprocal T (the positive complementary tilt). The calculation does not supply an exact quarter turn from positive R alone."
                ])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    folder = parser.parse_args().output
    data = main()
    folder.mkdir(parents=True, exist_ok=True)
    (folder/"residue_frames.json").write_bytes((json.dumps(data, default=str, separators=(",", ":"))+"\n").encode("utf-8"))
    print("Verified four dressed comparisons, 48 pointer basis identities and all signed routes.")
