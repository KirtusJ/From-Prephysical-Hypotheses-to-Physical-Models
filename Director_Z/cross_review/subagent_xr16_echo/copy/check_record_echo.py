"""Localized finite record-echo test on eight wires with a private routing bit."""
import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
from check_causal_wires import Line, apply_counts, born, cells, local_fourth, transport


WIDTH = 8
PREP = [
    [(1,5),(0,4),(7,2),(3,6)],
    [(6,1),(5,0),(3,4),(7,2)],
    [(3,5),(4,7),(1,2),(0,6)],
    [(2,7),(0,4),(3,6),(1,5)],
]


def echo_cells(gate):
    kind, pos = gate
    if kind != "pair":
        return cells(gate, WIDTH)
    # At all spectator wires, mix only the private bit and keep the wire fixed.
    spectators = [((2*j,2*j+1),(2*j,2*j+1)) for j in range(WIDTH) if j not in (pos,pos+1)]
    pair = [((2*pos+r,2*(pos+1)+r),(2*pos+r,2*(pos+1)+r)) for r in (0,1)]
    return spectators + pair


def wire_masses(p):
    return [p[2*j]+p[2*j+1] for j in range(WIDTH)]


def snapshot(state, pair):
    v, power, local = state
    square = born(v)
    a, b = pair
    return dict(amplitude_numerators=v, squared_denominator=1<<power,
                born_all=list(map(str,square)), local_fourth_all=list(map(str,local)),
                selected_wire_labels=[a,b],
                born_pair=[str(wire_masses(square)[j]) for j in pair],
                local_fourth_pair=[str(wire_masses(local)[j]) for j in pair])


