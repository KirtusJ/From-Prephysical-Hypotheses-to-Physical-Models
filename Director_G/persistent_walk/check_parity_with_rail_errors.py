"""Check the 41-preparation three-tick parity decision with exact integers."""
from fractions import Fraction as F


GRID = 1024


def terminal_slots(correct, wrong, lost):
    """Of 1024 possible terminal words, how many reject at these counts?"""
    numerator = 59**correct * 19**wrong * 39**lost
    denominator = 20 * 40**(correct + wrong + lost)
    return min(GRID, GRID * numerator // denominator)


def check_cap(n, target_weights):
    """Backward recursion for worst adapted-null size and target power."""
    # Target weights are integer numerators for correct, wrong, loss.
    good, bad, loss = target_weights
    target_denom = good + bad + loss
    values = {}
    for k in range(n + 1):
        for j in range(n + 1 - k):
            slots = terminal_slots(k, j, n-k-j)
            values[k, j] = (slots, slots)
    null_unit = target_unit = GRID
    for t in range(n-1, -1, -1):
        null_unit *= 40
        target_unit *= target_denom
        previous = {}
        for k in range(t + 1):
            for j in range(t + 1 - k):
                if terminal_slots(k, j, t-k-j) == GRID:
                    previous[k, j] = null_unit, target_unit
                    continue
                plus, minus, zero = values[k+1, j], values[k, j+1], values[k, j]
                # Null vertices of a-b <= 1/20: all loss, all wrong,
                # (1/20,0), and (21/40,19/40), in (correct, wrong) coordinates.
                worst = max(40*zero[0], 40*minus[0], 2*plus[0] + 38*zero[0],
                            21*plus[0] + 19*minus[0])
                target = good*plus[1] + bad*minus[1] + loss*zero[1]
                previous[k, j] = worst, target
        values = previous
    size, power = values[0, 0]
    return F(size, null_unit), F(power, target_unit)


def main():
    g, error = F(9, 10), F(1, 20)
    visibility = g - (1+g)*error
    if visibility != F(161, 200):
        raise ArithmeticError('visibility floor')
    for n, weights, label in [
            (40, (361, 39, 400), 'per-rail error limit'),
            (41, (361, 39, 400), 'per-rail error limit'),
            (41, (9, 1, 10), 'five percent of hits mislabelled'),
            (42, (9, 1, 10), 'five percent of hits mislabelled')]:
        size, power = check_cap(n, weights)
        expected_pass = (n == 41 and weights[0] == 361) or n == 42
        if not (size <= F(1, 20) and (power >= F(19, 20)) == expected_pass):
            raise ArithmeticError((label, n, float(size), float(power)))
        print(f'{n}, {label}: null size <= {float(size):.12f}, '
              f'target power >= {float(power):.12f}')


if __name__ == '__main__':
    main()
