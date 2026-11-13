#!/usr/bin/env python3
"""Validate file inventory and SHA-256 pins only. Never certify proofs or physical models."""
from __future__ import annotations
import hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
try:
 manifest=json.loads((ROOT/'MANIFEST.json').read_text())
 files=manifest['payloads']
 expected={p['path'] for p in files}
 actual={str(p.relative_to(ROOT)).replace('\\','/') for p in ROOT.rglob('*') if p.is_file() and p.name!='MANIFEST.json'}
 assert expected==actual,{'missing':sorted(expected-actual),'unexpected':sorted(actual-expected)}
 for d in files:
  p=ROOT/d['path'];assert p.stat().st_size==d['bytes'],d['path']
  assert hashlib.sha256(p.read_bytes()).hexdigest()==d['sha256'],d['path']
 assert manifest['stage']=='Initial External Grounding OPEN; root G1 OPEN'
 assert manifest['ontology']=='not selected'
 print(f"DIRECTOR_G_G3_LOCAL_PACKET_INTEGRITY_PASS {len(files)} payloads; no authenticating authorship, proof, physical emergence or ACR host enforcement")
except Exception as exc:
 print('FAIL_G3_LOCAL_PACKET_INTEGRITY',repr(exc));sys.exit(1)
