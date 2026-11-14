"""Recover walk cell masses from the ordering of a joint terminal read."""
from argparse import ArgumentParser
from collections import Counter
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path

from check_reflecting_path import physical_step


def hadamard_layers(state):
    """Unnormalised in-place Walsh butterflies, from low bit to high bit."""
    step = 1
    while step < len(state):
        for start in range(0, len(state), 2*step):
            for i in range(start, start+step):
                a, b = state[i], state[i+step]
                state[i], state[i+step] = a+b, a-b
        step *= 2
    return state


def reference(K):
    assert K > 0 and K & (K-1) == 0
    n = 2*K
    masses = []
    for k in range(1,K+1):
        signed = [1 if y < K+k else -1 for y in range(n)]
        output = hadamard_layers(signed.copy())
        direct = [sum(s*(-1)**((y & j).bit_count()) for y,s in enumerate(signed))
                  for j in range(n)]
        assert output == direct and output[0] == 2*k
        assert sum(a*a for a in output) == n*n
        masses.extend(F(a*a, K*n*n) for a in output)
    assert sum(masses) == 1
    return masses


def five_ticks():
    counts = Counter()
    for word in product((0,1), repeat=5):
        x, rail, sign = 5, 0, 1
        for d in word:
            if d == rail == 1:
                sign = -sign
            x += 1 if d == 0 else -1
            rail = d
        counts[x,rail] += sign
    state = [[0,0] for _ in range(11)]
    state[5][0] = 1
    for _ in range(5):
        state = physical_step(state)
    flat = [counts[x,r] for x in range(11) for r in (0,1)]
    assert flat == [entry for pair in state for entry in pair]
    return [F(a*a,32) for a in flat]


def product_cells(science, ref):
    return [[h*r for r in ref] for h in science]


def respond(table, score):
    weights = [[score(c) for c in row] for row in table]
    total = sum(map(sum,weights))
    return [[v/total for v in row] for row in weights]


def fit_one_scalar(table, data):
    """Strictly increasing piecewise-linear interpolation exists iff this passes."""
    assignments = {F(0):F(0)}
    for row, observed in zip(table,data,strict=True):
        for x,y in zip(row,observed,strict=True):
            if assignments.setdefault(x,y) != y:
                return None
    ordered = sorted(assignments.items())
    if any(y0 >= y1 for (_,y0),(_,y1) in zip(ordered,ordered[1:])):
        return None
    assert sum(map(sum,data)) == 1
    return ordered


def exact_grid_ratios(data,K):
    jmax = (K-1)*2*K
    anchor = max(range(len(data)),key=lambda i:data[i][jmax])
    ratios = []
    for row in data:
        if row[jmax] == 0:
            ratios.append(F(0))
            continue
        # All pairs of positive reference numerators, including 1 and K.
        matches = {F(l*l,k*k) for k in range(1,K+1) for l in range(1,K+1)
                   if row[(k-1)*2*K] == data[anchor][(l-1)*2*K]}
        assert len(matches) == 1
        ratios.append(matches.pop())
    return [v/sum(ratios) for v in ratios]


def hull_witness(ref):
    target = product_cells([F(5,8),F(3,8)],ref)
    impostor = product_cells([F(3,4),F(1,4)],ref)
    interpolation = fit_one_scalar(impostor,target)
    return target,interpolation


def strings(table):
    return [[str(x) for x in row] for row in table]


def run():
    h = five_ticks()
    ref = reference(4)
    cells = product_cells(h,ref)
    ordinary = respond(cells,lambda x:x)
    nonlinear = respond(cells,lambda x:x+x*x)
    # Two normalizations are performed before averaging over unknown response types.
    observed = [[(a+b)/2 for a,b in zip(row,other)] for row,other in zip(ordinary,nonlinear)]
    assert exact_grid_ratios(observed,4) == h
    marginal = [sum(row) for row in observed]
    discrepancy = sum(abs(a-b) for a,b in zip(h,marginal))/2
    assert discrepancy > 0
    blind = five_ticks()
    known,impostor = hull_witness(blind)
    assert impostor is not None
    assert hull_witness(ref)[1] is None
    flat_observed = respond(cells,lambda x:F(int(x>0)))
    assert fit_one_scalar(cells,flat_observed) is None
    refsum = sum(ref)
    assert refsum == 1 and sum(r*r for r in ref) > 0
    return {
        "science_kinematic_by_well_then_R_L":list(map(str,h)),
        "reference_K":4,"reference_mass_rows":strings([ref[k*8:(k+1)*8] for k in range(4)]),
        "equal_mix_identity_and_x_plus_x_squared":{
            "reported_word_marginal":list(map(str,marginal)),
            "recovered_from_joint_order":list(map(str,exact_grid_ratios(observed,4))),
            "total_variation_from_kinematic":str(discrepancy),
            "all_joint_rates":strings(observed)},
        "bare_five_tick_reference_impostor":{
            "science_true":["5/8","3/8"],"science_alternative":["3/4","1/4"],
            "interpolation_knots":strings(impostor),
            "initial_observed_table":strings(known)},
        "comparator_cells": {"K":4,"k":2,"l":3,
            "true_ratio":"5/3","alternative_ratio":"3","reference_ratio":"9/4"},
        "flat_on_occupied_support_fails_strictness":True}


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("output",type=Path)
    args = parser.parse_args()
    with args.output.open("x",encoding="utf-8",newline="\n") as sink:
        sink.write(json.dumps(run(),indent=2)+"\n")
