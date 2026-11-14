"""Verify fixed-schedule predictions and finite exposure for the eight scalar masks."""

from argparse import ArgumentParser
from fractions import Fraction as Q
from itertools import product
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def step(coeff, numerator, denominator):
    """Numerators of the Bernoulli convolution, in increasing hit-count order."""
    fail = denominator-numerator
    return [coeff[0]*fail, *(a*numerator+b*fail for a,b in zip(coeff,coeff[1:])),
            coeff[-1]*numerator]


def direct_paths(probs, denom):
    dist = [0]*(len(probs)+1)
    for word in product((0,1),repeat=len(probs)):
        weight = 1
        for x,p in zip(word,probs):
            weight *= p if x else denom-p
        dist[sum(word)] += weight
    return dist


def decimal_up(numer,denom,digits=9):
    unit = 10**digits
    upper = (numer*unit+denom-1)//denom
    return f"{upper//unit}.{upper%unit:0{digits}d}"


def study(sites, square):
    resolution = 2**16
    # Upper Bernoulli parameters dominate the identity's upper tail. Lower
    # parameters dominate the square's lower tail for every possible cutoff.
    upper = [(p.numerator*resolution+p.denominator-1)//p.denominator for p in sites]
    lower = [p.numerator*resolution//p.denominator for p in square]
    plans = [(0,0,Q(1,20)), (2,1,Q(1,20)), (4,2,Q(1,20)), (0,0,Q(1,100))]
    done = {}
    identity = [1]
    squared = [1]
    for blocks in range(1,101):
        n = 8*blocks
        for p,q in zip(upper,lower):
            identity = step(identity,p,resolution)
            squared = step(squared,q,resolution)
        den = resolution**n
        require(sum(identity)==sum(squared)==den, "convolution preserves all paths")
        if blocks==1:
            require(identity==direct_paths(upper,resolution) and squared==direct_paths(lower,resolution),
                    "first block independent enumeration")
        cdf0, cdf1 = [0], [0]
        for a,b in zip(identity,squared):
            cdf0.append(cdf0[-1]+a)
            cdf1.append(cdf1[-1]+b)
        for u,c,alpha in plans:
            key = (u,c,alpha)
            if key in done:
                continue
            for cutoff in range(1,n+1):
                # P(identity true hits >= cutoff-c), P(square true hits < cutoff+u+c).
                false_square = den-cdf0[max(cutoff-c,0)]
                false_identity = cdf1[min(cutoff+u+c,n+1)]
                if max(false_square,false_identity)*alpha.denominator<=alpha.numerator*den:
                    done[key] = dict(exposures=n,blocks=blocks,confirmed_hit_cutoff=cutoff,
                                     max_unresolved=u,max_corrupt=c,each_error_goal=str(alpha),
                                     false_square_upper=decimal_up(false_square,den),
                                     false_identity_upper=decimal_up(false_identity,den))
                    break
        if len(done)==len(plans):
            return dict(parameter_denominator=resolution,identity_upper_numerators=upper,
                        square_lower_numerators=lower,certificates=[done[p] for p in plans])
    raise ValueError("exposure search limit")


def interval_control():
    """Exhaust small missing/flip configurations and both worst-case cutoffs."""
    n=7
    for t in range(n+1):
        for u in range(3):
            for c in range(3):
                feasible=set()
                for erase_yes in range(min(t,u)+1):
                    for erase_no in range(min(n-t,u-erase_yes)+1):
                        for flip_yes in range(min(t-erase_yes,c)+1):
                            for flip_no in range(min(n-t-erase_no,c-flip_yes)+1):
                                h=t-erase_yes-flip_yes+flip_no
                                unknown=erase_yes+erase_no
                                require(max(0,h-c)<=t<=min(n,h+unknown+c),"identified count interval")
                                feasible.add(h)
                require((min(feasible),max(feasible))==(max(0,t-u-c),min(n,t+c)),
                        "sharp corrupted confirmed hit extremes")
    return n


def main():
    parser=ArgumentParser(description=__doc__)
    parser.add_argument("output",type=Path)
    out=parser.parse_args().output
    source=Path(__file__).parent/"results"/"shifted_site_mask.json"
    row=json.loads(source.read_bytes())["three_bit_mirrored_shell_bins"]
    size=int(row["denominator"])
    bins=list(map(int,row["bin_numerators"]))
    masks=[[(j-i)%8<5 for j in range(8)] for i in range(8)]
    require(all(sum(col)==5 for col in zip(*masks)), "offline score of every bin label")
    # Untabulated radii map to bin zero in both operations.
    labels={r:k for k,group in enumerate(row["bin_radii"]) for r in group}
    for x in [-259,-258,-1,0,2,1,257,258,259]:
        require(sum(mask[labels.get(abs(x),0)] for mask in masks)==5, "singleton read")
    sums=[sum(v for v,keep in zip(bins,mask) if keep) for mask in masks]
    require(sums==list(map(int,row["seed_mass_numerators"])), "actual eight masks")
    sites=[Q(v,size) for v in sums]
    square=[p*p/(p*p+(1-p)**2) for p in sites]
    expected0=sum(sites)/8
    expected1=sum(square)/8
    require(expected0==Q(5,8) and Q(735281069747005,10**15)<expected1<Q(735281069747007,10**15),
            "exact means under the balanced schedule")
    # Shared uniform U is fixed across launches; rational interval between
    # extrema shows that most data sets are all zero or all one forever.
    shared = [min(square),1-max(square)]
    require(sum(shared)>Q(98,100), "strong dependence control")
    record=dict(identity_mean=str(expected0),square_mean_enclosure=["0.735281069747005","0.735281069747007"],
                per_setting_square_minus_identity=[float(q-p) for p,q in zip(sites,square)],
                sharp_small_counts_exhausted=interval_control(),shared_uniform_all_one_or_all_zero=float(sum(shared)),
                fixed_exposure=study(sites,square))
    with out.open("x",encoding="utf-8",newline="\n") as f:
        json.dump(record,f,indent=2)
        f.write("\n")


if __name__=="__main__":
    main()
