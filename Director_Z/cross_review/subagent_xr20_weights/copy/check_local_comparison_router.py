"""Literal forward ticks on a doubled flat signed walk, with local rail/coin switches."""

import argparse
import json
from collections import deque
from hashlib import sha256
from pathlib import Path

from check_coherent_comparison import compile_down, full_match, hadamards, index

def cell(x,c,n):
    return 2*(x % n)+c


def step_mode(v,direction,n):
    x,c = divmod(v,2)
    return cell(x+direction*(1 if c==0 else -1),c,n)


def link_reverse(v,n):
    """T=S X_all on mode coordinates. T is an involution."""
    return step_mode(v^1,1,n)


def tick(vector,n,switch):
    # One positive clock. On plus, U=SH. On minus, U^T=H S^-1.
    # A chosen on-site swap is relative to that rail's own H, in both rails.
    out = [0]*len(vector)
    for rail in range(2):
        base = 2*n*rail
        for x in range(n):
            in_here = [cell(x,c,n) for c in (0,1)]
            if rail:
                in_here = [step_mode(v,1,n) for v in in_here]
            a,b = (vector[base+v] for v in in_here)
            if switch==("pre",x):
                a,b = b,a
            pair = [a+b,a-b]
            if switch==("post",x):
                pair.reverse()
            for c,val in enumerate(pair):
                dest = cell(x,c,n) if rail else step_mode(cell(x,c,n),1,n)
                out[base+dest] = val
    return out


