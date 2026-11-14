"""Verify all 21 prefix spectra of one prospective three-qubit circuit.
Use --qasm NEW_FILE and/or --table NEW_CSV to export. No hardware backend.
"""
import argparse
import csv
from collections import Counter, defaultdict
from functools import cmp_to_key
from itertools import product
from pathlib import Path
from runpy import run_path


BASE = run_path(str(Path(__file__).with_name("generate.py")))
require = BASE["require"]
ZERO = (0, 0, 0, 0)
ONE = (1, 0, 0, 0)


def phase(v):
    """Multiply by z=exp(i*pi/4) in the integral basis 1,z,z²,z³, z⁴=-1."""
    a,b,c,d=v
    return -d,a,b,c


def norm(v):
    """Coefficients of |v|² = A+B*sqrt(2)."""
    a,b,c,d=v
    return a*a+b*b+c*c+d*d, a*(b-d)+c*(b+d)


def add(a,b):
    return tuple(x+y for x,y in zip(a,b))


def positive(pair):
    a,b=pair
    if a>=0 and b>=0:
        return bool(a or b)
    if a<=0 and b<=0:
        return False
    return a*a>2*b*b if a>0 else 2*b*b>a*a


def compare(a,b):
    if a==b:
        return 0
    return 1 if positive((a[0]-b[0],a[1]-b[1])) else -1


def qasm():
    original=BASE["circuit"](0,(1,1))
    lines=[]
    ticks=0
    for line in original.splitlines():
        lines.append(line)
        if line==BASE["CX"]:
            ticks+=1
            if ticks%3==2:
                lines.append("t q[0];")
    require(ticks==9 and lines.count("t q[0];")==3,"placement of three T gates")
    return "\n".join(lines)+"\n"


def execute(program):
    """Independent registers: the 3-bit basis state and the six retained bits.
    All nine H denominators are common to the 64 full words.
    """
    instructions=program.splitlines()
    require(tuple(instructions[:4])==BASE["PROLOGUE"],"register sizes")
    state={(0,0):ONE}
    for instruction in instructions[4:]:
        if instruction=="barrier q;":
            continue
        out=defaultdict(lambda:ZERO)
        for (i,record),amp in state.items():
            bit=i&1
            if instruction==BASE["H"]:
                out[i&~1,record]=add(out[i&~1,record],amp)
                other=tuple(-x for x in amp) if bit else amp
                out[i|1,record]=add(out[i|1,record],other)
            else:
                if instruction==BASE["CCX"]:
                    i ^= 4 if i&3==3 else 0
                elif instruction==BASE["CX"]:
                    i ^= 2 if bit else 0
                elif instruction in ("t q[0];","s q[0];"):
                    if bit:
                        amp=phase(amp)
                        if instruction.startswith("s "):
                            amp=phase(amp)
                elif instruction.startswith("record[") and "] = measure q[" in instruction:
                    dest,src=instruction[:-2].split("] = measure q[")
                    k=int(dest[len("record["):])
                    j=int(src)
                    require(0<=k<6 and j in (1,2),"measured index")
                    record |= ((i>>j)&1)<<k
                else:
                    raise ValueError(instruction)
                out[i,record]=add(out[i,record],amp)
        state=out
    words={w:(0,0) for w in BASE["WORDS"]}
    for (_,record),amp in state.items():
        w=tuple((record>>(2*k))&3 for k in range(3))
        words[w]=add(words[w],norm(amp))
    return words


def signed_paths():
    """Infinite-line oracle. Track integer phase exponents along 512 paths,
    then form pairwise path differences: cos(pi*k/4) supplies the norm.
    This bypasses the QASM gate interpreter and its amplitude arithmetic.
    """
    groups=defaultdict(Counter)
    for path in product((1,-1),repeat=9):
        prev=1
        exponent=0
        for tick,rail in enumerate(path,1):
            if prev==rail==-1:
                exponent+=4
            if tick in (2,5,8) and rail==-1:
                exponent+=1
            if tick in (3,6) and rail==-1:
                exponent+=2
            prev=rail
        d=tuple(sum(path[t:t+3]) for t in (0,3,6))
        groups[d,prev][exponent%8]+=1
    # Twice the real part of z^k, as a pair A+B sqrt(2).
    cos2=((2,0),(0,1),(0,0),(0,-1),(-2,0),(0,-1),(0,0),(0,1))
    result=defaultdict(lambda:(0,0))
    for (d,_),counter in groups.items():
        a=b=0
        for k,n in counter.items():
            for l,m in counter.items():
                re,rt=cos2[(k-l)%8]
                a+=n*m*re
                b+=n*m*rt
        require(a%2==0 and b%2==0,"squared-norm integrality")
        result[d]=add(result[d],(a//2,b//2))
    return {w:result[BASE["displacement"](w)] for w in BASE["WORDS"]}


def ordinary_word_weights():
    """Map (y3,y6,y9) to (A,B), giving mass (A+B sqrt(2))/512. No output."""
    words=execute(qasm())
    require(words==signed_paths(),"exact emitted QASM differs from signed line history")
    return words


def verified():
    program=qasm()
    words=ordinary_word_weights()
    totals={}
    for word,weight in words.items():
        require(positive(weight),"unreachable terminal word")
        for size in range(4):
            prefix=word[:size]
            totals[prefix]=add(totals.get(prefix,(0,0)),weight)
    require(totals[()]==(512,0),"all incident launches")
    nodes=[]
    levels=Counter()
    for depth in range(3):
        for prefix in product(range(4),repeat=depth):
            children=[totals[prefix+(j,)] for j in range(4)]
            distinct=len(set(children))
            require(all(positive(w) for w in children) and distinct>=3,"prefix lacks three positive levels")
            ordered = sorted(set(children), key=cmp_to_key(compare))
            levels[depth, distinct] += 1
            nodes.append((prefix, children, (ordered[0], ordered[1], ordered[-1])))
    require(len(nodes)==21 and len(words)==64,"tree coverage")
    require(nodes[0][1]==[(64,0),(192,64),(192,-64),(64,0)],"root orientation")
    return program,nodes,levels


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--qasm",type=Path,help="write one new OpenQASM 3 file")
    parser.add_argument("--table",type=Path,help="write a new CSV with all child masses")
    args=parser.parse_args()
    program,nodes,levels=verified()
    if args.qasm:
        with args.qasm.open("x",encoding="ascii",newline="\n") as f:
            f.write(program)
    if args.table:
        with args.table.open("x",encoding="ascii",newline="") as f:
            w=csv.writer(f,lineterminator="\n")
            w.writerow(("prefix_y","child_y","A","B","incident_denominator","selected_level"))
            for prefix,children,picked in nodes:
                for j,(a,b) in enumerate(children):
                    tier=("min","middle","max")[picked.index((a,b))] if (a,b) in picked else ""
                    w.writerow(("".join(map(str,prefix)),j,a,b,512,tier))
    for depth in range(3):
        print(f"depth {depth}: {levels[depth,3]} prefixes with 3 levels; "
              f"{levels[depth,4]} with 4")
    print("Verified all 64 terminal words and all 21 prefixes; minimum distinct positive levels = 3.")


if __name__=="__main__":
    main()
