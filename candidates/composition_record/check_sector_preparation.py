"""Replay contact-order selection and compare the two prepared physical flights."""
from collections import defaultdict
from cmath import exp
from math import ceil, comb, cos, floor, isqrt, pi, sin, sqrt
import json
from pathlib import Path

from check_contact_flight import actual_contacts, decoded


def multiply_word(word, p):
    r = l = z = 0
    for dr, dl in word:
        z = (z + pow(2, -1, p) * (r*dl - l*dr)) % p
        r, l = (r + dr) % p, (l + dl) % p
    return r, l, z


def order_pair(s, side):
    right, left = (1, 0), (0, 1)
    base = [left]*side + [right]*side
    full, partial = divmod(s, side)
    if full == side:
        return base, [right]*side + [left]*side
    # The number of R-before-L pairs is the required excess area.
    return base, ([right]*full + [left]*(side-partial) + [right] +
                  [left]*partial + [right]*(side-full-1))


def mask(s, p):
    residue = 2*s % p
    return 1 if min(residue, p-residue) <= p//4 else -1


def score(k, p):
    return sum(mask(s, p)*cos(2*pi*(s*k % p)/p) for s in range(p))/p


def score_formula(k, p):
    n = k * pow(2, -1, p) % p
    if n == 0:
        return (2*(2*(p//4)+1)-p)/p
    n = min(n, p-n)
    return 2*sin((2*(p//4)+1)*pi*n/p)/(p*sin(pi*n/p))


def binomial_acceptance(mu, rounds):
    # Score threshold 1/2 corresponds to a fraction of +1 of at least 3/4.
    positive = (1+mu)/2
    return sum(comb(rounds, k)*positive**k*(1-positive)**(rounds-k)
               for k in range(ceil(3*rounds/4), rounds+1))


def replay_selector(p, rounds):
    side = isqrt(p-2)+1
    triplets = []
    for s in range(p):
        base, shifted = order_pair(s, side)
        undo = [(-dr, -dl) for dr, dl in reversed(base)]
        assert multiply_word(base+undo, p) == (0, 0, 0)
        assert multiply_word(shifted+undo, p) == (0, 0, s)
        # Keep the order, including zero shift and all endpoint ties.
        triplets.append({"s": s, "sign": mask(s, p)})
    means = [score(k, p) for k in range(p)]
    assert max(abs(mu-score_formula(k, p)) for k, mu in enumerate(means)) < 1e-13
    targets = {2, p-2}
    assert min(means[k] for k in targets) > 2/pi
    assert max(abs(mu) for k, mu in enumerate(means) if k not in targets) <= 1/3
    passing = [binomial_acceptance(mu, rounds) for mu in means]
    incident = sum(passing)/p
    return {"prime": p, "side": side, "contacts_per_query": 4*side,
            "settings": triplets, "means": means, "passes_by_sector": passing,
            "incident_pass_rate": incident,
            "folded_weight_after_pass": sum(passing[k] for k in targets)/sum(passing)}


def phase_offset(theta, p):
    return (pow(2, -1, p)*floor(-p*theta/(2*pi)+0.5)) % p


def flight_check(p, ticks):
    # Nonadjacent sites of one parity interfere after propagation. The
    # amplitudes are deliberately unequal and signs/phases are not symmetric.
    profile = {-3: 1, -1: 2, 1: 3, 3: 1}
    initial, encoded = {}, {}
    for x, amplitude in profile.items():
        for rail in (1, -1):
            theta = -pi*(x+(rail == -1))/2 + 0.13*x
            offset = phase_offset(theta, p)
            initial[x, rail, offset] = amplitude
            encoded[x, rail, x*pow(2,-1,p)%p, -x*pow(2,-1,p)%p,
                    (offset+x*pow(4,-1,p))%p] = amplitude
            assert abs(exp(-4j*pi*offset/p)-exp(1j*theta)) <= pi/p + 1e-13
    out = decoded(actual_contacts(encoded, ticks, p), ticks, p)
    fibers = {}
    for k in (2, -2):
        reduced = defaultdict(complex)
        for (x, rail, z), a in initial.items():
            reduced[x, rail] += a*exp(-2j*pi*(k*z % p)/p)
        for _ in range(ticks):
            following = defaultdict(complex)
            for (x, incoming), a in reduced.items():
                phase = exp(-2j*pi*(x*(k//2) % p)/p)
                following[x+1, 1] += phase*a
                following[x-1, -1] += phase*a*incoming
            reduced = following
        actual = defaultdict(complex)
        for (x, rail, z), a in out.items():
            actual[x, rail] += a*exp(-2j*pi*(k*z % p)/p)
        assert max(abs(actual[port]-a) for port, a in reduced.items()) < 1e-10
        fibers[k] = reduced
    norm = 2*sum(a*a for a in profile.values())*2**ticks
    assert abs(sum(abs(a)**2 for a in fibers[2].values())/norm - 1) < 1e-12
    assert max(abs(a.conjugate()-fibers[-2][port])
               for port, a in fibers[2].items()) < 1e-10
    return [{"site": x, "rail": rail, "probability": abs(a)**2/norm}
            for (x, rail), a in sorted(fibers[2].items())]


def main():
    rounds = 64
    primes = (5, 7, 11, 13, 17, 31, 61, 127)
    result = {"rounds": rounds, "selector": [replay_selector(p, rounds) for p in primes],
              "packet": [{"prime": p, "ticks": n, "ports": flight_check(p, n)}
                         for p in (5, 11, 31) for n in (0, 1, 4, 9)]}
    print(json.dumps(result, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
