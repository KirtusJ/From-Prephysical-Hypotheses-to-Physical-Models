"""Two distinguishable always-moving walkers align planes, scatter, and interfere.

Run python -B check_collision_phase_reference.py OUTPUT_DIRECTORY.
"""

import argparse
import json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path


# (xA,xB,incidence,Aplane,Bplane,WalshIndex,junk,whichPath) with incidence
# 0=RL, 1=LR. Planes, tags and the selector move with the distinguishable walkers.
def compact(state):
    return {key: v for key, v in state.items() if v}


def norm(state):
    return sum(v * v for v in state.values())


def set_field(key, field, new):
    return key[:field] + (new,) + key[field + 1 :]


def contact(state):
    assert all(k[0] == k[1] == 0 for k in state)


def transport(state, steps, reverse):
    for _ in range(steps):
        out = {}
        for (a, b, c, *rest), v in state.items():
            d = 1 - 2 * c
            out[(a + d, b - d, c, *rest)] = v
        state = out
    if reverse:
        state = {set_field(k, 2, k[2] ^ 1): v for k, v in state.items()}
    return state


def excursion(state, L):
    contact(state)
    away = transport(state, L, True)
    assert all(abs(k[0]) == abs(k[1]) == L and k[0] == -k[1] for k in away)
    home = transport(away, L, True)
    assert state == home
    return home


def hbit(state, field, mask):
    contact(state)
    out = Counter()
    for k, v in state.items():
        base = k[field] & ~mask
        out[set_field(k, field, base)] += v
        out[set_field(k, field, base | mask)] += v * (-1 if k[field] & mask else 1)
    return compact(out)


def applyq(state):
    contact(state)
    return {
        set_field(set_field(k, 3, 1 - k[3]), 4, 1 - k[4]): -(1 - 2 * k[3]) * (1 - 2 * k[4]) * v
        for k, v in state.items()
    }


def applyBflip(state):
    return {k: (1 - 2 * k[4]) * v for k, v in state.items()}


def grade_expect(state):
    q = applyq(state)
    return F(sum(v * q.get(k, 0) for k, v in state.items()), norm(state))


def anchored(state):
    # H on the B coordinate, followed by B-controlled -J_A. It is a
    # reversible unitary on every input; it prepares grade + only for B=0.
    state = excursion(hbit(state, 4, 1), 1)
    out = Counter()
    for k, v in state.items():
        target = k
        if k[4]:
            target = set_field(k, 3, 1 - k[3])
            v *= -(1 - 2 * k[3])
        out[target] += v
    result = excursion(compact(out), 1)
    assert norm(result) == norm(state)
    return result


def grade_projection(src, g):
    # Literal H -- controlled Q -- H -- unresolved grade bit read. Use the
    # vacant junk bit here and replace its common known result with zero.
    assert all(not k[6] for k in src)
    state = excursion(hbit(src, 6, 1), 1)
    zero = {k: v for k, v in state.items() if k[6] == 0}
    one = {k: v for k, v in state.items() if k[6] == 1}
    state = excursion({**zero, **applyq(one)}, 1)
    state = excursion(hbit(state, 6, 1), 1)
    out = {set_field(k, 6, 0): v for k, v in state.items() if k[6] == int(g == -1)}
    return excursion(out, 1)


def coherent_grade_slot(src, adjoint=False):
    """Four-slot coarse grade-to-blank-pointer unitary and its time reversal.

    The last bit here is a grade register, rather than the outer-route record.
    """
    state = src
    for op in ("Z", "H", "Q", "H") if adjoint else ("H", "Q", "H", "Z"):
        if op == "H":
            state = hbit(state, 7, 1)
        else:
            zero = {k: v for k, v in state.items() if k[7] == 0}
            one = {k: v for k, v in state.items() if k[7] == 1}
            state = {**zero, **(applyq(one) if op == "Q" else applyBflip(one))}
        state = excursion(state, 1)
    return state


