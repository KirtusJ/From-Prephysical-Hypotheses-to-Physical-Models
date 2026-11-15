"""Estimate incident per-prefix and terminal-sum scores from one six-bit histogram.

python analyze_write_powers.py run.json [--alpha 0.05]
python analyze_write_powers.py --ideal uniform-t
python analyze_write_powers.py --ideal addressed-real
"""
import argparse
from collections import Counter
from decimal import Decimal, getcontext
from functools import cmp_to_key
import json
from pathlib import Path
from runpy import run_path


HERE = Path(__file__).resolve().parent
PROTOCOL = {"uniform-t":"check_all_writes.py", "addressed-real":"addressed_write_test.py"}
HELPERS = run_path(str(HERE / "analyze_counts.py"))
ZERO = (0,0)
getcontext().prec = 60
D = Decimal


def key(w):
    a,b,c=w
    return f"{a+4*b+16*c:06b}"


def compare(a,b):
    """Sign of A+B*sqrt(2), including exact equality of algebraic levels."""
    A,B=a[0]-b[0],a[1]-b[1]
    if not A and not B:
        return 0
    if A>=0 and B>=0:
        return 1
    if A<=0 and B<=0:
        return -1
    return (1 if A>0 else -1) * (1 if A*A>2*B*B else -1)


def scorers(protocol):
    source=run_path(str(HERE/PROTOCOL[protocol]))["ordinary_word_weights"]()
    if set(map(key,source))!=set(f"{i:06b}" for i in range(64)):
        raise ValueError("ordinary law must include every six-bit word")
    totals={}
    for word,p in source.items():
        if compare(p,ZERO)<0:
            raise ValueError("negative expected mass")
        for size in range(4):
            prefix=word[:size]
            a,b=totals.get(prefix,ZERO)
            totals[prefix]=(a+p[0],b+p[1])
    if totals[()]!=(512,0):
        raise ValueError("model weights must sum to (512,0)")
    root2=D(2).sqrt()
    def mass(pair):
        return D(pair[0])+D(pair[1])*root2
    nodes={}
    terminal={w:D(0) for w in source}
    for prefix,p in sorted(totals.items(), key=lambda item:(len(item[0]),item[0])):
        if p==ZERO or len(prefix)==3:
            continue
        children=[totals[prefix+(i,)] for i in range(4)]
        counts=Counter(children)
        levels=sorted((r for r in counts if r!=ZERO),key=cmp_to_key(compare))
        if len(levels)<3:
            raise ValueError(f"model lacks three positive levels at {prefix}")
        low,middle,high=levels[0],levels[1],levels[-1]
        theta=(mass(middle)/mass(low)).ln()/(mass(high)/mass(low)).ln()
        coeff={low:(1-theta)*mass(p)/(counts[low]*mass(low)),
               middle:-mass(p)/(counts[middle]*mass(middle)),
               high:theta*mass(p)/(counts[high]*mass(high))}
        scores={w:(coeff.get(children[w[len(prefix)]],D(0))
                   if w[:len(prefix)]==prefix else D(0)) for w in source}
        nodes[prefix]=(scores,children,coeff)
        if len(prefix)==2:
            for w in source:
                terminal[w]+=scores[w]
    return source,nodes,terminal


