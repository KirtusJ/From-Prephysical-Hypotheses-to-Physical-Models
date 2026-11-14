"""Generate and check eight OpenQASM 3 circuits using only Python's stdlib."""
import argparse
import csv
import json
from itertools import product
from pathlib import Path


PROLOGUE = ('OPENQASM 3.0;', 'include "stdgates.inc";', 'qubit[3] q;', 'bit[6] record;')
H = 'h q[0];'
CCX = 'ccx q[0], q[1], q[2];'
CX = 'cx q[0], q[1];'
PATTERNS = tuple(product((1, -1), repeat=2))
WORDS = tuple(product(range(4), repeat=3))


def require(value, message):
    if not value:
        raise ValueError(message)


def circuit(source, signs):
    lines = list(PROLOGUE)
    if source == 1:
        lines.append('x q[0];')
    for clock in range(3):
        for _ in range(3):
            lines.extend((H, CCX, CX))
        lines.append('barrier q;')
        for bit in (0, 1):
            lines.append(f'record[{2*clock+bit}] = measure q[{bit+1}];')
        lines.append('barrier q;')
        if clock < 2:
            lines.append(('s' if signs[clock] == 1 else 'sdg') + ' q[0];')
    return '\n'.join(lines) + '\n'


def add(state, index, value):
    state[index] = state.get(index, 0) + value


def execute(qasm):
    """Interpret emitted statements, including measured bit targets and gate order.

    All amplitudes omit the same factor 2^-9/2. Double-precision complex
    numbers exactly represent the small Gaussian integers in this circuit.
    """
    lines = qasm.splitlines()
    require(tuple(lines[:4]) == PROLOGUE, 'unexpected declaration')
    branches = {0: {0: 1}}
    for instr in lines[4:]:
        if instr == 'barrier q;':
            continue
        nxt = {}
        for record, state in branches.items():
            for i, amp in state.items():
                board = nxt.setdefault(record, {})
                coin = i & 1
                if instr == H:
                    add(board, i & ~1, amp)
                    add(board, i | 1, -amp if coin else amp)
                elif instr == CCX:
                    add(board, i ^ (4 if i & 3 == 3 else 0), amp)
                elif instr == CX:
                    add(board, i ^ (2 if coin else 0), amp)
                elif instr == 'x q[0];':
                    add(board, i ^ 1, amp)
                elif instr in ('s q[0];', 'sdg q[0];'):
                    add(board, i, amp * ((1j if instr == 's q[0];' else -1j) if coin else 1))
                elif instr.startswith('record[') and '] = measure q[' in instr:
                    target, sensor = instr[:-2].split('] = measure q[')
                    bit, qubit = int(target[len('record['):]), int(sensor)
                    require(0 <= bit < 6 and qubit in (1, 2), 'measurement index')
                    output = record | (((i >> qubit) & 1) << bit)
                    add(nxt.setdefault(output, {}), i, amp)
                else:
                    raise ValueError(f'unsupported statement: {instr}')
        branches = nxt
    probs = {}
    for a, b, c in WORDS:
        board = branches.get(a + 4*b + 16*c, {})
        power = sum(z.real*z.real + z.imag*z.imag for z in board.values())
        require(power == int(power), 'noninteger weight in exact small circuit')
        probs[a, b, c] = int(power)
    require(sum(probs.values()) == 512, 'nine-tick squared norm')
    return probs


def displacement(word):
    previous = 0
    result = []
    for y in word:
        result.append(3 - 2*((y-previous) % 4))
        previous = y
    return tuple(result)


