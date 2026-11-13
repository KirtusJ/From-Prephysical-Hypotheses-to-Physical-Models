import json,glob,math,statistics as st,os,sys
R='/home/user/From-Prephysical-Hypotheses-to-Physical-Models/'
files=sorted(glob.glob(R+'Z4_COMPUTATION/**/*.json',recursive=True)+glob.glob(R+'Director_Z_cross_review/*.json'))
ncols=0;flags=[];fails=[];nan=[];contra=[]
KW=("residual","defect","error","difference","violation")
def isnum(v): return isinstance(v,(int,float)) and not isinstance(v,bool)
def walk(o,path,f,passed=None):
    if isinstance(o,dict):
        if 'passed' in o:
            passed=o['passed']
            if o['passed'] is False: fails.append((f,path))
        for k,v in o.items():
            if isinstance(v,float) and (math.isnan(v) or math.isinf(v)): nan.append((f,path+'/'+k,v))
            walk(v,path+'/'+k,f,passed)
        # contradiction
        if passed:
            for k,v in o.items():
                if isnum(v) and 'dimension' in k:
                    for k2,v2 in o.items():
                        if 'expected' in k2 and isnum(v2) and v!=v2 and ('dimension' in k2 or k2=='expected'):
                            contra.append((f,path,k,v,k2,v2))
    elif isinstance(o,list):
        rows=[r for r in o if isinstance(r,dict)]
        if len(rows)>=5: cols(rows,path,f)
        for i,v in enumerate(o):
            if isinstance(v,float) and (math.isnan(v) or math.isinf(v)): nan.append((f,path+f'[{i}]',v))
            walk(v,path+f'[{i}]',f,passed)
def cols(rows,path,f):
    global ncols
    keys={}
    for i,r in enumerate(rows):
        for k,v in r.items():
            if isnum(v) and math.isfinite(v): keys.setdefault(k,[]).append((i,v))
    for k,iv in keys.items():
        if len(iv)<5: continue
        ncols+=1
        vals=[v for _,v in iv]; med=st.median(vals)
        mad=st.median([abs(v-med) for v in vals])*1.4826
        if mad>0:
            for i,v in iv:
                z=abs(v-med)/mad
                if z>4: flags.append((z,'MAD',f,path,i,k,v,med))
        elif len(set(vals))>1:
            for i,v in iv:
                if v!=med: flags.append((float('inf'),'MAD0',f,path,i,k,v,med))
        if any(w in k.lower() for w in KW):
            a=[abs(v) for v in vals]; m=st.median(a); mx=max(a)
            if mx>0 and mx>100*m:
                i=[i for i,v in iv if abs(v)==mx][0]
                flags.append((mx/m if m else float('inf'),'RES100',f,path,i,k,mx,m))
for f in files:
    walk(json.load(open(f)),'',os.path.basename(f))
print('files',len(files),'cols',ncols,'flags',len(flags))
print('NAN',nan);print('CONTRA',contra)
print('FAILS');[print(' ',x) for x in fails]
flags.sort(key=lambda x:-x[0] if math.isfinite(x[0]) else -1e300)
from collections import Counter
c=Counter((x[1],x[2],x[3],x[5]) for x in flags)
print('FLAG GROUPS');[print(' ',n,k) for k,n in c.most_common(60)]
json.dump(flags,open(sys.argv[1],'w'))
