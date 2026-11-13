"""Reproduce a selected mathematical calculation in a temporary directory."""
from pathlib import Path
import json, os, shutil, subprocess, sys, tempfile
base=Path(__file__).resolve().parent
query=sys.argv[1] if len(sys.argv)>1 else ""
cases=[x for x in json.loads((base/"cases.json").read_text()) if query.lower() in x[0].lower()]
if not cases:raise SystemExit("No matching calculation.")
for name,result,reference in cases:
    for mode in ([],["-O"],["-OO"]):
        with tempfile.TemporaryDirectory() as directory:
            work=Path(directory);shutil.copyfile(base/name,work/name)
            proc=subprocess.run([sys.executable,*mode,str(work/name)],cwd=work,check=True,capture_output=True,timeout=240,env={**os.environ,"OPENBLAS_NUM_THREADS":"1","OMP_NUM_THREADS":"1"})
            data=(work/result).read_bytes() if result else proc.stdout
            if data!=(base/reference).read_bytes():raise SystemExit(f"Mismatch in {name} {mode}")
    print("PASS",name)