def summary(data, protocol, alpha):
    source,nodes,terminal=scorers(protocol)
    # One family contains every scored prefix, the terminal sum and an explicit
    # dark-word indicator. Dependence among these statistics is allowed.
    dark_words={w for w,p in source.items() if p==ZERO}
    score_list=[("terminal_sum",terminal),("dark_word",{w:D(w in dark_words) for w in source})]
    for prefix,(scores,_,_) in nodes.items():
        name="prefix:"+"".join(map(str,prefix))
        score_list.append((name,scores))
    answer={"protocol":protocol, "score_family_size":len(score_list),
            "numeric_precision":"Algebraic levels and ties are exact. Decimal score bounds and intervals "
                                "are 60-digit numerical estimates, not outward-rounded certificates."}
    if data is None:
        # AM-GM coefficients were constructed to give exact zero ordinary mean.
        # Check every mean numerically to catch any implementation mistake.
        p={w:(D(a)+D(b)*D(2).sqrt())/512 for w,(a,b) in source.items()}
        if any(abs(sum(p[w]*s[w] for w in source))>D("1e-54") for _,s in score_list):
            raise ValueError("ordinary mean inconsistent with zero")
        answer.update(provenance="ideal",confidence_level=None,
                      ordinary_dark_words=sorted(map(key,dark_words)),
                      scores={name:{"ordinary_mean":"0"} for name,_ in score_list})
    else:
        if not isinstance(data,dict) or data.get("schema")!="write-power-counts-v1":
            raise ValueError("expected write-power-counts-v1")
        provenance=data["provenance"]
        if provenance not in ("simulator","hardware"):
            raise ValueError("declare hardware or simulator; use --ideal for ordinary predictions")
        n=HELPERS["integer"](data["attempts"])
        if not n:
            raise ValueError("no attempted launches")
        counts=data["counts"]
        if not isinstance(counts,dict):
            raise ValueError("counts must map six-bit display strings to multiplicities")
        for word,m in counts.items():
            HELPERS["displacements"](word)
            HELPERS["integer"](m)
        complete={w:counts.get(key(w),0) for w in source}
        missing=n-sum(complete.values())
        if missing<0:
            raise ValueError("more recorded words than attempts")
        buckets={}
        factor=((D(2*len(score_list))/alpha).ln()/(2*n)).sqrt()
        for name,s in score_list:
            a,b=min(s.values()),max(s.values())
            seen=sum(complete[w]*s[w] for w in source)
            lo,hi=(seen+a*missing)/n,(seen+b*missing)/n
            e=(b-a)*factor
            buckets[name]={"possible_sample_mean":[str(lo),str(hi)],
                           "simultaneous_interval":[str(max(a,lo-e)),str(min(b,hi+e))]}
        answer.update(provenance=provenance,attempts=n,recorded=n-missing,missing=missing,
                      confidence_level=str(1-alpha),
                      sampling_assumption="Independent incident launches; missing words may take any six-bit value.",
                      ordinary_dark_words={key(w):complete[w] for w in sorted(dark_words,key=key)},
                      recorded_dark_total=sum(complete[w] for w in dark_words),
                      scores=buckets)
    info={}
    for prefix,(_,children,coeff) in nodes.items():
        row={"child_mass_numerators_A_B":children,
             "scores_in_child_code_order":[str(coeff.get(c,D(0))) for c in children]}
        if data is not None:
            row["recorded_visits"]=sum(complete[w] for w in source if w[:len(prefix)]==prefix)
        info["".join(map(str,prefix))]=row
    answer["prefix_controls"]=info
    if protocol == "addressed-real":
        assumption = ("One fixed real embedding per launch and calibrated relative gate phase, "
                      "occupied-support powers q >= 0, specified projective coin updates, "
                      "and faithfully decoded words or separately bounded readout error.")
        embedding = {"score": "prefix:23", "conservative_gap_per_conjugate_launch": "1/2",
                     "model_assumptions": assumption}
        if data is not None:
            upper = D(answer["scores"]["prefix:23"]["simultaneous_interval"][1])
            if upper < 0:
                embedding["status"] = "The upper confidence limit is below the model minimum."
            else:
                embedding["conjugate_fraction_upper_if_model_holds"] = str(min(D(1), 2*upper))
        answer["real_embedding_comparison"] = embedding
    return answer


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument("histogram",type=Path,nargs="?")
    group.add_argument("--ideal",choices=PROTOCOL)
    parser.add_argument("--alpha",default="0.05",type=Decimal)
    args=parser.parse_args()
    if not args.alpha.is_finite() or not 0<args.alpha<1:
        parser.error("--alpha must be strictly between zero and one")
    data=None
    protocol=args.ideal
    if args.histogram:
        data=json.loads(args.histogram.read_bytes(),object_pairs_hook=HELPERS["object_with_unique_keys"])
        if not isinstance(data,dict) or data.get("protocol") not in PROTOCOL:
            parser.error("expected protocol uniform-t or addressed-real")
        protocol=data["protocol"]
    print(json.dumps(summary(data,protocol,args.alpha),indent=2))


if __name__=="__main__":
    main()
