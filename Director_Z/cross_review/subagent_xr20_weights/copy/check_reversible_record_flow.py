"""Finite reversible counting lifts of Born and contextual-flow laws on one signed clock."""
import argparse
from bisect import bisect_right
from fractions import Fraction
import hashlib
import json
from math import lcm
from pathlib import Path


PREP = [
    [3,1,0,4,5,2,7,6], [6,2,5,4,3,7,0,1], [3,2,5,7,0,4,1,6],
    [7,6,1,5,0,4,2,3], [0,5,2,7,6,3,4,1], [7,1,4,6,2,3,0,5],
]
ECHO = [2,1,0,3,4,5,6,7]
WORD = PREP + [ECHO,ECHO] + PREP[::-1]


def square(v):
    norm = sum(x*x for x in v)
    return [Fraction(x*x,norm) for x in v]


def probabilities(rule):
    vectors = [[1]+[0]*7]
    phases = [square(vectors[0])]
    for match in WORD:
        v, p = vectors[-1], phases[-1]
        w = [0]*8
        q = [Fraction(0)]*8
        for a,b in zip(match[::2],match[1::2]):
            w[a],w[b]=v[a]+v[b],v[a]-v[b]
            total=p[a]+p[b]
            norm=w[a]**4+w[b]**4
            if norm:
                q[a]=total*Fraction(w[a]**4,norm)
                q[b]=total-q[a]
            else:
                assert total==0
        q=square(w) if rule=="Born" else q
        assert all(q[i]==0 for i in range(8) if w[i]==0)
        assert sum(q)==1
        vectors.append(w)
        phases.append(q)
    assert vectors[-1]==[128]+[0]*7 and phases[-1]==phases[0]
    return phases,vectors


def offsets(weights):
    out=[0]
    for w in weights:
        out.append(out[-1]+w)
    return out


def interval_map(before, after, match):
    """Greedy transport on each cell, consecutive disjoint ranges at each port."""
    matrix=[[0]*8 for _ in range(8)]
    for a,b in zip(match[::2],match[1::2]):
        assert before[a]+before[b]==after[a]+after[b]
        z=min(before[a],after[a])
        matrix[a][a],matrix[a][b]=z,before[a]-z
        matrix[b][a],matrix[b][b]=after[a]-z,before[b]-after[a]+z
    source=offsets(before)[:-1]
    target=offsets(after)[:-1]
    segments=[]
    for i in range(8):
        for j in range(8):
            count=matrix[i][j]
            assert count>=0
            if count:
                segments.append([i,j,source[i],target[j],count])
                source[i]+=count
                target[j]+=count
    assert source==offsets(before)[1:] and target==offsets(after)[1:]
    # A row is (input port,output port,input offset,output offset,length).
    return segments,matrix