def advance(state, gate):
    v, power, prev = state
    parts = echo_cells(gate)
    assert sorted(i for s,_ in parts for i in s)==list(range(2*WIDTH))
    assert sorted(i for _,d in parts for i in d)==list(range(2*WIDTH))
    assert all(abs(i//2-j//2)<=1 for s,d in parts for i in s for j in d)
    out, power = apply_counts(v,parts,power)
    local = local_fourth(prev,out,parts)
    for p,q in ((born(v),born(out)), (prev,local)):
        assert sum(q)==1 and all(a>=0 for a in q)
        assert not transport(p,q,parts)[0]
        if gate[0] in ("swap","bit"):
            expected=wire_masses(p)
            if gate[0]=="swap":
                a=gate[1]
                expected[a],expected[a+1]=expected[a+1],expected[a]
            assert expected==wire_masses(q)
        if gate[0]=="pair":
            a=gate[1]
            p_wire,q_wire=wire_masses(p),wire_masses(q)
            assert p_wire[a]+p_wire[a+1]==q_wire[a]+q_wire[a+1]
            assert all(p_wire[j]==q_wire[j] for j in range(WIDTH) if j not in (a,a+1))
    assert all(q==0 for a,q in zip(out,local) if a==0)
    return out,power,local


def native_preparation():
    line=Line(WIDTH)
    for i,pairs in enumerate(PREP):
        line.logical_h(pairs,f"regroup {i+1}")
    assert len(line.gates)==216
    localized=[1]+[0]*(2*WIDTH-1)
    state=localized,0,born(localized)
    for gate in line.gates:
        state=advance(state,gate)
    v,power,p=state
    assert power==4 and v[::2]==[-2,0,-1,1,0,0,3,1] and not any(v[1::2])
    assert p[6]==Fraction(5,656) and p[14]==Fraction(1,16)
    return state


def full_matrix_identity(word):
    for i in range(2*WIDTH):
        source=[int(i==j) for j in range(2*WIDTH)]
        x,power=source,0
        for gate in word:
            x,power=apply_counts(x,echo_cells(gate),power)
        assert power%2==0 and x==[a*(1<<(power//2)) for a in source]


def probe(state, label, a, b):
    assert a<b
    approach = [j for j in range(b-1,a,-1)]
    route = [gate for pos in approach for gate in (("swap",pos),("bit",None))]
    unroute = [gate for pos in reversed(approach) for gate in (("swap",pos),("bit",None))]
    echo=[("pair",a)]*2
    reference=[("bit",None)]*2
    source=state
    stages={"common_query":snapshot(source,(a,b))}
    for gate in route:
        state=advance(state,gate)
    stages["in_place_before"]=snapshot(state,(a,a+1))
    echo_trace=[]
    for j,gate in enumerate(echo):
        state=advance(state,gate)
        echo_trace.append(snapshot(state,(a,a+1)))
    stages["after_first_H"],stages["after_second_H"]=echo_trace
    for gate in unroute:
        state=advance(state,gate)
    stages["final_echo"]=snapshot(state,(a,b))
    idle=source
    for gate in route+reference+unroute:
        idle=advance(idle,gate)
    stages["final_matched_idle"]=snapshot(idle,(a,b))
    assert state[:2]==source[:2]==idle[:2] and source[2]==idle[2]
    before,after=source[2],state[2]
    assert all(before[i]==after[i] for i in range(2*WIDTH) if i//2 not in (a,b))
    assert not any(after[1::2]) and not any(idle[2][1::2])
    full_matrix_identity(route+echo+unroute)
    full_matrix_identity(route+reference+unroute)
    p0=[before[2*a],before[2*b]]
    p1=[Fraction(s) for s in stages["after_first_H"]["local_fourth_pair"]]
    p2=[after[2*a],after[2*b]]
    # First flow F then G. A reciprocal choice G=F^T exists iff pre/post marginals
    # coincide here: the pair transition graph is complete bipartite and both
    # transitions have the same intermediate marginal.
    assert sum(p0)==sum(p1)==sum(p2)
    reciprocal_possible=p0==p2
    distance=sum(abs(x-y) for x,y in zip(before,after))/2
    if label=="original equal positive witness":
        assert p1==[Fraction(23,328),0] and p2==[Fraction(23,656)]*2
        assert distance==Fraction(9,328)
    return dict(case=label,initial_wires=[a,b],outward_adjacent_swaps=approach,
                route_ticks_each_way=len(route),native_echo_ticks=2,depth_from_launch=216+2*len(route)+2,
                all_identity_columns_checked_each_arm=2*WIDTH,
                route_wire_marginal_checks_both_laws_per_arm=2*WIDTH*2*len(route),
                stages=stages,total_variation_local_fourth_echo_vs_idle=str(distance),
                reciprocal_local_fourth_flows_possible=reciprocal_possible,
                reciprocal_born_flows_possible=True)


def run(output):
    state=native_preparation()
    controls=[("original equal positive witness",3,7),("opposite same magnitude",2,3),
              ("unequal live magnitudes",0,6),("single occupied input",1,2),
              ("two empty inputs",4,5)]
    result=dict(source="Localized wire 0, private bit zero. The 216-tick four-layer preparation is "
                       "replayed in full. Every arm uses an identical prefix without intervening measurements.",
                source_logical_layers=PREP,
                instrument="Each adjacent wire permutation P is PH_r followed by H_r. At the echo, H "
                           "acts on the selected two wires separately for each private r while all other "
                           "wires mix their private bits; the next tick repeats this same pairing. The "
                           "matched idle gate mixes private bits on every wire twice. Restore the routing.",
                output_coordinates="Mode 2*j+r represents wire j, private value r. Each snapshot "
                                   "lists all 16 outcomes separately; final comparison uses all launches.",
                controls=[probe(state,name,a,b) for name,a,b in controls],
                premises="Local signed balanced gates and programmed reversible wiring are supplied. "
                         "Per-edge nonnegative flow constrains the direct undisturbed marginals, dark "
                         "output cells are sharp, and an occupied single pair input has a calibrated fair "
                         "split in its surrounding context. Using this echo to infer an earlier equality "
                         "also needs equality of the returned marginal with the direct/matched-idle read "
                         "and no dependence of the shared prefix on its later setting.",
                reciprocal_flow="For two reciprocal H cells, a reverse coupling equal to the transpose of "
                                "the forward coupling suffices locally: its returned marginal reproduces "
                                "the initial one. Merely existing forward supported couplings at each time "
                                "does not require this transpose or identify pre- and post-echo marginals. "
                                "Reciprocal flow is a possible local dynamical assumption; echo readout "
                                "equality needs no particular choice of underlying coupling.")
    output.mkdir(parents=True,exist_ok=True)
    dest=output/"record_echo.json"
    dest.write_bytes((json.dumps(result,indent=1)+"\n").encode())
    print(dest,hashlib.sha256(dest.read_bytes()).hexdigest())


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_directory",type=Path)
    run(parser.parse_args().output_directory)
