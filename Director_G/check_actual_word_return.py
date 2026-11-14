"""Compare an actual word and its terminal walk state to an ideal inverse flight."""
from argparse import ArgumentParser
from fractions import Fraction
from itertools import product
import json
from pathlib import Path

from check_reflected_histories import cut, norm, tick


def inverse_tick(state):
    right, left = state
    plus = [*right[1:], left[-1]]
    minus = [right[0], *left[:-1]]
    return [p + m for p, m in zip(plus, minus)], [p - m for p, m in zip(plus, minus)]


def phase_flip(state):
    return state[0], [-l for l in state[1]]


def source(length, site):
    state = ([0] * length, [0] * length)
    state[0][site] = 1
    return state


def flight(word, intervention):
    state = source(4, 1)
    bits = dict(zip((2, 4, 8), word))
    for t in range(1, 9):
        state = tick(state)
        if t in bits:
            state = cut(state, bits[t])
            if t == 4 and bits[t] == "1":
                if intervention == "left_rail":
                    state = phase_flip(state)
                if intervention == "left_rail_at_well_2":
                    state[1][2] *= -1
    return state


def inverse_word(state, word):
    # Reading the original register as blank eliminates paths outside each supplied bit.
    bits = dict(zip((2, 4, 8), word))
    for t in range(8, 0, -1):
        if t in bits:
            state = cut(state, bits[t])
        state = inverse_tick(state)
    return state[0][1]


def dot(a, b):
    return sum(x * y for left, right in zip(a, b) for x, y in zip(left, right))


def histories(intervention):
    rows = {}
    for bits in product("01", repeat=3):
        word = "".join(bits)
        ideal = flight(word, "none")
        actual = flight(word, intervention)
        p, q = norm(ideal), norm(actual)
        assert inverse_word(ideal, word) == p
        echo = inverse_word(actual, word)
        assert echo == dot(ideal, actual)
        rows[word] = {"ideal_count": p, "actual_count": q, "signed_return": echo,
                      "incident_pass": str(Fraction(echo**2, 256**2)),
                      "conditional_fidelity": str(Fraction(echo**2, p*q)) if p*q else None}
    assert sum(r["ideal_count"] for r in rows.values()) == 256
    assert sum(r["actual_count"] for r in rows.values()) == 256
    return rows


def false_pass():
    # Sharp (0,R) at left wall gives modes (0,R) and (1,R) after one tick.
    pre = tick(source(4, 0))
    assert pre == ([1, 1, 0, 0], [0, 0, 0, 0])
    outputs = []
    for bit in range(2):
        ideal = ([0] * 4, [0] * 4)
        ideal[0][bit] = 1
        opposite = ([0] * 4, [0] * 4)
        opposite[0][1-bit] = 1
        for k, actual in (("repeatable", ideal), ("opposite", opposite)):
            bare = inverse_tick(actual)[0][0]
            tested = tuple([value if x == bit else 0 for x, value in enumerate(rail)]
                           for rail in actual)
            filtered = inverse_tick(tested)[0][0]
            outputs.append({"b": bit, "instrument": k, "q": "1/2",
                            "bare_return": str(Fraction(bare**2, 4)),
                            "matched_return": str(Fraction(filtered**2, 4)),
                            "repeat_disagrees": str(Fraction(norm(actual)-norm(tested), 2))})
    assert [r["bare_return"] for r in outputs] == ["1/4"] * 4
    assert [r["matched_return"] for r in outputs] == ["1/4", "0"] * 2
    return outputs


def run():
    rows = histories("left_rail_at_well_2")
    changes = [abs(r["ideal_count"] - r["actual_count"]) for r in rows.values()]
    tv = Fraction(sum(changes), 512)
    assert tv == Fraction(1, 16)
    quiet = histories("left_rail")
    assert all(r['ideal_count'] == r['actual_count'] for r in quiet.values())
    assert quiet['110']['conditional_fidelity'] == '25/49'
    assert quiet['111']['conditional_fidelity'] == '1/25'
    return {"word_denominator": 256, "echo_denominator": 65536,
            "reflection_phase": 1, "source": [1, "R"], "wells": 4,
            "cut_clocks": [2, 4, 8], "word_rows": rows,
            "tv_of_visible_words": str(tv), "same_word_law_phase_control": quiet,
            "unfiltered_false_pass": false_pass()}


if __name__ == "__main__":
    ap = ArgumentParser(description=__doc__)
    ap.add_argument("output", type=Path)
    report = run()
    with ap.parse_args().output.open("x", encoding="utf-8", newline="\n") as file:
        file.write(json.dumps(report, indent=2) + "\n")
