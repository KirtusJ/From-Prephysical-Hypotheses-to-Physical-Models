#!/usr/bin/env python3
"""Director A A3 additive packet consistency checker, no authenticity/proof claim."""
from __future__ import annotations
import csv,hashlib,json
from pathlib import Path

root=Path(__file__).resolve().parent
manifest=json.loads((root/'MANIFEST.json').read_text(encoding='utf-8'))
assert manifest['edition']=='FPHPM-DIRECTOR-A-2026-11-12-A3'
assert manifest['research_root']=='G1 OPEN'
assert not manifest['ontology_selected']
expected=set(manifest['payloads'])
actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() and p.name!='MANIFEST.json'}
assert actual==expected, ('inventories mismatch',sorted(expected-actual),sorted(actual-expected))
for rel,info in manifest['payloads'].items():
 p=(root/rel)
 assert p.resolve().is_relative_to(root.resolve())
 data=p.read_bytes()
 assert len(data)==info['bytes'] and hashlib.sha256(data).hexdigest()==info['sha256'],rel
with (root/'REGISTERS/CLAIM_DELTA.csv').open(newline='') as f: claims=list(csv.DictReader(f))
with (root/'REGISTERS/OPEN_PROBLEMS_DELTA.csv').open(newline='') as f: ops=list(csv.DictReader(f))
assert len(claims)==22 and len({c['claim_id'] for c in claims})==22
assert len(ops)==13 and len({o['id'] for o in ops})==13
assert all(x['status']=='OPEN' for x in ops)
valid={'SUPPORTED_IN_SCOPE','CONDITIONAL','REFUTED_IN_SCOPE','NOT_IDENTIFIED_IN_SCOPE','UNRESOLVED','DISPUTED','INCOMPARABLE'}
assert all(c['disposition'] in valid for c in claims)
summary=json.loads((root/'VERIFICATION/A3_check_summary.json').read_text())
assert summary['records']=={'arbitrary_precision_parameter_cases':217,'finite_matrix_filter_cases':249,'ghz_biseparable_trials':480,'pure_seed_filter_trials':240,'high_precision_digits':95}
assert all(summary['false_controls'].values())
for k,fn in [('arbitrary_precision_parameter_cases','all_A3_high_precision_parameter_cases.csv'),
('finite_matrix_filter_cases','all_A3_finite_matrix_checks.csv'),
('ghz_biseparable_trials','all_A3_GHZ_biseparable_samples.csv'),
('pure_seed_filter_trials','all_A3_pure_seed_filter_samples.csv')]:
 with (root/'VERIFICATION'/fn).open(newline='') as f:count=sum(1 for _ in csv.DictReader(f))
 assert count==summary['records'][k]
edges=json.loads((root/'REGISTERS/ONTOLOGY_EDGE_DELTA.json').read_text())
assert not edges['ontology_selected'] and edges['baseline_status'].endswith('G1 OPEN')
ids={node['id'] for node in edges['nodes']}
assert all(edge['from'] in ids and edge['to'] in ids for edge in edges['edges'])
print('A3_PACKET_PASS',len(expected),'payloads; 22 scoped claims; 13 open problems; 1186 retained trials; G1 OPEN; ontology not identified')
print('Local integrity/registry only; not authenticity, proof certification, peer review, host integration or physical validation.')
