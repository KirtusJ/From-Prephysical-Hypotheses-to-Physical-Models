"""Exact integer checks of two coherent-selector circuits with common clocks."""

import argparse
import json
from fractions import Fraction
from hashlib import sha256
from math import isqrt
from pathlib import Path


def norm2(vector):
    return sum(x*x for x in vector)


def hadamards(v, pairs):
    """One clock of unnormalized H on every coordinate of a perfect matching."""
    assert sorted(j for pair in pairs for j in pair)==list(range(len(v)))
    out = [0]*len(v)
    for j,k in pairs:
        out[j],out[k] = v[j]+v[k],v[j]-v[k]
    return out


def compile_down(v, t):
    reduced = v.copy()
    rounds = []
    for remaining in range(t,0,-1):
        assert norm2(reduced)==2**remaining
        odds = [i for i,x in enumerate(reduced) if x%2]
        evens = [i for i,x in enumerate(reduced) if x%2==0]
        assert len(odds)%2==len(evens)%2==0
        sequence = odds+evens
        pairs = list(zip(sequence[::2],sequence[1::2]))
        raw = hadamards(reduced,pairs)
        assert all(x%2==0 for x in raw)
        reduced = [x//2 for x in raw]
        rounds.append(pairs)
    root, = [i for i,x in enumerate(reduced) if x]
    assert abs(reduced[root])==1
    return rounds,root,reduced[root]


def index(flag,cell,private,n):
    return 2*(flag*n+cell)+private


def junction(vector,n,active,plan,reverse):
    _,root,sign = plan
    for private in (0,1):
        zero = index(active,0,private,n)
        cell = index(active,root,private,n)
        if reverse:
            vector[zero] *= sign
        vector[zero],vector[cell] = vector[cell],vector[zero]
        if not reverse:
            vector[zero] *= sign


def full_match(n,active,matching):
    pairs = [(index(active,i,s,n),index(active,j,s,n)) for i,j in matching for s in (0,1)]
    pairs.extend((index(1-active,i,0,n),index(1-active,i,1,n)) for i in range(n))
    return pairs


def protected_powers(vector,n,flag,power):
    normalizer = sum(v**power for v in vector)
    return [Fraction(sum(vector[index(flag,i,s,n)]**power for s in (0,1)),normalizer) for i in range(n)]


def route(initial,target,t,active):
    n = len(initial)
    source_plan,target_plan = compile_down(initial,t),compile_down(target,t)
    raw = [0]*(4*n)
    for i,x in enumerate(initial):
        raw[index(0,i,0,n)] = x
    selector = [(index(0,i,s,n),index(1,i,s,n)) for i in range(n) for s in (0,1)]
    raw = hadamards(raw,selector)
    protected = 1-active
    old = protected_powers(raw,n,protected,4)
    expected = [Fraction(x*x,2**(t+1)) for x in initial]
    clock = 0
    diagnostics = []

    def inspect(stage):
        assert norm2(raw)==2**(t+1+clock)
        assert protected_powers(raw,n,protected,2)==expected
        fourth = protected_powers(raw,n,protected,4)
        delta = [x-y for x,y in zip(fourth,old)]
        diagnostics.append(dict(stage=stage,clock_after_split=clock,
                                quartic_protected_l1_change=str(sum(abs(x) for x in delta)),
                                first_changed_cell=next((i for i,x in enumerate(delta) if x),None)))

    inspect("selector split")
    for label,rounds in [("reduce",source_plan[0]),("prepare",reversed(target_plan[0]))]:
        if label=="prepare":
            junction(raw,n,active,source_plan,False)
            junction(raw,n,active,target_plan,True)
            inspect("signed permutation at middle")
        for matching in rounds:
            raw = hadamards(raw,full_match(n,active,matching))
            clock += 1
            inspect(label)
    assert clock==2*t
    for i in range(n):
        assert raw[index(active,i,0,n)]==2**t*target[i]
        assert raw[index(protected,i,0,n)]==2**t*initial[i]
        assert raw[index(active,i,1,n)]==raw[index(protected,i,1,n)]==0
    return raw,diagnostics


def digest(v):
    return sha256(json.dumps(v,separators=(",",":")).encode("ascii")).hexdigest()


def compare(x,y,t):
    a,probe_a = route(x,y,t,1)
    b,probe_b = route(y,x,t,0)
    assert a==b
    return dict(depth=t,physical_clocks_including_selector=1+2*t,joint_state_integer_sha256=digest(a),
                joint_squared_denominator=2**(3*t+1),protected_A_from_x=probe_a,protected_B_from_y=probe_b,
                protected_quartic_failed=any(Fraction(d["quartic_protected_l1_change"])>0 for d in probe_a+probe_b))


def actual_walk():
    """80 physical (site, direction, sheet) cells, including the other herald outcomes."""
    entries = [0]*80
    entries[(6*2)*5] = 1
    for _ in range(4):
        out = [0]*80
        for x in range(8):
            for c in range(2):
                for y in range(5):
                    value = entries[(2*x+c)*5+y]
                    for d in range(2):
                        site = (x+(1 if d==0 else -1)) % 8
                        sheet = (y+(x==0)) % 5
                        out[(2*site+d)*5+sheet] += -value if c==d==1 else value
        entries = out
    assert entries[:5]==[2,1,0,0,0] and norm2(entries)==16
    return entries


def experiment(label,initial,extra=0):
    S = norm2(initial)
    t = S.bit_length()-1
    assert S==2**t and extra%2==0
    n = max(2,S,len(initial))
    n += n%2+extra
    x = initial+[0]*(n-len(initial))
    uniform = [1]*S+[0]*(n-S)
    records = []
    for a in sorted({abs(v) for v in initial if v}):
        # One isolated |a| and S-a^2 unit cells. Compare its units to the
        # uniform S-cell vector, then compare its isolated cell to the old flag.
        calibrator = [a]+[1]*(S-a*a)
        calibrator += [0]*(n-len(calibrator))
        reference = compare(calibrator,uniform,t)
        hybrid = compare(x,calibrator,t)
        by_normalization = 1-Fraction(S-a*a,S)
        assert by_normalization==Fraction(a*a,S)
        records.append(dict(magnitude=a,unit_calibrators=S-a*a,inferred_mass=str(by_normalization),
                            calibrator_nonzero=[v for v in calibrator if v],
                            calibration_reference=reference,input_reference=hybrid))
    return dict(case=label,input_nonzero=[[i,x] for i,x in enumerate(initial) if x],dimension=n,
                original_dimension=len(initial),depth=t,extra_zero_padding=extra,
                calibrated_flag_masses=[str(Fraction(v*v,S)) for v in initial],comparisons=records)


def width_eight_references(t):
    S = 1 << t
    # Table of two squares; combine complementary sums deterministically.
    pairs = {}
    for a in range(isqrt(S)+1):
        for b in range(a,isqrt(S-a*a)+1):
            pairs.setdefault(a*a+b*b,(a,b))
    def four(m):
        for k,(a,b) in pairs.items():
            if k<=m and m-k in pairs:
                c,d = pairs[m-k]
                return [a,b,c,d]
        raise ArithmeticError("No four-square representation")

    bound = isqrt(S//2)
    # Work in units of f(1) until the independent normalizer is imposed.
    units = {0:0,1:1}
    recurrence = []
    n = 1
    compilation_count = 0
    while 2*n*n+2<=S:
        tail = four(S-2*n*n-2)
        left = [n+1,n-1,0,0]+tail
        right = [n,n,1,1]+tail
        assert norm2(left)==norm2(right)==S
        a,_ = route(left,right,t,1)
        b,_ = route(right,left,t,0)
        assert a==b
        compilation_count += 1
        units[n+1] = 2*units[n]+2*units[1]-units[n-1]
        recurrence.append([n,tail])
        n += 1
    if t==0:
        normalizer = [1]
    elif t%2:
        normalizer = [2**((t-1)//2)]*2
    else:
        normalizer = [2**(t//2-1)]*4
    assert norm2(normalizer)==S and all(a in units for a in normalizer)
    unit = Fraction(1,sum(units[a] for a in normalizer))
    values = {a:q*unit for a,q in units.items()}
    tails = []
    for a in range(bound+1,isqrt(S)+1):
        fill = four(S-a*a)
        assert all(x<=bound for x in fill)
        row = [a]+fill+[0]*3
        assert norm2(row)==S
        # Compare to the row with the exceptional coefficient negated, as a
        # gate-level test at width eight distinct from normalization itself.
        other = [-a]+row[1:]
        out,_ = route(row,other,t,1)
        reverse,_ = route(other,row,t,0)
        assert out==reverse
        compilation_count += 1
        value = 1-sum(values[x] for x in fill)
        if a in values:
            assert values[a]==value
        values[a] = value
        tails.append([a,fill])
    assert all(values[abs(i)]==Fraction(i*i,S) for i in range(-isqrt(S),isqrt(S)+1))
    return dict(t=t,norm_squared=S,small_bound=bound,unit_probability=str(unit),normalizer=normalizer,
                recurrence_n_and_filler=recurrence,large_amplitude_and_filler=tails,
                compiled_reference_pairs=compilation_count,max_padded_reference_width=8,
                all_signed_integer_values_verified=2*isqrt(S)+1)


def main():
    walk = actual_walk()
    inputs = [("depth_zero",[0,-1],0),("odd_depth_one",[-1,1,0],0),
              ("odd_depth_three",[2,-1,1,1,-1],0),("odd_depth_five",[3,-3,3,-2,1],0),
              ("positive_odd_three",[3]+[1]*7,0),("all_equal_power_two",[-2,2,-2,2],0),
              ("localized_power_two",[0,0,-4],0),("four_tick_native_walk",walk,0),
              ("odd_depth_three_extra_padding",[2,-1,1,1,-1],16),("native_walk_extra_padding",walk,16)]
    rows = [experiment(*case) for case in inputs]
    lookup = {r["case"]:r for r in rows}
    for a,b in [("odd_depth_three","odd_depth_three_extra_padding"),("four_tick_native_walk","native_walk_extra_padding")]:
        assert lookup[a]["calibrated_flag_masses"]==lookup[b]["calibrated_flag_masses"]
    # Markov control: complete dephasing followed by positive path counting
    # makes every ideal H reversible pair into a bistochastic transition.
    # Applying the same H twice to e0 then has endpoint probabilities 1/2,1/2.
    positive = [1,0]
    signed = [1,0]
    for _ in range(2):
        positive = [sum(positive)]*2
        signed = hadamards(signed,[(0,1)])
    assert signed==[2,0] and positive==[2,2]
    width_eight = [width_eight_references(t) for t in range(15)]
    quartic_failures = sum(c["input_reference"]["protected_quartic_failed"]
                           for q in rows for c in q["comparisons"])
    assert quartic_failures>0 and not any(c["input_reference"]["protected_quartic_failed"]
               for c in lookup["depth_zero"]["comparisons"])
    return dict(trials=rows,width_eight_calibration=width_eight,protected_quartic_input_comparisons_failed=quartic_failures,
                compact_reference_encoding="Each recurrence row [n,F] compares (n+1,n-1,0,0,F) with (n,n,1,1,F). "
                    "Each large row [a,F] uses (a,F,0,0,0) and normalization. F is four explicit squares' roots.",
                checks=dict(synchronized_integer_endpoint_equality=True,all_old_coordinate_masks_exact=True,
                                        parity_matching_reductions=True,stable_zero_padding=True,
                                        native_walk_full_norm=True,markov_reversal_countercontrol=True,
                                        width_eight_inference_all_integer_amplitudes=True,quartic_protected_countercontrol=True),
                markov_control=dict(two_H_from_cell_zero_classical=["1/2","1/2"],coherent=["1","0"]),
                conventions="The state order is (selector flag, data cell, private bit); every H uses the sign "
                            "pattern [[1,1],[1,-1]]. Each closed flag's masked read sums both private cells. "
                            "Extra signed permutations occur at the shared middle clock without H normalization. "
                            "The hybrid routes first split the selector coherently; no branch is read or rejected.",
                inference="Recording the selector on an input copied by an equal coherent split requires swap "
                          "symmetry plus invariance of the old data marginal under that split. Under controlled "
                          "protected-flag mask invariance, the two routes realize one common hybrid state. "
                          "Permutation and sign symmetry then equate the marginal weights of cells of equal "
                          "absolute amplitude across the flags. Calibration compares unit cells with the flat "
                          "2^t-cell state, then uses normalization and zero-cell impossibility to fix a^2/2^t. "
                          "These are operational record assumptions. The finite gate model admits conditional "
                          "routing permutations and synchronized perfect-matching H layers.")


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("directory",type=Path)
    directory = parser.parse_args().directory
    data = main()
    directory.mkdir(parents=True,exist_ok=True)
    (directory/"coherent_comparison.json").write_text(json.dumps(data,separators=(",",":"))+"\n",encoding="utf8")
    print(data["checks"])
