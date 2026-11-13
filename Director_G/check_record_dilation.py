"""Finite signed-history comparison with a Born model containing unobserved records.

Run python -B check_record_dilation.py <output-directory>. Only integer or exact
quadratic-field arithmetic is used. The two path computations are independent.
"""

import argparse
import itertools
import json
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path

M = 5
# Labels denote count, then k=0,1,2,3,4. All coefficients are nonnegative.
PRIOR = (F(1,3),F(1,6),F(1,6),F(1,12),F(1,12),F(1,6))
UNIT = (1,0,0,0)


def qr(a=0,b=0):
    return F(a),F(b)


def scalar(p):
    return [str(p[0]),str(p[1])]


def rotate(poly, power):
    # In Z[zeta5]: zeta5^4=−(1+zeta5+zeta5²+zeta5³).
    c=list(poly)+[0]
    c=[c[(j-power)%M] for j in range(M)]
    return tuple(z-c[4] for z in c[:4])


def square(vector):
    # Sum z_i z_j cos(2pi(i−j)/5) in Q(sqrt(5)).
    # vector can be either a four-coefficient canonical polynomial or a
    # full five-component lift. No complex binary64 arithmetic enters.
    # Multiplicities at signed order-zero need no separate branch.
    a=b=0
    for i,p in enumerate(vector):
        for j,q in enumerate(vector):
            h=(i-j)%M
            w=p*q
            if h==0:
                a+=4*w
            else:
                a-=w
                b+=(w if h in (1,4) else -w)
    return qr(F(a,4),F(b,4))


def append_record(t,x,rail,record):
    # The second setting controls later departures; the pointer only copies
    # a function of the *current* physical coordinates and the old record.
    if t==3:
        return record+(int(x>0),)
    if t==5:
        return record+(int((rail==1 and x==1) if record[0] else x < -1),)
    if t==7:
        return record+(int((x+rail)%3==0),)
    return record


def departure(t,x,record):
    return x//2 if t<=3 or record[0] else x


def words(depth):
    grouped=defaultdict(lambda:[0,[0]*M])
    for word in itertools.product((1,-1),repeat=depth):
        x=y=0
        last=sign=1
        record=()
        for t,d in enumerate(word,1):
            y=(y+departure(t,x,record))%M
            x+=d
            sign*=(-1 if last==d==-1 else 1)
            last=d
            record=append_record(t,x,last,record)
        bucket=grouped[record,x,last]
        bucket[0]+=1
        bucket[1][y]+=sign
    return grouped


def direct_law(depth):
    out=defaultdict(lambda:[qr() for _ in PRIOR])
    for (record,x,rail),(n,bins) in words(depth).items():
        contributions=[qr(n)]
        for k in range(M):
            values=[0]*M
            for j,v in enumerate(bins):
                values[k*j%M]+=v
            contributions.append(square(values))
        for i,(a,b) in enumerate(contributions):
            u,v=out[record][i]
            out[record][i]=u+a/2**depth,v+b/2**depth
    return out


def born_hidden(depth):
    # Separate, orthogonal sector flag. The count component writes its
    # outgoing rail to an unused tape bit; copying into that bit is reversible.
    counts={(0,1,0,(),()):1}
    # Character sectors evolve on the base only. Each complete inherited pointer
    # branch carries its visibly recorded sequence of base readouts.
    states=[{(0,1,()):UNIT} for _ in range(M)]
    for t in range(1,depth+1):
        marked=defaultdict(int)
        for (x,prev,y,r,tape),z in counts.items():
            g=departure(t,x,r)
            for d in (1,-1):
                y1=(y+g)%M
                rec=append_record(t,x+d,d,r)
                marked[x+d,d,y1,rec,tape+(d,)]+=z*(-1 if prev==d==-1 else 1)
        counts=marked
        new=[]
        for k,state in enumerate(states):
            ns=defaultdict(lambda:[0]*4)
            for (x,prev,r),z in state.items():
                g=departure(t,x,r)
                phase=rotate(z,k*g)
                for d in (1,-1):
                    rec=append_record(t,x+d,d,r)
                    sign=-1 if prev==d==-1 else 1
                    target=ns[x+d,d,rec]
                    for j,c in enumerate(phase):
                        target[j]+=sign*c
            new.append(ns)
        states=new
    out=defaultdict(lambda:[qr() for _ in PRIOR])
    for (_,_,_,r,_),z in counts.items():
        a,b=out[r][0]
        out[r][0]=(a+F(z*z,2**depth),b)
    for k,state in enumerate(states):
        for (_,_,r),poly in state.items():
            a,b=square(poly)
            u,v=out[r][k+1]
            out[r][k+1]=(u+a/2**depth,v+b/2**depth)
    return out

