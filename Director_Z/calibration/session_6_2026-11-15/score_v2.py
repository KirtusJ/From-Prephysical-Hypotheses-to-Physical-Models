"""Score committed retrieval answers against `pcpos clause`. Exact substring for WORDS;
ABSENT is FOR when the tool reports no such provision; NOT_INSPECTED is FOR when the
participant supplied no words (the tool is not consulted for the text). Usage:
score_v2.py <pcpos> <method dir> <answers.json> <out.json>  (refuses to overwrite out).
Version 2 (15 Nov 2026, after Director G's controls): an empty WORDS answer is AGAINST; an unknown kind is AGAINST;
NOT_INSPECTED is FOR only when the tool reports no such provision is absent... no: only when the answer supplies no words
AND the kind is exactly NOT_INSPECTED; duplicate ids are refused."""
import json,subprocess,sys,hashlib,os
b,m,a,o=sys.argv[1:5]
assert not os.path.exists(o)
raw=open(a,'rb').read(); items=json.loads(raw); out=[]
ids=[it['id'] for it in items]; assert len(ids)==len(set(ids)), 'duplicate answer id'
for it in items:
    r=subprocess.run([b,'clause',m,it['module'],it['section']],capture_output=True,text=True)
    txt=r.stdout+r.stderr
    if it['kind']=='WORDS': s='FOR' if r.returncode==0 and it['answer'].strip() and it['answer'] in r.stdout else 'AGAINST'
    elif it['kind']=='ABSENT': s='FOR' if 'has no provision numbered' in txt else 'AGAINST'
    elif it['kind']=='NOT_INSPECTED': s='FOR' if 'no words supplied' in it['answer'] else 'AGAINST'
    else: s='AGAINST'
    out.append({'id':it['id'],'module':it['module'],'section':it['section'],'kind':it['kind'],'tool_exit':r.returncode,'scored':s,'tool_first_line':txt.splitlines()[0] if txt else ''})
json.dump({'answers_sha256':hashlib.sha256(raw).hexdigest(),'scores':out},open(o,'w'),indent=1)
print(sum(x['scored']=='FOR' for x in out),'of',len(out)); [print(x['id'],x['scored']) for x in out]