def run_case(rule):
    phases,vectors=probabilities(rule)
    size=lcm(*(p.denominator for row in phases for p in row))
    counts=[[int(p*size) for p in row] for row in phases]
    assert all(all(Fraction(n,size)==p for n,p in zip(row,probs))
               for row,probs in zip(counts,phases))
    intervals=[]
    maps=[]
    inverses=[]
    matrices=[]
    for t,word in enumerate(WORD):
        segments,matrix=interval_map(counts[t],counts[t+1],word)
        direct=[-1]*size
        inverse=[-1]*size
        for _,_,x,y,k in segments:
            assert all(d==-1 for d in direct[x:x+k]) and all(d==-1 for d in inverse[y:y+k])
            direct[x:x+k]=range(y,y+k)
            inverse[y:y+k]=range(x,x+k)
        assert all(inverse[y]==x for x,y in enumerate(direct))
        assert all(direct[x]==y for y,x in enumerate(inverse))
        intervals.append(segments)
        maps.append(direct)
        inverses.append(inverse)
        matrices.append(matrix)

    # The stored t is a spatial clock phase. The forward sheet moves t to t+1;
    # the reverse sheet moves it to t-1 using the inverse map at t-1.
    def step(t,k,orientation):
        if orientation==1:
            return (t+1)%14,maps[t][k],1
        prev=(t-1)%14
        return prev,inverses[prev][k],-1

    def reversal(t,k,orientation):
        return t,k,-orientation

    for t in range(14):
        for k in range(size):
            for orientation in (1,-1):
                state=t,k,orientation
                assert reversal(*reversal(*state))==state
                assert step(*reversal(*step(*reversal(*state))))==state  # P J P J = I
    # Evaluate distributions using all actual microstates with the bright port label at t=7.
    bright=2
    t=7
    off=offsets(counts[t])
    reverse_hist=[0]*8
    forward_hist=[0]*8
    for k in range(off[bright],off[bright+1]):
        for o,hist in ((1,forward_hist),(-1,reverse_hist)):
            dest,slot,_=step(t,k,o)
            port=bisect_right(offsets(counts[dest]),slot)-1
            hist[port]+=1
    bright_count=counts[7][bright]
    assert sum(reverse_hist)==sum(forward_hist)==bright_count>0
    assert reverse_hist==[matrices[6][a][bright] for a in range(8)]
    assert forward_hist==matrices[7][bright]
    assert forward_hist[1]==forward_hist[2]==bright_count//2
    splits=[Fraction(reverse_hist[j],bright_count) for j in (1,2)]
    mixed=[Fraction(reverse_hist[j]+forward_hist[j],2*bright_count) for j in (1,2)]
    if rule=="Born":
        assert splits==mixed==[Fraction(1,2)]*2
    else:
        assert splits==[Fraction(5,46),Fraction(41,46)]
        assert mixed==[Fraction(7,23),Fraction(16,23)] and size==22304
    # Every single-occupied cell in the forward direction is fair. Reverse dynamics
    # may leave the dark port sharp yet split the bright port unfairly.
    reverse_biased=[]
    forward_count=0
    for t,match in enumerate(WORD):
        for a,b in zip(match[::2],match[1::2]):
            if bool(vectors[t][a])!=bool(vectors[t][b]):
                assert counts[t+1][a]==counts[t+1][b]
                forward_count+=1
            if bool(vectors[t+1][a])!=bool(vectors[t+1][b]) and counts[t][a]!=counts[t][b]:
                reverse_biased.append([t+1,a,b,counts[t][a],counts[t][b]])
    # Closing the clock does not assert that every microscopic trajectory has period 14.
    monodromy=list(range(size))
    for f in maps:
        monodromy=[f[k] for k in monodromy]
    seen=set()
    lengths={}
    for k in range(size):
        if k in seen:
            continue
        j=k
        n=0
        while j not in seen:
            seen.add(j)
            n+=1
            j=monodromy[j]
        assert j==k
        lengths[n]=lengths.get(n,0)+1
    return dict(rule=rule,D=size,phase_count=14,total_uniform_microstates=28*size,
                signed_numerator_at_t_over_sqrt_2_power_t=vectors,
                port_cardinalities_by_phase=counts,interval_column_labels=[
                    "from_port","to_port","from_slot","to_slot","length"],
                intervals_by_forward_tick=intervals,
                explicit_labeled_state_reversal_checks=28*size,
                monodromy_orbit_count_by_number_of_clock_laps=lengths,
                fair_forward_single_occupied_pairs=forward_count,
                reverse_unfair_single_occupied_pairs=reverse_biased,
                bright_control=dict(clock_phase=7,port=bright,port_fiber_per_orientation=bright_count,
                  next_port_counts_forward=forward_hist,next_port_counts_reverse=reverse_hist,
                  reverse_conditional_by_port_1_2=list(map(str,splits)),
                  unobserved_orientation_conditional_by_port_1_2=list(map(str,mixed)),
                  dark_partner_port=1,dark_port_cardinality=counts[7][1],
                  dark_conditioning="undefined for a zero-size fiber"))


def main(output):
    result=dict(model="States are (t,k,o) with 14 clock sites, 0<=k<D, o=+1 or -1. "
                      "Port i labels the consecutive interval of cardinality c[t,i]. A forward step "
                      "f_t translates each listed source interval to its destination interval. "
                      "At o=-1 use f_(t-1)^-1. J flips o at fixed physical clock and slot; in "
                      "oriented elapsed phase coordinates a=o*t mod 14 this is a->-a. "
                      "The entire doubled permutation and J preserve uniform counting.",
                matchings=WORD,cases=[run_case("Born"),run_case("local fourth powers")],
                interpretation="Conditioning on forward orientation yields the designed causal "
                               "law. The full uniform ensemble is J-invariant, but it does not impose "
                               "equal counts on two distinct predecessor-port fibers of the bright "
                               "mode. Conditioning only on physical time and brightness averages the "
                               "two orientations equally. Selecting the reverse orientation recovers "
                               "the transpose of the earlier actual joint, not a fresh fair prepare.",
                scope="A finite contextual simulator for this one signed trajectory. Port labels "
                      "are fixed functions of microscopic state and are even under J. The signed "
                      "amplitude columns are attached as phase labels, not derived from the hidden "
                      "permutation. Couplings and fiber degeneracies are chosen per law; the same "
                      "microscopic measure, arbitrary interventions, and universal preparation-independent "
                      "port dynamics have not been derived from the signed update.")
    output.mkdir(parents=True,exist_ok=True)
    dest=output/"reversible_record_flow.json"
    dest.write_bytes((json.dumps(result,indent=1)+"\n").encode())
    print(dest,hashlib.sha256(dest.read_bytes()).hexdigest())


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_directory",type=Path)
    main(parser.parse_args().output_directory)
