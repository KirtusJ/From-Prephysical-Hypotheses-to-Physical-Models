"""Exact five-site signed walk: identical port intensities with different futures.

Run with Python 3.9+. Printed weights are per original launch. Field entries
are signed integer amplitudes with a common factor 2**(-t/2) left implicit.
A site mask either passes both rails coherently or removes both.
"""

import json
from collections import defaultdict
from fractions import Fraction
from itertools import combinations, product

SITES = 5
OPEN = frozenset(range(SITES))
START = (1, 0) + (0,) * (2 * SITES - 2)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def step(state, mask):
    result = [0] * len(state)
    for site in range(SITES):
        right, left = state[2 * site:2 * site + 2]
        target_right = (site + 1) % SITES
        target_left = (site - 1) % SITES
        if target_right in mask:
            result[2 * target_right] = right + left
        if target_left in mask:
            result[2 * target_left + 1] = right - left
    return tuple(result)


def sparse(entries):
    state = [0] * (2 * SITES)
    for site, rail, value in entries:
        state[2 * site + int(rail == "L")] = value
    return tuple(state)


def squares(state):
    return tuple(x * x for x in state)


def propagate(schedule, word_check=False):
    state = START
    for t, mask in enumerate(schedule, start=1):
        state = step(state, mask)
        if word_check:
            require(state == enumerate_words(schedule[:t]), ("Word propagation", t))
    return state


def enumerate_words(schedule):
    result = [0] * (2 * SITES)
    for word in product("RL", repeat=len(schedule)):
        site, old, sign = 0, "R", 1
        for direction, mask in zip(word, schedule):
            site = (site + (1 if direction == "R" else -1)) % SITES
            if site not in mask:
                break
            if old == direction == "L":
                sign *= -1
            old = direction
        else:
            result[2 * site + int(old == "L")] += sign
    return tuple(result)


def masks_from(first, tail):
    return (frozenset({first}),) + tuple(frozenset(mask) for mask in tail)


def earliest_open_difference():
    # Full mask set: equivalent effects on unoccupied sites are counted once
    # by storing distinct amplitude fields at each time. Later masks act only
    # by deletion, so checking the next open field covers every next mask.
    masks = [set(sites) for k in range(SITES + 1) for sites in combinations(range(SITES), k)]
    states = {START}
    rows = []
    for tick in range(1, 5):
        states = {step(state, mask) for state in states for mask in masks}
        groups = defaultdict(list)
        for state in states:
            groups[squares(state)].append(state)
        separated = sum(squares(step(a, OPEN)) != squares(step(b, OPEN))
                        for fields in groups.values() for a, b in combinations(fields, 2))
        rows.append({"tick": tick, "distinct_amplitudes": len(states),
                     "distinct_intensities": len(groups), "immediately_separated_pairs": separated})
    actual = [(r["distinct_amplitudes"], r["distinct_intensities"], r["immediately_separated_pairs"])
              for r in rows]
    require(actual == [(4, 4, 0), (12, 12, 0), (43, 41, 0), (250, 209, 18)],
            ("Unexpected enumeration", rows))
    return rows


def four_distinct_futures():
    # At tick five the full intensity vector is the same across these settings.
    # The next field reveals two independently variable relative rail signs.
    tails = (
        (1, ({0, 2}, {3, 4}, {0, 2, 3}, {1, 4})),
        (1, ({0, 2}, {1, 3, 4}, {0, 2, 3}, {1, 4})),
        (4, ({0, 3}, {1, 2, 4}, {0, 2, 3}, {1, 4})),
    )
    schedules = [masks_from(first, tail) for first, tail in tails]
    schedules.append(({1, 4}, {2, 3}, {1, 2}, {0, 2, 3}, {1, 4}))
    common = sparse([(1, "R", 1), (1, "L", 1), (4, "R", 1), (4, "L", 1)])
    futures = set()
    for schedule in schedules:
        require(squares(propagate(schedule, word_check=True)) == common, "Four-way input")
        futures.add(squares(propagate(tuple(schedule) + (OPEN,), word_check=True)))
    require(len(futures) == 4, "Four-way outputs")
    return {"preparation_clock": 5, "equal_nonzero_input_weights": "1/32 per rail at sites 1,4",
            "distinct_next_open_fields": 4, "deterministic_auxiliary_states_required": "at least 4"}


