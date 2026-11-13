"""Compare rerun JSON with stored JSON: max abs and max relative numeric difference per file, and non-numeric diffs."""
import json,sys
def walk(a,b,path,out):
    if isinstance(a,dict) and isinstance(b,dict):
        for k in set(a)|set(b):
            if k not in a or k not in b: out['struct'].append(path+'/'+k)
            else: walk(a[k],b[k],path+'/'+k,out)
    elif isinstance(a,list) and isinstance(b,list):
        if len(a)!=len(b): out['struct'].append(path+' len')
        for i,(x,y) in enumerate(zip(a,b)): walk(x,y,path+'/%d'%i,out)
    elif isinstance(a,bool) or isinstance(b,bool) or isinstance(a,str) or a is None or b is None:
        if a!=b: out['other'].append((path,a,b))
    else:
        d=abs(a-b)
        if d>0:
            out['n']+=1
            if d>out['abs'][0]: out['abs']=(d,path,a,b)
            # largest difference among fields the note quotes
            key=path.rsplit('/',1)[-1]
            if key in ('spinor_distance','walk_relative_separation_observable','ref_observable','classical_point_observable','compared_with_unrounded_cosine') and d>out['quoted'][0]: out['quoted']=(d,path,a,b)
for f in sys.argv[3:]:
    out={'struct':[],'other':[],'n':0,'abs':(0,),'quoted':(0,)}
    walk(json.load(open(sys.argv[1]+'/'+f)),json.load(open(sys.argv[2]+'/'+f)),'',out)
    print(f,json.dumps(out,default=str)[:1500])
