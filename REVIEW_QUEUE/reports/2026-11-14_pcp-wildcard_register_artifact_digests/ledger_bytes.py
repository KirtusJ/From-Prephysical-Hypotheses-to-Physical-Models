"""ledger_bytes.py REPO OUTDIR  -- reads only; writes OUTDIR/ledger_bytes_result.json (mode 'x').
Predicates, fixed before the first run (exact: digests and set equality, no tolerance):
 L1 every record's `prev` is the SHA-256 of the preceding line (without newline); seq = line index.
 L2 every distinct sha256 in an ARTIFACT_ADDED record is the SHA-256 of some blob in the
    repository's git object store (all refs, all history). Reports those that are not.
 L3 for each review, coverage.open_objections in REVIEW_CLOSED equals the set of objection ids
    of that review whose OBJECTION_RESOLVED record has resolution OPEN_RECORDED.
 Hypothesis test for L2: the repository is not shallow (else L2 is NOT_APPLICABLE).
"""
import json,hashlib,subprocess,sys,os
repo,out=sys.argv[1],sys.argv[2]
g=lambda *a,**k: subprocess.run(['git','-C',repo]+list(a),capture_output=True,**k).stdout
lines=[l for l in open(os.path.join(repo,'.pcp/register.jsonl'),'rb').read().split(b'\n') if l]
rows=[json.loads(l) for l in lines]
L1=all(rows[i]['prev']==hashlib.sha256(lines[i-1]).hexdigest() for i in range(1,len(rows))) and all(r['seq']==i for i,r in enumerate(rows))
shallow=g('rev-parse','--is-shallow-repository').decode().strip()
want={}
for r in rows:
    if r['kind']=='ARTIFACT_ADDED': want.setdefault(r['body']['sha256'],[]).append([r['seq'],r['body']['name'],r['body']['size']])
sizes={v[0][2] for v in want.values()}
found=set()
for l in g('cat-file','--batch-all-objects','--batch-check=%(objectname) %(objecttype) %(objectsize)').decode().split('\n'):
    p=l.split()
    if len(p)==3 and p[1]=='blob' and int(p[2]) in sizes:
        h=hashlib.sha256(g('cat-file','blob',p[0])).hexdigest()
        if h in want: found.add(h)
missing={h:v for h,v in want.items() if h not in found}
cited={h:[[r['seq'],r['kind']] for r in rows if r['kind']!='ARTIFACT_ADDED' and h in json.dumps(r['body'])] for h in missing}
rev=None; raised={}; openrec={}; L3rows=[]
owner={}
for r in rows:
    b=r['body']
    if r['kind']=='OBJECTION_RAISED': owner[b['id']]=b['review']
    if r['kind']=='OBJECTION_RESOLVED' and b['resolution']=='OPEN_RECORDED': openrec.setdefault(owner[b['id']],[]).append(b['id'])
    if r['kind']=='REVIEW_CLOSED':
        L3rows.append([b['review'],r['seq'],b['coverage']['open_objections'],sorted(openrec.get(b['review'],[]))])
res={'records':len(rows),'L1_chain_intact':L1,'shallow':shallow,
 'L2_distinct_artifact_digests':len(want),'L2_found_in_git':len(found),'L2_missing':missing,'L2_missing_cited_by':cited,
 'L2_pass':(len(missing)==0) if shallow=='false' else 'NOT_APPLICABLE',
 'L3_per_review':L3rows,'L3_pass':all(set(a[2])==set(a[3]) for a in L3rows),
 'L3_open_recorded_total':sum(len(a[3]) for a in L3rows),'L3_listed_in_closings_total':sum(len(a[2]) for a in L3rows)}
with open(os.path.join(out,'ledger_bytes_result.json'),'x') as f: json.dump(res,f,indent=1,sort_keys=True)
print({k:v for k,v in res.items() if k!='L3_per_review'})
