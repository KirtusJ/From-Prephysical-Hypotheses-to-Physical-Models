"""Check native folded-return sector filters using integer counts on the five-sheet line."""
import argparse
import json
from fractions import Fraction
from itertools import product
from math import sqrt
from pathlib import Path


ORDER = 5
WITNESS = (2, 1, 1, 2, 1, 1, 2, 2)


def radius_paths(k):
    """Signed counts; initial coin and final coin are indexed R=0, L=1."""
    table = [[[0] * ORDER for _ in range(2)] for _ in range(2)]
    for col, initial_coin in enumerate((1, -1)):
        for directions in product((1, -1), repeat=2*k):
            pos, sheet, old_coin, sign = 0, 0, initial_coin, 1
            for tick, direction in enumerate(directions, start=1):
                sheet = (sheet+pos) % ORDER
                pos += direction
                if abs(pos) != min(tick, 2*k-tick):
                    break
                if old_coin == direction == -1:
                    sign = -sign
                old_coin = direction
            else:
                row = int(old_coin == -1)
                table[row][col][sheet] += sign
    return table


def native_word(word):
    state = [[1, 0, 0, 0, 0], [0]*ORDER]
    for k in word:
        table = radius_paths(k)
        out = [[0]*ORDER for _ in range(2)]
        for row, col, source, shift in product(range(2), range(2), range(ORDER), range(ORDER)):
            out[row][(source+shift) % ORDER] += state[col][source]*table[row][col][shift]
        state = out
    return state


def exact_readout(word):
    state = native_word(word)
    count = state[1]
    correlation = [sum(count[j]*count[(j+d) % ORDER] for j in range(ORDER))
                   for d in range(ORDER)]
    c0, c1, c2, c3, c4 = correlation
    assert (c1, c2) == (c4, c3)
    den = 2**len(word)
    rational = Fraction(2*c0-c1-c2, 2*den)
    sqrtpart = Fraction(c1-c2, 2*den)
    zero = Fraction(sum(count)**2, den)
    word_mass = Fraction(1, 2**sum(2*k-1 for k in word))
    # The exact native word, including normalization for every physical step.
    joint = Fraction(c0, 2**(2*sum(word)))
    assert joint == word_mass*(zero+4*rational)/ORDER
    assert sum(x*x for row in state for x in row) == word_mass*(2**(2*sum(word)))
    p1 = float(rational)+sqrt(5)*float(sqrtpart)
    p2 = float(rational)-sqrt(5)*float(sqrtpart)
    return dict(radii=word, walk_ticks=2*sum(word), source="Localized at site and sheet zero, incoming R.",
                recorded="All corridor memberships followed by direction L.",
                right_integer_counts=state[0], left_integer_counts=count,
                left_cyclic_correlations=correlation, word_mass=str(word_mass),
                zero_sector_L_given_word=str(zero), plus_minus_one_L_rational=str(rational),
                plus_minus_one_L_sqrt5_coefficient=str(sqrtpart),
                plus_minus_one_L_given_word=p1, plus_minus_two_L_given_word=p2,
                joint_word_and_L_from_localized_sheet=str(joint),
                posterior_target_pair=max(p1, p2)/(float(zero)/2+p1+p2))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("output_directory", type=Path)
    args = parser.parse_args()
    witnesses = [exact_readout(word) for word in (WITNESS, (1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1))]
    w = witnesses[0]
    assert w["left_integer_counts"] == [-5, 2, 2, -5, 6]
    assert w["word_mass"] == "1/65536" and w["joint_word_and_L_from_localized_sheet"] == "47/8388608"
    assert w["plus_minus_one_L_rational"] == "235/512" and w["plus_minus_one_L_sqrt5_coefficient"] == "-105/512"
    assert w["zero_sector_L_given_word"] == "0"
    report = dict(scope="Fixed accepted words, five-sheet character model. At tag two the sqrt(5) term changes sign. "
                        "Density, adaptive stopping and efficient synthesis are not inferred from these finite cases.",
                  definition="T sends sheet y to y+1. Complex convention T maps to exp(2*pi*i*r/5).",
                  word_selection="Finite search over binary radius-one/two words; no minimal-length claim.",
                  witnesses=witnesses)
    args.output_directory.mkdir(parents=True, exist_ok=True)
    (args.output_directory/"simultaneous_sectors.json").write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8")
    print("Exact path counts and normalization passed for", len(witnesses), "sector filters.")


if __name__ == "__main__":
    main()
