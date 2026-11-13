#!/usr/bin/env python3
"""B2 local provenance-free ZIP payload check. This does NOT authenticate publisher."""
from pathlib import Path
import hashlib,json,sys
root=Path(__file__).resolve().parents[1]
mfile=root/'MANIFEST.json'
manifest=json.loads(mfile.read_text())
expected=set()
for item in manifest['payloads']:
 p=(root/item['path']).resolve()
 if not p.is_relative_to(root.resolve()):raise SystemExit('FAIL path escape')
 if not p.is_file():raise SystemExit('FAIL missing '+item['path'])
 by=p.read_bytes()
 if len(by)!=item['bytes'] or hashlib.sha256(by).hexdigest()!=item['sha256']:
  raise SystemExit('FAIL mismatch '+item['path'])
 expected.add(item['path'])
files={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() and p.name not in ('MANIFEST.json',) and p.suffix not in ('.aux','.log','.out')}
if files!=expected:
 raise SystemExit('FAIL file-set mismatch: missing '+str(expected-files)+'; extra '+str(files-expected))
if manifest['root_state']!='G1 OPEN' or manifest['ontology_selected']:
 raise SystemExit('FAIL disposition misuse')
print('B2_PACKET_INTEGRITY_PASS',len(expected),'payloads; no authentication, peer review, physical model validation or ACR host enforcement')
