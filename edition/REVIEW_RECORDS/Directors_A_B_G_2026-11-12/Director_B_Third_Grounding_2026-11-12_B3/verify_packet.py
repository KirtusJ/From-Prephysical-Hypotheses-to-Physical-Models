#!/usr/bin/env python3
"""Local integrity and schema checker; neither authentication nor scientific proof."""
import csv, hashlib, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def fail(message):
 print('FAIL_B3_PACKET',message);sys.exit(1)

m=json.loads((ROOT/'MANIFEST.json').read_text())
if m.get('packet_id')!='FPHPM-DIRECTOR-B-GROUNDING-2026-11-12-B3':fail('packet identity')
if m.get('root_G1')!='OPEN' or m.get('ontology_selected') is not False:fail('research stage')
entries=m['payloads']; expected={x['path'] for x in entries}
actual={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file() and p.name!='MANIFEST.json'}
if actual!=expected:fail('missing or unexpected file: '+str(sorted(expected^actual)))
for x in entries:
 p=ROOT/x['path'];data=p.read_bytes()
 if len(data)!=x['bytes'] or hashlib.sha256(data).hexdigest()!=x['sha256']:fail('digest: '+x['path'])
with (ROOT/'records/CLAIM_RECONCILIATION.csv').open() as f:claims=list(csv.DictReader(f))
with (ROOT/'records/OPEN_PROBLEMS.csv').open() as f:problems=list(csv.DictReader(f))
if len(claims)!=14 or len({r['id'] for r in claims})!=14:fail('claims inventory')
if len(problems)!=12 or len({r['id'] for r in problems})!=12 or any(x['status']!='OPEN' for x in problems):fail('problem inventory')
graph=json.loads((ROOT/'records/ONTOLOGY_GATE_MAP.json').read_text())
if graph.get('root_G1')!='OPEN' or graph.get('ontology_selected') is not False:fail('graph scope')
ids={n['id'] for n in graph['nodes']}
if len(ids)!=len(graph['nodes']) or any(e['source'] not in ids or e['target'] not in ids for e in graph['edges']):fail('graph consistency')
result=json.loads((ROOT/'verification/B3_RESULTS.json').read_text())
if result['ontology_selected'] or result['trial_counts']['filter_parameter_rows_with_duplicates_retained']!=261 or result['trial_counts']['cycle_rows']!=29:fail('check counts')
with (ROOT/'verification/ALL_FILTER_TRIALS.csv').open() as f:fr=list(csv.DictReader(f))
with (ROOT/'verification/ALL_CYCLE_TRIALS.csv').open() as f:cr=list(csv.DictReader(f))
if len(fr)!=261 or len(cr)!=29 or fr[0]['status']!='ENDPOINT_NO_SUCCESS_FOR_CHOSEN_X':fail('trial table endpoints')
neg=json.loads((ROOT/'verification/NEGATIVE_CONTROL_RESULTS.json').read_text())
if neg['pass_count']!=8 or not all(neg['controls'].values()):fail('negative controls')
print('PASS_B3_PACKET',len(entries),'payloads;',len(claims),'claims;',len(problems),'open problems; 261 filter/29 cycle rows; G1 OPEN')
print('Local byte consistency only; not authentication, peer review, empirical test or host enforcement')
