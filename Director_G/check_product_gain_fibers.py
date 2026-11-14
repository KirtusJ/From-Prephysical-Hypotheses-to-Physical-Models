"""Check product records on a shared cyclic gain sheet, using whole-position masks.

Run python -B check_product_gain_fibers.py OUTDIR. Uses only the standard library.
"""
import argparse
from collections import Counter
from fractions import Fraction
from itertools import combinations, product
import json
from pathlib import Path

from check_compact_residue_preparation import compile_masks, physical_census


def require(ok, message):
    if not ok:
        raise ValueError(message)


def convolve(a, b, order):
    counts = Counter()
    for (s, j), n in a.items():
        for (r, k), u in b.items():
            counts[s*r, (j+k) % order] += n*u
    return counts


def cells(census):
    return [[s, j, multiplicity] for (s, j), multiplicity in sorted(census.items())]


def items(census):
    return [g for g,n in sorted(census.items()) for _ in range(n)]


def physical_local(census, m):
    rows, _, _ = compile_masks(m, items(census), [], 0)
    state = physical_census(rows, m, 0)
    expected = Counter({(0, "R", s, j):n for (s,j),n in census.items()})
    require(state == expected, "local mask failed to prepare its named port/gains")
    return len(rows), Counter({(s,j):n for (_,_,s,j),n in state.items()})


def order_four_scores(census):
    """Count and all folded character scores, using exact Gaussian integer amplitudes."""
    phases = [(1,0), (0,1), (-1,0), (0,-1)]
    scores = [sum(census.values())]
    for label in (0,1,2):
        real = imag = 0
        for (s,j),n in census.items():
            a,b = phases[label*j % 4]
            real += n*s*a
            imag += n*s*b
        scores.append(real*real + imag*imag)
    return scores


def mixed(scores, weights):
    return sum(Fraction(s*w, sum(weights)) for s,w in zip(scores,weights))


def four_products(scores, weights_a, weights_b):
    moments = [[mixed(scores[k], w) for k in ("BB","BH","HH")] for w in (weights_a,weights_b)]
    (aa, ab, ac), (ba, bb, bc) = moments
    return dict(BB_HH=aa*bc, HH_BB=ac*ba, BH_BH=ab*bb,
                BB_BH=aa*bb, BH_BB=ab*ba)


def universal():
    b = Counter({(1,0):5})
    h = Counter({(1,0):3, (-1,0):1, (1,1):1})
    output = []
    for m in (3,4,5,6,8,12):
        states = {}
        times = set()
        for key, left, right in (("BB",b,b), ("BH",b,h), ("HH",h,h)):
            ticks, census = physical_local(convolve(left, right, m), m)
            require(sum(census.values()) == 25, "equal-size single-port calibration")
            states[key] = census
            times.add(ticks)
        require(len(times)==1, "equal launch clocks")
        products = {key:convolve(states[l],states[r],m) for key,l,r in
                    (("BB_HH","BB","HH"),("HH_BB","HH","BB"),("BH_BH","BH","BH"),
                     ("BB_BH","BB","BH"),("BH_BB","BH","BB"))}
        require(products["BB_HH"]==products["HH_BB"]==products["BH_BH"],
                "same-total records disagree before applying scores")
        require(products["BB_BH"]==products["BH_BB"], "swapped total record")
        require(products["BB_HH"]==Counter({(1,0):250, (-1,0):150, (1,1):150,
                                            (-1,1):50, (1,2):25}), "shared 625-word census")
        # An independent ordered pair of gains retains the two factors. Computing convolution
        # by enumerating all 25 x 25 entries must reproduce the same shared histogram.
        independent = Counter((s*r,(j+k)%m) for (s,j),(r,k) in
                              product(items(states["BB"]), items(states["HH"])))
        require(independent==products["BH_BH"], "explicit product-word census")
        output.append(dict(order=m,ticks=times.pop(),local={k:cells(c) for k,c in states.items()},
                           common_625=cells(products["BB_HH"]),common_swap=cells(products["BB_BH"])))
        if m == 4:
            scores = {k:order_four_scores(v) for k,v in states.items()}
            require(scores["BB"]==[25,625,625,625], "BB order-four scores")
            require(scores["BH"]==[25,225,125,25], "BH order-four scores")
            require(scores["HH"]==[25,81,25,1], "HH order-four scores")
    return output, scores


