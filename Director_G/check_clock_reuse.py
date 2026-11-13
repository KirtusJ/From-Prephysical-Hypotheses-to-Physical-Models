"""Check repeated experimental reads using one physical cyclic clock.

Run python -B check_clock_reuse.py results. Every probability below uses
fractions of integer path weights. Neither Fourier orientation is sampled
in the physical-coordinate calculation.
"""

import argparse
import json
from collections import Counter
from fractions import Fraction as F
from math import comb
from pathlib import Path


def translate(v, offset):
    return tuple(v[(j - offset) % len(v)] for j in range(len(v)))


def norm(v):
    return sum(a * a for a in v)


def probe(v, offset, sign):
    """Unsigned scalar 1/2 omitted: H, path-controlled translation, H."""
    return tuple(a + sign * b for a, b in zip(v, translate(v, offset)))


def full_tree(vector, offsets, adapt):
    records = {(): vector}
    for t, offset in enumerate(offsets):
        children = {}
        for history, v in records.items():
            d = offset if not adapt or not history or history[-1] == 1 else 0
            for sign in (1, -1):
                child = probe(v, d, sign)
                if any(child):
                    children[history + (sign,)] = child
        records = children
        assert sum(norm(v) for v in records.values()) == norm(vector) * 4 ** (t + 1)
    return {key: F(norm(v), norm(vector) * 4 ** len(offsets)) for key, v in records.items()}


def tv(a, b):
    return sum(abs(a.get(k, 0) - b.get(k, 0)) for k in a.keys() | b.keys()) / 2


def record_tests():
    # On this four-cycle T^2=-I in k=+-1 and T^2=+I in k=0.
    # A unit-shift interference read instead gives different, overlapping laws.
    good = (1, 0, -1, 0)  # exactly the k=+-1 plane
    bad = (1, 1, 1, 1)  # k=0
    initial = tuple(4 * a + b for a, b in zip(good, bad))
    wrong = F(norm(bad), norm(initial))
    assert wrong == F(1, 9)
    trials = []
    for count in (1, 2, 4, 8, 10):
        for adaptive in (False, True):
            settings = [1] * (count - 1) + [2] if adaptive else [1] * count
            actual = full_tree(initial, settings, adaptive)
            pure = full_tree(good, settings, adaptive)
            nuisance = full_tree(bad, settings, adaptive)
            combined = {
                key: (1 - wrong) * pure.get(key, 0) + wrong * nuisance.get(key, 0)
                for key in pure.keys() | nuisance.keys()
            }
            assert actual == combined and tv(actual, pure) <= wrong
            row = {
                "number": count,
                "initial_offsets": settings,
                "zero_current_setting_if_previous_minus": adaptive,
                "coherent_integer_tree_nonzero_histories": len(actual),
                "joint_TV_to_all_good": str(tv(actual, pure)),
            }
            if not adaptive:
                accepted = actual[(1,) * count]
                posterior = wrong / accepted
                assert accepted == wrong + (1 - wrong) * F(1, 2) ** count
                mean = (1 - wrong) / 2 + wrong
                # Independent fresh clocks have the same per-trial marginal mean.
                frequency = Counter()
                for history, probability in actual.items():
                    frequency[history.count(1)] += probability
                mean_by_tree = sum(F(k, count) * q for k, q in frequency.items())
                assert mean_by_tree == mean
                assert tv(actual, pure) == wrong * (1 - F(1, 2) ** count)
                var = sum((F(k, count) - mean) ** 2 * q for k, q in frequency.items())
                assert var == (1 - wrong) / (4 * count) + wrong * (1 - wrong) / 4
                fresh = {
                    k: F(comb(count, k)) * mean**k * (1 - mean) ** (count - k) for k in range(count + 1)
                }
                row.update(
                    {
                        "shared_count_distribution": [str(frequency[k]) for k in range(count + 1)],
                        "same_single_shot_mean_shared_and_fresh": str(mean),
                        "shared_sample_mean_variance": str(var),
                        "fresh_sample_mean_variance": str(mean * (1 - mean) / count),
                        "TV_shared_vs_refreshed_counts": str(tv(dict(frequency), fresh)),
                        "rare_all_plus_joint": str(accepted),
                        "wrong_given_all_plus": str(posterior),
                        "joint_TV_formula_verified": tv(actual, pure) == wrong * (1 - F(1, 2) ** count),
                    }
                )
            trials.append(row)
    cap = 6
    records = full_tree(initial, [2] * cap, False)
    assert records == {(-1,) * cap: 1 - wrong, (1,) * cap: wrong}
    return {
        "clock_size": 4,
        "good_clock": good,
        "bad_clock": bad,
        "input_counts": initial,
        "wrong_fraction": str(wrong),
        "unit_shift_bright_good": "1/2",
        "unit_shift_bright_bad": "1",
        "trials": trials,
        "strong_marker_control": {
            "shift": 2,
            "number": cap,
            "shared_all_minus": str(1 - wrong),
            "shared_all_plus": str(wrong),
            "shared_TV_to_ideal": str(wrong),
            "fresh_TV_to_ideal": str(1 - (1 - wrong) ** cap),
        },
    }


