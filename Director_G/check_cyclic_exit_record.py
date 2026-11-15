"""Compare the cyclic exit record theorem with exact forward amplitudes."""
from collections import defaultdict
from math import gcd


def check(length, retain_first=False, middle=None):
    state = {(0, 0, 0, 0): 1}
    period = 4 * length // gcd(length, 2)
    for tick in range(2 * period):
        updated = defaultdict(int)
        bit = 1 << (tick % length)
        for (port, memory, first, extra), value in state.items():
            updated[0, memory, first, extra] += value
            updated[1, memory ^ bit, first | int(retain_first and tick == 0), extra | int(tick+1 == middle)] += -value if port else value
        state = updated
        weights = [sum(v*v for (p, _, _, _), v in state.items() if p == port) for port in (0, 1)]
        total = 2**(tick+1)
        assert sum(weights) == total
        expected = total if not retain_first and (tick+1) % period == 0 else total//2
        assert weights[0] == expected, (length, tick+1, weights)
        if retain_first and (middle is None or tick == period):
            matches = sum(v*v for (p, _, first, _), v in state.items() if p == first)
            repeat = tick % period == 0 and (middle is None or (middle-1) % 2 == 0)
            assert matches == (total if repeat else total//2), (length, tick, middle)
    return period


if __name__ == "__main__":
    for length in range(1, 11):
        for middle in (None, 2, 3):
            check(length, retain_first=True, middle=middle)
    print([(length, check(length)) for length in range(1, 11)])
