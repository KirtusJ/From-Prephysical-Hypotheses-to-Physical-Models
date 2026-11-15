"""Exact stationary word, endpoint, and preparation checks for a swept target register."""
from fractions import Fraction as F
from itertools import product
from math import comb


PRIOR = (F(55, 128), F(73, 128))
TARGET = (F(467, 880), F(173, 1168))
HERALD = (F(45, 1024), F(925, 1024))
RETURN = tuple(F(1, 8) + b/4 for b in HERALD)


def words(n):
    return product((0, 1), repeat=n)


def mixture(n, successes):
    return sum(w * a**successes * (1-a)**(n-successes) for w, a in zip(PRIOR, TARGET))


def setup(k):
    rows = []
    for ones in range(k):
        ratio = mixture(k, ones+1)/mixture(k, ones)
        rows.append((ratio.denominator, ratio.numerator))
    bits = (2 * max(a+b for a, b in rows) - 1).bit_length()
    return rows, 1 << bits


def step(q, rows, denom):
    a, b = rows[sum(q[1:])]
    flip = F(a if q[0] else b, denom)
    return ((q[1:] + (q[0],), 1-flip), (q[1:] + (1-q[0],), flip))


def full_word_check(k):
    rows, denom = setup(k)
    initial = {q: mixture(k, sum(q)) for q in words(k)}
    assert sum(initial.values()) == 1
    outgoing = dict.fromkeys(initial, F())
    for q, prob in initial.items():
        for new_q, weight in step(q, rows, denom):
            assert weight > 0 and weight.denominator & (weight.denominator-1) == 0
            outgoing[new_q] += prob * weight
    assert outgoing == initial

    # Generate actual emitted words from full register transitions, retaining
    # correlation between the twice-read slot and the first emitted target.
    law = {(q, ()): prob for q, prob in initial.items()}
    for _ in range(k+1):
        following = {}
        for (q, word), mass in law.items():
            for new_q, weight in step(q, rows, denom):
                key = (new_q, word+(q[0],))
                following[key] = following.get(key, 0) + mass*weight
        law = following
    observed = dict.fromkeys(words(k+1), F())
    for (_, word), mass in law.items():
        observed[word] += mass
    assert all(observed[u+(0,)]+observed[u+(1,)] == initial[u] for u in initial)
    assert all(observed[(0,)+u]+observed[(1,)+u] == initial[u] for u in initial)

    # Apply the physical binary read channel on every clock independently.
    def read_returns(target_law):
        panel = target_law.copy()
        for t in range(k+1):
            output = {}
            for u, mass in panel.items():
                q = RETURN[u[t]]
                for r, chance in ((0, 1-q), (1, q)):
                    v = u[:t]+(r,)+u[t+1:]
                    output[v] = output.get(v, 0) + mass*chance
            panel = output
        return panel

    held = {u: mixture(k+1, sum(u)) for u in observed}
    fixed, old = read_returns(observed), read_returns(held)
    tv = sum(abs(fixed[u]-old[u]) for u in fixed)/2
    matched = sum(fixed[u]-old[u] for u in fixed if u[0] == u[-1])
    assert tv == matched == agreement_gap(k)


def agreement_gap(k):
    rows, denom = setup(k)
    total = F()
    for r, (a, b) in enumerate(rows):
        mu = mixture(k-1, r)
        q = mixture(k, r+1)/mu
        posterior_variance = mixture(k+1, r+2)/mu - q*q
        excess = (1-F(a+b, denom))*q*(1-q)-posterior_variance
        assert excess >= F(7, 1024)
        total += comb(k-1, r)*mu*excess
    return 2*(RETURN[1]-RETURN[0])**2 * total


def check_preload(k, bits):
    rows, denom = setup(k)
    grid = 1 << bits
    rounded = [F(round(grid*a), grid) for a in TARGET]
    bound = F(k, 2*grid)
    target = {q: mixture(k, sum(q)) for q in words(k)}
    start = {}
    for q in target:
        r = sum(q)
        start[q] = sum(w*a**r*(1-a)**(k-r) for w, a in zip(PRIOR, rounded))
    assert sum(start.values()) == 1
    for _ in range(2*k+1):
        assert sum(abs(start[q]-target[q]) for q in start)/2 <= bound
        future = dict.fromkeys(start, F())
        for q, mass in start.items():
            for new_q, weight in step(q, rows, denom):
                future[new_q] += mass*weight
        start = future


def main():
    for k in range(1, 6):
        full_word_check(k)
        check_preload(k, 5)
    sharp = F(8090335, 1224736768)
    assert agreement_gap(1) == sharp
    for k in (1, 2, 3, 4, 8, 16, 32):
        assert all(mixture(k, j).denominator == 16*64240**(k-1) for j in range(k+1))
        assert agreement_gap(k) >= sharp
        _, denom = setup(k)
        print(f"K={k}, fair bits/update={denom.bit_length()-1}, "
              f"return-agreement gap={float(agreement_gap(k)):.8f}")
    prob_hh = sum(w*(HERALD[0]+a*(HERALD[1]-HERALD[0]))**2
                  for w, a in zip(PRIOR, TARGET))
    prob_rr = sum(w*(RETURN[0]+a*(RETURN[1]-RETURN[0]))**2
                  for w, a in zip(PRIOR, TARGET))
    assert (prob_hh, prob_rr) == (F(145, 1168), F(401, 9344))
    tape_excess = (RETURN[1]-RETURN[0])**2 * sum(w*a*(1-a) for w, a in zip(PRIOR, TARGET))
    assert tape_excess == F(10117855, 1224736768)
    print(f"Two-herald and two-return probabilities from held launches: {prob_hh}, {prob_rr}.")


if __name__ == "__main__":
    main()
