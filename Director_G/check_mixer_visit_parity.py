"""Exact mixer-visit parity records in the controlled eight-well walk."""
from fractions import Fraction as F
from itertools import combinations

ZERO = (F(0), F(0))


def tagged_walk(word):
    # Store x + y sqrt(2) at each (well, rail, parity).
    state = {(0, 1, 0): (F(1), F(0))}
    for pair in word.split():
        a, b = (2 * int(label) for label in pair)
        delay = ((b - a) % 8) // 2
        for tick in range(16):
            after = {}
            for (site, rail, parity), (x, y) in state.items():
                if tick == delay and site == (a + delay) % 8:
                    outputs = [(1, parity ^ 1, y, x/2), (-1, parity ^ 1, rail*y, rail*x/2)]
                else:
                    turn = site == b and tick in (0, 8)
                    outputs = [(-rail if turn else rail, parity, x, y)]
                for direction, flag, u, v in outputs:
                    key = ((site + direction) % 8, direction, flag)
                    old_u, old_v = after.get(key, ZERO)
                    after[key] = old_u + u, old_v + v
            state = after
    return state


def check(word, expected_return):
    state = tagged_walk(word)
    assert all(rail == 1 and site % 2 == 0 and value[1 - flag] == 0
               for (site, rail, flag), value in state.items())
    total = cross = 0
    for site in range(0, 8, 2):
        e = state.get((site, 1, 0), ZERO)[0]
        o = state.get((site, 1, 1), ZERO)[1]
        mean, difference = e*e + 2*o*o, 2*e*o
        if site == 0:
            assert (mean, difference) == expected_return
        total += mean
        cross += difference
    assert (total, cross) == (1, 0)


def counterpart(word):
    """Copy the unordered pair at each step, choosing its physical orientation."""
    signs = [1] * 4
    result = []
    for pair in word.split():
        left, right = map(int, pair)
        if signs[left] == signs[right]:
            result.append(pair)
            signs[left] *= -1
            signs[right] *= -1
        else:
            result.append(pair[::-1])
    return " ".join(result)


def check_relative_sign_states():
    # A subset records the negative coordinates. Complementing it preserves
    # all pair comparisons. Include the empty prefix and every one-gate prefix.
    pairs = list(combinations(range(4), 2))
    classes = {
        tuple((i in negative) == (j in negative) for i, j in pairs)
        for negative in [(), *pairs]
    }
    assert len(classes) == 4


if __name__ == "__main__":
    check_relative_sign_states()
    cases = [
        ("01 12 01", "01 21 01", F(3, 8), F(1, 4)),
        ("01 02 21 10 12 10 20 21 02 20 01 21 10 20 01 02",
         "01 20 12 10 12 01 02 21 02 20 01 12 10 20 10 02",
         F(513, 1024), F(45, 128)),
    ]
    for original, partner, mean, contrast in cases:
        assert counterpart(original) == partner and counterpart(partner) == original
        check(original, (mean, contrast))
        check(partner, (mean, -contrast))
    print("Both equal-length pairs exchange the port-zero probabilities.")
