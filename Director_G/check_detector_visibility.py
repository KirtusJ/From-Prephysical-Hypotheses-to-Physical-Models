"""Reproduce native detector controls, exact false passes and terminal sign repair."""
import argparse
from fractions import Fraction as F
import json
from pathlib import Path


def check(condition, reason):
    if not condition:
        raise ValueError(reason)


def to_json(obj):
    if isinstance(obj, F):
        return str(obj)
    raise TypeError(type(obj).__name__)


def phase_bias(x, t):
    return [1, 0, x, 1-x*x][t]


def count_bias(t):
    return int(t == 0)


def readout(cases, t):
    """Each row is (mass, cosine or None for count, R column, L column)."""
    n = len(cases[0][2])
    out = [F(0)]*n
    for mass, x, r, l in cases:
        check(len(r)==len(l)==n and sum(r)==sum(l)==1 and min(*r,*l)>=0,
              "invalid channel")
        b = count_bias(t) if x is None else phase_bias(x,t)
        p = (1+F(b))/2
        for j in range(n):
            out[j] += mass*(p*r[j]+(1-p)*l[j])
    check(sum(out)==1, "all launches counted")
    return out


def invert(y, u, b):
    return None if u==b else (y-b)/(u-b)


def record(name, even, odd, coordinate, m):
    rows = [[readout(cases,t) for t in range(4)] for cases in (even,odd)]
    obs = [rows[t%2][t][coordinate] for t in range(4)]
    biases = [invert(rows[t%2][t][coordinate],rows[t%2][0][coordinate],
                     rows[t%2][1][coordinate]) for t in (2,3)]
    score = None if None in biases else 1-biases[1]-2*m*biases[0]+m*m
    return dict(name=name, all_reports=rows, used_event=coordinate, raw_test=obs,
                recovered=biases, score=score)


def stochastic_binary(v):
    return ((1+F(v))/2,(1-F(v))/2), ((1-F(v))/2,(1+F(v))/2)


def two_phases(c, ev, od):
    masses = [(F(1,2),F(-1)),(F(1,2),F(0))]
    even=[(*row,*stochastic_binary(v)) for row,v in zip(masses,ev)]
    odd=[(*row,*stochastic_binary(v)) for row,v in zip(masses,od)]
    return record(c,even,odd,0,-F(1,2))


def meter(ensemble, twirl, toggle_probability=F(1,2)):
    """Return per-launch effect probabilities, directly propagating Bloch triples."""
    totals = [F(0)]*4
    trajectories = []
    for mass, cos, sin in ensemble:
        check(cos*cos+sin*sin==1, "phase norm")
        x,y,z=0,0,1
        states=[]
        for t in range(4):
            states.append([x,y,z])
            # E is 1/5 the Y+ outcome and 4/5 the Z+ outcome.
            y_read = (1-2*toggle_probability)*y if twirl else y
            totals[t]+=mass*(F(1,2)+(y_read+4*z)*F(1,10))
            x,y,z=cos*z+sin*y,sin*z-cos*y,x
        trajectories.append(states)
    return totals,trajectories


def meter_score(rates,m):
    u,b,y2,y3=rates
    score=1-invert(y3,u,b)-2*m*invert(y2,u,b)+m*m
    scaled=(1+m*m)*u+(2*m-m*m)*b-2*m*y2-y3
    check(scaled==(u-b)*score,"undivided witness")
    return score


def run():
    m=-F(1,2)
    true_r = (F(3,5),F(1,10),F(3,10))
    true_l = (F(1,8),F(3,8),F(1,2))
    swapped_r = (F(1,4),F(1,4),F(1,2))
    swapped_l = (F(5,8),F(1,8),F(1,4))
    cases=[]
    for name,x,c in [('cubic',m,0),('trivial',F(1),0),('pure_count',0,1),
                     ('mixture',F(1,5),F(2,7))]:
        def make(r,l):
            return [(1-F(c),x,r,l),(F(c),None,r,l)]
        row=record(name,make(true_r,true_l),make(swapped_r,swapped_l),0,m)
        check(row['score']==(1-c)*(x-m)**2+c*(1+m*m), "different well calibration")
        cases.append(row)
    blind=[(F(1),F(1),true_r,true_r)]
    row=record('no contrast',blind,blind,0,m)
    check(row['score'] is None,"blind denominator")
    cases.append(row)
    false=[(F(w,10),F(x),*stochastic_binary(F(v))) for w,x,v in
           [(3,-1,1),(6,0,1),(1,1,-1)]]
    row=record('signed visibility',false,false,0,m)
    check(row['score']==0,"signed fake")
    cases.append(row)
    for settings, expected in [(([1,1],[F(1,3),1]),0),
                               (([1,1],[1,1]),F(1,4)),
                               (([F(1,3),1],[F(1,3),1]),F(1,4))]:
        row=two_phases('different weights' if expected==0 else 'one fixed detector',*settings)
        check(row['score']==expected,"common visibility")
        cases.append(row)
    phases=[(F(1,5),-1,0),(F(4,5),0,1)]
    original,states=meter(phases,False)
    repaired,_=meter(phases,True)
    check(original==[F(x,50) for x in [45,29,21,41]],"coherent fake")
    check(repaired==[F(x,50) for x in [45,25,21,41]],"fair sign toggle")
    check(meter_score(original,m)==0 and meter_score(repaired,m)==F(1,4),"toggle witness")
    biased,_=meter(phases,True,F(1,4))
    # Coherence at tick one survives an asymmetric switch.
    check(biased!=repaired,"biased toggle")
    # The cubic phase needs no square roots after the toggle: its population
    # alone is used with the effect diagonal (9/10, 1/10).
    target=[F(1,2)+F(2,5)*phase_bias(m,t) for t in range(4)]
    check(meter_score(target,m)==0,"positive control")
    bounds=[]
    for sign in (-1,1):
        delta=F(sign,1000)
        u,b,y=original[:3]
        bhat=invert(y+delta,u-delta,b+2*delta)
        err=abs(bhat-invert(y,u,b))
        limit=(abs(delta)+2*abs(2*delta)+abs(delta))/abs(u-delta-b-2*delta)
        check(err<=limit,"raw-error bound")
        bounds.append(dict(perturbation=delta,error=err,limit=limit))
    return dict(report_order=['A','B','miss'],calibrations=cases,phase_trajectories=states,
                unswitched=original,fair_switch=repaired,biased_switch=biased,
                biased_score=meter_score(biased,m),pure_target=target,
                pure_target_score=meter_score(target,m),error_controls=bounds)


if __name__=="__main__":
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("directory",type=Path)
    out=ap.parse_args().directory
    out.mkdir(parents=True,exist_ok=True)
    with (out/"detector_visibility.json").open("x",encoding="utf8",newline="\n") as handle:
        json.dump(run(),handle,default=to_json,indent=2,allow_nan=False)
        handle.write("\n")
