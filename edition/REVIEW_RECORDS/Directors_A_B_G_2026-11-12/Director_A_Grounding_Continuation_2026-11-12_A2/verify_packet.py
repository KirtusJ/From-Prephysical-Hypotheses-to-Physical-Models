#!/usr/bin/env python3
"""Check only the delivered packet's internal byte consistency, not scientific correctness."""
from pathlib import Path
import hashlib
import json
import sys

ROOT=Path(__file__).resolve().parent
manifest=json.loads((ROOT/'MANIFEST.json').read_text(encoding='utf-8'))
entries=manifest['payloads']
expected={r['path'] for r in entries}
actual={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file() and p.name!='MANIFEST.json'}
if expected!=actual:
    print('FAIL_PAYLOAD_INVENTORY', 'missing=', sorted(expected-actual), 'unexpected=',sorted(actual-expected));sys.exit(1)
for item in entries:
    p=ROOT/item['path']
    b=p.read_bytes()
    actual_hash=hashlib.sha256(b).hexdigest()
    if actual_hash!=item['sha256'] or len(b)!=item['bytes']:
        print('FAIL_HASH_OR_SIZE',item['path']);sys.exit(1)
print('PASS_A2_LOCAL_BYTE_INTEGRITY', len(entries), 'payloads',manifest['research_status'])
