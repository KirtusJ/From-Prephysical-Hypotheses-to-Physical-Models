"""Sharp terminal-efficiency sensitivity for the six Broome position reads."""
import argparse
from fractions import Fraction as F
import json
from pathlib import Path


def size(z):
    return z[0]**2 + z[1]**2


def walks():
    # Gaussian-integer amplitudes share denominator sqrt(2^(t+1)).
    # H goes left and V right. Input polarization is (H+iV)/sqrt(2).
    amp = {(0,0):(1,0), (0,1):(0,1)}
    mass = {(0,0):F(1,2), (0,1):F(1,2)}
    tables = []
    for t in range(1,7):
        out, flow = {}, {}
        for x in range(1-t,t,2):
            u,v = [amp.get((x,k),(0,0)) for k in (0,1)]
            lo,hi = (x-1,0),(x+1,1)
            out[lo] = (u[0]+v[0],u[1]+v[1])
            out[hi] = (u[0]-v[0],u[1]-v[1])
            m = sum(mass.get((x,k),0) for k in (0,1))
            weights = [size(out[key])**2 for key in (lo,hi)]
            if sum(weights):
                flow[lo] = m*weights[0]/sum(weights)
                flow[hi] = m-flow[lo]
            else:
                assert m==0
                flow[lo]=flow[hi]=F(0)
        amp,mass = out,flow
        bins=list(range(-t,t+1,2))
        b = [F(sum(size(amp.get((x,k),(0,0))) for k in (0,1)),2**(t+1)) for x in bins]
        q = [sum(mass.get((x,k),0) for k in (0,1)) for x in bins]
        assert sum(b)==sum(q)==1 and b==b[::-1] and q==q[::-1] and min(q)>0
        tables.append((bins,b,q))
    return tables


def tv(p,q):
    return sum(abs(x-y) for x,y in zip(p,q))/2


def tilted(p,weights):
    values=[x*w for x,w in zip(p,weights)]
    return [v/sum(values) for v in values]


def fit(b,q,R):
    """Minimum TV(b, normalize(eta*q)) over 1<=eta_i<=R for one histogram."""
    assert R>=1 and len(b)==len(q) and min(q)>0
    one=F(1)
    points={one/R,one}
    for x,y in zip(b,q):
        for breakpoint in (x/y,x/(R*y)):
            if one/R < breakpoint < one:
                points.add(breakpoint)
    def clipped(a):
        return [min(max(x,a*y),a*R*y) for x,y in zip(b,q)]
    last_a=one/R
    last_sum=sum(clipped(last_a))
    for a in sorted(points):
        s=sum(clipped(a))
        if s>=1:
            root=a if s==1 else last_a+(one-last_sum)*(a-last_a)/(s-last_sum)
            h=clipped(root)
            # Any admissible histogram in [a*q,R*a*q] must absorb these deficits
            # and excesses. One decreases and the other increases as a varies.
            deficit=sum(max(F(0),x-root*R*y) for x,y in zip(b,q))
            excess=sum(max(F(0),root*y-x) for x,y in zip(b,q))
            eta=[p/(root*y) for p,y in zip(h,q)]
            assert sum(h)==1 and deficit==excess==tv(b,h)
            assert min(eta)>=1 and max(eta)<=R and tilted(q,eta)==h
            return deficit,h,eta
        last_a,last_sum=a,s
    raise AssertionError("The clipping root must lie between 1/R and 1.")


def mean(values):
    return sum(values)/len(values)


def exact_ratio(b,q):
    ratio=[x/y for x,y in zip(b,q)]
    return max(ratio)/min(ratio)


def threshold(tables,target):
    # Conservative decimal brackets. All endpoint predicates use rationals.
    digits=10**9
    low=digits
    high=2*digits
    def distance(n):
        return mean([fit(b,q,F(n,digits))[0] for _,b,q in tables])
    while distance(high)>target:
        high*=2
    while high-low>1:
        mid=(low+high)//2
        if distance(mid)>target:
            low=mid
        else:
            high=mid
    dl,du=distance(low),distance(high)
    assert dl>target>=du
    return dict(R_lower=F(low,digits),R_upper=F(high,digits),
                target_mean_TV=target,distance_at_lower=dl,distance_at_upper=du)


