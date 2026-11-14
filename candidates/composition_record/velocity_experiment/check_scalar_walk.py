"""Site effects of synchronized H/I schedules. Exact integers, no external dependencies.

Default: verify and print all named effects, including dark sites. --search
replays limited clock/ring enumeration. --qasm NEW_FILE exports the
ten-tick geometric ring protocol; --eight-tick exports a shorter alternative
and --all-scalar selects the twelve-tick ring with a completely scalar site
POVM. The emitted QASM example initializes the coin in R.
"""
import argparse
from itertools import product
from pathlib import Path


ZERO = (0,0,0)
LINE = "HIHHIIHIIIHI"
GEOMETRIC = "HIIHHHHHII"
EIGHT = "HHHIHIIH"
ALL_SCALAR = "HHHIIHIHHIIH"
SMALL_SCALAR = "HIIHHIHHII"
CASES = ((LINE,None),(GEOMETRIC,16),(EIGHT,16),("HIHHHHHI",12),("HHHIHIHHIIIII",7),
         (SMALL_SCALAR,12),(ALL_SCALAR,16))


def require(ok,reason):
    if not ok:
        raise ValueError(reason)


def kernels(word):
    """Ordered x=-t,-t+2,...,t; two initial coin columns in every 2x2 matrix."""
    table=[(1,0,0,1)]
    for op in word:
        out=[[0,0,0,0] for _ in range(len(table)+1)]
        for i,(a,b,c,d) in enumerate(table):
            if op=="H":
                a,b,c,d=a+c,b+d,a-c,b-d
            out[i+1][:2]=a,b
            out[i][2:]=c,d
        table=out
    return table


def gram(a,b,c,d):
    return a*a+c*c,a*b+c*d,b*b+d*d


def effects(word,length,table=None):
    if table is None:
        table=kernels(word)
    t=len(word)
    domain=range(-t,t+1) if length is None else range(length)
    sums={x:[0]*4 for x in domain}
    for k,row in enumerate(table):
        x=2*k-t
        target=sums[x if length is None else x%length]
        for i in range(4):
            target[i]+=row[i]
    return {x:gram(*row) for x,row in sums.items()}


def enumerate_paths(word,length):
    """Independent oracle branches only at an H. Ring paths combine
    coherently at their final residue, prior to squaring the rail sums."""
    t=len(word)
    sites=range(-t,t+1) if length is None else range(length)
    mats={x:[0]*4 for x in sites}
    for src in (0,1):
        for moves in product((0,1),repeat=word.count("H")):
            h=iter(moves)
            rail=src
            sign=1
            x=0
            for op in word:
                next_rail=next(h) if op=="H" else rail
                if op=="H" and next_rail==rail==1:
                    sign=-sign
                rail=next_rail
                x+=1-2*rail
            mats[x if length is None else x%length][2*rail+src]+=sign
    return {x:gram(*row) for x,row in mats.items()}


def positive(a,b,d):
    return a>0 and a*d>b*b


def scalar_levels(board):
    levels=sorted({a for a,b,d in board.values() if a==d and b==0 and a>0})
    if len(levels)<3:
        return []
    peak=levels[-1]
    # Strict dominance outside the scalar maximum class for every complex
    # input, including mixed states: peak*I - E_x positive definite.
    if all((a,b,d)==(peak,0,peak) or positive(peak-a,-b,peak-d)
           for a,b,d in board.values()):
        return levels
    return []


