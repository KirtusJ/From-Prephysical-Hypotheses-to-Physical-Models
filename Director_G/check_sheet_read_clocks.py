"""Exact terminal-basis discrimination for the eight-well randomized sheet walk."""
from collections import Counter
from fractions import Fraction


def advance(state):
    after = Counter()
    for (well, rail, sheet), amplitude in state.items():
        written = (sheet + (well in (1, 6))) % 3
        after[(well + 1) % 8, 1, written] += amplitude
        after[(well - 1) % 8, -1, written] += rail * amplitude
    return after


def panel(state):
    result = Counter()
    for (well, rail, _), amplitude in state.items():
        result[well, rail] += amplitude**2
    return result


def clock_scores(last):
    source = advance(advance({(0, 1, 0): 1}))
    translation = source
    reflection = {(x, r, -y % 3): a for (x, r, y), a in source.items()}
    for tick in range(2, last + 1):
        t, f = panel(translation), panel(reflection)
        assert sum(t.values()) == sum(f.values()) == 2**tick
        selected = sorted(cell for cell in t.keys() | f.keys() if t[cell] > f[cell])
        advantage = sum(t[cell] - f[cell] for cell in selected)
        assert 3 * advantage**2 < 4**tick
        yield tick, (1 + Fraction(advantage, 2**tick)) / 2, selected
        translation, reflection = advance(translation), advance(reflection)


if __name__ == "__main__":
    import sys

    rows = list(clock_scores(int(sys.argv[1]) if len(sys.argv) > 1 else 1024))
    if len(rows) >= 9:
        assert rows[8][1] == Fraction(731, 1024)
    best = max(rows, key=lambda row: row[1])
    print(best[0], float(best[1]), best[2])