def entangled_test():
    # Correlated incidence and two-plane coordinates; the scalar state can
    # be coherently gathered at the origin from both distinct incident arms.
    src = {(0, 0, 0, 0, 0, 0, 0, 0): 2, (0, 0, 0, 1, 0, 0, 0, 0): -1, (0, 0, 1, 0, 1, 0, 0, 0): 3}
    state = coherent_grade_slot(src)
    assert norm(state) == 4 * norm(src) and grade_expect(state) == 1
    restored = coherent_grade_slot(state, True)
    assert restored == {k: 4 * v for k, v in src.items()}
    for bit, g in ((0, 1), (1, -1)):
        branch = {set_field(k, 7, 0): v for k, v in state.items() if k[7] == bit}
        expected = grade_projection(src, g)
        assert branch == (expected if g == 1 else applyBflip(expected))
    after, _ = delivered(state, "A", 1, False)
    after = excursion(after, 4)
    after, _ = delivered(after, "B", -1, False)
    assert after == {k: v * 25 for k, v in state.items()}
    freed = coherent_grade_slot(after, True)
    assert freed == {k: 100 * v for k, v in src.items()}
    return {
        "coherent_initial_origin_coefficients": [[*k, v] for k, v in sorted(src.items())],
        "initial_Q_mean": str(grade_expect(src)),
        "blank_grade_pointer_fixed_all_output_grade": "+1",
        "corrected_branches_as_coordinate_map": "P+ and Z_B P- to orthogonal pointer values",
        "uncompute_scalar_from_both_two-H-contact_numerators": 4,
        "full_scatter_echo_and_contact_inverse_returns_complete_input": True,
        "duration_after_gather_through_uncompute": 2 * (4 + 8 + 8 + 4) + 8,
    }


def select(state, plane, orientation):
    contact(state)
    out = Counter()
    for k, v in state.items():
        target = k
        if 3 <= k[5] < 7:
            j = 3 if plane == "A" else 4
            target = set_field(set_field(k, 2, 1 - k[2]), j, 1 - k[j])
            v *= orientation * (1 - 2 * k[j])
        elif k[5] == 7:
            target = set_field(k, 6, 1 - k[6])
        out[target] += v
    return compact(out)


def block(state, plane, orientation):
    contact(state)
    for mask in (1, 2, 4):
        state = excursion(hbit(state, 5, mask), 1)
    state = excursion(select(state, plane, orientation), 1)
    for mask in (4, 2, 1):
        state = excursion(hbit(state, 5, mask), 1)
    return state


def ideal_numerator(src, plane, orientation):
    out = Counter()
    j = 3 if plane == "A" else 4
    for k, v in src.items():
        out[k] += 3 * v
        out[set_field(set_field(k, 2, 1 - k[2]), j, 1 - k[j])] += 4 * orientation * (1 - 2 * k[j]) * v
    return compact(out)


def delivered(src, plane, orientation, save):
    state = block(src, plane, orientation)
    assert block(state, plane, -orientation) == {k: 64 * v for k, v in src.items()}
    good = {k: v for k, v in state.items() if k[5] == k[6] == 0}
    good = excursion(good, 1)
    assert good == ideal_numerator(src, plane, orientation)
    assert norm(state) == 64 * norm(src) and norm(good) == 25 * norm(src)
    bins = Counter()
    for k, v in state.items():
        bins[k[5], k[6]] += v * v
    return good, [
        [l, j, str(F(bins[l, j], 64 * norm(src)))] for l in range(8) for j in range(2)
    ] if save else []


def launch(rail, blankA, blankB, D):
    direction = 1 - 2 * rail
    initial = {
        (-D * direction, D * direction, rail, i, j, 0, 0, 0): u * v
        for i, u in enumerate(blankA)
        for j, v in enumerate(blankB)
        if u * v
    }
    state = transport(initial, D, False)
    contact(state)
    return state


