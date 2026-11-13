#!/usr/bin/env python3
"""Local known-invalid mutation controls for verify_geometry_and_composition.py.
The mutations are only applied to disposable copies; the source and baseline are unchanged.
"""
from pathlib import Path
import tempfile,subprocess,sys,json
script=Path(__file__).with_name('verify_geometry_and_composition.py')
source=script.read_text()
controls={
 'good_source_accept': (source,0),
 'replace_Bargmann_square_with_first_power':(source.replace('predicted=(P/abs(P))**2','predicted=(P/abs(P))'),1),
 'replace_Tsirelson_target_with_classical_target':(source.replace('assert abs(chsh-2*sqrt(2))<1e-13','assert abs(chsh-2)<1e-13'),1),
}
assert len(set(v[0] for v in controls.values()))==len(controls),'Mutation failed to change source'
results={}
with tempfile.TemporaryDirectory(prefix='directorB_mut_') as tmp:
 for name,(code,expected) in controls.items():
  p=Path(tmp)/(name+'.py')
  p.write_text(code)
  run=subprocess.run([sys.executable,str(p)],capture_output=True,text=True,timeout=65)
  observed='ACCEPT' if run.returncode==0 else 'REJECT'
  want='ACCEPT' if expected==0 else 'REJECT'
  results[name]={'expected':want,'observed':observed,'exit_code':run.returncode,
                 'passed':observed==want,'last_stdout':run.stdout.strip().splitlines()[-1:]}
  assert observed==want,(name,run.stdout[-500:],run.stderr[-500:])
Path(__file__).with_name('qa_mutation_results.json').write_text(json.dumps(results,indent=2,sort_keys=True)+'\n')
print('PASS_MUTATION_CONTROLS',list(results))
