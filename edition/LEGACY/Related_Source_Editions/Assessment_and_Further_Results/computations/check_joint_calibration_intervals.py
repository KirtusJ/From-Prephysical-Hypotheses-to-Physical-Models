#!/usr/bin/env python3
"""Second arithmetic route for the already fixed binary-calibration experiment.

No import or execution of the primary implementation. This implementation uses
Fraction binomial recurrences, exact CDF quantiles, interval unions/intersections,
and conditional calibration probabilities. It does not build acceptance masks
or enumerate integer-weight count triples. The model and source lineage are
shared, and the reviewer has seen the submitted code/results: this is code
independence for arithmetic checking, not an independent study or experiment.
"""
from fractions import Fraction as Q
from functools import lru_cache
from itertools import product
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
PARENT = HERE
N, M = 80, 4
ALPHA = Q(1,20)
THETA = tuple(Q(j,6) for j in range(7))
CAL = (Q(1,5), Q(1,2), Q(4,5))


def demand(ok, why):
    if not ok:
        raise ArithmeticError(why)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


@lru_cache(None)
def distribution(n, q):
    """Binomial mass by adjacent-mass recurrence, without comb/integer weights."""
    if q == 0:
        return (Q(1),) + (Q(0),)*n
    if q == 1:
        return (Q(0),)*n + (Q(1),)
    masses = [(1-q)**n]
    for k in range(n):
        masses.append(masses[-1] * Q(n-k,k+1) * q/(1-q))
    demand(sum(masses) == 1, "binomial recurrence is not normalized")
    return tuple(masses)


@lru_cache(None)
def cumulative(n, q):
    cdf = [Q(0)]
    for value in distribution(n,q):
        cdf.append(cdf[-1]+value)
    return tuple(cdf)


@lru_cache(None)
def interval(n, q, error):
    """Inclusive-tail strict acceptance from the exact CDF quantiles."""
    cdf = cumulative(n,q)
    cutoff = error/2
    lower = next(k for k in range(n+1) if cdf[k+1] > cutoff)
    upper = next(k for k in range(n,-1,-1) if 1-cdf[k] > cutoff)
    demand(lower <= upper, "empty binomial acceptance interval")
    return lower, upper


def union(parts):
    result = []
    for lo,hi in sorted(parts):
        if result and lo <= result[-1][1]+1:
            result[-1] = (result[-1][0], max(hi,result[-1][1]))
        else:
            result.append((lo,hi))
    return tuple(result)


def intersect(left, right):
    result = []
    i=j=0
    while i<len(left) and j<len(right):
        lo=max(left[i][0],right[j][0]); hi=min(left[i][1],right[j][1])
        if lo<=hi:
            result.append((lo,hi))
        if left[i][1]<right[j][1]: i+=1
        else: j+=1
    return tuple(result)


def all_intersections(parts):
    result=((0,N),)
    for value in parts:
        result=intersect(result,value)
    return result


def probability(n, q, parts):
    cdf=cumulative(n,q)
    return sum((cdf[hi+1]-cdf[lo] for lo,hi in parts),Q(0))


@lru_cache(None)
def reference_candidates(count):
    return tuple(q for q in CAL if interval(M,q,ALPHA/3)[0]<=count<=interval(M,q,ALPHA/3)[1])


@lru_cache(None)
def joint_source_intervals(theta, a, b):
    return union(interval(N,(1-theta)*f+theta*s,ALPHA/3)
                 for f,s in product(reference_candidates(a),reference_candidates(b)))


@lru_cache(None)
def plugin_source_intervals(theta, a, b):
    return (interval(N,(1-theta)*Q(a,M)+theta*Q(b,M),ALPHA),)


def as_number(x):
    return {"fraction":str(x),"decimal":float(x)}


