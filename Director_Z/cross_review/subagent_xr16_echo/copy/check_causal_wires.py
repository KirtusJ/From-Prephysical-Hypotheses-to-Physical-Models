"""Exact finite-speed wire routing, supported flows and contextual readout controls."""
import argparse
from collections import Counter, defaultdict
from fractions import Fraction
import hashlib
import json
from pathlib import Path


class Line:
    def __init__(self, width):
        self.order = list(range(width))
        self.gates = []
        self.stages = []

    def logical_h(self, pairs, name, masks=()):
        """Route a matching to adjacent physical slots, mix, and reverse the routing."""
        arranged = [i for pair in pairs for i in pair]
        assert sorted(arranged) == self.order
        routes = []
        for j, wanted in enumerate(arranged):
            k = self.order.index(wanted)
            while k > j:
                routes.append(k-1)
                self.order[k-1:k+1] = self.order[k-1:k+1][::-1]
                k -= 1
        start = len(self.gates)
        for k in routes:
            self.gates.extend([("swap", k), ("bit", None)])
        self.gates.append(("logical", None))
        for k in reversed(routes):
            self.gates.extend([("swap", k), ("bit", None)])
        self.order[:] = range(len(arranged))
        self.stages.append((name,start,len(self.gates),pairs,masks))


def cells(gate, width):
    """Each component has two inputs, two ordered outputs and a signed Walsh block."""
    kind, k = gate
    if kind == "logical":
        return [((2*x+r,2*x+2+r),(2*x+r,2*x+2+r))
                for x in range(0,width,2) for r in range(2)]
    return [((2*x,2*x+1),(2*y,2*y+1)) for x in range(width)
            for y in [k+1 if kind == "swap" and x == k else
                      k if kind == "swap" and x == k+1 else x]]


