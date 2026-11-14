"""Exact shifted masks for the sharp right-rail Hadamard launch on the line."""

from argparse import ArgumentParser
from bisect import bisect_left, bisect_right
from collections import Counter
from fractions import Fraction
from itertools import accumulate, product
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def walk_profiles(clocks):
    """Integer site weights in order -t,-t+2,...,t. Keep exact zeroes."""
    state = [(1, 0)]
    for tick in range(max(clocks) + 1):
        if tick in clocks:
            weights = [r*r + l*l for r, l in state]
            require(sum(weights) == 2**tick, "unit norm at the attained clock")
            yield tick, weights
        if tick < max(clocks):
            right = [0] + [r+l for r, l in state]
            left = [r-l for r, l in state] + [0]
            state = list(zip(right, left))


def positive_starts(weights):
    return [start for start, n in zip(accumulate(weights, initial=0), weights) if n]


def selected(start, origin, width, size):
    return (start-origin) % size < width


def cumulative_labels(coordinates, weights, *, mirror=False):
    """The mass strictly before a site (or before its radius), at every integer."""
    boundary = list(accumulate(weights,initial=0))
    def label(x):
        coord = abs(x) if mirror else x
        return boundary[bisect_left(coordinates,coord)] % boundary[-1]
    return label


def point_site_selected(label, x, origin, width, size):
    """The same switch for physical site routing and for a completed site read."""
    return selected(label(x),origin,width,size)


