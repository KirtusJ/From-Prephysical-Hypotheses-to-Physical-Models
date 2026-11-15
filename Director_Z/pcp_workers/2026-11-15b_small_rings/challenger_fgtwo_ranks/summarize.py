#!/usr/bin/env python3
"""summarize.py RUNDIR: one line per result file (carrier N M r k L L0 states bound unknowns rank |P| P2cos dimproj pred P2 P3 P0)."""
import json, glob, sys, os
print('carrier N M r k L L0 states boundhit unknowns rankA |P| P_twocos dim_proj pred P2 P3 P0fail')
for f in sorted(glob.glob(os.path.join(sys.argv[1], 'res_*.json'))):
    try:
        r = json.load(open(f))
    except Exception as e:
        print(os.path.basename(f), 'UNREADABLE', e); continue
    if not r['P1_qualifies']:
        print(r['carrier'], r['N'], r['M'], 'NOT QUALIFYING s=%d' % r['s']); continue
    print(*[r.get(k) for k in ['carrier','N','M','r','k','L','L0','states','P4_state_bound_hit','unknowns','rank_A','P_size','P_keys_meeting_two_delta_cosets','dim_proj_P','predicted_dim_on_P','P2_pass','P3_pass','P0_coset_failures']])
