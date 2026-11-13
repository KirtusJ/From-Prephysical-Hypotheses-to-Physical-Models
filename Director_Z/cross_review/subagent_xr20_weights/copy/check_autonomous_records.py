"""Fixed positive-clock signed graphs for a simultaneous record comparison."""

import argparse
import json
from collections import Counter, defaultdict
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path


def norm(v):
    return sum(x*x for x in v)


def parity_plan(v,t):
    a = v.copy()
    layers = []
    for _ in range(t):
        order = [i for i,x in enumerate(a) if x%2]+[i for i,x in enumerate(a) if x%2==0]
        pairs = list(zip(order[::2],order[1::2]))
        for j,k in pairs:
            assert (a[j]-a[k])%2==0
            a[j],a[k] = (a[j]+a[k])//2,(a[j]-a[k])//2
        layers.append(pairs)
    j, = [j for j,x in enumerate(a) if x]
    assert abs(a[j])==1
    return layers,j,a[j]


# A block (a,b,c,d,s,t,u,v) applies diag(u,v)*H*diag(s,t) to inputs
# a,b and writes outputs c,d. The common factor 1/sqrt(2) is implicit.
def block(a,b,c,d,s=1,t=1,u=1,v=1):
    return (a,b,c,d,s,t,u,v)


def adjoint(layer):
    return [block(c,d,a,b,u,v,s,t) for a,b,c,d,s,t,u,v in layer]


def apply(layer,x):
    y = [0]*len(x)
    for a,b,c,d,s,t,u,v in layer:
        first,second = s*x[a],t*x[b]
        y[c],y[d] = u*(first+second),v*(first-second)
    return y


def graph_tick(graph,state):
    # Sparse over clock phases, dense within each slice. Distinct clock slices
    # always have distinct successors, including the final wrap to zero.
    return {(c+1)%len(graph):apply(graph[c],v) for c,v in state.items()}


def embed(f,i,b,w):
    return 2*(w*f+i)+b


def on_tag(f,pairs,w,middle=None):
    a,b,sign = middle if middle is not None else (0,0,1)
    def earlier(i):
        return a if i==b else b if i==a else i
    return [block(embed(f,earlier(i),s,w),embed(f,earlier(j),s,w),
                  embed(f,i,s,w),embed(f,j,s,w),sign if earlier(i)==a else 1,
                  sign if earlier(j)==a else 1) for i,j in pairs for s in (0,1)]


def native_layer(k,w):
    result = []
    for f in range(k):
        for b in (0,1):
            for x in range(8):
                for z in range(5):
                    y = (z+int(x==0))%5
                    i = (2*x)*5+z
                    j = (2*((x+1)%8))*5+y
                    l = (2*((x-1)%8)+1)*5+y
                    result.append(block(embed(f,i,b,w),embed(f,i+5,b,w),embed(f,j,b,w),embed(f,l,b,w)))
    return result


def native_prefix_target():
    # Independent scalar signed path enumeration, including every port.
    out = [0]*80
    for word in range(16):
        x,c,z,sign = 6,0,0,1
        for j in range(4):
            d = (word>>j)&1
            z = (z+(x==0))%5
            if c==d==1:
                sign = -sign
            x,c = (x+(1 if d==0 else -1))%8,d
        out[(2*x+c)*5+z] += sign
    return out


def refs_for(x,t):
    S,w = 1<<t,len(x)
    def padded(v):
        return v+[0]*(w-len(v))
    refs = [x,padded([1]*S)]
    if -1 in x:
        refs.append(padded([-1]*S))
    for a in sorted(set(x)-{0,1,-1}):
        refs.append(padded([a]+[1]*(S-a*a)))
    while len(refs)&(len(refs)-1):
        refs.append(refs[1])
    return refs


