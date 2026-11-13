"""Exact probability checks for a signed ring walk with a reversible history flag."""
import argparse
from collections import Counter, defaultdict
from fractions import Fraction
import hashlib
import json
from pathlib import Path


def words(ticks, gains, order):
    """Class-operator oracle: trace each direction string without a tape."""
    result = []
    for word in range(1 << ticks):
        x, previous, sign, sheet = 0, 0, 1, 0
        for j in reversed(range(ticks)):
            left = (word >> j) & 1
            sheet = (sheet + gains[x]) % order
            if previous and left:
                sign = -sign
            x = (x + (1, -1)[left]) % len(gains)
            previous = left
        result.append(((x, previous, sheet), sign))
    return result


def copy_tape(ticks, bits, gains, order):
    """Propagate on actual (site,coin,sheet,tape) basis, XORing each copied coin."""
    state = {(0, 0, 0, 0): 1}
    for tick in range(ticks):
        following = Counter()
        for (x, coin, sheet, tape), amplitude in state.items():
            s = (sheet + gains[x]) % order
            following[(x + 1) % len(gains), 0, s, tape] += amplitude
            left_tape = tape ^ (1 << (bits - tick - 1)) if tick < bits else tape
            following[(x - 1) % len(gains), 1, s, left_tape] += -amplitude if coin else amplitude
        state = following
    return state


def read_tape(state, ticks, bits, mask):
    """XOR a clean flag with membership, then apply one Hadamard per tape bit."""
    out = Counter()
    for (x, coin, sheet, tape), value in state.items():
        word = tape if bits == ticks else 2 * tape + coin
        flag = (mask >> word) & 1
        out[flag, tape, x, coin, sheet] += value
    for j in range(bits):
        following = Counter()
        bit = 1 << j
        for (flag, tape, x, coin, sheet), value in out.items():
            low = tape & ~bit
            following[flag, low, x, coin, sheet] += value
            following[flag, low | bit, x, coin, sheet] += -value if tape & bit else value
        out = following
    return out


def class_oracle(paths, ticks, bits, mask):
    out = Counter()
    for word, ((x, coin, sheet), value) in enumerate(paths):
        flag = (mask >> word) & 1
        prefix = word >> (ticks - bits)
        for row in range(1 << bits):
            sign = -1 if (row & prefix).bit_count() % 2 else 1
            out[flag, row, x, coin, sheet] += sign * value
    return out


def measure(out, bits):
    masses = [[0] * (1 << bits) for _ in range(2)]
    for (flag, row, _x, _coin, _sheet), value in out.items():
        masses[flag][row] += value * value
    return masses


def check_case(paths, copied, ticks, bits, mask):
    physical = read_tape(copied, ticks, bits, mask)
    oracle = class_oracle(paths, ticks, bits, mask)
    assert physical == oracle
    masses = measure(physical, bits)
    denominator = 1 << (ticks + bits)
    assert sum(map(sum, masses)) == denominator
    assert sum(masses[1]) == mask.bit_count() * (1 << bits)
    return masses, physical


def extend(mask, ticks):
    return sum(3 << (2 * word) for word in range(1 << ticks) if (mask >> word) & 1)


def mask_for(ticks, kind):
    count = 1 << ticks
    full = (1 << count) - 1
    if kind == "full":
        return full
    if kind == "empty":
        return 0
    if kind == "singleton_Rs":
        return 1
    if kind == "all_except_RLL":
        return full ^ (1 << 3)   # binary 011 = RLL
    if kind == "continuation_except_RLL_prefix":
        return extend(mask_for(3, "all_except_RLL"), 3)
    raise ValueError(kind)


def named_rows(gains, order):
    rows = []
    for ticks in (1, 2, 3, 4):
        cases = ["full", "empty", "singleton_Rs"]
        if ticks == 3:
            cases.append("all_except_RLL")
        if ticks == 4:
            cases = ["continuation_except_RLL_prefix"]
        paths = words(ticks, gains, order)
        for bits in (ticks - 1, ticks):
            copied = copy_tape(ticks, bits, gains, order)
            for kind in cases:
                mask = mask_for(ticks, kind)
                masses, _ = check_case(paths, copied, ticks, bits, mask)
                den = 1 << (ticks + bits)
                yes = Fraction(masses[1][0], den)
                no = Fraction(masses[0][0], den)
                if kind == "full":
                    assert yes == Fraction(1, 1 << bits) and no == 0
                if kind == "singleton_Rs":
                    assert yes == Fraction(1, den)
                if kind == "empty":
                    assert yes == 0 and no == Fraction(1, 1 << bits)
                if order == 1 and "except" in kind:
                    assert yes * (1 << bits) == Fraction(9, 8)
                    assert no * (1 << bits) == Fraction(1, 8)
                rows.append(dict(ticks=ticks, tape_bits=bits, event=kind,
                                 all_tape_numerators_by_flag_no_yes=masses, denominator=den,
                                 yes_zero=str(yes), no_zero=str(no), scaled_yes=str(yes * (1 << bits)),
                                 conditional_yes_given_tape_zero=str(yes / (yes + no))))
    return rows


