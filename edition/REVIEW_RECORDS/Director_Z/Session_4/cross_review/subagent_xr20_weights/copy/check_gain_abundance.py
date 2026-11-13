"""Equal-length labelled path coverage and multiplicity on finite regular digraphs.

Run python -B check_gain_abundance.py results. Edges are distinct choices.
Integer counts count histories before complex amplitudes are summed.
"""

from argparse import ArgumentParser
from collections import deque
from itertools import combinations
from math import gcd
from pathlib import Path
import json


def ring_edges(n, q, mode, gains):
    """Vertices 2*x and 2*x+1 are (x,R) and (x,L), respectively."""
    def potential(x, c):
        return x*x + 2*(c == -1)*x + (c == -1)

    edges = []
    for x in range(n):
        for i, c in enumerate((1, -1)):
            for j, out in enumerate((1, -1)):
                y = (x + out) % n
                minus = int(c == out == -1)
                if mode == "odd_sheet":
                    gain = 2*gains[x] + (q//2)*minus
                elif mode == "signed":
                    gain = minus
                elif mode == "iH":
                    gain = 1+2*minus
                elif mode == "switch":
                    gain = potential(y, out)-potential(x, c)
                else:
                    raise ValueError(mode)
                edges.append((2*x+i, 2*y+j, gain % q))
    return edges


def bezout(a, b):
    """Return a nonnegative gcd and Bezout coefficients, including signed b."""
    if b == 0:
        return abs(a), (-1 if a < 0 else 1), 0
    divisor, x, y = bezout(b, a % b)
    return divisor, y, x-(a//b)*y


def path_lattice(vertices, edges, q, start):
    # Choose directed paths from start and prove strong connectivity by a second,
    # reversed walk. No lifted residue states enter this calculation.
    forward = [[] for _ in range(vertices)]
    back = [[] for _ in range(vertices)]
    for u, v, z in edges:
        forward[u].append((v, z))
        back[v].append(u)
    paths = {start:(0, 0)}
    queue = deque([start])
    while queue:
        u = queue.popleft()
        length, weight = paths[u]
        for v, z in forward[u]:
            if v not in paths:
                paths[v] = (length+1, weight+z)
                queue.append(v)
    seen = {start}
    queue = deque([start])
    while queue:
        for v in back[queue.popleft()]:
            if v not in seen:
                seen.add(v)
                queue.append(v)
    if len(paths) != vertices or len(seen) != vertices:
        raise ValueError("The lattice comparison assumes a strongly connected base.")
    residual = [(paths[u][0]+1-paths[v][0], paths[u][1]+z-paths[v][1])
                for u,v,z in edges] + [(0,q)]
    # Residuals telescope around every directed closed walk. Conversely, a
    # residual is the difference of two based closed walks obtained by appending
    # the same directed return from v to the chosen paths.
    determinant = gcd(*(x*b-y*a for (x,y),(a,b) in combinations(residual,2)))
    period = slope = 0
    for length, weight in residual:
        period, left, right = bezout(period, length)
        slope = left*slope+right*weight
    assert period > 0 and determinant > 0 and determinant % period == 0
    index = determinant//period
    assert q % index == 0
    assert all(x % period == 0 and (y-(x//period)*slope) % index == 0 for x,y in residual)
    return dict(base_period=period, determinant_gcd=determinant, equal_length_gain_index=index,
                equal_length_gain_subgroup=list(range(0,q,index)), gain_per_period_mod_index=slope%index,
                root_paths=[paths[v] for v in range(vertices)], residual_generators=sorted(set(residual)))


def predicted_mask(lattice, q, v, time):
    length, weight = lattice["root_paths"][v]
    period = lattice["base_period"]
    if (time-length) % period:
        return 0
    index = lattice["equal_length_gain_index"]
    residue = (weight+((time-length)//period)*lattice["gain_per_period_mod_index"]) % index
    return sum(1 << z for z in range(residue,q,index))


def support_step(current, edges, q):
    following = [0]*len(current)
    mask = (1 << q)-1
    for u,v,gain in edges:
        word = current[u]
        rotated = ((word << gain) | (word >> (q-gain))) & mask
        following[v] |= rotated
    return tuple(following)


def support_cycle(vertices, edges, q, targets, lattice, start):
    full = (1 << q)-1
    current = tuple(int(v == start) for v in range(vertices))
    seen = {}
    hist = []
    while current not in seen:
        seen[current] = len(hist)
        hist.append(current)
        current = support_step(current, edges, q)
    begin = seen[current]
    cycle_length = len(hist)-begin
    # Check every cell and lifted phase, including accessible times with partial
    # support. Verify the lattice prediction repeats on the observed period.
    matches = all(mask == predicted_mask(lattice,q,v,t) == predicted_mask(lattice,q,v,t+cycle_length)
                  for t in range(begin,len(hist)) for v,mask in enumerate(hist[t]))
    first = next((t for t,row in enumerate(hist) if all(row[v]==full for v in targets)),None)
    return dict(first_full_time=first, eventual_start=begin, eventual_period=cycle_length,
                target_masks_by_time=[[row[v] for v in targets] for row in hist],
                all_eventual_vertex_masks_match_lattice=matches), hist


def exact_counts(vertices, edges, q, targets, start, hist, boolean):
    # Independent recurrence on flattened (vertex,residue) cells, with separate
    # parallel edges contributing separate histories. Capping at two preserves
    # reachability of all thresholds 0, 1, 2, so a repeated capped state certifies
    # a negative common-time result without a chosen time cutoff.
    degree = len(edges)//vertices
    lifted = [(q*u+z,q*v+(z+gain)%q) for u,v,gain in edges for z in range(q)]
    current = [0]*(vertices*q)
    current[start*q] = 1
    first = loop = loop_count = witness = amplified = None
    capped_seen = {}
    first_repeat = None
    t = 0
    total_ok = agreement = True
    start_cycle = boolean["eventual_start"]
    length = boolean["eventual_period"]
    while True:
        capped = tuple(min(v,2) for v in current)
        if capped in capped_seen and first_repeat is None:
            first_repeat = (capped_seen[capped],t-capped_seen[capped])
        capped_seen.setdefault(capped,t)
        total_ok &= sum(current) == degree**t
        bitrow = hist[t if t < len(hist) else start_cycle+(t-start_cycle)%length]
        for v in range(vertices):
            agreement &= bitrow[v] == sum(1 << z for z in range(q) if current[q*v+z])
        target_counts = [current[q*v:q*(v+1)] for v in targets]
        if first is None and min(min(row) for row in target_counts) >= 2:
            first, witness = t, target_counts
        if t and loop is None and current[start*q] >= 2:
            loop, loop_count = t, current[start*q]
        if first is not None and loop is not None and t == first+loop:
            amplified = target_counts
        if first_repeat is not None and (first is None or loop is None or amplified is not None):
            break
        following = [0]*len(current)
        for u,v in lifted:
            following[v] += current[u]
        current = following
        t += 1
    domination = (None if amplified is None else
                  all(b >= loop_count*a for row,more in zip(witness,amplified) for a,b in zip(row,more)))
    return dict(first_common_time_at_least_two=first, witness_target_counts=witness,
                witness_minimum=(min(map(min,witness)) if witness else None),
                zero_gain_closed_loop_time=loop, distinct_zero_gain_closed_loops=loop_count,
                one_prefixed_loop_time=first+loop if amplified is not None else None,
                prefixed_loop_lower_bound_holds=domination, amplified_target_counts=amplified,
                cap_two_cycle_start=first_repeat[0], cap_two_cycle_period=first_repeat[1],
                final_exact_time=t, final_target_counts=target_counts, total_histories=degree**t,
                all_exact_supports_match_boolean=agreement, total_count_exact=total_ok)


def path_gain_index_only(vertices, q, edges):
    # Forget the time coordinate. This intentionally weaker test cannot
    # distinguish a genuine fixed-time gain from a phase supplied by the clock.
    seen = {(0,0)}
    queue = deque(seen)
    by_vertex = [[] for _ in range(vertices)]
    for u,v,z in edges:
        by_vertex[u].append((v,z))
    while queue:
        u,z = queue.popleft()
        for v,dz in by_vertex[u]:
            dest = (v,(z+dz)%q)
            if dest not in seen:
                seen.add(dest)
                queue.append(dest)
    return sorted(z for u,z in seen if u==0)


def component_period(adjacency, root=0):
    """Measure the period by directed BFS on the literal positive-edge graph."""
    def distances(graph):
        level = {root:0}
        queue = deque([root])
        while queue:
            u = queue.popleft()
            for v in graph[u]:
                if v not in level:
                    level[v] = level[u]+1
                    queue.append(v)
        return level

    reverse = [[] for _ in adjacency]
    for u,out in enumerate(adjacency):
        for v in out:
            reverse[v].append(u)
    level = distances(adjacency)
    reachable = set(level)
    component = reachable & set(distances(reverse))
    period = gcd(*(level[u]+1-level[v] for u in component for v in adjacency[u] if v in component))
    assert period > 0
    classes = [level[v]%period if v in component else None for v in range(len(adjacency))]
    return dict(reachable_vertices=len(reachable), strongly_connected_vertices=len(component),
                reachable_is_one_SCC=(component==reachable), all_vertices_in_root_SCC=(len(component)==len(adjacency)),
                period=period, cyclic_classes=classes)


def cyclic_lift_period(vertices, q, edges, lattice, returns):
    base = [[] for _ in range(vertices)]
    lifted = [[] for _ in range(vertices*q)]
    for u,v,dz in edges:
        base[u].append(v)
        for z in range(q):
            lifted[q*u+z].append(q*v+(z+dz)%q)
    base_check = component_period(base)
    lift_check = component_period(lifted)
    h = lattice["equal_length_gain_subgroup"]
    assert set(h) <= set(returns) and len(returns)%len(h)==0
    ratio = len(returns)//len(h)
    fiber = lift_check["cyclic_classes"][:q]
    return dict(base_period_BFS=base_check["period"],reachable_lift=lift_check,
                period_ratio_Q_over_H=ratio,predicted_lift_period=lattice["base_period"]*ratio,
                root_fiber_in_identity_class=[z for z,c in enumerate(fiber) if c==0],
                computed_identity_class_equals_H=([z for z,c in enumerate(fiber) if c==0]==h),
                predicted_period_matches=lift_check["period"]==lattice["base_period"]*ratio)


def cyclotomic_polynomial(q):
    """Return ascending integer coefficients for the minimal polynomial of zeta_q."""
    polynomials = {}
    for n in range(1,q+1):
        if q % n:
            continue
        numerator = [-1]+[0]*(n-1)+[1]
        for d,divisor in polynomials.items():
            if n % d:
                continue
            quotient = [0]*(len(numerator)-len(divisor)+1)
            for j in reversed(range(len(quotient))):
                quotient[j] = numerator[j+len(divisor)-1]
                for k,coefficient in enumerate(divisor):
                    numerator[j+k] -= quotient[j]*coefficient
            assert not any(numerator)
            numerator = quotient
        polynomials[n] = numerator
    return polynomials[q]


def column_geometry(vertices, edges, q, degree):
    # A polynomial in the primitive root is zero iff its remainder modulo
    # the monic cyclotomic polynomial is zero. This includes repeated edges.
    by_column = [[] for _ in range(vertices)]
    for u,v,z in edges:
        by_column[u].append((v,z))
    modulus = cyclotomic_polynomial(q)
    checks = []
    for u in range(vertices):
        for w in range(u,vertices):
            differences = [(y-z)%q for v,z in by_column[u] for s,y in by_column[w] if v==s]
            desired = degree if u==w else 0
            remaining = [0]*q
            remaining[0] = -desired
            for z in differences:
                remaining[z] += 1
            for j in reversed(range(q-len(modulus)+1)):
                factor = remaining[j+len(modulus)-1]
                for k,coefficient in enumerate(modulus):
                    remaining[j+k] -= factor*coefficient
            if any(remaining):
                checks.append(dict(columns=[u,w],difference_exponents=differences,desired=desired,
                                   exact_remainder=remaining[:len(modulus)-1]))
    return dict(scaled_isometry=not checks,failed_column_pairs=len(checks),
                first_failed_inner_product=checks[0] if checks else None,
                cyclotomic_coefficients=modulus,
                method="Exact Gram before division by sqrt(degree), reduced modulo the cyclotomic "
                       "polynomial in ascending powers. The first failure retains its exponents and remainder.")


def trial(name, vertices, q, edges, targets, abundance, metadata):
    start = 0
    degrees = [sum(u==v for u,_,_ in edges) for v in range(vertices)]
    indegrees = [sum(w==v for _,w,_ in edges) for v in range(vertices)]
    assert len(set(degrees+indegrees))==1
    lattice = path_lattice(vertices,edges,q,start)
    timing = len({lattice["root_paths"][v][0]%lattice["base_period"] for v in targets}) == 1
    forecast = timing and lattice["equal_length_gain_index"]==1
    support, hist = support_cycle(vertices,edges,q,targets,lattice,start)
    counts = exact_counts(vertices,edges,q,targets,start,hist,support)
    unrestricted = path_gain_index_only(vertices,q,edges)
    formula = None
    if metadata.get("label_rule") == "odd_sheet":
        m = q//2
        gain = metadata["site_gains"]
        differences = [gain[(x+1)%len(gain)]-gain[x-1] for x in range(len(gain))]
        divisor = gcd(m,*differences)
        formula = dict(M=m,nearest_site_differences=differences,gcd_with_M=divisor,
                       predicted_subgroup_order=2*m//divisor,
                       computed_subgroup_order=q//lattice["equal_length_gain_index"])
    return dict(name=name, vertices=vertices, degree=degrees[0], q=q, start=start, targets=targets,
                graph=metadata, edge_gain_residues=sorted({z for _,_,z in edges}), lattice=lattice,
                target_times_compatible=timing, algebra_predicts_all_residues=forecast,
                expected_abundance=abundance, boolean=support, integer_counts=counts,
                unrestricted_closed_walk_gain_residues=unrestricted, native_sheet_formula=formula,
                reachable_period_check=cyclic_lift_period(vertices,q,edges,lattice,unrestricted),
                column_geometry=column_geometry(vertices,edges,q,degrees[0]))


def z15_nonfaithful():
    # Use two independent bits. Packing a label as 2a+b is only a vertex index:
    # group addition is bitwise XOR, never addition modulo four.
    arcs = [(0,0,(0,1)),(0,1,(0,1)),(1,0,(0,1)),(1,1,(1,0))]
    lifted = [[] for _ in range(8)]
    projected_edges = []
    for u,v,(a,b) in arcs:
        projected_edges.append((u,v,a))
        for z in range(4):
            lifted[4*u+z].append(4*v+(z^(2*a+b)))
    group = component_period(lifted)
    projected = trial("nonfaithful_character_projection",2,2,projected_edges,[0,1],True,
                      dict(edges=projected_edges,label_rule="chi(a,b)=(-1)^a"))
    counts = [1]+[0]*7
    character_counts = [1,0,0,0]
    time = 0
    history = []
    while True:
        by_character = [[sum(counts[4*v+2*a:4*v+2*a+2]) for a in range(2)] for v in range(2)]
        assert character_counts == by_character[0]+by_character[1]
        bits = [[z for z in range(4) if counts[4*v+z]] for v in range(2)]
        assert all((z//2+z%2-time)%2==0 for row in bits for z in row)
        history.append(dict(time=time,group_indices_at_each_vertex=bits,counts_by_character=by_character))
        if min(min(row) for row in by_character)>=1000:
            break
        following = [0]*8
        for u,targets in enumerate(lifted):
            for v in targets:
                following[v] += counts[u]
        counts = following
        following_character = [0]*4
        for u,v,gain in projected_edges:
            for z in range(2):
                following_character[2*v+(z^gain)] += character_counts[2*u+z]
        character_counts = following_character
        time += 1
    kernel = [divmod(z,2) for z,c in enumerate(group["cyclic_classes"][:4]) if c==0]
    return dict(source="Z15 challenger_4/follow.py, F2", base_vertices=2, group="Z2 x Z2",
                index_convention="2*a+b with componentwise addition modulo two", edges=arcs,
                full_group_lift=group, full_group_same_time_subgroup=kernel,
                full_group_same_time_all_four=False,
                full_group_obstruction="Every arc changes a+b modulo two by one; a+b equals time modulo two.",
                projected_character_trial=projected, common_time_1000=time, group_counts_at_threshold=counts,
                exact_character_counts_by_time=history, pushforward_matches_projected_DP_at_every_tick=True,
                agrees_with_Z15_F2=(
                    group["all_vertices_in_root_SCC"] and group["period"]==2 and kernel==[(0,0),(1,1)] and
                    projected["column_geometry"]["scaled_isometry"] and
                    projected["reachable_period_check"]["reachable_lift"]["period"]==1 and
                    projected["reachable_period_check"]["base_period_BFS"]==1 and
                    min(min(row) for row in by_character)>=1000))


def run():
    rows = []
    def add(name,n,q,kind,gain,targets,wanted):
        edges = ring_edges(n,q,kind,gain)
        rows.append(trial(name,2*n,q,edges,targets,wanted,dict(N=n,label_rule=kind,site_gains=gain)))
    bump = [1]+[0]*7
    pair = [0,1]
    for m in (3,5,9,15):
        add(f"one_site_M{m}",8,2*m,"odd_sheet",bump,pair,True)
        add(f"constant_M{m}",8,2*m,"odd_sheet",[1]*8,pair,False)
    for m in (9,15):
        add(f"proper_subgroup_M{m}",8,2*m,"odd_sheet",[3]+[0]*7,pair,False)
    add("ordinary_signed",8,2,"signed",[],pair,True)
    add("clock_twisted_iH",8,4,"iH",[],pair,False)
    add("pure_switch_all_five_labels",8,5,"switch",[],pair,False)
    add("parity_incompatible_targets",8,6,"odd_sheet",bump,[0,2],False)
    add("odd_ring",7,6,"odd_sheet",[1]+[0]*6,pair,True)
    add("nonconstant_alternating_clock",8,10,"odd_sheet",[x%2 for x in range(8)],pair,False)
    add("all_labels_ramp_M3",8,6,"odd_sheet",list(range(8)),pair,True)
    rows.append(trial("parallel_ternary_loops",1,5,[(0,0,z) for z in (0,1,2)],[0],True,
                      dict(edges=[[0,0,z] for z in (0,1,2)])))
    rows.append(trial("degree_one_single_history",1,1,[(0,0,0)],[0],False,dict(edges=[[0,0,0]])))
    for q in (4,8):
        edges = []
        for layer in range(2):
            for c in range(2):
                for d in range(2):
                    z = layer+2*c*d if q==4 else layer+2*c+4*c*d
                    edges.append((2*layer+c,2*(1-layer)+d,z%q))
        rows.append(trial(f"unitary_alternating_layers_q{q}",4,q,edges,[0,1],False,
                          dict(edges=edges,vertex="2*layer+coin; coin 0=R, 1=L",
                               label_rule="layer+2*c*d" if q==4 else "layer+2*c+4*c*d")))
    z_edges = [(0,2,0),(0,3,1),(1,0,1),(1,1,3),(2,0,0),(2,1,0),(3,2,0),(3,3,3)]
    rows.append(trial("Z15_G10_four_vertex_counterexample",4,4,z_edges,[0,3],False,
                      dict(edges=z_edges,source="Edition Z15, G10, When the gains are abundant",
                           common_successors=[2,3])))
    z15 = rows[-1]
    nonfaithful = z15_nonfaithful()
    indexed = {r["name"]:r for r in rows}
    switching = indexed["pure_switch_all_five_labels"]
    pair_vs_single = {name:dict(same_site_start_and_target=True,
                                zero_length_difference_gain_subgroup=indexed[name]["lattice"]["equal_length_gain_subgroup"],
                                arbitrary_length_closed_gain_subgroup=indexed[name]["unrestricted_closed_walk_gain_residues"])
                      for name in ("pure_switch_all_five_labels","unitary_alternating_layers_q4",
                                   "unitary_alternating_layers_q8","clock_twisted_iH")}
    alternating = [indexed[f"unitary_alternating_layers_q{q}"] for q in (4,8)]
    checks = dict(
        algebra_and_boolean_coverage=all(r["algebra_predicts_all_residues"] ==
                                        (r["boolean"]["first_full_time"] is not None) for r in rows),
        all_lifted_eventual_cells=all(r["boolean"]["all_eventual_vertex_masks_match_lattice"] for r in rows),
        boolean_and_integer_support=all(r["integer_counts"]["all_exact_supports_match_boolean"] for r in rows),
        sums_and_branch_multiplicity=all(r["integer_counts"]["total_count_exact"] and
            ((r["integer_counts"]["first_common_time_at_least_two"] is not None)==r["expected_abundance"])
            for r in rows),
        growing_common_time_witnesses=all(r["integer_counts"]["prefixed_loop_lower_bound_holds"] is True
                                         for r in rows if r["expected_abundance"]),
        pure_switch_all_labels_is_nonunitary=len(switching["edge_gain_residues"])==5 and
            switching["lattice"]["equal_length_gain_index"]==5 and not switching["column_geometry"]["scaled_isometry"],
        unitary_layers_distinguish_cross_time_gains=all(
            r["column_geometry"]["scaled_isometry"] and len(r["unrestricted_closed_walk_gain_residues"])==r["q"]
            and r["lattice"]["equal_length_gain_subgroup"]==list(range(0,r["q"],2))
            and r["boolean"]["first_full_time"] is None for r in alternating),
        all_native_sheet_order_formulas=all(r["native_sheet_formula"]["computed_subgroup_order"]==
            r["native_sheet_formula"]["predicted_subgroup_order"] for r in rows if r["native_sheet_formula"]),
        all_native_ring_coins_are_scaled_isometries=all(r["column_geometry"]["scaled_isometry"]
            for r in rows if r["graph"].get("label_rule") in ("odd_sheet","iH","signed")),
        periods_from_reachable_lift=all(
            r["reachable_period_check"]["predicted_period_matches"] and
            r["reachable_period_check"]["computed_identity_class_equals_H"] and
            r["reachable_period_check"]["reachable_lift"]["reachable_is_one_SCC"] and
            r["reachable_period_check"]["base_period_BFS"]==r["lattice"]["base_period"] and
            r["reachable_period_check"]["reachable_lift"]["strongly_connected_vertices"]==
            r["vertices"]*len(r["unrestricted_closed_walk_gain_residues"])
            for r in rows),
        Z15_four_vertex_period_obstruction=(
            z15["reachable_period_check"]["base_period_BFS"]==1 and
            z15["reachable_period_check"]["reachable_lift"]["period"]==2 and
            z15["reachable_period_check"]["reachable_lift"]["all_vertices_in_root_SCC"] and
            z15["column_geometry"]["scaled_isometry"] and z15["lattice"]["equal_length_gain_subgroup"]==[0,2]),
        Z15_nonfaithful_projection=nonfaithful["agrees_with_Z15_F2"])
    return dict(checks=checks,trials=rows,same_length_vs_unrestricted=pair_vs_single,
        nonfaithful_group_control=nonfaithful,
        period_comparison="Based return words have length multiples of p and gains in Q. Sending a return "
                          "gain to its length mod p-prime defines a surjection Q onto the multiples of p "
                          "mod p-prime: close walks of the same gain with a common return from that "
                          "lifted endpoint. Lengths of base returns generate pZ. The kernel is H, the "
                          "zero-length gain subgroup: a difference with length a multiple of p-prime "
                          "can have that length cancelled by an integer combination of zero-gain return "
                          "words, whose lengths generate p-prime Z. Hence p-prime=p*[Q:H]. Each cyclic "
                          "trial measures p-prime directly in the reachable positive-edge SCC.",
        conventions="The finite regular base is strongly connected. Each edge is a distinguishable history "
                    "choice. The ring starts at (0,R); vertex 2x means (x,R), 2x+1 means (x,L). "
                    "The two directions at site zero are the common read, except the explicit incompatible "
                    "parity control. A Boolean target mask stores residue z in bit z.",
        algebra="Root path attributes are (length, additive gain). An edge yields the difference between "
                "the chosen route to its endpoint and the route through the edge (through minus chosen). "
                "Adjoin (0,q). The gcd h of residual lengths is the base period. The gcd D of absolute "
                "two-row determinants is the lattice index in Z^2. The zero-length gain subgroup has "
                "index D/h. A Bezout combination with length h fixes its drift per h ticks.",
        multiplicity="Both endpoint coins must realize every one of the q labels at the same time. "
                     "For positive rows the integer witness gives each count explicitly. Prefixing j "
                     "independently chosen same-length zero-gain closed walks multiplies every witness "
                     "count by at least the displayed loop multiplicity to the power j. These counts "
                     "precede any interference, record or probability assignment.")


if __name__=="__main__":
    parser = ArgumentParser()
    parser.add_argument("output",type=Path)
    output = parser.parse_args().output
    result = run()
    output.mkdir(parents=True,exist_ok=True)
    (output/"gain_abundance.json").write_text(json.dumps(result,indent=2)+"\n",encoding="utf8")
    print(len(result["trials"]),"trials",result["checks"])
    if not all(result["checks"].values()):
        raise SystemExit(1)
