"""Run python -B check_collision_scattering.py OUTPUT_DIRECTORY. Standard library.

Infinite line in half-cell units. Real amplitudes have an arbitrary common input
normalization. All squared masses below are exact and include both particles.
"""
import argparse
import json
from collections import defaultdict
from fractions import Fraction as F
from itertools import product
from pathlib import Path


T, R = F(3,5), F(4,5)


def clean(d):
    return {k:v for k,v in d.items() if v}


def norm(v):
    return sum(x*x for x in v.values())


def scatter(v, tag=False, inverse=False):
    out = defaultdict(F)
    for (a,b,u,w,z),amp in v.items():
        if a!=b or u==w:
            out[a,b,u,w,z] += amp
        else:
            # RL column (3,4)/5; LR column (-4,3)/5.
            out[a,b,u,w,z] += T*amp
            out[a,b,-u,-w,z^int(tag)] += R*u*(-1 if inverse else 1)*amp
    return clean(out)


def stream(v, sign=1):
    return {(a+sign*u,b+sign*w,u,w,z):amp for (a,b,u,w,z),amp in v.items()}


def flip(v):
    return {(a,b,-u,-w,z):amp for (a,b,u,w,z),amp in v.items()}


def reverse_frame(v,tag):
    # Stored states are incoming immediately before scattering. F reverses
    # both arrows and local C^{-1} shifts the reversal back to that convention.
    return scatter(flip(v),tag,True)


def encounter_formula(raw,ticks,tag):
    """Separate geometric evaluator, summing amplitudes at shared outgoing events."""
    out = defaultdict(F)
    for (a,b,u,w,z),amp in raw.items():
        meet = F(b-a,u-w) if u!=w else None
        if meet is None or meet.denominator!=1 or not 0<=meet<ticks:
            out[a+u*ticks,b+w*ticks,u,w,z] += amp
            continue
        h = int(meet)
        x = a+u*h
        out[x+u*(ticks-h),x+w*(ticks-h),u,w,z] += T*amp
        out[x+w*(ticks-h),x+u*(ticks-h),w,u,z^int(tag)] += u*R*amp
    return clean(out)


def snapshot(v,init_norm):
    # Every occupied coherent coordinate, with two integers for each signed amp.
    # Zero is implicit elsewhere on the unbounded line.
    return [[*k,F(amp).numerator,F(amp).denominator,str(amp*amp/init_norm)]
            for k,amp in sorted(v.items())]


def evolve(raw,depth,tag=False):
    E = norm(raw)
    cur = raw.copy()
    timeline = []
    for t in range(depth+1):
        assert norm(cur)==E and cur==encounter_formula(raw,t,tag)
        # For full unitary and time reversal use correlated superpositions as well.
        nxt = stream(scatter(cur,tag))
        undo = scatter(stream(nxt,-1),tag,True)
        assert undo==cur and reverse_frame(reverse_frame(cur,tag),tag)==cur
        assert reverse_frame(stream(scatter(reverse_frame(nxt,tag),tag)),tag)==cur
        assert all(any(abs(a-x)<=t and abs(b-y)<=t for x,y,_,_,_ in raw)
                   for a,b,_,_,_ in cur)
        timeline.append(snapshot(cur,E))
        cur = nxt
    return timeline,encounter_formula(raw,depth,tag)


def marginal(v, key):
    masses = defaultdict(F)
    E = norm(v)
    for coords,amp in v.items():
        masses[key(*coords)] += F(amp*amp,E)
    return dict(masses)


def display_bins(bins):
    return [[*k,str(v)] for k,v in sorted(bins.items())]


def swap_labels(v):
    return {(b,a,w,u,z):amp for (a,b,u,w,z),amp in v.items()}


def arrival_source(sign):
    return {(-h,h,1,-1,0):v for h,v in ((2,1),(4,sign))}


def pair_analyzer(state,flight,at_party):
    """One local balanced H for the two possible exit positions of each ray.

    Equal-depth H numerator on the occupied rail subspace. The four location
    pairs (two per party) can be measured after transporting the two bins to
    one detector at each party; the routing time is outside the flight.
    """
    out = defaultdict(F)
    for (a,b,u,w,z),amp in state.items():
        location,arrow = (a,u) if at_party==0 else (b,w)
        p0,p1 = arrow*(flight-2),arrow*(flight-4)
        assert location in (p0,p1)
        key = (a,b,u,w,z)
        for dst in (p0,p1):
            target = list(key)
            target[at_party] = dst
            out[tuple(target)] += -amp if dst==p1 and location==p1 else amp
    assert norm(out)==2*norm(state)
    return clean(out)