def common_detector(tables):
    # Symmetrizing a common detector's efficiencies at x and -x preserves the
    # normalization at every depth, and cannot worsen TV from symmetric Born.
    # Even and odd position groups may have separate ratios, but the same
    # ratio must hold at all depths of the same parity.
    certificates=[]
    for convention,left,right,depths in [
        ("signed_lattice",0,2,(2,4,6)),("signed_lattice",1,3,(3,5)),
        ("physical_path_index",1,2,(2,3,4,5,6))]:
        profiles=[]
        for t in depths:
            xs,b,q=tables[t-1]
            def grouped(vec,i):
                if convention=="physical_path_index":
                    return vec[i]
                return sum(v for x,v in zip(xs,vec) if abs(x)==i)
            profiles.append((grouped(b,left),grouped(b,right),grouped(q,left),grouped(q,right)))

        # Minimize over every positive ratio r=eta_right/eta_left, including
        # arbitrarily large ratios. On the two retained groups the conditional
        # left proportion is f=ql/(ql+r*qr). Whatever their total detected
        # mass, TV on the full vector is >= |bl-(bl+br)*f|. This follows by
        # testing the difference of detected and Born with scores 1-f,-f,0
        # on left, right and elsewhere. The score's oscillation is exactly 1.
        # Each signed term is monotone in r. Rational interval enclosures
        # give a rigorous lower bound on the global one-variable minimum.
        ratios=[F(i,1000) for i in range(2001)]+[F(i,100) for i in range(201,1601)]+[None]
        lower_bounds=[]
        for low,high in zip(ratios,ratios[1:]):
            limit=F(0)
            for bl,br,ql,qr in profiles:
                lowdiff=bl-(bl+br)*ql/(ql+low*qr)
                highdiff=bl if high is None else bl-(bl+br)*ql/(ql+high*qr)
                assert lowdiff<=highdiff
                limit+=max(F(0),lowdiff,-highdiff)
            lower_bounds.append(limit)
        at_unity=sum(abs(bl-(bl+br)*ql/(ql+qr)) for bl,br,ql,qr in profiles)
        certificates.append(dict(convention=convention,position_groups=[left,right],depths=depths,
            lower_bound_sum_over_depths=min(lower_bounds),value_of_group_bound_at_ratio_one=at_unity))
    signed_lower=sum(c["lower_bound_sum_over_depths"] for c in certificates[:2])/6
    path_lower=certificates[2]["lower_bound_sum_over_depths"]/6
    assert signed_lower>F(1,20) and path_lower>F(45,1000)
    return dict(signed_lattice_lower_bound_all_positive_contrasts=signed_lower,
        physical_path_index_lower_bound_all_positive_contrasts=path_lower,
        certificates=certificates,ratio_partition="0 to 2 by 1/1000; 2 to 16 by 1/100; [16,infinity]",
        proof="For common signed-lattice efficiencies, reflection-symmetric input position probabilities at every depth permit symmetrizing efficiencies. A separate physical-port convention fixes efficiencies at path indices j=(t+x)/2; it uses bins 1 and 2 directly, without symmetrizing. For two retained groups with fixed efficiency ratio r, f=q_l/(q_l+r*q_r) is the corrected conditional left fraction. Scores 1-f, -f and 0 on the left, right and other groups have oscillation one and corrected expectation zero. Thus TV is at least |b_l-(b_l+b_r)*f| regardless of other efficiencies. On each interval use monotonicity to bound each absolute value, sum on the indicated depths, minimize, and divide by six. Signed even and odd contributions can be added because their depths are disjoint. These lower bounds do not optimize every remaining efficiency.")


