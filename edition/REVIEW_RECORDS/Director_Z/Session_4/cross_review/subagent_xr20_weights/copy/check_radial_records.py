"""All-outcome interferometer, including timeout mass and a shared-sheet Bell source."""

import argparse
import csv
import json
from collections import defaultdict
from itertools import product
from math import pi, sqrt
from pathlib import Path

import numpy as np


H = np.array([[1,1],[1,-1]],complex)/sqrt(2)
Z = np.diag([1.,-1.])
X = np.array([[0.,1.],[1.,0.]])
Y = np.array([[0.,-1j],[1j,0.]])


def matrix_for_run(radii, order):
    phase = np.exp(-2j*pi/order)
    result = np.zeros((2,2),complex)
    for arm in (1,-1):
        col = 0 if arm == 1 else 1
        sign = 1
        gain = arm*sum(radii[:-1])
        direction = arm
        for last, current in zip(radii[1:], radii[2:]):
            next_direction = arm*(current-last)
            if direction == next_direction == -1:
                sign *= -1
            direction = next_direction
        result[int(direction==-1),:] = sign*phase**(gain%order)*H[col,:]
    return result


def exhaustive(order, radius, max_ticks):
    phase = np.exp(-2j*pi/order)
    size = 2*radius
    def propagate(state):
        out = defaultdict(lambda:np.zeros(2,complex))
        for (x,c),v in state.items():
            for d in (-1,1):
                out[((x+d)%size,d)] += v*phase**(x%order)*(-1 if c==d==-1 else 1)/sqrt(2)
        return out
    rows = []
    for start in (0,radius):
        def visit(path,state):
            r=path[-1]
            t=len(path)-1
            ended=t>0 and r in (0,radius)
            if ended or t==max_ticks:
                matrix=np.stack(list(state.values()))
                pr=2.**(1-t)
                gram=np.linalg.norm(matrix.conj().T@matrix-pr*np.eye(2))
                mismatch=None
                if ended:
                    x=(start+r)%size
                    normalized=np.stack([state[(x,c)] for c in (1,-1)])/sqrt(pr)
                    mismatch=float(np.linalg.norm(normalized-matrix_for_run(path,order)))
                rows.append(dict(start=start,path=",".join(map(str,path)),arrived=ended,ticks=t,
                                 probability=pr,gram_error=float(gram),matrix_error=mismatch))
                return
            groups=defaultdict(dict)
            for (x,c),v in propagate(state).items():
                d=(x-start)%size
                groups[min(d,size-d)][(x,c)]=v
            for d,next_state in groups.items():
                visit(path+[d],next_state)
        visit([0],{(start,1):np.array([1,0],complex),(start,-1):np.array([0,1],complex)})
    return rows


def draw_excursion(rng, order, radius, bank, remaining):
    path=[0,1]
    while path[-1] not in (0,radius) and len(path)-1<remaining:
        path.append(path[-1]+(1 if rng.integers(2) else -1))
    if path[-1] not in (0,radius):
        return None, len(path)-1
    # Only finitely many signed arm permutations (modulo global phase).
    angle=sum(path[:-1]) % order
    plus_directions=np.diff(path)
    left_after_left=int(np.sum((plus_directions[:-1]==-1)&(plus_directions[1:]==-1)))
    right_after_right=int(np.sum((plus_directions[:-1]==1)&(plus_directions[1:]==1)))
    key=(angle,int(plus_directions[-1]),left_after_left%2,right_after_right%2)
    if key not in bank:
        bank[key]=matrix_for_run(path, order)
    return bank[key],len(path)-1


def bloch(matrix):
    observable=matrix.conj().T@Z@matrix
    return np.array([np.trace(observable@p).real/2 for p in (X,Y,Z)])


def finite_horizon(order, radius, seed, eta, deadline, runs):
    rng=np.random.default_rng(seed)
    targets={"Z":np.array([0.,0.,1.]),"X":np.array([1.,0.,0.]),"Y":np.array([0.,1.,0.]),
             "oblique":np.array([2.,3.,1.])/sqrt(14)}
    bank={}
    rows=[]
    for name,target in targets.items():
        for i in range(runs):
            frame=np.eye(2,dtype=complex)
            ticks=0
            completed=0
            axis=bloch(frame)
            while np.linalg.norm(axis-target)>eta and ticks<deadline:
                gate,duration=draw_excursion(rng,order,radius,bank,deadline-ticks)
                ticks+=duration
                if gate is None:
                    break
                completed+=1
                frame=gate@frame
                axis=bloch(frame)
            success=np.linalg.norm(axis-target)<=eta
            rows.append(dict(target=name,trial=i,ticks=ticks,completed=completed,hit=bool(success),
                             axis_error=float(np.linalg.norm(axis-target)),fallback_plus=int(not success)))
    stats={}
    for name,target in targets.items():
        subset=[r for r in rows if r["target"]==name]
        success=sum(r["hit"] for r in subset)
        stats[name]=dict(hits=success,timeouts=runs-success,mean_ticks=sum(r["ticks"] for r in subset)/runs)
    return rows,stats


