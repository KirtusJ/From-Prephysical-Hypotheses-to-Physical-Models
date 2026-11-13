#!/usr/bin/env python3
"""Adverse QA probes against ORIGINAL B release and B-embedded older C release.
All mutations take place in disposable extracted copies, never source/release files.
Arguments: B_SOURCE_ZIP output_json
"""
import hashlib,json,subprocess,sys,tempfile,zipfile
from pathlib import Path
BZIP=Path(sys.argv[1]).resolve(); OUT=Path(sys.argv[2]).resolve()

def safe_unpack(zpath,d):
    with zipfile.ZipFile(zpath) as z:
        assert z.testzip() is None
        for member in z.namelist():
            assert (d/member).resolve().is_relative_to(d.resolve()),member
        z.extractall(d)

def run(r):
    p=subprocess.run([sys.executable,str(r/'validate_release.py')],cwd=r,capture_output=True,text=True,timeout=150)
    return p.returncode

def rehash(r,rel,sizekey):
    m=r/'RELEASE_MANIFEST.json';j=json.loads(m.read_text())
    b=(r/rel).read_bytes();j['payloads'][rel]={'sha256':hashlib.sha256(b).hexdigest(),sizekey:len(b)}
    m.write_text(json.dumps(j,indent=2,sort_keys=True)+'\n')

with tempfile.TemporaryDirectory(prefix='B-qa-') as tmp:
    d=Path(tmp);safe_unpack(BZIP,d)
    root=d/'Director_B_Parity_QA_2026-11-11'
    assert run(root)==0
    csource=root/'source_archives/C_CURRENT.zip'
    rel='subreviews/LOCAL_FOCUSED_EXAMINATIONS.json';p=root/rel
    obj=json.loads(p.read_text());obj['assessments'][0]['G5']='G5 FAILED: CONTROLLED MUTATION'
    p.write_text(json.dumps(obj,indent=2)+'\n')
    assert run(root)!=0
    rehash(root,rel,'size_bytes')
    assert run(root)==0
    # current B checks own calculations without overwriting reference output
    b_ref=(root/'verification/EXACT_PARITY_RESULTS.json').read_bytes()
    assert run(root)==0 and (root/'verification/EXACT_PARITY_RESULTS.json').read_bytes()==b_ref
    # A wrong numerical result must be rejected even if its local self-manifest is changed.
    relmath='verification/EXACT_PARITY_RESULTS.json';mp=root/relmath
    j=json.loads(mp.read_text());j['PR_orientations']=0
    mp.write_text(json.dumps(j,indent=2,sort_keys=True)+'\n')
    rehash(root,relmath,'size_bytes')
    assert run(root)!=0
    # original C checker in C_CURRENT silently overwrites mathematical reference
    with tempfile.TemporaryDirectory(prefix='C-qa-') as t2:
        cd=Path(t2);safe_unpack(csource,cd)
        c=cd/'Director_C_PostWithdrawal_Parity_Time_QA_2026-11-11'
        assert run(c)==0
        relc='verification/INDEPENDENT_C_RESULTS.json';pc=c/relc
        j=json.loads(pc.read_text());assert j['affine_local_models']==8
        j['affine_local_models']=0;pc.write_text(json.dumps(j,indent=2,sort_keys=True)+'\n')
        assert run(c)!=0
        j=json.loads(pc.read_text());j['affine_local_models']=0
        pc.write_text(json.dumps(j,indent=2,sort_keys=True)+'\n')
        rehash(c,relc,'size')
        assert run(c)==0
        assert json.loads(pc.read_text())['affine_local_models']==8
        assert run(c)!=0
obj={
 'B_unmodified_pass':True,
 'B_G5_failed_stale_manifest_rejected':True,
 'B_G5_failed_self_rehashed_accepted':True,
 'B_current_reference_unchanged_after_validation':True,
 'B_corrupted_self_rehashed_mathematical_reference_rejected':True,
 'C_unmodified_pass':True,
 'C_corrupted_reference_stale_manifest_rejected':True,
 'C_corrupted_reference_self_rehashed_first_pass':True,
 'C_saved_reference_rewritten_in_place':True,
 'C_second_validation_rejected_stale_manifest':True,
 'interpretation':'Scoped integrity/oracle coverage only, not claims about actual G5 performance or scientific validity.'
}
OUT.write_text(json.dumps(obj,sort_keys=True,indent=2)+'\n')
print('RECIPROCAL_QA_MANUAL_PASS')