def erase(v):
    out = defaultdict(F)
    for (a,b,u,w,z),amp in v.items():
        for n in (0,1):
            out[a,b,u,w,n] += (-1)**(z*n)*amp
    assert norm(out)==2*norm(v)
    return clean(out)


def single(sites,u=1,w=-1):
    return {(*sites,u,w,0):1}


def simulate_cases():
    left = (-4,4,1,-1,0)
    right = (4,-4,-1,1,0)
    runs = [
        ('one_from_left',{left:1},8,False),('one_from_right',{right:1},8,False),
        ('coincident_incoming_plus',{left:1,right:1},8,False),
        ('coincident_incoming_minus',{left:1,right:-1},8,False),
        ('selected_column_cancels_transmission',{left:4,right:3},8,False),
        ('selected_column_cancels_reflection',{left:3,right:-4},8,False),
        ('plus_with_reflection_tag',{left:1,right:1},8,True),
        ('minus_with_reflection_tag',{left:1,right:-1},8,True),
        ('unequal_arrival_plus',arrival_source(1),7,False),
        ('unequal_arrival_minus',arrival_source(-1),7,False),
        ('independent_broad_packets',{(a,b,1,-1,0):x*y for (a,x),(b,y)
                                     in product(((-4,1),(-2,-2)),((2,3),(4,1)))},7,False),
        ('equal_directions_same_site',single((0,0),1,1),6,True),
        ('already_separating',single((-2,2),-1,1),6,False),
        ('coincidence_at_launch',single((0,0)),4,False),
        ('coarse_adjacent_missed',single((0,1)),3,False),
        ('coarse_adjacent_refined',single((0,2)),6,False),
        ('integer_coarse_sites_to_even_fine_mesh',single((-2,4)),6,False),
        ('distant_source_near_option',single((0,12)),9,False),
        ('distant_source_far_option',single((0,18)),9,False),
    ]
    trajectories = []
    final = {}
    for label,init,ticks,tag in runs:
        rows,final[label] = evolve(init,ticks,tag)
        trajectories.append(dict(case=label,depth=ticks,reflection_marker=tag,
                                 initial_squared_norm=str(norm(init)),all_microstep_ports=rows))
    return trajectories,final


def tests(final):
    rail = lambda a,b,u,w,z:(u,)
    ray_bin = lambda a,b,u,w,z:tuple(sorted(((a,u),(b,w))))
    expected = {'one_from_left':T*T,'one_from_right':R*R,'coincident_incoming_plus':F(1,50),
                'coincident_incoming_minus':F(49,50),'selected_column_cancels_transmission':0,
                'selected_column_cancels_reflection':1,'plus_with_reflection_tag':F(1,2),
                'minus_with_reflection_tag':F(1,2),'coarse_adjacent_missed':1,
                'coarse_adjacent_refined':T*T,'already_separating':0,
                'equal_directions_same_site':1,'integer_coarse_sites_to_even_fine_mesh':T*T}
    for name,q in expected.items():
        assert marginal(final[name],rail).get((1,),0)==q
    # Sorting the two direction-labelled physical positions discards the path assignment.
    for label in list(expected)[:8]:
        assert marginal(final[label],ray_bin)=={((-4,-1),(4,1)):1}
    tag_records = []
    for launch in ('plus','minus'):
        v = erase(final[launch+'_with_reflection_tag'])
        table = marginal(v,lambda a,b,u,w,z:(z,u))
        same = expected['coincident_incoming_'+launch]
        assert table[(0,1)]==same/2 and table[(1,1)]==(1-same)/2
        tag_records.append(dict(launch=launch,tag_H_and_A_direction_joint=display_bins(table)))
    raw_equal = marginal(final['unequal_arrival_plus'],lambda *k:k)
    assert raw_equal==marginal(final['unequal_arrival_minus'],lambda *k:k)
    local_rows = []
    for sign,name in ((1,'plus'),(-1,'minus')):
        v = final['unequal_arrival_'+name]
        v = pair_analyzer(pair_analyzer(v,7,0),7,1)
        measurements = marginal(v,lambda a,b,u,w,z:(u, int(abs(a)==3), int(abs(b)==3)))
        equality = sum(p for (_,ra,rb),p in measurements.items() if ra==rb)
        assert equality==int(sign>0)
        local_rows.append(dict(input_sign=sign,ports=display_bins(measurements),
                               equals_mass=str(equality)))
    near,far = single((0,12)),single((0,18))
    site_rail = lambda a,b,u,w,z:(a,u)
    distances = []
    for t in range(10):
        a = marginal(encounter_formula(near,t,False),site_rail)
        b = marginal(encounter_formula(far,t,False),site_rail)
        tv = sum(abs(a.get(i,0)-b.get(i,0)) for i in set(a)|set(b))/2
        assert tv==(0 if t<7 else R*R)
        distances.append(dict(microstep=t,A_near=display_bins(a),A_far=display_bins(b),TV=str(tv)))
    rho = single((0,0))
    exchange_commutes = swap_labels(scatter(rho))==scatter(swap_labels(rho))
    naive_reverse = flip(stream(scatter(flip(stream(scatter(rho))))))==rho
    assert not exchange_commutes and not naive_reverse
    return dict(A_right_port={k:str(v) for k,v in expected.items()},
                sorted_outgoing_position_direction_multiset=[[-4,-1],[4,1]],
                reflected_marker_interference=tag_records,
                different_arrivals_raw_sharp_bins_equal=True,held_local_arrival_analyzer=local_rows,
                causal_controls=distances,bare_arrow_flip_is_one_tick_reversal=False,
                labelled_coin_commutes_with_particle_exchange=False)


