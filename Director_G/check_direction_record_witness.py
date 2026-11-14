"""Compare broad direction reports with an unread copy of the intermediate site.

Run python -B check_direction_record_witness.py OUTDIR. Only integer path sums,
cyclic sheet addresses and rational probabilities enter the finite witness.
"""
import argparse
import json
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path
from math import expm1, log


def require(ok, why):
    if not ok:
        raise ValueError(why)


def paths(ticks, incoming="R", home=0):
    rows=[]
    for letters in product("RL",repeat=ticks):
        x, rail, g, sign=home,incoming,0,1
        trail=[]
        for out in letters:
            g+=x//2
            if rail==out=="L":
                sign=-sign
            x+=1 if out=="R" else -1
            rail=out
            trail.append(x)
        rows.append(("".join(letters),trail,g,sign))
    return rows


def instrument(rows, order, prefix):
    """Columns are broad, copied-site and counted numerators; both flags retained."""
    bins=defaultdict(lambda:defaultdict(Counter))
    counted=Counter()
    for word,trail,gain,sign in rows:
        final_x=trail[-1]
        tag=trail[prefix-1]
        if order is not None:
            # Output coordinates are given relative to home 0 in the centred ring chart.
            final_x=(final_x+2*order)%(4*order)-2*order
            tag%=4*order
            gain%=order
        key=word[prefix-1],final_x,word[-1]
        counted[key]+=1
        bins[key][tag][gain]+=sign
    result={}
    for key,sites in bins.items():
        addresses=set().union(*(poly.keys() for poly in sites.values()))
        broad=sum(sum(poly[a] for poly in sites.values())**2 for a in addresses)
        hidden=sum(sum(v*v for v in poly.values()) for poly in sites.values())
        result[key]=[broad,hidden,counted[key]]
    denominator=len(rows)
    require(all(sum(row[i] for row in result.values())==denominator for i in (0,1,2)),
            "unconditioned probability did not normalize")
    return result


def census():
    cases=[]
    orders=(*range(3,29),None)
    summary={m:[] for m in orders}
    for t in range(2,9):
        rows=paths(t)
        for order in orders:
            for prefix in range(1,t):
                data=instrument(rows,order,prefix)
                diffs=[[y[0]-y[1] for k,y in data.items() if k[0]==flag] for flag in "RL"]
                require(all(sum(delta)==0 for delta in diffs),"prefix marginal changed")
                denom=2**t
                tv=Fraction(sum(abs(z) for arr in diffs for z in arr),2*denom)
                flag_tv=[str(Fraction(sum(abs(z) for z in arr),2*denom)) for arr in diffs]
                cases.append([order,t,prefix,str(tv),*flag_tv])
                if tv:
                    summary[order].append((t,prefix))
    first=[]
    for order,v in summary.items():
        t=min(a for a,b in v)
        first.append([order,t,[b for a,b in v if a==t],min(a for a,b in v if b==2)])
    require(min(row[1] for row in first)==5 and first[0][1]==5,"shortest witness")
    require(first[-1][1]==7 and first[-1][-1]==7,"unwrapped shortest witness")
    return dict(columns=["order_or_null_for_unwrapped","total_ticks","read_tick","joint_TV",
                         "R_flag_TV_per_launch","L_flag_TV_per_launch"],rows=cases,
                first_columns=["order","earliest","all_detecting_prefixes_at_earliest","earliest_at_prefix_2"],
                earliest=first)


def endpoint_table(order,t):
    data=instrument(paths(t),order,2)
    return [[*k,*v] for k,v in sorted(data.items())]


def witnesses():
    specs=[(3,5,-1,"L",(5,3,3)),(5,6,0,"R",(4,6,6)),
           (None,7,1,"R",(10,12,10)),(None,8,-2,"R",(17,13,15)),
           (None,8,0,"L",(17,21,15))]
    items=[]
    for order,t,x,r,expected in specs:
        rows=paths(t)
        named=[(w,tr[1],g,s) for w,tr,g,s in rows if w[1]=="L" and (tr[-1],w[-1])==(x,r)]
        got=instrument(rows,order,2)["L",x,r]
        require(tuple(got)==expected,"named probability witness")
        tags=sorted({tr for _,tr,_,_ in named})
        require(tags==[-2,0],"two surviving marked sites")
        allbins=endpoint_table(order,t)
        require(sum(row[3] for row in allbins if row[0]=="L")==2**(t-1),"L prefix")
        items.append(dict(M=order,ticks=t,read_at=2,flag="L",event=[x,r],
                          words_gain_sign=[[w,tr,g,s] for w,tr,g,s in named],
                          broad_copied_count=got,denominator=2**t,all_ports=allbins))
    # With a complex marker overlap gamma, physical local-sheet vectors have
    # real coefficients. B(gamma)=copied + Re(gamma)*(broad-copied).
    source=[(0,-1),(-1,-1)]
    other=[(-3,-1)]
    cross_lags=Counter((u-v)%3 for u,a in source for v,b in other)
    require(cross_lags=={0:1,2:1},"M3 phase dependent cross term")
    return items


