"""Score committed retrieval answers against `pcpos clause`. Exact substring for WORDS;
ABSENT is FOR when the tool reports no such provision; NOT_INSPECTED is FOR when the
participant supplied no words (the tool is not consulted for the text). Usage:
score.py <pcpos> <method dir> <answers.json> <out.json>  (refuses to overwrite out)."""
import json,subprocess,sys,hashlib,os
b,m,a,o=sys.argv[1:5]
assert not os.path.exists(o)
raw=open(a,'rb').read(); items=json.loads(raw); out=[]
for it in items:
    r=subprocess.run([b,'clause',m,it['module'],it['section']],capture_output=True,text=True)
    txt=r.stdout+r.stderr
    if it['kind']=='WORDS': s='FOR' if r.returncode==0 and it['answer'] in r.stdout else 'AGAINST'
    elif it['kind']=='ABSENT': s='FOR' if 'has no provision numbered' in txt else 'AGAINST'
    else: s='FOR' if 'no words supplied' in it['answer'] else 'AGAINST'
    out.append({'id':it['id'],'module':it['module'],'section':it['section'],'kind':it['kind'],'tool_exit':r.returncode,'scored':s,'tool_first_line':txt.splitlines()[0] if txt else ''})
json.dump({'answers_sha256':hashlib.sha256(raw).hexdigest(),'scores':out},open(o,'w'),indent=1)
print(sum(x['scored']=='FOR' for x in out),'of',len(out)); [print(x['id'],x['scored']) for x in out]
