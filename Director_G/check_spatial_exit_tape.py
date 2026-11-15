"""Exact spatial marginals for a homogeneous walk with a cyclic exit tape."""
from collections import Counter
from math import comb


def check(length):
    state = {(0, 1, 0): 1}
    for n in range(1, 2*length + 5):
        later = Counter()
        bit = 1 << ((n-1) % length)
        for (x, rail, tape), amplitude in state.items():
            later[x+1, 1, tape] += amplitude
            later[x-1, -1, tape ^ bit] += rail * amplitude
        state = later
        counts = Counter()
        for (x, _, _), a in state.items():
            counts[x] += a*a
        assert sum(counts.values()) == 2**n
        q, r = divmod(n-1, length)
        assert counts[n-2] == 1 + r*(q+1)**2 + (length-r)*q*q
        classical = {n-2*k: comb(n,k) for k in range(n+1)}
        assert (counts == classical) == (n <= length+1)


if __name__ == "__main__":
    for length in range(1, 9):
        check(length)
    print("Full spatial panels and one-left edge counts agree with the theorem for L=1..8.")
