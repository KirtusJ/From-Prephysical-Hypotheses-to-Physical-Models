"""Print the exact three-well predictions for the proposed cesium phase comparison.

Run python Director_G/check_three_well_phase.py. Uses only the standard library.
"""
from fractions import Fraction as F
from itertools import product
import json


WELLS = (-2, -1, 0, 1, 2)


def require(ok, message):
    if not ok:
        raise ValueError(message)


def terminal_amplitudes():
    """Signed word sums indexed by terminal well, final spin and first arm."""
    ports = {(j, spin, arm): 0 for j in WELLS for spin in (0, 1) for arm in (0, 1)}
    for word in product((0, 1), repeat=4):
        j = sum(word) - 2
        negative_factors = sum(a == b == 1 for a, b in zip((0,) + word, word))
        ports[j, word[-1], word[0]] += (-1)**negative_factors
    return ports


def site_law(ports, left_weight, real_coherence):
    """Propagate a unit-trace two-arm density matrix through the last three steps."""
    require(0 <= left_weight <= 1 and real_coherence**2 <= left_weight*(1-left_weight),
            "unphysical arm population or real off-diagonal entry")
    mass = {}
    for j in WELLS:
        value = F(0)
        for spin in (0, 1):
            left, right = (ports[j, spin, arm] for arm in (0, 1))
            value += (left_weight*left**2 + (1-left_weight)*right**2
                      + 2*real_coherence*left*right)
        mass[j] = value/8
    require(sum(mass.values()) == 1 and min(mass.values()) >= 0, "endpoint law")
    return mass


def measured(law, efficiency, brightness):
    return {j: brightness*efficiency[j]*law[j] for j in WELLS}


def positions(row, left, right):
    """Locate the joint row between sharp-arm reference odds at two wells."""
    result = []
    for j in (-2, -1):
        l, r, s = (setting[j]/setting[0] for setting in (left, right, row))
        require(l != r, "sharp odds coincide")
        result.append((s-r)/(l-r))
    return tuple(result)


def run():
    ports = terminal_amplitudes()
    half = F(1, 2)
    left = site_law(ports, 1, 0)
    right = site_law(ports, 0, 0)
    require([list(law.values()) for law in (left, right)] ==
            [[F(k, 8) for k in row] for row in [(1, 5, 1, 1, 0), (0, 1, 1, 5, 1)]],
            "sharp arm laws or physical orientation")
    gains = [
        dict.fromkeys(WELLS, F(1)),
        dict(zip(WELLS, (F(1, 7), F(5, 6), F(1, 3), F(2, 5), F(3, 4)))),
        dict(zip(WELLS, (F(3, 4), F(1, 9), F(7, 8), F(2, 7), F(1, 10)))),
    ]
    tested = dict(balanced_phases=0, varying_arm_mixtures=0, real_unequal_or_sharp_inputs=0)
    for efficiency in gains:
        ref_left = measured(left, efficiency, F(23, 8))
        ref_right = measured(right, efficiency, F(5, 21))
        for i in range(17):
            w, t = F(i, 16), F(i-8, 8)
            brightness = F(13+i, 5+i)
            joint = site_law(ports, half, t/2)
            require([16*joint[j] for j in WELLS] == [1, 6+4*t, 2, 6-4*t, 1],
                    "balanced five-well prediction")
            coords = positions(measured(joint, efficiency, brightness), ref_left, ref_right)
            require(coords == (half, (1+t)/2), "invariant phase positions")
            tested["balanced_phases"] += 1
            mixture = {j: w*left[j]+(1-w)*right[j] for j in WELLS}
            require(mixture == site_law(ports, w, 0), "incoherent propagation")
            require(positions(measured(mixture, efficiency, 1/brightness), ref_left, ref_right)
                    == (w, w), "variable-brightness mixture null")
            tested["varying_arm_mixtures"] += 1
        for x, y in product(range(-4, 5), repeat=2):
            norm = x*x + y*y
            if not norm or x*x == y*y:
                continue
            w, c = F(x*x, norm), F(x*y, norm)
            row = measured(site_law(ports, w, c), efficiency, F(13, norm))
            h_outer, h_inner = positions(row, ref_left, ref_right)
            require((h_outer, h_inner-h_outer) == (w, c), "unequal-arm real input")
            tested["real_unequal_or_sharp_inputs"] += 1

    # Change only the response of joint preparations. The same sharp controls survive.
    flat = dict.fromkeys(WELLS, F(3, 5))
    ref_left, ref_right = measured(left, flat, 1), measured(right, flat, 1)
    diagonal = site_law(ports, half, 0)
    examples = {}
    for sign, label in [(1, "identity"), (-1, "reversal")]:
        joint = site_law(ports, half, F(sign, 2))
        changed = dict(flat)
        changed[-1], changed[1] = F(3+2*sign, 5), F(3-2*sign, 5)
        mimic = measured(diagonal, changed, 1)
        require(mimic == measured(joint, flat, 1), "joint-specific gain imitation")
        h_outer, h_inner = positions(mimic, ref_left, ref_right)
        examples[label] = dict(site_law=list(joint.values()), h_minus_2=h_outer,
                               h_minus_1=h_inner, contrast=h_inner-h_outer)
    restored = positions(measured(diagonal, flat, 1), ref_left, ref_right)
    require(restored == (half, half), "restored gain null")
    return dict(scope="Prospective model predictions; no experimental phase scan",
                well_order=WELLS, sharp_left=list(left.values()), sharp_right=list(right.values()),
                fixed_gain_profiles=len(gains), exact_cases=tested, predicted_settings=examples,
                joint_only_gain_mimic=dict(matches_both_full_rows=True,
                                          sharp_controls_unchanged=True,
                                          restored_contrast=restored[1]-restored[0]))


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, default=str))
