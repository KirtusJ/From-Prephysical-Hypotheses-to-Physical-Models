"""Exact integer tag circuits and sorted occupation histories for the local two-tag read."""

import argparse
import json
from fractions import Fraction as Q
from pathlib import Path

from check_occupation_contact import TILTS, ZERO, add, multiply, scale, times_i
from check_contact_tag_identity import scalar_run


def calibrated_gate(v, phase):
    """Twice the unitary P_sym + phase P_anti on four Gaussian coordinates."""
    mid = add(v[1], v[2])
    delta = multiply(phase, add(v[1], scale(-1, v[2])))
    return [scale(2, v[0]), add(mid, delta), add(mid, scale(-1, delta)), scale(2, v[3])]


def require(ok, why):
    if not ok:
        raise ValueError(why)


def norm(v):
    return sum(a * a + b * b for a, b in v)


def physical(c, d, n, phases, reads):
    """Input tags (c,d)/sqrt(n) and (c,-d)/sqrt(n) in their local erasing basis."""
    require(c * c + d * d == n, "tag normalization")
    state = {((), 5): [(c * c, 0), (-c * d, 0), (c * d, 0), (-d * d, 0)]}
    for t, z in enumerate(phases):
        digit = t % 2
        new = {}

        def deposit(key, v):
            prev = new.get(key, [ZERO] * 4)
            new[key] = [add(a, b) for a, b in zip(prev, v)]

        for (word, bits), v in state.items():
            occ = (bits >> digit) & 3
            if occ == 3:
                deposit((word, bits), [scale(5, a) for a in calibrated_gate(v, z)])
            elif occ == 0:
                deposit((word, bits), [scale(10, a) for a in v])
            else:
                diag, imag = TILTS[digit]
                deposit((word, bits), [scale(2 * diag, a) for a in v])
                deposit((word, bits ^ (3 << digit)), [times_i(2 * imag, a) for a in v])
        if t + 1 in reads:
            new = {(word + (bits,), bits): v for (word, bits), v in new.items()}
        state = new
    denom = (n * 10 ** len(phases)) ** 2
    records = {}
    for (word, bits), v in state.items():
        records[word + (bits,)] = [Q(norm([a]), denom) for a in v]
    return records


def odd_sector(phases, reads):
    """Separate scalar imaginary-contact recurrence, one phase per layer."""
    state = {((), 5): (1, 0)}
    for t, z in enumerate(phases):
        bond = t % 2
        new = {}

        def take(k, v):
            new[k] = add(new.get(k, ZERO), v)

        for (word, bits), v in state.items():
            occ = (bits >> bond) & 3
            if occ in (0, 3):
                take((word, bits), scale(5, multiply(z, v) if occ == 3 else v))
            else:
                diag, imag = TILTS[bond]
                take((word, bits), scale(diag, v))
                take((word, bits ^ (3 << bond)), times_i(imag, v))
        if t + 1 in reads:
            new = {(word + (bits,), bits): v for (word, bits), v in new.items()}
        state = new
    return {
        word + (bits,): Q(norm([v]), 25 ** len(phases))
        for (word, bits), v in state.items()
    }


def calibration():
    examples = {}
    maps = {
        "unit": lambda v: v,
        "opposite_orthogonal_tag_sectors": lambda v: [v[0], v[2], v[1], v[3]],
        "opposite_mixed_computational_pairs": lambda v: [
            v[0],
            scale(-1, v[1]),
            scale(-1, v[2]),
            v[3],
        ],
    }
    originals = {
        "00": [(1, 0), ZERO, ZERO, ZERO],
        "11": [ZERO, ZERO, ZERO, (1, 0)],
        "plus_plus": [(1, 0)] * 4,
    }
    for name, gate in maps.items():
        rates = {}
        for label, v in originals.items():
            w = gate(v)
            amp = [add(scale(36, a), scale(-80, b)) for a, b in zip(v, w)]
            rate = Q(norm(amp), 15625 * norm(v))
            defect = Q(norm([add(a, scale(-1, b)) for a, b in zip(v, w)]), norm(v))
            require(
                rate - Q(1936, 15625) == Q(2880, 15625) * defect,
                "native ray calibration",
            )
            rates[label] = str(rate)
        examples[name] = rates
    require(
        examples["opposite_mixed_computational_pairs"]["plus_plus"]
        == str(Q(7696, 15625)),
        "two-probe false pass",
    )
    # The uncalibrated gate is diagonal in the preparation basis. On |01>
    # it contributes phase -1. A local Hadamard on each tag gives four
    # equally sized coordinates, so agreement accepts two of the four.
    tagged = [ZERO, (1, 0), ZERO, ZERO]
    bypass = [scale(36, a) for a in tagged]
    contact = [scale(-80, a) for a in maps["opposite_mixed_computational_pairs"](tagged)]
    before_read = [add(a, b) for a, b in zip(bypass, contact)]
    after_read = []
    for i in range(4):
        value = ZERO
        for j, coordinate in enumerate(before_read):
            value = add(value, scale((-1) ** ((i & j).bit_count()), coordinate))
        after_read.append(value)
    equal_return = Q(norm([after_read[0], after_read[3]]), 4 * 15625)
    require(2 * equal_return == Q(13456, 15625), "false pass in the eraser")
    examples["false_pass_joint_equal_return_for_orthogonal_tags"] = str(equal_return)
    return examples


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("output", type=Path)
    out = ap.parse_args().output
    archive = {"calibrations": calibration(), "schedules": []}
    for phases, reads in (
        ([(1, 0)] * 3, ()),
        ([(-1, 0)] * 3, ()),
        ([(0, 1)] * 3, ()),
        ([(1, 0), (-1, 0), (0, 1), (0, -1), (1, 0), (0, 1)], (2, 4)),
    ):
        even = scalar_run(len(phases), 1, reads)
        odd = odd_sector(phases, reads)
        for c, d, n in ((1, 1, 2), (1, 0, 1), (4, 3, 25), (3, 4, 25)):
            p = Q(c**4 + d**4, n**2)
            direct = physical(c, d, n, phases, reads)
            words = even.keys() | odd.keys() | direct.keys()
            for key in words:
                v = direct.get(key, [0] * 4)
                require(v[0] + v[3] == p * even.get(key, 0), "equal terminal tags")
                require(
                    v[1] + v[2] == (1 - p) * odd.get(key, 0), "different terminal tags"
                )
            require(
                sum(sum(v) for v in direct.values()) == 1, "complete launch outcomes"
            )
            archive["schedules"].append(
                dict(
                    phases=phases,
                    read=reads,
                    tags=[c, d, n],
                    equal_probability=str(p),
                    joint_words={
                        str(k): list(map(str, v)) for k, v in sorted(direct.items())
                    },
                )
            )
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("x", encoding="utf8", newline="\n") as f:
        json.dump(archive, f, indent=2)
        f.write("\n")


if __name__ == "__main__":
    main()
