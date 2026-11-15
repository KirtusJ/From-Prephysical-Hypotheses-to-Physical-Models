"""Compare final site powers and bin-first readings on a reflected Hadamard walk."""
import argparse
from fractions import Fraction
from itertools import product
import json
from math import atan, pi, sqrt
from pathlib import Path


def line_step(right, left):
    # Ascending reachable sites are -t, -t+2, ..., t before advancing one tick.
    plus = [a + b for a, b in zip(right, left)]
    minus = [a - b for a, b in zip(right, left)]
    return [0] + plus, minus + [0]


def explicit_line(tick):
    amplitudes = [[0, 0] for _ in range(tick + 1)]
    for word in product((0, 1), repeat=tick):
        negative_turns = sum(a == b == 1 for a, b in zip((0,) + word, word))
        final_rail = word[-1] if word else 0
        amplitudes[word.count(0)][final_rail] += (-1) ** negative_turns
    return amplitudes


def reflected(wells, source, ticks):
    right, left = [0] * wells, [0] * wells
    right[source] = 1
    for _ in range(ticks):
        plus = [a + b for a, b in zip(right, left)]
        minus = [a - b for a, b in zip(right, left)]
        right, left = [minus[0]] + plus[:-1], minus[1:] + [plus[-1]]
    return right, left


def fold_port(site, wells):
    lift = site % (2 * wells)
    if lift < wells:
        return lift, False
    return 2 * wells - 1 - lift, True


def control_folds():
    verified = 0
    for wells in range(3, 21):
        for source in range(wells):
            right, left = [1], [0]
            for tick in range(wells):
                folded_right, folded_left = reflected(wells, source, tick)
                visited = set()
                for index, (a, b) in enumerate(zip(right, left)):
                    site, swap = fold_port(source + 2 * index - tick, wells)
                    assert site not in visited
                    visited.add(site)
                    if swap:
                        a, b = b, a
                    assert (folded_right[site] ** 2, folded_left[site] ** 2) == (a * a, b * b)
                assert sum(a * a + b * b for a, b in zip(folded_right, folded_left)) == 2 ** tick
                verified += 1
                right, left = line_step(right, left)
    return verified


def fraction_row(numerator, denominator):
    value = Fraction(numerator, denominator)
    # Hexadecimal output avoids decimal conversion limits on large integers.
    return {
        "ratio": float(value),
        "numerator_hex": hex(value.numerator),
        "denominator_hex": hex(value.denominator),
    }


def panel(tick, right, left):
    # The launch fraction tends to 1/8 and the elapsed scaled time tends to 3/4.
    wells = (4 * tick + 2) // 3
    source = wells // 8
    assert tick < wells

    event_indices = []
    for index in range(len(right)):
        site, _ = fold_port(source + 2 * index - tick, wells)
        if 3 * wells < 8 * (2 * site + 1) < 5 * wells:
            event_indices.append(index)

    site_masses = [a * a + b * b for a, b in zip(right, left)]
    total_mass = sum(site_masses)
    assert total_mass == 2 ** tick
    event_mass = sum(site_masses[index] for index in event_indices)

    power_rows = {}
    for power in (1, 2, 3, 4):
        site_weights = [mass ** power for mass in site_masses]
        rail_weights = [a ** (2 * power) + b ** (2 * power) for a, b in zip(right, left)]
        pooled_event_weight = event_mass ** power
        pooled_total = pooled_event_weight + (total_mass - event_mass) ** power
        power_rows[str(power)] = {
            "power_then_pool": fraction_row(
                sum(site_weights[index] for index in event_indices), sum(site_weights)
            ),
            "rails_powered_before_pool": fraction_row(
                sum(rail_weights[index] for index in event_indices), sum(rail_weights)
            ),
            "pool_then_power": fraction_row(pooled_event_weight, pooled_total),
        }

    # The test window avoids both limiting front locations. At a site of mass n,
    # any rail partition has at least one cell of mass n/2 or larger.
    event_peak = max((site_masses[index] for index in event_indices), default=0)
    if event_peak:
        large_site_squares = sum(mass * mass for mass in site_masses if mass > 2 * event_peak)
        event_squares = sum(site_masses[index] ** 2 for index in event_indices)
        bound = min(1, Fraction(4 * event_squares, large_site_squares)) if large_site_squares else 1
    else:
        bound = 0

    site_collision = Fraction(sum(mass * mass for mass in site_masses), total_mass * total_mass)
    return {
        "tick": tick,
        "wells": wells,
        "source": source,
        "powers": power_rows,
        "t_times_site_collision": float(tick * site_collision),
        "uniform_upper_bound_for_event": float(bound),
    }


def velocity_cdf(velocity):
    if velocity <= -sqrt(0.5):
        return 0.0
    if velocity >= sqrt(0.5):
        return 1.0
    root = sqrt(1 - 2 * velocity * velocity)
    return 0.5 + (atan(velocity / root) - atan(root)) / pi


def pooled_mesh(tick, right, left, bins):
    """Fixed equal-width velocity bins, with +1 assigned to the last bin."""
    assert all((a + b) % 2 for a, b in zip(right, left))
    bin_masses = [0] * bins
    for index, (a, b) in enumerate(zip(right, left)):
        bin_index = min(bins - 1, bins * index // tick)
        bin_masses[bin_index] += a * a + b * b
    assert min(bin_masses) > 0 and sum(bin_masses) == 2 ** tick
    return {
        "tick": tick,
        "bins": bins,
        "masses_over_two_to_t_hex": [hex(mass) for mass in bin_masses],
    }


def limiting_mesh(bins):
    # These numbers approximate analytic integrals after the inner limit.
    edges = [2 * k / bins - 1 for k in range(bins + 1)]
    bin_masses = [velocity_cdf(b) - velocity_cdf(a) for a, b in zip(edges, edges[1:])]
    assert min(bin_masses) >= 0
    statistics = {}
    for power in (0, 0.5, 1, 2, 3):
        # Zero power on the finite full-support subsequence also counts exterior bins.
        weights = [1] * bins if power == 0 else [mass ** power for mass in bin_masses]
        total_weight = sum(weights)
        statistics[str(power)] = {
            "positive_velocity": sum(weights[bins // 2:]) / total_weight,
            "central_quarter": sum(weights[3 * bins // 8:5 * bins // 8]) / total_weight,
        }
    return {"bins": bins, "statistics": statistics}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    output = parser.parse_args().output

    panel_ticks = {6, 12, 24, 48, 96, 192, 384, 768, 1536}
    last_tick = max(panel_ticks)
    right, left = [1], [0]
    panels = []
    finite_meshes = []
    for tick in range(last_tick + 1):
        if tick <= 10:
            assert explicit_line(tick) == [list(pair) for pair in zip(right, left)]
        if tick in panel_ticks:
            panels.append(panel(tick, right, left))
        if tick >= 15 and (tick & (tick + 1)) == 0:
            for bins in (8, 16, 32):
                if bins <= tick + 1:
                    finite_meshes.append(pooled_mesh(tick, right, left, bins))
        if tick < last_tick:
            right, left = line_step(right, left)

    data = {
        "line_vs_interval_cases": control_folds(),
        "event": "3/16 < (x+1/2)/L < 5/16",
        "all_clocks": panels,
        "finite_pooled_meshes": finite_meshes,
        "after_inner_limit": [limiting_mesh(2 ** j) for j in (3, 5, 7, 9, 11, 13, 15)],
    }
    with output.open("x", encoding="utf-8", newline="\n") as sink:
        sink.write(json.dumps(data, indent=2) + "\n")


if __name__ == "__main__":
    main()