def independent_laws(scores):
    pure = [[int(i==j) for j in range(4)] for i in range(4)]
    distributions = pure + [[int(i in pair) for i in range(4)] for pair in combinations(range(4),2)]
    distributions += [[3,1,4,2],[1,1,1,1]]
    tests=mean_swap_passes=0
    positive_gaps=[]
    for a,b in product(distributions,repeat=2):
        row=four_products(scores,a,b)
        agrees=row["BB_HH"]==row["HH_BB"]==row["BH_BH"]
        equal_pure=a==b and a in pure
        require(agrees==equal_pure, "three-setting identification with unequal marginals")
        gap=(row["BB_HH"]+row["HH_BB"])/2-row["BH_BH"]
        low=sum(Fraction(wa*wb*(bi*hj-bj*hi)**2, 2*sum(a)*sum(b))
                for wa,bi,hi in zip(a,(5,25,25,25),(5,9,5,1))
                for wb,bj,hj in zip(b,(5,25,25,25),(5,9,5,1)))
        require(gap==low and ((gap==0) if equal_pure else (gap>0)), "crossed squared-distance gap")
        if gap>0:
            positive_gaps.append(gap)
        means=[mixed(scores["BH"],w)/mixed(scores["BB"],w) for w in (a,b)]
        swap=row["BB_BH"]==row["BH_BB"]
        require(swap==(means[0]==means[1]), "optional swap must test tilted means alone")
        mean_swap_passes+=int(swap)
        tests+=1
    examples=[]
    for a,b in (([1,0,1,0],[1,0,1,0]),(pure[0],pure[2]),(pure[3],pure[3])):
        out=four_products(scores,a,b)
        require(all(x>0 for x in out.values()), "unexpected zero response")
        examples.append(dict(A=a,B=b,independent_local_products=out))
    require(examples[0]["independent_local_products"]["BB_HH"]==8125 and
            examples[0]["independent_local_products"]["BH_BH"]==5625, "mixed product mismatch")
    asymmetric=[]
    pure_one=pure[2]
    zero_two=[0,1,0,9]
    for a,b in ((pure_one,zero_two),(zero_two,pure_one)):
        row=four_products(scores,a,b)
        crossed=[row["BB_HH"],row["HH_BB"]]
        require(sorted(crossed)==[5625,15625] and row["BH_BH"]==5625,
                "one crossed equality passes despite different marginal laws")
        require((sum(crossed)/2)-row["BH_BH"]==5000, "asymmetric strict gap")
        asymmetric.append(dict(A=a,B=b,independent_local_products=row,half_sum_gap=5000))
    return dict(label_order=["count","folded 0","folded 1","folded 2"],ordered_pairs_checked=tests,
                three_setting_passes=tests-len(positive_gaps),positive_half_sum_gaps=len(positive_gaps),
                smallest_positive_half_sum_gap=min(positive_gaps),largest_half_sum_gap=max(positive_gaps),
                optional_mean_swap_passes=mean_swap_passes,one_equality_counterexamples=asymmetric,
                examples=examples,normalization="Each joint numerator divides by 2^(2*ticks).")