def singleton_records(tick, label, size, seeds):
    stride = size//seeds
    width = 5*size//8
    half = tick//2
    wrong_parity = 1-tick%2
    probes = sorted({-tick-2,-tick-1,-tick,-half,-wrong_parity,0,wrong_parity,
                     half,tick,tick+1,tick+2})
    counts = {}
    assigned = {}
    for x in probes:
        # The same switch handles an input localized at x and a completed
        # site read reporting x, even when the reference walk never reached it.
        hits = [u for u in range(seeds)
                if point_site_selected(label,x,u*stride,width,size)]
        assigned[x] = str(label(x))
        if abs(x) > tick:
            require(label(x) == 0, "exterior sentinel at zero")
        require(len(hits)==5*seeds//8, "singleton incidence on complete well labels")
        counts[x] = len(hits)
    return dict(origin_count=seeds,site_start_or_bin=assigned,site_hit_counts=counts)


def masks_by_mass(weights, width):
    """Map selected population to number of integer origins, via changes of membership."""
    size = sum(weights)
    require(0 <= width <= size, "mask width outside circle")
    if width in (0, size):
        return Counter({width: size})
    changes = Counter()
    initial = 0
    for start, n in zip(accumulate(weights, initial=0), weights):
        if selected(start, 0, width, size):
            initial += n
        changes[(start-width+1) % size] += n
        changes[(start+1) % size] -= n
    limits = sorted({0, size, *changes})
    hist = Counter()
    mass = initial
    for start, end in zip(limits, limits[1:]):
        if start:
            mass += changes[start]
        hist[mass] += end-start
    require(sum(hist.values()) == size, "lost seed")
    require(sum(m*c for m, c in hist.items()) == width*size, "wrong mass mean")
    require(max(abs(m-width) for m in hist) <= max(weights)-1, "integer overshoot bound")
    return hist


def mass_at_seed(starts, origin, width, size):
    """Direct successor-distance computation; coordinates may cross the circle seam."""
    lifted = starts + [a+size for a in starts] + [2*size]
    return lifted[bisect_left(lifted, origin+width)] - lifted[bisect_left(lifted, origin)]


def sharp_brackets(weights, target):
    """Largest width with all S<=target; smallest width with all S>=target."""
    size = sum(weights)
    require(0 < target < size, "interior target")
    starts = positive_starts(weights)
    lifted = starts + [a+size for a in starts] + [2*size]
    lower, upper = size, 0
    for i, start in enumerate(starts):
        prev = starts[i-1] if i else starts[-1]-size
        first_above = bisect_right(lifted, start+target)-1
        first_at_least = bisect_left(lifted, start+target)-1
        lower = min(lower, lifted[first_above]-start)
        upper = max(upper, lifted[first_at_least]-prev)
    require(max(masks_by_mass(weights,lower)) <= target < max(masks_by_mass(weights,lower+1)),
            "lower endpoint sharpness")
    require(min(masks_by_mass(weights,upper-1)) < target <= min(masks_by_mass(weights,upper)),
            "upper endpoint sharpness")
    return lower, upper


def exact_fraction(num, den):
    return str(Fraction(num, den))


def small_checks():
    trials = 0
    for t, weights in walk_profiles(set(range(7))):
        size = 1 << t
        occupied = positive_starts(weights)
        sites = list(range(-t,t+1,2))
        starts_by_site = cumulative_labels(sites,weights)
        probes = sites + [-t-2,-t-1,t+1,t+2,1-t%2]
        for k in range(size+1):
            direct = Counter()
            rates = [0 for _ in probes]
            for r in range(size):
                mask = [point_site_selected(starts_by_site,x,r,k,size) for x in probes]
                mass = sum(n for n, b in zip(weights,mask) if b)
                require(mass == mass_at_seed(occupied,r,k,size), "half-open endpoint")
                direct[mass] += 1
                rates = [v + b for v, b in zip(rates,mask)]
            require(direct == masks_by_mass(weights,k), "breakpoint count differs from complete enumeration")
            require(all(v == k for v in rates), "offline marginal for arbitrary complete site distribution")
            trials += size
        for a in range(1,size):
            sharp_brackets(weights,a)
    return trials


def iid_tick_three_escape(weights):
    size = sum(weights)
    nonzero = [n for n in weights if n]
    require(sorted(nonzero) == [1,1,1,5] and size == 8, "wrong dated source")
    scores = {0:0,1:1,2:2,3:3,5:9,6:10,7:11,8:12}
    sums, counts = Counter(), Counter()
    for mask in product((0,1), repeat=4):
        j = sum(mask)
        counts[j] += 1
        sums[j] += scores[sum(w*b for w,b in zip(nonzero,mask))]
    means = [Fraction(sums[j],12*counts[j]) for j in range(5)]
    require(means == [Fraction(j,4) for j in range(5)], "conditional iid-mask transfer")
    require(scores[5] == 9 and all(scores[j]+scores[8-j]==12 for j in scores), "complement")
    return dict(score_numerators_over_12=scores, conditional_rates=list(map(str,means)),
                heavy_rate="3/4", ordinary_heavy="5/8")


def profile_escape():
    # Equally spaced labels with occupied weights concentrated on a block.
    # A uniformly shifted semicircle has the right one-site marginals.
    # At origins 0 and D/2 the two resulting masses are respectively 1 and 0.
    rows = []
    for occupied in (4,8,16):
        size = occupied**2
        weights = [occupied]*occupied + [0]*(size-occupied)
        k = 3*size//4
        values = [sum(n for a,n in enumerate(weights[:occupied]) if selected(a,r,k,size))
                  for r in range(size)]
        partial = sum(0 < v < size for v in values)
        require(min(values)==0 and max(values)==size and sum(values)==size*k, "profile escape")
        require(partial == 2*(occupied-1), "number of seeds cutting the packet")
        require(masks_by_mass(weights,k) == {k:size}, "calibrated mass-label control")
        # An endpoint-sharp physical read that is zero at every interior
        # mass can nevertheless approach the offline rate of three quarters.
        endpoint_only = Fraction(values.count(size),size)
        require(endpoint_only == Fraction(k-occupied+1,size), "missed interior response")
        rows.append(dict(sites=size,occupied_block=occupied,max_weight=exact_fraction(1,occupied),
                         spatial_partial_origins=partial,spatial_endpoint_only_read=str(endpoint_only),
                         incorrectly_placed_mass_range=["0","1"],matched_mass_range=["3/4","3/4"]))
    return rows


def hidden_mix():
    # Rapidly changing, independent response types retain their deviations even
    # under a perfectly calibrated averaged monotone response at all masses.
    evidence = {}
    for j in range(9):
        s = Fraction(j,8)
        offset = s*(1-s)*(2*s-1)/2
        pair = s-offset,s+offset
        require(sum(pair)/2 == s, "hidden-curve average")
        evidence[str(s)] = [str(v) for v in pair]
    require(evidence["5/8"] == ["305/512","335/512"], "hidden type true deviations")
    return evidence


def panel(tick, weights):
    size = 1 << tick
    peak = max(weights)
    if size < 8:
        raise ValueError("target 5/8 requires three or more ticks")
    nominal = size*5//8
    lo, hi = sharp_brackets(weights,nominal)
    hist = masks_by_mass(weights,nominal)
    row = dict(tick=tick,denominator=str(size),maximum_site_numerator=str(peak),
               all_site_numerators_in_order_minus_t_to_t=list(map(str,weights)),
               maximum_weight_decimal=peak/size, nominal_mass="5/8",
               actual_numerators_at_nominal=[str(min(hist)),str(max(hist))],
               sharp_bracket_widths=[str(lo),str(hi)],sharp_bracket_decimals=[lo/size,hi/size],
               worst_general_mass_error=exact_fraction(peak-1,size),
               assigned_origins=str(sum(hist.values())))
    if tick == 512:
        practical = 1024
        stride = size//practical
        starts = positive_starts(weights)
        nominal_reads = [mass_at_seed(starts,r*stride,nominal,size) for r in range(practical)]
        sparse_lower, sparse_upper = lo//stride, (hi+stride-1)//stride
        require(max(mass_at_seed(starts,r*stride,sparse_lower*stride,size) for r in range(practical)) <= nominal,
                "1024-seed lower bracket")
        require(min(mass_at_seed(starts,r*stride,sparse_upper*stride,size) for r in range(practical)) >= nominal,
                "1024-seed upper bracket")
        for k in [0,sparse_lower,640,sparse_upper,1024]:
            # This eligibility window in origin coordinates is the closed integer
            # interval [a-k*stride+1,a], modulo size. Count stride multiples.
            for a in starts+[size//3,size+3]:
                require(a//stride - (a-k*stride)//stride == k, "sparse grid marginal")
        prefix_values = list(accumulate(weights))
        near = min(range(len(weights)),key=lambda i:abs(prefix_values[i]-nominal))
        edge = 2*near-tick
        prefix = prefix_values[near]
        require(edge==310 and abs(prefix/size-.6270233076106853)<1e-15, "actual prefix")
        G = lambda m: Fraction(m*m,m*m+(size-m)**2)
        # Rounding each rate down to twelve decimal places brackets the exact
        # weighted mean without creating a common denominator of thousands of factors.
        precision=10**12
        floored = sum(c*int(G(m)*precision) for m,c in hist.items())
        lower = Fraction(floored, size*precision)
        upper = lower+Fraction(1,precision)
        sampled = sum(int(G(m)*precision) for m in nominal_reads)
        sampled_lower = Fraction(sampled,practical*precision)
        require(lower > Fraction(7348,10000) and sampled_lower>Fraction(7348,10000), "power-rule gap")
        actual_lo, actual_hi = sharp_brackets(weights,prefix)
        sites = range(-tick,tick+1,2)
        label = cumulative_labels(sites,weights)
        row["singleton_extension"] = singleton_records(tick,label,size,practical)
        require(all(sum(w for x,w in zip(sites,weights)
                        if point_site_selected(label,x,u*stride,nominal,size)) == n
                    for u,n in enumerate(nominal_reads)), "site rule reproduces every nominal mass")
        row["ten_bit_seed"] = dict(origins=practical,nominal_width=640,
            nominal_mass_min_max=[str(min(nominal_reads)),str(max(nominal_reads))],
            safe_lower_upper_widths=[sparse_lower,sparse_upper],
            square_mean_lower_upper_decimal=[float(sampled_lower),float(sampled_lower)+1/precision])
        prefix_widths = [actual_lo//stride, (actual_hi+stride-1)//stride]
        require(max(mass_at_seed(starts,r*stride,prefix_widths[0]*stride,size)
                    for r in range(practical)) <= prefix <=
                min(mass_at_seed(starts,r*stride,prefix_widths[1]*stride,size)
                    for r in range(practical)), "1024-seed physical prefix bracket")
        row["prefix_nearest_to_5_8"] = dict(right_endpoint=edge,numerator=str(prefix),
            ten_bit_safe_widths=prefix_widths,
            sharp_bracket_widths=[str(actual_lo),str(actual_hi)],mass_decimal=prefix/size,
            sharp_bracket_decimals=[actual_lo/size,actual_hi/size])
        row["all_origins_square_mean"] = dict(lower_upper_decimal=[float(lower),float(upper)],
            floor_sum=str(floored),ceiling_sum=str(floored+size),denominator=str(size*precision))
    return row


def shell_weights(tick, weights):
    """Increasing radii of the occupied parity; both mirror sites share a start."""
    by_radius = Counter()
    for i, n in enumerate(weights):
        by_radius[abs(2*i-tick)] += n
    return [by_radius[r] for r in sorted(by_radius)]


def direct_word_shells(tick, right, left):
    """Independent direct signs on rail words for an unnormalized integer launch."""
    amplitudes = Counter()
    for word in product((0,1),repeat=tick):
        x = tick-2*sum(word)
        for incident, amp in enumerate((right,left)):
            signs = sum(a*b for a,b in zip((incident,)+word,word))
            amplitudes[x,word[-1]] += (-1)**signs * amp
    totals = Counter()
    for (x,_), amp in amplitudes.items():
        totals[abs(x)] += amp*amp
    return [totals[r] for r in sorted(totals)]


def mirrored_panel(tick, weights):
    size = 2**tick
    shell = shell_weights(tick,weights)
    if tick <= 8:
        for launch in [(1,0),(0,1),(1,1),(1,-1)]:
            sqnorm = sum(a*a for a in launch)
            require(direct_word_shells(tick,*launch) == [a*sqnorm for a in shell],
                    "R, L and both diagonal input states agree on every mirror shell")
    grid = min(1024,size)
    stride = size//grid
    width = 5*size//8
    radii = list(range(tick%2,tick+1,2))
    label = cumulative_labels(radii,shell,mirror=True)
    by_mass = Counter()
    inclusion = Counter()
    for u in range(grid):
        origin = u*stride
        accepted = [i for i,r in enumerate(radii) if point_site_selected(label,r,origin,width,size)]
        inclusion.update(accepted)
        by_mass[sum(shell[i] for i in accepted)] += 1
    require(all(inclusion[i]==5*grid//8 for i in range(len(shell))), "offline marginals of both mirror sites")
    require(sum(n*count for n,count in by_mass.items())==grid*width, "common mean target")
    require(max(abs(n-width) for n in by_mass)<=max(shell)-1, "shell discrepancy")
    precision=10**12
    floor_total = sum(count*(precision*n*n//(n*n+(size-n)**2)) for n,count in by_mass.items())
    den = grid*precision
    if tick==512:
        require(Fraction(floor_total,den)>Fraction(73,100), "ten-bit mirror-square separation")
    return dict(tick=tick,denominator=str(size),shell_order="increasing radius",
                singleton_extension=singleton_records(tick,label,size,grid),
                occupied_parity_shells=len(shell),origin_count=grid,distinct_mass_count=len(by_mass),
                each_site_inclusion_count=5*grid//8,shell_weight_max_numerator=str(max(shell)),
                shell_weight_max_decimal=max(shell)/size,
                mass_min_max_numerators=list(map(str,(min(by_mass),max(by_mass)))),
                mass_min_max_decimals=[min(by_mass)/size,max(by_mass)/size],
                square_rate_numerator_bounds=[floor_total,floor_total+grid],square_rate_denominator=den,
                square_rate_decimal_bounds=[floor_total/den,(floor_total+grid)/den],
                all_masses_with_origin_counts=[[str(n),count] for n,count in sorted(by_mass.items())])


def balanced_shell_panel(tick, weights):
    """Load the largest shell first, choosing the first least-loaded bin."""
    size = 2**tick
    by_radius = list(zip(range(tick%2,tick+1,2),shell_weights(tick,weights)))
    bins = [0]*8
    radii = [[] for _ in bins]
    for r,n in sorted(by_radius,key=lambda item:(-item[1],item[0])):
        dest = min(range(8),key=bins.__getitem__)
        bins[dest] += n
        radii[dest].append(r)
    require(sum(bins)==size, "balanced bins retain the whole carrier")
    radius_bin = {r:b for b,group in enumerate(radii) for r in group}
    def label(x):
        return radius_bin.get(abs(x),0)
    off_grid = [-tick-2,-tick-1,-1,1,tick+1,tick+2]
    require(all(label(x)==0 for x in off_grid), "untabulated coordinates use bin zero")
    masses = []
    for origin in range(8):
        actual = sum(n for r,n in by_radius if point_site_selected(label,r,origin,5,8))
        require(actual == sum(bins[(origin+j)%8] for j in range(5)), "site/bin agreement")
        masses.append(actual)
    require(sum(masses)==5*size, "mean three-bit scalar mass")
    for dest in range(8):
        require(sum((dest-origin)%8 < 5 for origin in range(8))==5,
                "every site label is seen at five origins")
    require(Fraction(min(masses),size)>Fraction(6205,10000) and
            Fraction(max(masses),size)<Fraction(6281,10000), "tight three-bit interval")
    precision = 10**15
    floors = sum(precision*n*n//(n*n+(size-n)**2) for n in masses)
    den = 8*precision
    return dict(tick=tick,denominator=str(size),origin_count=8,inclusion_count=5,
                singleton_extension=singleton_records(tick,label,8,8),
                bin_numerators=list(map(str,bins)),bin_radii=radii,
                seed_mass_numerators=list(map(str,masses)),
                seed_mass_decimals=[n/size for n in masses],
                square_rate_numerator_bounds=[floors,floors+8],square_rate_denominator=den,
                square_rate_decimal_bounds=[floors/den,(floors+8)/den])


def main():
    parser=ArgumentParser(description=__doc__)
    parser.add_argument("output",type=Path)
    output=parser.parse_args().output
    clocks={3,8,16,32,64,128,512}
    rows=[]
    mirrors=[]
    escape=None
    for t,weights in walk_profiles(clocks | {256}):
        if t == 256:
            balanced = balanced_shell_panel(t,weights)
            continue
        rows.append(panel(t,weights))
        if t in (3,8,512):
            mirrors.append(mirrored_panel(t,weights))
        if t==3:
            escape=iid_tick_three_escape(weights)
    # Interior zero-weight sites at a nonzero cumulative boundary keep their
    # original starts, even when several consecutive entries repeat it.
    example = cumulative_labels((-4,-2,0,2,4),(3,0,0,2,3))
    require(example(-2)==example(0)==example(2)==example(-1)==3, "repeated boundary through gap")
    require(example(3)==5 and example(-9)==example(9)==0, "strictly smaller cumulative mass")
    explicit = [u for u in range(8) if point_site_selected(example,-2,u,5,8)]
    omitted = [u for u in range(8) if point_site_selected(example,-1,u,5,8)]
    require(explicit==omitted==[0,1,2,3,7], "tabulated dark site and intervening gap")
    repeated=dict(tabulated_dark_site=-2,untabulated_gap=-1,
                  tabulated_hit_seeds=explicit,untabulated_hit_seeds=omitted)
    result=dict(repeated_boundary_control=repeated,small_integer_origin_cases=small_checks(),clock_panels=rows,
                finite_iid_monotone_escape=escape,geometric_coordinate_escape=profile_escape(),
                independent_hidden_curve_mixture=hidden_mix(),mirrored_shell_masks=mirrors,
                three_bit_mirrored_shell_bins=balanced)
    with output.open("x",encoding="utf-8",newline="\n") as stream:
        json.dump(result,stream,indent=2,allow_nan=False)
        stream.write("\n")


if __name__=="__main__":
    main()
