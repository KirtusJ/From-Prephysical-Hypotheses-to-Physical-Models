"""Fixed signed sheet lift: literal paths, exact sector support and pointer controls."""

import argparse
import csv
import json
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import product
from math import comb
from pathlib import Path

from check_relative_transport import mass, record


def link(x, p, carrier):
    x %= 2*p
    if carrier == "static":
        # Integrate on the two parity cycles, with g(0)=g(1)=0.
        if x % 2 == 0:
            return 0, (x//2) % p
        n = x//2
        return n % p, (-n*(n+1)//2) % p
    if carrier == "quadratic":
        return x % p, x*x % p
    return x % p, 2*x % p


def propagate(state, steps, p, carrier):
    for _ in range(steps):
        out = defaultdict(int)
        for (x,c,y,z), amp in state.items():
            a,b = link(x, p, carrier)
            for d in (-1,1):
                dest = ((x+d) % (2*p), d, (y+a) % p, (z+b) % p)
                out[dest] += -amp if c == d == -1 else amp
        state = out
    return state


def destructive_block(p, x, c, carrier):
    return record(propagate({(x,c,0,0): 1}, 3, p, carrier),
                  (x-c) % (2*p), -c)


def annihilates(state, p, r, s):
    # A polynomial of degree <p vanishes at a primitive p-th root iff
    # its coefficients are constant. This also handles the zero character.
    sums = [0]*p
    for (_,_,y,z), amp in state.items():
        sums[(r*y+s*z) % p] += amp
    return len(set(sums)) == 1


def diamond(p, x, carrier):
    a,b = link(x+1, p, carrier)
    c,d = link(x-1, p, carrier)
    return (a-c) % p,(b-d) % p


def route(p, state, site):
    x,c = next(iter(state))[:2]
    distance = (site-x) % (2*p)
    d = 1 if distance <= p else -1
    length = min(distance,2*p-distance)
    for _ in range(length):
        x,c = (x+d) % (2*p),d
        state = record(propagate(state,1,p,"static"),x,c)
    return state,length


def prepare(p,target):
    state = {(0,1,0,0):1}
    routing_steps = 0
    for centre in [1]+[2*j for j in range(p) if j != target]:
        state,length = route(p,state,centre)
        routing_steps += length
        x,c = next(iter(state))[:2]
        state = record(propagate(state,3,p,"static"),(x-c)%(2*p),-c)
    pos,c = next(iter(state))[:2]
    cosets = [[state.get((pos,c,y,(j-target*y)%p),0) for y in range(p)] for j in range(p)]
    profile = [values[0] for values in cosets]
    support = [j for j in range(p) if profile[j]]
    # The vertical difference is one in place of two in the switched carrier.
    correct = (all(len(set(v)) == 1 for v in cosets) and
               sorted(profile) == [-1]+[0]*(p-2)+[1] and
               (support[1]-support[0]) % p in (1,p-1) and mass(state) == 2*p)
    probes=[]
    for j in range(p):
        before,_ = route(p,state,2*j)
        x,c = next(iter(before))[:2]
        after = record(propagate(before,3,p,"static"),(x-c)%(2*p),-c)
        observed = Fraction(mass(after),8*mass(before))
        d=(target-j)%p
        predicted = Fraction(0) if not d else Fraction(3,8) if d in (1,p-1) else Fraction(1,4)
        probes.append(dict(j=j,conditional=str(observed),correct=(observed==predicted)))
    return dict(target=target, deterministic_routing_steps=routing_steps, counts=profile,
                prepared=correct, fixed_route_joint=str(Fraction(mass(state),2**routing_steps*8**p)),
                all_routes_joint=str(Fraction(mass(state),8**p)),probes=probes)


def horizontal_filter(p, target):
    # Strip known translations, then compose all horizontal differences except one.
    counts = {(0,0): 1}
    half = (p+1)//2
    for j in range(p):
        if j == target:
            continue
        a,b = half, -j*half
        out = defaultdict(int)
        for (y,z), val in counts.items():
            out[(y+a)%p,(z+b)%p] += val
            out[(y-a)%p,(z-b)%p] -= val
        counts = out
    return {(0,1,y,z):v for (y,z),v in counts.items()}


def single_setting_support(p):
    rows = []
    for target in range(p):
        line = {(target*s % p,s) for s in range(1,p)}
        state = horizontal_filter(p,target)
        support = {(r,s) for r,s in product(range(p),repeat=2) if not annihilates(state,p,r,s)}
        vertical = {(r,0) for r in range(1,p)}
        g = [0]*p
        n = p-1
        for k in range(n+1):
            g[((n-2*k)*((p+1)//2)) % p] += (-1)**k*comb(n,k)
        total = mass(state)
        # Parseval on the target line gives p-1; on s=0 it gives sum(g_y^2)/p.
        expected = Fraction(p-1)+Fraction(sum(a*a for a in g),p)
        rows.append(dict(target=target, mass=total, decomposed_mass=str(expected),
                         target_weight=str(Fraction(p-1,total)), retained_vertical=len(vertical & support),
                         agrees=(support == line | vertical and total == expected)))
    return rows


def pointer_control():
    # At gain zero two histories cancel in the destructive output.
    # Copying the first direction into a distinct endpoint register destroys the cancellation.
    def history_counts(copy, erase):
        state={(0,1,0):1}
        for k in range(3):
            out=defaultdict(int)
            for (x,c,b),amp in state.items():
                for d in (-1,1):
                    bit = b ^ int(copy and k == 0 and d == -1)
                    # At step two the first departure sign is still determined by x.
                    if erase and k == 1 and x == -1:
                        bit ^= 1
                    out[(x+d,d,bit)] += -amp if d == c == -1 else amp
            state=out
        return [state.get((-1,-1,b),0) for b in (0,1)]
    return {k:history_counts(a,b) for k,a,b in (("blank",False,False),
            ("retained",True,False),("reversibly_uncomputed",True,True))}


def explore_flags():
    p=5
    state=propagate({(0,1,0,0):1},2,p,"static")
    yes={key:v for key,v in state.items() if key[:2]==(2,1)}
    other={key:v for key,v in state.items() if key[:2]!=(2,1)}
    def histogram(vector):
        return dict(sorted(Counter(abs(v) for v in vector.values() if v).items()))
    rows=[]
    for steps in range(4):
        h=histogram(yes)
        k=histogram(other)
        odds=[str(Fraction(sum(a*n**exponent for n,a in h.items()),
                            sum(a*n**exponent for n,a in k.items()))) for exponent in (1,2,4)]
        rows.append(dict(extra_steps=steps,yes=h,other=k,flag_odds_L1_L2_L4=odds))
        yes,other=propagate(yes,1,p,"static"),propagate(other,1,p,"static")
    return rows


def magnitude_ranges(writer):
    """All endpoint counts for the first 24 step depths of this small lift."""
    state={(0,1,0,0):1}
    reports=[]
    for t in range(1,25):
        state=propagate(state,1,5,"static")
        for x,c,y,z in product(range(10),(-1,1),range(5),range(5)):
            writer.writerow((t,x,c,y,z,state.get((x,c,y,z),0)))
        reports.append(dict(t=t, histogram=dict(sorted(Counter(abs(v) for v in state.values() if v).items())),
                            total=mass(state), expected=2**t))
    return reports


def corridor(p, carrier, largest_n):
    period = 2*p
    state = {(0,1,0,0):1}
    rows = []
    for t in range(1,2+period*largest_n):
        evolved = propagate(state,1,p,carrier)
        lead = t % period
        trail = (t-2) % period
        state = {k:v for k,v in evolved.items() if v and
                 (k[:2] == (lead,1) or k[0] == trail and (k[1] == 1 or lead == 1))}
        if t<=1 or lead!=1:
            continue
        n=(t-1)//period
        merging={k:v for k,v in state.items() if k[0]==trail}
        spectator={k:v for k,v in state.items() if k[0]==lead}
        after=propagate(merging,1,p,carrier)
        other=propagate(spectator,1,p,carrier)
        sheet_positions={(k[2],k[3]) for k in merging}
        hist=lambda vec: sorted(abs(v) for v in vec.values() if v)
        correct=(hist(merging)==[1,n] and len(sheet_positions)==1 and
                 hist(spectator)==[1] and hist(other)==[1,1] and
                 hist(after)==[v for v in (n-1,n+1) if v])
        rows.append(dict(p=p,carrier=carrier,n=n,t=t,merging=hist(merging),
                         merging_later=hist(after),spectator_later=hist(other),
                         common_sheet=sorted(sheet_positions),unconditional_count=mass(state),agrees=correct))
    return rows


def main(output):
    output.mkdir(parents=True, exist_ok=True)
    checks = dict(diamond_difference=True, all_native_nulls=True, affine_obstruction=True,
                  incomplete_menu_support=True, finite_preparation=True, followup_probabilities=True,
                  routing_hitting_equations=True)
    trials = []
    with (output/"fixed_transport.csv").open("w",encoding="utf8",newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(("p","carrier","centre","incoming","r","s","dark","predicted_dark"))
        for p in (3,5,7,11,13):
            for carrier in ("static","quadratic","linear"):
                for x,c in product(range(2*p),(-1,1)):
                    a,b = diamond(p,x,carrier)
                    expected = {"static":(0,1) if x%2 else (1,(-x//2)%p),"quadratic":(2%p,4*x%p),
                                "linear":(2%p,4%p)}[carrier]
                    checks["diamond_difference"] &= (a,b) == expected
                    state=destructive_block(p,x,c,carrier)
                    for r,s in product(range(p),repeat=2):
                        dark=annihilates(state,p,r,s)
                        prediction=(r*a+s*b)%p==0
                        checks["all_native_nulls"] &= dark==prediction
                        writer.writerow((p,carrier,x,c,r,s,int(dark),int(prediction)))
            supports = single_setting_support(p)
            checks["incomplete_menu_support"] &= all(row["agrees"] for row in supports)
            affine = propagate({(0,1,0,0):1},2*p+3,p,"linear")
            checks["affine_obstruction"] &= all((z-2*y)%p == 0 for (_,_,y,z),v in affine.items() if v)
            words=[prepare(p,u) for u in range(p)]
            checks["finite_preparation"] &= all(w["prepared"] for w in words)
            checks["followup_probabilities"] &= all(row["correct"] for w in words for row in w["probes"])
            expected_times=[j*(2*p-j) for j in range(2*p+1)]
            checks["routing_hitting_equations"] &= all(2*expected_times[j]==2+expected_times[j-1]+expected_times[j+1]
                                                       for j in range(1,2*p))
            trials.append(dict(prime=p,partial_filter=supports,static_filtered_words=words,mean_hitting_times=expected_times))
    pointer=pointer_control()
    checks["record_and_eraser"] = (sum(v*v for v in pointer["retained"])==2 and
                                   pointer["blank"]==pointer["reversibly_uncomputed"]==[0,0])
    flags=explore_flags()
    with (output/"fixed_transport_free_counts.csv").open("w",encoding="utf8",newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(("steps","site","direction","sheet_A","sheet_B","signed_count"))
        histograms=magnitude_ranges(writer)
    checks["free_norms"]=all(row["total"]==row["expected"] for row in histograms)
    checks["flag_forces_first_doubling"]=(flags[0]["flag_odds_L1_L2_L4"]==["1/3"]*3 and
                                         flags[-1]["yes"]=={1:8} and flags[-1]["other"]=={1:20,2:1})
    corridor_runs=[row for p in (3,5,7,11,13) for carrier in ("static","linear","quadratic")
                   for row in corridor(p,carrier,96)]
    checks["corridor_recurrence"]=all(r["agrees"] and r["unconditional_count"]==r["n"]**2+2
                                      for r in corridor_runs)
    report=dict(checks=checks, trials=trials, destructive_output_pointer_counts=pointer,
                persistent_flag_controls=flags, free_magnitude_histograms=histograms,
                recurrent_flags=corridor_runs)
    (output/"fixed_transport.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf8")
    print(checks)
    if not all(checks.values()):
        raise SystemExit(1)


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("output",type=Path)
    main(parser.parse_args().output)
