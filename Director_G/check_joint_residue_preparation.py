"""Prepare signed two-residue multisets on diagonal rail inputs with joint position masks.

Run python -B check_joint_residue_preparation.py OUTDIR. Source is always (0,R;0,R).
The two cyclic sheets stay separate; only the two Hadamard signs are multiplied.
"""
import argparse
from collections import Counter
from itertools import product
import json
from pathlib import Path

from check_compact_residue_preparation import S, V, W, events, lineage, raw_gain


def require(ok, message):
    if not ok:
        raise ValueError(message)


def prefix(target, m):
    """Place both walkers in R, with start difference equal to the required target difference."""
    size = 4*m
    left = (target[0]-target[1]) % size // 2
    n = size+1
    words = ("R"*n, "L"*left+"R"*(n-left))
    starts = tuple((w.count("R")-w.count("L")) % size for w in words)
    require((starts[1]-starts[0]-target[1]+target[0]) % size == 0, "prefix parity")
    seq = []
    x = [0,0]
    for a,b in zip(*words):
        x = [(p + (1 if c=="R" else -1)) % size for p,c in zip(x,(a,b))]
        seq.append({tuple(x)})
    return seq, words, starts


def compile_joint(m, rr, ll, target):
    size=4*m
    require(m>=3 and all(0<=x<size for x in target) and (target[0]-target[1])%2==0,
            "target outside source parity component")
    wanted=rr+ll
    roles=["R"]*len(rr)+["L"]*len(ll)
    first, words, starts = prefix(target, m)
    program=events(m,roles,target[0],starts[0])
    switches=[[[S]*m for _ in wanted] for _ in range(2)]
    def trace(i, axis):
        return raw_gain(words[axis]+lineage(program,roles,switches[axis],i),0)

    receipts=[]
    for i,(sign,j,k) in enumerate(wanted):
        require(sign in (-1,1) and 0<=j<m and 0<=k<m, "signed residue target")
        a,b=trace(i,0),trace(i,1)
        if a[0]*b[0] != sign:
            switches[0][i][0]=V
        for axis,initial,end in ((0,a[1],j),(1,b[1],k)):
            n=(end-initial)%m
            switches[axis][i][1:1+n]=[W]*n
        receipts.append(dict(rail=roles[i], target=(sign,j,k),
                             controls=["".join({S:"S",V:"V",W:"W"}[w] for w in ch[i])
                                       for ch in switches]))
    for i,(sign,j,k) in enumerate(wanted):
        a,b=trace(i,0),trace(i,1)
        require((a[0]*b[0],a[1]%m,b[1]%m,a[2],b[2])==(sign,j,k,roles[i],roles[i]),
                "an already deposited lineage changed")

    # Each row is a set of PAIRED wells. Taking the Cartesian product would open crossed arms.
    rows=list(first)
    offset=0
    def emit(pairs):
        t=len(rows)-len(first)+1
        rows.append({tuple((start+t-2*(offset+d))%size for start,d in zip(starts,pair))
                     for pair in pairs})
    for kind,side,i,k in program:
        walls={0,2} if side=="R" else {0,2,4}
        if kind=="macro":
            rd=[0,0]
            sd=0
            for a,b,stock in zip(switches[0][i][k],switches[1][i][k],S):
                rd=[rd[0]+(a=="L"),rd[1]+(b=="L")]
                sd+=stock=="L"
                emit([tuple(rd)]+[(d+sd,d+sd) for d in walls if d])
            offset+=2
        elif kind=="deposit":
            for z in (1,2,2):
                emit([(d,d) for d in walls|{z}])
        elif kind=="transfer":
            for z in (3,4,4):
                emit([(0,0),(z,z)])
        elif kind=="hold":
            for _ in range(k):
                emit([(d,d) for d in (0,2,4)])
        else:
            for wells in ((2,4),(3,4),(4,)):
                emit([(d,d) for d in wells])
    require(rows[-1]=={tuple(target)} and max(map(len,rows))<=4, "terminal site or aperture")
    return rows,receipts


