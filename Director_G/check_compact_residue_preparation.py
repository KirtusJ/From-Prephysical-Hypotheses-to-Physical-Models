"""Verify signed-residue preparation by whole-site masks on the original 4M ring.

Run python check_compact_residue_preparation.py OUTDIR. Output must be new.
"""
from collections import Counter
import argparse
from pathlib import Path
import json

S = "LRRLR"
V = "RLLRR"
W = "RLRLR"


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def raw_gain(word, start):
    x, s, j, rail = start, 1, 0, "R"
    for out in word:
        j += x//2
        x += 1 if out == "R" else -1
        if rail == out == "L":
            s = -s
        rail = out
    return s, j, rail


def events(m, roles, target, start):
    """One fixed-duration block per deposited item. Site masks are moving deficits."""
    macro_time = 5*m
    horizon0 = (macro_time+3)*len(roles) + 6
    offset = 2*m*len(roles)
    hold = (target - (start+horizon0-2*(offset+4))) % (4*m)
    seq = []
    for side in "RL":
        for i,role in enumerate(roles):
            if side == role:
                seq.extend(("macro", side, i, k) for k in range(m))
                seq.append(("deposit", side, i, 0))
        if side == "R":
            seq.append(("transfer",side,-1,0))
    seq.append(("hold","L",-1,hold))
    seq.append(("finish","L",-1,0))
    return seq


def lineage(program, roles, selected, trace):
    """Directions taken by one injected lineage in the specified full schedule."""
    words=[]
    for kind,side,i,k in program:
        if kind == "macro":
            words.append(selected[i][k] if trace >= i else S)
        elif kind == "deposit":
            words.append("LLR" if trace == i else "RRR")
        elif kind == "transfer":
            words.append("LLR" if roles[trace] == "R" else "RRR")
        elif kind == "hold":
            words.append("R"*k)
        else:
            words.append("RRR" if roles[trace] == "R" else "RLL")
    return "".join(words)


def schedule(program, selected):
    offset=0
    sets=[]
    for kind,side,i,k in program:
        walls = {0,2} if side=="R" else {0,2,4}
        if kind=="macro":
            rd=sd=0
            for r,s in zip(selected[i][k],S):
                rd += r == "L"
                sd += s == "L"
                sets.append({offset+rd}|{offset+d+sd for d in walls if d})
            offset+=2
        elif kind=="deposit":
            sets.extend([{offset+d for d in walls|{z}} for z in (1,2,2)])
        elif kind=="transfer":
            sets.extend([{offset,offset+z} for z in (3,4,4)])
        elif kind=="hold":
            sets.extend([{offset,offset+2,offset+4}]*k)
        else:
            sets.extend([{offset+2,offset+4},{offset+3,offset+4},{offset+4}])
    return sets


def compile_masks(m,right,left,target,start=0):
    size=4*m
    roles=["R"]*len(right)+["L"]*len(left)
    wanted=right+left
    require(m >= 3 and all(s in (-1,1) and 0 <= g < m for s,g in wanted), "invalid target")
    require(0 <= target < size and 0 <= start < size, "invalid named site")
    program=events(m,roles,target,start)
    receipts=[]
    selected=[[S]*m for _ in wanted]
    for i,(sign,residue) in enumerate(wanted):
        base_s,base_g,rail=raw_gain(lineage(program,roles,selected,i),start)
        require(rail==roles[i],"lineage rail")
        if base_s != sign:
            selected[i][0]=V
        changes=(residue-base_g)%m
        selected[i][1:1+changes]=[W]*changes
        s,j,c=raw_gain(lineage(program,roles,selected,i),start)
        receipts.append(dict(rail=rail, requested=(sign,residue), initial_signed_gain=(base_s,base_g),
                             switches="".join({S:"S",V:"V",W:"W"}[w] for w in selected[i]),
                             selected_signed_gain=(s,j)))
        require((s,j%m,c)==(sign,residue,rail),
                "same slot did not supply requested gain")
    for i,(sign,residue) in enumerate(wanted):
        s,j,c=raw_gain(lineage(program,roles,selected,i),start)
        require((s,j%m,c)==(sign,residue,roles[i]),
                "later controls disturbed settled item")
    rows=schedule(program,selected)
    padding=next(k for kind,side,i,k in program if kind=="hold")
    require(len(rows)==(5*m+3)*len(roles)+6+padding and 0<=padding<size, "native schedule length")
    require(max(map(len,rows))<=4, "unintended extra mask well")
    return rows, receipts, padding


