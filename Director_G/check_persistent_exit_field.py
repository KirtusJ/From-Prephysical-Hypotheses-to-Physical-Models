"""Compare spatial field counts to persistent Markov transport for a two-site launch."""
from collections import Counter
from itertools import product


def check(n):
    amplitudes = Counter()
    classical = Counter()
    for origin in (0, 2):
        for exits in product((1,-1), repeat=n):
            x, rail, weight = origin, 1, 1
            marks = []
            for tick, new in enumerate(exits):
                if new == -1:
                    marks.append(x - 2*tick)
                weight *= 3 if rail == new else 4*rail
                x, rail = x+new, new
            amplitudes[x, rail, tuple(sorted(marks))] += weight
            classical[x, rail] += weight**2
    read = Counter()
    for (x, rail, _), weight in amplitudes.items():
        read[x, rail] += weight**2
    assert read == classical
    assert sum(read.values()) == 2*25**n


if __name__ == "__main__":
    for ticks in range(1, 11):
        check(ticks)
    print("Two-origin joint site and velocity panels agree through ten ticks.")