def tensor_test():
    # Ordinary eight-cycle. (1,0,0,0,-1,0,0,0) is supported on *all*
    # odd k, not purely low. Use an M=4 cosine eigenplane for a literal
    # exact zero-contamination example, or embed it as a period-4 wave in M=8.
    v = (1, 0, -1, 0)
    w = translate(v, 1)
    assert sum(a * b for a, b in zip(v, w)) == 0
    states = {}
    # Product basis ordered as |A B>. With a shared clock, translations add.
    # With refreshed clocks they act on distinct tensor factors.
    for reuse in (False, True):
        state = {}
        for a in (0, 1):
            for b in (0, 1):
                if reuse:
                    for j, n in enumerate(translate(v, a + b)):
                        state[a, b, j] = n
                else:
                    for i, p in enumerate(translate(v, a)):
                        for j, q in enumerate(translate(v, b)):
                            state[a, b, 4 * i + j] = p * q
        den = norm(state.values())
        end = 4 if reuse else 16
        reduced = [
            [
                F(sum(state[a // 2, a % 2, j] * state[b // 2, b % 2, j] for j in range(end)), den)
                for b in range(4)
            ]
            for a in range(4)
        ]
        # Bell measurement by physical integer differences/sums. Its two
        # negative-Y⊗Y eigenvectors are Phi+ and Psi-.
        bell = {}
        for label, x, y, sign in [
            ("Phi+", 0, 3, 1),
            ("Phi-", 0, 3, -1),
            ("Psi+", 1, 2, 1),
            ("Psi-", 1, 2, -1),
        ]:
            bell[label] = (reduced[x][x] + reduced[y][y] + 2 * sign * reduced[x][y]) / 2
        assert sum(bell.values()) == 1
        states["retained" if reuse else "refreshed"] = {
            "two_qubit_reduced": [[str(q) for q in row] for row in reduced],
            "real_Bell_law": {k: str(p) for k, p in bell.items()},
            "positive_Y_tensor_Y": str(bell["Phi-"] + bell["Psi+"]),
        }
    assert states["retained"]["positive_Y_tensor_Y"] == "1"
    assert states["refreshed"]["positive_Y_tensor_Y"] == "1/2"
    # Per complete flight fresh |+>, use controlled T once and discard base.
    # Target orientation populations stay fixed; off-diagonal overlap falls
    # by |(1+e^(2 i h))/2|=|cos(h)| each time. At h=pi/2 it vanishes once.
    clock = [[F(v[i] * v[j] + w[i] * w[j], 2 * norm(v)) for j in range(4)] for i in range(4)]
    purity = sum(q * q for row in clock for q in row)
    fidelity = sum(F(v[i] * v[j], norm(v)) * clock[i][j] for i in range(4) for j in range(4))
    assert fidelity == purity == F(1, 2)
    # Pure eigenprogram z_j=i^j: one conditional translation is -i z
    # at every physical coordinate. A product is preserved for arbitrary path
    # amplitudes, unlike the pure standing-wave program above.
    z = (1, 1j, -1, -1j)
    assert translate(z, 1) == tuple(-1j * a for a in z)
    return {
        "clock_size": 4,
        "initial_exact_conjugate_plane": [1, 0, -1, 0],
        "flight": "Fresh |+> path and controlled one-cell T. An independent oriented quadrature "
        "is unnecessary for the final joint Bell measurement: it is a real signed basis.",
        "after_one_flight_clock_purity": str(purity),
        "fidelity_with_initial_standing_wave": str(fidelity),
        "both_single_base_reduced": "I/2",
        "clock_coord_probabilities_if_initial": ["1/2", "0", "1/2", "0"],
        "clock_coord_probabilities_after_one": ["1/4"] * 4,
        "single_coordinate_read_TV_before_vs_after": "1/2",
        "oriented_exact_character_factorizes": True,
        "two_flight_control": states,
        "joint_TV_retained_vs_refreshed_real_Bell": "1/2",
        "qualification": "At order 8, applying T^2 on the abstract exact k=+-1 plane has the "
        "same pi/2 conditional phase. Literal integer tests use order 4. "
        "The addition of a comparator retaining both emitted qubits changes "
        "the allowed observation. For signed real per-flight readouts the two "
        "orientations have identical conditional laws.",
    }


def gauge_obstruction():
    # Same base site AND incoming direction at the end: the extra shared
    # right step closes the diagram even for a direction-dependent gauge.
    a = 3
    m = 128
    side = 32

    def path(word):
        x, c = 0, 1
        cells = [(x, c)]
        gains = []
        for d in word:
            gains.append(x)
            x, c = (x + d) % side, d
            cells.append((x, c))
        return cells, gains

    first = (1,) * a + (-1,) * a + (1,)
    second = tuple(-d for d in first[:-1]) + (1,)
    asites, agains = path(first)
    bsites, bgains = path(second)
    # Use the line representative x in (-side/2,side/2), keeping the
    # native g(x)=x with identical centre on the two short paths.
    agains = [x if x < side // 2 else x - side for x in agains]
    bgains = [x if x < side // 2 else x - side for x in bgains]
    assert asites[0] == bsites[0] and asites[-1] == bsites[-1]

    def gauge(t, site):
        x, c = site
        return (3 * t * x + 2 * t * t + x * x + (t + 1) * c) % m

    def transformed(sites, gains):
        return [(g + gauge(t, sites[t]) - gauge(t + 1, sites[t + 1])) % m for t, g in enumerate(gains)]

    old = (sum(agains) - sum(bgains)) % m
    after = (sum(transformed(asites, agains)) - sum(transformed(bsites, bgains))) % m
    assert old == after == 2 * a * a and old <= m // 2
    assert old > 2 * len(first)
    return {
        "clock_size": m,
        "duration": len(first),
        "two_direction_histories": [first, second],
        "common_initial_and_final_base_modes": [asites[0], asites[-1]],
        "native_departure_sums": [sum(agains), sum(bgains)],
        "cyclic_holonomy_distance_before_and_after_position_time_gauge": old,
        "maximum_difference_if_all_physical_shifts_have_speed_one": 2 * len(first),
        "general": "Take R^a L^a R and L^a R^a R on a line with g(x)=x. Both go from "
        "(0,R) to (1,R) in 2a+1 steps with gain sums +/-a^2. Every time-,site-, "
        "and direction-dependent translation of the local sheet frame telescopes "
        "between the same endpoints. For M>4a^2 the cycle distance of 2a^2 "
        "exceeds 2v(2a+1) when a is large enough for any fixed v. There is then "
        "no such gauge making the exact whole lift bounded-speed in one tick per base step. "
        "This tests the exact transport, not a lower bound on observed coarse probabilities, "
        "a separate simulator, or an arbitrarily selected force packet.",
    }


def main():
    return {
        "record_mixture": "A clock-blind instrument diagonal in Fourier label k has Kraus blocks "
        "K_h(k) for every finite transcript. With independent fresh raw inputs, tracing the "
        "clock gives P(h)=sum_k w_k P_k(h), including common history-dependent choices. If "
        "the good blocks have the same complete record law Q, joint TV(P,Q)<=e for any n. "
        "One must specify Q under the same adaptive policy. If ideal products with fresh "
        "random orientations are requested, good-sector equality for single marginals alone "
        "does not establish that comparison. Classical labels are a sampling representation.",
        "homogeneous_integer_examples": record_tests(),
        "real_memory_control": tensor_test(),
        "moving_frame_signed_loop": gauge_obstruction(),
        "no_broadcast_scope": "For a unitary preserving each of two pure programs c,d uncorrelated "
        "while starting a target in the same pure input, inner-product conservation gives "
        "<c|d>=<c|d><out_c|out_d> (up to phase). Thus distinguishable pure outputs require "
        "orthogonal program states. Exactly distinct character programs are orthogonal: there "
        "is no such obstruction to their repeated controlled translations. For an arbitrary "
        "family of noncommuting programs one cannot infer a universal independent copy. A "
        "dephased orientation mixture may keep its own marginal exactly yet correlate all signals.",
        "bounds_and_costs": "For independently prepared real bases and individual clock-blind "
        "real records the good orientation laws coincide even for common adaptive feedback. "
        "If eta is the per-flight comparison error to a continuum law, using the same good "
        "clock for n independent ideal flights gives joint error <=e+n eta (or the sum of "
        "uniform conditional errors under feedback). Mean frequency error per flight is at "
        "most e+eta. A rare final herald E may increase the wrong posterior by up to e/P(E). "
        "Reuse lowers amortized setup only: an expected O(M r) preparation at tau per tick "
        "costs O(r/delta) mechanical time and O(r/(n delta)) per flight in the cited force "
        "scaling. The first usable clock still has its original causal latency. Correlated "
        "product-transcript estimates use e+n eta. To make both available upper bounds vanish "
        "one needs n delta/r -> infinity and n eta -> 0, feasible when r eta / delta -> 0. "
        "A convergence theorem with no quantitative rate does not give this tradeoff. "
        "Flights sharing a clock cannot be counted as independent calibrations. A translation of the support "
        "centre, even if record-dependent, does not change the sharp arc spectral bound. "
        "Sequential reuse assumes all flights can couple to this same physical register. "
        "Local travel, transport delay, and concurrent geographical copies require a separate "
        "physical account. This checker does not implement long-range couplings or new units.",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()
    out = main()
    args.directory.mkdir(parents=True, exist_ok=True)
    (args.directory / "clock_reuse.json").write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(
        "Verified",
        len(out["homogeneous_integer_examples"]["trials"]),
        "complete transcript comparisons and the two real Bell controls.",
    )