def exhaust(gains, order):
    rows = []
    for ticks in (1, 2, 3):
        paths = words(ticks, gains, order)
        extended = words(ticks + 1, gains, order)
        copies = {b: copy_tape(ticks, b, gains, order) for b in (ticks - 1, ticks)}
        zeros = []
        for mask in range(1 << (1 << ticks)):
            zero = []
            for bits, copied in copies.items():
                masses, _ = check_case(paths, copied, ticks, bits, mask)
                zero.append(masses[1][0])
            assert zero[0] == zero[1]
            # A class-operator continuation leaves each accepted last direction unrestricted.
            extended_yes = Counter()
            expanded = extend(mask, ticks)
            for word, (end, sign) in enumerate(extended):
                if (expanded >> word) & 1:
                    extended_yes[end] += sign
            assert sum(x*x for x in extended_yes.values()) == 2 * zero[0]
            zeros.append(zero[0])
        rows.append(dict(ticks=ticks, subsets=len(zeros), both_tape_lengths=list(copies),
                         raw_class_numerator_by_subset_mask=zeros,
                         raw_class_denominator=1 << ticks,
                         above_unit_class_weight=[i for i, n in enumerate(zeros) if n > 1 << ticks]))
    return rows


def fifth_cyclotomic(coefficients, k):
    """Represent evaluation at zeta_5^k in basis (1,z,z^2,z^3) exactly."""
    shifted = [0] * 5
    for j, value in enumerate(coefficients):
        shifted[(j*k) % 5] += value
    return [value - shifted[4] for value in shifted[:4]]


def sector_test(gains):
    """Compare physical point-sheet readout with all five character squared norms."""
    ticks, bits = 3, 2
    mask = mask_for(ticks, "full")
    paths = words(ticks, gains, 5)
    _, physical = check_case(paths, copy_tape(ticks, bits, gains, 5), ticks, bits, mask)
    tests = []
    den = 1 << (ticks + bits)
    for coin, x, label in ((0, 1, "constructive"), (1, len(gains)-1, "destructive")):
        polynomial = [physical[1, 0, x, coin, s] for s in range(5)]
        gram = [sum(polynomial[s] * polynomial[(s-j) % 5] for s in range(5)) for j in range(5)]
        # Independent: sum all ordered history pairs at this base endpoint before tracing sheets.
        pairs = Counter()
        for (a, v) in paths:
            for (b, w) in paths:
                if a[:2] == b[:2] == (x, coin):
                    pairs[(a[2] - b[2]) % 5] += v*w
        assert [pairs[j] for j in range(5)] == gram
        phase = 1 if not coin else -1
        assert gram == [2, phase, 0, 0, phase]
        sectors = [fifth_cyclotomic(gram, k) for k in range(5)]
        assert sectors[1] == sectors[4] and sectors[2] == sectors[3] and sectors[1] != sectors[2]
        assert sectors[0] == [2 + 2*phase, 0, 0, 0]
        assert list(map(sum, zip(*sectors))) == [5 * gram[0], 0, 0, 0]
        tests.append(dict(port=label, base=[x,coin], denominator=den,
                          signed_point_sheet_amplitudes=polynomial, lag_coefficients=gram,
                          character_numerators_in_Q_zeta5_basis=sectors,
                          localized_sheet_joint_probability=str(Fraction(gram[0], den))))
    return tests


def multiply_fifth(a, b):
    coefficients = [0] * 5
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            coefficients[(i+j) % 5] += x*y
    return fifth_cyclotomic(coefficients, 1)


