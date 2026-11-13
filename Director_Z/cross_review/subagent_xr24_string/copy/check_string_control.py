"""Run python -B check_string_control.py OUTPUT_DIRECTORY (NumPy).

Addressable adjacent Givens with (c,s)=(3,4)/5 and a separately selectable
uniform string kick w=(3-4i)/5. All numerical ranks are exact lower bounds
from reduction of Gaussian-integer Lie words modulo a split prime.
"""
import argparse
import json
import os
from collections import deque
from fractions import Fraction
from itertools import combinations
from pathlib import Path

for key in ("OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "OMP_NUM_THREADS"):
    os.environ[key] = "1"
import numpy as np
from check_gauss_string import add, bond, defect, launch, mult, rationalize, single_link_kicks


PRIME = 1009
IMAG = 469
assert IMAG**2 % PRIME == PRIME-1
PREP = (0,2,1)
ANALYZER = (1,)
MODES = tuple(combinations(range(4),2))
FIELD = (3,-4,5)


def index_pairs(n):
    coords = list(combinations(range(n),2))
    return coords,{q:i for i,q in enumerate(coords)}


def one_body_hop(q,k):
    if (k in q) == (k+1 in q):
        return None
    return tuple(sorted(set(q)^{k,k+1}))


def integral_generators(n):
    coords,index = index_pairs(n)
    size = len(coords)
    gs = []
    for k in range(n-1):
        g = np.zeros((size,size),dtype=np.int64)
        for i,q in enumerate(coords):
            v = one_body_hop(q,k)
            if v is not None:
                g[index[v],i] = 1 if k in q else -1
        gs.append(g)
    diag = np.diag([IMAG*(b-a) for a,b in coords])
    return coords,gs,diag


def lie_rank(generators):
    """Span ad-generator Lie words. RREF representatives may be commuted:
    they lie in the current span and span it, so closure loses no brackets.
    """
    d = generators[0].shape[0]
    pivots = {}
    queue = deque()
    def add_row(mat):
        v = mat.ravel().copy()%PRIME
        while v.any():
            k = int(np.flatnonzero(v)[0])
            if k in pivots:
                v = (v-v[k]*pivots[k])%PRIME
            else:
                v = (v*pow(int(v[k]),-1,PRIME))%PRIME
                pivots[k] = v
                queue.append(v.reshape(d,d))
                return
    for h in generators:
        add_row(h)
    work=0
    while queue and len(pivots)<d*d:
        v = queue.popleft()
        for h in generators:
            add_row(h@v-v@h)
            work+=1
    return dict(rank=len(pivots),column_dimension=d*d,brackets_tested=work)


def ranks(n):
    coords,g,d = integral_generators(n)
    full=lie_rank([*g,d])
    only=lie_rank(g)
    scalar=np.eye(len(coords),dtype=np.int64)*IMAG
    constant=lie_rank([*g,scalar])
    all_active=lie_rank([sum(g),d])
    assert full['rank']==len(coords)**2
    assert only['rank']==(0 if n==2 else n*(n-1)//2)
    assert constant['rank']==only['rank']+1
    return dict(sites=n,coordinates=len(coords),with_separation=full,rotations_only=only,
                uniform_scalar_replacing_separation=constant,
                single_summed_hopping_generator_instead_of_addressable=all_active)


def diagonal_extraction(n):
    coords,ix=index_pairs(n)
    def dist(order):
        pos={label:k for k,label in enumerate(order)}
        return np.array([abs(pos[i]-pos[j]) for i,j in coords])
    def difference(a,b,left,rest):
        return dist([*left,b,a,*rest])-dist([*left,a,b,*rest])
    triples=0
    for a,b in coords:
        for k in range(n):
            if k in (a,b):
                continue
            rest=[x for x in range(n) if x not in (k,a,b)]
            delta=difference(a,b,[k],rest)-difference(a,b,[],[k,*rest])
            expected=np.zeros(len(coords),int)
            expected[ix[tuple(sorted((a,k)))]]=2
            expected[ix[tuple(sorted((b,k)))]]=-2
            assert np.array_equal(delta,expected)
            triples+=1
    return dict(sites=n,pairs=len(coords),verified_three_label_identities=triples,
                trace_distance=sum(b-a for a,b in coords))


def hop_small(state,k):
    out={q:(0,0) for q in MODES}
    for q,(a,b) in state.items():
        v=one_body_hop(q,k)
        c=5 if v is None else 3
        out[q]=add(out[q],(c*a,c*b))
        if v is not None:
            s=4 if k in q else -4
            out[v]=add(out[v],(s*a,s*b))
    return out,5


def power(w,m):
    z=(1,0)
    for _ in range(m):
        z=mult(z,w)
    return z


def reduced_step(state,gate,field):
    if gate=="kick":
        a,b,d=field
        return {q:mult(z,tuple(t*d**(3-q[1]+q[0]) for t in power((a,b),q[1]-q[0])))
                for q,z in state.items()},d**3
    return hop_small(state,gate)


def stats(st,den):
    a,b,c,d,e,f=[st.get(q,(0,0)) for q in MODES]
    neg=mult(b,e)
    pf=add(add(mult(a,f),(-neg[0],-neg[1])),mult(c,d))
    vals=[sum(t*t for t in st.get(q,(0,0)))/Fraction(den*den) for q in MODES]
    assert sum(vals)==1
    return dict(amplitude_denominator=den,amplitude_numerators=[st.get(q,(0,0)) for q in MODES],
                position_probabilities=list(map(str,vals)),
                plucker_real_imag=[str(Fraction(t,den*den)) for t in pf],
                squared_plucker_modulus=str(Fraction(sum(t*t for t in pf),den**4)))


def add_report(numerator,den,raw,raw_den):
    assert all(defect(m,e)==0 for m,e in raw)
    for i,j in MODES:
        key=(1<<i)|(1<<j),(1<<j)-(1<<i)
        a,b=numerator.get((i,j),(0,0))
        c,d=raw.get(key,(0,0))
        assert a*raw_den==c*den and b*raw_den==d*den
    return stats(numerator,den)


def schedule(field):
    reduced={(0,2):(1,0)}
    physical=launch(4,0,2)
    den=raw_den=1
    rows=[]
    for gate in (*PREP,"kick",*ANALYZER):
        reduced,inc=reduced_step(reduced,gate,field)
        reduced,den=rationalize(reduced,den*inc)
        if gate=="kick":
            physical,inc=single_link_kicks(physical,4,field)
        else:
            physical,inc=bond(physical,gate,3,4,1),5
        physical,raw_den=rationalize(physical,raw_den*inc)
        row=add_report(reduced,den,physical,raw_den)
        rows.append(dict(gate=gate,**row))
    assert all(q["squared_plucker_modulus"]=="0" for q in rows[:3])
    assert rows[2]["position_probabilities"]==rows[3]["position_probabilities"]
    return dict(energized_link_phase=field,source=[0,2],basis=MODES,steps=rows)


def finite_witness():
    actual=schedule(FIELD)
    no_phase=schedule((1,0,1))
    conjugate=schedule((3,4,5))
    parity=schedule((-1,0,1))
    for q in (no_phase,parity):
        assert all(r['squared_plucker_modulus']=='0' for r in q['steps'])
    rows=actual['steps']
    assert Fraction(rows[3]['squared_plucker_modulus'])>0
    assert rows[3]['squared_plucker_modulus']==rows[-1]['squared_plucker_modulus']
    assert all(x['position_probabilities']==y['position_probabilities']
               for x,y in zip(rows,conjugate['steps']))
    idx=MODES.index((2,3))
    passed=Fraction(rows[-1]['position_probabilities'][idx])
    idle=Fraction(no_phase['steps'][-1]['position_probabilities'][idx])
    assert passed!=idle
    return dict(actual=actual,no_phase=no_phase,conjugated_phase=conjugate,parity_phase=parity,
                analyzed_port=[2,3],string_on=str(passed),string_off=str(idle),difference=str(passed-idle))


def hodge_control():
    # The real four-mode exterior rotations commute with Hodge star; a
    # nonconstant product of complementary phases also breaks its bilinear
    # Plucker form up to scalar. Both are exact Gaussian-integer tests.
    _,gs,_=integral_generators(4)
    h=np.zeros((6,6),dtype=int)
    for q,v,s in (((0,1),(2,3),1),((0,2),(1,3),-1),((0,3),(1,2),1)):
        i,j=MODES.index(q),MODES.index(v)
        h[i,j]=h[j,i]=s
    assert np.array_equal(h@h,np.eye(6)) and all(np.array_equal(h@g,g@h) for g in gs)
    exponents=[1+1,2+2,3+1]
    products=[(power(FIELD[:2],e),5**e) for e in exponents]
    def distinct(x,y):
        return any(a*y[1]!=b*x[1] for a,b in zip(x[0],y[0]))
    assert distinct(products[0],products[1]) and products[1]==products[2]
    assert distinct((power(FIELD[:2],3),5**3),(power(FIELD[:2],1),5))
    return dict(kinetic_generators_commute_with_star=True,
                complementary_pairings=[[[0,1],[2,3]],[[0,2],[1,3]],[[0,3],[1,2]]],
                string_exponents_summed_over_complements=exponents,
                resulting_products_gaussian_integer_numerator_and_denominator=products,
                commutes_with_star=False,preserves_Plucker_bilinear_form_up_to_common_scalar=False)


def length_search():
    # A string kick cannot change a sharp position. Group physically redundant
    # global phases by retaining them in the exact state rather than pruning.
    controls=(0,1,2,"kick")
    nshort=0
    frontier=[({q:(1,0)},1,q,()) for q in MODES]
    rows=[]
    for depth in range(5):
        good=[]
        for s,den,launch_at,bank in frontier:
            if stats(s,den)['squared_plucker_modulus']!='0':
                good.append((launch_at,bank))
        rows.append(dict(depth=depth,all_localized_start_words=len(frontier),non_Slater=len(good),
                         first=good[0] if good else None))
        if good:
            break
        nshort+=len(frontier)
        following=[]
        for s,den,q,bank in frontier:
            for g in controls:
                t,inc=reduced_step(s,g,FIELD)
                t,out_den=rationalize(t,den*inc)
                following.append((t,out_den,q,bank+(g,)))
        frontier=following
    assert rows[-1]['depth']==4 and rows[-1]['non_Slater']>0
    return dict(first_depth=4,shorter_controls=nshort,all_rows=rows)


def main():
    return dict(scope="Open n-site chain with exactly two identical occupations in the defect-free sector and vacuum exterior links. Supplied primitives are one individually addressed adjacent single-occupation Givens at a time, (c,s)=(3,4)/5, the identity on 00/11, and one separately selectable w=(3-4i)/5 kick per energized link. Single read is the terminal position pair. No arbitrary real gate, negative exponent or independently programmed diagonal occurs in the finite witness.",
        density="The rotation and phase angle are irrational multiples of pi since 2*cos(theta)=6/5 is rational but not an algebraic integer. Positive powers have full circles in the compact closure. Adjacent real rotations include signed site permutations in their closure. Use permuted distance diagonals; two adjacent-label swap differences with the spectator moved from right to left give 2(E_ak-E_bk). Connectedness of the line graph of the complete graph supplies every traceless diagonal and the nonzero trace of distance supplies the scalar. A diagonal projector commuted with the addressed hopping generator isolates an individual occupation edge. Further commutators give both matrix units and the full unitary Lie algebra on the connected exclusion graph. This proves density for n>=3, with arbitrary precision but without a uniform synthesis rate. For n=2 the single ray is unique and the scalar phase circle is dense. For n<2 the sector is empty. At n=3 all two-forms are Slater; interaction certification by a nonzero Plucker coordinate starts at n=4.",
        rank_test="Original infinitesimal generators, no pre-isolated coordinate switches: iterated commutators over F_1009, i sent to 469. A nonsingular minor over the field certifies a nonzero Gaussian-integer minor over C. Rows use reductions and linear combinations only. Full rank d^2 saturates the ambient dimension of the compact Lie algebra. A lower rank in a deliberately weakened modular control is reported as measured; it does not alone prove a characteristic-zero upper bound.",
        checks=[ranks(n) for n in range(2,7)],diagonal_identities=[diagonal_extraction(n) for n in range(2,10)],
        finite=finite_witness(),four_site_hodge_control=hodge_control(),shorter_controls=length_search(),
        limitations="An addressed bank and independently selectable string kick enlarge the previously stipulated lockstep Floquet walk. Repeating a single fixed cycle has abelian closure and is insufficient for d>1. The explicit detector distinguishes fixed controls from an idle kick; it cannot exclude every possible Slater input from one recorded probability. Conjugate w and real sources/analyzers produce the same position law. The real phase -1 exponent |j-i| factors into independent one-site parity phases.")


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output',type=Path)
    directory=parser.parse_args().output
    result=main()
    directory.mkdir(parents=True,exist_ok=True)
    (directory/'string_control.json').write_bytes((json.dumps(result,separators=(',',':'))+'\n').encode())
    print([(r['sites'],r['with_separation']['rank']) for r in result['checks']])