def window_words(m, key, start=0):
    rows = []
    home = start
    for block in key:
        if block in "CI":
            rows.extend((({home-1,home+1} if block=="C" else {home+1}),{home},{home+1}))
            home += 1
        else:
            require(block in "DJ", "unknown filter")
            rows.extend((({home-1,home+1} if block=="D" else {home+1}),
                         ({home,home+2} if block=="D" else {home+2}),{home+1},{home+2}))
            home += 2
    rows = [{x%(4*m) for x in r} for r in rows]
    accepted = []
    for seq in product("RL",repeat=len(rows)):
        x,r,s,g = start,"R",1,0
        for c,mask in zip(seq,rows):
            g = (g+x//2)%m
            x = (x + (1 if c=="R" else -1))%(4*m)
            if r==c=="L":
                s=-s
            r=c
            if x not in mask:
                break
        else:
            require((x,r)==(home%(4*m),"R"), "wrong local window endpoint")
            accepted.append(("".join(seq),s,g))
    return accepted,Counter((s,g) for _,s,g in accepted)


def short_witness():
    words,records={},{}
    for key in ("CC","II","CI","IC"):
        words[key],records[key] = window_words(4,key)
    common=convolve(records["CC"],records["II"],4)
    require(common==convolve(records["CI"],records["IC"],4)==Counter({(1,0):1,(1,1):2,(1,2):1}),
            "six-tick same-total control")
    scores={k:mixed(order_four_scores(c),[1,1,0,0]) for k,c in records.items()}
    x,y=scores["CC"]*scores["II"],scores["CI"]*scores["IC"]
    require((x,y)==(10,9), "short independent positive products")
    return dict(order=4,local_ticks=6,accepted_words=words,shared=cells(common),
                marginal_weights="half counting, half folded character 0",
                probabilities={"CC_II":x/4096,"CI_IC":y/4096})


def short_panels():
    exact=[]
    for m in (3,4,5,6,8,12):
        panel=[]
        for step,fork,single in ((1,"C","I"),(2,"D","J")):
            settings=(fork*2,single*2,fork+single,single+fork)
            singles={}
            for home in (0,step,4*m-1):
                f,fc=window_words(m,fork,home)
                i,ic=window_words(m,single,home)
                words=["RLR","LRR"] if fork=="C" else ["RRLR","RLRR","LRRR"]
                require([w for w,s,g in f]==words and i==f[:1], "incorrect multi-arm paths")
                require(all(s==1 for w,s,g in f), "wrong multi-arm path sign")
                require(all((a[2]-b[2])%m==1 for a,b in zip(f,f[1:])), "translated consecutive gains")
                singles[home,fork],singles[home,single]=fc,ic
            records={}
            for x,y in [(k[0],k[1]) for k in settings]:
                _,records[x+y]=window_words(m,x+y)
                require(records[x+y]==convolve(singles[0,x],singles[step,y],m),
                        "local two-block physical gain factorization")
            ff,ii,fi,if_=settings
            pairs=((ff,ii),(ii,ff),(fi,if_))
            pooled=[convolve(records[x],records[y],m) for x,y in pairs]
            require(pooled[0]==pooled[1]==pooled[2] and sum(pooled[0].values())==(step+1)**2,
                    "short joint fibers differ")
            panel.append(dict(ticks=2*(step+2), settings=pairs, local={k:cells(v) for k,v in records.items()},
                              joint_shared=cells(pooled[0])))
            if m == 4:
                a,b=order_four_scores(singles[0,fork]),order_four_scores(singles[step,fork])
                require(a==b==([2,4,2,0] if fork=="C" else [3,9,1,1]), "fourth-order fork ratios")
                local={k:order_four_scores(v) for k,v in records.items()}
                example=[mixed(local[x],[1,0,1,0])*mixed(local[y],[1,0,1,0]) for x,y in pairs]
                require(example==([4,4,4] if fork=="C" else [5,5,4]), "quarter-turn false pass")
                laws=[[int(i==j) for j in range(4)] for i in range(4)]+[
                    [int(i in pair) for i in range(4)] for pair in combinations(range(4),2)]
                laws += [[3,1,4,2],[1,1,1,1]]
                zeros=[]
                for ai,bi in product(range(len(laws)),repeat=2):
                    wa,wb=laws[ai],laws[bi]
                    values=[mixed(local[x],wa)*mixed(local[y],wb) for x,y in pairs]
                    gap=(values[0]+values[1])/2-values[2]
                    formula=Fraction(sum(u*v*(ri-rj)**2 for u,ri in zip(wa,a)
                                         for v,rj in zip(wb,b)),2*sum(wa)*sum(wb))
                    require(gap==formula and gap>=0, "short averaged gap")
                    if gap==0:
                        zeros.append((ai,bi))
                panel[-1].update(half_count_half_quarter=example,raw_gap=(example[0]+example[1])/2-example[2],
                                 zero_gap_ordered_cases=zeros)
        labels=["count",*range(m//2+1)]
        def value_key(label):
            if label=="count":
                return "cos_zero"
            residue=label%m
            return "cos_zero" if (2*residue)%m!=0 and (4*residue)%m==0 else min(residue,m-residue)
        ties=[(x,y) for x,y in combinations(labels,2) if value_key(x)==value_key(y)]
        require(ties==([("count",m//4)] if m%4==0 else []), "wrong six-tick collision")
        if ties:
            # For z=i the three terms 1,z,z² have total z. Counting still reports three.
            actual=Counter()
            for s,g in window_words(m,"D")[1].elements():
                actual[s,g%4]+=1
            scores=order_four_scores(actual)
            require(scores[0]==3 and scores[1+1]==1, "eight-tick fork missed the quarter turn")
        if m==4:
            common=set(panel[0]["zero_gap_ordered_cases"]) & set(panel[1]["zero_gap_ordered_cases"])
            require(common=={(j,j) for j in range(4)}, "two-panel mixture selection")
        exact.append(dict(order=m,six_tick_ties=ties,panels=panel))
    return exact


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory",type=Path)
    directory=parser.parse_args().directory
    preparations,scores=universal()
    result=dict(scope="Model comparison for fresh independent local preparations. No measured flux.",
                preparations=preparations,order_four=independent_laws(scores),
                six_tick=short_witness(),short_common_fibers=short_panels())
    directory.mkdir(parents=True,exist_ok=True)
    with (directory/"product_gain_fibers.json").open("x",encoding="utf8",newline="\n") as out:
        json.dump(result,out,default=str,separators=(",",":"))
        out.write("\n")
