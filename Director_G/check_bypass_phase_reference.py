"""M=8 coherent bypass, synchronized spectator, and a calibrated relative delay.

Run python -B check_bypass_phase_reference.py OUTPUT_DIRECTORY.
"""

import argparse
import cmath
import json
from fractions import Fraction as F
from math import cos, pi, sqrt
from pathlib import Path

LAYER_PAIRS = (((0, 4),), ((0, 2), (4, 6)), ((2, 1), (6, 5)))
PLACEMENT = ((0, 0, 1), (4, 4, -1), (2, 1, 1), (1, 3, -1), (6, 5, -1), (5, 7, 1))


def circuit(sign, phase, fill, tag_deep=False):
    """Either split the idle spectator (integer circuit), or apply its idle phase."""
    state = {(0, 0): 1}
    ntag = 2
    for t, pairs in enumerate(LAYER_PAIRS, 1):
        edges = {y for pair in pairs for y in pair}
        after = {}
        for left, right in pairs:
            for marker in range(ntag):
                l = state.get((left, marker), 0)
                r = state.get((right, marker), 0)
                for y, v in ((left, l + r), (right, l - r)):
                    dst = marker ^ int(tag_deep and t == 3)
                    after[y, dst] = sign * v if fill else sign * v / sqrt(2)
        for y in set(range(8)) - edges:
            if fill:
                l, r = (state.get((y, z), 0) for z in range(2))
                after[y, 0] = sign * (l + r)
                after[y, 1] = sign * (l - r)
            else:
                for z in range(2):
                    after[y, z] = phase * state.get((y, z), 0)
        state = {p: v for p, v in after.items() if v}
    return {
        (dst, z): sign * v for src, dst, sign in PLACEMENT for (y, z), v in state.items() if y == src
    }


def comparator(state, sign, stride, exact):
    # Full balanced H once before and once after a translation on arm 1.
    # State uses integer numerators in exact mode, normalized complex entries
    # otherwise. Here all three outcomes are addressed directly at the end.
    split = {p: sign * v for p, v in state.items()}
    final = {}
    for y in range(8):
        for z in range(2):
            v = split.get((y, z), 0)
            w = split.get(((y - stride) % 8, z), 0)
            for s in (1, -1):
                raw = sign * (v + s * w)
                final[s, y, z] = F(raw * raw, 32) if exact else abs(raw) ** 2 / 4
    assert abs(float(sum(final.values())) - 1) < 2e-12
    return final


def grouped(port):
    return [sum(v for (s, _, z), v in port.items() if s == 1 and z == j) for j in (0, 1)]


def synchronized():
    rows = []
    for tag in (False, True):
        plus = circuit(1, 1, True, tag)
        minus = circuit(-1, 1, True, tag)
        assert minus == {p: -v for p, v in plus.items()}
        for stride in range(8):
            law = comparator(plus, 1, stride, True)
            assert law == comparator(minus, -1, stride, True)
            bright = grouped(law)
            denom = [sum(v for (_, _, z), v in law.items() if z == j) for j in (0, 1)]
            if stride == 1:
                assert sum(bright) == F(3, 4)
                assert bright[tag] / denom[tag] == F(5, 6) and bright[not tag] / denom[not tag] == F(
                    1, 2
                )
            rows.append(
                {
                    "tag_deep_flip": tag,
                    "stride": stride,
                    "bright_by_marker": list(map(str, bright)),
                    "marker_probabilities": list(map(str, denom)),
                    "all_bits_plus_sheet_marker_probability": [
                        [s, y, z, str(v)] for (s, y, z), v in law.items()
                    ],
                }
            )
    # Marking the two source depths orthogonally after synthesis gives 1/2.
    marked = {(y, z): v for (y, _), v in circuit(1, 1, False).items() for z in (int(y % 2 == 0),)}
    assert abs(sum(grouped(comparator(marked, 1, 1, False))) - 0.5) < 1e-12
    return rows


