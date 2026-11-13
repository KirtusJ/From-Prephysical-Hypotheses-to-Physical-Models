#!/usr/bin/env python3
"""Director G additive handoff local checks only; authenticity and proof not certified."""
from __future__ import annotations
import csv, hashlib, json, math, sys
from pathlib import Path
root=Path(__file__).resolve().parent
manifest=json.loads((root/'MANIFEST.json').read_text(encoding='utf-8'))
assert manifest['packet_id']=='FPHPM-DIRECTOR-G-AB-2026-11-12'
expected=set(manifest['payloads'])
actual={x.relative_to(root).as_posix() for x in root.rglob('*') if x.is_file() and x.name!='MANIFEST.json'}
assert expected==actual,('inventory mismatch',sorted(expected-actual),sorted(actual-expected))
for name, item in manifest['payloads'].items():
 b=(root/name).read_bytes()
 assert len(b)==item['bytes'] and hashlib.sha256(b).hexdigest()==item['sha256'],name
with (root/'records/CLAIM_DELTA.csv').open(newline='') as f:
 c=list(csv.DictReader(f))
with (root/'records/OPEN_PROBLEMS_DELTA.csv').open(newline='') as f:
 op=list(csv.DictReader(f))
assert len(c)==18 and len({row['id'] for row in c})==18
assert len(op)==9 and all(q['status']=='OPEN' for q in op)
valid={'SUPPORTED_IN_SCOPE','CONDITIONAL','REFUTED_IN_SCOPE','NOT_IDENTIFIED_IN_SCOPE','UNRESOLVED','DISPUTED','INCOMPARABLE'}
assert all(row['disposition'] in valid for row in c)
graph=json.loads((root/'records/ONTOLOGY_OBLIGATION_GRAPH.json').read_text())
assert graph['root_G1']=='OPEN' and not graph['ontology_selected']
ids={node['id'] for node in graph['nodes']}
assert all(e['source'] in ids and e['target'] in ids for e in graph['edges'])
data=json.loads((root/'verification/composition_results.json').read_text())
assert not data['ontology_selected'] and data['checks']['num_retained_parameter_cases']==101
assert data['checks']['num_random_pure_targets']==200
assert data['checks']['num_positive_gap_cases']==99
assert len(data['retained_trials'])==101
assert abs(data['retained_trials'][0]['naive_family_violation'])<1e-12
assert abs(data['retained_trials'][-1]['naive_family_violation'])<1e-12
for row in data['retained_trials']:
 t=row['t']; gap=row['naive_family_violation']
 assert abs(gap-t*(1-t)/4)<2e-12
print('PASS_LOCAL_DIRECTOR_G_AB_PACKET',len(expected),'payloads; 18 claims; 9 open problems; 101 retained grid cases; G1 OPEN; ontology NOT IDENTIFIED')
print('Integrity/registry only; not authentication, proof certification, peer review or empirical validation')
