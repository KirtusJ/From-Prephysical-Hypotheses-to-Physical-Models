import json,os,re,sys,math,statistics,glob
R='/home/user/From-Prephysical-Hypotheses-to-Physical-Models'
files=[]
for d in ['Z4_COMPUTATION','Director_Z_challenger','Director_Z_cross_review','REVIEW_QUEUE/reports']:
    for dp,dn,fn in os.walk(os.path.join(R,d)):
        for f in fn:
            if f.endswith('.json'): files.append(os.path.join(dp,f))
rec=''
recfiles=glob.glob(R+'/ADDENDUM_EDITION_Z*_SESSION_4.md')+[R+'/DIRECTOR_Z_TECHNICAL_DISPOSITION_SESSION_4.md']+glob.glob(R+'/NEW_Z_SCOPED_FINDINGS_SESSION_4*.csv')+glob.glob(R+'/edition/PROGRAM/registers/*.csv')+glob.glob(R+'/edition/PROGRAM/registers/*.json')
for f in recfiles: rec+=open(f,errors='replace').read()+'\n'
RES=re.compile(r'resid|err|defect|dev|diff|gap|norm|max_|tol',re.I)
def const(x): return {'__nonfinite__':x}
out=[]
for f in sorted(files):
    try: J=json.loads(open(f).read(),parse_constant=const)
    except Exception as e:
        print('UNPARSEABLE',f,e); continue
    flags=[]
    def walk(o,p,key=''):
        if isinstance(o,dict):
            if '__nonfinite__' in o: flags.append(('b',p,o['__nonfinite__'],9e99));return
            nums={k:v for k,v in o.items() if isinstance(v,(int,float)) and not isinstance(v,bool)}
            fam=[abs(v) for k,v in nums.items() if RES.search(k)]
            if len(fam)>=3:
                m=statistics.median(fam)
                for k,v in nums.items():
                    if RES.search(k) and m>0 and abs(v)>100*m: flags.append(('c',p+'/'+k,v,abs(v)/m))
            # pass/run pairs
            ks={k.lower():k for k in o}
            for a,b in [('passed','run'),('pass','run'),('passed','total'),('pass','total'),('n_pass','n_run'),('n_pass','n'),('passed','checked'),('qualify','total'),('ok','total'),('met','total')]:
                if a in ks and b in ks and isinstance(o[ks[a]],(int,float)) and isinstance(o[ks[b]],(int,float)) and not isinstance(o[ks[a]],bool) and o[ks[a]]!=o[ks[b]]:
                    flags.append(('d',p+'/'+ks[a],f'{o[ks[a]]} vs {b}={o[ks[b]]}',1))
            for k,v in o.items(): walk(v,p+'/'+str(k),str(k))
        elif isinstance(o,list):
            ns=[abs(v) for v in o if isinstance(v,(int,float)) and not isinstance(v,bool)]
            if len(ns)>=3 and len(ns)==len(o):
                m=statistics.median(ns)
                for i,v in enumerate(o):
                    if m>0 and abs(v)>100*m and RES.search(p): flags.append(('c',f'{p}[{i}]',v,abs(v)/m))
            # list of dicts: same keyed family across siblings
            if len(o)>=3 and all(isinstance(x,dict) for x in o):
                keys=set().union(*[x.keys() for x in o])
                for k in keys:
                    vs=[(i,x[k]) for i,x in enumerate(o) if isinstance(x.get(k),(int,float)) and not isinstance(x.get(k),bool)]
                    if len(vs)>=3 and RES.search(k):
                        m=statistics.median([abs(v) for i,v in vs])
                        for i,v in vs:
                            if m>0 and abs(v)>100*m: flags.append(('c',f'{p}[{i}]/{k}',v,abs(v)/m))
            if key.lower() in('failures','failed','failed_predicates','fails') and len(o)>0: flags.append(('a',p,f'nonempty list len {len(o)}: {str(o)[:150]}',1e9))
            for i,v in enumerate(o): walk(v,f'{p}[{i}]',key)
        elif o is False: flags.append(('a',p,False,1e9))
        elif o is None: flags.append(('b',p,None,1e8))
        elif isinstance(o,str):
            s=o.strip()
            if re.fullmatch(r'(?i)fail(ed)?|not met|false',s) or re.match(r'(?i)^(FAIL|NOT MET)\b',s): flags.append(('a',p,s[:120],1e9))
            for m in re.finditer(r'\b(\d+)\s*(?:of|/)\s*(\d+)\b',s):
                if m.group(1)!=m.group(2) and re.search(r'(?i)pass|met|qualif|ok|hold|agree',s+key): flags.append(('d',p,s[:140],1))
            if re.fullmatch(r'(?i)-?(nan|inf(inity)?)',s): flags.append(('b',p,s,9e99))
        elif isinstance(o,float) and not math.isfinite(o): flags.append(('b',p,o,9e99))
    walk(J,'')
    rel=os.path.relpath(f,R)
    cnt={t:sum(1 for x in flags if x[0]==t) for t in 'abcd'}
    if not flags: out.append((rel,cnt,[]));continue
    print('==',rel,cnt)
    for t,p,v,s in sorted(flags,key=lambda x:-x[3])[:int(sys.argv[1]) if len(sys.argv)>1 else 3]:
        # mention check
        parts=rel.split('/'); names=set([parts[-2] if len(parts)>1 else '',os.path.splitext(parts[-1])[0]]+[p.split('/')[-1].split('[')[0]]+[q.split('[')[0] for q in p.split('/')[1:]])
        hit=[n for n in names if len(n)>4 and n in rec]
        print('  ',t,p,'=',str(v)[:150],'| x%.3g'%s if t=='c' else '','| recorded-by:',hit[:4] if hit else 'NONE')
print('\nclean files:',len(out),'of',len(files))
for r,c,_ in out: print('  ',r)
