"""Check remote position rates for two late choices on a sharp Hadamard walk."""
import argparse
import json
from fractions import Fraction
from pathlib import Path


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def walk(ticks, change=None):
    state = {0: (1, 0)}
    for t in range(ticks):
        outputs = {}
        for x, (right, left) in state.items():
            if change == (t, x):
                right, left = -right, -left
            outputs.setdefault(x + 1, [0, 0])[0] = right + left
            outputs.setdefault(x - 1, [0, 0])[1] = right - left
        state = outputs
    return state


def signed_paths(ticks, change):
    totals = {}
    for bits in range(2**ticks):
        x, rail, sign = 0, 0, 1
        for t in range(ticks):
            out = (bits >> t) & 1
            if change == (t, x):
                sign = -sign
            if rail == out == 1:
                sign = -sign
            x += 1 - 2 * out
            rail = out
        totals.setdefault(x, [0, 0])[rail] += sign
    return totals


def site_masses(state):
    return {x: a*a + b*b for x, (a, b) in sorted(state.items())}


def probabilities(masses, power):
    # The q=0 boundary uses the limit from positive powers, including at dark sites.
    weights = {x: n**power if n else 0 for x, n in masses.items()}
    total = sum(weights.values())
    return {x: Fraction(n, total) for x, n in weights.items()}


def check_choice(horizon, change, monitors, expected, reverse):
    states = [walk(horizon, setting) for setting in (None, change)]
    masses = [site_masses(s) for s in states]
    require([list(m.values()) for m in masses] == expected, "site tables")
    for setting, state, table in zip((None, change), states, masses):
        require(state == signed_paths(horizon, setting), "signed path replay")
        require(sum(table.values()) == 2**horizon, "norm")
    for x in monitors:
        require(abs(x-change[1]) > horizon-change[0], "monitor in control cone")
        require(states[0][x] == states[1][x], "remote coherent rails differ")
    big, edge = monitors
    base = masses[0][big]
    require(masses[0][edge] == 1, "edge reference")
    trials = []
    for power in (0, 1, 2, 3, 8, 32):
        bare, marked = [probabilities(table, power) for table in masses]
        delta = {x: bare[x] - marked[x] for x in monitors}
        witness = delta[big] - base * delta[edge]
        if reverse:
            witness = -witness
        require(witness >= 0, "remote witness changed sign")
        require((witness == 0) == (power == 1 or (power == 0 and reverse)),
                "unexpected null")
        trials.append(dict(q=power, bare_remote=[bare[x] for x in monitors],
                           marked_remote=[marked[x] for x in monitors], witness=witness))
    return dict(ticks=horizon, change=change, monitors=monitors,
                site_mass_numerators=masses, sampled_exponents=trials)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    out = parser.parse_args().output
    first = check_choice(5, (2, -2), (3, 5),
                         [[1,5,4,4,17,1], [1,5,0,8,17,1]], False)
    second = check_choice(7, (5, 1), (5, 7),
                          [[1,17,5,9,17,41,37,1], [1,17,5,25,25,17,37,1]], True)
    require(first["sampled_exponents"][0]["witness"] == Fraction(8,15), "left boundary")
    require(first["sampled_exponents"][2]["bare_remote"][0] == Fraction(289,348),
            "quartic record")
    early = probabilities(site_masses(walk(2)), 2)
    later = probabilities(site_masses(walk(3)), 2)
    reachable = sum(later[x] for x in (-3, -1))
    deficit = early[-2] - reachable
    require(deficit == Fraction(2,21), "one-tick cut")
    fair_dark = Fraction(sum(bits.bit_count() == 3 for bits in range(32)), 32)
    require(first["site_mass_numerators"][1][-1] == 0 and fair_dark == Fraction(5,16),
            "five-tick count component")
    data = dict(five_ticks=first, seven_ticks=second, marked_count_dark_rate=fair_dark,
                unmodified_quartic=dict(earlier=early, later=later,
                                       reachable_mass=reachable, missing_mass=deficit))
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("x", encoding="utf8", newline="\n") as handle:
        json.dump(data, handle, indent=2, default=str)
        handle.write("\n")


if __name__ == "__main__":
    main()
