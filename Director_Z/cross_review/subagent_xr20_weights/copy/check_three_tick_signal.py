"""Native three-tick A-only signal from a localized two-walker coin and shared sheet."""
import argparse
from collections import Counter, defaultdict
from fractions import Fraction
import hashlib
from itertools import combinations, product
import json
from pathlib import Path

from check_cycle_interaction import count_table


def exact_profile(n, scale):
    depth=n*n*(n-1).bit_length()
    counts=count_table(n,depth)
    assert sum(counts)==4**depth and counts[1:]==counts[:0:-1]
    norm=counts[0]-counts[n//2]
    assert norm>0
    gains=[(4*scale*(counts[0]-c)+norm)//(2*norm) for c in counts]
    assert all(2*abs(g*norm-2*scale*(counts[0]-c))<=norm for c,g in zip(counts,gains))
    return dict(n=n,scale=scale,auxiliary_depth=depth,rounding="nearest integer, ties upwards",
                normalized_profile="R(d)=2(C(0)-C(d))/(C(0)-C(N/2))",
                raw_cycle_count_row_hex=[hex(x) for x in counts],gains=gains)


def path_table(n, order, gain, start_b, ticks):
    """Sum signed histories sharing exactly the same complete endpoint, then square."""
    table=Counter()
    paths=defaultdict(list)
    directions=list(product((1,-1),repeat=ticks))
    for a,b in product(directions,repeat=2):
        x,y,ca,cb,sheet,sign=0,start_b,1,1,0,1
        for da,db in zip(a,b):
            sheet=(sheet+gain[(x-y)%n])%order
            if ca==da==-1:
                sign=-sign
            if cb==db==-1:
                sign=-sign
            x,y,ca,cb=(x+da)%n,(y+db)%n,da,db
        endpoint=(x,ca,y,cb,sheet)
        table[endpoint]+=sign
        paths[x,ca].append((a,b,endpoint,sign))
    return table,paths


def stream(n, order, gain, start_b, ticks):
    """Independent tickwise update on sparse position/direction/sheet states."""
    state={(0,1,start_b,1,0):1}
    for tick in range(ticks):
        out=Counter()
        for (x,c,y,e,s),value in state.items():
            dest_sheet=(s+gain[(x-y)%n])%order
            for i,j in product((1,-1),repeat=2):
                sign=(-1 if i==c==-1 else 1)*(-1 if j==e==-1 else 1)
                out[(x+i)%n,i,(y+j)%n,j,dest_sheet]+=sign*value
        state=out
    return state


def mass_by_port(table):
    masses=Counter()
    for (x,ca,y,cb,s),v in table.items():
        masses[x,ca]+=v*v
    return masses


def collisions(paths):
    classes={key:[0,0] for key in ("only_a_differs","only_b_differs","both_differ")}
    for (a,b,e,s),(a2,b2,e2,s2) in combinations(paths,2):
        if e==e2:
            key="both_differ" if a!=a2 and b!=b2 else "only_a_differs" if a!=a2 else "only_b_differs"
            classes[key][0]+=1
            classes[key][1]+=s*s2
    interference=sum(v[1] for v in classes.values())
    return dict(raw_paths=len(paths),unordered_pairs_and_signed_sums=classes,
                squared_count=len(paths)+2*interference)


def run_scenario(name,n,order,gain,starts):
    runs=[]
    for start_b in starts:
        times=[]
        for tick in range(4):
            table,paths=path_table(n,order,gain,start_b,tick)
            streamed=stream(n,order,gain,start_b,tick)
            assert dict(table)==dict(streamed)
            marginal=mass_by_port(table)
            assert sum(marginal.values())==4**tick
            times.append(dict(tick=tick,raw_histories=4**tick,total_signed_count=sum(table.values()),
                              squared_mass=sum(marginal.values()),probability_denominator=4**tick,
                              reached_endpoints_including_cancellations=[list(k)+[v] for k,v in sorted(table.items())],
                              implicit_zero_endpoint_count=4*n*n*order-len(table),
                              a_port_marginals=[list(k)+[v] for k,v in sorted(marginal.items())]))
        binary={}
        for port in ((1,1),(n-1,-1)):
            row=collisions(paths[port])
            assert row["squared_count"]==marginal[port]
            row["probability"]=str(Fraction(row["squared_count"],64))
            row["complement"]=str(1-Fraction(row["squared_count"],64))
            binary[str(port)]=row
        runs.append(dict(initial_B=start_b,times=times,binary_records=binary))
    return dict(name=name,N=n,M=order,gains=gain,inputs=runs)


def observed(scenario,port):
    return [Fraction(r["binary_records"][str(port)]["probability"]) for r in scenario["inputs"]]


def signed_correlation(paths,order):
    """Trace B and form the sheet autocorrelation prior to fixing its input."""
    by_b=defaultdict(Counter)
    by_word=defaultdict(dict)
    for a,b,(_,_,site,coin,sheet),sg in paths:
        by_b[site,coin][sheet]+=sg
        by_word[b][a]=sheet
    coefficients=[0]*order
    for shifted in by_b.values():
        for i,vi in shifted.items():
            for j,vj in shifted.items():
                coefficients[(i-j)%order]+=vi*vj
    gaps=sorted({(arms[(1,-1,1)]-arms[(-1,1,1)])%order for arms in by_word.values()})
    return dict(sheet_autocorrelation_numerator=coefficients,denominator=64,
                arm_difference_mod_M_by_B_word={",".join(str(x) for x in b):
                  (arms[(1,-1,1)]-arms[(-1,1,1)])%order for b,arms in by_word.items()},
                distinct_arm_differences=gaps)



def main(out):
    profile=exact_profile(32,3)
    small=exact_profile(24,1)
    g=profile["gains"]
    standard=run_scenario("exact count-built interaction",32,17,g,(8,16))
    reversed_gain=run_scenario("opposite global sheet gain",32,17,[-a for a in g],(8,16))
    free=run_scenario("zero interaction",32,17,[0]*32,(8,16))
    trivial=run_scenario("constant sheet character (sheet factored out exactly)",32,1,g,(8,16))
    streaming=run_scenario("local contact-only gain; initial walkers cannot meet before last departure",
                           32,17,[1]+[0]*31,(8,16))
    small_control=run_scenario("finite count-profile rounding near half-integer",24,17,small["gains"],(5,6))
    # These exact constants reproduce the separate float-cosine pilot. At d=4 and 8, the ideal
    # continuous values 1-cos(2πd/24) are exactly 1/2 and 3/2. Do not use floating tie choices
    # as approximations to the signs of the tiny residuals of the finite count construction.
    pilot=[0,0,0,0,0,1,1,1,1,2,2,2,2,2,2,2,2,1,1,1,0,0,0,0]
    pilot_control=run_scenario("previous floating-point rounded cosine pilot, not the finite count profile",
                               24,17,pilot,(5,6))
    assert observed(standard,(1,1))==[Fraction(1,4),Fraction(1,2)]
    assert observed(standard,(31,-1))==[Fraction(1,4),Fraction(0)]
    for s in (free,trivial,streaming):
        assert observed(s,(1,1))==[Fraction(1,2)]*2 and observed(s,(31,-1))==[0,0]
    for inputs,other in zip(standard["inputs"],reversed_gain["inputs"]):
        assert all(x["a_port_marginals"]==y["a_port_marginals"] for x,y in zip(inputs["times"],other["times"]))
    assert observed(small_control,(1,1))==[Fraction(3,8)]*2
    assert observed(pilot_control,(1,1))==[Fraction(3,8),Fraction(1,4)]
    general={}
    for b in (8,16):
        _,paths=path_table(32,17,g,b,3)
        row=signed_correlation(paths[1,1],17)
        truth=[0]*17
        truth[0]=16 if b==8 else 32
        if b==8:
            truth[1]=truth[-1]=8
        assert row["sheet_autocorrelation_numerator"]==truth
        assert row["distinct_arm_differences"]==([16] if b==8 else [0])
        general[b]=row
    result=dict(profile=profile,adverse_profile=small,endpoint_columns=["A_site","A_coin","B_site","B_coin","sheet","signed_count"],
                initial="A at 0, both incoming directions R, sheet localized at zero; B specified for each run. "
                        "Only the binary A port is read, at tick three. Earlier tables are computed without intervening measurements.",
                exact_readout="A=(1,R) gives probability 1/4 for B=8, 1/2 for B=16; complements 3/4 and 1/2. "
                              "A=(-1,L) gives 1/4 versus 0. Four other reachable A ports each have mass 1/8.",
                cone=dict(port=1,ticks=3,range_per_tick=1,distances_of_B_from_port=[7,15],
                          unconditional_binary_TV="1/4",minimum_worst_input_error_for_strictly_local_target="1/8"),
                scope="The distinguishing initial states are localized with the same ancillary preparation. A radius-one physical "
                      "circuit cannot distinguish either B input at the A port in three layers. The shared-sheet transport is a "
                      "joint rule on configurations. The cone conclusion requires a local ring encoding of input, output, clock "
                      "and independent ancillas. The finite values are not a continuum or empirical measurement.",
                arbitrary_initial_sheet=dict(bob_position=general,
                    formula="At B=8 the A=(1,R) POVM on any initial sheet density is (16I+8T+8T^{-1})/64. "
                            "At B=16 it is 32I/64. Evaluating the first on character k gives (1+cos(2 pi k/17))/4. "
                            "This assumes the same initially localized bases and a sheet uncorrelated with remote preparation."),
                controls=[standard,reversed_gain,free,trivial,streaming,small_control,pilot_control])
    out.mkdir(parents=True,exist_ok=True)
    dest=out/"three_tick_signal.json"
    dest.write_text(json.dumps(result,indent=1)+"\n",encoding="utf-8")
    print("All signed endpoint tables and collision controls passed.",dest,hashlib.sha256(dest.read_bytes()).hexdigest())


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("directory",type=Path)
    main(parser.parse_args().directory)
