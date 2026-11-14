"""Crossover bounds with one-step residuals weighted by live probabilities."""
from mpmath import iv
from check_checkpoint_value_bounds import expected_checks
from check_finer_checkpoints import PREVIOUS, WIDTHS, selected_laws


def main():
    iv.dps = 85
    block = 25_000_000_000_000
    for table, increments in selected_laws():
        old = expected_checks(table, increments, PREVIOUS, 20, weight_by_survival=True)
        new = expected_checks(table, increments, WIDTHS, 40, weight_by_survival=True)
        assert new.a > old.b and 2*old.a > new.b

        def crossover(a, b):
            return block*(2*a-b)/(b-a)

        low, high = crossover(old.a, new.b), crossover(old.b, new.a)
        print('expected checks', float(old.a), float(old.b), float(new.a), float(new.b))
        print('break-even pair times', float(low.a), float(high.b))
        assert low > 181775450000 and high < 193339090000


if __name__ == '__main__':
    main()