def check(word,length):
    board=effects(word,length)
    require(board==enumerate_paths(word,length),"independent column/sign replay")
    unit=2**word.count("H")
    require(tuple(map(sum,zip(*board.values())))==(unit,0,unit),"effect completeness")
    require(all(a>=0 and d>=0 and a*d>=b*b for a,b,d in board.values()),"positive effects")
    levels=scalar_levels(board)
    require(levels,"missing scalar levels or unproved strict maximum")
    print(f"{word}, {'line' if length is None else 'ring '+str(length)}, "
          f"denominator={unit}, scalar levels={levels}")
    print("  x:(RR,RL,LL)", " ".join(f"{x}:{e}" for x,e in board.items()))
    if word==LINE:
        require(levels==[2,4,8] and board[0]==(8,0,8)
                and board[-2]==board[2]==(4,0,4)
                and board[-8]==board[8]==(2,0,2),"line witness")
    if word==GEOMETRIC:
        require(levels==[2,8,32] and board[8]==(32,0,32)
                and board[0]==(8,0,8) and board[4]==board[12]==(2,0,2),"ring witness")
    if word==EIGHT or length in (7,12):
        require(all(e==ZERO or positive(*e) for e in board.values()),"non-dark site singular")
    if length==7:
        require(all(positive(*e) for e in board.values()),"dark physical site on odd ring")
    if word in (SMALL_SCALAR, ALL_SCALAR):
        expected=([0,2,10,8,10,2] if word==SMALL_SCALAR else [58,10,2,10,26,10,2,10])
        require(all(board[x]==((expected[x//2],0,expected[x//2]) if x%2==0 else ZERO)
                    for x in range(length)),"all scalar site effect table")
    return board


def schedules():
    """Reproduce only the stated finite exclusions. For horizon t every
    larger L>2t has the line effects on its light cone, so one such ring
    represents all larger rings for the maximum/level test."""
    for t in range(1,12):
        for coins in product("HI",repeat=t):
            word="".join(coins);table=kernels(word)
            require(not scalar_levels(effects(word,None,table)),"shorter line schedule")
            if t<8:
                for length in range(3,2*t+2):
                    require(not scalar_levels(effects(word,length,table)),"shorter ring schedule")
            if t==8:
                for length in range(3,12):
                    require(not scalar_levels(effects(word,length,table)),"smaller eight-tick ring")
    print("Bounded search: no matching line schedule through 11 ticks; "
          "no ring schedule through 7 ticks, or below 12 sites at 8 ticks.")


def exported(word,blocks=1):
    # q[0] coin; q[1:3] low through high address bits. High carry must be
    # computed before lower bits change. y counts left steps modulo eight.
    lines=['OPENQASM 3.0;','include "stdgates.inc";','qubit[4] q;',f'bit[{3*blocks}] site_code;']
    for block in range(blocks):
        for gate in word:
            if gate=="H":
                lines.append('h q[0];')
            lines += ['ctrl(3) @ x q[0], q[1], q[2], q[3];',
                      'ccx q[0], q[1], q[2];','cx q[0], q[1];']
        if blocks>1:
            lines.append('barrier q;')
        lines += [f'site_code[{3*block+j}] = measure q[{j+1}];' for j in range(3)]
        if blocks>1:
            lines.append('barrier q;')
    return "\n".join(lines)+"\n"


def check_export(word,text):
    instructions=text.splitlines()[4:]
    require(instructions[-3:]==[f'site_code[{j}] = measure q[{j+1}];' for j in range(3)],
            "terminal address-only measurement")
    cols={}
    for src in (0,1):
        amp={src:1}
        for instr in instructions[:-3]:
            out={}
            for i,a in amp.items():
                if instr=='h q[0];':
                    ki=i&~1;out[ki]=out.get(ki,0)+a
                    ki=i|1;out[ki]=out.get(ki,0)+(-a if i&1 else a)
                    continue
                if instr.startswith('ctrl(3) @ x '):
                    require(instr=='ctrl(3) @ x q[0], q[1], q[2], q[3];',"high carry")
                    ki=i^(8 if i&7==7 else 0)
                elif instr=='ccx q[0], q[1], q[2];':
                    ki=i^(4 if i&3==3 else 0)
                elif instr=='cx q[0], q[1];':
                    ki=i^(2 if i&1 else 0)
                else:
                    raise ValueError(instr)
                out[ki]=out.get(ki,0)+a
            amp=out
        cols[src]=amp
    board=effects(word,16)
    for y in range(8):
        x=(len(word)-2*y)%16
        require(gram(*(cols[s].get(2*y+r,0) for r in (0,1) for s in (0,1)))==board[x],
                "exported register effect differs from physical ring")


def check_two_blocks():
    """Execute the actual exported 2-block syntax, split branches on writes,
    and keep both *signed* initial columns. The independent oracle uses
    signed infinite-line kernels folded coherently to the physical ring.
    """
    word=ALL_SCALAR
    lines=exported(word,2).splitlines()
    require(lines[3]=='bit[6] site_code;', "two distinct address registers in classical bits")
    offsets=[j for j,line in enumerate(lines) if ' = measure ' in line]
    require([lines[j] for j in offsets]==[
        f'site_code[{k}] = measure q[{1+k%3}];' for k in range(6)], "chronological absolute bits")
    columns=[]
    for src in (0,1):
        amps={(0,src):1}
        for instruction in lines[4:]:
            nxt={}
            def collect(rec,basis,amplitude):
                state=rec,basis
                nxt[state]=nxt.get(state,0)+amplitude
            for (record,basis),amp in amps.items():
                if instruction=='h q[0];':
                    collect(record,basis & ~1,amp)
                    collect(record,basis | 1,-amp if basis&1 else amp)
                elif instruction=='ctrl(3) @ x q[0], q[1], q[2], q[3];':
                    collect(record,basis^(8 if basis&7==7 else 0),amp)
                elif instruction=='ccx q[0], q[1], q[2];':
                    collect(record,basis^(4 if basis&3==3 else 0),amp)
                elif instruction=='cx q[0], q[1];':
                    collect(record,basis^(2 if basis&1 else 0),amp)
                elif instruction=='barrier q;':
                    collect(record,basis,amp)
                elif '] = measure q[' in instruction:
                    left,right=instruction[:-2].split('] = measure q[')
                    target=int(left[len('site_code['):])
                    collect(record | (((basis>>int(right))&1)<<target),basis,amp)
                else:
                    raise ValueError(instruction)
            amps=nxt
        columns.append(amps)
    route=[[0]*4 for _ in range(16)]
    for j,row in enumerate(kernels(word)):
        x=(2*j-len(word))%16
        route[x]=[a+b for a,b in zip(route[x],row)]
    expected=[58,10,2,10,26,10,2,10]
    for y1,y2 in product(range(8),repeat=2):
        record=y1+8*y2
        x=(len(word)-2*y1)%16
        dx=(len(word)-2*((y2-y1)%8))%16
        a,b,c,d=route[dx];e,f,g,h=route[x]
        signed=[a*e+b*g,a*f+b*h,c*e+d*g,c*f+d*h]
        actual=[columns[src].get((record,2*y2+r),0) for r in (0,1) for src in (0,1)]
        require(actual==signed, "signed post-write state across two blocks")
        mass=expected[x//2]*expected[dx//2]
        require(gram(*actual)==(mass,0,mass),"all 64 initial-coin-independent joint probabilities")
    require(all((basis//2)==(record>>3) or amp==0
                for board in columns for (record,basis),amp in board.items()),"final address mismatch")
    print("Two-block exported record verified: all 64 chronological pairs and both signed source columns.")


def compare_which_way():
    """Write position after every tick. The incoming rail is sharp after
    every conditional shift; I preserves it, H supplies a fair sign.
    Check every endpoint against a separate enumeration of all 128
    equal-weight direction choices at H; deterministic I ticks also move.
    """
    counts={(0,0):1}
    for gate in ALL_SCALAR:
        out={}
        for (x,r),count in counts.items():
            for nxt in ((0,1) if gate=="H" else (r,)):
                dest=((x+1-2*nxt)%16,nxt)
                out[dest]=out.get(dest,0)+count
        counts=out
    terminal=[sum(counts.get((x,r),0) for r in (0,1)) for x in range(16)]
    enumerated=[0]*16
    for signs in product((-1,1),repeat=ALL_SCALAR.count("H")):
        it=iter(signs)
        direction=1
        x=0
        for gate in ALL_SCALAR:
            if gate=="H":
                direction=next(it)
            x+=direction
        enumerated[x%16]+=1
    require(terminal==enumerated and terminal[::2]==[18,18,16,14,14,14,16,18],
            "tick-resolved ring probabilities")
    require(terminal[1::2]==[0]*8 and sum(terminal)==128,"all tick-resolved cells")
    coherent=effects(ALL_SCALAR,16)
    require(sum(abs(coherent[x][0]-terminal[x]) for x in range(16))==104,
            "total variation between the two ordinary experiments")
    print("Tick-resolved sharp-R site numerators at even sites:",terminal[::2],
          "over 128; total variation from end-only read = 13/32.")


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--search",action="store_true")
    parser.add_argument("--qasm",type=Path,help="write one new OpenQASM 3 file")
    parser.add_argument("--blocks",type=int,default=1,
                        help="repeat the all-scalar word; absolute y at block j occupies bits 3j..3j+2 (j starts at 0)")
    variants=parser.add_mutually_exclusive_group()
    variants.add_argument("--eight-tick",action="store_true",help="export the eight-tick 16-site option")
    variants.add_argument("--all-scalar",action="store_true",help="export the all-scalar 16-site option")
    args=parser.parse_args()
    if args.blocks<1 or (args.blocks>1 and not args.all_scalar):
        parser.error("--blocks must be positive; more than one requires --all-scalar")
    for word,length in CASES:
        check(word,length)
    for word in (GEOMETRIC,EIGHT,ALL_SCALAR):
        check_export(word,exported(word))
    check_two_blocks()
    compare_which_way()
    if args.search:
        schedules()
    if args.qasm:
        with args.qasm.open('x',encoding='ascii',newline='\n') as f:
            selection=ALL_SCALAR if args.all_scalar else (EIGHT if args.eight_tick else GEOMETRIC)
            f.write(exported(selection,args.blocks))


if __name__=="__main__":
    main()
