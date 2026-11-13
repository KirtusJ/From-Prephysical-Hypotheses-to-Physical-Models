#!/usr/bin/env python3
"""Verify this Director A overlay's content consistency. This is NOT scientific, ACR, or identity certification."""
from pathlib import Path
from hashlib import sha256
import json, csv, sys

root=Path(__file__).resolve().parent
manifest=json.loads((root/'RUN_MANIFEST.json').read_text())
errors=[]
expected=set(manifest['payloads'])
seen={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() and p.name!='RUN_MANIFEST.json'}
if seen != expected:
    errors.append('payload listing differences: absent='+repr(sorted(expected-seen))+' unexpected='+repr(sorted(seen-expected)))
for rel,rec in manifest['payloads'].items():
    p=root/rel
    if not p.is_file(): errors.append('missing '+rel); continue
    b=p.read_bytes()
    if len(b)!=rec['bytes'] or sha256(b).hexdigest()!=rec['sha256']:
        errors.append('digest/length mismatch '+rel)
try:
    with open(root/'REGISTERS/CLAIM_DISPOSITION_DELTA.csv',newline='') as f: claims=list(csv.DictReader(f))
    with open(root/'REGISTERS/OPEN_PROBLEMS_DELTA.csv',newline='') as f: questions=list(csv.DictReader(f))
    ids=[r['id'] for r in claims]
    qids=[r['id'] for r in questions]
    allowed={'SUPPORTED_IN_SCOPE','CONDITIONAL','REFUTED_IN_SCOPE','NOT_IDENTIFIED_IN_SCOPE','DISPUTED','UNRESOLVED','INCOMPARABLE'}
    assert len(ids)==len(set(ids)) and len(ids)==16,'claim IDs not unique or wrong count'
    assert len(qids)==len(set(qids)) and len(qids)==9,'question IDs not unique or wrong count'
    assert all(r['status'] in allowed for r in claims),'unknown claim disposition'
    graph=json.loads((root/'REGISTERS/ONTOLOGY_GATE_GRAPH.json').read_text())
    nodes={n['id'] for n in graph['nodes']}
    assert not graph['ontology_selected'] and not graph['quantum_mechanics_emergent'] and not graph['classical_mechanics_emergent']
    assert all(e['source'] in nodes and e['target'] in nodes for e in graph['edges'])
    assert all(r['status']=='OPEN' for r in questions)
except Exception as exc:
    errors.append('logical registry test: '+repr(exc))
if errors:
    print('LOCAL_OVERLAY_CHECK_FAIL')
    for e in errors: print(' -',e)
    sys.exit(1)
print('LOCAL_OVERLAY_CHECK_PASS:',len(expected),'payloads;',len(claims),'claim findings;',len(questions),'open questions;',len(graph['nodes']),'graph nodes,',len(graph['edges']),'typed edges')
print('Scope: local byte consistency and simple register invariants only. No authentication, independent proof checking, ACR host integration, or ontology validation.')
