#!/usr/bin/env python3
"""Check local packet member integrity only; no signature or science verification."""
import hashlib
import json
import sys
from pathlib import Path

root=Path(__file__).resolve().parent
manifest=json.loads((root/'MANIFEST.json').read_text(encoding='utf-8'))
files=manifest['files']
errors=[]
seen=set()
for entry in files:
    rel=entry['path']
    path=(root/rel).resolve()
    if path == root or root not in path.parents:
        errors.append(f'unsafe path: {rel}')
        continue
    if not path.is_file():
        errors.append(f'absent: {rel}')
        continue
    data=path.read_bytes()
    actual=hashlib.sha256(data).hexdigest()
    if actual != entry['sha256'] or len(data)!=entry['bytes']:
        errors.append(f'hash/size mismatch: {rel}')
    seen.add(rel)
actual_files={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() and p.name!='MANIFEST.json'}
if actual_files!=seen:
    errors.append(f'unexpected/missing packet members: {sorted(actual_files^seen)}')
if errors:
    for err in errors: print('FAIL',err)
    sys.exit(1)
print(f'PASS_LOCAL_PACKET_INTEGRITY {len(files)} files; does not certify external provenance, science, or method efficacy')
