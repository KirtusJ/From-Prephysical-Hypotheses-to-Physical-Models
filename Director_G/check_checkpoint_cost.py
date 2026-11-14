"""Cost crossover under a common additive per-checkpoint delay."""
from mpmath import iv
from check_finer_checkpoints import PREVIOUS, WIDTHS, check, selected_laws


def main():
    iv.dps = 85
    for table, increments in selected_laws():
        means = []
        for schedule, scale in [(PREVIOUS, 20), (WIDTHS, 40)]:
            lo, _ = check(table, increments, schedule, scale, True)
            hi, _ = check(table, increments, schedule, scale, False)
            means.append((lo, hi))
        old, new = means
        block = 25_000_000_000_000

        def crossover(a, b):
            return (a-b)/(b/block-a/(2*block))

        extra = iv.mpf([new[0],new[1]])/block - iv.mpf([old[0],old[1]])/(2*block)
        assert extra > 0 and old[0] > new[1]
        low = crossover(old[0], new[1])
        high = crossover(old[1], new[0])
        print('extra checkpoints', float(extra.a), float(extra.b))
        print('break-even pair times', float(low.a), float(high.b))
        assert extra > iv.mpf("44.9166") and extra < iv.mpf("44.9490")
        assert low > 177162900000 and high < 197956800000


if __name__ == '__main__':
    main()
