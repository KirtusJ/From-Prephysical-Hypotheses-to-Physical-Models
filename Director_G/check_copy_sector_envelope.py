"""Total sector survival of copied alternating-rail switch words on the staircase.

Run with standard Python: python -B check_copy_sector_envelope.py NEW_DIRECTORY
Every composition is included. Integer coefficients determine sector sums and
their ties. Individual complex-character checks use binary64 and are labelled.
"""

import argparse
from collections import Counter, defaultdict
from fractions import Fraction
from functools import lru_cache
import json
import math
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ArithmeticError(message)


def step(states, order, keep, copy=False):
    """One actual signed H and shift. Copies retain the sharp site as a tag."""
    result = defaultdict(int)
    for (x, rail, y, pointer), amplitude in states.items():
        new_y = (y+x//2) % order
        for out in (1, -1):
            if keep and out != keep:
                continue
            new_tag = pointer + (x+out,) if copy else pointer
            sign = -1 if rail == out == -1 else 1
            result[x+out, out, new_y, new_tag] += sign * amplitude
    return {key: value for key, value in result.items() if value}


def autocorrelation(states, order):
    """Squared field in each character, as a Laurent polynomial on Z/order."""
    ports = defaultdict(dict)
    for (x, c, y, pointer), v in states.items():
        ports[x,c,pointer][y] = v
    coefficients = Counter()
    for port in ports.values():
        for y, a in port.items():
            for z, b in port.items():
                coefficients[(y-z) % order] += a*b
    return {k:v for k,v in coefficients.items() if v}


def segment_kernels(order, m):
    state = {(0,1,0,()):1}
    kernels = [{}]
    for j in range(1, m+1):
        state = step(state, order, 0)
        state = step(state, order, (-1)**j)
        kernels.append(autocorrelation(state, order))
    return kernels


def multiply(a, b, order):
    out = Counter()
    for x, v in a.items():
        for y, w in b.items():
            out[(x+y) % order] += v*w
    return {k:v for k,v in out.items() if v}


def integral_rows(order, m):
    # Each product is a trigonometric polynomial of degree j in exp(2iq);
    # uniform integration over one period uses more than j equally spaced nodes.
    points = 2*m+3
    results = []
    for s in range(order):
        h = math.pi*s/order
        values = [1.0]*points
        lengths = [1.0]
        for j in range(1, m+1):
            for i in range(points):
                values[i] *= math.sin(math.pi*i/points+(2*j-1)*h)**2
            lengths.append(math.fsum(values)/points)
        results.append(lengths)
    return results


def sector(poly, order, s):
    return math.fsum(v*math.cos(2*math.pi*((k*s) % order)/order) for k,v in poly.items())


def compositions(m):
    multiplicities = Counter()
    for mask in range(1 << (m-1)):
        ends = [0]+[i for i in range(1,m) if mask & (1 << (i-1))]+[m]
        multiplicities[tuple(sorted(b-a for a,b in zip(ends,ends[1:])))] += 1
    return sorted(multiplicities.items())


def fraction_text(a, b):
    return str(Fraction(a,b))


def small_pointer_oracle(order, m, kernels):
    rows = []
    for j in range(1,m+1):
        for word in range(1 << (j-1)):
            ends = [0]+[i for i in range(1,j) if word & (1 << (i-1))]+[j]
            expected = {0:1}
            for a,b in zip(ends,ends[1:]):
                expected = multiply(expected,kernels[b-a],order)
            for home, rail in ((0,1),(1,-1)):
                state = {(home,rail,0,()):1}
                for p in range(1,j+1):
                    state = step(state,order,0)
                    state = step(state,order,rail*(-1)**p,word & (1 << (p-1)))
                require(autocorrelation(state,order)==expected, "pointed signed branches")
            rows.append([j,word,expected.get(0,0)])
    return dict(M=order, launch_pairs=[[0,1],[1,-1]],columns=["m","mask","localized numerator at 4^m"],
                rows=rows)


def unit_footprint(order, m):
    """Actual R-launch successful source in sector 1, for a final sharp site copy."""
    state = {(0,1,0,()):1}
    for j in range(1,m+1):
        state = step(state,order,0)
        state = step(state,order,(-1)**j)
    amplitudes = defaultdict(complex)
    for (x,_,y,_), z in state.items():
        phi = -2*math.pi*y/order
        amplitudes[x] += z*complex(math.cos(phi),math.sin(phi))/2**m
    weights = [abs(z)**2 for _,z in sorted(amplitudes.items())]
    total = math.fsum(weights)
    return total, math.fsum((p/total)**2 for p in weights)


def rivals(order, m, seg, patterns):
    free = Fraction(math.comb(2*m,m),4**m)
    all_copied = Fraction(1,2**m)
    units = Fraction(2,order)
    mask_probability = float(units)
    field_on_good = seg[1][m]
    field_on_typical = math.fsum(multiplicity*mask_probability**(len(parts)-1)*
                                 (1-mask_probability)**(m-len(parts))*
                                 math.prod(seg[1][j] for j in parts) for parts,multiplicity in patterns)
    # An identical zero-field mixture of whole masks from a sector-independent
    # Bernoulli selector gives the SAME table for every forced mask F.
    max_deficit = units*(1-all_copied/free)
    src, fidelity = unit_footprint(order,m)
    require(abs(src-field_on_good)<2e-13 and 0<fidelity<1, "last copy purity witness")
    return dict(prior_unit=fraction_text(2,order),
                zero_field_all_good=str(free),
                zero_field_unit_selective=str((1-units)*free+units*all_copied),
                zero_field_relative_deficit=str(max_deficit),
                field_on_unit_survival={
                    "all_good":field_on_good,"only_units_copied_every_boundary":float(all_copied),
                    "exogenous_shared_all_copy_event_probability_2_over_M":
                        (1-mask_probability)*field_on_good+mask_probability*float(all_copied),
                    "independent_boundary_bits_probability_2_over_M":field_on_typical},
                relative_unit_word_retained=float(all_copied)/field_on_good,
                unit_joint_per_original_all_good=mask_probability*field_on_good,
                unit_joint_per_original_selective=mask_probability*float(all_copied),
                final_only_unit_copy=dict(preparation_probability_unchanged=src,
                    coherent_state_projector_expectation_after_copy=fidelity,
                    same_projector_without_copy=1,
                    next_switch_given_word_no_copy=seg[1][m+1]/field_on_good,
                    next_switch_given_word_with_final_copy=0.5))


def panel(order):
    m = 2*max(1,math.floor(0.25*order**(2/3)+0.5))
    require(2*m+2 < 2*order, "unwrapped lightcone")
    kernels = segment_kernels(order,m)
    seg = integral_rows(order,m+1)
    local_err = max(abs(sector(kernels[j],order,s)/4**j - seg[s][j])
                    for s in range(order) for j in range(1,m+1))
    require(local_err<2e-13, "physical polynomials versus sine product")
    patterns = compositions(m)
    denominator = 4**m

    @lru_cache(maxsize=None)
    def kernel(parts):
        if not parts:
            return {0:1}
        return multiply(kernel(parts[:-1]), kernels[parts[-1]], order)

    results = []
    probabilities = []
    for parts,multiplicity in patterns:
        poly = kernel(parts)
        exact_sum_num = order*poly.get(0,0)
        vector = [math.prod(row[j] for j in parts) for row in seg]
        probabilities.append(vector)
        discrepancy = abs(math.fsum(vector)-exact_sum_num/denominator)
        results.append([list(parts),multiplicity,exact_sum_num,discrepancy])
    error = max(row[3] for row in results)
    require(error<1e-11, "all-character sum versus exact constant coefficient")
    require(sum(row[1] for row in results)==2**(m-1), "all compositions covered")
    # At a localized terminal x the count of middle L hops is fixed by x
    # and the projected final directions. It fixes the common history sign.
    # Copying thus only splits same-sign sums in each localized sheet cell.
    numerators = {tuple(row[0]):row[2] for row in results}
    refinements = []
    for parts in numerators:
        for i, length in enumerate(parts):
            for a in range(1,length):
                split = tuple(sorted(parts[:i]+parts[i+1:]+(a,length-a)))
                gap = numerators[parts]-numerators[split]
                require(gap>=0, "a localized all-sector pointer refinement increased survival")
                refinements.append(gap)

    def maximum(rows):
        best = max(r[2] for r in rows)
        tied = [r for r in rows if r[2]==best]
        return dict(max_exact=fraction_text(best,denominator),max_times_sqrt_m=best/denominator*math.sqrt(m),
                    maximizing_patterns=[r[0] for r in tied],ordered_degeneracy=sum(r[1] for r in tied))

    by_cuts = [maximum([r for r in results if len(r[0])==q]) for q in range(1,m+1)]
    folded = []
    for s in range(order//2+1):
        values = [v[s] for v in probabilities]
        k = max(range(len(values)),key=values.__getitem__)
        folded.append(dict(s=s, no_copy=seg[s][m],all_copied=2**(-m),max=values[k],
                           min=min(values),one_maximizer_binary64=results[k][0]))
    sheet_good = order*kernels[m].get(0,0)
    return dict(M=order,m=m,ordered_patterns=2**(m-1),
                all_good_sector_sum=fraction_text(sheet_good,denominator),
                all_copy_sector_sum=fraction_text(order,2**m),
                max_S_over_all=maximum(results),max_S_indexed_by_number_cuts=by_cuts,
                sector_sum_denominator=denominator,
                partition_rows=results,sector_extrema_binary64=folded,
                single_split_checks=dict(number=len(refinements),
                    ties=refinements.count(0),largest_numerator_decrease=max(refinements)),
                method_agreement_max_absolute={"segment":local_err,"summed_patterns":error},
                controls=rivals(order,m,seg,patterns))


def run():
    orders=(5,6,11,12,17,32,33,48,49,64,65,88,89,120,121,128,129)
    return dict(definitions=dict(
        setting="Zero to m-1 unread sharp site copies between the m two-tick opposite-rail records. Fixed mask and a localized physical sheet of order M; uniform Fourier weights.",
        quantity="S sums unnormalized word probabilities over all M signed charges. Original-sheet probability is S/M.",
        cuts="Bit i-1 copies the site after block i; the last-only control instead copies after the final successful block.",
        multiplicity="Rows [sorted segment lengths, number of ordered masks, integer numerator of S, absolute difference of independent trigonometric sum]. These rows encode every ordered composition, including all ties in S.",
        maxima="Global and cut-count maxima and ties use exact integers. Per folded charge one numerical maximizer is given; exact ties between partitions there are not resolved.",
        refinement="A pass at each block fixes its final rail. The complete history sign is (-1) to the number of middle L hops, fixed by terminal x. An additional site pointer separates same-sign sums in the localized sheet. Every additive single split of every partition is checked, including repeated parts and both split orders.",
        correlated_rival="The units alone copy every internal boundary. Exogenous comparison copies every boundary with probability 2/M, independently of sector, or uses iid per-boundary bits with that same rate. The first comparison agrees under ALL zero-field forced masks. Sector-dependent copies require access to the charge or an initially correlated apparatus.",
        final_copy="Expectation of the incident successful coherent-state projector after a final unread copy equals the sum of squared normalized position probabilities. An additional native opposite-rail switch also probes the change.",
        limits="Finite fixed-order data. No threshold constant or asymptotic rate is fitted."),
        pointer_oracles=[small_pointer_oracle(q,5,segment_kernels(q,5)) for q in (7,8,11)],
        panels=[panel(q) for q in orders])


if __name__ == "__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination",type=Path)
    path=parser.parse_args().destination/"copy_sector_envelope.json"
    if path.exists():
        raise FileExistsError(path)
    result=run()
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("x",encoding="utf-8",newline="\n") as output:
        json.dump(result,output,indent=2,allow_nan=False)
        output.write("\n")
