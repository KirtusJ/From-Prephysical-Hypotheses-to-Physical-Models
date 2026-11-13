#!/usr/bin/env python3
"""Check B4 packet exact local integrity. --math reruns in an isolated temporary copy.
Not authentication, refereeing, host-level ACR enforcement or physical certification.
"""
import argparse,csv,hashlib,json,subprocess,sys,tempfile,shutil
from pathlib import Path

root=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--math',action='store_true');args=ap.parse_args()
manifest=json.loads((root/'MANIFEST.json').read_text(encoding='utf-8'))
assert manifest['edition']=='FPHPM-DIRECTOR-B-2026-11-12-B4'
assert manifest['root']=='G1 OPEN' and manifest['ontology']=='NOT_IDENTIFIED'
payloads=manifest['payloads']
actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() and p.name!='MANIFEST.json' and '__pycache__' not in p.parts}
assert set(payloads)==actual, ('inventory mismatch',sorted(set(payloads)-actual),sorted(actual-set(payloads)))
for rel,meta in payloads.items():
 p=root/rel
 assert p.resolve().is_relative_to(root.resolve())
 b=p.read_bytes()
 assert len(b)==meta['bytes'] and hashlib.sha256(b).hexdigest()==meta['sha256'],rel
with (root/'REGISTERS/CLAIM_DELTA_B4.csv').open(newline='') as f: claims=list(csv.DictReader(f))
with (root/'REGISTERS/OPEN_PROBLEMS_B4.csv').open(newline='') as f: ops=list(csv.DictReader(f))
assert len(claims)==11 and len({c['claim_id'] for c in claims})==11
assert len(ops)==6 and all(op['status']=='OPEN' for op in ops)
assert len(json.loads((root/'REGISTERS/ONTOLOGY_GATE_MAP_B4.json').read_text())['gates'])==13
assert all(g['state'].startswith('OPEN') for g in json.loads((root/'REGISTERS/ONTOLOGY_GATE_MAP_B4.json').read_text())['gates'])
print('B4_LOCAL_INTEGRITY_PASS',len(payloads),'payloads, 11 findings, 6 local open obligations, 13 unadvanced gates')
if args.math:
 with tempfile.TemporaryDirectory(prefix='b4_repro_') as td:
  dest=Path(td)/'verification'
  shutil.copytree(root/'VERIFICATION',dest)
  cp=subprocess.run([sys.executable,'verify_B4.py'],cwd=dest,text=True,capture_output=True)
  if cp.returncode:
   print(cp.stdout,cp.stderr);raise RuntimeError('math script did not pass')
  for name in ('B4_RESULTS.json','all_k4_walk_counts_k0_to_k40.csv','all_triangle_gain_switching_cases.csv'):
   assert (dest/name).read_bytes()==(root/'VERIFICATION'/name).read_bytes(),name
  print(cp.stdout.strip())
  print('B4_CLEAN_MATH_REPRODUCTION_BYTE_IDENTICAL')
