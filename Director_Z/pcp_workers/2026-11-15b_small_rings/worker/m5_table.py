#!/usr/bin/env python3
"""Tick tables of the M = 5 gadgets (finite check G2 of m5_schedule.py, written out).
PREDICATE (fixed before the run): every tick of every gadget, started from its boundary
configuration, is exclusive (required and excluded residues disjoint mod 5), packets stay at
distinct residues except the declared merge, and the gadget returns to its boundary
(positions relative to S and rails).  Usage: m5_table.py OUTFILE
"""
import sys, json
sys.path.insert(0, __import__('os').path.dirname(__file__))
import m5_schedule as m

M = 5
G = dict(m.search_gadgets(('L', 'R', 'R'), 8))
G['trans'] = m.trans_search('RRR', 'LRR', 8)
lines, allok = [], True

def run(name, start, rails, ticks, merge_tick=None, split_kind=None):
    global allok
    pk = dict(start); rl = dict(rails)
    lines.append(f'## {name}: start {pk} rails {rl}')
    for t, mv in enumerate(ticks):
        ok, req = m.excl_ok(pk, mv)
        exc = set()
        for n, e in pk.items():
            if mv[n] == 'R': exc.add((e + 1) % M)
            if mv[n] == 'L': exc.add(e % M)
            if mv[n] == 'X': exc |= {e % M, (e + 1) % M}
        new = {}
        for n, e in pk.items():
            if mv[n] == 'R': new[n] = e; rl[n] = 'R'
            elif mv[n] == 'L': new[n] = e + 1; rl[n] = 'L'
            elif mv[n] == 'S':
                if split_kind == 'X': new[n] = e; rl[n] = 'R'      # right part stays source
                else: new[n] = e + 1; rl[n] = 'L'                  # left part is the source
        res = [e % M for e in new.values()]
        distinct = len(set(res)) == len(res)
        allok &= ok
        lines.append(f'  tick {t+1}: pos {pk} moves {mv} required {sorted(req)} excluded {sorted(exc)} exclusive={ok} distinct_after={distinct}')
        pk = new
    s = pk.get('S', 0)
    rel = {n: e - s for n, e in pk.items()}
    lines.append(f'  end: relative {rel} rails {rl}')
    return rel, rl

alpha = {'S': 0, 'X': 1, 'Y': -2}; rho = {'S': 'L', 'X': 'R', 'Y': 'R'}
for name in ('adv', 'depX', 'depY'):
    path = G[name] if name == 'adv' else G[name][0]
    ticks = [{'S': a, 'X': b, 'Y': c} for (a, b, c) in path]
    rel, rl = run(name, alpha, rho, ticks, split_kind=name[-1] if name != 'adv' else None)
    back = rel == {'S': 0, 'X': 1, 'Y': -2} and rl == rho
    allok &= back
    lines.append(f'  returns to ALPHA(LRR): {back}; increments (dS,dX,dY,stage,copy) = {G[name][1] if name != "adv" else "(1,0,0)"}')
ticks = [{'S': a, 'X': b, 'Y': c} for (a, b, c) in G['trans']]
rel, rl = run('trans (phase P end -> ALPHA)', alpha, {'S': 'R', 'X': 'R', 'Y': 'R'}, ticks)
allok &= (rel == {'S': 0, 'X': 1, 'Y': -2} and rl['S'] == 'L' and rl['Y'] == 'R')
run('remove', alpha, rho, [{'S': 'X', 'X': 'L', 'Y': 'R'}])
run('phase P adv (P at +3, P-low -2)', {'S': 0, 'Y': 3}, {'S': 'R', 'Y': 'R'},
    [{'S': a, 'Y': b} for a, b in zip('LLRR', 'LRLR')])
txt = '\n'.join(lines) + f'\nALL_OK={allok}\n'
open(sys.argv[1], 'x').write(txt)
print(txt)
