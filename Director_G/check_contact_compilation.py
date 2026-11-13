"""Run python -B check_contact_compilation.py OUTPUT_DIRECTORY (standard library).

Four scalar occupation sites. Every update is an integer numerator with a
single common denominator. Operation lists are chronological (left to right).
"""
import argparse
import json
from fractions import Fraction
from itertools import combinations, permutations, product
from math import isqrt, prod
from pathlib import Path


def rotations():
    A = [('R',0),('R',2)]
    S = [('S',1)]
    B = S+A+S
    return A,B


def invert(word):
    inverse = []
    for kind,i in reversed(word):
        if kind=='R':
            # Independently available single-mode sign on every occupied mode i.
            inverse.extend([('Z',i),('R',i),('Z',i)])
        else:
            inverse.append((kind,i))
    return inverse


def walk(occupied,word,r,swap,c,s):
    data = [int(i==occupied) for i in range(16)]
    denom = 1
    for kind,i in word:
        if kind=='Z':
            data = [-n if j & (1<<i) else n for j,n in enumerate(data)]
            continue
        out = [0]*16
        for j,n in enumerate(data):
            bits = (j>>i)&3
            if bits in (0,3):
                coeff = 1 if bits==0 else r if kind=='R' else swap
                out[j] += n*coeff*(5 if kind=='R' else 1)
            elif kind=='S':
                out[j^(3<<i)] += n
            elif kind=='R':
                out[j] += c*n
                out[j^(3<<i)] += (s if bits==1 else -s)*n
            else:
                raise ValueError(kind)
        denom *= 5 if kind=='R' else 1
        data = out
    assert sum(n*n for n in data)==denom**2
    return [Fraction(n,denom) for n in data]


def det(square):
    size = len(square)
    return sum((-1)**sum(p[i]>p[j] for i,j in combinations(range(size),2))*
               prod(row[col] for row,col in zip(square,p)) for p in permutations(range(size)))


def response(word,r,swap,c,s):
    return [walk(i,word,r,swap,c,s) for i in range(16)]


def matrices(w,c,s):
    responses = response(w,1,-1,c,s)
    modes = [[responses[1<<i][1<<j] for i in range(4)] for j in range(4)]
    for source in range(16):
        cols = [i for i in range(4) if source & (1<<i)]
        for target in range(16):
            rows = [i for i in range(4) if target & (1<<i)]
            actual = responses[source][target]
            assert (det([[modes[x][y] for y in cols] for x in rows]) if len(cols)==len(rows) else 0)==actual
    return modes


def tables(matrix):
    # Each sector's input and output order is increasing bitmask. Keep signs
    # as well as all zeros. Probability of an entry is its square.
    sectors = []
    for k in range(5):
        masks = [m for m in range(16) if m.bit_count()==k]
        sectors.append(dict(masks=masks,signed_columns=[[str(matrix[i][j]) for j in masks] for i in masks]))
    return sectors


def cases(c,s):
    A,B = rotations()
    read = [('R',0),('R',1)]
    ab,ba = A+B,B+A
    comm,echo = A+B+invert(A)+invert(B),A+B+invert(B)+invert(A)
    programs = dict(AB=ab,BA=ba,AB_read=ab+read,BA_read=ba+read,
                    commutator=comm,matched_echo=echo)
    modes = {k:matrices(word,c,s) for k,word in programs.items()}
    ident = [[int(i==j) for i in range(4)]for j in range(4)]
    assert modes['AB']==modes['BA'] and modes['AB_read']==modes['BA_read']
    assert modes['commutator']==modes['matched_echo']==ident
    assert sorted(comm)==sorted(echo) and len(comm)==len(echo)==20
    rows = []
    for r,swap in product((1,-1),repeat=2):
        mats = {k:response(w,r,swap,c,s) for k,w in programs.items()}
        assert all(all(x==int(i==j) for j,x in enumerate(v)) for i,v in enumerate(mats['matched_echo']))
        single = mats['commutator'][3][3]**2
        assert (single==1)==(r==1 and swap==-1)
        for k in ('AB','AB_read','commutator'):
            for idx in range(4):
                assert mats[k][1<<idx]==walk(1<<idx,programs[k],1,-1,c,s)
        raw = [mats[k][3][5]**2 for k in ('AB','BA')]
        analyzed = [mats[k][3][3]**2 for k in ('AB_read','BA_read')]
        rows.append(dict(rotation_contact=r,swap_contact=swap,raw_AB_BA_at_02=list(map(str,raw)),
                         AB_BA_after_analyzer_return_01=list(map(str,analyzed)),
                         commutator_return_01=str(single),echo_return_01='1',
                         full_port_tables={k:tables(M) for k,M in mats.items()}))
    return dict(cos_numerator=c,sin_numerator=s,one_mode_denominator=5,
                programs={k:['%s%d'%op for op in w] for k,w in programs.items()},
                one_particle_AB=[[str(v) for v in row] for row in modes['AB']],
                records=rows)


