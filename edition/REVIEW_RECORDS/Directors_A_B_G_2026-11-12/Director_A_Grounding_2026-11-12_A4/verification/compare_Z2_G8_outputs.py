#!/usr/bin/env python3
"""Compare supplied and rerun Z2 G8 numerical JSON. Explicit resolved paths required."""
from pathlib import Path
import argparse,hashlib,json
p=argparse.ArgumentParser();p.add_argument('--original',type=Path,required=True);p.add_argument('--rerun',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
BASE=a.original.expanduser().resolve(strict=True);REPRO=a.rerun.expanduser().resolve(strict=True);OUT=a.out.expanduser().resolve()
A=json.loads(BASE.read_text());B=json.loads(REPRO.read_text());changes=[]
def traverse(x,y,path='$'):
 if type(x) != type(y):changes.append({'path':path,'original':x,'reexecution':y,'type':'type'});return
 if isinstance(x,dict):
  if set(x)!=set(y):changes.append({'path':path,'key_difference':[sorted(set(x)-set(y)),sorted(set(y)-set(x))]})
  for k in sorted(set(x)&set(y)):traverse(x[k],y[k],path+'.'+k)
 elif isinstance(x,list):
  if len(x)!=len(y):changes.append({'path':path,'lengths':[len(x),len(y)]})
  for i,(aa,bb) in enumerate(zip(x,y)):traverse(aa,bb,path+f'[{i}]')
 elif x!=y:
  record={'path':path,'original':x,'reexecution':y}
  if isinstance(x,(int,float)) and not isinstance(x,bool) and isinstance(y,(int,float)) and not isinstance(y,bool):record['abs_delta']=abs(x-y)
  changes.append(record)
traverse(A,B)
num=[x['abs_delta'] for x in changes if 'abs_delta' in x]
out={'scope':'double-precision rerun of Z2 G8 code; not a certified error bound','original_sha256':hashlib.sha256(BASE.read_bytes()).hexdigest(),'rerun_sha256':hashlib.sha256(REPRO.read_bytes()).hexdigest(),'change_count':len(changes),'numeric_change_count':len(num),'max_numeric_abs_delta':max(num) if num else 0,'all_changes':changes}
OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(out,indent=2)+'\n')
print('Z2 G8 changed scalars',len(changes),'max abs numeric delta',out['max_numeric_abs_delta'])
