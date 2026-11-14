"""Certify the fixed-ring comparison for G1's sharp (0,R) source.

The two scores must have identical complete distributions on rings 4 and 8.
The all-time check uses an exact translated or rescaled source return and
isolated magnitudes within one cycle. On ring 16 the specified rate must
change from 1/8 to 1/5 and the perturbed score must fail marker conservation.
Independently count all direction words at the decisive depth. The general
unit-equation proof is in the accompanying note.
"""

import argparse
import json
from fractions import Fraction
from itertools import product
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def panels(size, last_tick):
    state = [(int(x == 0), 0) for x in range(size)]
    yield state
    for _ in range(last_tick):
        next_state = [[0, 0] for _ in state]
        for x, (right, left) in enumerate(state):
            next_state[(x + 1) % size][0] = right + left
            next_state[(x - 1) % size][1] = right - left
        state = [tuple(pair) for pair in next_state]
        yield state


def panel_weights(state, doubled):
    def score(value):
        factor = 2 if doubled and abs(value) == 32 else 1
        return factor * value * value

    rows = [(score(right), score(left)) for right, left in state]
    return rows, sum(right + left for right, left in rows)


def periodic_certificate(size, ticks, scale, shift):
    fields = list(panels(size, ticks))
    target = [(scale if x == shift else 0, 0) for x in range(size)]
    require(fields[-1] == target, f"Source return failed on ring {size}")
    hit_ticks = []
    for tick, field in enumerate(fields[:-1]):
        magnitudes = {abs(v) for pair in field for v in pair if v}
        if size == 4:
            require(len(magnitudes) == 1, "The four-site panel mixes magnitudes")
        if 32 in magnitudes:
            hit_ticks.append(tick)
            require(magnitudes == {32}, "Magnitude 32 shares a panel")
        square, total = panel_weights(field, False)
        rival, other_total = panel_weights(field, True)
        for first, second in zip(square, rival):
            require(all(v * other_total == w * total for v, w in zip(first, second)),
                    f"Normalized panels differ on ring {size} at tick {tick}")
    cutoff = size // 2 + 1
    require(all(v % 2 == 0 for pair in fields[cutoff] for v in pair),
            "The dyadic parity cutoff failed")
    positive_odds = sorted({v for field in fields[:cutoff] for pair in field
                            for v in pair if v > 0 and v % 2})
    return {"period_steps": ticks, "raw_scale": scale, "source_translation": shift,
            "magnitude_32_ticks_in_first_period": hit_ticks,
            "positive_odd_totals_before_even_cutoff": positive_odds}


def enumerate_words(size, tick):
    state = [[0, 0] for _ in range(size)]
    for word in product((0, 1), repeat=tick):
        # 0 means right and 1 means left. The launch rail is right.
        x = (tick - 2 * sum(word)) % size
        left_pairs = sum(a * b for a, b in zip(word, word[1:]))
        state[x][word[-1]] += -1 if left_pairs % 2 else 1
    return [tuple(pair) for pair in state]


def separating_panel():
    size, tick = 16, 13
    fields = list(panels(size, tick))
    before, after = fields[-2:]
    require(after == enumerate_words(size, tick), "Signed-word totals disagree")
    marked = [(x, rail) for x, pair in enumerate(after) for rail, v in enumerate(pair)
              if abs(v) == 32]
    require(marked == [(7, 0), (9, 0)], "Unexpected magnitude-32 ports")
    predictions = {}
    for label, doubled, rate, daughter, normalizer in [
        ("square", False, Fraction(1, 8), Fraction(73, 512), 8192),
        ("double_at_32", True, Fraction(1, 5), Fraction(137, 640), 10240),
    ]:
        prev_weights, prev_total = panel_weights(before, doubled)
        weights, total = panel_weights(after, doubled)
        parent_mass = Fraction(sum(prev_weights[6]), prev_total)
        daughter_mass = Fraction(weights[7][0] + weights[5][1], total)
        observed_rate = Fraction(weights[7][0], total)
        require(total == normalizer and observed_rate == rate, "Named rate failed")
        require(parent_mass == Fraction(73, 512) and daughter_mass == daughter,
                "Conservation comparison failed")
        predictions[label] = {"normalizer": total, "probability_7R": str(observed_rate),
                              "parent_6": str(parent_mass), "daughters_7R_5L": str(daughter_mass)}
    return {"ring": size, "tick": tick, "signed_words": 2 ** tick,
            "magnitude_32_ports": ["7R", "9R"], "predictions": predictions}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path, help="new JSON file")
    output = parser.parse_args().output
    if output.exists():
        parser.exit(2, f"Refusing to overwrite {output}\n")
    four = periodic_certificate(4, 4, 4, 2)
    eight = periodic_certificate(8, 24, 4096, 0)
    require(eight["magnitude_32_ticks_in_first_period"] == [12, 13], "Wrong eight-site ticks")
    require(four["positive_odd_totals_before_even_cutoff"] == [1], "Wrong odd totals on four sites")
    require(eight["positive_odd_totals_before_even_cutoff"] == [1, 3], "Wrong odd totals on eight sites")
    data = {"four_sites": four, "eight_sites": eight, "separating_panel": separating_panel()}
    with output.open("x", encoding="utf-8") as stream:
        json.dump(data, stream, indent=2)
        stream.write("\n")


if __name__ == "__main__":
    main()