def calculate(p,f,s,target):
    whole={"joint":Q(0),"plugin":Q(0)}
    point={name:{theta:Q(0) for theta in target} for name in whole}
    for a,fa in enumerate(distribution(M,f)):
        for b,sb in enumerate(distribution(M,s)):
            calibration_mass=fa*sb
            for name,rule in (("joint",joint_source_intervals),("plugin",plugin_source_intervals)):
                parts={theta:rule(theta,a,b) for theta in target}
                accepted=all_intersections(parts.values())
                whole[name]+=calibration_mass*probability(N,p,accepted)
                for theta,ranges in parts.items():
                    point[name][theta]+=calibration_mass*probability(N,p,ranges)
    # Every theta in the population fibre has the same true p when f,s are known.
    whole["known"]=probability(N,p,(interval(N,p,ALPHA),))
    point["known"]={theta:whole["known"] for theta in target}
    admission=(probability(N,p,(interval(N,p,ALPHA/3),))
               *probability(M,f,(interval(M,f,ALPHA/3),))
               *probability(M,s,(interval(M,s,ALPHA/3),)))
    demand(whole["joint"]>=admission>=1-ALPHA,"joint coverage/admission inequality failed")
    demand(whole["known"]>=1-ALPHA,"known-calibration coverage failed")
    return {"p":str(p),"f":str(f),"s":str(s),
            "population_identified_set":[str(t) for t in target],
            "whole_set_coverage":{k:as_number(v) for k,v in whole.items()},
            "point_coverage":{k:{str(t):as_number(v) for t,v in ps.items()} for k,ps in point.items()},
            "true_joint_law_acceptance":as_number(admission)}


