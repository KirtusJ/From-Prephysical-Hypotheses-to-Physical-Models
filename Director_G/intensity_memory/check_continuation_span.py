"""Exact real-state observability for five sites with a balanced real Hadamard coin.

Form the span of legal backward port effects over F_101. All unnormalized
matrices have integer entries. A 55-dimensional result certifies rank 55
over the reals as well. Count reachable pure fields separately over Z.
No third-party dependencies, reads or writes. Python 3.9+.
"""
from collections import Counter
from itertools import combinations
import json

SITES = 5
DIM = 2 * SITES
PRIME = 101
PORTS = range(DIM)
POSITIONS = range(SITES)
UPPER = [(i, j) for i in PORTS for j in range(i, DIM)]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def extend_modular_basis(matrix, basis):
    """Add an upper triangle if independent of all previously accepted ones."""
    return add_row([matrix[i][j] for i, j in UPPER], basis)


def add_row(entries, basis):
    row = [entry % PRIME for entry in entries]
    for pivot, existing in sorted(basis.items()):
        factor = row[pivot]
        if factor:
            row = [(x - factor * y) % PRIME for x, y in zip(row, existing)]
    pivot = next((index for index, entry in enumerate(row) if entry), None)
    if pivot is None:
        return False
    inverse = pow(row[pivot], -1, PRIME)
    basis[pivot] = [(entry * inverse) % PRIME for entry in row]
    return True


def successors():
    """Entries ((out-port, signed integer matrix entry), ...) per in-port."""
    table = []
    for i in PORTS:
        position, rail = divmod(i, 2)
        right_out = 2 * ((position + 1) % SITES)
        left_out = 2 * ((position - 1) % SITES) + 1
        table.append(((right_out, 1), (left_out, 1 if rail == 0 else -1)))
    return table


def pull_back(effect, kept, successors_by_port):
    """Omit the common factor 1/2 from the two copies of a normalized one-step matrix."""
    output = [[0] * DIM for _ in PORTS]
    for i, j in UPPER:
        value = 0
        for k, s in successors_by_port[i]:
            if k // 2 in kept:
                for m, t in successors_by_port[j]:
                    if m // 2 in kept:
                        value += s * t * effect[k][m]
        output[i][j] = output[j][i] = value
    return output


def port_effect_ranks():
    """Generate independent actual port effects, also tracking shortest horizons."""
    basis = {}
    frontier = []
    certificate = []
    for i in PORTS:
        E = [[0] * DIM for _ in PORTS]
        E[i][i] = 1
        require(extend_modular_basis(E, basis), "Dependent initial port")
        frontier.append((E, (), i))
        certificate.append(((), i))
    ranks = [len(basis)]
    step = successors()
    # Two-site and singleton masks suffice to span all whole-site masks:
    # M_S E M_S contains only diagonal site blocks and pairwise cross blocks.
    masks = [frozenset(group) for size in (1, 2) for group in combinations(POSITIONS, size)]
    for _ in range(5):
        fresh = []
        for E, history, port in frontier:
            for mask in masks:
                new_effect = pull_back(E, mask, step)
                if extend_modular_basis(new_effect, basis):
                    new_history = (tuple(sorted(mask)),) + history
                    fresh.append((new_effect, new_history, port))
                    certificate.append((new_history, port))
        frontier = fresh
        ranks.append(len(basis))
    require(ranks[-1] == len(UPPER), "Incomplete effect basis")
    return ranks, certificate


def forward(field, masks):
    for mask in masks:
        values = [0] * DIM
        for rail in PORTS:
            position = rail // 2
            if position in mask:
                if rail % 2 == 0:
                    source = (position - 1) % SITES
                    values[rail] = field[2*source] + field[2*source+1]
                else:
                    source = (position + 1) % SITES
                    values[rail] = field[2*source] - field[2*source+1]
        field = tuple(values)
    return field


def replay_certificate(certificate):
    # Reconstruct each effect from scalar responses on the standard basis.
    # No reverse propagation or polarization surrogate is used here.
    basis = {}
    for masks, port in certificate:
        row = [forward(tuple(int(k == j) for k in PORTS), masks)[port] for j in PORTS]
        E = [[x*y for y in row] for x in row]
        require(extend_modular_basis(E, basis), "Dependent forward-replayed reader")
    require(len(basis) == len(UPPER), "Incomplete forward certificate")


