import json,sys
R='/home/user/From-Prephysical-Hypotheses-to-Physical-Models/'
fl=json.load(open(sys.argv[1]))
want=['oddness_defect','residual_of_X','least_residual_of_even_characters','residual_of_odd_characters','largest_defect_of_conjugate_rules','largest_defect_of_scalar_fit','residual_averaged_ray_with_offset','return_probability','trivial_gains_quadratic_defect','solution_dimension','weight_outside','distance','product_imag','rms_band_velocity','mean_scaled_position']
import glob,os
seen=set()
for z,kind,f,path,i,k,v,med in fl:
    if k not in want: continue
    key=(f,path,i)
    p=glob.glob(R+'*/'+f)[0]; o=json.load(open(p))
    cur=o
    import re
    for part in path.strip('/').split('/'):
        m=re.match(r'(.*)\[(\d+)\]$',part)
        cur=cur[m.group(1)][int(m.group(2))] if m else cur[part]
    row=cur[i]
    s=json.dumps({a:b for a,b in row.items() if not isinstance(b,(list,dict))})[:420]
    print(f"{kind} z={z:.3g} {f[:38]} {path.split('/')[1][:30]} #{i} {k}={v:.4g} med={med:.4g}")
    if key not in seen: print('    ',s)
    seen.add(key)