def echo(src, plane, orientation, read_sign, L, tag, save):
    scattered, first = delivered(src, plane, orientation, save)
    separated = transport(scattered, L, False)
    bins = Counter()
    for k, v in separated.items():
        bins[k[0], k[1]] += v * v
    if tag:
        separated = {set_field(k, 7, k[7] ^ k[2]): v for k, v in separated.items()}
    # No nonlocal encounter during this interval: fixed mirrors act on each
    # walker separately. Reverse both rails, stream back, restore incidence.
    turned = transport(separated, 0, True)
    home = transport(turned, L, True)
    contact(home)
    if tag == "erased":
        home = {set_field(k, 7, k[7] ^ k[2]): v for k, v in home.items()}
    recombined, second = delivered(home, "B", read_sign, save)
    same = next(iter(src))[2]
    mass = F(sum(v * v for k, v in recombined.items() if k[2] == same), norm(recombined))
    base = F(337, 625)
    predicted = (
        base if tag == "retained" else base - F(288, 625) * orientation * read_sign * grade_expect(src)
    )
    assert mass == predicted
    return mass, {
        "outward_separated_position_probabilities": [
            [*p, str(F(v, norm(scattered)))] for p, v in sorted(bins.items())
        ],
        "first_gate_index_junk_probabilities": first,
        "second_gate_index_junk_probabilities": second,
        "return_probability_given_two_passes": str(mass),
        "complete_success_port_weights": [
            [*k, str(F(v * v, norm(recombined)))] for k, v in sorted(recombined.items())
        ]
        if save
        else None,
    }


