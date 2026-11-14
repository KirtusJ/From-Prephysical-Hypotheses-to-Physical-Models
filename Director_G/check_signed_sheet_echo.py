"""Check the fixed-point echo on physical data and sheet coordinates."""

from argparse import ArgumentParser
from fractions import Fraction as Q
import json
from pathlib import Path


def require(ok, message):
    if not ok:
        raise ValueError(message)


def compose(a, b):
    return [[sum(x*y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def act(a, v):
    return [sum(x*y for x,y in zip(row,v)) for row in a]


def norm(v):
    return sum(x*x for x in v)


def data_echo(r, t):
    # [[r,-t],[t,r]] on data, copied identically on every sheet address.
    w = [[r,-t],[t,r]]
    return [[w[i//3][j//3] if i%3 == j%3 else 0 for j in range(6)] for i in range(6)]


def cycle(on_blank, direction=1):
    gate = [[0]*6 for _ in range(6)]
    for j in range(6):
        d, s = divmod(j,3)
        if on_blank is None or (d == 0) == on_blank:
            gate[3*d+(s+direction)%3][j] = -1
        else:
            gate[j][j] = 1
    return gate


def advance(v, phase0, phase1):
    return compose(v, compose(phase0, compose(list(zip(*v)), compose(phase1, v))))


def panel(r, t, sheet, reduced):
    require(r*r+t*t == 1, "unitary data preparation")
    start = sheet + [0]*3
    v = data_echo(r,t)
    phase1 = cycle(True,-1) if reduced else cycle(False)
    masses = []
    physical = []
    for k in range(4):
        state = act(v,start)
        require(norm(state) == norm(start), "all physical norm retained")
        masses.append(norm(state[:3])/Q(norm(start)))
        physical.append(state if k <= 1 else None)
        if k < 3:
            v = advance(v,cycle(True),phase1)
    return masses, physical[:2]


def main():
    args = ArgumentParser(description=__doc__)
    args.add_argument("output_file", type=Path)
    out = args.parse_args().output_file
    pairs = [(Q(0),Q(1)),(Q(1),Q(0)),(Q(3,5),Q(4,5)),(Q(4,5),Q(3,5))]
    require(compose(cycle(None), cycle(True,-1)) == cycle(False), "complement mask identity")
    clean_checks = 0
    for r,t in pairs:
        for sheet in ([1,-1,0],[0,1,-1],[1,1,-2]):
            for reduced in (False,True):
                masses, _ = panel(r,t,sheet,reduced)
                require(masses == [(r*r)**(3**k) for k in range(4)], "cubic blank mass")
                clean_checks += len(masses)
    b = Q(144,169)
    r,t = Q(12,13), Q(5,13)
    clean, ports = panel(r,t,[1,-1,0],False)
    reduced, _ = panel(r,t,[1,-1,0],True)
    dirty, _ = panel(r,t,[1,0,0],False)
    require(clean == reduced, "pooled complement and single-address circuits agree")
    require(ports[1] == [0, -Q(1728,2197), Q(1728,2197), -Q(5,13), -Q(720,2197), Q(1565,2197)],
            "named first-step amplitudes in increasing data and sheet order")
    require(sum(ports[1][:3]) == sum(ports[1][3:]) == 0, "zero sum in each physical data row")
    require(dirty[1] == (2*b**3 + b*(4*b-3)**2)/3 and dirty[1] != clean[1],
            "localized sheet retains a one-third contaminating sector")
    require(Q(1,2)**3 == Q(1,8) and
            (2*Q(1,2)**3 + Q(1,2)*(4*Q(1,2)-3)**2)/3 == Q(1,4),
            "localized-sheet control on a balanced data splitter")
    result = dict(depths=[0,1,2,3], clean_mass_checks=clean_checks,
                  data_column=[r,t], initial_blank_mass=b,
                  depth_one_unnormalized_ports=ports[1], input_squared_norm=2,
                  clean_blank_mass=clean[1], localized_blank_mass=dirty[1],
                  balanced_data_clean="1/8", balanced_data_localized="1/4")
    with out.open("x",encoding="utf-8",newline="\n") as f:
        json.dump(result,f,indent=2,default=str)
        f.write("\n")


if __name__ == "__main__":
    main()
