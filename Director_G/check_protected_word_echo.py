"""Exact forward, copy and inverse of the two-comparison flight on 16 wells."""
from collections import Counter
from itertools import product
import json


LENGTH, START, TICKS = 16, 8, 6
RAILS = (0, 1)  # R, L
WORDS = range(4)  # bit 1 is the earlier comparison
DIRECTIONS = list(product(RAILS, repeat=TICKS))


def flag(tick, site):
    if tick == 3 and site <= 5:
        return 2
    if tick == 6 and site >= 12:
        return 1
    return 0


def transfer(site, direction, reverse=False):
    """Both shifts are permutations; an outward attempt holds and changes rail."""
    step = 1 if direction == 0 else -1
    neighbor = site + (-step if reverse else step)
    if 0 <= neighbor < LENGTH:
        return neighbor, direction
    return site, 1 - direction


def outbound(initial, proposals):
    site, rail, flags = initial
    sign = 1
    for tick, direction in enumerate(proposals, 1):
        if rail == direction == 1:
            sign = -sign
        site, rail = transfer(site, direction)
        flags ^= flag(tick, site)
    return (site, rail, flags), sign


def backward(turnaround, predecessors):
    site, rail, flags = turnaround
    sign = 1
    for offset, predecessor in enumerate(predecessors):
        flags ^= flag(TICKS - offset, site)
        site, coin_output = transfer(site, rail, reverse=True)
        if predecessor == coin_output == 1:
            sign = -sign
        rail = predecessor
    return (site, rail, flags), sign


def flight_tables():
    paths = {}
    for site, rail, flags in product(range(LENGTH), RAILS, WORDS):
        signed, counted = Counter(), Counter()
        for proposals in DIRECTIONS:
            terminal, sign = outbound((site, rail, flags), proposals)
            signed[terminal] += sign
            counted[terminal] += 1
        paths[site, rail, flags] = signed, counted
    return paths


def sign_at(site, defect):
    return -1 if defect and site == 12 else 1


def gram_column(tables, defect=False):
    """Multiply each restricted forward column against every other column."""
    initial = tables[START, 0, 0]
    outputs = {}
    for state, comparison in tables.items():
        for word in WORDS:
            a = sum(value * comparison[0][d] * sign_at(d[0], defect)
                    for d, value in initial[0].items() if d[2] == word)
            n = sum(value * comparison[1][d] for d, value in initial[1].items()
                    if d[2] == word)
            outputs[(*state, word)] = (a, n)
    return outputs


def echo_words(defect=False, dirty_original=0, dirty_spare=0, copy=True):
    """Enumerate every proposal and inverse predecessor, including failed returns."""
    signed, counted = Counter(), Counter()
    for proposals in DIRECTIONS:
        middle, first_sign = outbound((START, 0, dirty_original), proposals)
        protected = dirty_spare ^ (middle[2] if copy else 0)
        for predecessors in DIRECTIONS:
            state, last_sign = backward(middle, predecessors)
            endpoint = (*state, protected)
            signed[endpoint] += first_sign * last_sign * sign_at(middle[0], defect)
            counted[endpoint] += 1
    return {key: (signed[key], counted[key])
            for key in product(range(LENGTH), RAILS, WORDS, WORDS)}


def summarize(states):
    returns = [states[START, 0, 0, w] for w in WORDS]
    dirty = [states[START, 0, 1, w] for w in WORDS]
    assert sum(n for a, n in states.values()) == 4096
    assert sum(a*a for a, n in states.values()) == 4096
    return {"signed_clean_returns": [a for a, n in returns],
            "counted_clean_returns": [n for a, n in returns],
            "mass_outside_clean_returns": 4096 - sum(a*a for a, n in returns),
            "signed_source_original_01": [a for a, n in dirty],
            "mass_if_only_source_well_is_checked": [
                sum(a*a for (x, rail, flags, label), (a, n) in states.items()
                    if x == START and label == w) for w in WORDS]}


def run():
    tables = flight_tables()
    signed, counted = tables[START, 0, 0]
    forward = [[sum(v*v for d, v in signed.items() if d[2] == w),
                sum(v for d, v in counted.items() if d[2] == w)] for w in WORDS]
    assert forward == [[29, 49], [27, 7], [8, 8], [0, 0]]
    controls = {}
    for label, settings in (("ideal", {}), ("sign_at_12_before_inverse", {"defect": True}),
                            ("spare_initial_01", {"dirty_spare": 1}),
                            ("original_initial_01", {"dirty_original": 1}),
                            ("spare_copy_omitted", {"copy": False})):
        data = echo_words(**settings)
        if label in ("ideal", "sign_at_12_before_inverse"):
            assert data == gram_column(tables, defect=settings.get("defect", False))
        controls[label] = summarize(data)
        if label == "ideal":
            retained = [[*state, a, n] for state, (a, n) in data.items() if n]
    ideal = controls["ideal"]
    assert ideal["signed_clean_returns"] == [29, 27, 8, 0]
    assert ideal["counted_clean_returns"] == [405, 27, 12, 0]
    assert ideal["mass_if_only_source_well_is_checked"] != [29**2, 27**2, 8**2, 0]
    assert 12 * 27**2 > 27 * 8**2 and 405 * 27**2 > 27 * 29**2
    assert controls["sign_at_12_before_inverse"]["signed_clean_returns"] == [29, -25, 8, 0]
    assert controls["spare_initial_01"]["signed_clean_returns"] == [27, 29, 0, 8]
    assert controls["original_initial_01"]["signed_source_original_01"] == [27, 29, 0, 8]
    assert controls["spare_copy_omitted"]["signed_clean_returns"] == [64, 0, 0, 0]
    return {"counts_denominator": 4096, "signed_echo_amplitude_denominator": 64,
            "forward_signed_mass_and_count_numerators_in_binary_order": forward,
            "controls": controls, "reachable_endpoints_x_rail_original_spare_signed_counted": retained}


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
