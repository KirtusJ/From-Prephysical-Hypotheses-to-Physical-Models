"""Fair-record stopping reference. Two exact finite-horizon calculations."""
from collections import defaultdict
from fractions import Fraction as F
from math import comb, isqrt


def counts(d, n):
    assert 0 < d < n*n and isqrt(d)**2 != d
    move = n*n-d
    death = 4*d
    words = 1 << (2*move + death-1).bit_length()
    return move, death, words-2*move-death, words


def propagate(ticks, move, death, hold, words):
    live = {1: F(1)}
    hit = killed = F()
    for j in range(ticks):
        nxt = defaultdict(F)
        for x, mass in live.items():
            if x == 1:
                hit += mass*F(move, words)
            else:
                nxt[x-1] += mass*F(move, words)
            nxt[x+1] += mass*F(move, words)
            nxt[x] += mass*F(hold, words)
            killed += mass*F(death, words)
        live = nxt
        assert hit + killed + sum(live.values()) == 1
        assert sum(live.values()) <= (1-F(death,words))**(j+1)
    return hit, sum(live.values())


def hit_by_first_passage(ticks, move, hold, words):
    # If first hit is at time t and needs 2j+1 moves, append its final
    # down step to a nonnegative excursion; holds occupy the other slots.
    hit = F()
    for t in range(1, ticks+1):
        for j in range((t-1)//2+1):
            catalan = comb(2*j, j)//(j+1)
            placements = comb(t-1, 2*j)
            hit += F(catalan*placements*move**(2*j+1)*hold**(t-2*j-1), words**t)
    return hit


def at_most_root(q, d, n):
    # q <= (n-sqrt(d))/(n+sqrt(d)); both sides of the squared test are >= 0.
    assert 0 <= q <= 1
    return n*n*(1-q)**2 >= d*(1+q)**2


def main():
    for d, n in ((2,2),(3,2),(5,3),(6,3),(7,3),(10,4),(13,4)):
        move, death, hold, words = counts(d, n)
        for t in (0, 1, 2, 5, 12, 24):
            lo, pending = propagate(t, move, death, hold, words)
            assert hit_by_first_passage(t, move, hold, words) == lo
            assert at_most_root(lo, d, n) and not at_most_root(lo+pending, d, n)
        print(f"d={d}, n={n}, {t}-round hit lower bound {float(lo):.10g}; "
              f"unresolved {float(pending):.5g} (rounded)")

    # Recover the first addressed position panel using a fresh three-bit mask.
    for t in (0, 1, 4, 8, 16, 24):
        hit, pending = propagate(t, 1, 4, 2, 8)
        lo = (6-hit-pending)/8
        hi = (6-hit)/8
        known = ((0,0), (lo,hi), ((1+hit)/8,(1+hit+pending)/8), (F(1,8),F(1,8)))
        assert hi-lo == pending/8 and lo >= F(5,8)
        assert sum(l for l,_ in known)+pending/8 == 1
        if t == 8:
            print(f"Eight-round code-one bracket [{lo}, {hi}]; underdetermined {pending/8}")
    # Independently draw a uniform symbol per PAIR of rounds; swap up/down
    # in the second round. At height one every surviving pair returns to one.
    labels = ("down", "up", "hold", "hold", "kill", "kill", "kill", "kill")
    outcomes = defaultdict(int)
    for first in labels:
        second = {"down":"up", "up":"down"}.get(first, first)
        height = 1
        for move in (first, second):
            if move == "kill":
                outcomes["killed"] += 1
                break
            height += (move == "up") - (move == "down")
            if height == 0:
                outcomes["hit"] += 1
                break
        else:
            assert height == 1
            outcomes["live"] += 1
    assert outcomes == {"hit":1, "live":3, "killed":4}
    correlated_hit = F(outcomes["hit"], 8-outcomes["live"])
    assert correlated_hit == F(1,5) and not at_most_root(correlated_hit, 2, 2)


if __name__ == "__main__":
    main()
