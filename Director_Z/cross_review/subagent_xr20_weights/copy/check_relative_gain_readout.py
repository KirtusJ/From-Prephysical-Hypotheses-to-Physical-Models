"""Reconstruct five-sheet Fourier-pair masses with a one-qubit path label.

Run python -B check_relative_gain_readout.py results. Direction 0 is right
and 1 is left. All measured probabilities use exact integer sheet vectors.
"""
import argparse
from collections import defaultdict
from fractions import Fraction
import json
from math import cos, pi, sin
from pathlib import Path


N, M = 8, 5


def advance(x, c, z, d):
    return (x + (1 if d == 0 else -1)) % N, d, (z + (x == 0)) % M, -1 if c == d == 1 else 1


def representative_words():
    """Keep two distinct prefixes per physical endpoint, residue and sign."""
    current = {(0,0,0,1): [""]}
    layers = [{"depth": 0, "reached_states": 1, "available_positive_gains_at_target": [0]}]
    for t in range(1, 65):
        nxt = defaultdict(list)
        for (x,c,z,s), words in current.items():
            for d in range(2):
                y, dr, v, sign = advance(x,c,z,d)
                dest = nxt[y,dr,v,s*sign]
                dest.extend(w+str(d) for w in words[:2-len(dest)])
        current = nxt
        available = [z for z in range(M) if current.get((0,0,z,1))]
        layers.append({"depth":t, "reached_states":len(current), "available_positive_gains_at_target":available})
        if (len(available) == M and len(current[0,0,0,1]) == 2 and current.get((0,0,0,-1))):
            return t, current, layers
    raise RuntimeError("No common certified horizon within the bound")


def route(word):
    x = c = z = 0
    s = 1
    for d in word:
        x,c,z,sign = advance(x,c,z,int(d))
        s *= sign
    return {"word":word, "x":x, "direction":c, "gain":z, "sign":s}


def norm2(vector):
    return sum(v*v for v in vector)


def exact_instrument(sheet, words, t):
    # The initial plus-label has two equally normalized amplitudes. One
    # joint projector retains all allowed (label, outgoing direction) pairs.
    state = {(label,0,0,z):v for label in range(2) for z,v in enumerate(sheet) if v}
    denominator = 2*norm2(sheet)
    failures = []
    for i in range(t):
        all_edges = defaultdict(int)
        for (label,x,c,z), weight in state.items():
            for d in range(2):
                y, dr, v, sign = advance(x,c,z,d)
                all_edges[label,y,dr,v] += sign*weight
        denominator *= 2
        state = {key:w for key,w in all_edges.items()
                 if w and words[key[0]] is not None and key[2] == int(words[key[0]][i])}
        lost = sum(w*w for key,w in all_edges.items() if key not in state)
        failures.append(Fraction(lost,denominator))
    keys = {(x,c,z) for _,x,c,z in state}
    mass = {}
    for sigma, port in [(1,"plus"),(-1,"minus")]:
        totals = defaultdict(int)
        for x,c,z in keys:
            amplitude = state.get((0,x,c,z),0) + sigma*state.get((1,x,c,z),0)
            totals[x,c] += amplitude**2
        mass[port] = Fraction(sum(totals.values()),2*denominator)
        mass[port+"_target"] = Fraction(totals[0,0],2*denominator)
    accounted = sum(failures)+mass["plus"]+mass["minus"]
    if accounted != 1:
        raise ArithmeticError("Mask failures and final ports do not exhaust the probability tree")
    return {"routes":[None if w is None else route(w) for w in words],
            "first_mask_failure_mass":[str(p) for p in failures],
            "all_masks_pass":str(mass["plus"]+mass["minus"]),
            "all_endpoint_plus":str(mass["plus"]), "all_endpoint_minus":str(mass["minus"]),
            "named_endpoint_plus":str(mass["plus_target"]), "named_endpoint_minus":str(mass["minus_target"]),
            "total_mass":str(accounted)}


def direct_autocorrelation(sheet, t):
    return Fraction(sum(v*sheet[(y-t)%M] for y,v in enumerate(sheet)),norm2(sheet))


def fourier_masses(sheet):
    result=[]
    for k in range(M):
        re=sum(v*cos(2*pi*k*j/M) for j,v in enumerate(sheet))
        im=sum(-v*sin(2*pi*k*j/M) for j,v in enumerate(sheet))
        result.append((re*re+im*im)/(M*norm2(sheet)))
    return [result[0],result[1]+result[-1],result[2]+result[-2]]


