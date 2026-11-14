"""Replay the returned position-color pointer using elementary integer-amplitude gates."""
from argparse import ArgumentParser
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


# A port consists of position, rail, pointer address, and an untouched spectator.
# Hadamard gates below omit their 1/sqrt(2) factor; all paths in each layer have
# the same denominator, including both pointer-control arms of the correction.
def hadamard(state):
    changed = {}
    for (x, rail, address, spectator), value in state.items():
        for target in (0, 1):
            port = (x, target, address, spectator)
            changed[port] = changed.get(port, 0) + value * (-1 if rail == target == 1 else 1)
    return {p: v for p, v in changed.items() if v}


def shift(state, distance, n, bit=None):
    changed = {}
    for (x, rail, address, spectator), value in state.items():
        delta = distance * (1 - 2 * rail) if bit is None or address & bit else 0
        changed[(x + delta) % n, rail, address, spectator] = value
    return changed


def color_xor(state, bit):
    return {(x, rail, address ^ (((x // 2) % 2) * bit), spectator): value
            for (x, rail, address, spectator), value in state.items()}


def rail_gate(state, bit, kind):
    changed = {}
    for (x, rail, address, spectator), value in state.items():
        if kind == "x0" and not (address & bit):
            rail ^= 1
        if kind == "z1" and (address & bit) and rail:
            value = -value
        changed[x, rail, address, spectator] = value
    return changed


def pointer_gate(state, bit, n, inverse=False):
    if inverse:
        state = hadamard(state)
        state = rail_gate(state, bit, "x0")
        state = rail_gate(state, bit, "z1")
        state = shift(state, 2, n, bit)
        state = color_xor(state, bit)
        for _ in range(2):
            state = hadamard(shift(state, -1, n))
        return color_xor(state, bit)
    state = color_xor(state, bit)
    for _ in range(2):
        state = shift(hadamard(state), 1, n)
    state = color_xor(state, bit)
    state = shift(state, -2, n, bit)
    state = rail_gate(state, bit, "z1")
    state = rail_gate(state, bit, "x0")
    return hadamard(state)


def ladder(state, m, n, inverse=False):
    for i in (reversed(range(m)) if inverse else range(m)):
        state = pointer_gate(state, 1 << i, n, inverse)
    return state


def assign_address(state, address):
    return {(x, rail, address, spectator): value for (x, rail, _, spectator), value in state.items()}


def scale(state, coefficient):
    return {port: coefficient * value for port, value in state.items() if coefficient * value}


def combine(states):
    result = {}
    for state in states:
        for port, value in state.items():
            result[port] = result.get(port, 0) + value
    return {p: v for p, v in result.items() if v}


def sliced(state, address):
    return {(x, r, 0, s): value for (x, r, a, s), value in state.items() if a == address}


def norm2(state):
    return sum(value * value for value in state.values())


def sign(state, k):
    return {p: (-value if p[2] < k else value) for p, value in state.items()}


def reference_a(state, n):
    """Twice the amplitude of V0†V1, from its direct one-rail formula H X S2 Z H."""
    result = {}
    for (x, r, a, s), value in state.items():
        for q in (0, 1):
            for j in (0, 1):
                p = ((x + 2 * (1 - 2 * q)) % n, j, a, s)
                exponent = q * r + q + (1 - q) * j
                result[p] = result.get(p, 0) + value * (-1) ** exponent
    return {p: v for p, v in result.items() if v}


def ring_columns(n):
    expected = {"blank": 0, "dirty": 0}
    first_failure = {}
    for x in range(n):
        for r, initial in ((r, initial) for r in (0, 1) for initial in (0, 1)):
            unit = {(x, r, 0, 0): 1}
            actual = pointer_gate(assign_address(unit, initial), 1, n)
            if initial == 0:
                wanted = combine((scale(unit, 2), scale(assign_address(unit, 1), 2)))
                key = "blank"
            else:
                a = reference_a(unit, n)
                wanted = combine((a, scale(assign_address(a, 1), -1)))
                key = "dirty"
            if actual != wanted:
                expected[key] += 1
                first_failure.setdefault(key, [x, r])
            restored = pointer_gate(actual, 1, n, inverse=True)
            require(restored == scale(assign_address(unit, initial), 8), "two-sided unitary replay")
    return dict(ring=n, columns_checked_per_bit=2*n, failed_columns=expected, first_failure=first_failure)


def digest(state):
    rows = [[*p, v] for p, v in sorted(state.items())]
    return sha256(json.dumps(rows, separators=(",", ":")).encode("ascii")).hexdigest()


def prepare_carrier():
    # A signed state on both colors and all rail-spectator pairs, with unequal
    # local profiles for the two spectator values. One global normalization suffices.
    result = {}
    for x, r, s, value in [(0, 0, 0, 2), (1, 1, 0, -1), (3, 0, 0, 3), (6, 1, 0, 1),
                            (1, 0, 1, 1), (2, 0, 1, -2), (4, 1, 1, 3), (7, 1, 1, -1)]:
        result[x, r, 0, s] = value
    return result


def clean_and_dirty_sweep(m, n, carrier):
    size = 2**m
    raw = ladder(carrier, m, n)
    require(all(sliced(raw, a) == scale(carrier, size) for a in range(size)), "clean factoring")
    require(norm2(raw) == 8**m * norm2(carrier), "integer forward norm")
    dirty_pattern = sum(1 << i for i in range(0, m, 2))
    dirty = assign_address(carrier, dirty_pattern)
    dirty_out = ladder(dirty, m, n)
    reference = carrier
    for i in range(m):
        reference = reference_a(reference, n) if dirty_pattern & (1 << i) else scale(reference, 2)
    for a in range(size):
        phase = (-1) ** ((a & dirty_pattern).bit_count())
        require(sliced(dirty_out, a) == scale(reference, phase), "dirty basis formula")
    # An unrestricted signed superposition over all input addresses checks unitarity
    # even when the pointer is entangled with the walker or the spectator.
    mixed_addresses = {}
    for a in range(size):
        for p, value in carrier.items():
            x, r, _, s = p
            coefficient = (1 + (x + 2*s + a) % 3) * (-1) ** ((r ^ s ^ a) & 1)
            mixed_addresses[x, r, a, s] = coefficient * value
    require(ladder(ladder(mixed_addresses, m, n), m, n, True) == scale(mixed_addresses, 8**m),
            "return on unrestricted entangled inputs")
    trials = []
    for k in range(size + 1):
        hit = Fraction(sum(norm2(sliced(raw, a)) for a in range(k)), norm2(raw))
        returned = ladder(sign(raw, k), m, n, inverse=True)
        zero = sliced(returned, 0)
        require(zero == scale(carrier, 8**m * (size - 2*k) // size), "zero register carrier block")
        returned_norm = norm2(returned)
        require(returned_norm == 8**(2*m) * norm2(carrier), "full echo norm")
        escape = 1 - Fraction(norm2(zero), returned_norm)
        require(hit == Fraction(k, size) and escape == 4 * hit * (1 - hit), "dyadic escape")
        trials.append(dict(k=k, address_mass=str(hit), escape_mass=str(escape), echo_sha256=digest(returned)))
    return dict(bits=m, original_norm_numerator=norm2(carrier), dirty_input=dirty_pattern,
                same_carrier_up_to_sign_despite_dirty=(reference == scale(carrier, size)
                                                        or reference == scale(carrier, -size)),
                dirty_register_full_output_sha256=digest(dirty_out), observations=trials)


def dirty_bias(carrier, n):
    # Input components 2 psi and 2 A† psi share one common normalization.
    other = scale(assign_address(reference_a(carrier, n), 1), -1)
    source = combine((scale(carrier, 2), other))
    actual = pointer_gate(source, 1, n)
    require(actual == scale(carrier, 8), "correlated dirty source has deterministic pointer zero")
    return dict(input_norm=norm2(source), output_norm_numerator=norm2(actual),
                mass_one_given_true_blank="1/2", mass_one_with_correlated_dirty_input="0")


def secondary_carrier_read(n):
    """An H-only address reference agrees on escape but fails the same-launch position read."""
    rows = []
    for rail in (0, 1):
        port = {(0, rail, 0, 0): 1}
        final = pointer_gate(sign(pointer_gate(port, 1, n), 1), 1, n, True)
        require(all(a == 1 and x in {2, n-2} for x, r, a, s in final), "escaped address and shifted carrier")
        require(norm2(final) == 64, "secondary position read denominator")
        rows.append(dict(input_rail=rail, amplitudes_with_denominator_8=[[*p, v] for p, v in sorted(final.items())]))
    return dict(ring=n, input_site=0, bits=1, threshold=1, signed_walk_carrier_departure="1",
                independent_H_reference_carrier_departure="0", rows=rows)


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    carrier = prepare_carrier()
    rings = [ring_columns(n) for n in (4, 8, 12, 6, 10)]
    for ring in rings:
        for key in ("blank", "dirty"):
            require((ring["failed_columns"][key] == 0) == (ring["ring"] % 4 == 0),
                    "position color at the periodic seam")
    result = dict(column_checks=rings, source_amplitudes=[[*p, v] for p, v in sorted(carrier.items())],
                  coherent_sweeps_on_ring_8=[clean_and_dirty_sweep(m, 8, carrier) for m in range(1, 6)],
                  correlated_dirty_control=dirty_bias(carrier, 8),
                  secondary_carrier_read=secondary_carrier_read(8),
                  normalization="Each forward pointer gate divides integer amplitudes by sqrt(8). "
                                "The inverse gate has the same factor.")
    with args.output.open("x", encoding="utf8", newline="\n") as out:
        json.dump(result, out, indent=2)
        out.write("\n")


if __name__ == "__main__":
    main()
