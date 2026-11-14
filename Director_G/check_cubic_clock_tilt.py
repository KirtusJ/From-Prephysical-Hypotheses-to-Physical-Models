"""Exact cubic phase programs for a finite-clock constraint on a sharp detector."""
from argparse import ArgumentParser
from decimal import Decimal, localcontext
from fractions import Fraction as Q
import json
from pathlib import Path


NORTH = (Q(0), Q(0), Q(1))
D = (0, 1)        # chronological U_0 then U_1 gives diag(1,omega)
H = (0,)
RX = H + D + H
B = RX + D
IDENTITY = (0, 0)
REFERENCES = (NORTH, (0, Q(1,2), Q(-1,2)), (Q(-3,4), Q(-1,4), Q(-1,2)),
              (Q(3,4), Q(-1,4), Q(-1,2)))


def need(ok, message):
    if not ok:
        raise ValueError(message)


def turn(state):
    x, y, z = state                  # physical vector = (x, sqrt(3)*y, z)
    return (-x-3*y)/2, (x-y)/2, z


def evolve(start, program):
    s = start
    for enabled in program:
        x, y, z = s
        s = (z, -y, x)
        if enabled:
            s = turn(s)
    return s


def weights(s):
    # Unique barycentric coefficients of the displayed four reference directions.
    x, y, z = s
    top = (1+2*z)/3
    b1 = (1-top+4*y)/3
    b2 = (1-top-b1)/2 - 2*x/3
    b3 = 1-top-b1-b2
    out = top, b1, b2, b3
    need(sum(out)==1 and all(sum(k*r[j] for k,r in zip(out,REFERENCES))==s[j]
                             for j in range(3)), "affine reconstruction")
    return out


def amplification(s):
    return 1 + sum(-x for x in weights(s) if x < 0)


def dec(q):
    return Decimal(q.numerator) / Decimal(q.denominator)


def panel(n, s):
    z = s[2]
    radius2 = 1-z*z
    ring = (s, turn(s), turn(turn(s)))
    need(radius2 > 0 and all(x*x+3*y*y+z*z == 1 for x,y,z in ring), "ray norm")
    need(all(sum(p[i] for p in ring)==0 for i in (0,1)), "equally spaced transverse vectors")
    south = (0,0,Q(-1))
    ring_gain = max(amplification(p) for p in ring)
    south_gain = amplification(south)
    eta = eps = Q(1,1000)
    with localcontext() as ctx:
        ctx.prec = 50
        rho = dec(radius2).sqrt()
        zero = dec(1-z)/rho
        # North is a reference vertex; at south A >= -south_gain*eps follows from F >= 0.
        numerator = (1-z) + (1+z)*eta + (2*ring_gain+(1-z)*south_gain)*eps
        transverse = dec(numerator) / rho
        return dict(power=n, ticks=6*n+4, z=str(z), radius_squared=str(radius2),
                    ring_X_YoverSqrt3=[(str(p[0]),str(p[1])) for p in ring],
                    ring_comparison_gain=str(ring_gain), south_comparison_gain=str(south_gain),
                    zero_error_tilt=str(zero),
                    example_eta_eps="1/1000", example_transverse_cap=str(transverse))


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    reference_programs = ((), H+D+D+H, H+D+D+H+D, H+D+D+H+D+D)
    for word, ref in zip(reference_programs, REFERENCES):
        need(evolve(NORTH,word) == ref, "reference program")
    trajectory = []
    high = Q(0)
    s = NORTH
    for n in range(1,604):
        previous = s
        s = evolve(previous,B)
        x,y,z = previous
        alternate = turn((x,(-y-z)/2,(3*y-z)/2))
        need(s == alternate, "direct X and Z rotations disagree with tick expansion")
        trajectory.append(dict(n=n,z=str(s[2]),record_high=s[2]>high))
        if s[2] > high:
            high = s[2]
    selected = []
    for row in trajectory:
        if not row["record_high"]:
            continue
        n = row["n"]
        ticks = 6*n+4
        s = evolve(NORTH,B*n)
        for j, ray in enumerate((s,turn(s),turn(turn(s)))):
            middle = B*n + D*j + IDENTITY*(2-j)
            need(len(middle)==ticks and evolve(NORTH,middle)==ray, "unequal terminal panel")
        for word, ref in zip(reference_programs,REFERENCES):
            padded = word + IDENTITY*((ticks-len(word))//2)
            need(len(padded)==ticks and evolve(NORTH,padded)==ref, "reference padding")
        need(evolve((Q(0),Q(0),Q(-1)),IDENTITY*(ticks//2))==(0,0,-1), "south padding")
        selected.append(panel(n,s))
    result=dict(in_coordinates="(x,y/sqrt(3),z)", B_ticks=B, cubic_plate_ticks=D,
                chronological_reference_programs=reference_programs, comparisons=selected,
                all_powers_with_z=trajectory)
    args.output.parent.mkdir(exist_ok=True,parents=True)
    with args.output.open("x",encoding="utf8",newline="\n") as file:
        json.dump(result,file,indent=2)
        file.write("\n")


if __name__ == "__main__":
    main()