def tomography():
    """A fixed N=8 site-0 gain bump; select two actual words per test."""
    ticks, bits = 10, 9
    gains = [1] + [0]*7
    paths = words(ticks, gains, 5)
    representatives = defaultdict(list)
    for word, ((site, coin, sheet), sign) in enumerate(paths):
        if (site, coin) == (0, 0):
            representatives[sheet, sign].append(word)
    reference = representatives[0, 1][0]
    state = copy_tape(ticks, bits, gains, 5)
    def word_string(word):
        return format(word, f"0{ticks}b").translate(str.maketrans("01", "RL"))

    def selected_zero_word_pair(word_indices):
        # Project to the computed yes flag first; this commutes with tape readout.
        # On this fixed final coin the compressed tape is the whole word prefix.
        predicate = {word >> 1 for word in word_indices}
        chosen = {end: value for end, value in state.items() if
                  end[0:2] == (0, 0) and end[3] in predicate}
        assert len(chosen) == len(word_indices)
        accepted = read_tape(chosen, ticks, bits, sum(1 << w for w in word_indices))
        return [accepted[1, 0, 0, 0, sheet] for sheet in range(5)]

    assert selected_zero_word_pair([reference]) == [1, 0, 0, 0, 0]
    rows = []
    by_a = {}
    # Folded weights in (0, ±1, ±2), normalized by 10.
    weights = [1, 3, 6]
    for relative_sign in (1, -1):
        for a in range(5):
            choices = representatives[a, relative_sign]
            partner = next(w for w in choices if w != reference)
            sheet_amplitude = selected_zero_word_pair([reference, partner])
            localized_ratio = sum(v*v for v in sheet_amplitude)
            ratios = []
            for k in range(5):
                # Independent of the pair cosine formula: transform physical amplitudes,
                # transform the conjugate, then multiply inside the cyclotomic field.
                z = fifth_cyclotomic(sheet_amplitude, k)
                zbar = fifth_cyclotomic(sheet_amplitude, -k)
                ratio = multiply_fifth(z, zbar)
                expected = [2, 0, 0, 0, 0]
                expected[(k*a) % 5] += relative_sign
                expected[(-k*a) % 5] += relative_sign
                assert ratio == fifth_cyclotomic(expected, 1)
                ratios.append(ratio)
            assert list(map(sum, zip(*ratios))) == [5*localized_ratio, 0, 0, 0]
            # The signed sheet increment (sign, a) corresponds to exponent 2a or 2a+5
            # in mu_10. The five physical sheet characters extend with sign fixed negative.
            r = (2*a + (5 if relative_sign == -1 else 0)) % 10
            for k, K in enumerate((5, 1, 7, 3, 9)):
                assert K % 2 == 1 and (K*r - 2*k*a) % 10 == (0 if relative_sign == 1 else 5)
            mixed = [sum(weights[k]*ratios[k][i] for k in range(3)) for i in range(4)]
            if relative_sign == 1:
                by_a[a] = mixed
            rows.append(dict(sheet_lag=a, sign=relative_sign, exponent_mod_10=r,
                             words=[word_string(reference), word_string(partner)],
                             point_sheet_numerator_about_singleton=localized_ratio,
                             five_character_ratios_in_Q_zeta5_basis=ratios,
                             weighted_ratio_in_Q_zeta5_basis_over_10=mixed))
    # Invert the all-positive-pair records: R(a)-2 is the signed-frequency series.
    # Its zero coefficient is twice the folded zero weight, its others the pair weights.
    recovered = []
    for k in range(3):
        coefficient = [0]*4
        for a, measured in by_a.items():
            centred = [measured[0]-20, *measured[1:]]
            phase = [int(i == (-k*a) % 5) for i in range(5)]
            term = multiply_fifth(centred, fifth_cyclotomic(phase, 1))
            coefficient = [x+y for x,y in zip(coefficient, term)]
        assert coefficient[1:] == [0]*3
        recovered.append(Fraction(coefficient[0], 50*(2 if k == 0 else 1)))
    assert recovered == [Fraction(w,10) for w in weights]
    return dict(N=8, M=5, departure_gains=gains, ticks=ticks, tape_bits=bits, endpoint=[0,0],
                positive_words_available=[len(representatives[a,1]) for a in range(5)],
                negative_words_available=[len(representatives[a,-1]) for a in range(5)],
                singleton_yes_zero="1/524288", full_yes_zero="1/512",
                basis="1,z,z^2,z^3 with z=exp(2 pi i/5); every row is a pair/singleton ratio.",
                folded_input_weights=[str(Fraction(w,10)) for w in weights],
                recovered_by_inverse_DFT=[str(w) for w in recovered],
                order_10_indices_for_sheet_k_0_to_4=[5,1,7,3,9], rows=rows)


def main(output):
    gains = [0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
    cases = []
    for order, profile in ((1, [0]*len(gains)), (5, gains)):
        cases.append(dict(order=order, departure_gains=profile, N=len(profile),
                          exhaustive=exhaust(profile, order), named=named_rows(profile, order)))
    result = dict(initial="Site 0, incoming R, sheet 0, all tape/flag/work bits blank.",
                  word_convention="R=0, L=1; a mask includes each t-bit word indexed by its binary integer.",
                  instrument="Signed Hadamard walk, native departure translation, XOR of outgoing coin into "
                             "a blank bit, reversible membership flag (oracle action with scratch returned), "
                             "Hadamard on each copied bit, record flag and tape in coordinates. This assumes "
                             "tape, controlled gates and squared-norm readout as supplied operations.",
                  normalization="The walker contributes 2^(-t/2), tape erasure 2^(-k/2). All outcome "
                                "numerators use denominator 2^(t+k). In compressed mode k=t-1 the last "
                                "direction is in the base output. Summing tape outcomes gives path counts.",
                  continuation="For all endpoints together, Ext gives the same scaled class weight. "
                               "At the next depth, the zero-tape joint probability is halved in either "
                               "tape design. A fixed partial endpoint need not be conserved.",
                  cases=cases, five_sheet_full_event_yes_zero_ports=sector_test(gains),
                  five_sheet_pair_tomography=tomography(),
                  scope="Character rows assume a prepared character, or its conjugate pair on real "
                        "records, and the same sheet-blind instrument. A point sheet gives their equal "
                        "mean. This is an exact finite calculation, with no empirical readout assumed verified.")
    output.mkdir(parents=True, exist_ok=True)
    target = output / "history_flags.json"
    target.write_bytes((json.dumps(result, indent=1) + "\n").encode())
    print(target, hashlib.sha256(target.read_bytes()).hexdigest())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_directory", type=Path)
    main(parser.parse_args().output_directory)
