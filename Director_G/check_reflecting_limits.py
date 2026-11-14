"""Compare finite reflecting walks with folded ballistic and Neumann heat moments."""

import json
from math import cos, exp, floor, fsum, pi, sqrt


LENGTHS = (32, 64, 128, 256)
MODES = (1, 2, 3)
BALLISTIC_TIMES = (0.25, 1.5)
HEAT_TIMES = (1 / 32, 0.25)
SOURCE_LIMIT = 0.25
MESH = 8192


def quantum_flight(length, start, tick):
    # H acts before the shift. A proposal across a wall stays and reverses rail.
    # All signed numerators are exact; normalization occurs only at readout.
    right, left = [0] * length, [0] * length
    right[start] = 1
    for _ in range(tick):
        plus = [r + l for r, l in zip(right, left)]
        minus = [r - l for r, l in zip(right, left)]
        right, left = [minus[0], *plus[:-1]], [*minus[1:], plus[-1]]
    totals = [r * r + l * l for r, l in zip(right, left)]
    assert sum(totals) == 2 ** tick
    return [weight / 2 ** tick for weight in totals]


def count_flight(length, start, tick):
    values = [0.0] * length
    values[start] = 1.0
    for _ in range(tick):
        neighbors_left = [values[0], *values[:-1]]
        neighbors_right = [*values[1:], values[-1]]
        values = [(left + right) / 2 for left, right in zip(neighbors_left, neighbors_right)]
    return values


def cosine_moment(values, mode):
    length = len(values)
    return fsum(p * cos(mode * pi * (x + 0.5) / length) for x, p in enumerate(values))


def bloch_moment(source, tau, mode, panels):
    # For Fourier phase +ikx the velocities are v,-v and the R-column
    # spectral weights are (1+v)/2,(1-v)/2. Cosine is even and 2-periodic
    # in scaled position, so folding an unfolded trajectory leaves it unchanged.
    def at(k):
        c = cos(k)
        v = c / sqrt(1 + c * c)
        return sum((1 + velocity) * cos(mode * pi * (source + tau * velocity)) / 2
                   for velocity in (v, -v))

    return fsum(at((j + 0.5) * 2 * pi / panels) for j in range(panels)) / panels


def main():
    ballistic, heat = [], []
    limits = {(tau, mode): bloch_moment(SOURCE_LIMIT, tau, mode, MESH)
              for tau in BALLISTIC_TIMES for mode in MODES}
    coarse = {(tau, mode): bloch_moment(SOURCE_LIMIT, tau, mode, MESH // 2)
              for tau in BALLISTIC_TIMES for mode in MODES}
    for length in LENGTHS:
        start = floor(SOURCE_LIMIT * length)
        for tau in BALLISTIC_TIMES:
            tick = floor(tau * length)
            law = quantum_flight(length, start, tick)
            moments = []
            for mode in MODES:
                measured = cosine_moment(law, mode)
                reference = limits[tau, mode]
                moments.append({"mode": mode, "finite": measured, "limit_quadrature": reference,
                                "absolute_difference": abs(measured - reference),
                                "absolute_quadrature_mesh_change": abs(reference - coarse[tau, mode])})
            ballistic.append({"length": length, "start": start, "ticks": tick, "tau": tau,
                              "mass_sum_error": abs(fsum(law) - 1), "moments": moments})
        for s in HEAT_TIMES:
            tick = floor(s * length ** 2)
            law = count_flight(length, start, tick)
            moments = []
            for mode in MODES:
                measured = cosine_moment(law, mode)
                finite_eigen = cos(mode * pi / length) ** tick * cos(mode * pi * (start + 0.5) / length)
                reference = exp(-s * (mode * pi) ** 2 / 2) * cos(mode * pi * SOURCE_LIMIT)
                moments.append({"mode": mode, "finite": measured, "finite_eigenvalue_formula": finite_eigen,
                                "absolute_finite_formula_difference": abs(measured - finite_eigen),
                                "limit": reference, "absolute_difference": abs(measured - reference)})
            heat.append({"length": length, "start": start, "ticks": tick, "s": s,
                         "mass_sum_error": abs(fsum(law) - 1), "moments": moments})
    print(json.dumps({"source": "sharp right rail at floor(L/4), positive reflection at both ends",
                      "observable": "cos(m*pi*(x+1/2)/L)",
                      "difference": "absolute scalar moment difference from limit at y0=1/4",
                      "quadrature": "periodic midpoint average of both Bloch bands, 8192 and 4096 points",
                      "ballistic_wall_control": "At tau=1.5 both y0 +/- tau/sqrt(2) extend past a wall.",
                      "ballistic": ballistic, "heat": heat}, indent=2))


if __name__ == "__main__":
    main()
