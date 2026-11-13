"""Trace two forward-only comparisons on a four-mode occupation line.

Run python -B check_contact_exchange.py OUTPUT_DIRECTORY. A polynomial term
records powers of the cosine, sine, left contact, right contact and swap phase.
"""

import argparse
import cmath
import itertools
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path


LEFT, RIGHT, SWAP = "L", "R", "S"
A = LEFT + RIGHT
B = SWAP + A + SWAP
PORTS = (3, 5, 6, 9, 10, 12)  # bit masks of all two-site patterns
ZERO = (0, 0, 0, 0, 0)


def bump(exponents, index):
    powers = list(exponents)
    powers[index] += 1
    return tuple(powers)


def paths(source, word):
    amplitudes = {(source, ZERO): 1}
    for symbol in word:
        lo = {LEFT: 0, RIGHT: 2, SWAP: 1}[symbol]
        pair = 3 << lo
        new = Counter()
        for (mask, powers), multiplicity in amplitudes.items():
            occupation = (mask & pair) >> lo
            if occupation == 0:
                new[mask, powers] += multiplicity
            elif occupation == 3:
                index = {LEFT: 2, RIGHT: 3, SWAP: 4}[symbol]
                new[mask, bump(powers, index)] += multiplicity
            elif symbol == SWAP:
                new[mask ^ pair, powers] += multiplicity
            else:
                new[mask, bump(powers, 0)] += multiplicity
                sign = 1 if occupation == 1 else -1
                new[mask ^ pair, bump(powers, 1)] += sign * multiplicity
        amplitudes = {k: v for k, v in new.items() if v}
    return {
        output: {powers: coeff for (mask, powers), coeff in amplitudes.items() if mask == output}
        for output in PORTS
    }


def evaluate(polynomial, values):
    total = 0
    for powers, coeff in polynomial.items():
        term = coeff
        for value, power in zip(values, powers):
            term *= value**power
        total += term
    return total


def serialized(tables):
    return {
        str(port): [list(powers) + [coeff] for powers, coeff in sorted(poly.items())]
        for port, poly in tables.items()
    }


def compile_tables():
    specs = ((3, A+B), (3, B+A), (5, A+B+A), (5, B+A+A))
    tables = [paths(source, word) for source, word in specs]
    dark, swap, contact, echo = [table[port] for table, port in zip(tables, (5, 5, 10, 10))]
    # These identities hold before imposing c²+h²=1 or |contact|=1.
    assert not dark
    assert swap == {(2,2,0,0,0):-1, (2,2,0,0,1):-1}
    assert contact == {(2,2,1,0,0):1,(2,2,0,1,0):1,
                       (4,2,0,0,0):1,(4,2,0,0,2):1,(2,4,0,0,1):-2}
    assert echo == {(2,2,1,0,0):4}
    return specs,tables


def square(z):
    return z.real*z.real + z.imag*z.imag


def diagonal_probe(c,h,u,g):
    # With mode zero occupied, a gate on 01 having one-body diag(u,1)
    # acts as diag(g,u) in the ordered basis |01>, |02>. The mixer on 12
    # only encounters one occupied mode in this invariant pair of states.
    def mix(col, sine):
        x,y=col
        return c*x-sine*y,sine*x+c*y

    source=(1,0)
    after_mix=mix(source,h)
    diag_after=(g*after_mix[0],u*after_mix[1])
    one=mix(diag_after,-h)
    other=mix(mix((g,0),h),-h)
    assert abs(one[1]-c*h*(u-g))<1e-14 and abs(other[1])<1e-14
    return dict(single=[u.real,u.imag],double=[g.real,g.imag],
                leaked=square(one[1]),reference=square(other[1]))