def main():
    tables=walks()
    distances=[tv(b,q) for _,b,q in tables]
    assert distances[:3]==[0]*3 and mean(distances)==F(14855,159198)
    radii=[F(31,1000),F(63,2000)]  # authors report .031, nearest-rounded upper endpoint .0315
    decisions=[]
    for radius in radii:
        decisions.append(dict(assumed_Born_mean_radius=radius,
            strict_closer_to_Born_boundary=threshold(tables,2*radius),
            exact_fit_within_radius_boundary=threshold(tables,radius)))
    variants=[]
    for R in (F(1),F(6,5),F(3,2),F(2),F(3),F(4),F(6),F(7)):
        rows=[]
        for _,b,q in tables:
            d,h,e=fit(b,q,R)
            rows.append(dict(best_TV=d,tilted_position_histogram=h,relative_efficiencies=e))
        variants.append(dict(R=R,depths=rows,mean_best_TV=mean([v["best_TV"] for v in rows])))
    # A depth-independent position-only calibration matching Born needs constant
    # relative ratios at all overlapping bin pairs. Steps 2 and 4 both see 0,+2.
    two,four=[tables[t-1] for t in (2,4)]
    ratios=[]
    for xs,b,q in (two,four):
        z,p=xs.index(0),xs.index(2)
        ratios.append((b[p]/q[p])/(b[z]/q[z]))
    assert ratios[0]==1 and ratios[1]!=1
    shared=common_detector(tables)
    return dict(source=dict(article="Broome et al., Phys. Rev. Lett. 104, 153602 (2010), Fig. 2a",
        doi="https://doi.org/10.1103/PhysRevLett.104.153602",manuscript="https://arxiv.org/pdf/1002.4923",
        observed="The six-step-depth mean total variation of detected position histograms from coherent theory is reported as 0.031. The paper normalizes counts separately at each depth. Its figure compares each of depths one to six; the reported mean is a single statistic. No raw event counts enter this checker."),
        arrays=[dict(t=t,positions=x,Born=b,local_fourth=q,TV=d,exact_match_efficiency_ratio=exact_ratio(b,q))
                for t,((x,b,q),d) in enumerate(zip(tables,distances),1)],
        propagation="Exact complex continuation of the pair-local rule. A pair carries its incoming record total into the two signed Hadamard outputs in proportion to their fourth powers of the complex moduli. Initial input is the reported circular state, the shift is H-left/V-right, and both polarizations are summed at every reported position.",
        ideal_equal_depth_mean_TV=mean(distances),ideal_quartic_residual_lower_at_rounded_bound=mean(distances)-radii[-1],
        efficiency_model="Only terminal positive multiplicative position efficiency varies. Per depth, normalize eta_i*q_i by its sum and bound max(eta)/min(eta) by R. The six independent depth adjustments give the exact lower envelope over all such response families and a lower bound for a common detector with the same maximum contrast.",
        theorem="For any fixed normalization factor a in [1/R,1], a*q_i <= h_i <= R*a*q_i. Its TV from b is at least both the bottom excess sum(a*q_i-b_i)_+ and the top deficit sum(b_i-R*a*q_i)_+. The first increases and the second decreases with a. Their crossing is attained by clipping b_i to the interval and normalizing through choice of a. The rational breakpoints b_i/q_i, b_i/(R*q_i) make the normalization piecewise linear. Empty coordinates of q remain empty; if q_i=b_i=0 the coordinate can be omitted. R=1 fixes h=q.",
        bounds="The average TV obeys the triangle inequality across six normalized histograms of equal weight. If E(R)>2r then every detected profile within r of unadjusted Born lies strictly nearer to Born than to any allowed tilted quartic profile. When E(R)<=2r, a convex midpoint of Born and an ideal fitted quartic witness shows why that ranking no longer follows from the summary alone. If E(R)<=r a tilted quartic profile itself fits in the Born ball. These are necessary information boundaries for this summary; no significance level or repeated-trial distribution is inferred.",
        depth_independent_nuisance=dict(efficiency_eta_plus2_over_eta_0_for_exact_match_at_steps_2_and_4=ratios,
            exact_all_depth_match_impossible=True,common_bin_certificate=shared,
            scope="Independent per-depth fits need not be jointly realizable by a shared detector. Contradictory pair ratios prohibit an exact common fixed-bin fit across depths even with unbounded positive efficiency. The two-group certificate separately proves a quantitative lower bound on the best possible shared positive-efficiency fit. If the six setups are adjusted independently the independent-depth envelope is exact."),
        nominal_and_rounded_boundaries=decisions,examples=variants,
        loss_and_sampling_scope="For positive entries, exact single-histogram compensation needs ratio max_i(b_i/q_i)/min_i(b_i/q_i). With finite strictly positive response, exact supports must match. A positive measured bin where the model is structurally zero cannot be generated by pure diagonal efficiencies; a zero counted bin can also be a finite-sample zero or a censored bin. Unknown fully lost bins require a separate outcome or conditioning on a declared observed set. Without a total-rate measurement the absolute efficiency scale is unidentifiable. Intermediate polarization-dependent losses can change the coherent amplitudes and the conditional physical walk, and background counts mix in a separate distribution. The table does not model either of those mechanisms.")


if __name__=="__main__":
    args=argparse.ArgumentParser(description=__doc__)
    args.add_argument("output",type=Path)
    dst=args.parse_args().output
    dst.mkdir(parents=True,exist_ok=True)
    obj=main()
    (dst/"detector_envelope.json").write_bytes((json.dumps(obj,indent=2,default=str)+"\n").encode())
    print("Nominal mean",obj["ideal_equal_depth_mean_TV"])
    for row in obj["nominal_and_rounded_boundaries"]:
        print(row["assumed_Born_mean_radius"],[float(row[k]["R_upper"]) for k in
              ("strict_closer_to_Born_boundary","exact_fit_within_radius_boundary")])