def bell_source(order):
    phase=np.exp(-2j*pi/order)
    # Actual integer path counts: retain a destructive three-step record of A
    # on three sheets, starting on a localized sheet and R. Shift of B is off.
    source=defaultdict(int)
    for path in product((1,-1),repeat=3):
        x=sheet=0
        c=1
        sign=1
        for d in path:
            sheet=(sheet+x)%order
            sign*= -1 if c==d==-1 else 1
            x+=d
            c=d
        if (x,c)==(-1,-1):
            source[sheet]+=sign
    filtered_probability=sum(v*v for v in source.values())/8
    # Both inputs R, origins aligned (route after the sheet record).
    output=defaultdict(int)
    for (a,b),sheet in product(product((1,-1),repeat=2),range(order)):
        # One split per walker, then enforce the joint coherent return.
        # The contact acts once at the intervening departure, while x1+x2
        # supplies the two self phases. Changing directions never yields LL.
        output[(-a,-b,(sheet+a+b+int(a==b))%order)]+=source[sheet]
    total=sum(v*v for v in output.values())
    density=np.zeros((4,4),complex)
    for k in range(order):
        vec=np.array([output.get((a,b,k),0) for a,b in product((1,-1),repeat=2)])
        density+=np.outer(vec,vec)/total
    coeff=np.array([[phase**(a+b+int(a==b))/2 for b in (-1,1)] for a in (-1,1)])
    tagged=coeff.reshape(-1)
    # Tracing sheets is a mixture. Measurements on the chosen real plane
    # conjugate with their sector; only real observables can use this density alone.
    mixture=(np.outer(tagged,tagged.conj())+np.outer(tagged.conj(),tagged))/2
    return dict(raw_filtered_mass=filtered_probability,conditional_contact_gate_mass=total/(16*sum(v*v for v in source.values())),
                zero_mode_mass=abs(sum(source.values()))**2,
                mixture_error=float(np.linalg.norm(density-mixture)),
                concurrence=float(2*abs(np.linalg.det(coeff))),ideal_max_chsh=float(2*sqrt(1+4*abs(np.linalg.det(coeff))**2)))


def main(directory):
    directory.mkdir(parents=True,exist_ok=True)
    order,radius=3,6
    exact=exhaustive(order,radius,10)
    raw,stats=finite_horizon(order,radius,41729,0.63,180,64)
    with (directory/"radial_trials.csv").open("w",encoding="utf8",newline="") as f:
        w=csv.DictWriter(f,list(raw[0]));w.writeheader();w.writerows(raw)
    source=bell_source(order)
    sums=[sum(r["probability"] for r in exact if r["start"]==x) for x in (0,radius)]
    checks=dict(whole_tree=sums==[1.,1.],branch_gram=max(r["gram_error"] for r in exact)<2e-14,
                all_return_matrices=max(r["matrix_error"] for r in exact if r["arrived"])<2e-12,
                all_trials=(len(raw)==256 and all(v["hits"]+v["timeouts"]==64 for v in stats.values())),
                event_ready_source=(source["raw_filtered_mass"]==.25 and source["conditional_contact_gate_mass"]==.25 and
                                    source["zero_mode_mass"]==0 and source["mixture_error"]<2e-14))
    report=dict(checks=checks,first_excursion_tree=exact,tree_probability_totals=sums,source=source,
                sampling=dict(seed=41729,axis_tolerance=.63,deadline_ticks=180,trials_per_setting=64,statistics=stats,
                              scope="Logical-frame simulation and fixed binary fallback; no Bell data or confidence bound."))
    (directory/"radial_records.json").write_text(json.dumps(report,indent=2,allow_nan=False)+"\n",encoding="utf8")
    print(checks,stats)
    if not all(checks.values()):
        raise SystemExit(1)


if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("output",type=Path)
    main(p.parse_args().output)