def make_clock(x,t,native):
    ref = refs_for(x,t)
    k,w = len(ref),len(x)
    down,root,sign = parity_plan(x,t)
    if native:
        prep = [native_layer(k,w) for _ in range(t)]
        start = 60
    else:
        prep = [[g for f in range(k) for g in on_tag(f,p,w,(0,root,sign) if h==0 else None)]
                for h,p in enumerate(reversed(down))]
        start = 0
    split = []
    bit = 1
    while bit<k:
        split.append([block(embed(f,i,b,w),embed(f|bit,i,b,w),embed(f,i,b,w),embed(f|bit,i,b,w))
                      for f in range(k) if not f&bit for i in range(w) for b in (0,1)])
        bit <<= 1
    compare = [[block(embed(0,i,0,w),embed(0,i,1,w),embed(0,i,0,w),embed(0,i,1,w))
                for i in range(w)] for _ in range(2*t)]
    for f,target in enumerate(ref[1:],1):
        other,dst,sgn = parity_plan(target,t)
        for h,pairs in enumerate(down+other[::-1]):
            mid = (root,dst,sign*sgn) if h==t else None
            compare[h].extend(on_tag(f,pairs,w,mid))
    forward = prep+split+compare
    graph = forward+[adjoint(layer) for layer in reversed(forward)]
    dim = 2*k*w
    for layer in graph:
        assert sorted(i for g in layer for i in g[:2])==list(range(dim))
        assert sorted(i for g in layer for i in g[2:4])==list(range(dim))
    return graph,ref,start,len(prep),len(split),len(compare)


def solve_table(rows):
    # Unknowns are probabilities per OCCUPIED cell of each distinct signed
    # value. Identical columns of different signs are never assumed equal.
    labels = sorted(set(v for row in rows for v in row if v))
    A = [[F(row.count(v)) for v in labels]+[F(1,len(rows))] for row in rows]
    original = [r.copy() for r in A]
    pivot = 0
    for j in range(len(labels)):
        k = next((i for i in range(pivot,len(A)) if A[i][j]),None)
        if k is None:
            raise ArithmeticError("Reference system does not determine all signed weights")
        A[pivot],A[k] = A[k],A[pivot]
        A[pivot] = [v/A[pivot][j] for v in A[pivot]]
        for i in range(len(A)):
            if i!=pivot:
                A[i] = [a-A[i][j]*b for a,b in zip(A[i],A[pivot])]
        pivot += 1
    assert all(not any(r) for r in A[pivot:])
    solution = [A[i][-1] for i in range(pivot)]
    assert all(sum(a*b for a,b in zip(r,solution))==r[-1] for r in original)
    return dict(labels=labels,integer_rows=[list(map(int,r[:-1])) for r in original],
                row_total=str(original[0][-1]),rank=pivot,per_cell=[str(v) for v in solution])


def fourth_power_control(rows):
    k = len(rows)
    totals = [sum(v**4 for v in row) for row in rows]
    flat = [F(q,sum(totals)) for q in totals]
    unequal = None
    for i,row in enumerate(rows):
        for j,other in enumerate(rows[:i]):
            common = sorted((set(row)&set(other))-{0})
            if common and totals[i]!=totals[j]:
                v = common[0]
                unequal = dict(tags=[j,i],same_signed_value=v,
                               hierarchical_quartic_cell_weights=[str(F(v**4,k*totals[q])) for q in (j,i)])
                break
        if unequal:
            break
    return dict(flat_quartic_tag_weights=list(map(str,flat)),common_preserved_tag_weight=str(F(1,k)),
                flat_violates_tag_marginal=any(v!=F(1,k) for v in flat),
                hierarchical_respects_tag_marginal=True,hierarchical_violates_equal_cells=unequal)


def class_chains(values):
    classes = defaultdict(list)
    for cell,a in enumerate(values):
        if a:
            classes[a].append(cell)
    settings = [[],[]]
    for cells in classes.values():
        for j,pair in enumerate(zip(cells,cells[1:])):
            settings[j%2].append(pair)
    for pairs in settings:
        assert len({i for edge in pairs for i in edge})==2*len(pairs)
    return classes,settings