def run_word(vector,n,word):
    power = 0
    for gate in word:
        if gate=="J":
            vector = vector[2*n:]+vector[:2*n]
        else:
            vector = tick(vector,n,gate)
            power += 1
            if power>=2 and all(x%2==0 for x in vector):
                vector = [v//2 for v in vector]
                power -= 2
    return vector,power


def scale_to(v,old,new):
    assert new>=old and (new-old)%2==0
    return [a*2**((new-old)//2) for a in v]


def compare_columns(n,word,expected,expected_power):
    maximum = 0
    wrong = []
    payload = sha256()
    plus_leak = 0
    for k in range(4*n):
        x = [int(i==k) for i in range(4*n)]
        v,p = run_word(x,n,word)
        target = expected(x)
        power = max(p,expected_power)
        actual = scale_to(v,p,power)
        want = scale_to(target,expected_power,power)
        error = max(abs(a-b) for a,b in zip(actual,want))
        maximum = max(maximum,error)
        if error:
            wrong.append(k)
        if k<2*n:
            plus_leak += sum(vv!=0 for vv in v[2*n:])
        payload.update(json.dumps([p,v],separators=(",",":")).encode("ascii")+b"\n")
    return dict(columns=4*n,wrong_columns=wrong,max_integer_coefficient_error=maximum,
                blank_minus_nonzero_entries_at_end=plus_leak,normalized_column_sha256=payload.hexdigest(),
                positive_ticks=sum(g!="J" for g in word),rail_switches=word.count("J"))


def oracle_perm(v,n,swaps):
    v = v.copy()
    for u,w in swaps:
        v[u],v[w] = v[w],v[u]
        a,b = 2*n+link_reverse(u,n),2*n+link_reverse(w,n)
        v[a],v[b] = v[b],v[a]
    return v


def oracle_U(v,n):
    # Independent sparse columns, using forward signed arc scattering and its
    # algebraic transpose. This is distinct from tick's destination gathering.
    out = [0]*len(v)
    for x in range(n):
        for c in (0,1):
            i = cell(x,c,n)
            for d in (0,1):
                j = cell(x+(1 if d==0 else -1),d,n)
                sign = -1 if c==d==1 else 1
                out[j] += sign*v[i]
                out[2*n+i] += sign*v[2*n+j]
    return out


INVERSE = ["J",None,"J"]


def local_edges(n):
    # Value is the physical gate sequence for one logically isolated swap.
    out = {}
    for x in range(n):
        branches = {("pre",x):[("pre",x)]+INVERSE,("post",x):INVERSE+[("post",x)]}
        for (kind,site),word in branches.items():
            pair = [cell(site,c,n) for c in (0,1)]
            if kind=="post":
                pair = [step_mode(v,1,n) for v in pair]
            out.setdefault(tuple(sorted(pair)),word)
    return out


def path_between(start,end,edges):
    parent = {start:None}
    queue = deque([start])
    while queue:
        u = queue.popleft()
        if u==end:
            path = []
            while u is not None:
                path.append(u)
                u = parent[u]
            return path[::-1]
        for i,j in edges:
            if u!=i and u!=j:
                continue
            v = j if u==i else i
            if v not in parent:
                parent[v] = u
                queue.append(v)
    return []


def route_swap(a,b,edges):
    path = path_between(a,b,edges)
    assert path
    chain = [tuple(sorted(p)) for p in zip(path,path[1:])]
    sequence = chain+chain[-2::-1]
    return [g for edge in sequence for g in edges[edge]],path


def pairs_to_swaps(sources,destinations):
    # Return chronological endpoint transpositions that realize this full
    # bijection. Keep the mapping separate from physical neighbor swaps.
    assert set(sources)==set(destinations) and len(sources)==len(set(sources))
    mapping = dict(zip(sources,destinations))
    visited = set()
    out = []
    for start in sources:
        if start in visited:
            continue
        u = start
        while u not in visited:
            visited.add(u)
            next_u = mapping[u]
            if next_u!=start:
                out.append((start,next_u))
            u = next_u
    return out


def permutation_word(swaps,edges):
    return [g for a,b in swaps for g in route_swap(a,b,edges)[0]]


def ordered_matching(n,parity):
    # Interlace modes from distant sites, changing also which endpoint reads
    # the negative column. The desired outputs use the same local labels on
    # the other spatial parity.
    sites = range(parity,n,2)
    inputs = [cell(x+(j%2)*2, j%2,n) for x in sites for j in (0,1)]
    # Reverse every other pair, so signs as well as coverage are tested.
    for i in range(2,len(inputs),4):
        inputs[i],inputs[i+1] = inputs[i+1],inputs[i]
    outputs = [cell((v//2+1)%n,v%2,n) for v in inputs]
    regular = [cell(x,c,n) for x in sites for c in (0,1)]
    pre = pairs_to_swaps(inputs,regular)
    post = pairs_to_swaps([step_mode(v,1,n) for v in regular],outputs)
    return inputs,outputs,pre,post


def match_on_parity(n,parity,edges):
    inputs,outputs,pre,post = ordered_matching(n,parity)
    word = permutation_word(pre,edges)+[None]+permutation_word(post,edges)
    def predicted(v):
        return oracle_perm(oracle_U(oracle_perm(v,n,pre),n),n,post)
    matrix = compare_columns(n,word,predicted,1)
    desired_wrong = []
    leakage = 0
    destructive_controls = []
    for j,source in enumerate(inputs):
        raw = [int(i==source) for i in range(4*n)]
        value,p = run_word(raw,n,word)
        assert p==1
        # Direct specified matching, independent of the chosen pre/post permutations.
        desired = [0]*(4*n)
        offset = j-j%2
        desired[outputs[offset]] = 1
        desired[outputs[offset+1]] = -1 if j%2 else 1
        if value!=desired:
            desired_wrong.append(source)
        leakage += sum(val!=0 for i,val in enumerate(value) if i not in outputs)
    for sign in (1,-1):
        raw = [0]*(4*n)
        raw[inputs[0]],raw[inputs[1]] = 1,sign
        value,p = run_word(raw,n,word)
        # The prepared input has a further common factor 1/sqrt(2).
        target = [0]*(4*n)
        bright = outputs[0 if sign==1 else 1]
        dark = outputs[1 if sign==1 else 0]
        target[bright] = 2
        actual = scale_to(value,p,1)
        destructive_controls.append(dict(relative_sign=sign,bright=bright,dark=dark,
                                         dark_numerator=actual[dark],bright_numerator=actual[bright],
                                         other_cells_sum_squared=sum(a*a for i,a in enumerate(actual) if i!=bright),
                                         full_signed_vector_exact=(actual==target)))
    return dict(input_parity=parity,ordered_source_pairs=list(zip(inputs[::2],inputs[1::2])),
                ordered_output_pairs=list(zip(outputs[::2],outputs[1::2])),pre_logical_swaps=pre,
                post_logical_swaps=post,physical_word=word,full_matrix=matrix,
                desired_matching_wrong_columns=desired_wrong,nonzero_outside_blank_coordinates=leakage,
                dark_and_bright_controls=destructive_controls)


def trial(n):
    edges = local_edges(n)
    # Choose a longest same-component shortest path from plus root 0.
    path = max((path_between(0,v,edges) for v in range(2*n)),key=len)
    u,w = path[0],path[-1]
    swap,chain = route_swap(u,w,edges)
    inverse = compare_columns(n,[None]+INVERSE,lambda v:v,0)
    inverse_back = compare_columns(n,INVERSE+[None],lambda v:v,0)
    native = compare_columns(n,[None],lambda v:oracle_U(v,n),1)
    elementary = []
    for x in range(n):
        for kind in ("pre","post"):
            pair = [cell(x,c,n) for c in (0,1)]
            word = [(kind,x)]+INVERSE
            if kind=="post":
                pair = [step_mode(v,1,n) for v in pair]
                word = INVERSE+[(kind,x)]
            result = compare_columns(n,word,lambda v,p=pair:oracle_perm(v,n,[p]),0)
            elementary.append(dict(site=x,switch=kind,plus_pair=pair,**result))
    transposition = compare_columns(n,swap,lambda v:oracle_perm(v,n,[(u,w)]),0)
    matching = [match_on_parity(n,p,edges) for p in (0,1)]
    wrong = compare_columns(n,[None,None],lambda v:v,0)
    # Delete exactly one J, retaining the same number of forward ticks.
    broken = swap.copy()
    broken.remove("J")
    wrong_swap = compare_columns(n,broken,lambda v:oracle_perm(v,n,[(u,w)]),0)
    return dict(N=n,sites_and_directions="2*x+c, c=0 for R and 1 for L; minus rail offset 2*N",
                base_forward=native,echo_after=inverse,echo_before=inverse_back,
                isolated_generators=elementary,isolated_edges=list(edges),
                reachable_from_zero=[v for v in range(2*n) if path_between(0,v,edges)],
                opposite_parity_path=path_between(0,cell(1,0,n),edges),nonlocal_swap=dict(endpoints=[u,w],
                    shortest_chain=chain,physical_word=swap,columns=transposition),
                requested_matchings=matching,forward_instead_of_inverse=wrong,
                missing_one_switch=wrong_swap)


def parity_cells(n,p):
    return [cell(x,c,n) for x in range(p,n,2) for c in (0,1)]


def physical_matching(n,p,pairs,edges):
    before,after = parity_cells(n,p),parity_cells(n,1-p)
    ordered = [i for pair in pairs for i in pair]
    assert sorted(ordered)==list(range(n))
    pre = pairs_to_swaps([before[i] for i in ordered],before)
    post = pairs_to_swaps([step_mode(v,1,n) for v in before],[after[i] for i in ordered])
    return permutation_word(pre,edges)+[None]+permutation_word(post,edges)


def sign_word(n,p,targets,edges,disabled=False):
    # H X H on a selected ordered pair is diag(1,-1). Partner cells
    # and inactive pairs receive identity. Both H layers run over the full register.
    allowed = [i for i in range(n) if i not in targets]
    pairs = list(zip(allowed[:len(targets)],targets))
    rest = allowed[len(targets):]
    pairs += list(zip(rest[::2],rest[1::2]))
    middle = parity_cells(n,1-p)
    selected = [(middle[a],middle[b]) for a,b in pairs[:len(targets)]]
    middle_word = permutation_word(selected,edges)
    if disabled:
        middle_word = ([None]+INVERSE)*(sum(g!="J" for g in middle_word)//2)
    return (physical_matching(n,p,pairs,edges)+middle_word+
            physical_matching(n,1-p,pairs,edges))


def compile_selector_route(source,target,active,sign_source):
    n,t,w = 32,3,8
    edges = local_edges(n)
    p = 0
    actions = []
    def add_H(stage,pairs):
        nonlocal p
        actions.append((stage,physical_matching(n,p,pairs,edges),("H",pairs),1))
        p = 1-p
    def add_sign(stage,targets):
        actions.append((stage,sign_word(n,p,targets,edges),("Z",targets),0))
    def add_swaps(stage,pairs):
        modes = parity_cells(n,p)
        word = permutation_word([(modes[a],modes[b]) for a,b in pairs],edges)
        actions.append((stage,word,("X",pairs),0))
    add_H("selector",[(index(0,i,s,w),index(1,i,s,w)) for i in range(w) for s in (0,1)])
    targets = [index(active,0,s,w) for s in (0,1)]
    modified = target.copy() if not sign_source else source.copy()
    modified[0] *= -1
    plan_src = compile_down(modified if sign_source else source,t)
    plan_dst = compile_down(target if sign_source else modified,t)
    # A signed reference compilation makes the middle signed permutation
    # genuinely active even though both requested end vectors are nonnegative.
    if sign_source:
        add_sign("before reduction phase",targets)
    else:
        actions.append(("before reduction phase",[],("X",[]),0))
    for i,pairs in enumerate(plan_src[0]):
        add_H(f"reduce {i+1}",full_match(w,active,pairs))
    src,dst = plan_src[1],plan_dst[1]
    assert src!=dst and plan_src[2]*plan_dst[2]==-1
    add_swaps("middle permutation",[(index(active,src,s,w),index(active,dst,s,w)) for s in (0,1)])
    add_sign("middle phase",[index(active,dst,s,w) for s in (0,1)])
    for i,pairs in enumerate(reversed(plan_dst[0])):
        add_H(f"prepare {i+1}",full_match(w,active,pairs))
    if not sign_source:
        add_sign("after preparation phase",targets)
    else:
        actions.append(("after preparation phase",[],("X",[]),0))
    return actions


def logical_action(vector,action):
    kind,args = action
    if kind=="H":
        return hadamards(vector,args)
    v = vector.copy()
    if kind=="X":
        for a,b in args:
            v[a],v[b] = v[b],v[a]
    else:
        for i in args:
            v[i] *= -1
    return v


def physical_propagation(source,active,actions,durations,j_budgets,omit_phase=False):
    n,w = 32,8
    physical = [0]*(4*n)
    logical = [0]*n
    for i,value in enumerate(source):
        physical[parity_cells(n,0)[index(0,i,0,w)]] = value
        logical[index(0,i,0,w)] = value
    power,ideal_power,clock,p = 0,0,0,0
    rows = []
    for (label,word,action,parity_change),duration,j_budget in zip(actions,durations,j_budgets):
        if omit_phase and label=="middle phase":
            word = sign_word(n,p,action[1],local_edges(n),disabled=True)
        size = sum(g!="J" for g in word)
        assert duration>=size and (duration-size)%2==0
        padded = word+([None]+INVERSE)*((duration-size)//2)
        # J is itself a local physical layer. Align the wall-clock count for
        # these as well as W at every comparison boundary using J^2=I.
        extra = j_budget-padded.count("J")
        assert extra>=0 and extra%2==0
        padded += ["J"]*extra
        fixed = [parity_cells(n,p)[index(1-active,0,s,w)] for s in (0,1)]
        # A stationary single-rail geometric mask is a separate diagnostic
        # from the encoded mask at the completed stage. Include its rail mate
        # as well, so a J alone cannot cause this example.
        fixed += [v+2*n for v in fixed]
        initial_fixed = sum(physical[v]**2 for v in fixed)
        start_power = power
        first_static_change = None
        peak_minus_support = 0
        for gate in padded:
            if gate=="J":
                physical = physical[2*n:]+physical[:2*n]
            else:
                physical = tick(physical,n,gate)
                power += 1
                clock += 1
                if power>=2 and all(a%2==0 for a in physical):
                    physical = [a//2 for a in physical]
                    power -= 2
                if label!="selector" and first_static_change is None:
                    now = sum(physical[v]**2 for v in fixed)
                    if (now << start_power)!=(initial_fixed << power):
                        first_static_change = clock
            peak_minus_support = max(peak_minus_support,sum(v!=0 for v in physical[2*n:]))
        logical = logical_action(logical,action)
        ideal_power += parity_change
        p ^= parity_change
        modes = parity_cells(n,p)
        mask = set(modes)
        actual = [physical[v] for v in modes]
        common = max(power,ideal_power)
        a = scale_to(actual,power,common)
        b = scale_to(logical,ideal_power,common)
        leakage = sum(v!=0 for i,v in enumerate(physical) if i not in mask)
        assert sum(a*a for a in physical)==8*(1<<power)
        numerators = [sum(actual[index(1-active,i,s,w)]**2 for s in (0,1)) for i in range(w)]
        protected = all(2*value==source[i]**2*(1<<power) for i,value in enumerate(numerators))
        rows.append(dict(stage=label,positive_ticks=size,padded_positive_ticks=duration,elapsed_positive_ticks=clock,
                         on_site_rail_switch_layers=padded.count("J"),logical_parity=p,
                         logical_oracle_mismatch=sum(v!=z for v,z in zip(a,b)),outside_logical_modes=leakage,
                         logical_protected_masks_unchanged=protected,intermediate_peak_occupied_minus_modes=peak_minus_support,
                         first_change_of_input_static_two_rail_mask=first_static_change,
                         expanded_word_sha256=sha256(json.dumps(padded,separators=(",",":")).encode()).hexdigest()))
    final = scale_to(physical,power,max(power,1))
    assert power==1  # Input numerators have common intrinsic denominator sqrt(8).
    return dict(stages=rows,physical_mode_numerators=final,occupancy_squared_denominator=16,
                elapsed_positive_ticks=clock,total_rail_switch_layers=sum(r["on_site_rail_switch_layers"] for r in rows))


def entire_comparison():
    x,y = [2,1,1,1,1,0,0,0],[1]*8
    a = compile_selector_route(x,y,1,False)
    b = compile_selector_route(y,x,0,True)
    durations = [max(sum(g!="J" for g in word),sum(g!="J" for g in other))
                 for (_,word,_,_),(_,other,_,_) in zip(a,b)]
    j_budgets = [max(w.count("J")+duration-sum(g!="J" for g in w) for w in (u[1],v[1]))
                 for u,v,duration in zip(a,b,durations)]
    left = physical_propagation(x,1,a,durations,j_budgets)
    right = physical_propagation(y,0,b,durations,j_budgets)
    bad = physical_propagation(x,1,a,durations,j_budgets,omit_phase=True)
    expected = [0]*128
    modes = parity_cells(32,1)
    for flag,values in enumerate((x,y)):
        for i,v in enumerate(values):
            expected[modes[index(flag,i,0,8)]] = v
    good = all(r["physical_mode_numerators"]==expected and
               all(s["logical_oracle_mismatch"]==s["outside_logical_modes"]==0 and s["logical_protected_masks_unchanged"]
                   for s in r["stages"]) for r in (left,right))
    mismatch = [i for i,(u,v) in enumerate(zip(bad["physical_mode_numerators"],expected)) if u!=v]
    return dict(N=32,t=3,data_width=8,start_x=x,start_y=y,logical_index="2*(8*selector+cell)+private",
                parity_embedding="At parity p order plus modes by increasing x=p,p+2,... and R,L at each site.",
                source_x_route=left,source_y_route=right,common_stage_ticks=durations,
                common_stage_J_layers=j_budgets,common_serial_layer_count=sum(durations)+sum(j_budgets),
                both_routes_equal_expected=good,synchronized_rail_switch_counts=(
                    [r["on_site_rail_switch_layers"] for r in left["stages"]]==
                    [r["on_site_rail_switch_layers"] for r in right["stages"]]),
                omitted_middle_phase_bad_cells=mismatch,
                adverse_elapsed_W_and_J=[bad["elapsed_positive_ticks"],bad["total_rail_switch_layers"]],
                static_mask_scope="After the selector, the stationary physical read on the two input-embedding "
                                  "coordinates for the protected flag's cell zero, on both rails, can change "
                                  "during routed W ticks. All eight encoded protected masks were checked at each "
                                  "padded logical boundary. Their intermediate Heisenberg pullbacks need not be site masks.",
                experimental_scope="Every reported good and bad route was executed as explicit W and J operations on "
                                   "one full integer mode vector. Switches inside routed permutation echoes were "
                                   "executed; no intermediate projective reads or symbolic swap replacement.")


def main():
    rows = [trial(n) for n in (2,4,6,10,18)]
    checks = dict(
        base_and_both_echo_orders=all(not r[k]["wrong_columns"] for r in rows for k in ("base_forward","echo_after","echo_before")),
        all_isolated_generators=all(not a["wrong_columns"] for r in rows for a in r["isolated_generators"]),
        within_parity_routing=all(len(r["reachable_from_zero"])==r["N"] and not r["opposite_parity_path"]
                                  and not r["nonlocal_swap"]["columns"]["wrong_columns"] for r in rows),
        full_requested_matchings=all(not a["full_matrix"]["wrong_columns"] and not a["desired_matching_wrong_columns"]
                                     and a["nonzero_outside_blank_coordinates"]==0 for r in rows for a in r["requested_matchings"]),
        missing_switch_detected=all(len(r["missing_one_switch"]["wrong_columns"])==4*r["N"] for r in rows),
        mistaken_forward_echo_small_ring_exception=all(
            len(r["forward_instead_of_inverse"]["wrong_columns"])==(0 if r["N"]==2 else 4*r["N"]) for r in rows),
        destructive_and_constructive_superpositions=all(
            c["full_signed_vector_exact"] for r in rows for a in r["requested_matchings"] for c in a["dark_and_bright_controls"]))
    comparison = entire_comparison()
    checks["entire_literal_comparison"] = (comparison["both_routes_equal_expected"] and
                  comparison["synchronized_rail_switch_counts"] and bool(comparison["omitted_middle_phase_bad_cells"]))
    return dict(trials=rows,checks=checks,entire_comparison=comparison,
                clock="Each None in the physical word is a forward W; [pre,x] or [post,x] is a forward W "
                      "with a local coin exchange at site x, before or after its rail's H. J is an on-site "
                      "exchange of the two rails at all sites. All inverse words are literal J,W,J.",
                scope="The supplied minus rail has the reverse propagation order and the transpose of the "
                      "plus walk. Switches at the local coin are common to both rails. T=S X_all relates "
                      "the minus-rail and plus-rail permutations. Neither spatial recurrence nor a negative "
                      "clock tick is used. One logical H moves a parity register to the opposite parity.")


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("directory",type=Path)
    directory = parser.parse_args().directory
    data = main()
    directory.mkdir(parents=True,exist_ok=True)
    (directory/"local_comparison_router.json").write_text(json.dumps(data,separators=(",",":"))+"\n",encoding="utf8")
    print(data["checks"])
    if not all(data["checks"].values()):
        raise SystemExit(1)
