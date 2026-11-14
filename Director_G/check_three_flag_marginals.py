"""Exact three-flag tables, threshold bounds and site masks of two signed walks."""

from argparse import ArgumentParser
from fractions import Fraction as Q
from itertools import permutations, product
import json
from pathlib import Path


WORDS = tuple(product((0,1),repeat=3))


def require(ok, message):
    if not ok:
        raise ValueError(message)


def offline_site_controls():
    source = Path(__file__).parent / "results" / "cesium_spatial_weight.json"
    record = json.loads(source.read_text(encoding="utf-8"))
    arms = [
        ("retain_negative", [-2, -1, 0, 1], -1, Q(149, 603)),
        ("retain_positive", [-1, 0, 1, 2], 1, Q(5, 49)),
    ]
    results = {}
    for name, occupied, peak, expected in arms:
        counts = dict(zip(record["sites"], record["detected_counts"][name], strict=True))
        retained = sum(counts[x] for x in occupied)
        light = [Q(counts[x], retained) for x in occupied if x != peak]
        heavy = Q(counts[peak], retained)
        residuals = []
        for u, v, w in permutations(light):
            g1, g2, g3 = u, u+v, u+v+w
            residuals.append((2*g1-g2, 2*g2-g1-g3, 2*g3-g1-heavy))
        averaged = [sum(row)/6 for row in zip(*residuals)]
        require(averaged == [0, 0, expected] and expected == (5-8*heavy)/3,
                "permutation-averaged offline residuals")
        results[name] = dict(heavy=counts[peak], retained=retained,
                             displaced=sum(counts.values())-retained, averaged=averaged)
    return results


def margins(c):
    return tuple(sum(v for w,v in zip(WORDS,c) if all(w[i] for i in idx))
                 for idx in [(0,),(1,),(2,),(0,1),(0,2),(1,2)])


def cells(d, m, h):
    a,b,c,ab,ac,bc = m
    return (d-a-b-c+ab+ac+bc-h, c-ac-bc+h, b-ab-bc+h, bc-h,
            a-ab-ac+h, ac-h, ab-h, h)


def endpoints(d,m):
    a,b,c,ab,ac,bc = m
    return max(0,ab+ac-a,ab+bc-b,ac+bc-c), min(ab,ac,bc,d-a-b-c+ab+ac+bc)


def tails(w):
    return tuple(sum(v for word,v in zip(WORDS,w) if sum(word)>=j) for j in (1,2,3))


def weights(d,k):
    if k == 1:
        yield (d,)
    else:
        for x in range(d+1):
            for rest in weights(d-x,k-1):
                yield (x,)+rest


def rank_cap(x):
    """Extremize a monotone complementary read on a finite mass grid."""
    signed = [2*s-1 for s in x]
    cuts = {abs(v) for v in signed if v} | {1}
    return Q(1,2)+Q(max(sum((v>=c)-(v<=-c) for v in signed) for c in cuts), 2*len(x))


def grid(d):
    groups = {}
    for w in weights(d,8):
        groups.setdefault(margins(w),[]).append(w)
    total = 0
    for m, tables in groups.items():
        lo,hi = endpoints(d,m)
        require(sorted(tables)==sorted(cells(d,m,h) for h in range(lo,hi+1)), "entire margin fiber")
        scores = [sum(tails(w)[1:]) for w in tables]
        require((min(scores),max(scores))==(sum(m[3:])-hi,sum(m[3:])-lo), "sharp extrema")
        for w in tables:
            s = tails(w)
            require(s[1]+s[2] <= m[3]+m[2], "one-pair bound")
            cap = rank_cap([Q(v,d) for v in s])
            require((cap <= Q(2,3)) == (s[1]+s[2] <= d), "complementary cap versus all monotone thresholds")
        total += len(tables)
    return dict(tables=total, distinct_margins=len(groups))


def walk(ticks,sites):
    state = [[0,0] for _ in range(sites)]
    state[0][0]=1
    for _ in range(ticks):
        new = [[0,0] for _ in range(sites)]
        for i,(r,l) in enumerate(state):
            new[(i+1)%sites][0] += r+l
            new[(i-1)%sites][1] += r-l
        state = new
    masses = [Q(r*r+l*l,2**ticks) for r,l in state]
    require(sum(masses)==1, "walk norm")
    return state, masses


def product_table(p):
    a,b,c = p
    return tuple((a if u else 1-a)*(b if v else 1-b)*(c if s else 1-c) for u,v,s in WORDS)


