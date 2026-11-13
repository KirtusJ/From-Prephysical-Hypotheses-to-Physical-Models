"""Check equal scalar character sums on a signed five-sheet, seven-tick carrier.

Run python -B check_multiset_fibres.py <output-directory>. No external packages.
"""

import argparse
import itertools
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path

ORDER = 5
DEPTH = 7


def trace(word):
    x = y = 0
    previous = "R"
    sign = 1
    for direction in word:
        y += x
        if previous == direction == "L":
            sign = -sign
        x += 1 if direction == "R" else -1
        previous = direction
    return dict(word="".join(word), end_x=x, end_coin=previous, gain_integer=y,
                sheet=y % ORDER, sign=sign)


def native_histogram():
    current = {(0, "R", 0):1}
    for _ in range(DEPTH):
        following = Counter()
        for (x,previous,y), amplitude in current.items():
            for direction,step in (("R",1),("L",-1)):
                dest = (x+step,direction,(y+x)%ORDER)
                following[dest] += amplitude * (-1 if previous==direction=="L" else 1)
        current = following
    assert sum(v*v for v in current.values()) == 2**DEPTH
    return current


def describe(selected):
    pos,neg = ([sum(p["sheet"]==j and p["sign"]==sign for p in selected)
                for j in range(ORDER)] for sign in (1,-1))
    diff = [a-b for a,b in zip(pos,neg)]
    norm = sum(x*x for x in diff)
    total = sum(diff)
    # A polynomial of degree at most four over Q has value zero at a primitive
    # fifth root exactly when it is a multiple of 1+z+z²+z³+z⁴.
    # For each nontrivial embedding, permute exponents then reduce z^4.
    primitive={}
    for s in range(1,ORDER):
        rotated=[0]*ORDER
        for j,c in enumerate(diff):
            rotated[s*j%ORDER] = c
        primitive[s] = [x-rotated[4] for x in rotated[:4]]
    correlation=[sum(diff[j]*diff[(j-d)%ORDER] for j in range(ORDER)) for d in range(ORDER)]
    # A direct algebraic Parseval check: the trace of a reduced polynomial
    # P(z), summed over all four primitive powers, has ζ^j-trace -1, j!=0.
    primitive_norm_trace = 4*correlation[0] - sum(correlation[1:])
    assert primitive_norm_trace + total*total == ORDER*norm
    return dict(words=[p["word"] for p in selected],size=len(selected),positive_counts=pos,
                negative_counts=neg,signed_sheet_vector=diff,primitive_sum_in_basis_1_z_z2_z3=primitive,
                sheet_norm_squared=norm,formal_sheet_weight=str(Fraction(norm,2**DEPTH)),
                sign_character_sum=total,sign_character_square=total**2,
                sum_nontrivial_sheet_character_squares=primitive_norm_trace,
                formal_sign_character_weight=str(Fraction(total**2,2**DEPTH)))


def rho(g, v):
    # zeta_10^e = (-1)^e * zeta_5^(3e).
    return [(-1 if g%2 else 1)*v[(j-3*g)%5] for j in range(5)]


def add(a,b):
    return [x+y for x,y in zip(a,b)]


def norm(a):
    return sum(x*x for x in a)


def block_tests(x,y):
    tested=0
    # Orthogonality fixes the fourth phase: every normalized 2-by-2 block
    # over mu10 has this form. This enumeration tests all ordered blocks
    # on actual event inputs and on two full integer multiset vectors.
    inputs=[(x,y),([2,-1,0,3,1],[1,2,-2,0,-3])]
    for a,b,c in itertools.product(range(10),repeat=3):
        d=(5+c-a+b)%10
        for u,v in inputs:
            out=[add(rho(i,u),rho(j,v)) for i,j in ((a,b),(c,d))]
            assert sum(map(norm,out))==2*(norm(u)+norm(v))
            assert sum(sum(r)**2 for r in out)==2*(sum(u)**2+sum(v)**2)
            tested+=1
    # At degree five, the scalar Fourier block on mu5 is orthogonal in its
    # primitive complex character. Two equal column inputs in the sign
    # sector both look like +1 at every output, violating degree-five law.
    ordinary=[1,0,0,0,0]
    higher=[add(ordinary,rho(2*j,ordinary)) for j in range(5)]
    assert sum(map(norm,higher))==12 and 5*(2*norm(ordinary))==10
    return dict(ordered_degree_two_mu10_blocks=1000,ordered_input_checks=tested,
                identities="Every scalar unit block [[a,b],[c,d]] satisfying B*B=2I has d=−c*a^-1*b and is a row/column switched H. In the signed permutation representation, switching permutes or negates coordinates and the H norm identity is the integer parallelogram identity. The same identity holds for the square of the sum of signed counts.",
                five_by_five_primitive_Fourier_control=dict(input="unit impulses in two adjacent input columns",
                    scalar_degree=5,expected_lifted_norm=10,observed_lifted_norm=12,
                    sign_only_expected=10,sign_only_observed=20))