def per_cell_system(ref,edges):
    k,w = len(ref),len(ref[0])
    cells = [i for i,v in enumerate(sum(ref,[])) if v]
    columns = {v:i for i,v in enumerate(cells)}
    equations = []
    for i,j in edges:
        row = [F(0)]*(len(cells)+1)
        row[columns[i]],row[columns[j]] = 1,-1
        equations.append(row)
    edge_count = len(equations)
    for f in range(k):
        equations.append([F(v//w==f) for v in cells]+[F(1,k)])
    original = [r.copy() for r in equations]
    for j in range(len(cells)):
        i = next((i for i in range(j,len(equations)) if equations[i][j]),None)
        assert i is not None
        equations[i],equations[j] = equations[j],equations[i]
        fac = F(equations[j][j])
        equations[j] = [x/fac for x in equations[j]]
        for i,row in enumerate(equations):
            if i!=j and row[j]:
                multiplier = row[j]
                equations[i] = [a-multiplier*b for a,b in zip(row,equations[j])]
    assert all(not any(r) for r in equations[len(cells):])
    solution = [r[-1] for r in equations[:len(cells)]]
    assert all(sum(a*x for a,x in zip(r,solution))==r[-1] for r in original)
    for i,value in zip(cells,solution):
        assert value==F(ref[i//w][i%w]**2,k*norm(ref[0]))
    return dict(occupied_columns=cells,edge_equations=edge_count,tag_equations=k,rank=len(cells),
                per_cell=list(map(str,solution)))


def echo_tv(weights,settings,classes):
    # Independent operational propagation of the compared outputs and the
    # individually idling outputs; the comparator input masses need not be equal.
    start = [[w/2 for w in weights] for _ in settings]
    returned = [r.copy() for r in start]
    for s,pairs in enumerate(settings):
        for i,j in pairs:
            bright = start[s][i]+start[s][j]
            returned[s][i]=returned[s][j]=bright/2
    resolved = sum(abs(a-b) for row,base in zip(returned,start) for a,b in zip(row,base))/2
    edge_sum = sum(abs(weights[i]-weights[j]) for pairs in settings for i,j in pairs)
    marginal = sum(abs(row[0]+row[1]-b) for row,b in zip(zip(*returned),weights))/2
    spread = max(max(weights[i] for i in indices)-min(weights[i] for i in indices) for indices in classes.values())
    assert resolved==edge_sum/4 and spread<=4*resolved and marginal<=resolved
    return dict(resolved_TV=str(resolved),setting_unread_TV=str(marginal),edge_variation=str(edge_sum),
                largest_class_spread=str(spread),cancellation_on_forgetting_setting=(marginal<resolved))


def extend_probes(x,t,native):
    old,ref,launch,prep,fanout,compare = make_clock(x,t,native)
    w,k = len(x),len(ref)
    cells = sum(ref,[])
    classes,settings = class_chains(cells)
    old_dim = 2*len(cells)
    dim = 2*old_dim
    half = len(old)//2
    def double_layer(layer):
        return [block(2*a+s,2*b+s,2*c+s,2*d+s,*g) for s in (0,1) for a,b,c,d,*g in layer]
    forward = [double_layer(layer) for layer in old[:half]]
    fork = [block(2*v,2*v+1,2*v,2*v+1) for v in range(old_dim)]
    probe = []
    for s,pairs in enumerate(settings):
        used = {i for pair in pairs for i in pair}
        old_pairs = [(2*i+b,2*j+b) for i,j in pairs for b in (0,1)]
        # An unmatched active cell meets only its own blank private rail. An
        # H twice on these two coordinates leaves the cell unchanged in both
        # probability and amplitude, using sharpness of the returned dark rail.
        old_pairs += [(2*i,2*i+1) for i in range(len(cells)) if i not in used]
        probe += [block(2*a+s,2*b+s,2*a+s,2*b+s) for a,b in old_pairs]
    forward += [fork,probe]
    graph = forward+[adjoint(layer) for layer in reversed(forward)]
    for layer in graph:
        assert sorted(i for g in layer for i in g[:2])==list(range(dim))
        assert sorted(i for g in layer for i in g[2:4])==list(range(dim))
    basis = [int(i==2*embed(0,launch,0,w)) for i in range(dim)]
    state = {0:basis}; zeros=Counter(); kernel_prefix = []
    for c in range(len(graph)):
        v = state[c]
        state = graph_tick(graph,state)
        u = state[(c+1)%len(graph)]
        assert norm(u)==1<<(c+1)
        # Check the zero-mass induction independently of a Born weight:
        # zero-input rows have zero total under local positive flow; a new
        # zero on a two-occupied-input block requires a sharp dark read.
        for a,b,o,p,*_ in graph[c]:
            occupied = int(v[a]!=0)+int(v[b]!=0)
            blanks = int(u[o]==0)+int(u[p]==0)
            if occupied==0:
                assert blanks==2
                zeros["zero_input_pair_outputs"]+=2
            elif occupied==1:
                assert blanks==0
                zeros["single_arm_blocks"]+=1
            else:
                assert blanks<=1
                zeros["destructive_zero_outputs"]+=blanks
            if prep+fanout<=c<half:
                # Each filled comparison-wire block preserves its old tag. On
                # tag zero the two endpoints also preserve the physical cell.
                assert len({j//(4*w) for j in (a,b,o,p)})==1
                if a//(4*w)==0:
                    assert len({j//4 for j in (a,b,o,p)})==1
        # Prior tag fanout and deferred setting fanout are literal balanced
        # splitters against blank children, so the assumed fair law applies
        # cell-by-cell even if different active cells have different weights.
        if prep<=c<prep+fanout or c==half:
            assert all(v[b]==0 and abs(u[o])==abs(u[p]) for a,b,o,p,*_ in graph[c])
            kernel_prefix.append(c)
        if c+1==half+1:
            assert all(u[4*i+s]==(1<<t)*a and u[4*i+2+s]==0 for i,a in enumerate(cells) for s in (0,1))
        if c+1==half+2:
            assert all(u[4*i+s]==(2<<t)*cells[i] and u[4*j+s]==0
                       for s,pairs in enumerate(settings) for i,j in pairs)
            assert all(u[4*i+2+s]==u[4*j+2+s]==0 for s,pairs in enumerate(settings) for i,j in pairs)
        if c+1==half+3:
            assert all(u[4*i+s]==(2<<t)*a and u[4*i+2+s]==0 for i,a in enumerate(cells) for s in (0,1))
    assert state=={0:[d*(1<<(len(graph)//2)) for d in basis]}
    alt = {1:[(i%5)-2 for i in range(dim)],half+1:basis}
    updated = alt
    for _ in graph:
        updated = graph_tick(graph,updated)
    assert updated=={p:[d*(1<<(len(graph)//2)) for d in v] for p,v in alt.items()}
    edge_system = per_cell_system(ref,settings[0]+settings[1])
    born = [F(a*a,k*norm(x)) for a in cells]
    quartic = [F(a**4,k*sum(b**4 for b in row)) for row in ref for a in row]
    tv_born = echo_tv(born,settings,classes)
    tv_quartic = echo_tv(quartic,settings,classes)
    assert tv_born["resolved_TV"]=="0"
    return dict(original_period=len(old),period=len(graph),fiber=dim,graph_vertices=dim*len(graph),
                graph_sha256=sha256(json.dumps(graph,separators=(",",":")).encode()).hexdigest(),
                table_phase=half,clean_setting_split_phase=half+1,bright_dark_phase=half+2,
                resolved_echo_phase=half+3,per_cell_fair_split_input_phases=kernel_prefix,
                classes=[[a,idx] for a,idx in sorted(classes.items())],settings=settings,edge_system=edge_system,
                support_induction_block_counts=dict(zeros),zero_launch_support=len(basis)-1,
                nonzero_odd_class_sizes=[len(idx) for idx in classes.values() if len(idx)%2],
                squared_weight_echo=tv_born,hierarchical_quartic_echo=tv_quartic,
                literal_launch_closure=True,two_phase_input_closure=True)


def verify_case(name,x,t,native):
    graph,ref,initial,prep,split,comparison = make_clock(x,t,native)
    k,w = len(ref),len(x)
    n = 2*k*w
    v0 = [int(i==embed(0,initial,0,w)) for i in range(n)]
    state = {0:v0}
    table_phase = len(graph)//2
    state_hashes = []
    phase_checks = []
    for clock in range(len(graph)+1):
        phase = clock%len(graph)
        assert list(state)==[phase]
        v = state[phase]
        assert norm(v)==1<<clock
        state_hashes.append(sha256(json.dumps(v,separators=(",",":")).encode()).hexdigest())
        if clock==prep:
            assert [v[embed(0,i,0,w)] for i in range(w)]==x
        if prep<=clock<=prep+split:
            assert all(sum(v[embed(f,i,b,w)]**2 for f in range(k) for b in (0,1))==
                       x[i]**2*(1<<(clock-prep)) for i in range(w))
        if prep+split<=clock<=table_phase+comparison:
            assert all(k*sum(v[embed(f,i,b,w)]**2 for i in range(w) for b in (0,1))==1<<clock for f in range(k))
            assert all(k*(1<<t)*sum(v[embed(0,i,b,w)]**2 for b in (0,1))==x[i]**2*(1<<clock)
                       for i in range(w))
            phase_checks.append(phase)
        if clock==table_phase:
            assert all(v[embed(f,i,b,w)]==((1<<t)*ref[f][i] if b==0 else 0)
                       for f in range(k) for i in range(w) for b in (0,1))
        if clock<len(graph):
            state = graph_tick(graph,state)
    assert state=={0:[v*(1<<table_phase) for v in v0]}
    # Independent nonlocalized clock input: no phase-dependent driver. Over a
    # complete cycle every conjugate of the identity monodromy is the identity.
    v1 = [(i%5)-2 for i in range(n)]
    alt = {1:v1,table_phase:v0}
    after = alt
    for _ in graph:
        after = graph_tick(graph,after)
    assert after=={p:[a*(1<<table_phase) for a in v] for p,v in alt.items()}
    system = solve_table(ref)
    per_cell = dict(zip(system["labels"],map(F,system["per_cell"])))
    old_record = [k*per_cell.get(a,F(0)) for a in x]
    assert old_record==[F(a*a,1<<t) for a in x] and sum(old_record)==1
    for a,q in zip(system["labels"],system["per_cell"]):
        assert F(q)==F(a*a,k*(1<<t))
    quartic = fourth_power_control(ref)
    assert quartic["flat_violates_tag_marginal"] and quartic["hierarchical_violates_equal_cells"]
    return dict(case=name,w=w,K=k,period=len(graph),total_graph_vertices=n*len(graph),fiber=n,
                positive_ticks_to_x=prep,positive_ticks_to_table=table_phase,launch_cell=initial,
                native_prefix_herald_vector=x[:5] if native else None,protected_phase_checks=phase_checks,
                reference_table=[[ [i,v] for i,v in enumerate(row) if v] for row in ref],
                normalized_target_event_masses=list(map(str,old_record)),linear_system=system,
                phase_state_hashes=state_hashes,full_orbit_return=True,two_phase_superposition_return=True,
                graph_sha256=sha256(json.dumps(graph,separators=(",",":")).encode()).hexdigest(),quartic=quartic)


def main():
    x = native_prefix_target()
    assert x[:5]==[2,1,0,0,0] and norm(x)==16
    rows = [verify_case("physical_N8_M5_launch",x,4,True),
            verify_case("odd_signed_depth_three",[-2,1,1,1,-1,0,0,0],3,False)]
    # Dense adverse check: every table coordinate has positive mass. Both tags
    # initially have the same squared norm; an inter-tag swap breaks protection.
    dense = [[3,3,3,1,1,1,1,1],[4,2,2,2,1,1,1,1]]
    leakage = [row.copy() for row in dense]
    leakage[0][0],leakage[1][0] = leakage[1][0],leakage[0][0]
    quartic = fourth_power_control(dense)
    assert list(map(norm,dense))==[32,32] and list(map(norm,leakage))==[39,25]
    assert quartic["flat_violates_tag_marginal"] and quartic["hierarchical_violates_equal_cells"]
    probes = [extend_probes(x,4,True),extend_probes([-2,1,1,1,-1,0,0,0],3,False),
              extend_probes([1,0],0,False)]
    single_classes,single_edges = class_chains([-1,1,1,1,0])
    assert single_classes[-1]==[0] and single_edges==[[(1,2)],[(2,3)]]
    linear_classes,linear_edges = class_chains([1,1,1])
    linear_weights = [F(1,6),F(1,3),F(1,2)]
    cancellation = echo_tv(linear_weights,linear_edges,linear_classes)
    assert cancellation["resolved_TV"]=="1/12" and cancellation["setting_unread_TV"]=="1/24"
    for r in probes[:2]:
        assert F(r["hierarchical_quartic_echo"]["resolved_TV"])>0
    # A marginally fair setting is insufficient: with half the mass in each
    # setting, each initial data coordinate can still be confined to one side.
    return dict(trials=rows,checks=dict(balanced_signed_graph_regular=True,cyclic_clock_including_origin=True,
                 native_full_walk_equals_direct_words=True,all_split_and_protected_masks=True,
                 separate_signed_unknowns_full_rank=True,reconstructed_every_target_marginal=True,
                 two_phase_superposition_control=True,flat_and_conditional_quartic_failures=True,
                 dense_tag_leakage_detected=True),deferred_probe_addendum=dict(trials=probes,
                    occupied_singleton_control=dict(values=[-1,1,1,1,0],settings=single_edges),
                    setting_marginal_cancellation=dict(weights=list(map(str,linear_weights)),result=cancellation),
                    checks=dict(clean_single_bit_split_per_cell=True,two_disjoint_matchings_span_signed_classes=True,
                                full_rank_per_occupied_cell_without_class_unknowns=True,blank_private_comparators=True,
                                zero_support_structural_induction=True,echo_and_reverse_uncomputation=True,
                                alternative_clock_input=True,squared_zero_and_quartic_nonzero_TV=True,
                                exact_edge_variation_and_marginal_cancellation=True,local_tag_and_target_masks=True),
                    opaque_setting_control=dict(joint=[["1/2","0"],["0","1/2"]],marginal_settings=["1/2","1/2"],
                                                conditional_setting_probabilities=[["1","0"],["0","1"]]),
                    scope="The original trials describe a table with stipulated equal-cell symmetry. The augmented "
                          "clocks replace that stipulation and tag-fanout symmetry with a per-cell fair single-arm "
                          "response, nonnegative flow confined to the paired wires, and sharp destructive outputs "
                          "from a sharp localized launch. Conditional reversed fairness at an occupied bright "
                          "output gives equality of the two input flows; for zero pair mass equality is automatic. "
                          "Alternatively a coordinatewise undisturbed H-squared echo and forward single-arm fairness "
                          "give the same equality. Only the added comparison clock provides the tests. The "
                          "echo-TV calculation compares these forward response assumptions on the supplied table "
                          "to an individually idling read, before setting recombination; amplitude closure is for "
                          "a coherent unmeasured orbit."),
                 dense_adverse=dict(rows=dense,all_cells_occupied=True,
                 before_tag_mass=["1/2","1/2"],after_cross_tag_swap=["39/64","25/64"],quartic=quartic),
                convention="A clock phase is an actual coordinate. Every edge goes from c to c+1 mod P, "
                           "with a signed 2x2 block and amplitude normalization 1/sqrt(2). The second half "
                           "contains transpose blocks in reverse order and still advances the clock. "
                           "All reference columns are present at one table phase in one run; the read is "
                           "distinct from propagation without a read around the closed orbit.",
                assumptions="Additivity and normalization of coordinate records, zero-cell impossibility, "
                            "symmetry between occupied cells of equal signed amplitude at the stipulated "
                            "read (including tag symmetry of the balanced copied flags), and invariance of "
                            "record weights of the indicated protected masks. These experimental laws are "
                            "additional to signed geometric propagation. A controlled, finite comparison "
                            "apparatus and a readable phase are supplied.")


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("directory",type=Path)
    directory = parser.parse_args().directory
    data = main()
    directory.mkdir(parents=True,exist_ok=True)
    (directory/"autonomous_records.json").write_text(json.dumps(data,separators=(",",":"))+"\n",encoding="utf8")
    print([(v["case"],v["period"],v["linear_system"]["rank"]) for v in data["trials"]])
