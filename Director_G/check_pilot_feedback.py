"""Exact records for randomized science targets following one pilot hit or miss."""

from fractions import Fraction as F


def science_table(types):
    """Joint tables keyed by pilot x, assigned target j and science outcome y.

    Each j table is conditional on setting that action and sums to one.
    The tuples are (type weight, direct pilot probability, direct science probability).
    """
    table = {}
    for x in (0, 1):
        for j in (0, 1):
            for y in (0, 1):
                value = F(0)
                for weight, pilot, direct in types:
                    hit = direct if j else 1 - direct
                    value += weight * (pilot if x else 1-pilot) * (hit if y else 1-hit)
                table[x, j, y] = value
    assert all(sum(value for (x, action, y), value in table.items() if action == j) == 1
               for j in (0, 1))
    return table


def score(table, mass, hit_policy):
    return sum(prob * (hit_policy[x] if j else 1-hit_policy[x]) * (y - (mass if j else 1-mass))
               for (x, j, y), prob in table.items())


def contrast(table, mass):
    pilot = sum(table[1, 1, y] for y in (0, 1))
    return score(table, mass, [0, 1]) - score(table, mass, [pilot, pilot])


def midpoint_controls():
    a, b, s = F(1, 8), F(3, 8), F(1, 4)
    table = science_table([(F(1, 2), a, a), (F(1, 2), b, b)])
    direct_after = [F(11, 48), F(5, 16)]
    for (x, j, y), value in table.items():
        hit = direct_after[x] if j else 1-direct_after[x]
        assert value == (s if x else 1-s) * (hit if y else 1-hit)
    assert contrast(table, s) == F(1, 32)
    # Assign science using a different coin in each pilot stratum, then evaluate a third policy.
    logged, policy = [F(2, 7), F(3, 5)], [F(4, 9), F(1, 6)]
    observations = {key: value * (logged[key[0]] if key[1] else 1-logged[key[0]])
                    for key, value in table.items()}
    assert sum(observations.values()) == 1
    importance_value = sum(value * (policy[x] if j else 1-policy[x])
                           / (logged[x] if j else 1-logged[x]) * (y - (s if j else 1-s))
                           for (x, j, y), value in observations.items())
    assert importance_value == score(table, s, policy)
    fresh = science_table([(F(1, 4), u, v) for u in (a, b) for v in (a, b)])
    assert contrast(fresh, s) == 0
    # A donor in the same drift stratum with an independent Bernoulli(t) read
    # has the same joint decision/science law as the real pilot at that t.
    own = score(table, s, [0, 1])
    donor = sum((t * (t-s) + (1-t) * (s-t)) / 2 for t in (a, b))
    assert donor == own and score(table, s, [s, s]) == 0


def curve_controls():
    a, b = F(1, 8), F(3, 8)
    width = b-a
    mesh = [a + width*i/4 for i in range(5)]
    masses = [a + width*i/8 for i in range(9)]
    # One crossing interval per equally likely type; interpolate only in that interval.
    def ramp(i, x):
        return a + width * min(F(1), max(F(0), (x-mesh[i])/(mesh[i+1]-mesh[i])))

    def crossing(i, x):
        return b if x >= (mesh[i]+mesh[i+1])/2 else a

    assert all(sum(ramp(i, x) for i in range(4))/4 == x for x in masses)
    deficits = {}
    for z in masses:
        population = [(F(1, 4), ramp(i, z), ramp(i, z)) for i in range(4)]
        d = 2*(z-a)*(b-z) - contrast(science_table(population), z)
        assert d == sum((ramp(i, z)-a)*(b-ramp(i, z))/2 for i in range(4))
        # Exact shared-vertical-seed rounding. At our tested masses each rescaled height
        # is 0, 1/2 or 1, so two equiprobable interior quadrature points suffice.
        distance = sum(abs(ramp(i, z) - (b if v <= (ramp(i, z)-a)/width else a))
                       for i in range(4) for v in (F(1, 4), F(3, 4)))/8
        assert width * distance == d
        assert (d == 0) == (z in mesh)
        deficits[z] = d
    for z in masses:
        for s in masses:
            pop = [(F(1, 4), ramp(i, z), ramp(i, s)) for i in range(4)]
            table = science_table(pop)
            cov = sum(w*(u-z)*(v-s) for w, u, v in pop)
            assert contrast(table, s) == 2*cov
            if z <= s:
                loss = (z-a)*(b-s)-cov
                assert 0 <= loss <= min(deficits[z], deficits[s])/2
            if z in mesh and s in mesh:
                threshold = [(F(1, 4), crossing(i, z), crossing(i, s)) for i in range(4)]
                assert table == science_table(threshold)
    print("4 crossing types, 9 probe masses, all 81 ordered probe pairs checked")


if __name__ == "__main__":
    midpoint_controls()
    curve_controls()
    print("midpoint feedback 1/32, fresh-type gain zero, invasive table reproduced")