def apply_counts(v, parts, depth):
    out = [0]*len(v)
    for (a,b),(c,d) in parts:
        out[c], out[d] = v[a]+v[b], v[a]-v[b]
    depth += 1
    if depth >= 2 and all(x%2 == 0 for x in out):
        return [x//2 for x in out], depth-2
    return out, depth


def born(v):
    total = sum(a*a for a in v)
    return [Fraction(a*a,total) for a in v]


def fourth(v):
    total = sum(a**4 for a in v)
    return [Fraction(a**4,total) for a in v]


def local_fourth(previous, v, parts):
    out = [Fraction(0)]*len(previous)
    for (a,b),(c,d) in parts:
        weight = previous[a]+previous[b]
        norm = v[c]**4+v[d]**4
        if norm:
            out[c] = weight*Fraction(v[c]**4,norm)
            out[d] = weight-out[c]
        else:
            assert weight == 0
    return out


def transport(before, after, parts):
    """Build actual nonnegative edge flows; report any infeasible component mass."""
    violations, count = [], 0
    for (a,b),(c,d) in parts:
        if before[a]+before[b] != after[c]+after[d]:
            violations.append((a,b,c,d,str(before[a]+before[b]),str(after[c]+after[d])))
            continue
        z = min(before[a],after[c])
        ac,ad,bc,bd = z,before[a]-z,after[c]-z,before[b]-after[c]+z
        assert min(ac,ad,bc,bd) >= 0 and (ac+bc,ad+bd) == (after[c],after[d])
        assert (ac+ad,bc+bd) == (before[a],before[b])
        count += sum(int(f>0) for f in (ac,ad,bc,bd))
    return violations,count


def word_columns(width, pairs):
    """Verify the exact logical matrix on all 2*width basis inputs including private bit 1."""
    line = Line(width)
    line.logical_h(pairs,"arbitrary matching")
    limits = Counter()
    for j in range(2*width):
        v = [int(i==j) for i in range(2*width)]
        depth = 0
        for gate in line.gates:
            parts = cells(gate,width)
            for sources,targets in parts:
                limits[max(abs(s//2-d//2) for s in sources for d in targets)] += 1
            v,depth = apply_counts(v,parts,depth)
        expected = [0]*len(v)
        for a,b in pairs:
            if j//2 in (a,b):
                expected[2*a+j%2] = 1
                expected[2*b+j%2] = 1 if j//2 == a else -1
        assert depth==1 and v==expected
    assert max(limits)<=1
    return dict(width=width, columns=2*width, ticks=len(line.gates), ordered_pairs=pairs,
                all_columns_exact=True, maximum_step_distance=max(limits))


def program():
    # x=(2,1,1,1,1,0,0,0)/sqrt(8); y is uniform. All named pair orders matter.
    x1 = [(0,1),(2,3),(4,5),(6,7)]
    x2 = [(0,2),(1,3),(4,5),(6,7)]
    x3 = [(0,1),(2,5),(3,6),(4,7)]
    y1 = [(0,1),(2,3),(4,5),(6,7)]
    y2 = [(0,2),(1,3),(4,6),(5,7)]
    y3 = [(0,4),(1,5),(2,6),(3,7)]
    xprep = [x1,x2,x3]
    yprep = [y1,y2,y3]
    width = 16
    line = Line(width)
    for i,pairs in enumerate(xprep):
        line.logical_h(pairs+[(8+a,8+b) for a,b in y1],f"target prep {i+1}")
    target_stage = len(line.stages)
    selector = [(i,8+i) for i in range(8)]
    line.logical_h(selector,"duplicate target",selector)
    active = list(reversed(xprep))+yprep
    for i,pairs in enumerate(active):
        # Arrange A adjacent by pairs but override its H below to act on private
        # bit at the original wire. It then returns blank after six logical Hs.
        line.logical_h(y1+[(8+a,8+b) for a,b in pairs],f"mixed comparison {i+1}",
                       [(j,) for j in range(8)]+[tuple(range(8,16))])
        # The arranger never moves an A wire here; mark H at adjacent B slots only.
        start,end=line.stages[-1][1:3]
        h=next(j for j in range(start,end) if line.gates[j][0]=="logical")
        line.gates[h]=("mixed",None)
    return line,target_stage


def physical_cells(gate,width):
    if gate[0] != "mixed":
        return cells(gate,width)
    return [((2*i,2*i+1),(2*i,2*i+1)) for i in range(8)] + [
        ((2*i+r,2*i+2+r),(2*i+r,2*i+2+r)) for i in range(8,width,2) for r in (0,1)]


def protected_follow(masks, parts):
    following=[]
    for mask in masks:
        dst=set()
        for sources,targets in parts:
            membership=[s in mask for s in sources]
            assert membership[0]==membership[1]
            if membership[0]:
                dst.update(targets)
        following.append(dst)
    return following


def trial():
    line,target_stage=program()
    width=16
    v=[1]+[0]*(2*width-1)
    depth=0
    local=born(v)
    snapshots=[]
    edge_counts=Counter()
    max_speed=0
    failed=[]
    target_probs={}
    for stage_index,(name,start,end,_pairs,subjects) in enumerate(line.stages):
        masks=[{2*j+r for j in cols for r in (0,1)} for cols in subjects]
        for t in range(start,end):
            parts=physical_cells(line.gates[t],width)
            assert sorted(a for ss,_ in parts for a in ss)==list(range(2*width))
            assert sorted(a for _,ds in parts for a in ds)==list(range(2*width))
            speed=max(abs(s//2-d//2) for ss,ds in parts for s in ss for d in ds)
            max_speed=max(max_speed,speed)
            assert speed<=1
            prev,global_prev=born(v),fourth(v)
            v,depth=apply_counts(v,parts,depth)
            now,global_now=born(v),fourth(v)
            local_now=local_fourth(local,v,parts)
            assert sum(local_now)==1 and all(not p or value!=0 for p,value in zip(local_now,v))
            next_masks=protected_follow(masks,parts)
            for p,q,rule in ((prev,now,"Born"),(local,local_now,"local_fourth")):
                errors,nonzero=transport(p,q,parts)
                assert not errors, (name,rule,errors)
                edge_counts[rule]+=nonzero
                for a,b in zip(masks,next_masks):
                    assert sum(p[j] for j in a)==sum(q[j] for j in b)
                    edge_counts["protected_equalities_"+rule]+=1
            errors,_=transport(global_prev,global_now,parts)
            if errors:
                failed.append(dict(tick=t+1,stage=name,component_count=len(errors),first=errors[0]))
            local=local_now
            masks=next_masks
        assert masks==[{2*j+r for j in cols for r in (0,1)} for cols in subjects]
        assert sum(a*a for a in v)==1<<depth
        if stage_index+1 in (target_stage,target_stage+1,len(line.stages)):
            snapshots.append(dict(stage=name,tick=end,depth=depth,numerators=v.copy(),
                                  born=list(map(str,born(v))),local_fourth=list(map(str,local))))
        if stage_index+1==target_stage:
            target_probs=dict(Born=list(map(str,born(v))),local_fourth=list(map(str,local)))
    groups=defaultdict(list)
    for i,a in enumerate(v):
        if a:
            groups[a].append(i)
    unequal=[]
    for a,indices in groups.items():
        for j in indices:
            for k in indices:
                if j<k and local[j]!=local[k]:
                    unequal.append(dict(numerator=a,physical_modes=[j,k],weights=[str(local[j]),str(local[k])]))
    target=snapshots[0]["numerators"]
    assert sorted(target)==[0]*27+[1]*4+[2]
    assert v[:16]==target[:16] and v[16:]==[1,0]*8 and depth==4
    return dict(logical_wires=width,physical_modes=2*width,native_ticks=len(line.gates),
                stage_timetable=[dict(name=n,from_tick=s,to_tick=e,protected_wire_sets=m)
                                 for n,s,e,_,m in line.stages], maximum_step_distance=max_speed,
                counts=dict(edge_counts),snapshots=snapshots,target=target_probs,
                local_fourth_final_equal_live_disparities=unequal,
                global_fourth_flow_violations=failed)


def regrouping_control():
    """Regroup a pair of amplitudes of unequal sizes; keep the fair-quartet control separate."""
    line = Line(8)
    layers = [[(1,5),(0,4),(7,2),(3,6)],[(6,1),(5,0),(3,4),(7,2)],
              [(3,5),(4,7),(1,2),(0,6)],[(2,7),(0,4),(3,6),(1,5)]]
    for j, pairs in enumerate(layers):
        line.logical_h(pairs,f"regroup {j+1}")
    v,depth=[1]+[0]*15,0
    local=born(v)
    failures=[]
    for t,gate in enumerate(line.gates):
        parts=cells(gate,8)
        gprev=fourth(v)
        v,depth=apply_counts(v,parts,depth)
        new=local_fourth(local,v,parts)
        assert not transport(local,new,parts)[0]
        assert all(not p or a for p,a in zip(new,v))
        local=new
        errors,_=transport(gprev,fourth(v),parts)
        if errors:
            failures.append(dict(tick=t+1,components=errors))
    a,b=6,14
    assert (depth,v[a],v[b],local[a],local[b])==(4,1,1,Fraction(5,656),Fraction(1,16))
    assert failures
    return dict(ordered_layers=layers,ticks=len(line.gates),numerators=v,depth=depth,
                local_fourth=list(map(str,local)),global_fourth=list(map(str,fourth(v))),
                equal_live_witness=dict(modes=[a,b],same_amplitude="1/4",
                                        distinct_local_probabilities=[str(local[a]),str(local[b])]),
                global_fourth_flow_violations=failures)


def fringe():
    # Both input rays have (1/2,1/2) position/coin marginals, and nonnegative
    # supported couplings exist separately. A single stochastic kernel would
    # have to send this one input marginal to two distinct outputs.
    cases=[]
    for a,b in ((1,1),(1,-1),(2,1)):
        first=[a,b]
        after=[a+b,a-b]
        again=[after[0]+after[1],after[0]-after[1]]
        u=Fraction(2*a*b,a*a+b*b)
        g=Fraction(1,2)+u/(1+u*u)
        assert fourth(after)[0]==g and fourth(again)==fourth(first)
        cases.append(dict(input=[a,b],born_input=list(map(str,born(first))),
                          born_output=list(map(str,born(after))),fourth_output=list(map(str,fourth(after))),
                          fringe_contrast=str(u),fourth_H2_reset=list(map(str,fourth(again)))))
    return cases


def main(output):
    result=dict(model="A line of wires, a private two-state bit on every wire, a programmed finite "
                      "clock and local signed balanced scatterers. The wire/bit output basis is read. "
                      "A neighboring wire swap P is implemented as (P H_bit) then H_bit; every tick "
                      "has two signed edges per input, with disjoint two-input/two-output cells.",
                premise="The marginals for each unmeasured clock phase have a nonnegative coupling "
                        "on the actual single-step edges. It may depend on the full state and controls. "
                        "This logical condition does not identify a measured pair of times with the "
                        "undisturbed marginals or supply a physical apparatus.",
                circuit=trial(),direct_matching=word_columns(8,[(0,7),(5,1),(6,2),(3,4)]),
                fourth_power_regrouping=regrouping_control(),
                sign_sensitive_H=fringe(),
                boundaries="Local per-block fourth-power normalization admits supported couplings "
                           "and sharp zeros but breaks active equal-entry symmetry across cells. "
                           "Global fourth-power normalization has equal leaves and sharp zeros but "
                           "can violate edge-supported mass conservation. A single common Markov "
                           "kernel for all coherent inputs cannot implement the H fringe.")
    output.mkdir(parents=True,exist_ok=True)
    dest=output/"causal_wires.json"
    dest.write_bytes((json.dumps(result,indent=1)+"\n").encode())
    print(dest,hashlib.sha256(dest.read_bytes()).hexdigest())


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_directory",type=Path)
    main(parser.parse_args().output_directory)