def mask_search():
    """Smallest fork of two signed words; derive candidate orders from the gaps."""
    summary=[]
    for t in range(2,7):
        words=paths(t)
        candidates=isolated=0
        gaps=set()
        for left,right in combinations(words,2):
            w,u,g,s=left
            v,z,f,h=right
            if (u[-1],w[-1])!=(z[-1],v[-1]) or s==h:
                continue
            mask=[{x,y} for x,y in zip(u,z)]
            for prefix in range(1,t):
                if u[prefix-1]==z[prefix-1] or w[prefix-1]!=v[prefix-1]:
                    continue
                candidates+=1
                admitted=[(ww,gg) for ww,xx,gg,_ in words if ww[-1]==w[-1] and
                          ww[prefix-1]==w[prefix-1] and all(x in m for x,m in zip(xx,mask))]
                if len(admitted)==2:
                    isolated+=1
                    gaps.add(abs(g-f))
                upper=[max(xx[j] for ww,xx,gg,_ in words if ww[-1]==w[-1]
                           and ww[prefix-1]==w[prefix-1] and all(a in b for a,b in zip(xx,mask)))
                       for j in range(t)]
                maxgain=max(gg for _,gg in admitted)
                require(sum(gg==maxgain for _,gg in admitted)==1 and
                        sum(x//2 for x in [0]+upper[:-1])==maxgain,"unique upper history")
        orders=sorted({m for gap in gaps for m in range(3,gap+1) if gap%m==0})
        require(0 not in gaps,"two isolated routes cannot cancel unwrapped")
        summary.append(dict(t=t,opposite_sign_pair_markers=candidates,isolated=isolated,
                            unwrapped_absolute_gaps=sorted(gaps),eligible_orders=orders))
    require(all(not r["eligible_orders"] for r in summary[:-1])
            and summary[-1]["eligible_orders"]==[3,5,6],"smallest masked two-word dark")
    return summary


def dark_run(order,which_site_read):
    """Enumerate positive and negative flags separately; earlier failures stop."""
    masks=[{1,-1},{2,-2},{3,-1},{2,0},{1},{0}]
    active=[("",0,0,"R",1,None)]
    leaves=[]
    surviving=[]
    for t,mask in enumerate(masks,1):
        branches=defaultdict(Counter)
        counts=Counter()
        new=[]
        for word,x,y,rail,s,tag in active:
            for c in "RL":
                dest=x+(1 if c=="R" else -1)
                gain=(y+x//2)%order
                sign=s*(-1 if c==rail=="L" else 1)
                accepted=dest in mask and (t!=3 or c=="R")
                tag_out=dest if accepted and t==which_site_read else tag
                if accepted and t<6:
                    new.append((word+c,dest,gain,c,sign,tag_out))
                else:
                    status="terminal_pass" if accepted else "first_miss"
                    branches[status,dest,c][gain,tag_out]+=sign
                    counts[status,dest,c]+=1
                    if accepted:
                        surviving.append([word+c,dest,gain,c,sign])
        for (status,x,c),coeffs in sorted(branches.items()):
            prob=Fraction(sum(a*a for a in coeffs.values()),2**t)
            count=Fraction(counts[status,x,c],2**t)
            leaves.append([t,status,x,c,str(prob),str(count)])
        active=new
    require(sum(Fraction(v[-2]) for v in leaves)==1 and
            sum(Fraction(v[-1]) for v in leaves)==1,"dark complete normalization")
    click=sum(Fraction(v[-2]) for v in leaves if v[1]=="terminal_pass")
    count_click=sum(Fraction(v[-1]) for v in leaves if v[1]=="terminal_pass")
    require(count_click==Fraction(1,32) and len(surviving)==2,"two surviving words")
    return dict(M=order,which_site_read=which_site_read,click=str(click),count_click=str(count_click),
                paths=surviving,all_first_miss_and_final_bins=leaves)


def masked_witness():
    runs=[]
    for order in (3,4,5,6,7,13):
        for which in (None,1,2,3,4,5):
            row=dark_run(order,which)
            mark=which in (1,2,3,4)
            expected=Fraction(0 if 6%order==0 and not mark else 1,32)
            require(Fraction(row["click"])==expected,"earlier/later/site-copy control")
            runs.append(row)
    # Fixed (unselected) realness scale of the detector is 1-Re(gamma).
    # A zero-click one-sided bound is -expm1(log(alpha)/N), stable at large N.
    limits=[]
    for n in (100,1000,10000):
        upper=-expm1(log(.05)/n)
        limits.append(dict(fresh_independent_validations=n,zero_click_95_upper=upper,
                           unit_square_leakage_upper=min(2.,32*upper)))
    return dict(mask_sites=[[1,-1],[2,-2],[3,-1],[2,0],[1],[0]],
                read_rail_R_at=3,leaves_columns=["tick","status","site","rail","square","count"],
                pair_minimality=mask_search(),runs=runs,zero_click_examples=limits)


def run():
    findings=census()
    selected=witnesses()
    # Exact M=3 check for the nonzero character pair: its polynomial is reduced
    # in Q[z]/(z²+z+1), with norm of (a+bz) = a²-ab+b².
    def m3norm(sequence):
        g=Counter()
        for j,s in sequence:
            g[j%3]+=s
        a,b=g[0]-g[2],g[1]-g[2]
        return a*a-a*b+b*b
    bytag=defaultdict(list)
    for w,tag,g,s in selected[0]["words_gain_sign"]:
        bytag[tag].append((g,s))
    combined=[p for a in bytag.values() for p in a]
    other=[m3norm(combined),sum(m3norm(a) for a in bytag.values())]
    zero=[sum(s for g,s in combined)**2,sum(sum(s for g,s in a)**2 for a in bytag.values())]
    require(zero==[9,5] and other==[3,2],"unit/zero character controls")
    # Collapsed real site markers interpolate between the broad and hidden
    # columns, while a persistent counted component is unaffected by the tag.
    eight=paths(8)
    two_ports=[]
    for m in (*range(3,29),None):
        data=instrument(eight,m,2)
        a,b=data["L",-2,"R"],data["L",0,"L"]
        if m is None or m>=10:
            require((a,b)==([17,13,15],[17,21,15]),"two-port separation")
        two_ports.append([m,a,b])
    inversions=[]
    for c in (Fraction(0),Fraction(1,3),Fraction(1)):
        for coherence in (Fraction(-1),Fraction(0),Fraction(2,5),Fraction(1)):
            a=15*c+(1-c)*(13+4*coherence)
            b=15*c+(1-c)*(21-4*coherence)
            inferred_c=(34-a-b)/4
            require(inferred_c==c,"sum calibration")
            inferred=None if c==1 else 1+(a-b)/(8*(1-c))
            require(inferred is None or inferred==coherence,"coherence inversion")
            inversions.append([str(c),str(coherence),str(a/256),str(b/256),
                               str(inferred_c),None if inferred is None else str(inferred)])
    # At seven ticks in the unwrapped limit, ALL broad port scores agree with
    # count on this flag, even though broad-vs-copied remains visible.
    require(all(b==c for rail,x,r,b,n,c in endpoint_table(None,7) if rail=="L"),
            "seven-tick nuisance degeneracy")
    return dict(scope="One sharp localized (0,R,sheet 0) source, staircase signed Hadamard. "
                      "One intermediate rail read; sheet stays unresolved at all times. "
                      "Complete terminal site/rail. Unoccupied ports are zero.",
                census=findings, witnesses=selected, masked_dark=masked_witness(),
                all_ports_columns=["intermediate_rail","terminal_x","terminal_rail",
                                   "broad","hidden_site_copy","classical_count"],
                two_port_order_census=two_ports,
                two_port_events=["L at tick 2 then (-2,R)", "L at tick 2 then (0,L)"],
                inversion_columns=["count","real_overlap","joint_A","joint_B",
                                   "inferred_count","inferred_overlap_or_null"],
                inversions=inversions,
                M3_pure_sector_numerators=dict(constant=zero,nonzero=other),
                M3_partial_marker={"fixed_pointer_convention":"localized square, real overlap projection",
                                   "joint_formula":"(3+2*Re(gamma))/32",
                                   "conditional_formula":"(3+2*Re(gamma))/16",
                                   "phase_flipped_gamma_minus_one":"1/32",
                                   "imaginary_overlap":"3/32"})


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory",type=Path)
    out=parser.parse_args().directory
    data=run()
    out.mkdir(parents=True,exist_ok=True)
    with (out/"direction_record_witness.json").open("x",encoding="utf8",newline="\n") as handle:
        json.dump(data,handle,separators=(",",":"),allow_nan=False)
        handle.write("\n")