def interferometer(phase, sign, cal_sign=1):
    # On a separate balanced interferometer, the upper arm is explicitly
    # assigned the calibrated delay. Its use assumes the same differential
    # transfer as the one inferred for the installed idle arm.
    lo, hi = sign / sqrt(2), cal_sign * phase * sign / sqrt(2)
    bright = abs(sign * (lo + hi) / sqrt(2)) ** 2
    assert abs(bright - (1 + cal_sign * phase.real) / 2) < 1e-12
    return bright


def partial(state, theta, orientation):
    # The marker of the shallow even sites is |0>; deep odd sites carry
    # cos(theta)|0>+sin(theta)|1>, now with a complete unseen marker.
    marker = (cos(theta), cmath.sin(theta).real)
    out = {}
    for (y, z), v in state.items():
        assert not z
        for j, w in enumerate(marker if y % 2 else (1, 0)):
            out[y, j] = v * w * (orientation if y % 2 else 1)
    return out


def phase_rows():
    rows = []
    mx = 0.0
    for angle in (0, pi / 3, pi / 2, pi):
        phase = cmath.exp(1j * angle)
        for theta in (0, pi / 3, pi / 2):
            for sign in (1, -1):
                ref = circuit(sign, phase, False)
                other = circuit(-sign, -phase, False)
                assert all(
                    abs(ref.get(p, 0) + other.get(p, 0)) < 1e-12 for p in ref.keys() | other.keys()
                )
                for orientation in (1, -1):
                    state = partial(ref, theta, orientation)
                    alt = partial(other, theta, orientation)
                    for d in range(8):
                        ports = comparator(state, sign, d, False)
                        twin = comparator(alt, -sign, d, False)
                        mx = max(mx, max(abs(ports[p] - twin[p]) for p in ports))
                        z = 2 * sum(grouped(ports)) - 1
                        expected = cos(pi * d / 4) * (
                            sign * orientation * cos(theta) * cos(angle) if d % 2 else 1
                        )
                        assert abs(z - expected) < 2e-12
                    D = interferometer(phase, sign)
                    twin_D = interferometer(-phase, -sign)
                    rows.append(
                        {
                            "H_sign": sign,
                            "idle_angle_over_pi": angle / pi,
                            "marker_angle_over_pi": theta / pi,
                            "extra_odd_sign": orientation,
                            "unit_stride_bright": sum(grouped(comparator(state, sign, 1, False))),
                            "independently_addressed_delay_bright": D,
                            "gauge_twin_delay_bright": twin_D,
                        }
                    )
    assert mx < 2e-12
    return rows, mx


def sign_noise():
    rows = []
    for p in (F(), F(1, 4), F(1, 2), F(3, 4), F(1)):
        u = 2 * p - 1
        for sign in (1, -1):
            # E[S1 S2] on a fresh pair of bypass runs, using the same
            # random sign, independent signs, or opposite signs.
            products = {}
            sensor = {}
            for coupling in ("shared", "independent", "opposite"):
                e = F()
                sensor_coefficient = F()
                for g in (1, -1):
                    pg = p if g == 1 else 1 - p
                    for h in (1, -1):
                        ph = (
                            (p if h == 1 else 1 - p)
                            if coupling == "independent"
                            else F(h == (g if coupling == "shared" else -g))
                        )
                        e += pg * ph * F(sign * g * sign * h, 2)
                        sensor_coefficient += pg * ph * g * sign * h
                products[coupling] = e
                sensor[coupling] = sensor_coefficient
            assert products == {"shared": F(1, 2), "independent": u * u / 2, "opposite": F(-1, 2)}
            assert sensor == {"shared": sign, "independent": sign * u * u, "opposite": -sign}
            # A separately installed matched-path phase sensor, with same
            # sign error per shot, can report S_D=g exactly for real ±1.
            # Then E[S_D S] = sign/sqrt(2) even for a fair sign.
            rows.append(
                {
                    "plus_phase_probability": str(p),
                    "H_sign": sign,
                    "mean_unit_contrast_coefficient_of_1_over_sqrt2": str(sign * u),
                    "two_bypass_sign_product": {k: str(v) for k, v in products.items()},
                    "phase_sensor_times_bypass_in_units_of_1_over_sqrt2": {
                        k: str(v) for k, v in sensor.items()
                    },
                }
            )
    return rows