def physical(rows, m):
    size=4*m
    field=Counter({(0,0,"R","R",1,0,0):1})
    for wells in rows:
        nxt=Counter()
        for (x,y,c,d,s,j,k),n in field.items():
            for a,b in product("RL",repeat=2):
                u=(x+(1 if a=="R" else -1))%size
                v=(y+(1 if b=="R" else -1))%size
                if (u,v) in wells:
                    neg=(a==c=="L") != (b==d=="L")
                    nxt[u,v,a,b,-s if neg else s,(j+x//2)%m,(k+y//2)%m]+=n
        field=nxt
    return field


def trial(m, rr, ll, target, retain=False):
    rows,receipts=compile_joint(m,rr,ll,target)
    found=physical(rows,m)
    expected=Counter((*target,c,c,s,j,k) for c,items in (("R",rr),("L",ll)) for s,j,k in items)
    require(found==expected,"physical four-successor census")
    result=dict(ticks=len(rows), maximum_well_pairs=max(map(len,rows)), terminal_paths=sum(found.values()))
    if retain:
        result.update(controls=receipts, census=[[*q,n] for q,n in sorted(found.items())])
    return result


def rank_two_mask(m):
    size=4*m
    rows=[{(1,1),(size-1,size-1)},{(0,0)},{(1,1)}]
    shared=physical(rows,m)
    separate=physical([{(a,b) for a in (1,size-1) for b in (1,size-1)},*rows[1:]],m)
    one=lambda z: [[j,k,n] for (x,y,c,d,s,j,k),n in sorted(z.items())]
    require(one(shared)==[[0,0,1],[m-1,m-1,1]],"diagonal three-tick filter")
    require(sum(separate.values())==4 and len(separate)==4, "Cartesian-mask leakage")
    return dict(joint=one(shared),cartesian_mutant=one(separate))


def successor_controls(m):
    size=4*m
    target=(size-1,1)
    payload=[(1,0,m-1),(-1,0,m-1),(1,2,1)]
    modes=[]
    for a,b in product("RL",repeat=2):
        parent=((target[0]-(1 if a=="R" else -1))%size,
                (target[1]-(1 if b=="R" else -1))%size)
        adjusted=[(s,(j-parent[0]//2)%m,(k-parent[1]//2)%m) for s,j,k in payload]
        rows,_=compile_joint(m,adjusted,[],parent)
        census=physical(rows+[{target}],m)
        require(census==Counter((*target,a,b,s,j,k) for s,j,k in payload), "one-rail transfer")
        modes.append(dict(output=a+b,parent=parent,ticks=len(rows)+1))

    rr,ll=payload[:2],payload[1:]
    rows,_=compile_joint(m,rr,ll,target)
    next_sites={((target[0]+dx)%size,(target[1]+dy)%size) for dx,dy in product((-1,1),repeat=2)}
    observed=physical(rows+[next_sites],m)
    expected=Counter()
    for a,b in product("RL",repeat=2):
        x=(target[0]+(1 if a=="R" else -1))%size
        y=(target[1]+(1 if b=="R" else -1))%size
        for origin,items in ((True,rr),(False,ll)):
            for s,j,k in items:
                sign=-s if not origin and a!=b else s
                expected[x,y,a,b,sign,(j+target[0]//2)%m,(k+target[1]//2)%m]+=1
    require(observed==expected, "diagonal split signs, gains or count")
    return dict(target=target, all_single_modes=modes, diagonal_extension_words=sum(observed.values()))


def check():
    summaries=[]
    for m in (3,4,5,7,8):
        size=4*m
        bins=[(s,j,k) for j in range(m) for k in range(m) for s in (1,-1)]
        complete=trial(m,bins,bins[::-1],(size-1,1)) if m in (3,4) else None
        max_ticks=0
        for target in product(range(size),repeat=2):
            if (target[0]-target[1])%2:continue
            verify=trial(m,[(1,0,0),(-1,1,0)],[(-1,0,m-1)],target)
            max_ticks=max(max_ticks,verify["ticks"])
        no_paths=trial(m,[],[],(0,0))
        summaries.append(dict(order=m, all_sites=size*size//2, latest_sparse_ticks=max_ticks,
                              complete_signed_square=complete, empty=no_paths))
    m=3
    example=trial(m,[(1,0,1),(1,0,1),(-1,2,2)],[(1,1,0),(-1,1,0)],(11,3),True)
    return dict(scope="Non-Cartesian joint whole-position masks and independent local gains on one clock.",
                coverage=summaries, named_example=example, crossed_arm_control=rank_two_mask(5),
                successor_controls=successor_controls(3))


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory",type=Path)
    directory=parser.parse_args().directory
    result=check()
    directory.mkdir(parents=True,exist_ok=True)
    with (directory/"joint_residue_preparation.json").open("x",encoding="utf8",newline="\n") as f:
        json.dump(result,f,separators=(",",":"))
        f.write("\n")