def transcript_check(depth):
    direct=direct_law(depth)
    dilation=born_hidden(depth)
    assert direct==dilation and sum(PRIOR)==1
    for i in range(len(PRIOR)):
        assert tuple(sum(v[i][j] for v in direct.values()) for j in (0,1))==qr(1)
    rows=[]
    for key, laws in sorted(direct.items()):
        mixture=tuple(sum(w*law[j] for w,law in zip(PRIOR,laws)) for j in (0,1))
        rows.append(dict(record=list(key),conditional_sector_weights=[scalar(a) for a in laws],
                         mixture=scalar(mixture)))
    return rows


def lifted_dark():
    # Same physical M5 coordinate in count and ordinary lifted coherent
    # branches. The sheet-sensitive pointer is a legitimate projector here.
    full={(0,1,0):1}
    tagged={(0,1,0,()):1}
    for _ in range(5):
        nfull=defaultdict(int)
        ntape=defaultdict(int)
        for (x,c,y),a in full.items():
            for d in (1,-1):
                nfull[x+d,d,(y+x//2)%M]+=a*(-1 if c==d==-1 else 1)
        for (x,c,y,tape),a in tagged.items():
            for d in (1,-1):
                ntape[x+d,d,(y+x//2)%M,tape+(d,)]+=a*(-1 if c==d==-1 else 1)
        full,tagged=nfull,ntape
    coarse=defaultdict(int);count=defaultdict(int)
    for key,amp in full.items():
        coarse[key]+=amp**2
    for (x,c,y,_),amp in tagged.items():
        count[x,c,y]+=amp**2
    assert sum(coarse.values())==sum(count.values())==32
    target=(1,1,4)
    assert coarse[target]==0 and count[target]==2
    one=F(1,3)
    p=(F(count[target],32),F(coarse[target],32))
    two={}
    for a,b in itertools.product((0,1),repeat=2):
        vec1=[v if a else 1-v for v in p]
        vec2=[v if b else 1-v for v in p]
        # If the hidden law is retained it is the same on both physical
        # launches. Both have fresh base, sheet, tape and detector input.
        persistent=one*vec1[0]*vec2[0]+(1-one)*vec1[1]*vec2[1]
        reset=(one*vec1[0]+(1-one)*vec1[1])*(one*vec2[0]+(1-one)*vec2[1])
        two[str(a)+str(b)]={"retained_sector":str(persistent),"reset_sector":str(reset)}
    assert sum(F(row["retained_sector"]) for row in two.values())==1
    assert sum(F(row["reset_sector"]) for row in two.values())==1
    assert two["11"]=={"retained_sector":"1/768","reset_sector":"1/2304"}
    # Direct finite example of the passive-tagging boundary for general
    # character priors: two coherent paths to an otherwise single port
    # with sheet separation one have scalar squared mass 2+2cos(2pi k/5);
    # distinguishable pointer cells have 1+1 instead.
    coarse_two=[]
    for k in range(M):
        assert square(rotate(UNIT,k))==qr(1)
        a=tuple(u+v for u,v in zip(UNIT,rotate(UNIT,k)))
        coarse_two.append(scalar(square(a)))
    assert [sum(F(row[i]) for row in coarse_two)/M for i in (0,1)]==list(qr(2))
    return dict(target={"site":1,"direction":"R","sheet":4,"ticks":5},
            probabilities_conditional_on_sector={"count":"1/16","ordinary_localized_sheet":"0"},
            all_complete_output_numerators_over32=[
                dict(x=x,direction=d,sheet=y,count=count[x,d,y],lifted=coarse[x,d,y])
                for x,d,y in sorted(count.keys()|coarse.keys())],
            count_prior="1/3",one_read_dark="1/48",two_read_joint=two,
            two_singletons_raw_parity_control=dict(separation=1,coherently_summed_sector_k=coarse_two,
                distinguishable_sheet_outputs_raw_sum="2",average_over_all_character_k="2"))


def echo(erase,hidden):
    # Basis (rail, exposed tag, environment). H, rail-controlled copy, local
    # inaccessible copy (or identity), optional rail-controlled undo, H.
    # All five time slots occur in each case; the outgoing rail at the undo
    # is exactly the one that carried the original tag.
    state={(0,0,0):1}
    for op in ("H","tag","environment","undo","H"):
        new=defaultdict(int)
        for (b,t,e),a in state.items():
            if op=="H":
                for d in (0,1):
                    new[d,t,e]+=a*(-1 if b==d==1 else 1)
            else:
                new[b,t^(b if op=="tag" or (op=="undo" and erase) else 0),
                      e^(b if op=="environment" and hidden else 0)]+=a
        state=new
    probs={(r,t):sum(state.get((r,t,e),0)**2 for e in (0,1)) for r,t in itertools.product((0,1),repeat=2)}
    # Fundamentally linear path counting on the very same gate graph.
    count=defaultdict(int)
    for first,second in itertools.product((0,1),repeat=2):
        count[second,0 if erase else first]+=1
    assert sum(probs.values())==sum(count.values())==4
    expected=[2,0,2,0] if hidden and erase else ([4,0,0,0] if erase else [1,1,1,1])
    assert list(probs.values())==expected
    return dict(exposed_tag_uncomputed=erase,inaccessible_copy=hidden,
        basis_order=["0,0","0,1","1,0","1,1"],ordinary_Born_over4=list(probs.values()),
        linear_count_over4=[count[k] for k in probs],
        environment_resolved_amplitude_numerators=[
          dict(rail=r,tag=t,hidden=e,numerator=state.get((r,t,e),0)) for r,t,e in itertools.product((0,1),repeat=3)])


def main():
    cases=transcript_check(7)
    assert len(cases)==8
    return dict(model="Five sheets on an integer line, initial (0,R); each Hadamard contributes one common 1/sqrt(2). Gain floor(x/2) is applied on departure through tick 3. Afterwards, the tick-3 positive-site read decides between floor(x/2) and x. A second base/rail pointer at tick 5 depends on the first outcome, followed by a terminal base/rail parity flag at tick 7. All eight transcripts, including any zero support, use unnormalized branch masses; no probabilities are conditioned or silently postselected.",
        dilation="On a fixed ideal graph with unit-modulus gain and physical coherent blocks unitary in each allowed signed character, initialize an orthogonal, unobserved count or character label with the declared nonnegative probabilities. In the count sector the signed physical walk writes a distinct outgoing branch to a clean tape cell at each branching tick (distinguishable history or edge labels as required). The trace over the tape sums path squares. In each character sector, the unmarked signed walk applies its own gain phase and adds amplitudes at common final ports. The sector label persists. Reading only the specified common output projectors and tracing this label produces the count-plus-character law on each transcript by linearity of density operators. This can also be purified by retaining the label. It presupposes a Born carrier, a fresh orthogonal tape and a common block/instrument model, not an independent rule for all conceivable operations.",
        read_scope="Pointer copies of an already available base or rail predicate commute with the hidden-sector split; a pointer physically copied and then ignored is traced, so its differing outcomes dephase alternatives. A reversible uncomputation can restore that coherence.  For a fine sheet pointer use a real localized sheet register in the lifted model as in the dark example. Applying history masks to a scalar-character-only port as if they were automatically harmless changes its Kraus operators and can change the coarse weight. A sheet-insensitive unmarked localized physical lift reproduces the uniform character mixture by Fourier decomposition; a probe that mixes those characters requires the physical joint state and cannot in general be replaced by classical independently evolving scalar sectors.",
        scalar_format="Each pair [a,b] denotes the exact number a+b*sqrt(5). Character signs multiply the fifth-root gain; phase conjugation does not change norms.",
        hidden_sectors=["count","k=0 sign","k=1","k=2","k=3","k=4"],prior=[str(v) for v in PRIOR],
        adaptive_transcript_rows=cases,localization_control=lifted_dark(),
        echo=dict(clock_slots=["Hadamard","copy rail to tag","copy to environment or aligned identity","uncompute tag or aligned identity","Hadamard"],
                 output_normalization="The two Hadamards give denominator 2 for amplitudes and 4 for squared weights.",
                 controls=[echo(a,h) for a,h in itertools.product((False,True),repeat=2)],
                 scope="Only when the tagged rail still distinguishes the alternatives and every other record of it is absent or coherently erased does a final dark port distinguish unitary coherent evolution from counting the two histories as exclusive. An inaccessible surviving copy reproduces the linear-count statistics in this read, even if the accessible tag was fully uncomputed. It is not a unilateral unitary erasure of two orthogonal states after they have merged. Independent settings can repeat the test only under a specified model for environmental memory and resets."),
        independence="A fresh visible preparation does not imply a reset of a persistent hidden sector. Conversely, a product preparation with independent, deliberately prepared sector labels realizes the redraw model. The examples quantify that experimental distinction without assuming either memory model is compulsory.")


if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("directory",type=Path)
    directory=p.parse_args().directory
    directory.mkdir(parents=True,exist_ok=True)
    dest=directory/"record_dilation.json"
    dest.write_bytes((json.dumps(main(),indent=2,allow_nan=False)+"\n").encode())
    print(dest)