def experiment(sheet, t, words):
    base = words[0,0,0,1][0]
    ref = exact_instrument(sheet, [base,None],t)
    den = Fraction(ref["named_endpoint_plus"])
    if den != Fraction(1,4*2**t):
        raise ArithmeticError("Same-clock one-route reference failed")
    moments=[]
    settings=[]
    for a in range(M):
        other=words[0,0,a,1][1 if a == 0 else 0]
        result=exact_instrument(sheet,[base,other],t)
        plus=Fraction(result["named_endpoint_plus"])/den
        minus=Fraction(result["named_endpoint_minus"])/den
        c=plus/2-1
        if not (c == direct_autocorrelation(sheet,a) == (plus-minus)/4 and plus+minus == 4):
            raise ArithmeticError("Instrument and independent autocorrelation disagree")
        moments.append(c)
        settings.append({"sheet_difference":a,"plus_over_reference":str(plus),"minus_over_reference":str(minus),
                         "C":str(c),"instrument":result})
    recovered=[sum(float(c)*cos(2*pi*k*j/M) for j,c in enumerate(moments))*(1 if k==0 else 2)/M
               for k in range(3)]
    direct=fourier_masses(sheet)
    if abs(sum(recovered)-1)>1e-12 or max(abs(a-b) for a,b in zip(recovered,direct))>1e-12:
        raise ArithmeticError("Real Fourier inversion failed the direct sheet Parseval check")
    opposite=exact_instrument(sheet,[base,words[0,0,0,-1][0]],t)
    if opposite["named_endpoint_plus"] != "0" or Fraction(opposite["named_endpoint_minus"])/den != 4:
        raise ArithmeticError("Opposite-sign, same-gain dark control failed")
    different=next(w[0] for (x,c,z,s),w in words.items() if (x,c)!=(0,0) and z==0 and s==1)
    noncoincident=exact_instrument(sheet,[base,different],t)
    if (Fraction(noncoincident["all_endpoint_plus"])/den != 2
        or Fraction(noncoincident["all_endpoint_minus"])/den != 2
        or Fraction(noncoincident["named_endpoint_plus"])/den != 1):
        raise ArithmeticError("Noncoincident-ports control failed")
    # A fixed external k=1 has cos(2π/5) at difference one. A global
    # cyclotomic embedding b=2 also transforms the Fourier description of
    # the localized or biased physical state, permuting its coefficient masses.
    fixed = cos(2*pi/M)
    fixed_after = cos(4*pi/M)
    tagged_checks = []
    for b, predicted in [(1, fixed), (2, fixed_after)]:
        # This control stipulates the complex Fourier preparation by an
        # externally fixed tag. Shift the explicit normalized coordinate ray.
        ray = [complex(cos(2*pi*b*y/M),sin(2*pi*b*y/M))/M**0.5 for y in range(M)]
        shifted = ray[-1:]+ray[:-1]
        ratios = [sum(abs(v+sigma*w)**2 for v,w in zip(ray,shifted)) for sigma in (1,-1)]
        if max(abs(ratios[0]-2-2*predicted),abs(ratios[1]-2+2*predicted)) > 1e-12:
            raise ArithmeticError("Externally tagged coordinate-shift check failed")
        tagged_checks.append({"character_image":b,"plus_over_reference":ratios[0],"minus_over_reference":ratios[1]})
    relabel_mass = [direct[0],direct[2],direct[1]]
    simultaneous=[sum(relabel_mass[k]*cos(2*pi*2*k*a/M) for k in range(3)) for a in range(M)]
    held_mass_only=[sum(direct[k]*cos(2*pi*2*k*a/M) for k in range(3)) for a in range(M)]
    if max(abs(v-float(c)) for c,v in zip(moments,simultaneous)) > 1e-12:
        raise ArithmeticError("Named-coordinate comparison changed under simultaneous relabelling")
    return {"input_integer_sheet":sheet,"normalization_squared":norm2(sheet),"singleton":ref,
            "equal_sign_settings":settings,"moments_from_named_records":[str(c) for c in moments],
            "recovered_pair_masses_k0_k1pm_k2pm":recovered,"direct_grouped_Fourier_masses":direct,
            "controls":{"negative_same_sheet_difference":opposite,"different_physical_endpoint":noncoincident},
            "embedding_control":{"automorphism_b":2,"globally_transformed_algebraic_pair_masses":relabel_mass,
                "same_coordinate_input_C_after_global_transformation":simultaneous,
                "C_if_external_algebraic_pair_masses_held_fixed":held_mass_only,
                "externally_fixed_k1_difference_one":{"before_C":fixed,"after_C":fixed_after,
                    "checked_tagged_coordinate_rays":tagged_checks}}}


def main(output):
    t,words,layers=representative_words()
    result={"model":"Hadamard/sign then conditional spatial shift; departure x=0 adds one sheet unit modulo five. Source and named endpoint (0,R); N=8.",
            "read":"One clean plus label qubit, one coherent label/direction mask after each tick, no label measurement during the walk; final X-basis read. Each first mask failure ends its branch. Sum squared amplitudes over named endpoint sheet coordinates without summing amplitudes across different sheet coordinates.",
            "resources":{"label_qubits":1,"labels":2,"ticks_per_attempt":t,"joint_masks_per_attempt":t,
                "maximum_prescribed_direction_bits_per_setting":2*t,"physical_table_premise":"A controller supplies time- and label-dependent masks preserving all surviving coherences. The normalized input sheet is supplied. Each gain difference refers to a separate circuit."},
            "path_search":"Cap distinct prefixes at two for each (physical site, incoming direction, sheet gain, sign). Equal-state prefixes have identical continuations. Stop at the first common horizon with all five positive gains, two representatives at positive zero, and one at negative zero.",
            "dp_layers":layers,"experiments":[experiment(s,t,words) for s in ([1,0,0,0,0],[2,1,0,0,0],[1,-1,0,0,0])],
            "interpretation":"The real DFT reconstructs probability masses of conjugate character pairs and k=0 relative to the named sheet translation. Rephasing, a globally conjugate orientation, and a globally permuted algebraic character labeling do not follow from these record probabilities. Ratios use the same-clock unconditional singleton plus probability."}
    output.mkdir(parents=True,exist_ok=True)
    dest=output/"relative_gain_readout.json"
    dest.write_bytes((json.dumps(result,indent=2,allow_nan=False)+"\n").encode())
    print(dest,t,[(row["moments_from_named_records"],row["recovered_pair_masses_k0_k1pm_k2pm"]) for row in result["experiments"]])


if __name__ == "__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    main(parser.parse_args().output)
