#!/usr/bin/env python3
"""Offline, source-free packet SHA-256 integrity check; no validity certification."""
from __future__ import annotations
import hashlib, json, sys
from pathlib import Path

root = Path(__file__).resolve().parent
manifest = json.loads((root / 'MANIFEST.json').read_text(encoding='utf-8'))
assert manifest['edition'] == 'FPHPM-DIRECTOR-B-2026-11-12-B1'
seen = set()
for item in manifest['files']:
    rel = Path(item['path'])
    assert not rel.is_absolute() and '..' not in rel.parts
    assert str(rel) not in seen
    seen.add(str(rel))
    target = root / rel
    assert target.is_file(), f'MISSING: {rel}'
    raw = target.read_bytes()
    assert len(raw) == item['bytes'], f'SIZE MISMATCH: {rel}'
    digest = hashlib.sha256(raw).hexdigest()
    assert digest == item['sha256'], f'HASH MISMATCH: {rel}'
actual = set(str(f.relative_to(root)) for f in root.rglob('*') if f.is_file() and f.name != 'MANIFEST.json')
assert actual == seen, f'UNLISTED/ORPHAN FILES: {sorted(actual ^ seen)}'
print(f'PASS_INTERNAL_SHA256_PACKET {len(seen)} payloads (integrity only; not scientific validation)')
