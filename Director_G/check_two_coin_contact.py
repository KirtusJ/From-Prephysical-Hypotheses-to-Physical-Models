"""Replay all whole-site effects of two three-tick walks with a coincidence sign."""
from argparse import ArgumentParser
from fractions import Fraction
from itertools import product
import json
from pathlib import Path

from check_two_column_transport import diag, gram, times, transpose, walk


def check(ok, reason):
    if not ok:
        raise ValueError(reason)


def tensor(a, b):
    return [[u*v for u in left for v in right] for left in a for right in b]


def scaled(k, a):
    return [[k * v for v in row] for row in a]


def score_sum(effects, weights):
    return [[sum(weights[key] * matrix[i][j] for key, matrix in effects.items())
             for j in range(4)] for i in range(4)]


def rank(matrices):
    basis = {}
    for matrix in matrices:
        row = [Fraction(matrix[i][j]) for i in range(4) for j in range(i, 4)]
        for pivot, earlier in sorted(basis.items()):
            if row[pivot]:
                row = [x-row[pivot]*b for x,b in zip(row,earlier)]
        first = next((i for i,x in enumerate(row) if x), None)
        if first is not None:
            basis[first] = [x/row[first] for x in row]
    return len(basis)


def path_effects(separation, pulses, ticks):
    """Sum pairs of signed histories into each named site and output rail, then pool rails."""
    ends = {}
    for words in product(product((0, 1), repeat=ticks), repeat=2):
        x, z = 0, separation
        contact_sign = 1
        for tick, (a, b) in enumerate(zip(*words), 1):
            x += 1-2*a
            z += 1-2*b
            if tick in pulses and x == z:
                contact_sign *= -1
        for ca, cb in product((0, 1), repeat=2):
            sign, a_prev, b_prev = contact_sign, ca, cb
            for a, b in zip(*words):
                if (a*a_prev + b*b_prev) % 2:
                    sign *= -1
                a_prev, b_prev = a, b
            row = ends.setdefault((x,z-separation), {}).setdefault((a_prev,b_prev), [0]*4)
            row[2*ca+cb] += sign
    return {sites:gram(list(rails.values()), list(rails.values())) for sites,rails in ends.items()}


# The first tick is H followed by an outgoing displacement. A common well at that plane
# contributes a four-rail diagonal sign D. Pull D back to the input before using
# independently replayed one-walker position effects. Each local integer Gram has scale 8.
H = [[1,1],[1,-1]]
J = [[0,-1],[1,0]]
YY = scaled(-1, tensor(J,J))
ZZ = tensor([[1,0],[0,-1]], [[1,0],[0,-1]])


def first_plane_pullback(separation):
    hh = tensor(H,H)
    d = [[0]*4 for _ in range(4)]
    for a,b in product((0,1),repeat=2):
        d[2*a+b][2*a+b] = -1 if 1-2*a == separation + 1-2*b else 1
    return scaled(Fraction(1,4), times(hh, times(d,hh)))


def product_effects(ticks):
    local = {p:gram(rows,rows) for p,rows in walk(ticks).items()}
    return {(x,z):tensor(a,b) for x,a in local.items() for z,b in local.items()}


def pull_effects(effects, change):
    return {key:times(transpose(change), times(matrix, change)) for key,matrix in effects.items()}


def flag(offset):
    return offset in (-3, 1)


def score(x, z):
    return 1 if flag(x) == flag(z) else -1


def inner(a,b):
    return sum(i*j for r,s in zip(a,b) for i,j in zip(r,s))


def run():
    no_contact = product_effects(3)
    panels, sets = {}, {}
    for separation in (0, 1, 2, -2, 4):
        pulse = path_effects(separation, {1}, 3)
        actual = path_effects(separation, {1,2,3}, 3)
        check(actual == pulse == pull_effects(no_contact, first_plane_pullback(separation)),
              "permanent collisions and first-plane and algebraic constructions must agree")
        check(len(actual) == 16 and rank(actual.values()) == 9, "whole-site spanning table")
        check(score_sum(actual, {k:1 for k in actual}) == scaled(64, tensor(diag(1),diag(1))),
              "normalization on every two-coin input")
        signed = score_sum(actual, {k:score(*k) for k in actual})
        wanted = scaled(-16,YY) if abs(separation)==2 else scaled(16,ZZ)
        check(signed == wanted, "signed whole-site score")
        sets[separation] = actual
        panels[str(separation)] = dict(signed_score=signed, rank=rank(actual.values()),
                                       sites=[dict(offsets=k,gram=v) for k,v in sorted(actual.items())])
    combined = rank([*sets[2].values(),*sets[4].values()])
    check(combined == 10, "reconstruction of all real symmetric joint entries")
    check(all(inner(q,ZZ)==0 for q in sets[2].values()), "near misses a real longitudinal correlator")
    check(all(inner(q,YY)==0 for q in sets[4].values()), "far misses the joint imaginary correlator")
    deadlines=[]
    for ticks in (0,1,2):
        free=product_effects(ticks)
        for separation in range(-4,5):
            check(path_effects(separation, set(range(1,ticks+1)), ticks) == free,
                  "collisions before the first interfering site have no terminal effect")
        deadlines.append(dict(ticks=ticks, nearby_separations=list(range(-4,5)),rank=rank(free.values())))
    identity=tensor(diag(1),diag(1))
    witnesses, circular = {}, {}
    for sign in (-1,0,1):
        # rho=(I + sign Y-tensor-Y)/4. These are the real parts of the product
        # circular examples for signs +/- and exactly the two correlated mixtures.
        rho4=[[a+sign*b for a,b in zip(row,other)] for row,other in zip(identity, YY)]
        probs={key:Fraction(inner(effect,rho4),256) for key,effect in sets[2].items()}
        match=sum(v for k,v in probs.items() if score(*k)==1)
        check(sum(probs.values())==1 and match==Fraction(4-sign,8), "matched-score law")
        witnesses[str(sign)] = dict(agree=str(match),masses=[str(v) for k,v in sorted(probs.items())])
        circular[sign] = probs
    differences = {k:circular[1][k]-circular[-1][k] for k in circular[1]}
    for (x,z), value in differences.items():
        expected = -Fraction(x*z,8) if abs(x)==abs(z)==1 else 0
        check(value==expected, "circular orientations differ only at the four interior pairs")
    tv = sum(abs(v) for v in differences.values())/2
    check(tv == Fraction(1,4), "maximum terminal whole-site event separation")
    return dict(denominator=64,site_coordinates="offsets from each labeled walker's own launch",
                coin_order=["RR","RL","LR","LL"],panels=panels,combined_rank=combined,
                early_clocks=deadlines,mean_yy_witnesses=witnesses,whole_site_tv=str(tv))


if __name__ == "__main__":
    parser=ArgumentParser(description=__doc__)
    parser.add_argument("output",type=Path)
    dest=parser.parse_args().output
    dest.write_bytes((json.dumps(run(),indent=2)+"\n").encode())