def equal_intensity_example():
    start = (1,) + (0,) * (DIM - 1)
    A = ((1,), (0,), (1, 4))
    B = ((4,), (0,), (1, 4))
    a, b = forward(start, A), forward(start, B)
    require(tuple(map(abs, a)) == tuple(map(abs, b)), "Preparation mismatch")
    for mask_bits in range(1 << SITES):
        mask = [p for p in POSITIONS if mask_bits & (1 << p)]
        require(tuple(map(abs, forward(a, [mask]))) == tuple(map(abs, forward(b, [mask]))),
                "Spurious single-step distinction")
    port = 2
    a5, b5 = (forward(f, [POSITIONS, POSITIONS])[port] for f in (a, b))
    require((a5*a5, b5*b5) == (0, 4), "Common two-step tail failed")
    return {"prefix_A": A, "prefix_B": B, "integer_fields": [a, b],
            "number_of_steps_to_distinguish": 2, "common_tail": "all sites open twice",
            "port": [1, "R"], "weights_per_launch_A_B": ["0", "1/8"]}


def intensity_fibers(max_time=6):
    """Enumerate all masked pure states modulo a common sign at a fixed clock."""
    states = {(1,) + (0,) * (DIM - 1)}
    statistics = []
    for time in range(max_time + 1):
        sizes = Counter(tuple(abs(entry) for entry in field) for field in states)
        # At fixed time, squared normalized intensities are entry**2 / 2**time.
        largest = max(sizes.values())
        summary = {"clock": time, "pure_fields": len(states),
                   "intensities": len(sizes), "max_fields_per_intensity": largest}
        if time == max_time:
            summary["example_absolute_integer_amplitudes"] = min(
                values for values, count in sizes.items() if count == largest)
        statistics.append(summary)
        if time == max_time:
            break
        next_states = set()
        for field in states:
            raw = [0] * DIM
            for x in POSITIONS:
                right, left = field[2*x:2*x+2]
                raw[2*((x+1) % SITES)] = right + left
                raw[2*((x-1) % SITES)+1] = right - left
            live = [x for x in POSITIONS if any(raw[2*x:2*x+2])]
            for mask in range(1 << len(live)):
                kept = [0] * DIM
                for bit, x in enumerate(live):
                    if mask & (1 << bit):
                        kept[2*x:2*x+2] = raw[2*x:2*x+2]
                first = next((n for n in kept if n), 0)
                canonical = tuple(-n for n in kept) if first < 0 else tuple(kept)
                next_states.add(canonical)
        states = next_states
    return statistics


def certify_joint_rank(readers):
    # Keep one legal history for each physical ray, through preparation tick 5.
    sharp = (1,) + (0,) * (DIM - 1)
    fields = {sharp: ()}
    for _ in range(5):
        new = {}
        for field, prefix in fields.items():
            after_step = forward(field, [POSITIONS])
            live = [x for x in POSITIONS if any(after_step[2*x:2*x+2])]
            for bits in range(1 << len(live)):
                kept = tuple(x for i, x in enumerate(live) if bits & (1 << i))
                state = tuple(a if index // 2 in kept else 0 for index, a in enumerate(after_step))
                if next((a for a in state if a), 0) < 0:
                    state = tuple(-a for a in state)
                new.setdefault(state, prefix + (kept,))
        fields = new

    prep_basis = {}
    prefixes = []
    for vec, prefix in fields.items():
        if add_row([vec[i] * vec[j] for i, j in UPPER], prep_basis):
            prefixes.append(prefix)
        if len(prefixes) == len(UPPER):
            break
    require(len(prefixes) == len(UPPER), "Insufficient independent preparation rays")

    # Each column of the observed probability table is proportional to the
    # following integer column by the positive constant 2**(-5-len(tail)).
    # Replay the actual preparation, including its original global sign.
    table_basis = {}
    for prefix in prefixes:
        source = forward(sharp, prefix)
        entries = [forward(source, tail)[port] ** 2 for tail, port in readers]
        require(add_row(entries, table_basis), "Dependent physical probability row")
    return {"common_preparation_clock": 5, "independent_rows": len(table_basis),
            "upper_bound_on_reader_steps": 5, "preparation_masks": prefixes}


def main():
    ranks, certificate = port_effect_ranks()
    replay_certificate(certificate)
    stats = intensity_fibers()
    require([s["max_fields_per_intensity"] for s in stats] == [1, 1, 1, 2, 4, 6, 13],
            "Unexpected multiplicities")
    print(json.dumps({"sites": SITES, "rank_prime": PRIME,
                      "real_symmetric_dimension": len(UPPER),
                      "cumulative_modular_ranks": ranks, "reachable_fields": stats,
                      "first_equal_intensity_pair": equal_intensity_example(),
                      "joint_probability_rank": certify_joint_rank(certificate),
                      "reader_certificate": [{"masks": masks, "port": divmod(port, 2)}
                                             for masks, port in certificate],
                      "port_encoding": "site, then rail (0=R and 1=L)"},
                     indent=2))


if __name__ == "__main__":
    main()
