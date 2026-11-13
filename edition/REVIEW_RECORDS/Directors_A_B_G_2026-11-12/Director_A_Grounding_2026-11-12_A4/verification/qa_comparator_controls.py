#!/usr/bin/env python3
"""Cross-check comparator with identity, seven-residual, and mutation controls.
Use --original to point to the supplied Z2 G8 results JSON after extracting Z2.
"""
import argparse,json,subprocess,sys,tempfile
from pathlib import Path
root=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--original',type=Path,required=True);args=p.parse_args()
SOURCE=args.original.resolve(strict=True);RUN=root/'Gain_Graph_Pair_Measures_Results.json';TOOL=root/'compare_Z2_G8_outputs.py'
with tempfile.TemporaryDirectory() as td:
 d=Path(td);out=d/'comparison.json'
 def check(left,right):
  q=subprocess.run([sys.executable,str(TOOL),'--original',str(left),'--rerun',str(right),'--out',str(out)],capture_output=True,text=True)
  if q.returncode:raise RuntimeError(q.stdout+q.stderr)
  return json.loads(out.read_text())
 same=check(SOURCE,SOURCE);assert same['change_count']==0
 actual=check(SOURCE,RUN);assert actual['change_count']==7 and actual['numeric_change_count']==7
 changed=json.loads(RUN.read_text());changed['E5_limits']['long_walk_limit']['rows'][0]['total_variation_to_top_eigenvector']=0.731234
 mutation=d/'mutation.json';mutation.write_text(json.dumps(changed))
 damaged=check(SOURCE,mutation)
 assert damaged['change_count']==7 and any(z['path'].endswith('rows[0].total_variation_to_top_eigenvector') and z.get('reexecution')==0.731234 for z in damaged['all_changes'])
 print('PASS_A4_COMPARATOR_QA: unchanged, 7 residuals, mutation caught')
