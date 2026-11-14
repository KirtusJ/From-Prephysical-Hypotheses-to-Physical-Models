"""Exact controls for transferring paired binary calibration to a type-dependent mass."""
from argparse import ArgumentParser
from fractions import Fraction as Q
from itertools import combinations_with_replacement, pairwise, product
from pathlib import Path
import json


def require(condition, message):
    if not condition:
        raise ValueError(message)


def tent(x, center, radius):
    return max(Q(0), radius-abs(x-center))


def response(x, center, radius, sign):
    return x + sign*(tent(x,center,radius)-tent(x,1-center,radius))


def mean_score(x, p, q, joint):
    # Probability of each of (0,0), (1,0), (0,1), (1,1) given its two marginals.
    cells = {(0,0):1-p-q+joint, (1,0):p-joint, (0,1):q-joint, (1,1):joint}
    require(min(cells.values()) >= 0 and sum(cells.values()) == 1, "physical pair table")
    return sum(prob*(a-x)*(b-x) for (a,b),prob in cells.items())


def grid_audit():
    # Enumerate all endpoint-faithful monotone values on the 1/6 mesh,
    # inspect them at only the coarser 1/2 mesh and test the worst fine node.
    n = 6
    totals = [0,0]
    for inside in combinations_with_replacement(range(n+1),n-1):
        values = (0,*inside,n)
        d = max(abs(Q(g-i,n)) for i,g in enumerate(values))
        moment = (Q(values[3]-3,n)**2)/2
        excess = max(Q(0),d-Q(1,2))
        require(excess**3 <= 3*moment,"coarse mesh bound")
        totals[0] += 1
        if all(values[i]+values[n-i]==n for i in range(n+1)):
            require(2*excess**3 <= 3*moment,"complementary bound")
            totals[1] += 1
    return dict(fine_denominator=n,calibration_nodes=["0","1/2","1"],
                monotone_curves=totals[0],complementary_curves=totals[1])


def blind_cell():
    h,center = Q(1,8),Q(3,16)
    radius=h/2
    nodes=[i*h for i in range(9)]
    targets=[]
    for sign in (-1,1):
        require(all(response(x,center,radius,sign)==x for x in nodes),"blind grid")
        probe=center if sign==1 else 1-center
        targets.append(response(probe,center,radius,sign)-probe)
    require(targets==[radius,radius],"positive target error at both types")
    return dict(spacing=str(h),center=str(center),all_node_moments="0",
                type_target_absolute_error=str(radius))


def squared_linear_integral(a,b,length):
    return length*(a*a+a*b+b*b)/3


def center_average(x, radius):
    # Split the integration over the random center at all slope changes.
    lo,hi = Q(1,8),Q(3,8)
    split={lo,hi}
    for y in (x,1-x):
        split.update(c for c in (y-radius,y,y+radius) if lo<c<hi)
    total=Q(0)
    for a,b in pairwise(sorted(split)):
        left=response(x,a,radius,1)-x
        right=response(x,b,radius,1)-x
        total+=squared_linear_integral(left,right,b-a)
    return total/(hi-lo)


def moving_tents():
    examples=[]
    for radius in (Q(1,16),Q(1,32),Q(1,64)):
        center=Q(1,4)
        knots=sorted({Q(0),Q(1,2),Q(1),*(x+k*radius for x in (center,1-center)
                                           for k in (-1,0,1))})
        for sign in (-1,1):
            vals=[response(x,center,radius,sign) for x in knots]
            require(all(a<=b for a,b in pairwise(vals)),"monotone piecewise-linear law")
            require(all(response(1-x,center,radius,sign)==1-response(x,center,radius,sign)
                        for x in knots),"complementary curve")
        integral=sum(squared_linear_integral(response(a,center,radius,1)-a,
                                             response(b,center,radius,1)-b,b-a)
                     for a,b in pairwise(knots))
        maximum=8*radius**3/3
        require(integral==4*radius**3/3,"both reflected tents")
        require(center_average(center,radius)==maximum,"pointwise bound achieved at 1/4")
        require(all(center_average(Q(i,128),radius)<=maximum for i in range(129)),
                "rational checks beyond the support and on all interval boundaries")
        examples.append(dict(tent_height=str(radius),science_bias=str(radius),
                             integrated_mean_square=str(integral),
                             max_point_mean_square=str(maximum)))
    return examples


def paired_records():
    x,eps=Q(1,4),Q(1,16)
    high,low=x+eps,x-eps
    matched=(mean_score(x,high,high,high**2)+mean_score(x,low,low,low**2))/2
    redrawn=sum(mean_score(x,p,q,p*q) for p,q in product((low,high),repeat=2))/4
    # Conditional covariance -eps² masks the same per-type fluctuations.
    dependent=sum(mean_score(x,p,p,p*p-eps*eps) for p in (low,high))/2
    require((matched,redrawn,dependent)==(eps**2,0,0),"joint calibration contracts")
    return dict(site_mass=str(x),conditional_rates=[str(low),str(high)],
                matched_independent_score=str(matched),
                independently_redrawn_type_score=str(redrawn),
                matched_dependent_score=str(dependent),conditional_covariance=str(-eps**2))


def native_menu():
    source=Path(__file__).with_name("results")/"echo_probability_map.json"
    menu=json.loads(source.read_bytes())["finite_menu"]
    den=int(menu["mass_denominator"])
    left={Q(int(item["numerator"]),den) for item in menu["routed_left_half_masks"]}
    nodes=sorted(left | {1-x for x in left} | {Q(1,2)})
    spacing=max(b-a for a,b in pairwise(nodes))
    # Drawing a uniform y and rounding left or right with equal probabilities
    # gives each node half the sum of its incident gaps. Compare to the
    # individual left/right quadratures in the paper.
    widths=[b-a for a,b in pairwise(nodes)]
    weights=[(a+b)/2 for a,b in zip([0,*widths],[*widths,0])]
    require(sum(weights)==1 and weights==weights[::-1],"balanced quadrature")
    require(spacing<Q(21617,10**6),"reported physical mesh width")
    # For complementary curves the two directional quadratures are equal on
    # this symmetric grid. Test displacements between routed nodes as well.
    c,r=Q(1,4),Q(1,16)
    e2=[(response(x,c,r,1)-x)**2 for x in nodes]
    moment=sum(w*v for w,v in zip(weights,e2))
    require(moment==sum(w*v for w,v in zip(widths,e2[:-1])) and
            moment==sum(w*v for w,v in zip(widths,e2[1:])), "directed sums coincide")
    # Both reflected triangles live on opposite halves. Their directions
    # differ, so retaining only one of them gives constant 3 here.
    require(max(Q(0),r-spacing)**3 <= 3*moment,"symmetric irregular grid")
    return dict(source=source.name,tick=menu["ticks"],routed_node_count=len(left|{1-x for x in left}),
                additional_midpoint_anchor=True,quadrature_nodes=len(nodes),
                largest_gap=str(spacing),largest_gap_upper_decimal="0.021617",
                tent_moment=str(moment))


def main():
    parser=ArgumentParser(description=__doc__)
    parser.add_argument("output",type=Path)
    args=parser.parse_args()
    records=dict(ordered_grid=grid_audit(),unseen_cell=blind_cell(),moving_tent_family=moving_tents(),
                 pair_contracts=paired_records(),native_shell_menu=native_menu())
    with args.output.open("x",encoding="utf-8",newline="\n") as f:
        json.dump(records,f,indent=2)
        f.write("\n")


if __name__=="__main__":
    main()
