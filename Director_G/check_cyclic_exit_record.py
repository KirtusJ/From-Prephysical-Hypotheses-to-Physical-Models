"""Compare the cyclic exit record theorem with exact forward amplitudes."""
from collections import defaultdict
from math import gcd


def check(length, retain_first=False):
    state = {(0, 0, 0): 1}
    period = 4 * length // gcd(length, 2)
    for tick in range(2 * period):
        updated = defaultdict(int)
        bit = 1 << (tick % length)
        for (port, memory, first), value in state.items():
            updated[0, memory, first] += value
            updated[1, memory ^ bit, first | int(retain_first and tick == 0)] += -value if port else value
        state = updated
        weights = [sum(v*v for (p, _, _), v in state.items() if p == port) for port in (0, 1)]
        total = 2**(tick+1)
        assert sum(weights) == total
        expected = total if not retain_first and (tick+1) % period == 0 else total//2
        assert weights[0] == expected, (length, tick+1, weights)
    return period


if __name__ == "__main__":
    for length in range(1, 11):
        check(length, retain_first=True)
    print([(length, check(length)) for length in range(1, 11)])