def compiled_records(tables,specs):
    # On each fixed-number configuration a signed selector acts by either
    # a signed stay, a neighbor exchange, or moving to orthogonal junk.
    # Project all Walsh indices back to zero. The survivor application is
    # the integer numerator on each fresh stage, with common denominator 8.
    cases=[]
    for left,right,swap in itertools.product((1,-1),repeat=3):
        programs=[]
        for table,(source,word) in zip(tables,specs):
            survivors={source:1}
            count=0
            for letter in word:
                i={LEFT:0,RIGHT:2,SWAP:1}[letter]
                pair=3<<i
                new=Counter()
                for mask,value in survivors.items():
                    local=(mask & pair)>>i
                    if letter==SWAP:
                        new[mask^pair if local in (1,2) else mask]+=(
                            swap*value if local==3 else value)
                        continue
                    phase=left if letter==LEFT else right
                    for label in range(8):
                        if local in (0,3) and label<5:
                            new[mask]+=value*(phase if local==3 else 1)
                        elif local in (1,2) and label<3:
                            new[mask]+=value
                        elif local in (1,2) and label<7:
                            new[mask^pair]+=value*(1 if local==1 else -1)
                        # Other labels are in an orthogonal junk sector.
                survivors=new
                count+=letter!=SWAP
            c,h=Fraction(3,5),Fraction(4,5)
            passed=Fraction(25,64)**count
            bins={m:Fraction(survivors[m]**2,64**count) for m in PORTS}
            assert sum(bins.values())==passed
            for m in PORTS:
                want=evaluate(table[m],(c,h,left,right,swap))
                assert bins[m]==passed*want**2
            fails=[Fraction(25,64)**j*Fraction(39,64) for j in range(count)]
            assert sum(fails)+passed==1
            programs.append(dict(source=source,word=word,success=str(passed),
                all_pass_and_occupation={str(k):str(v) for k,v in bins.items()},
                first_failure_at_rotation=list(map(str,fails))))
        cases.append(dict(left=left,right=right,swap=swap,programs=programs))
    return cases


def check_phases(c,h,tables):
    rows = []
    v = c*c*h*h
    # Independent spatial phases, including unreliable swap controls where a
    # conditional certificate using delta_s=0 would be invalid.
    for g, q, s in itertools.product((1,-1,1j,cmath.exp(.37j)),repeat=3):
        evaluated = [[evaluate(poly, (c,h,g,q,s)) for poly in table.values()] for table in tables]
        assert all(abs(sum(square(z) for z in col)-1)<3e-14 for col in evaluated)
        swap = square(evaluated[1][1])
        direct, reference = (square(evaluated[j][4]) for j in (2,3))
        assert abs(swap-v*v*square(1+s))<1e-13
        # After calibration s=-1 the difference is a nonnegative witness.
        infidelity = 2*square(1-g)+2*square(1-q)+square(g-q)
        if s == -1:
            assert abs((reference-direct)-v*v*infidelity)<1e-13
        # Joint error budget for all s: changing two occurrences of a
        # unitary gate changes any bin probability by <= 2 ||S_s-S_-1||.
        assert v*v*infidelity <= abs(reference-direct)+2*abs(1+s)+1e-13
        rows.append(dict(left=[g.real,g.imag],right=[q.real,q.imag],swap=[s.real,s.imag],
                         forbidden=swap,contact=direct,reference=reference))
    return rows


def main():
    specs,tables = compile_tables()
    cases=[]
    for c,h in [(Fraction(3,5),Fraction(4,5)),(Fraction(4,5),Fraction(3,5)),
                (Fraction(1),Fraction(0)),(Fraction(0),Fraction(1))]:
        v = c*c*h*h
        ordinary = [evaluate(t[port],(c,h,1,1,-1))**2 for t,port in zip(tables,(5,5,10,10))]
        assert ordinary == [0,0,16*v*v,16*v*v]
        cases.append(dict(c=str(c),h=str(h),informative=bool(v),
                          determinant_reference=str(16*v*v),samples=check_phases(float(c),float(h),tables)))
    return dict(convention="Chronological L=R01, R=R23, S=swap12; R sends the first basis vector to (c,h). "
                "Masks use bit position equal to mode index. Unit vacuum on each addressed bond.",
                powers=["cos","sin","phase_left","phase_right","phase_swap"],
                columns=[dict(input=src,word=w,amplitudes=serialized(t)) for (src,w),t in zip(specs,tables)],
                cases=cases,coherent_Walsh_success_records=compiled_records(tables,specs),
                diagonal_phase_probe=[diagonal_probe(.6,.8,u,g)
                for u,g in itertools.product((1,-1,1j,cmath.exp(.37j)),repeat=2)])


if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("directory",type=Path)
    out=parser.parse_args().directory
    out.mkdir(parents=True,exist_ok=True)
    (out/"contact_exchange.json").write_bytes((json.dumps(main(),separators=(",",":"))+"\n").encode())
