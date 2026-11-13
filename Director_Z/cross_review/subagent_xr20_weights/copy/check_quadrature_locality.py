"""Check the conditional circular-coin bound in a real circuit with a tunable phase."""
import argparse
import cmath
import json
import math
from pathlib import Path


def angular_cost(p, wrong):
    if wrong > 0.5:
        raise ValueError("Designate the more probable circular polarization as the target.")
    return math.asin(math.sqrt(p / 2) * (math.sqrt(1 - wrong) - math.sqrt(wrong)))


def measured(right, left, rejected, target):
    # Read both mutually orthogonal circular ports after accepting, and count the rest.
    good = abs((right - 1j * target * left) / math.sqrt(2)) ** 2
    bad = abs((right + 1j * target * left) / math.sqrt(2)) ** 2
    p = good + bad
    assert abs(p + sum(abs(v)**2 for v in rejected) - 1) < 2e-14
    return p, bad / p if p else None


def dark_filter(angle):
    # Reference vs the difference of two phased routes. Keep the orthogonal bright output.
    beta = 1 / math.hypot(1, math.sin(angle))
    right = beta * math.sin(angle)
    upper = beta * cmath.exp(1j * angle) / math.sqrt(2)
    lower = beta * cmath.exp(-1j * angle) / math.sqrt(2)
    left = (upper - lower) / math.sqrt(2)
    bright = (upper + lower) / math.sqrt(2)
    p, wrong = measured(right, left, [bright], 1)
    assert abs(p - 2 * math.sin(angle)**2 / (1 + math.sin(angle)**2)) < 2e-14
    bound = angular_cost(p, wrong) if p else None
    assert bound is None or bound <= angle + 2e-14
    return dict(phase_radius=angle, success=p, rejected=abs(bright)**2,
                wrong_given_success=wrong, required_radius=bound)


def extremal(angle):
    # Counterpropagating phases with a real recombiner give (cos a,i sin a).
    u, v = cmath.exp(1j * angle) / 2, cmath.exp(-1j * angle) / 2
    p, wrong = measured(u + v, u - v, [], 1)
    if angle == 0:
        wrong = 0.5
    bound = angular_cost(min(1, p), min(0.5, wrong))
    assert abs(angle - bound) < 2e-14
    return dict(phase_radius=angle, success=p, wrong_given_success=wrong, required_radius=bound)


def sharp_herald(angle):
    up = cmath.exp(1j*angle)/2
    down = cmath.exp(-1j*angle)/2
    bright, dark = up + down, up - down
    keep = math.tan(angle)
    right = keep*bright
    rejected = math.sqrt(max(0, 1-keep**2))*bright
    p, wrong = measured(right, dark, [rejected], 1)
    assert abs(p - 2*math.sin(angle)**2) < 2e-14
    bound = angular_cost(min(1,p), wrong)
    assert abs(bound-angle) < 2e-14
    return dict(phase_radius=angle, success=p, rejected=abs(rejected)**2,
                wrong_given_success=wrong, required_radius=bound)


def flagged_spinors():
    # Complex auxiliary rails on both success and failure. The distance to real rays
    # follows independently by diagonalizing the two by two real/imaginary Gram matrix.
    rows = []
    for p in (0.01, 0.25, 0.5, 1.0):
        for eta in (0.0, 0.03, 0.25, 0.5):
            for phase in (0.0, 0.8, math.pi / 2):
                for overlap in (0.0, 0.5, 1.0):
                    q = cmath.exp(1j * phase)
                    good = [math.sqrt(p * (1-eta)), 0]
                    bad = [q * overlap * math.sqrt(p*eta),
                           q * math.sqrt((1-overlap**2)*p*eta)]
                    right = [(a+b)/math.sqrt(2) for a,b in zip(good,bad)]
                    left = [1j*(a-b)/math.sqrt(2) for a,b in zip(good,bad)]
                    state = right + left + [math.sqrt(1-p)]
                    rr = sum(z.real**2 for z in state)
                    ii = sum(z.imag**2 for z in state)
                    ri = sum(z.real*z.imag for z in state)
                    # Stable small eigenvalue at ties and for real rays.
                    large = (rr+ii+math.hypot(rr-ii, 2*ri))/2
                    small = max(0.0, (rr*ii-ri**2)/large)
                    dist = math.asin(math.sqrt(small))
                    lower = angular_cost(p, eta)
                    assert dist + 2e-14 >= lower
                    if phase == 0 and overlap == 1:
                        assert abs(dist-lower) < 2e-14
                    rows.append(dict(success=p, wrong_given_success=eta, phase=phase,
                                     auxiliary_overlap=overlap, distance=dist, lower_bound=lower))
    return rows


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    directory = parser.parse_args().directory
    directory.mkdir(parents=True, exist_ok=True)
    result = dict(dark_filter=[dark_filter(a) for a in (0, 1e-6, 0.01, 0.1, 0.4, math.pi/4)],
                  sharp_herald=[sharp_herald(a) for a in (1e-6, 0.01, 0.1, 0.4, math.pi/4)],
                  deterministic=[extremal(j*math.pi/32) for j in range(9)],
                  flagged_states=flagged_spinors(),
                  scope="Real field-free input, records and controls in the tested character. "
                        "Retain all herald probabilities. A preloaded circular phase is outside this bound.")
    (directory/"quadrature_locality.json").write_bytes((json.dumps(result, indent=2)+"\n").encode())
