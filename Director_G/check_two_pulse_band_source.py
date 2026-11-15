"""Replay signed position paths, pulse steering, and an end-to-end field release."""

import cmath
import itertools
import math
from fractions import Fraction

from check_tagged_transport_band import I, ROOT2, fibre, mul, projector, require


def power(matrix, ticks):
    result = I
    while ticks:
        if ticks % 2:
            result = mul(result, matrix)
        matrix = mul(matrix, matrix)
        ticks //= 2
    return result


def act(matrix, vector):
    return tuple(row[0]*vector[0]+row[1]*vector[1] for row in matrix)


def flip(vector):
    return vector[0], -vector[1]


def durations(switches, stays):
    peak = math.atan(math.sqrt(switches/stays))
    frequency = math.asin(math.sin(peak)/ROOT2)
    times = [2*math.ceil(theta/(4*frequency)-0.5) for theta in (math.pi/2, math.pi/4)]
    return peak, times


def steer(k, times, spin):
    for ticks in times:
        spin = flip(act(power(fibre(k), ticks), spin))
    return spin


def signed_tick(sites):
    result = {}
    for x, (right, left) in sites.items():
        result.setdefault(x+1, [0, 0])[0] = right+left
        result.setdefault(x-1, [0, 0])[1] = right-left
    return result


def rail_word(word):
    # Raw unnormalized integer tallies. Discard the other rail at each read.
    sites = {0: (1, 0)}
    for rail in word:
        moved = signed_tick(signed_tick(sites))
        sites = {x: (r, 0) if rail == 1 else (0, l)
                 for x, (r, l) in moved.items() if (r if rail == 1 else l)}
    return sites


def count_word(word):
    return sum(before != after for before, after in zip((1,)+word, word))


def central_mass(count):
    return Fraction(math.comb(2*count, count), 4**count)


def check_incident():
    for depth in range(1, 9):
        yields = [Fraction(0) for _ in range(depth+1)]
        for word in itertools.product((1, -1), repeat=depth):
            switched = count_word(word)
            stayed = depth-switched
            tallies = rail_word(word)
            weights = {x: r*r+l*l for x, (r, l) in tallies.items()}
            total = sum(weights.values())
            prob = Fraction(total, 4**depth)
            expected = central_mass(switched)*central_mass(stayed)
            require(prob*math.comb(depth, switched) == expected, "fine word")
            yields[switched] += prob
            centre = sum(word)
            require(sum(x*w for x, w in weights.items()) == centre*total, "site centre")
            if switched and stayed:
                variance = depth*(Fraction(switched, 2*switched-1)+Fraction(stayed, 2*stayed-1))
                require(sum((x-centre)**2*w for x, w in weights.items()) == variance*total,
                        "site width")
        require(sum(yields) == 1, "all incident launches")
        if depth == 8:
            print("D=8, retained counts 2..4, plus/minus/reject:",
                  yields[2]+yields[4], yields[3], 1-sum(yields[2:5]))


def wrong_band(k, sign, spin):
    # Project onto the analytic plus branch, then choose the wrong signed velocity.
    projected = act(projector(k), spin)
    if sign*math.cos(k) >= 0:
        projected = tuple(x-y for x, y in zip(spin, projected))
    return sum(abs(x)**2 for x in projected)


def integrated_control(depth, switched):
    stayed = depth-switched
    peak, times = durations(switched, stayed)
    sign = (-1)**switched
    spin = (1, 0) if sign == 1 else (0, 1)
    # All four chart masses have identical leaks. Check their direct matrices first.
    for k in (peak/2, peak, 1.4*peak):
        reference = wrong_band(k, sign, steer(k, times, spin))
        for replica in (-k, k-math.pi, math.pi-k):
            require(abs(wrong_band(replica, sign, steer(replica, times, spin))-reference) < 1e-12,
                    "conjugate or parity chart")
    grid = 16*math.isqrt(depth)
    norm = leak = unpulsed = 0.0
    for i in range(grid):
        k = (i+0.5)*math.pi/(2*grid)
        log_weight = (switched*math.log(math.sin(k)/math.sin(peak))
                      + stayed*math.log(math.cos(k)/math.cos(peak)))
        weight = math.exp(2*log_weight)
        # Values that underflow to zero make exactly zero contribution in binary64.
        if weight:
            norm += weight
            leak += weight*wrong_band(k, sign, steer(k, times, spin))
            unpulsed += weight*wrong_band(k, sign, spin)
    leak /= norm
    unpulsed /= norm
    radius = peak+1/math.sqrt(2*depth)
    bound = (sum(times)/math.sqrt(2*depth)+2*math.asin(math.sin(peak)/ROOT2)
             + (2*ROOT2+1/ROOT2)*radius)
    require(math.sqrt(leak) <= bound+1e-12, "finite band estimate")
    require(unpulsed >= (1-1/ROOT2)/2-1e-12, "unpulsed floor")
    if depth == 2**20:
        require(leak < 0.01, "finite one-percent wrong-band control")
    print(f"D={depth} A={switched} T={times} leak={leak:.8f} unpulsed={unpulsed:.8f}")