def main():
    source_code=PARENT/'verify_joint_calibration.py'
    source_result=PARENT/'results/joint_calibration_results.json'
    original_hashes={str(p.relative_to(HERE)):sha(p) for p in (source_code,source_result)}
    fibres={}
    for theta,f,s in product(THETA,CAL,CAL):
        p=(1-theta)*f+theta*s
        fibres.setdefault((p,f,s),set()).add(theta)
    demand(len(fibres)==45 and sum(len(v) for v in fibres.values())==63,"fixed family size mismatch")
    rows=[calculate(p,f,s,tuple(sorted(target))) for (p,f,s),target in sorted(fibres.items())]

    # Compare only after the second-route calculations have been completed.
    original=json.loads(source_result.read_text())
    lookup={(r['p'],r['f'],r['s']):r for r in original['rows']}
    comparisons=0; mismatches=[]
    for row in rows:
        other=lookup[row['p'],row['f'],row['s']]
        demand(row['population_identified_set']==other['population_identified_set'],'population fibre mismatch')
        for name in ('joint','plugin','known'):
            value=row['whole_set_coverage'][name]['fraction']
            comparisons+=1
            if value!=other['whole_set_coverage'][name]['fraction']:
                mismatches.append([row['p'],row['f'],row['s'],'whole',name])
            for theta,value in row['point_coverage'][name].items():
                comparisons+=1
                if value['fraction']!=other['point_coverage'][name][theta]['fraction']:
                    mismatches.append([row['p'],row['f'],row['s'],'point',name,theta])
        comparisons+=1
        if row['true_joint_law_acceptance']['fraction']!=other['true_joint_law_acceptance']['fraction']:
            mismatches.append([row['p'],row['f'],row['s'],'true-law admission'])
    summary={}
    for name in ('joint','plugin','known'):
        minimum=min(Q(r['whole_set_coverage'][name]['fraction']) for r in rows)
        points=[Q(v['fraction']) for r in rows for v in r['point_coverage'][name].values()]
        minimizers=[{k:r[k] for k in ('p','f','s','population_identified_set')} for r in rows if Q(r['whole_set_coverage'][name]['fraction'])==minimum]
        below=sum(Q(r['whole_set_coverage'][name]['fraction'])<1-ALPHA for r in rows)
        summary[name]={"minimum_whole_set_coverage":as_number(minimum),"minimum_point_coverage":as_number(min(points)),"minimizing_laws":minimizers,"laws_below_nominal":below}
        demand(minimum==Q(original['summary'][name]['minimum_whole_set_coverage']['fraction']),'minimum mismatch')
        demand(min(points)==Q(original['summary'][name]['minimum_point_coverage']['fraction']),'point minimum mismatch')
        demand(below==original['summary'][name]['laws_below_nominal'],'nominal-coverage count mismatch')
        demand(sorted(json.dumps(x,sort_keys=True) for x in minimizers)==sorted(json.dumps(x,sort_keys=True) for x in original['summary'][name]['minimizing_laws']),'minimizer list mismatch')
    demand(not mismatches,'fraction mismatch with primary calculation')

    example=next(r for r in rows if (r['p'],r['f'],r['s'])==('1/2','1/5','4/5'))
    # For theta=1/2, plugin p=(a+b)/8: aggregate to the nine possible sums.
    terms=[]; total=Q(0)
    for count_sum in range(2*M+1):
        weight=sum((distribution(M,Q(1,5))[a]*distribution(M,Q(4,5))[count_sum-a]
                    for a in range(M+1) if 0<=count_sum-a<=M),Q(0))
        accepted=interval(N,Q(count_sum,2*M),ALPHA)
        source_probability=probability(N,Q(1,2),(accepted,))
        total+=weight*source_probability
        terms.append({"calibration_count_sum":count_sum,"calibration_probability":str(weight),"source_acceptance_interval":list(accepted),"conditional_source_acceptance_probability":str(source_probability),"coverage_contribution":str(weight*source_probability)})
    demand(total==Q(example['whole_set_coverage']['plugin']['fraction'])<1-ALPHA,'nondegenerate plugin decomposition failed')
    demand(all(sha(HERE/p)==h for p,h in original_hashes.items()),'primary source or output was changed')
    result={
        "status":"PASS", "method":"Fraction adjacent-binomial recurrence; exact CDF quantiles; unions/intersections of integer source-count intervals conditional on the two calibration counts. No masks or integer-weight count-triple loop.",
        "lineage":"Second implementation after exposure to the primary code and results; shared fixed sampling model and research lineage. Code independence is not independent empirical or theoretical replication.",
        "fixed_design":{"N":N,"M_each":M,"alpha":str(ALPHA),"theta":[str(t) for t in THETA],"f_s_grid":[str(q) for q in CAL],"parameter_points":63,"distinct_laws":45,"design_expanded":False},
        "strict_boundary_convention":"Both inclusive binomial tails must be strictly above the cutoff; equality rejects. Joint coordinate cutoff=alpha/6; plugin/known source cutoff=alpha/2.",
        "source_sha256":original_hashes,"checker_sha256":sha(Path(__file__)),
        "exact_fraction_comparisons":comparisons,"mismatches":mismatches,
        "primary_inputs_unchanged":True,"summary":summary,
        "nondegenerate_interior_failure":{"theta":"1/2","f":"1/5","s":"4/5","p":"1/2","row":example,"plugin_nine_term_CDF_decomposition":terms},
        "rows":rows,
        "not_checked":["No enlarged parameter grid or changed design","No empirical data or physical calibration mechanism","No new validation of all continuous-parameter confidence regions","No recheck of the separate closed-rectangle projection formula or expected set cardinalities"],
        "interpretation":"The numerical minima concern the declared finite parameter family and independent streams. Whole-set coverage and pointwise coverage are different when f=s. Coverage does not by itself establish narrow confidence sets or physical identifiability.",
    }
    (HERE/'results/Joint_Calibration_Independent_Arithmetic.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({"status":result['status'],"exact_fraction_comparisons":comparisons,"minimum_whole_set_coverage":{k:v['minimum_whole_set_coverage']['decimal'] for k,v in summary.items()},"laws_below_nominal":{k:v['laws_below_nominal'] for k,v in summary.items()},"nondegenerate_example":example['whole_set_coverage']},indent=2))


if __name__=='__main__':
    main()