def main():
    words=[trace(w) for w in itertools.product("RL",repeat=DEPTH)]
    hist=native_histogram()
    by_word=Counter()
    for p in words:
        by_word[p["end_x"],p["end_coin"],p["sheet"]] += p["sign"]
    assert by_word == hist
    port=[p for p in words if (p["end_x"],p["end_coin"])==(3,"R")]
    pos=[p for p in port if p["sign"]==1]
    neg=[p for p in port if p["sign"]==-1]
    assert len(port)==15 and len(pos)==10 and len(neg)==5
    B=[]
    for j in range(ORDER):
        a=[p for p in pos if p["sheet"]==j]
        b=[p for p in neg if p["sheet"]==j]
        assert len(a)==2 and len(b)==1
        B.extend((a[0],b[0]))
    results={name:describe(event) for name,event in
             (("A",pos),("B",B),("complete_native_port",port))}
    a,b,all_port=results.values()
    assert a["size"]==b["size"]==10
    assert a["signed_sheet_vector"]==[2]*5 and b["signed_sheet_vector"]==[0]*5
    assert all(all(z==0 for z in v) for event in [a,b] for v in event["primitive_sum_in_basis_1_z_z2_z3"].values())
    assert all_port["signed_sheet_vector"]==[1]*5
    controls=block_tests(a["signed_sheet_vector"],b["signed_sheet_vector"])
    # A common padded selector uses a uniform four-qubit label, accepts only
    # the assigned outgoing direction at each tick, then postselects that same
    # uniform label. Sum the integer-character Hadamard outputs for *all*
    # final label results to check exact closure after the intermediate masks.
    label_results={}
    for name in ("A","B"):
        ev = [next(p for p in port if p["word"]==w) for w in results[name]["words"]]
        result=[]
        for z in range(16):
            bins=[0]*ORDER
            for j,p in enumerate(ev):
                bins[p["sheet"]] += p["sign"]*(-1)**((j&z).bit_count())
            result.append(str(Fraction(norm(bins),16**2*2**DEPTH)))
        survival=Fraction(10,16*2**DEPTH)
        assert sum(map(Fraction,result))==survival
        assert Fraction(result[0])==Fraction(results[name]["sheet_norm_squared"],16**2*2**DEPTH)
        label_results[name]=dict(final_label_probabilities=result,
                                 probability_any_path_mask_failed=str(1-survival))
    return dict(model="Hadamard R,L (minus only for L→L), translation y←y+x mod 5 on departure, x shifted by the outgoing direction. Start (0,R,0) on the integer line. At tick seven each path amplitude denominator is sqrt(128). Word enumeration in the order R before L is compared, cell by cell, with an independent aggregated walk.",
        source_scope="Z16 G10 thm:kernel and cor:kernel2 already classify the degree-two kernel freedom. This is an explicit equal-size, equal-primitive-sum witness to that existing distinction. On mu10=±mu5, each gain decomposes uniquely as sign times zeta5^j. The signed residue vector is therefore determined by the complete endpoint gain multiset.",
        enumeration=dict(full_walk_paths=len(words),whole_walk_squared_numerator=sum(v*v for v in hist.values()),
            selected_base_port=[3,"R"],all_fifteen_words_at_port=port,
            B_order_rule="for residues 0,...,4 take first positive in lexicographic order R before L, then the single negative",
            A_order_rule="all positive histories at this port in R-before-L enumeration order"),
        events=results,block_controls=controls,
        character_scope="F_lift=sum_j (a_j-b_j)^2 is one fifth of the sum of the squared moduli of the five signed characters chi_s(±zeta5^j)=±zeta5^(s*j). For s=0 this is the order-two gain-sign character, trivial on sheet translations only. The trivial mu10 character would send −1 to +1 and gives the square of the cardinality; it fails the signed degree-two continuation. Linear cardinality is separately additive. F_sign=(sum_j(a_j−b_j))² multiplies on Cartesian products and gives 100 vs 0 on this pair. All tested quadratic lifts give 4 rather than 2 to two copies of the identical positive unit gain.",
        physical_read="The raw weights are formal history-class squared masses. In the unfiltered lift the only actual terminal port is the coherent union of all fifteen words and it has weight 5/128. Subsets A and B are not separately reported by that port. Keeping sheet cells distinct is an operational change relative to passing only the scalar primitive character; a complete history multiset itself contains the signed sheet data. A label-controlled selector with labels padded to L=16 realizes both events with common amplitude attenuation 1/16. It requires a coherent conditional direction mask each tick and a final uniform label projection; a classical measurement of each word would instead lose the cancellations.",
        selector_control=dict(label_count=16,reported_label="all-plus (0)",masked_outcomes=label_results,
                A_raw_to_registered="5/32 to 5/8192",B_raw_to_registered="0 to 0",
                fully_dephased_control="Selecting each of the 10 words as an exclusive classical record would give the same summed diagonal class weight 10/128 for A and B before any selector normalization."))


if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("directory",type=Path)
    out=p.parse_args().directory
    out.mkdir(parents=True,exist_ok=True)
    dest=out/"multiset_fibres.json"
    dest.write_bytes((json.dumps(main(),indent=2,allow_nan=False)+"\n").encode())
    print(dest)
