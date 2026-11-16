"""Certify a signed timing sampler for the five-site walk. Python standard library."""
from array import array
from fractions import Fraction as F
from itertools import combinations, product
from math import comb, isqrt
from secrets import randbelow
import json
GRID = 2 ** 128
BINS = 2 ** 32
CAPS = (36733, 121786, 130167)


def require(test, message):
    if not test:
        raise ArithmeticError(message)
# Real intervals have outward-rounded integer endpoints in units of 1/GRID.


def constant(x):
    return (x * GRID, x * GRID)


def plus(x, y):
    return (x[0] + y[0], x[1] + y[1])


def minus(x, y):
    return (x[0] - y[1], x[1] - y[0])


def divide(x, n):
    return (x[0] // n, -(-x[1] // n))


def mul(x, y):
    corners = [i * j for i in x for j in y]
    return (min(corners) // GRID, -(-max(corners) // GRID))


def root(x):
    return (isqrt(x[0] * GRID), isqrt(x[1] * GRID) + 1)


def unit_phase(x):
    return (x, root(minus(constant(1), mul(x, x))))


def times(z, w):
    return (minus(mul(z[0], w[0]), mul(z[1], w[1])), plus(mul(z[0], w[1]), mul(z[1], w[0])))


def conjugate(z):
    return (z[0], (-z[1][1], -z[1][0]))


def power(z, k):
    ans = (constant(1), constant(0))
    while k:
        if k % 2:
            ans = times(ans, z)
        k //= 2
        if k:
            z = times(z, z)
    return ans


def forward(z, base):
    a, b = z
    c, d = base
    return ((a * c - b * d) // GRID, (a * d + b * c) // GRID)


def centers(phases):
    for z in phases:
        require(all((b - a < 64 for a, b in z)), 'Root enclosure too wide')
    return [(z[0][0], z[1][0]) for z in phases]


def resolve(z, r):
    running = (constant(1), constant(0))
    for diff in range(1, 56):
        running = times(running, z)
        j, k = (55, 55 - diff)
        rad = j * (2 * r - j) * k * (2 * r - k)
        right = ((r - j) * (r - k) * GRID - isqrt(rad * GRID ** 2) - 1) // (r * r)
        require(running[0][1] < right, 'Angular cap inequality')


def vertex_bound(z, lengths):
    """Bound the signed sum of phase powers over all subset sums."""
    # Conjugation or inclusion-exclusion signs leave the set of sign vertices invariant.
    powers = [power(z, sum(sub)) for k in range(len(lengths) + 1) for sub in combinations(lengths, k)]
    largest = 0
    for signs in product((-1, 1), repeat=len(powers)):
        x = y = constant(0)
        for sign, (a, b) in zip(signs, powers):
            x = (plus if sign > 0 else minus)(x, a)
            y = (plus if sign > 0 else minus)(y, b)
        largest = max(largest, max(map(abs, x)) ** 2 + max(map(abs, y)) ** 2)
    return F(isqrt(largest) + 1, GRID)


def normalized_weight(j, lengths):
    if len(lengths) == 2:
        a, b = lengths
        return max(0, min(a - 1, j) - max(0, j - b + 1) + 1)
    a, b, c = lengths

    def triangle(k):
        return (k + 1) * (k + 2) // 2 if k >= 0 else 0
    return (triangle(j) - triangle(j-a) - triangle(j-b) - triangle(j-c)
            + triangle(j-a-b) + triangle(j-a-c) + triangle(j-b-c) - triangle(j-a-b-c))


def design(lengths, indices, keep_table=False):
    sq5 = root(constant(5))
    u = unit_phase(divide(minus(constant(3), sq5), 8))
    v = unit_phase(divide(plus(constant(3), sq5), 8))
    phases = [times(u, conjugate(v)), u, times(u, v)]
    chosen = [phases[i] for i in indices]
    population = 1
    for n in lengths:
        population *= n
    last = sum((n - 1 for n in lengths))
    phase_error = F(260 * last, GRID)
    require(phase_error < 1, 'Phase propagation requires error below one')
    raw_bound = F(0)
    for z, i in zip(chosen, indices):
        resolve(z, CAPS[i])
        raw_bound += F(CAPS[i] ** len(lengths), 2 * population) * vertex_bound(z, lengths)
    raw_bound /= len(chosen)
    # Advance both the ideal amplitude and the candidate signed controller table.
    base = centers(chosen + [u, v])
    state = [(GRID, 0)] * len(base)
    table = array('q')
    accepted = contrast = total = 0
    positive = 0
    for j in range(last + 1):
        w = normalized_weight(j, lengths)
        total += w
        prediction = sum((x[0] for x in state[:-2]))
        threshold = min(BINS, abs(prediction) * BINS // (len(chosen) * GRID))
        if prediction < 0:
            threshold = -threshold
        if keep_table:
            table.append(threshold)
        amplitude = GRID + 2 * state[-2][0] + 2 * state[-1][0]
        accepted += w * abs(threshold)
        positive += w * max(threshold, 0)
        contrast += w * threshold * (2 * amplitude ** 2 - 25 * GRID ** 2)
        state = [forward(s, b) for s, b in zip(state, base)]
    require(total == population, 'Proposal counts')
    norm = F(accepted, population * BINS)
    null = F(1, 2) + (raw_bound + (phase_error + F(1, BINS)) / 2) / norm
    ideal = F(1, 2) + F(contrast, 50 * GRID ** 2 * accepted) - 3 * phase_error
    return (null, ideal, norm, table, F(positive, accepted))


def assignment(lengths, table, uniform=randbelow):
    """Return duration and scoring sign. Draw each proposal with fresh uniforms."""
    require(len(table) == 1 + sum((x - 1 for x in lengths)), 'Timing table length')
    while True:
        j = sum((uniform(x) for x in lengths))
        h = table[j]
        if uniform(BINS) < abs(h):
            return (2 * j, h > 0)


def decision(n, p, k, tie):
    a, b = p.as_integer_ratio()
    numerator = sum((comb(n, i) * a ** i * (b - a) ** (n - i) for i in range(k + 1, n + 1)))
    return (numerator + tie * comb(n, k) * a ** k * (b - a) ** (n - k)) / b ** n


def endpoint(x, up):
    unit = 10 ** 12
    return F(-(-x * unit // 1) if up else x * unit // 1, unit)


def main():
    results = []
    designs = [
        ((1_000_000, 1_000_000), (0, 1, 2), [(57, 38, F(33, 64)), (61, 40, F(0))]),
        ((166_152, 167_983, 165_859), (0,), [(386, 226, F(769, 1024)), (389, 227, F(0))]),
    ]
    for lengths, indices, tests in designs:
        null, ideal, norm, table, always_click = design(lengths, indices, True)
        p0, p1 = (endpoint(null, True), endpoint(ideal, False))
        lower_bound = {}
        if indices == (0, 1, 2):
            # For the two rounded Bernoulli endpoints the LR increases with count.
            for k in range(57):
                hi = decision(56, p0, k, F(0))
                at = decision(56, p0, k, F(1)) - hi
                if hi <= F(1, 20) <= hi + at:
                    best = decision(56, p1, k, (F(1, 20) - hi) / at)
                    require(best < F(19, 20), 'Endpoint obstruction')
                    lower_bound = {'best_level_5pct_power_at_56': str(endpoint(best, True))}
                    break
            require(lower_bound, 'Missing endpoint boundary')
        require(assignment(lengths, table, lambda bound: 0) == (0, True), 'Zero-word assignment')
        # Force a rejected proposal at the strict boundary, then a valid negative-sign
        # setting. These inputs test the actual sampler without disclosing a live assignment.
        neg = next((j for j in range(min(lengths)) if -BINS < table[j] < 0))
        proposal = [neg] + [0] * (len(lengths) - 1)
        draws = iter(proposal + [abs(table[neg])] + proposal + [abs(table[neg]) - 1])
        require(assignment(lengths, table, lambda _: next(draws)) == (2 * neg, False), 'Boundary and negative sign')
        require(next(draws, None) is None, 'A proposal was improperly accepted')
        cases = []
        for n, k, tie in tests:
            alpha, beta = (decision(n, p0, k, tie), decision(n, p1, k, tie))
            require(alpha < F(1, 20) and beta > F(19, 20), 'Error bound exceeded')
            require(max(always_click, 1 - always_click) <= p0, 'Constant detector exceeds null')
            cases.append(dict(
                launches=n, reject_above=k, at_boundary=str(tie),
                size_ceiling=str(endpoint(alpha, True)),
                power_floor=str(endpoint(beta, False)),
            ))
        # If the device sees the sign, a deterministic click on positive settings and
        # miss on negative ones succeeds on every launch.
        require(decision(tests[0][0], F(1), tests[0][1], tests[0][2]) == 1, 'Sign disclosure control')
        results.append(dict(
            lengths=lengths, frequencies=indices, accepted_fraction=str(norm),
            always_click=str(always_click), max_ticks=2 * sum(x - 1 for x in lengths),
            null_ceiling=str(p0), ideal_floor=str(p1), decisions=cases, **lower_bound,
        ))
    print(json.dumps(results, indent=2))

if __name__ == '__main__':
    main()
