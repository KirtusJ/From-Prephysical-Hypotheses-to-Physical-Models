import json,sys,hashlib
R='/home/user/From-Prephysical-Hypotheses-to-Physical-Models/Director_G/results/'
def walk(a,b,p,out):
    if type(a)!=type(b) and not (isinstance(a,(int,float)) and isinstance(b,(int,float))):
        out.append((p,'type',repr(a)[:60],repr(b)[:60]));return
    if isinstance(a,dict):
        for k in sorted(set(a)|set(b)):
            if k not in a or k not in b: out.append((p+'/'+k,'missing in '+('stored' if k not in a else 'rerun'),'',''))
            else: walk(a[k],b[k],p+'/'+k,out)
    elif isinstance(a,list):
        if len(a)!=len(b): out.append((p,'len',len(a),len(b)));return
        for i,(x,y) in enumerate(zip(a,b)): walk(x,y,p+'/%d'%i,out)
    elif a!=b:
        out.append((p,'value',repr(a)[:70],repr(b)[:70]))
for f in ['local_mediator','moving_source_records','three_tick_signal']:
    sa=open(R+f+'.json','rb').read(); sb=open('copy/results/'+f+'.json','rb').read()
    a=json.loads(sa); b=json.loads(sb); out=[]; walk(a,b,'',out)
    nd=[o for o in out if o[1]=='value' and isinstance(json.loads('0'),int)]
    mx=0
    for o in out:
        if o[1]=='value':
            try: mx=max(mx,abs(float(o[2])-float(o[3])))
            except: mx=float('inf')
    print(f,'bytes',len(sa),len(sb),'identical' if sa==sb else 'DIFFERENT','CRLF' if b'\r\n' in sa else 'LF','ndiff',len(out),'max num diff',mx)
    for o in out[:12]: print('   ',o)