def signed_subgroup():
    # Signed permutation conjugacy maps an axis reflection to itself, the other
    # coordinate axis, or to a permutation-like off-diagonal reflection; no dense split.
    # A rational orthogonal (not merely monomial) conjugator of Z has first
    # column a rational UNIT +1 eigenvector of the target reflection.
    cases = []
    for c,s,axis in ((3,4,(2,1)),(4,3,(3,1))):
        x,y = axis
        assert (c*x+s*y,s*x-c*y)==(5*x,5*y)
        length = x*x+y*y
        assert isqrt(length)**2!=length
        cases.append(dict(reflection_numerators=[[c,s],[s,-c]],denominator=5,
                          rational_axis=axis,squared_norm=length,
                          normalized_rational_axis_vector_exists=False))
    return cases


def main(output):
    pairs = [cases(3,4),cases(4,3)]
    canonical = pairs[0]['records']
    assert [r['commutator_return_01'] for r in canonical]==[
        '41075281/244140625','1','109014481/244140625','2401/390625']
    assert canonical[3]['AB_BA_after_analyzer_return_01']==['106929/390625','3249/390625']
    result = dict(
        claim='Assume identical labelled four-mode one-particle transformations may be substituted in any fixed-occupation experiment of the same duration; a localized low-mode pair source and local terminal occupation detectors already test this instance. A target rotation contact and a swap contact each have a portable real sign with vacuum fixed to +1. The numerical test gives the determinant signs (+1,-1) uniquely for these two gate types. The equivalence is an added physical premise; a localized one-particle characterization alone gives no such inference.',
        construction='R_i is (c,-s;s,c)/5 on one occupant of adjacent i,i+1. S_i swaps these two modes with no one-particle sign. Z_i is -1 when mode i is occupied, including in multi-occupation configurations. Other local modes are spectators. Put A=R0 R2, B=S1 A S1. They are the rotations of the low and high binary digits of the one-particle mode index and commute. Inverse R_i is Z_i R_i Z_i, also inverse on its contact because the sign is real. The held 20-operation commutator and matched 20-operation echo have the same settings multiset and one-particle identity. Each contains eight R, four S and eight Z strokes. No feedback or intermediate reads. Return detects the difference of their lifted evolutions; signed matrices for all inputs and outputs are included.',
        conventions='Bit i names occupied mode i, i=0,1,2,3. All inputs and outputs in each number sector are retained; signed_columns[input][output] is an exact rational amplitude, whose square is its complete unconditional port weight. Independent exterior-minor evaluations check the determinant lift across all five sectors. Gate timings can be matched with identities, which are assumed to preserve all occupations. Identifying a response only up to a phase common to its whole fixed-number sector is sufficient for this detector comparison.',
        qualifications='The commutator here tests portable real signs for these gates, orientations and bond locations, with the single-site sign instrument independently calibrated and stable on spectators. For a general unit-modulus contact g, Z R Z retains g on the doubly occupied state whereas the true gate inverse has conjugate g. The signed inverse protocol therefore does not prove the general complex-phase result; that case requires a forward-word or separately calibrated true-inverse test. Compiler-dependent contacts, hidden memories, and phases common to a complete fixed-number circuit remain distinct possibilities. The raw AB/BA probabilities can coincide with incorrect target sign; downstream probes or the closed loop reveal it. The reversed rational numerator (4,3) is an additional tested setting.',
        rational_conjugacy_obstruction=signed_subgroup(),
        rational_conjugacy_scope='Trying only to conjugate the fixed calibrated coordinate reflection Z into the reflection RZ inside O(2,Q) fails for these two angles: their +1 axes squared norms are 5 and 10, respectively. A rational nonzero multiple cannot normalize either. The quarter-turn (sine=1) and zero-angle are distinct degenerate controls; uniqueness above is asserted for the two tabulated angles. The four-mode commutator uses the target itself rather than an uncalibrated generator at half its angle.',
        cases=pairs)
    output.mkdir(parents=True,exist_ok=True)
    (output/'contact_compilation.json').write_bytes((json.dumps(result,separators=(',',':'))+'\n').encode())


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('output',type=Path)
    main(p.parse_args().output)