def main():
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("output_file",type=Path)
    output=cli.parse_args().output_file
    grid_checks={d:grid(d) for d in range(1,9)}
    p=Q(5,8)
    m=(40,40,40,25,25,25)
    lo,hi=endpoints(64,m)
    adverse, favorable=cells(64,m,lo),cells(64,m,hi)
    require((lo,hi)==(10,19) and tails(adverse)==(55,55,10), "pairwise iid counterexample")
    require(adverse==(9,0,0,15,0,15,15,10) and favorable==(0,9,9,6,9,6,6,19),
            "both endpoint tables in physical bit order")
    # At these margins 000 bounds h more strictly than any pair.
    require(all(v>=0 for v in adverse+favorable), "positive extremizers")
    require(rank_cap([Q(v,64) for v in tails(adverse)])==Q(5,6), "explicit adversarial complementary read")
    # A continuous monotone symmetric ramp can be linear between these knots.
    knot={0:Q(0),9:Q(0),10:Q(1,2),54:Q(1,2),55:Q(1),64:Q(1)}
    require(all(knot[z]+knot[64-z]==1 for z in knot) and sum(knot[v] for v in tails(adverse))/3==Q(5,6),
            "witness values on the triple")
    sites,masses=walk(3,8)
    require(sites[1]==[2,1] and [masses[i] for i in [1,3,5,7]]==[p,Q(1,8),Q(1,8),Q(1,8)], "three-tick named sites")
    A,B,C={1,3},{1,5},{3,5,7}
    probs=tuple(sum(masses[x] for x in event) for event in (A,B,C))
    require(probs==(Q(3,4),Q(3,4),Q(3,8)) and sum(probs)/3==p, "three local masks")
    iid=product_table(probs)
    require(margins(iid)[3]==Q(9,16) and margins(iid)[3]+probs[2]==Q(15,16), "independent upper pair")
    require(1-probs[2]-probs[0]*probs[1]==Q(1,16), "allowed excess covariance")
    # Same physical walker, protected position retained, three reversible predicates.
    joint=[Q(0)]*8
    for i,w in enumerate(masses):
        word=(int(i in A),int(i in B),int(i in C))
        joint[WORDS.index(word)] += w
    require(tails(joint)==(1,Q(7,8),0) and margins(joint)[3]==p, "single-walk marginal masks")
    def sq(s):
        return s*s/(s*s+(1-s)**2)
    require(sum(sq(x) for x in tails(joint))/3==Q(33,50), "one-bank three-setting square score")
    # Whole-site masks realize eight masses. Use J=0...8 in units of 1/8
    # and the three reachable comparisons 0-1-2, 1-2-3 and 1-3-5.
    attained=sorted({sum((w for w,selected in zip(masses,mask) if selected),Q(0))
                     for mask in product((0,1), repeat=8)})
    require(attained==[Q(j,8) for j in (0,1,2,3,5,6,7,8)], "whole-site subset sums")
    midpoints=[(0,1,2),(1,2,3),(1,3,5)]
    require(all(Q(j,8) in attained for row in midpoints for j in row)
            and all(i+k==2*j for i,j,k in midpoints), "three reachable fair mixtures")
    midpoint_residuals=[2*sq(Q(j,8))-sq(Q(i,8))-sq(Q(k,8)) for i,j,k in midpoints]
    require(all(v != 0 for v in midpoint_residuals), "square fails each native midpoint")
    # Three slots conditionally product given a common sharp or 4/5 type.
    bad=tuple(Q(7,32)*x+Q(25,32)*y for x,y in
              zip(product_table((Q(0),)*3),product_table((Q(4,5),)*3)))
    require(margins(bad)[:3]==(p,)*3 and margins(bad)[3:]!=(p*p,)*3, "hidden-type mixture")
    # One common continuous symmetric read, applied within the responding type.
    def ramp(s):
        return min(Q(1),max(Q(0),50*(s-Q(49,100))))
    high=tails(product_table((Q(4,5),)*3))
    mixed_read=Q(25,32)*sum(ramp(s) for s in high)/3
    require(mixed_read==Q(25,32) > Q(2,3), "common read, conditional product types")
    # Gain asymmetry and selective unresolved reporting can invalidate an
    # incident-run bound inferred only from reported flags.
    square=p*p/(p*p+(1-p)**2)
    require(square==Q(25,34) and square-Q(2,3)==Q(7,102), "base squared gap")
    stuck_first=(Q(1)+1-Q(1))/2
    require(stuck_first==Q(1,2), "one-port detector versus decoded fair routing")
    require(Q(2,3)/(Q(2,3)+Q(1,2)*Q(1,3))==Q(4,5), "half the negatives suppressed")
    five,m5=walk(5,12)
    small=sum(m5[i%12] for i in [-5,3,5])
    require(small==Q(19,32) and small*small+small<=1 and small*small>2*(1-small)**2,
            "five-tick one-pair window and square separation")
    data=dict(word_order=[''.join(map(str,w)) for w in WORDS],integer_grids=grid_checks,
              pairwise_five_eighths=dict(denominator=64,moments=m,triple_range=[lo,hi],
                                        max_tablescore=adverse,min_tablescore=favorable,max_tails=tails(adverse),
                                        complementary_rates_at_units_over_64=knot,adverse_mean="5/6"),
              three_tick_ports=sites,masks=[sorted(s) for s in (A,B,C)],masses=probs,
              separate_product_table=iid,positive_covariance_allowance="1/16",
              same_walker_table=joint,same_walker_tails=tails(joint),same_walker_squared_reference="33/50",
              whole_site_masses=attained,fair_midpoints_eighth_units=midpoints,
              base_square_midpoint_residuals=midpoint_residuals,
              base_square=square,square_gap_to_cap="7/102",hidden_type_mixture=bad,
              hidden_type_threshold_rate=mixed_read,one_stuck_port=dict(unrouted=1,decoded=stuck_first),
              kept_rate_after_half_negative_erasure="4/5",
              five_tick_ports=five,five_tick_mask=[-5,3,5],five_tick_mass=small,
              offline_cesium_arms=offline_site_controls())
    with output.open("x",encoding="utf-8",newline="\n") as f:
        json.dump(data,f,indent=2,default=str)
        f.write("\n")


if __name__=="__main__":
    main()
