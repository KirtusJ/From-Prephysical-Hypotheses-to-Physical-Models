"""Unamplified two-well witness on the native staircase flight.

Run from a research checkout with Python 3. The neighboring
check_character_tomography.py supplies the monic cyclotomic reduction.
"""
import argparse
from collections import Counter, defaultdict
from fractions import Fraction
import json
from math import comb
from pathlib import Path

from check_character_tomography import reduced


def require(ok, detail):
    if not ok:
        raise ValueError(detail)


def sharp_state():
    return Counter({(0, 0, 0, 1): 1})


def tick(state, order, block, step):
    next_state = Counter()
    for (x, left, sheet, sign), number in state.items():
        for outgoing in (0, 1):
            if step == 2 and outgoing != block % 2:
                continue
            y = (x + (1 if outgoing == 0 else -1)) % (4*order)
            gain = (sheet + x//2) % order
            target_sign = -sign if left and outgoing else sign
            next_state[y, outgoing, gain, target_sign] += number
    return next_state


def sector_numerators(state, order):
    """Square and sum physical port amplitudes, before quotient by Phi_M."""
    ports = defaultdict(Counter)
    for (x, rail, sheet, sign), number in state.items():
        ports[x, rail][sheet] += sign*number
    lags = [0]*order
    for vector in ports.values():
        for j, v in vector.items():
            for k, w in vector.items():
                lags[(j-k) % order] += v*w
    return [reduce_lags(lags, sector, order) for sector in range(order)]


def reduce_lags(lags, sector, order):
    group = [0]*order
    for i, value in enumerate(lags):
        group[(sector*i) % order] += value
    return reduced(group, order)


def integral_numerator(order, blocks):
    """Haar constant term of the finite sin-square product multiplied by 4^r.

    Use z=exp(2iq), w=exp(2pi i/M). The j-th factor is
    2-z*w^((2j-1)k)-z^-1*w^(-(2j-1)k). Keeping the Fourier mode
    in Z gives the continuous integral even when the spatial ring aliases.
    """
    terms = Counter({(0,0): 1})
    for j in range(1, blocks+1):
        later = Counter()
        for (mode, gap), number in terms.items():
            later[mode,gap] += 2*number
            later[mode+1,(gap+2*j-1) % order] -= number
            later[mode-1,(gap-2*j+1) % order] -= number
        terms = later
    return [terms[0,j] for j in range(order)]


def run_oracle():
    rows = []
    for order in (4,5,6,7,8,9,10,12,16,17):
        levels = {2,4,6}
        if order in (4,5,6):
            levels.update({2*order,2*order+2})
        state = sharp_state()
        for block in range(1,max(levels)+1):
            for step in (1,2):
                state = tick(state,order,block,step)
            if block not in levels:
                continue
            nums = sector_numerators(state,order)
            lags = integral_numerator(order,block)
            haar = [reduce_lags(lags,k,order) for k in range(order)]
            require(sum(state.values()) == 2**block, "complete count word")
            require(all(nums[k] == nums[-k % order] for k in range(order)), "conjugacy")
            if order % 2 == 0 and 2*block < 4*order:
                require(all(nums[k] == nums[(k + order//2) % order] for k in range(order)),
                        "half-order preparation alias")
            mismatches = [k for k in range(order) if nums[k] != haar[k]]
            if 2*block < 4*order:
                require(not mismatches, "ring and integral differ inside degree bound")
                require(nums[0] == [comb(2*block,block)], "zero-field yield")
                if order == 4:
                    require(all(0 <= p[0] <= nums[0][0] and len(p) == 1 for p in nums),
                            "rational M=4 bound")
            require(2**block <= comb(2*block,block), "fair vs continuum maximum")
            rows.append(dict(order=order, blocks=block, original_word_denominator=4**block,
                             all_surviving_count_words=sum(state.values()),
                             integer_sector_numerators_mod_cyclotomic=nums,
                             zero_field_line_numerator=comb(2*block,block),
                             strict_degree_condition=(2*block < 4*order),
                             continuum_integral_disagreements=mismatches))
    return rows


def rational_examples():
    rows = []
    for order, gap_squared, unit_cos in ((4, Fraction(1), Fraction(0)),
                                         (6, Fraction(1,4), Fraction(1,2))):
        for w in [Fraction(0),Fraction(1,11),Fraction(1,3),Fraction(1)]:
            for c in [Fraction(0), (1-w)/5, 1-w]:
                share = 1-w-c
                p2 = (1+w+share*unit_cos)/2
                p3 = 1-(c+w+share*unit_cos**2)/2
                W = 2*(1-p3)-2*unit_cos*(2*p2-1)+unit_cos**2
                require(W==w*gap_squared+c*(1+unit_cos**2), "centered two-well witness")
                require(W >= (w+c)*gap_squared, "all contamination including count")
                rows.append(dict(M=order, zero=str(w), count=str(c), unit=str(share),
                                 clock_two=str(p2), clock_three=str(p3), W=str(W)))
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_directory",type=Path)
    path = parser.parse_args().output_directory
    rows = run_oracle()
    require(any(row["continuum_integral_disagreements"] for row in rows),
            "missing wrapped counterexample")
    data = dict(convention="k=0..M-1; each coefficient vector is an ascending polynomial "
                           "evaluated at exp(2pi i/M); divide by 4^blocks. The "
                           "source-count panel uses 0..1 probabilities including original launch.",
                acceptance=rows, witness_controls=rational_examples())
    path.mkdir(parents=True,exist_ok=True)
    with (path/"witness_flight.json").open("x",encoding="utf8",newline="\n") as out:
        json.dump(data,out,indent=2)
        out.write("\n")


if __name__=="__main__":
    main()
