#!/usr/bin/env python3
"""SHA-256 and research-status verifier for Director A A4 overlay.
Run with an absolute or relative path; only own packet is inspected.
"""
from pathlib import Path
import csv,hashlib,json,sys
root=Path(__file__).resolve().parent;report=json.loads((root/'MANIFEST.json').read_text())
assert report['root_status']=='G1 OPEN' and report['ontology_selected']==False
assert report['baseline_modified']==False
assert len(report['files'])>=10
seen=set()
for item in report['files']:
 p=root/item['path'];assert p.is_file(),item['path'];assert p.resolve().is_relative_to(root.resolve())
 assert item['path'] not in seen;seen.add(item['path'])
 assert p.stat().st_size==item['size'],f'size changed {p}'
 assert hashlib.sha256(p.read_bytes()).hexdigest()==item['sha256'],f'hash mismatch {p}'
with (root/'records/CLAIM_DELTA.csv').open(newline='') as f:claims=list(csv.DictReader(f))
with (root/'records/OPEN_PROBLEMS_DELTA.csv').open(newline='') as f:issues=list(csv.DictReader(f))
assert len(claims)==23 and len(issues)==12
assert any(x['status']=='REFUTED_FOR_EXAMPLE' for x in claims)
assert all(x['status']=='OPEN' for x in issues)
print('PASS_A4_PACKET',len(report['files']),'payloads;',len(claims),'claims;',len(issues),'open obligations; G1 OPEN')
