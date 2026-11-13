#!/usr/bin/env python3
"""Source-safe controlled QA mutations of C's scoped release. Always works in temporary extracted copies.
Tests the declared narrow checker contract; not an authentication or substantive review certification.
"""
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile
import shutil,subprocess,sys,json,hashlib,csv
src=Path(__file__).resolve().parents[1]/'source_archives'/'DIRECTOR_C_CURRENT.zip'
assert src.is_file(),src

def extract(p):
 with ZipFile(src) as z:
  assert z.testzip() is None
  for info in z.infolist():
   dest=p.joinpath(*Path(info.filename).parts).resolve()
   assert dest.is_relative_to(p.resolve()),info.filename
  z.extractall(p)
 root=p/'Director_C_CHSH_QA_Adversarial_2026-11-11'
 assert (root/'verify_release.py').exists()
 return root

def verify(r):
 x=subprocess.run([sys.executable,str(r/'verify_release.py')],cwd=r,capture_output=True,text=True,timeout=45)
 return x.returncode==0

def update_manifest(r,name):
 mpath=r/'SHA256_RELEASE_MANIFEST.json'; m=json.loads(mpath.read_text())
 f=(r/name).read_bytes();m['payloads'][name]={'size_bytes':len(f),'sha256':hashlib.sha256(f).hexdigest()}
 mpath.write_text(json.dumps(m,indent=2)+'\n')

def one_test(test):
 with TemporaryDirectory() as tmp:
  r=extract(Path(tmp))
  if test=='baseline':return verify(r)
  if test.startswith('g5_'):
   f=r/'subreviews/LOCAL_FOCUSED_REVIEWS.json';d=json.loads(f.read_text())
   if test=='g5_literal_failure':d[0]['G5']['status']='FAILED'
   else:d[0]['G5']['basis']='No actual checking work occurred, notwithstanding the success-looking status'
   f.write_text(json.dumps(d,indent=2)+'\n')
   update_manifest(r,'subreviews/LOCAL_FOCUSED_REVIEWS.json')
  elif test=='wrong_claim':
   f=r/'registers/C_NEW_SCOPED_FINDINGS_12.csv'
   with f.open(newline='',encoding='utf8') as fh:
    dr=csv.DictReader(fh);fields=dr.fieldnames;rows=list(dr)
   target=next(x for x in rows if x['id']=='C-CHSH-005')
   target['exact_scoped_claim']='In this model, a single CHSH round suffices for size 5 percent and power 95 percent.'
   with f.open('w',encoding='utf8',newline='') as fh:
    wr=csv.DictWriter(fh,fieldnames=fields);wr.writeheader();wr.writerows(rows)
   update_manifest(r,'registers/C_NEW_SCOPED_FINDINGS_12.csv')
  elif test=='wrong_reference':
   f=r/'verification/REFERENCE_RESULTS.json';data=json.loads(f.read_text())
   data['noisy_pr_minimum_fixed_rounds_with_external_randomization']=1
   f.write_text(json.dumps(data,indent=2)+'\n')
   update_manifest(r,'verification/REFERENCE_RESULTS.json')
  else:raise ValueError(test)
  return verify(r)

out={k:one_test(k) for k in ['baseline','g5_literal_failure','g5_unsupported_basis','wrong_claim','wrong_reference']}
assert out=={'baseline':True,'g5_literal_failure':False,'g5_unsupported_basis':True,'wrong_claim':True,'wrong_reference':False},out
out['interpretation']='The current C verifier detects literal G5 failure and recomputed math corruption; it cannot substantively authenticate gate work or automatically bind arbitrary prose claims to computations.'
print(json.dumps(out,indent=2,sort_keys=True))