def physical_census(rows, m, start):
    size=4*m
    state=Counter({(start,"R",1,0):1})
    for t,ds in enumerate(rows,1):
        allowed={(start+t-2*d)%size for d in ds}
        next_state=Counter()
        for (x,c,s,j),n in state.items():
            for o,dx in (("R",1),("L",-1)):
                y=(x+dx)%size
                if y in allowed:
                    next_state[y,o,-s if c==o=="L" else s,(j+x//2)%m]+=n
        state=next_state
    return state


def run(m,right,left,target,start=0):
    rows, receipts, padding=compile_masks(m,right,left,target,start)
    state=physical_census(rows,m,start)
    expected=Counter((target,c,s,j) for c,items in (("R",right),("L",left)) for s,j in items)
    require(state==expected,"cyclic signed physical word census")
    return dict(order=m, start=start, target=target, ticks=len(rows), padding=padding,
                deposits=receipts, census=[[*k,n] for k,n in sorted(state.items())])


def isolated_macros():
    data=[]
    for word in (S,V,W):
        levels=[]
        pos=(0,2,4)
        for rc,sc in zip(word,S):
            nxt=tuple(x+(c=="L") for x,c in zip(pos,(rc,sc,sc)))
            wrong=[(i,j) for i,p in enumerate(pos) for j,q in enumerate(nxt)
                   if i!=j and (q-p)%6 in (0,1)]
            require(not wrong,"period-six extra path")
            # Every physical candidate spans fewer than six deficits; rule also works for larger M.
            require(max(pos)+1-min(nxt)<6 and max(nxt)-min(pos)<6,"wrap in the lifted table")
            levels.append(nxt);pos=nxt
        sign,j,rail=raw_gain(word,0)
        data.append(dict(word=word,final_rail=rail,sign=sign,relative_residue=j-raw_gain(S,0)[1],
                         admitted_deficits=levels))
    require([(row["sign"],row["relative_residue"]) for row in data] == [(1,0),(-1,0),(1,1)],
            "absolute switch differences")
    return data


def leaking_macro(data):
    # On the minimum circumference, one additional well on tick two opens a path
    # from the stored wire to the reservoir's *output*. Keep the individual path count.
    rows=[{d%6 for d in triple} for triple in data[2]["admitted_deficits"]]
    def matrix(masks):
        table=[]
        for start in (0,2,4):
            occupants=Counter({start:1})
            for allowed in masks:
                following=Counter()
                for x,n in occupants.items():
                    for y in (x,(x+1)%6):
                        if y in allowed:
                            following[y]+=n
                occupants=following
            table.append([occupants[q] for q in (2,4,0)])
        return table
    clean=matrix(rows)
    require(clean==[[1,0,0],[0,1,0],[0,0,1]], "macro did not isolate the three wires")
    rows[1].add(0)
    damaged=matrix(rows)
    require(damaged[2][0]>0, "leak failed to introduce wrong-wire path")
    return dict(tick=2, added_deficit=0, source_deficits=[0,2,4], final_deficits=[2,4,0],
                clean=clean, damaged=damaged)


def checks():
    macros=isolated_macros()
    reports=[]
    for m in (3,4,5,6,7,8,9,11,16):
        bins=[(s,j) for s in (1,-1) for j in range(m)]
        checks=[]
        for start in [0,4*m-1]:
            for target in range(4*m) if m<=4 else (0,4*m-1):
                for r,l in (([],[]), (bins,bins[::-1]), ([(1,0),(-1,0),(1,0)],[(-1,m-1)]*2)):
                    checks.append(run(m,r,l,target,start)["ticks"])
        reports.append(dict(M=m,cases=len(checks),longest=max(checks)))
    require([r["cases"] for r in reports] == [72,96,12,12,12,12,12,12,12], "coverage")
    sample=run(3,[(1,0),(1,0),(-1,2)],[(-1,1),(1,1)],11,11)
    return dict(macros=macros,reports=reports, seam_example=sample, leakage=leaking_macro(macros))


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory",type=Path)
    directory=parser.parse_args().directory
    result=checks()
    directory.mkdir(parents=True,exist_ok=True)
    with (directory/"compact_residue_preparation.json").open("x",encoding="utf8",newline="\n") as out:
        json.dump(result,out,separators=(",",":"))
        out.write("\n")
