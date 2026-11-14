"""run2.py -- larger lengths, line only, variants V0 (F independent of vertex), V1 (F depends on direction).
Predicates as in build_prod.py (P1,P2,P3,P7). Output: per run the list of excess by L. Result file mode 'x'."""
import sys, json, time
from build_prod import analyse
f = open(sys.argv[1], 'x'); res = []
cfg = [(None, T) for T in (6,7,8)] + [(k, T) for k in (1,2,3,4) for T in (7,8,9,10)]
for mode in ('vertex', 'position'):
    for (k, T) in cfg:
        if mode == 'position' and k is not None: continue
        for var in ('V0', 'V1'):
            t0 = time.time()
            out, car, raw, flen = analyse(None, mode, k, T, var)
            line = {'mode': mode, 'k': k, 'T': T, 'var': var, 'states': out['one_position_states'],
                    'P1': [out['P1_tested'], out['P1_pass']], 'unknowns': out['unknowns'], 'nullity': out['nullity'],
                    'unknowns_by_L': [b['unknowns'] for b in out['by_L']],
                    'excess_by_L': [b['excess'] for b in out['by_L']], 'sec': round(time.time()-t0,1)}
            res.append(line); print(json.dumps(line), flush=True)
json.dump(res, f, indent=1); f.close()