def check_terminal(word, slope, steps):
    # Direct line propagation includes the recorded centre, phases and both pulse signs.
    sites = rail_word(word)
    factor = 2**(-len(word))
    sites = {x: (r*factor, l*factor) for x, (r, l) in sites.items()}
    switches = count_word(word)
    stays = len(word)-switches
    _, times = durations(switches, stays)
    for ticks in times:
        for _ in range(ticks):
            sites = {x: (r/ROOT2, l/ROOT2) for x, (r, l) in signed_tick(sites).items()}
        sites = {x: flip(v) for x, v in sites.items()}
    for _ in range(steps):
        phased = {x: tuple(cmath.exp(-1j*slope*x)*z/ROOT2 for z in v) for x, v in sites.items()}
        sites = signed_tick(phased)

    # A padded inverse DFT gives independent per-port complex amplitudes, including phases.
    radius = 2*len(word)+sum(times)+steps
    size = 2*radius+1
    transform = []
    for idx in range(size):
        final_k = 2*math.pi*idx/size
        k = final_k+steps*slope
        envelope = (-1j)**switches*cmath.exp(-1j*sum(word)*k)*math.sin(k)**switches*math.cos(k)**stays
        spin = (envelope, 0) if word[-1] == 1 else (0, envelope)
        spin = steer(k, times, spin)
        for j in range(1, steps+1):
            spin = act(fibre(k-j*slope), spin)
        transform.append(spin)
    for x in range(-radius, radius+1):
        expected = sites.get(x, (0, 0))
        for rail in (0, 1):
            value = sum(cmath.exp(2j*math.pi*i*x/size)*v[rail]
                        for i, v in enumerate(transform))/size
            require(abs(value-expected[rail]) < 2e-13, "field release port")
    mass = sum(abs(v)**2 for spin in sites.values() for v in spin)
    expected_mass = central_mass(switches)*central_mass(stays)/math.comb(len(word), switches)
    require(abs(mass-float(expected_mass)) < 2e-13, "incident joint flight weight")


def check_position_control():
    # For a fixed count, every word differs only by its recorded translation.
    for word, joint_rates in [((-1,)*16, (456091, 1119736)),
                              ((-1,)+(1,)*15, (677691, 904110))]:
        count = count_word(word)
        stays = len(word)-count
        tag_rate = central_mass(count)*central_mass(stays)
        _, times = durations(count, stays)
        for apply_pulses, rounded in zip((True, False), joint_rates):
            sites = rail_word(word)
            for ticks in times:
                for _ in range(ticks):
                    sites = signed_tick(sites)
                if apply_pulses:
                    sites = {x: flip(v) for x, v in sites.items()}
            for _ in range(127):
                sites = signed_tick(sites)
            weights = {x: r*r+l*l for x, (r, l) in sites.items()}
            centre = sum(word)
            require(weights.get(centre, 0) == 0, "undisclosed tie")
            wrong = sum(w for x, w in weights.items() if word[-1]*(x-centre) < 0)
            joint = tag_rate*Fraction(wrong, sum(weights.values()))
            require(round(10**8*joint) == rounded, "incident wrong-side control")


if __name__ == "__main__":
    check_incident()
    check_position_control()
    for sample_depth in (2**12, 2**16, 2**20):
        for count in (math.isqrt(sample_depth), math.isqrt(sample_depth)+1):
            integrated_control(sample_depth, count)
    for sample_word in ((1, -1, -1, 1, 1, 1), (-1, 1, -1, -1, -1, -1)):
        for field in (-0.074, 0.0, 0.074):
            check_terminal(sample_word, field, 9)
    print("PASS: incident words, four wrong-side rates and six line/Fourier terminal comparisons")