def path_law(source, signs):
    """Enumerate 512 signed line walks from a source, with independent
    block displacements. Histories with different retained records or
    final coin do not interfere. None requests exact rail dephasing.
    """
    cells = {}
    for moves in product((1, -1), repeat=9):
        current = 1 if source == 0 else -1
        gain = 1
        saved = []
        for i, next_direction in enumerate(moves):
            if current == next_direction == -1:
                gain = -gain
            current = next_direction
            if i in (2, 5):
                if signs is None:
                    saved.append(current)
                elif current == -1:
                    gain *= signs[i//3] * 1j
        d = tuple(sum(moves[k:k+3]) for k in (0,3,6))
        add(cells, (d,current,*saved), gain)
    law = {displacement(word):0 for word in WORDS}
    for (d,*_),z in cells.items():
        law[d] += int(z.real*z.real + z.imag*z.imag)
    return {word:law[displacement(word)] for word in WORDS}


def turns(law, i, j):
    same = sum(w for word,w in law.items() if displacement(word)[i]*displacement(word)[j]>0)
    # Each flight has three ticks, so its displacement is odd and never zero.
    return same, sum(law.values())-same


def adjacent(law, pair):
    out = {}
    for word, mass in law.items():
        d = displacement(word)
        add(out, d[pair:pair+2], mass)
    return out


def verify():
    laws = {}
    for source in (0,1):
        dephased = path_law(source,None)
        for signs in PATTERNS:
            emitted = circuit(source,signs)
            actual = execute(emitted)
            require(actual == path_law(source,signs), 'word mismatch with signed line paths')
            laws[source,signs] = actual
        for word in WORDS:
            require(sum(laws[source,s][word] for s in PATTERNS)==4*dephased[word],
                    'independent sign randomization did not dephase')
            require(laws[source,(1,1)][word] == laws[source,(-1,-1)][word]
                    and laws[source,(1,-1)][word] == laws[source,(-1,1)][word],
                    'joint phase conjugation')
    baseline = None
    for signs in PATTERNS:
        law = {w:sum(laws[source,signs][w] for source in (0,1)) for w in WORDS}
        equal = signs[0]==signs[1]
        pair = adjacent(law, 0)
        if baseline is None:
            baseline = pair
        require(pair == adjacent(law, 1) == baseline, 'complete adjacent displacement tables')
        require(turns(law,0,1)==turns(law,1,2)==(640,384),'adjacent source mixture')
        require(turns(law,0,2)==((512,512) if equal else (640,384)), 'lag-two control')
    return laws


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',type=Path,help='create a new directory for eight .qasm files and the full CSV')
    ap.add_argument('--ideal-counts',type=Path,help='write a new JSON input for analyze_counts.py')
    opts=ap.parse_args()
    dest=opts.output
    laws=verify()
    if dest is not None:
        dest.mkdir(parents=True,exist_ok=False)
        with (dest/'ideal_words.csv').open('x',newline='',encoding='ascii') as f:
            writer=csv.writer(f,lineterminator='\n')
            writer.writerow(('source','phase1','phase2','y3','y6','y9','rec5_to_rec0',
                             'displacement1','displacement2','displacement3','count','denominator'))
            for (source,signs),law in laws.items():
                ch='R' if source==0 else 'L'
                tags=tuple('S' if s==1 else 'Sdg' for s in signs)
                (dest/f'{ch}_{tags[0]}_{tags[1]}.qasm').write_bytes(circuit(source,signs).encode('ascii'))
                for (a,b,c),count in law.items():
                    mask=a+4*b+16*c
                    writer.writerow((ch,*tags,a,b,c,f'{mask:06b}',*displacement((a,b,c)),count,512))
    if opts.ideal_counts is not None:
        arms=[]
        for (source,signs),law in laws.items():
            tags=tuple('S' if s==1 else 'Sdg' for s in signs)
            arms.append({'source':'R' if source==0 else 'L','phase1':tags[0],'phase2':tags[1],
                         'attempts':512,'counts':{f'{a+4*b+16*c:06b}':w for (a,b,c),w in law.items()}})
        with opts.ideal_counts.open('x',encoding='utf8') as f:
            json.dump({'schema':'velocity-history-counts-v1','provenance':'ideal','arms':arms},f,indent=2)
            f.write('\n')
    print('Verified 8 circuits, 64 chronological words per circuit, and exact independently dephased control.')
    print('Equal R/L mixture; same endpoint sign: equal pulses 1/2, opposite pulses 5/8, independent 9/16.')


if __name__=='__main__':
    main()