def main():
    rows = []
    for rail in (0, 1):
        for name, B in (("blank", (1, 0)), ("occupied", (0, 1)), ("unknown", (2, -1))):
            src = launch(rail, (2, -1), B, 3)
            for method in ("none", "anchored", "positive", "negative", "negative_corrected"):
                if method == "none":
                    state = src
                    p = F(1)
                elif method == "anchored":
                    state = anchored(src)
                    p = F(1)
                    assert grade_expect(state) == F(B[0] * B[0] - B[1] * B[1], B[0] * B[0] + B[1] * B[1])
                else:
                    g = 1 if method == "positive" else -1
                    state = grade_projection(src, g)
                    p = F(norm(state), 4 * norm(src))
                    assert p == F(1, 2) and grade_expect(state) == g
                    if method == "negative_corrected":
                        state = excursion(applyBflip(state), 1)
                        assert grade_expect(state) == 1
                for orientation, read_sign, tag in (
                    (1, -1, None),
                    (1, 1, None),
                    (-1, -1, None),
                    (1, -1, "retained"),
                    (1, -1, "erased"),
                ):
                    detailed = name == "blank" and method in {"anchored", "negative"}
                    mass, details = echo(state, "A", orientation, read_sign, 4, tag, detailed)
                    row = {
                        "input_rail": rail,
                        "initial_B": name,
                        "orientation_procedure": method,
                        "orientation_probability": str(p),
                        "grade_mean": str(grade_expect(state)),
                        "imaginary_scatter_sign": orientation,
                        "held_B_analyzer_sign": read_sign,
                        "path_record": tag,
                        "two_gate_pass_probability": "625/4096",
                        "first_gate_fail_probability": "39/64",
                        "second_first_fail_probability": "975/4096",
                        "joint_good_named_return": str(p * F(625, 4096) * mass),
                    }
                    row.update(details)
                    rows.append(row)
    blank = launch(0, (1, 0), (1, 0), 3)
    aligned = anchored(blank)
    early = ideal_numerator(ideal_numerator(aligned, "A", 1), "B", -1)
    late = anchored(ideal_numerator(ideal_numerator(blank, "A", 1), "B", -1))
    assert F(sum(v * v for k, v in early.items() if k[2] == 0), norm(early)) == 1
    assert F(sum(v * v for k, v in late.items() if k[2] == 0), norm(late)) == F(337, 625)
    # Measured Q and corrected Z_B commute/intertwine with an A-only
    # scatter: alignment may occur after S_A but before the B analyzer.
    pre = applyBflip(grade_projection(ideal_numerator(blank, "A", 1), -1))
    post = ideal_numerator(applyBflip(grade_projection(blank, -1)), "A", 1)
    assert pre == post
    return {
        "cases": rows,
        "coherent_all_grade_alignment": entangled_test(),
        "time_order": {
            "alignment_before_echo_return": "1",
            "alignment_after_both_gates_return": "337/625",
            "negative_feedforward_after_scatter_before_B_read_matches_early": True,
        },
        "schedule": {
            "launch_each_distance": 3,
            "outer_mirror_radius": 4,
            "stream_ticks_per_contact_slot": 2,
            "Walsh_SELECT_Walsh_slots": 7,
            "pass_or_fail_projection_slots": 1,
            "scatter_read_total_ticks_with_two_pass_checks": 32,
            "positive_or_negative_grade_check_slots": 4,
            "negative_Z_feedforward_extra_slots": 1,
            "blank_anchor_slots": 2,
            "common_wall_clock_pair_grade_correction_slots": 5,
            "total_ticks_blank_anchor_including_launch_and_outer_excursion_and_final_gate_check": 47,
            "total_ticks_grade_mode_with_padded_feedback_including_launch_and_outer_excursion_and_final_gate_check": 53,
        },
        "scope": "Two distinguishable counterstreaming walkers start at opposite sites, with incidence RL or LR. In the origin interaction region clean local computational modes carry the index, flag and blank reference. On each contact slot apply the scheduled gate then depart by one site, reflect on each side and return to the origin on the next tick. Invert both rails on arrival before the next gate. A pass check can use an identical shuttle; its projection commutes with the common return. The total includes one 2-tick shuttle after every pass read and an idle such shuttle on the positive grade route to equalize feedback clocks. Real signed permutations/Hs and a classical schedule are extra apparatus. This model uses repeated strictly moving nearby recollisions, rather than an instantaneous irrational or rational scattering primitive on the bare free walk.",
        "scattering": "On success S_R=(3I+4 X_incidence J_R)/5 is a real orthogonal realization of a relative imaginary reflection amplitude. An accepted Walsh block has numerator 3I+4XJ_R over 8 so P=25/64 on every normalized input. Coarse failure words are retained as first/second failed gate probabilities; detailed failure-index diagnostics are alternative reads and are unnecessary to the accepted record. Each two-gate attempt has success 625/4096; output ports are reported both conditional and joint with the contact record. The check verifies the actual transpose S block uncomputes the full SELECT dilation. A retry schedule is not used.",
        "alignment": "The deterministic blank isometry is H_B then B=1-controlled (-J_A). For any parent v it maps v tensor 0 to (v tensor 0 - J_A v tensor 1)/sqrt(2), in Q=−J_AJ_B grade +. It is a full reversible unitary whose other child coordinate maps to grade −; it does not reset arbitrary loaded data. The joint Q meter and physical B-plane reflection align independent planes when both grades are included, with possible conjugation of already encoded B data and need for sheet reflection if a B sheet must remain calibrated. One contact record contains no absolute chirality label.",
        "fringe": "The outer mirrors preserve both signed histories, return them to the origin, and a known rail relabel restores the incidence basis. A held B analyzer S_B^dagger then recombines. The same-incidence numerator is 9I+16Q, with conditional return (337+288<Q>)/625. Opposite grades produce 1 and 49/625, independent grades averaged give 337/625. A persistent record of the outward position/route gives 337/625 on all grades, and coherent erasure restores the fringe. Observation of free-separated transmission/reflection alone is 9/25 versus 16/25 for both imaginary signs. Late alignment after both interactions cannot change already formed incidence populations. An ideal A-only scatter commutes with the contact grade and B correction, so alignment after this scatter and before a coherent B read can recover the signal. These are predictions of the real apparatus and its squared rule; no absolute external imaginary unit, generic empirical collision law, or arbitrary causal speed is inferred.",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    directory = parser.parse_args().directory
    result = main()
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "collision_phase_reference.json").write_bytes(
        (json.dumps(result, separators=(",", ":")) + "\n").encode()
    )
    print(len(result["cases"]), "signed contact, transport and Ramsey controls.")
