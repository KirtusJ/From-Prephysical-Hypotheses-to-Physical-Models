"""Check the 46-state reset model against direct five-site propagation.

Uses Python 3 and its standard library. The note supplies the all-tick proof.
"""
import cmath
import math
from fractions import Fraction


def require(condition, message):
    if not condition:
        raise ArithmeticError(message)


def port_modes():
    """Read the sharp-port spectral weights from the five Fourier blocks."""
    modes = []
    for j in range(5):
        k = 2 * math.pi * j / 5
        omega = math.asin(math.sin(k) / math.sqrt(2))
        weight = (1 + math.cos(k) / (math.sqrt(2) * math.cos(omega))) / 10
        modes.append((cmath.exp(1j * omega), weight))
        modes.append((-cmath.exp(-1j * omega), 1 / 5 - weight))
    classes = []
    for z, w in modes:
        for v, h in modes:
            theta = abs(cmath.phase(z * v.conjugate()))
            for item in classes:
                if abs(theta - item[0]) < 1e-10:
                    item[1] += w * h
                    break
            else:
                classes.append([theta, w * h])
    return sorted(classes)


def direct_step(x):
    """State order is (site 0 right, site 0 left, site 1 right, ...)."""
    y = [0.] * 10
    for site in range(5):
        right, left = x[2 * site:2 * site + 2]
        y[2 * ((site + 1) % 5)] = (right + left) / math.sqrt(2)
        y[2 * ((site - 1) % 5) + 1] = (right - left) / math.sqrt(2)
    return y


def construct(classes, damping, background, prefix):
    states = prefix + 3 * len(classes)
    transition = [[0.] * states for _ in range(states)]
    readout = [0.] * states
    x = [1.] + [0.] * 9
    for t in range(prefix):
        readout[t] = background + damping**t * (x[0]**2 - background)
        x = direct_step(x)
        if t + 1 < prefix:
            transition[t][t + 1] = 1.
    for j, (theta, weight) in enumerate(classes):
        if j == 0:
            weight -= background
        start = prefix + 3 * j
        transition[prefix - 1][start] = weight / (1 - background)
        for k in range(3):
            phase = 2 * math.pi * k / 3
            readout[start + k] = (background + (1 - background)
                                  * damping**prefix * math.cos(prefix * theta + phase))
            for increment in range(3):
                angle = theta - 2 * math.pi * increment / 3
                transition[start + k][start + (k + increment) % 3] = (
                    1 + 2 * damping * math.cos(angle)) / 3
    return transition, readout


def main():
    r, c = Fraction(1, 2), Fraction(1, 10)
    require(Fraction(15, 116) > c, 'background exceeds the constant coefficient')
    require((1 - c) * r**4 <= min(c, 1 - c), 'prefix gives insufficient readout margin')
    require(Fraction(10043, 100000)**2 / (8 * 55) == Fraction(100861849, 4400000000000), 'high-coherence threshold differs')
    classes = port_modes()
    require(len(classes) == 14 and abs(classes[0][0]) < 1e-14, 'unexpected frequency classes')
    require(abs(classes[0][1] - 15/116) < 1e-14, 'incorrect zero-frequency weight')
    require(abs(sum(weight for _, weight in classes) - 1) < 1e-14, 'spectral weights do not sum to one')
    transition, readout = construct(classes, float(r), float(c), 4)
    states = len(readout)
    p = [1.] + [0.] * (states - 1)
    x = [1.] + [0.] * 9
    max_error = 0.
    for t in range(121):
        expected = float(c) + float(r)**t * (x[0]**2 - float(c))
        max_error = max(max_error, abs(sum(a * b for a, b in zip(p, readout)) - expected))
        p = [sum(p[i] * transition[i][j] for i in range(states)) for j in range(states)]
        x = direct_step(x)
    row_residual = max(abs(sum(row) - 1) for row in transition)
    require(states == 46 and min(map(min, transition)) >= -1e-14, 'incorrect state count or negative transition')
    require(min(readout) >= 0 and max(readout) <= 1, 'readout lies outside the unit interval')
    require(row_residual < 1e-13 and max_error < 1e-13, 'propagation comparison or stochastic row sums failed')
    print(f"states = {states}; cosine frequencies = {len(classes)}")
    print(f"minimum transition = {min(map(min, transition)):.3g}")
    print(f"maximum row-sum error = {row_residual:.3g}")
    print(f"readout range = [{min(readout):.12g}, {max(readout):.12g}]")
    print(f"maximum port discrepancy at ticks 0 through 120 = {max_error:.3g}")


if __name__ == "__main__":
    main()
