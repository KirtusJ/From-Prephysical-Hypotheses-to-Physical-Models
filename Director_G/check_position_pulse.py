"""Replay the eight-cycle rail correction using integer walks and rational costs."""

from fractions import Fraction


IDENTITY = ((1, 0), (0, 1))
ZERO = ((0, 0), (0, 0))
TURN = ((1, -1), (1, 1))
ANTIPODE = ((3, 1), (-1, 3))


def scale(factor, matrix):
    return tuple(tuple(factor * value for value in row) for row in matrix)


def transpose(matrix):
    return tuple(zip(*matrix))


def product(left, right):
    return tuple(
        tuple(sum(a * b for a, b in zip(row, col)) for col in transpose(right))
        for row in left
    )


def free_columns(origin):
    """Accumulate signed path counts before division by sqrt(2)**ticks."""
    snapshots = {t: [[[], []] for _ in range(8)] for t in (4, 6, 18, 24)}
    for incoming in (0, 1):
        state = [[0, 0] for _ in range(8)]
        state[origin][incoming] = 1
        for tick in range(1, 25):
            following = [[0, 0] for _ in range(8)]
            for x, (right, left) in enumerate(state):
                following[(x + 1) % 8][0] += right + left
                following[(x - 1) % 8][1] += right - left
            state = following
            if tick in snapshots:
                for x, pair in enumerate(state):
                    for outgoing, count in enumerate(pair):
                        snapshots[tick][x][outgoing].append(count)
    return {
        t: [scale(Fraction(1, 2 ** (t // 2)), rows) for rows in sites]
        for t, sites in snapshots.items()
    }


def check_flights():
    effects4 = {
        0: scale(Fraction(1, 8), IDENTITY),
        2: scale(Fraction(1, 16), ((10, 4), (4, 2))),
        4: scale(Fraction(1, 8), IDENTITY),
        6: scale(Fraction(1, 16), ((2, -4), (-4, 10))),
    }
    six_numerators = {0: scale(-1, TURN), 2: TURN, 4: ANTIPODE, 6: TURN}
    chances = {}
    for origin in range(8):
        flights = free_columns(origin)
        for d in range(8):
            site = (origin + d) % 8
            k4, k6, k18, k24 = (flights[t][site] for t in (4, 6, 18, 24))
            assert product(transpose(k4), k4) == effects4.get(d, ZERO)
            if d in (0, 4):
                # TURN = sqrt(2) HZ; the corrected matrix is +/- I/sqrt(8).
                assert product(TURN, k4) == scale(Fraction(1 if d else -1, 2), IDENTITY)
            assert k6 == scale(Fraction(1, 4), six_numerators.get(d, ZERO))
            assert k18 == transpose(flights[6][(origin - d) % 8])
            assert k24 == (IDENTITY if d == 0 else ZERO)
            weight = {0: 1, 2: 1, 4: 5, 6: 1}.get(d, 0)
            chances[d] = Fraction(weight, 8)
            for matrix in (k6, k18):
                assert product(transpose(matrix), matrix) == scale(chances[d], IDENTITY)
    assert product(TURN, ANTIPODE) == product(ANTIPODE, TURN)
    twice = product(TURN, TURN)
    assert product(twice, twice) == scale(-4, IDENTITY)
    return sum(chances[d] for d in (0, 2, 6)), chances[4]


def reachable(transitions, start):
    seen = {start}
    pending = [start]
    while pending:
        for other, probability in transitions[pending.pop()].items():
            if probability and other not in seen:
                seen.add(other)
                pending.append(other)
    return seen


def solve_expected(transitions, stop, costs):
    """Solve (I-P)t=c on the transient states with exact elimination."""
    states = [state for state in transitions if state != stop]
    rows = [
        [Fraction(state == nxt) - transitions[state].get(nxt, 0) for nxt in states]
        + [Fraction(costs[state])]
        for state in states
    ]
    for i in range(len(rows)):
        pivot = next(j for j in range(i, len(rows)) if rows[j][i])
        rows[i], rows[pivot] = rows[pivot], rows[i]
        divisor = rows[i][i]
        rows[i] = [value / divisor for value in rows[i]]
        for j, row in enumerate(rows):
            if j != i:
                coefficient = row[i]
                rows[j] = [a - coefficient * b for a, b in zip(row, rows[i])]
    return {stop: Fraction(0), **{state: row[-1] for state, row in zip(states, rows)}}


def check_controller(q, p):
    stop = ("ready", 1)
    transitions = {}
    for n in range(4):
        transitions["ready", n] = {("ready", (n + 1) % 4): q, ("inverse", n): p}
        transitions["inverse", n] = {("inverse", (n - 1) % 4): q, ("ready", n): p}
    transitions[stop] = {stop: Fraction(1)}
    assert all(sum(row.values()) == 1 for row in transitions.values())
    assert reachable(transitions, ("ready", 0)) == set(transitions)
    assert reachable(transitions, stop) == {stop}
    assert all(stop in reachable(transitions, state) for state in transitions)

    costs = {state: 6 if state[0] == "ready" else 18 for state in transitions}
    times = solve_expected(transitions, stop, costs)
    assert [times["ready", n] for n in range(4)] == [84, 0, 132, 128]
    trials = solve_expected(transitions, stop, {s: int(s[0] == "ready") for s in transitions})
    assert trials["ready", 0] == Fraction(7, 2)

    # Cross-check against the chain observed only when the antipodal turns cancel.
    shifts = [q * (d == 1) + p**2 * q**((-d) % 4) / (1 - q**4) for d in range(4)]
    assert shifts == [Fraction(n, 803) for n in (320, 318, 45, 120)]
    mean_trial = 6 + p * 18 / p
    for n in (0, 2, 3):
        after_trial = sum(w * times["ready", (n + d) % 4] for d, w in enumerate(shifts))
        assert times["ready", n] == mean_trial + after_trial
    return times["ready", 0]


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Run without -O so that exact assertions are checked.")
    direct, antipodal = check_flights()
    correction = check_controller(direct, antipodal)
    mean_block = 4 + Fraction(1, 4) * correction
    assert mean_block == 25
    print("Checked all 16 launch columns at clocks 4, 6, 18 and 24.")
    print("All eight controller states are reachable; ready(1) alone is absorbing.")
    print(f"Expected extra ticks per corrected null: {correction}.")
    print(f"Expected walk ticks per complete four-outcome measurement: {mean_block}.")
