#!/usr/bin/env python3
"""Local Director G supplement checksum and inventory checker. No scientific certification."""
import csv,hashlib,json
from pathlib import Path
p=Path(__file__).resolve().parent
manifest=json.loads((p/'MANIFEST.json').read_text())
assert manifest['edition']=='FPHPM-DIRECTOR-G-2026-11-12-G4'
assert manifest['root_review']=='G1 OPEN'
assert manifest['ontology_selected'] is False
expected=set(manifest['payloads'])
actual={x.relative_to(p).as_posix() for x in p.rglob('*') if x.is_file() and x.name!='MANIFEST.json'}
assert expected==actual, f'inventory mismatch {sorted(expected^actual)}'
for rel,spec in manifest['payloads'].items():
 x=(p/rel).resolve();assert x.is_relative_to(p.resolve())
 blob=x.read_bytes()
 assert len(blob)==spec['bytes'] and hashlib.sha256(blob).hexdigest()==spec['sha256'],rel
results=json.loads((p/'verification/RESULTS_G4.json').read_text())
assert results['lift']['primitive_exponent']==5 and results['lift']['minimum_entry_B5']==1
assert results['sync_composition']['synchronized_dim']==8 and results['sync_composition']['expected_tensor_dim']==16
expected_counts={'lift_cell_rows':285,'lift_coverage_rows':19,'phase_approximation_rows':1024,
                 'gauge_switch_rows':729,'sync_rank_rows':13,'formal_unitary_rows':6,
                 'formal_composite_rows':4,'filter_rows':7}
assert results['trial_counts']==expected_counts
assert sum(expected_counts.values())==2087
files={'lift_cell_rows':'all_lift_endpoint_gain_counts.csv',
       'lift_coverage_rows':'all_lift_coverage_bounds.csv',
       'phase_approximation_rows':'all_projective_approximation_trials.csv',
       'gauge_switch_rows':'all_triangle_switching_trials.csv',
       'sync_rank_rows':'all_synchronized_composition_rank_trials.csv',
       'formal_unitary_rows':'all_formal_unitary_controls.csv',
       'formal_composite_rows':'all_formal_composite_dynamics_trials.csv',
       'filter_rows':'all_filter_unconditional_witness_controls.csv'}
for key,filename in files.items():
 with (p/'verification'/filename).open(newline='') as f:
  assert sum(1 for _ in csv.DictReader(f))==expected_counts[key],filename
with (p/'verification/Z2_FLOAT_ROUNDOFF_DIFFS.csv').open(newline='') as f:
 errors=list(csv.DictReader(f))
assert len(errors)==7 and max(float(x['abs_delta']) for x in errors)<1e-12
with (p/'records/CLAIM_DISPOSITIONS.csv').open(newline='') as f:
 claims=list(csv.DictReader(f))
assert len(claims)==18 and len({x['claim_id'] for x in claims})==18
pdf=p/'papers/Finite_Gain_Graph_Rays_and_Composition_Obstructions.pdf'
assert pdf.read_bytes().startswith(b'%PDF-')
print('G4_LOCAL_PACKET_PASS',len(expected),'payloads',len(claims),'claims',sum(expected_counts.values()),'retained trials','G1 OPEN; no ontology')
print('Checks are local byte/inventory and test-count consistency, not peer review, proof certification, source authentication, or host-enforced ACR.')
