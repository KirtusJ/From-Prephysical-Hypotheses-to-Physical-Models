"""Exact reflecting-flight, hidden-tag and calibration-graph controls."""
import argparse
from fractions import Fraction as F
from itertools import combinations
import json
from pathlib import Path

from check_reflecting_path import launch, path_words, physical_step


def norm2(z):
    return sum(a*a for a in z)


def deficit(weights, tags):
    """Compare the returning environment amplitude with its pair-distance identity."""
    total = sum(weights)
    p = [F(weight, total) for weight in weights]
    mean = [sum(w*t[j] for w, t in zip(p, tags)) for j in (0, 1)]
    pair = sum(p[i]*p[j]*norm2([a-b for a, b in zip(tags[i], tags[j])])
               for i, j in combinations(range(len(tags)), 2))
    assert all(norm2(tag) == 1 for tag in tags)
    assert pair == 1 - norm2(mean)
    return pair


def uniform_constant(weights):
    a, b = sorted(F(w, sum(weights)) for w in weights)[:2]
    return (1/a + 1/b)/4


def inverse_step(state):
    # Invert the shift first, carrying each reflected output back to its own wall.
    length = len(state)
    result = []
    for x in range(length):
        r = state[x+1][0] if x+1 < length else state[x][1]
        l = state[x-1][1] if x > 0 else state[x][0]
        result.append([r+l, r-l])
    return result


def signed_echo(t, direction, phase_mode):
    """Return the left-bin branch and all other final amplitudes with a hidden phase."""
    state = launch(6, rail=direction)
    for _ in range(t):
        state = physical_step(state)
    weights = [z*z for pair in state[:3] for z in pair]
    tagged = [[(-v if (x, r) == phase_mode else v) if x < 3 else 0
               for r, v in enumerate(pair)] for x, pair in enumerate(state)]
    for _ in range(t):
        tagged = inverse_step(tagged)
    mass = sum(weights)
    clean = tagged[0][direction]
    expected = mass - 2*weights[2*phase_mode[0]+phase_mode[1]]
    assert clean == expected
    assert sum(norm2(pair) for pair in tagged) == 2**t * mass
    return {"tick": t, "launch_rail": direction, "phase_mode": phase_mode,
            "bin_mass_numerator": mass, "clean_amplitude_numerator": clean,
            "incident_clean_probability": str(F(clean*clean, 4**t)),
            "normalized_deficit": str(1-F(clean*clean, mass*mass)),
            "all_terminal_rail_numerators": tagged}


def run():
    state = launch(6)
    rows = []
    for t in range(1, 12):
        state = physical_step(state)
        left, right = state[:3], state[3:]
        rows.append({"tick": t, "terminal_rails": state,
                     "left_full_rail_support": all(r and l for r, l in left),
                     "right_full_rail_support": all(r and l for r, l in right)})
        if t in (6, 11):
            assert path_words(6, t)[0] == state
    assert next(row["tick"] for row in rows
                if row["left_full_rail_support"] and row["right_full_rail_support"]) == 6
    left6, right6 = rows[5]["terminal_rails"][:3], rows[5]["terminal_rails"][3:]
    modes = lambda pairs: [v*v for pair in pairs for v in pair]
    left11 = rows[-1]["terminal_rails"][:3]
    sites = [norm2(pair) for pair in left11]
    assert sites == [81, 153, 333]
    constants = {"left_site_tick11": uniform_constant(sites),
                 "left_rail_tick6": uniform_constant(modes(left6)),
                 "right_rail_tick6": uniform_constant(modes(right6))}
    assert list(constants.values()) == [F(91, 34), F(65, 8), F(19)]
    # Resistance-diameter voltage for the two least populated sites of p.
    p = [F(i, sum(sites)) for i in sites]
    voltage = [1/p[0], -1/p[1], F(0)]
    sharpness = []
    for denominator in (8, 32, 128, 512):
        t = [h/denominator for h in voltage]
        # Cayley parametrization of the unit circle gives exact rational phases.
        phases = [((1-x*x)/(1+x*x), 2*x/(1+x*x)) for x in t]
        ratio = deficit([1, 1, 0], phases)/deficit(sites, phases)
        assert 0 < ratio <= constants["left_site_tick11"]
        sharpness.append({"inverse_phase_scale": denominator, "exact_ratio": str(ratio)})
    tags = [(1, 0), (1, 0), (-1, 0)]
    assert deficit([1, 1, 0], tags) == deficit([0, 0, 1], tags) == 0
    assert deficit([1, 0, 1], tags) == 1
    # Two equal-weight, overlapping balanced two-site probes have conductance 1/8 per edge.
    # Voltages +1,0,-1 have energy 1/4 and squared range 4, attaining R_eff(0,2)=16.
    overlap = [F(1, 2)*deficit(w, tags) for w in ([1, 1, 0], [0, 1, 1])]
    assert sum(overlap) == F(1, 2)
    controls = [signed_echo(11, 0, (0, 0)), signed_echo(6, 0, (0, 0)),
                signed_echo(11, 0, (1, 1))]
    assert [F(c["normalized_deficit"]) for c in controls[:2]] == [0, F(88, 169)]
    return {"site_and_rail_coverage": rows, "constants": {k:str(v) for k,v in constants.items()},
            "small_phase_sharpness": sharpness, "hidden_phase_controls": controls,
            "disconnected_controls": {"two_probe_deficits": [0, 0], "cross_component_deficit": 1},
            "overlapping_pair_probes": {"weighted_deficits": list(map(str, overlap)),
                                        "endpoint_resistance": 16, "uniform_constant": 4}}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    with args.output.open("x", encoding="utf-8", newline="\n") as out:
        out.write(json.dumps(run(), indent=2) + "\n")
