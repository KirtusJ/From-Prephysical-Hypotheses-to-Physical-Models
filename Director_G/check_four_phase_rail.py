"""Exact two-well four-setting experiment and independent boundary controls."""
import argparse
from fractions import Fraction as Q
import json
from pathlib import Path

from check_clock_feedback import Quad, ONE, ZERO, ROOT_TWO, HALF


def require(test, label):
    if not test:
        raise ArithmeticError(label)


def phase(vector, eighths):
    """Diagonal rail phase on the Bloch vector, in Q(sqrt(2))."""
    x, y, z = vector
    diagonal = ROOT_TWO * HALF
    cosines = (ONE, diagonal, ZERO, ZERO-diagonal, ZERO-ONE, ZERO-diagonal, ZERO, diagonal)
    c, s = cosines[eighths % 8], cosines[(eighths - 2) % 8]
    return (c*x - s*y, s*x + c*y, z)


def output(program):
    state = (ZERO, ZERO, ONE)
    for phase_index in program:
        x, y, z = state
        state = phase((z, ZERO-y, x), phase_index)
        require(sum((r*r for r in state), ZERO) == ONE, "coherent norm")
    require(state[2].b == 0, "terminal z is rational")
    return state[2].a


def detector(x, order):
    return (1 + x**order) / 2


def means(values, split=Q(1, 2)):
    return [split*values[j] + (1-split)*values[j+2] for j in (0, 1)]


def rail_panel():
    rows = []
    for j in range(4):
        # U_phi = D_phi H. [0,k] implements D_{k*pi/4}; H D H uses four ticks.
        program = [0, 0, 1, 0] + [0, 2*j] + [0, 0, -1, 0]
        require(len(program) == 10, "shared terminal clock")
        z = output(program)
        rows.append(dict(j=j, phase_eighths=program, terminal_z=z,
                         ordinary=detector(z, 1), cubic=detector(z, 3)))
    coordinates = [row["terminal_z"] for row in rows]
    require(coordinates == [1, Q(1, 2), 0, Q(1, 2)], "measured geometry")
    ordinary = [row["ordinary"] for row in rows]
    cubic = [row["cubic"] for row in rows]
    require(means(ordinary) == [Q(3,4)]*2, "ordinary means")
    require(means(cubic) == [Q(3,4), Q(9,16)], "cubic means")
    require(means(ordinary, Q(3,4)) == [Q(7,8), Q(3,4)], "biased choice")
    # Detection probability one on j=0 and 1/2 on j=2. Pooled conditional
    # probability differs from equal weighting before conditioning.
    retained_even = (ordinary[0] + ordinary[2]/2) / (1+Q(1,2))
    require(retained_even == Q(5,6), "pooled postselection")
    return dict(rows=rows, balanced_ordinary=means(ordinary), balanced_cubic=means(cubic),
                biased_ordinary=means(ordinary, Q(3,4)),
                unequal_retention_even_conditional=retained_even)


def recurrence(t, function):
    if abs(t) == 1:
        return [], []
    chain, defects = [], []
    while abs(t) != 1:
        sign = 1 if t >= 0 else -1
        child = 2*t-sign
        defect = function(t) - (function(Q(sign))+function(child))/2
        chain.append(t)
        defects.append(defect)
        t = child
    return chain, defects


def finite_controls():
    rows = []
    for index in range(-32, 33):
        t = Q(index, 32)
        chain, diffs = recurrence(t, lambda x: detector(x,3))
        accumulated = sum((value/2**i for i,value in enumerate(diffs)), Q(0))
        require(accumulated == detector(t,3)-detector(t,1), "discounted error")
        require(not any(recurrence(t, lambda x: detector(x,1))[1]), "ordinary recurrence")
        rows.append(dict(t=t, chain=chain, defects=diffs, total_error=accumulated))
    return rows


def finite_alias(t):
    """Cubic calibration alone cannot certify a finite set of angles."""
    return detector(t,1) + t*(1-t*t)*(t*t-Q(1,4))**2/4


def edge_controls():
    seen = [Q(-1), Q(-1,2), Q(0), Q(1,2), Q(1)]
    require(all(finite_alias(t) == detector(t,1) for t in seen), "finite alias")
    test = Q(1,4)
    require(finite_alias(test) != detector(test,1), "off-panel alias")
    for j in range(-64,65):
        t = Q(j,64)
        require(0 <= finite_alias(t) <= 1 and finite_alias(t)+finite_alias(-t)==1, "valid two-rail probabilities")
        require(detector(t,3)+detector(-t,3)==1,"great-circle means")
    axis_cos = Q(7,25)
    axis_sin = Q(24,25)
    eta = (1-axis_cos)/2
    require(axis_cos**2 + axis_sin**2 == 1, "tilted detector")
    require(((axis_cos-1)**2 + axis_sin**2)/4 == eta, "sqrt(eta) sharpness")
    return dict(finite_seen=seen, unseen=test, unseen_ordinary=detector(test,1),
                unseen_alternative=finite_alias(test), clifford_cubic_equal=[detector(t,1)==detector(t,3) for t in (-1,0,1)],
                tilted_detector_cos=axis_cos, endpoint_error=eta, worst_error_squared=eta)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    target = parser.parse_args().output / "four_phase_rail.json"
    results = dict(ten_tick_panel=rail_panel(), dyadic_orbits=finite_controls(), alternatives=edge_controls())
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("x", encoding="utf8", newline="\n") as stream:
        json.dump(results, stream, indent=2, default=str)
        stream.write("\n")


if __name__ == "__main__":
    main()
