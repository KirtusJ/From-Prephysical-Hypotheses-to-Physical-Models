import json,os,re,glob
R='/home/user/From-Prephysical-Hypotheses-to-Physical-Models'
files=[]
for d in ['Z4_COMPUTATION','Director_Z_challenger','Director_Z_cross_review','REVIEW_QUEUE/reports']:
    for dp,dn,fn in os.walk(os.path.join(R,d)):
        files+= [os.path.join(dp,f) for f in fn if f.endswith('.json')]
recfiles=glob.glob(R+'/ADDENDUM_EDITION_Z*_SESSION_4.md')+[R+'/DIRECTOR_Z_TECHNICAL_DISPOSITION_SESSION_4.md']+glob.glob(R+'/NEW_Z_SCOPED_FINDINGS_SESSION_4*.csv')+glob.glob(R+'/edition/PROGRAM/registers/*.csv')+glob.glob(R+'/edition/PROGRAM/registers/*.json')
lines=[]
for f in recfiles:
    for l in open(f,errors='replace'): lines.append((os.path.basename(f),l))
rec='\n'.join(l for _,l in lines)
PK=re.compile(r'^(passed|pass|met|ok|holds)$',re.I)
for f in sorted(files):
    rel=os.path.relpath(f,R)
    if 'outlier-scan' in rel: continue
    try: J=json.loads(open(f).read(),parse_constant=lambda x:None)
    except Exception as e: print('UNPARSEABLE',rel);continue
    fails=[]
    def walk(o,p,depth):
        if isinstance(o,dict):
            for k,v in o.items():
                if v is False and (PK.match(k) or re.match(r'^[A-Z]\d+[a-z]?\d?(_|$)',k) or k.endswith('_met')) and depth<=3 and 'rows' not in p and 'instances' not in p and 'carriers' not in p:
                    fails.append(p+'/'+k)
                if k.lower() in('failed','failures','failed_predicates') and isinstance(v,list) and v: fails.append(p+'/'+k+'='+str(v)[:80])
                walk(v,p+'/'+k,depth+1)
        elif isinstance(o,list):
            for i,v in enumerate(o): walk(v,f'{p}[{i}]',depth+1)
    walk(J,'',0)
    if not fails: continue
    parts=rel.split('/'); stem=os.path.splitext(parts[-1])[0]
    prog=[stem, re.sub(r'_Results?$|_result.*$|_results$','',stem), parts[-2]]
    prog=[x for x in dict.fromkeys(prog) if len(x)>3 and x not in('Z4_COMPUTATION','Director_Z_cross_review','Director_Z_challenger','results')]
    phit=[x for x in prog if x in rec or x.replace('_',' ') in rec]
    print('==',rel,'| program mentioned as:',phit or 'NONE')
    for fl in fails[:8]:
        ids=re.findall(r'(?:^|/)([A-Z]\d+[a-z]?\d?)(?=_|/|$|=)',fl)+re.findall(r"'([A-Z]\d+\w*)'",fl)
        full=[q for q in fl.split('/') if len(q)>12]
        ok=False;where=''
        for fn_,l in lines:
            if any(x in l or x.replace('_',' ') in l for x in phit) and any(re.search(r'\b'+re.escape(i)+r'\b',l) for i in ids): ok=True;where=fn_;break
            if any(q in l for q in full): ok=True;where=fn_;break
        print('   ',fl[:110],'| ids',ids,'|', 'RECORDED in '+where if ok else 'NOT FOUND (pred id + program on one line)')
    if len(fails)>8: print('    ... +',len(fails)-8)
