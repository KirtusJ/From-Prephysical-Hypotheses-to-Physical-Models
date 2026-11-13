"""Finite signed-dyadic equalizers and heralded flag-weight consistency.

Run python -B check_heralded_weights.py results. Uses exact integer circuits
and rational probabilities. The operational probability premises are stated in
the result separately from column synthesis and numerical diagnostics.
"""

import argparse
import json
from fractions import Fraction
from hashlib import sha256
from math import lcm
from pathlib import Path


def matchings(size, groups):
    """Each layer acts on a perfect ordered matching with the ordinary real H."""
    used = {v for group in groups for v in group}
    idle = [v for v in range(size) if v not in used]
    padding = list(zip(idle[::2],idle[1::2]))
    first, second = padding.copy(), padding.copy()
    for a,b,c,d in groups:
        first.extend([(a,b),(c,d)])
        second.extend([(a,c),(b,d)])
    for pairs in (first,second):
        assert sorted(v for pair in pairs for v in pair)==list(range(size))
    return first,second


def balanced_layer(vector, pairs):
    # Numerators of H; after two layers the extra denominator is exactly 2.
    result = [0]*len(vector)
    for a,b in pairs:
        result[a],result[b] = vector[a]+vector[b],vector[a]-vector[b]
    return result


def flip(vector, indices):
    for i in indices:
        vector[i] = -vector[i]