def main():
    phases, mx = phase_rows()
    return {
        "synchronized_complete_integer_controls": synchronized(),
        "unequal_depth_phase_controls": phases,
        "max_coordinate_probability_discrepancy_of_gauge_twins": mx,
        "classical_sign_couplings": sign_noise(),
        "robustness": "For fixed unit-shift contrast with |Re(Gamma)|>=v and known sign of Re(Gamma), the predicted plus laws have TV at least v/sqrt(2). Circle intervals of per-model absolute plus-rate uncertainty eta are disjoint if 2eta<v/sqrt(2). With iid fresh preparations, no systematic error, and a held phase sign, thresholding the sample mean of S at zero has one-sided error <=exp(-n v²/4). Neither a port threshold nor this iid rate applies without phase calibration, or to unmodeled common run-to-run drifts.",
        "no_go": "On any finite coordinate transcript H->-H multiplies every retained physical amplitude by (-1)^t when each coherent history has t Hadamards, including the reference, apparatus and calibrator. Initial integer coordinates up to a scalar, signed permutations and coordinate masks preserve integer numerators; complete cylinder probabilities, conditioning and positive coarse graining are rational and identical. Different classical adaptive branches can have different t. This extends to equal parity of H depths after clearing dyadic denominators. A locally referenced approximate phase prepared by such coordinates obeys the same no-go when records include the reference.",
        "gauge": "Treat the black-box bypass at a layer as U(sigma,phi)=diag(sigma H,exp(i phi) I) on the addressed subspaces. The simultaneous change (sigma,phi)->(-sigma,phi+pi) sends U to -U and full H to -H. Any fixed invocation on the whole state has a common sign; arbitrary coordinate routing, feedback, tomography, fresh copies or same-machine calibration made only from this menu preserve every transcript. A further coherently controlled invocation that can itself be skipped needs a separately specified phase. A classical random common sign can also be latent across repeated trials.",
        "visibility": "For the original physical M=8 placement, let Gamma be the complex normalized shallow/deep marker overlap including phase. For odd strides E[S|d]=sigma Re(Gamma) cos(pi d/4); for even d it is cos(pi d/4). A known positive Re(Gamma)>=v gives opposite unit-stride predictions separated by >=v/sqrt(2) in plus probability. Re(Gamma)=0 makes all those unit-stride means 1/2. Complete orthogonal labels erase the interference; a purely imaginary Gamma has zero real contrast for these real reads. Populations alone do not measure the overlap. A single global field embedding conjugates all supplied algebraic gates; here the nuisance phase is an independently variable physical parameter.",
        "synchronized_control": "Supply a fresh spectator bit and H-pair every otherwise idle mode on it at each matched layer. Numerator depth three for all modes. Even shallow sites end with spectator (0+1)/sqrt(2), odd deep sites carry 0. For T the unconditional bright probability is 3/4 under either embedding, marker-zero yield 3/4 and conditional bright 5/6. These are properties of the synchronized integer ensemble including its calibrator. A permanent deep marker of the original bypass versus orthogonal shallow marker gives 1/2.",
        "phase_test": "Additional calibrated gate diag(1,exp(i phi)) on two equal-H-depth reference paths gives plus probability (1+cos(phi))/2, independent of sigma. If this separately addressable sensor is validated to have the same phase as the bypass and the route-marker overlap is real, known and positive, its contrast and the unit-stride bypass contrast give a relative sign when cos(phi) differs from zero. An interpretation as an embedding test needs an independently held acted/idle phase and a held physical T. Without establishing phase transfer or visibility the nuisance can absorb the sign. A reference can be on the same machine; no supplied empirical comparison is asserted.",
        "source_context": [
            "Finite_clock_purity.md",
            "Native_preparations_and_probability_embeddings.md",
            "check_clock_galois_support.py",
        ],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    directory = parser.parse_args().directory
    result = main()
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "bypass_phase_reference.json").write_text(
        json.dumps(result, separators=(",", ":")) + "\n", encoding="utf8"
    )
    print(
        len(result["synchronized_complete_integer_controls"]),
        "exact controls;",
        len(result["unequal_depth_phase_controls"]),
        "phase/marker settings.",
    )