def direct_collision():
    tail = [{0}, {1, 4}, {0}]
    state_a, state_b = (propagate(masks_from(first, tail), word_check=True)
                        for first in (1, 4))
    require(state_a == sparse([(0, "R", -1), (0, "L", 1)]), "Unexpected A field")
    require(state_b == sparse([(0, "R", 1), (0, "L", 1)]), "Unexpected B field")
    for first, expected in ((1, sparse([(4, "L", -2)])), (4, sparse([(1, "R", 2)]))):
        schedule = masks_from(first, tail) + (OPEN,)
        require(propagate(schedule, word_check=True) == expected, "Incorrect common-tail reading")
    return {"at_tick_4_per_rail_at_site_0": "1/16", "survival": "1/8",
            "open_tick_5_R_at_site_1_in_A_then_B": ["0", "1/8"],
            "open_tick_5_L_at_site_4_in_A_then_B": ["1/8", "0"]}


def delayed_collision(max_coast):
    tail = [{0}, {1, 4}, {2, 3}, {3, 4}]
    a, b = (propagate(masks_from(first, tail), word_check=True) for first in (1, 4))
    for h in range(max_coast + 1):
        x, y = (3 + h) % SITES, (4 + h) % SITES
        require(a == sparse([(x, "R", 1), (y, "R", 1)]), ("Coasting A", h))
        require(b == sparse([(x, "R", 1), (y, "R", -1)]), ("Coasting B", h))
        a_out, b_out = a, b
        for _ in range(2):
            a_out, b_out = step(a_out, OPEN), step(b_out, OPEN)
            require(squares(a_out) == squares(b_out), ("Early release distinction", h))
        a_out, b_out = step(a_out, OPEN), step(b_out, OPEN)
        port = 2 * (h % SITES) + 1
        opposite_port = 2 * ((2 + h) % SITES)
        diff = tuple(a2 - b2 for a2, b2 in zip(squares(a_out), squares(b_out)))
        require(diff == sparse([(h % SITES, "L", 4), ((2 + h) % SITES, "R", -4)]),
                ("Late release field", h))
        require((a_out[port] ** 2, b_out[port] ** 2) == (4, 0), ("Late release A", h))
        require((a_out[opposite_port] ** 2, b_out[opposite_port] ** 2) == (0, 4),
                ("Late release B", h))
        survival = Fraction(sum(squares(a)), 2 ** (5 + h))
        require(survival == Fraction(sum(squares(b)), 2 ** (5 + h)), ("Survival", h))
        require(Fraction(4, 2 ** (8 + h)) / survival == Fraction(1, 4), ("Contrast", h))
        next_mask = {(x + 1) % SITES, (y + 1) % SITES}
        a, b = step(a, next_mask), step(b, next_mask)
    for first in (1, 4):
        for h in range(3):
            coast = tuple({(3 + j) % SITES, (4 + j) % SITES} for j in range(1, h + 1))
            propagate(masks_from(first, tail) + coast + (OPEN,) * 3, word_check=True)
    return {"coast_lengths_verified": [0, max_coast],
            "pre_release_survival": "2^(-4-h)", "per_launch_difference": "2^(-6-h)",
            "difference_conditioned_on_pre_release_survival": "1/4"}


if __name__ == "__main__":
    print(json.dumps({"ring_size": SITES, "direct": direct_collision(),
                      "minimality": earliest_open_difference(),
                      "four_way": four_distinct_futures(),
                      "arbitrary_delay": delayed_collision(100)}, indent=2))