def prepare_column(target, depth):
    """Compile down to a signed single cell, then independently play gates forward."""
    size = len(target)
    work = target.copy()
    reduction = []
    for remaining in range(depth,0,-1):
        assert sum(v*v for v in work)==4**remaining
        odds = [i for i,v in enumerate(work) if v%2]
        assert len(odds)%4==0
        groups = [odds[j:j+4] for j in range(0,len(odds),4)]
        negatives = [i for i in odds if work[i]%4==3]
        flip(work,negatives)
        a,b = matchings(size,groups)
        work = balanced_layer(balanced_layer(work,a),b)
        assert all(v%4==0 for v in work)
        work = [v//4 for v in work]
        reduction.append(dict(groups=groups,negative_sign_cells=negatives))
    chosen, = [i for i,v in enumerate(work) if v]
    assert abs(work[chosen])==1
    vector = [0]*size
    vector[0] = 1
    vector[0],vector[chosen] = vector[chosen],vector[0]
    vector[chosen] *= work[chosen]
    for step in reversed(reduction):
        a,b = matchings(size,step["groups"])
        vector = balanced_layer(balanced_layer(vector,b),a)
        flip(vector,step["negative_sign_cells"])
    assert vector==target
    return vector, dict(blank_to_cell_swap=[0,chosen],initial_sign=work[chosen],
                        reduction_rounds=reduction,live_Walsh_quads=sum(len(s["groups"]) for s in reduction))


def fraction_list(values):
    return [str(v) for v in values]


def distribution(weights):
    return [Fraction(v,sum(weights)) for v in weights]


def trial(name, amplitudes):
    nonzero = [abs(n) for n in amplitudes if n]
    L = lcm(*nonzero)
    depth = L.bit_length()
    scale = 2**depth
    failures = scale**2-L**2
    size = max(4,2**((failures+max(nonzero)**2-1).bit_length()))
    columns,recipes = [],[]
    successful = []
    born = distribution([n*n for n in amplitudes])
    for n in amplitudes:
        # All branches use the same failure-tag cells. A zero-amplitude branch
        # permits an arbitrary normalized extension; keep it at the blank.
        target = [0]*size
        if n:
            target[:failures] = [1]*failures
            target[failures:failures+n*n] = [L//n]*(n*n)
        else:
            target[0] = scale
        col,recipe = prepare_column(target,depth)
        columns.append(col)
        recipes.append(recipe)
        successful.append([n*x for x in col[failures:] if n*x])
    assert all(s==[L]*(n*n) for s,n in zip(successful,amplitudes))
    assert all([n*col[f] for n,col in zip(amplitudes,columns)]==amplitudes for f in range(failures))
    norm = sum(n*n for n in amplitudes)
    assert sum((n*w)**2 for n,col in zip(amplitudes,columns) for w in col)==scale**2*norm
    assert sum(map(len,successful))==norm

    # A fourth-power escort is normalized and permutation-covariant for each
    # individual read; test whether it preserves the old flag across this circuit.
    quartic_before = distribution([n**4 for n in amplitudes])
    quartic_after = distribution([sum((n*w)**4 for w in col) for n,col in zip(amplitudes,columns)])
    quartic_gap = sum(abs(x-y) for x,y in zip(quartic_before,quartic_after))/2
    reference = [int(n!=0) for n in amplitudes]
    alternative = distribution(reference)
    consistency = []
    for ticket in (Fraction(0),Fraction(1,11),Fraction(1,2),Fraction(1)):
        def residual(proposed):
            return [p-(ticket*b+(1-ticket)*p) for p,b in zip(proposed,born)]
        assert not any(residual(born))
        assert any(residual(alternative)) == (ticket>0 and alternative!=born)
        consistency.append(dict(success_weight=str(ticket),squared_candidate_residual=fraction_list(residual(born)),
                                uniform_nonzero_candidate_residual=fraction_list(residual(alternative))))

    return dict(case=name,input=amplitudes,squared_norm=norm,nonzero_flags=len(nonzero),
                success_count_per_flag=[len(s) for s in successful],L=L,s=depth,denominator=scale,
                common_failure_tags=failures,conditional_ancilla_dimension=size,old_flag_dimension=len(amplitudes),
                total_flag_ancilla_cells=len(amplitudes)*size,actual_balanced_ticks=2*depth,
                success_amplitude_numerator=L,common_failure_vector_numerators=amplitudes,
                recipes=recipes,actual_dyadic_columns_sha256=sha256(json.dumps(columns,separators=(",",":")).encode()).hexdigest(),
                squared_flag_weights=fraction_list(born),quartic_before=fraction_list(quartic_before),
                quartic_after=fraction_list(quartic_after),quartic_marginal_total_variation=str(quartic_gap),
                consistency_examples=consistency,
                squared_norm_fraction_on_success_for_comparison_only=str(Fraction(L**2,scale**2)))


def main():
    inputs = {"odd_three_and_seven_units":[3]+[1]*7,"four_tick_walk_herald":[2,1],
              "mixed_signs_and_zero":[-3,0,2,1],"two_distinct_odd_factors":[6,-10,15,0,-3],
              "single_occupied_flag":[0,-1,0],"equal_magnitudes":[-2,2,2],"common_odd_factor":[3,-6,0]}
    rows = [trial(name,values) for name,values in inputs.items()]
    assert all((Fraction(r["quartic_marginal_total_variation"])>0)==
               (len({abs(n) for n in r["input"] if n})>1) for r in rows)
    return dict(cases=rows,
        checks=dict(exact_forward_columns=True,each_ancilla_tick_a_perfect_pair_matching=True,
                    signed_success_cells_equal=True,all_failure_tag_states_restore_input=True,
                    squared_norm_conserved=True,quartic_countercontrol=True,zero_success_cancellation_boundary=True),
        gates="At each old flag, the controlled permutation routes the blank to the listed initial cell. Apply its "
              "listed sign. Read reduction_rounds in reverse. In a quartet (a,b,c,d) apply first H to (a,c),(b,d), "
              "then to (a,b),(c,d); outside all quartets apply H twice to consecutive unused cells, yielding identity. "
              "Apply the listed sign flips after that pair of layers. Every branch has the same number of H clocks. "
              "The operator is block diagonal on the old flag, and acts reversibly on the complete ancilla space.",
        probability_argument="Assume old-flag marginal invariance under these controlled ancilla operations, additivity "
              "of the joint records, permutation symmetry of equal occupied success cells, impossibility of zero "
              "cells, and the operational rule that conditioning on an individual failure tag restores the old "
              "preparation's flag law. For positive total success weight t these imply p_i=t*n_i^2/S+(1-t)*p_i, "
              "so p_i=n_i^2/S. No numerical success probability enters this argument. The t=0 row shows the "
              "cancellation premise explicitly. Conditioning and positivity are probability assumptions.",
        scope="Finite nonzero signed integer input vectors and a coherent old flag. The applicable gate model "
              "provides conditional full-coordinate permutations, signs and global balanced pair matchings. "
              "Native spatial implementation and resource cost beyond the explicit register and layers require "
              "a separate construction. A stored squared-norm success fraction is a circuit diagnostic; the "
              "consistency equations permit arbitrary positive t at this stage.")


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output",type=Path)
    directory = parser.parse_args().output
    data = main()
    directory.mkdir(parents=True,exist_ok=True)
    (directory/"heralded_weights.json").write_text(json.dumps(data,separators=(",",":"))+"\n",encoding="utf8")
    print(data["checks"])
