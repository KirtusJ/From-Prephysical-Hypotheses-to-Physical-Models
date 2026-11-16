"""Find the minimum number of power settings for one specified optical-circle readout."""
from argparse import ArgumentParser
from fractions import Fraction as F
from itertools import combinations, pairwise
from pathlib import Path
from runpy import run_path
import json

full = run_path(str(Path(__file__).with_name('check_full_circle_display.py')))
require = full['require']
# Each mapping is a group of rounds sharing an initial power. Values are
# relative response weights used before applying the round normalization.
EFFECTIVE = ({0:7,2:12,3:25}, {5:47,6:16,17:199}, {4:7,7:38,8:8},
             {9:9,10:2,15:18}, {11:20,12:5,13:65}, {1:18,16:2,19:25}, {14:7,18:6})
ATTENUATED = ({2:791,3:1457,9:314,10:44,16:7}, {4:734,11:182,13:37,15:10,19:3},
              {0:259,5:676,6:106,12:44,14:12}, {1:167,7:218,8:47,17:10,18:2})
RETENTION = (F(3,5), F(33,50))
MARGIN = F(1,4096)


def ordered_keys(group, x, lower, upper):
    # Adjacent positive inputs must preserve their strict order for every
    # allowed retention profile. Common factors through the earlier round cancel.
    cells = [k for k,v in x.items() if k[0] in group and v > 0]
    cells.sort(key=lambda k: x[k]*lower**k[0])
    for (t,m),(h,n) in pairwise(cells):
        delta = h-t
        require(x[t,m] < x[h,n]*min(lower**delta,upper**delta),
                'input order changes within the group')
    return cells


def fit(groups, x, bands, lower, upper, separate_powers=True):
    rounds = sorted(t for group in groups for t in group)
    require(rounds == list(range(20)), 'round partition')
    powers, normalizations, response = {}, {}, {}
    # Use the midpoint only to exhibit the knots of one curve. Order checks
    # and bounds separating groups cover the entire retention interval.
    midpoint = (lower+upper)/2
    max_input = max_output = F(0)
    for group in groups:
        cells = ordered_keys(group,x,lower,upper)
        floor = min(x[t,m]*lower**t for t,m in cells)
        ceiling = max(x[t,m]*upper**t for t,m in cells)
        power = 1+max_input/floor if separate_powers else F(1)
        require(power*floor > max_input, 'power blocks overlap')
        previous = F(0)
        values = {}
        for t,m in cells:
            lo,hi = bands[t,m]
            if t:
                lo,hi = lo+MARGIN,hi-MARGIN
            else:
                lo=hi=F(1)
            y = max(group[t]*lo, previous+F(1,10**6))
            require(y <= group[t]*hi, 'ordered response misses band')
            values[t,m] = y
            previous = y
        multiplier = 1+max_output/min(values.values())
        max_input = power*ceiling
        max_output = multiplier*max(values.values())
        for t,weight in group.items():
            powers[t] = power
            normalizations[t] = 1/(multiplier*weight)
        for (t,m),y in values.items():
            argument = power*x[t,m]*midpoint**t
            require(argument not in response, 'duplicate positive knot')
            response[argument] = multiplier*y

    response[0] = F(0)
    scale = 2*max_output
    response = {u:y/scale for u,y in response.items()}
    ordered = sorted(response)
    require(all(response[u] < response[v] for u,v in pairwise(ordered))
            and response[ordered[-1]] == F(1,2), 'global response order')
    totals = []
    for t in range(20):
        total = F(0)
        for m in range(10):
            u = powers[t]*midpoint**t*x[t,m]
            q = scale*normalizations[t]*response[u]
            lo,hi = bands[t,m]
            if u>0 and t:
                lo,hi = lo+MARGIN,hi-MARGIN
            require(lo <= q <= hi and (t or q == int(m == 2)), 'full display')
            total += q
        require(0 < total <= 1, 'on-circle total')
        totals.append(total)
    return dict(power_settings=len(set(powers.values())), knots=len(response),
                postlaunch_total_range=list(map(str,(min(totals[1:]),max(totals[1:])))))


def pair_certificate(rounds, x, bands, lower, upper):
    results = []
    for t,h in combinations(rounds,2):
        # Use the smallest later/earlier retention ratio for a lower bound,
        # the largest for the upper bound. Other sites and rounds are immaterial.
        low,_ = full['scale_bounds'](t,h,{k:v*lower**k[0] for k,v in x.items()},bands)
        _,high = full['scale_bounds'](t,h,{k:v*upper**k[0] for k,v in x.items()},bands)
        require(low is not None and high is not None and low[0] > high[0],
                'pair does not exclude a shared power')
        results.append(dict(rounds=[t,h], lower=str(low[0]), lower_sites=low[1:],
                            upper=str(high[0]), upper_sites=high[1:]))
    return results


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('journal_pdf',type=Path)
    parser.add_argument('figure_png',type=Path)
    args = parser.parse_args()
    journal,both = full['read_bands'](args.journal_pdf,args.figure_png)
    x = full['intensities'](full['BLOCH'])
    effective = fit(EFFECTIVE,x,both,F(1),F(1))
    seven = pair_certificate(full['DISTINCT'],x,journal,F(1),F(1))
    attenuated = fit(ATTENUATED,x,both,*RETENTION)
    four = pair_certificate((3,4,5,7),x,journal,*RETENTION)
    require(len(seven)==21 and effective['power_settings']==7 and
            len(four)==6 and attenuated['power_settings']==4, 'power minimum')
    smallest = [min((v,m) for (r,m),v in x.items() if r==t and v>0) for t in range(20)]
    largest = [max((v,m) for (r,m),v in x.items() if r==t and v>0) for t in range(20)]
    limit,t = min((smallest[t][0]/largest[t+1][0], t) for t in range(19))
    require((limit,t,smallest[t][1],largest[t+1][1]) == (F(534652,19857765),18,0,5),
            'strong-loss endpoint')
    strong = fit(tuple({i:1} for i in reversed(range(20))),x,both,limit/2,limit/2,False)
    require(strong['power_settings']==1, 'single-power control')
    print(json.dumps(dict(cells=len(x),postlaunch_positive_margin=str(MARGIN),
                          no_loss=effective, no_loss_lower_bound_pairs=len(seven),
                          per_step_retention=list(map(str,RETENTION)), with_loss=attenuated,
                          loss_lower_bound_pairs=four,strong_loss_sufficient_open_limit=str(limit),
                          strong_loss_single_power_control=strong),indent=2))


if __name__ == '__main__':
    main()
