"""Check the address Hadamard, its bypass/phase controls and the re-encoded write."""

from fractions import Fraction

from check_ring_distance import check, columns, probabilities, signed_words


def effect(col_r, col_l, denominator):
    """Diagonal and upper off-diagonal terms of a real two-column Gram matrix."""
    return tuple(Fraction(sum(x*y for x, y in zip(a, b)), denominator)
                 for a, b in [(col_r, col_r), (col_r, col_l), (col_l, col_l)])


def combine(a, b, sign):
    return tuple(x+sign*y for x, y in zip(a, b))


def main():
    right, left = columns((1, 0)), columns((0, 1))
    bypass = [Fraction(i, 8) for i in (1, 0, 1, 0, 5, 0, 1, 0)]
    for t, phase in ((6, 1), (8, -1), (18, 1)):
        for rail, history in enumerate((right, left)):
            check(history[t] == signed_words(t, rail), "coordinate/word comparison")
            check(history[t][2] == tuple(phase*z for z in history[t][6]), "relative sign")
        matrices = list(zip(right[t], left[t]))
        if t in (6, 8):
            expected = ((2, 2), (-2, 2)) if t == 6 else ((-4, -4), (-4, 4))
            check(matrices[2] == expected, "raw matrix columns at site 2")
        for j, (r, l) in enumerate(matrices):
            check(effect(r, l, 2**t) == (bypass[j], 0, bypass[j]), "bare site effect")
        for mask_sign in (1, -1):
            bright = 2 if phase*mask_sign == 1 else 6
            expected = list(bypass)
            expected[2] = expected[6] = 0
            expected[bright] = Fraction(1, 4)
            for j, (r, l) in enumerate(matrices):
                denominator = 2**t
                if j & 2:
                    sign = mask_sign*(-1 if j & 4 else 1)
                    low, high = j & 3, j | 4
                    r = combine(right[t][low], right[t][high], sign)
                    l = combine(left[t][low], left[t][high], sign)
                    denominator *= 2
                    marked = (bypass[low]+bypass[high])/2
                    check(marked == bypass[j], "distinct marks give the average")
                check(effect(r, l, denominator) == (expected[j], 0, expected[j]), "sorted effect")
            for power in (-2, 0, 1, 2):
                ports = probabilities(expected, power)
                check([ports[j] for j in (0, bright, 4)] == probabilities([1, 2, 5], power),
                      "complete-address score")
            print(f"ticks={t:2d} mask={mask_sign:+} bright={bright} masses={list(map(str, expected))}")

    for history in (right, left):
        # H, project bright, H again. The factors 1/sqrt(2) cancel the coherent sum.
        spin = tuple(Fraction(v, 2) for v in combine(history[6][2], history[6][6], 1))
        state = [spin if j in (2, 6) else (0, 0) for j in range(8)]
        for _ in range(4):
            state = [(sum(state[(j-1) % 8]), state[(j+1) % 8][0]-state[(j+1) % 8][1])
                     for j in range(8)]
        check(state[2] == state[6] == (0, 0), "bright and repeat radius two is dark")


if __name__ == "__main__":
    main()
