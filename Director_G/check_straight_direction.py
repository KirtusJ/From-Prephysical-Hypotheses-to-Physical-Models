"""Direct microscopic and logical signed histograms for the straight-pair encoding.

Run python -B check_straight_direction.py NEW_DIRECTORY. No packages required.
"""
import argparse
import json
from collections import Counter
from itertools import product
from pathlib import Path


def require(value,message):
    if not value:
        raise ValueError(message)


def tick(rows,size,order,allow):
    out=Counter()
    for (x,r,g,s),n in rows.items():
        for d,dx in (("R",1),("L",-1)):
            y=(x+dx)%size
            if allow(y,d):
                out[y,d,(g+x//2)%order,-s if r==d=="L" else s]+=n
    return out


def census(m,a,initial,word):
    n=4*m
    actual=Counter({(2*a,initial,0,1):1})
    logical=Counter({(a,initial,0,1):1})
    prefix_counts=[]
    for j,rail in enumerate(word):
        base=(2*(a+j))%4
        wanted={(base+dx)%4 for d,dx in (("R",1),("L",-1)) if rail in ("*",d)}
        actual=tick(actual,4*n,n,lambda x,d:x%4 in wanted)
        actual=tick(actual,4*n,n,lambda x,d:x%4==(base+2)%4)
        logical=tick(logical,2*n,m,lambda x,d:rail in ("*",d))
        prefix_counts.append(sum(actual.values()))
        require(prefix_counts[-1]==sum(logical.values()),"lost or added lineage")
    t=len(word)
    offsets=2*sum((a+j)%2 for j in range(t))
    expect=Counter()
    for (x,r,g,s),count in logical.items():
        left_n=(a+t-x)//2
        sign=-s if left_n%2 else s
        expect[2*x,r,(4*g+offsets-left_n)%n,sign]+=count
    require(actual==expect,"signed cyclic gain histogram")
    return dict(order=m,N=n,a=a,initial=initial,rails=word,
                live_histories_by_logical_tick=prefix_counts,
                terminal_cells=len(actual),microclock=2*t,
                raw_histogram=[[*k,c] for k,c in sorted(actual.items())] if m==3 and a==0 and
                initial=="R" and len(word)<=6 else None)


def projected_ring(m,double):
    size=(8 if double else 4)*m
    rows=Counter({(0,"R",0,1):1})
    for t in range(1,2*m+1):
        allowed={t%size,(-t)%size}
        rows=tick(rows,size,m,lambda x,d:x in allowed)
    sites={(2*m+1)%size,(-2*m+1)%size}
    rows=tick(rows,size,m,lambda x,d:x in sites and d=="R")
    signed=Counter()
    for (x,r,g,s),n in rows.items():
        signed[x,r]+=s*n
    return sum(v*v for v in signed.values())


def run():
    tests=[]
    for m in (3,4,5,6):
        schedules=["*","L","R","*L*R**","RRLL", "L"*4, "*"*(8*m+1)]
        for a,rail,mask in product((0,1,8*m-1),"RL",schedules):
            tests.append(census(m,a,rail,mask))
    rings=[[m,projected_ring(m,False),projected_ring(m,True)] for m in (3,4,5,6)]
    require(all((x,y)==(0,2) for m,x,y in rings),"double-cover control")
    return dict(panels=tests,antipodal_control_ring4M_ring8M=rings)


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory",type=Path)
    directory=parser.parse_args().directory
    outfile=directory/"straight_direction.json"
    if outfile.exists():
        parser.exit(2,f"Refusing to overwrite {outfile}\n")
    result=run()
    directory.mkdir(parents=True,exist_ok=True)
    with outfile.open("x",encoding="utf8",newline="\n") as f:
        json.dump(result,f,separators=(",",":"))
        f.write("\n")
