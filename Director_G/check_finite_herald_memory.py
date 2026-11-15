"""Exact word laws for a held walk herald and its finite-memory rival."""
from fractions import Fraction as F
from itertools import product


PRIOR = (F(55, 128), F(73, 128))
RATES = (F(1, 2), F(25, 146))
RETURN = (F(1, 8), F(3, 8))
RETURN_CHANNEL = tuple({0: 1-q, 1: q} for q in RETURN)
SITES = (-4, -2, 0, 2, 4)
DISPLACEMENT_CHANNEL = tuple(dict(zip(SITES, (F(a, 16) for a in row)))
                             for row in ((1, 6, 2, 6, 1), (1, 4, 6, 4, 1)))


def words(length):
    return product((0, 1), repeat=length)


def likelihood(rate, word):
    good = sum(word)
    return rate ** good * (1 - rate) ** (len(word) - good)


def held(word):
    return sum(w * likelihood(p, word) for w, p in zip(PRIOR, RATES))


def rival(word, k):
    memory = k - 1
    prefix = word[:memory]
    mass = held(prefix)
    for j in range(memory, len(word)):
        past = word[j-memory:j]
        mass *= held(past + (word[j],)) / held(past)
    return mass


def read_channel(herald_law, channel):
    """Apply the same independent displacement or return channel on each axis."""
    result = herald_law.copy()
    n = len(next(iter(result)))
    for axis in range(n):
        output = {}
        for u, mass in result.items():
            for r, chance in channel[u[axis]].items():
                v = u[:axis] + (r,) + u[axis+1:]
                output[v] = output.get(v, 0) + mass * chance
        result = output
    return result


def verify(k):
    for u in words(k-1):
        assert sum(held((h,) + u) for h in (0, 1)) == held(u)
        assert sum(held(u + (h,)) for h in (0, 1)) == held(u)
    assert all(held(u) == rival(u, k) for u in words(k))
    length = k + 1
    a = {u: held(u) for u in words(length)}
    b = {u: rival(u, k) for u in words(length)}
    assert sum(a.values()) == sum(b.values()) == 1
    assert a[(1,) * length] > b[(1,) * length]
    variance = F()
    for u in words(k-1):
        weights = [w * likelihood(p, u) / held(u) for p, w in zip(RATES, PRIOR)]
        variance += held(u) * weights[0] * weights[1] * (RATES[0]-RATES[1])**2
    assert sum(abs(a[u]-b[u]) for u in a)/2 == 2 * variance
    r, s = read_channel(a, RETURN_CHANNEL), read_channel(b, RETURN_CHANNEL)
    variation = sum(abs(r[u]-s[u]) for u in r)/2
    agreement = sum(r[u]-s[u] for u in r if u[0] == u[-1])
    assert agreement == variation == variance/8 and variation > 0
    if k <= 3:
        x = read_channel(a, DISPLACEMENT_CHANNEL)
        y = read_channel(b, DISPLACEMENT_CHANNEL)
        assert sum(abs(x[u] - y[u]) for u in x)/2 == variation
    return variation


def check_inverse():
    for rho in (F(0), F(1, 7), F(5, 8), F(1)):
        def word_probability(u):
            value = F()
            for path in words(len(u)):
                mass = PRIOR[path[0]]
                for i, j in zip(path, path[1:]):
                    mass *= rho * (i == j) + (1-rho) * PRIOR[j]
                for j, observation in zip(path, u):
                    q = RETURN[0] + (RETURN[1]-RETURN[0]) * RATES[j]
                    mass *= q if observation else 1-q
                value += mass
            return value

        law = {u: word_probability(u) for u in words(4)}
        mean = sum(prob for u, prob in law.items() if u[0])

        def central(positions):
            ans = F()
            for u, prob in law.items():
                for j in positions:
                    prob *= u[j] - mean
                ans += prob
            return ans

        c1, c2 = central((0, 1)), central((0, 2))
        third, fourth = central((0, 1, 2)), central((0, 1, 2, 3))
        if rho == 0:
            assert all(law[u] == likelihood(mean, u) for u in law)
            continue
        assert c2/c1 == rho
        variance, delta = c1**2/c2, third/c2
        for rate in RATES:
            z = RETURN[0] + (RETURN[1]-RETURN[0])*rate - mean
            assert z*z == variance + delta*z
        assert fourth == c1**2 + third**2/c1


if __name__ == "__main__":
    check_inverse()
    for k in range(1, 9):
        advantage = verify(k)
        print(f"K={k}: exact binary laws agree through K; endpoint agreement gap "
              f"{float(advantage):.10g} (rounded)")