def main(directory):
    rows,final = simulate_cases()
    data = dict(
        geometry='Infinite 1D line. One microstep translates a particle by half of the coarse spatial scale during half of the coarse tick: speed c. Initial coarse sites sit at even fine coordinates. Stored states are arriving before scattering. When a+b has even parity, opposite rays directed towards each other have an integer encounter (s,x). It first changes outgoing sharp records at microstep s+1. Initial odd coordinate separation on the chosen mesh can still cross unnoticed.',
        collision='Apply C=[[3,-4],[4,3]]/5 in ordered labelled RL,LR at a coincidence, identity on equal directions or away from coincidence. Then stream. The two consistent routes to the same outgoing channel add amplitudes. Single converging RL gives transmission 9/25 and reflection 16/25; a classical per-encounter stochastic mechanism can imitate that one column. Every opposite-direction path has at most one scattering encounter in free flight. This rational collision operation is supplied as a local gate; a physical synthesis with a random completion time would require a separate clock analysis.',
        reciprocal='For the collision alone F switches RL and LR and F C F=C inverse; time-reversed amplitudes agree when both velocities are reversed. U=stream*C, so the site-local involution Theta=C inverse F obeys Theta U Theta=U inverse, including the reversible reflection-controlled marker. The bare arrow flip at the stored time slice fails. C does not commute with particle label exchange. A real exchange-symmetric two-channel orthogonal coin [[a,b],[b,a]] forces ab=0. Unordered ray detection by itself cannot infer Bose/Fermi dynamics.',
        record_encoding='Each row [xA,xB,vA,vB,tag,amp_num,amp_den,mass] gives the signed amplitude divided by sqrt(initial_squared_norm) and its exact probability. All other cells have exactly zero amplitude. Marker z flips on reflection if enabled; orthogonal tag readouts can be retained or summed. Readouts during the flight would change subsequent interference; each shown time is a separate possible terminal read.',
        scope='Elastic contact of two distinguishable equal-speed labelled walkers with a fixed freely supplied local gate, real amplitudes, coherent preparation, and squared-coordinate readout. Reflection tag models an additional carried two-state register. A recoupled time-bin test uses optional coherent local two-position analyzers after flight. This is not a long-range force, a solution of a continuum scattering problem, or experimental evidence.',
        trajectories=rows,diagnostics=tests(final))
    directory.mkdir(parents=True,exist_ok=True)
    (directory/'collision_scattering.json').write_bytes((json.dumps(data,separators=(',',':'))+'\n').encode())


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('output',type=Path)
    main(p.parse_args().output)
