"""xr77 cross-review program for Director_G/Double_flips_in_rotating_spin_records.md.
Written from the note's definitions; parses Figure5.pdf by geometry (all rectangles on the
lower-panel baseline), not by the checker's object numbers.  Seed 20261114.  Refuses to overwrite.

PREDICATES (fixed before first run; failures are kept in the result file):
P1  archive sha256 == 60e88b33... and Figure5.pdf sha256 == 40a36cbe... (pinned in the checker).
P2  exactly 16 filled ('B') and 16 stroked-only ('S') bars with bottom at 238.156 +- 0.001 pt
    (0.001 pt = last printed digit of the PDF coordinates); x strictly increasing.
P3  my 32 normalized frequencies == filed JSON, |diff| <= 1e-12 (double round-off only).
P4  UN-normalized sum of each series (height / (16*14.855 pt), scale from the red 1/16 line)
    is 1 within 16*0.0005/237.68 = 3.4e-5 (worst-case coordinate rounding).  Residual reported.
P5  table values of the note (4 dp) and the summary's 0.25284/0.26101/0.23865/0.25082 are the
    correct roundings of exact Fraction arithmetic on the heights.
P6  pooled double flip == P(b2=b0) - P(b0=b1=b2) exactly (Fractions).
P7a reading resolution: worst-case change of each heralded ratio under +-0.0005 pt per height < 5e-6
    (what five quoted decimals need).
P7b statistical: binomial s.e. of each heralded ratio < 5e-6.  HYPOTHESIS: shot number N from the
    figure's own error bars assuming half-length = sqrt(p(1-p)/N) (the paper states binomial s.d.
    for Fig. 3; NOT stated for Fig. 5 -> assumption).  Tested per bar: bar qualifies if it has an
    error bar centred on its top within 0.002 pt.
P8  every one of the 32 bars has such an error bar (qualifying count reported), and N estimates
    reported with min/median/max (no threshold; a measurement).
P9  count lattice: is there an integer N in [200,50000] with every freq*N within
    N*0.0005/237.68+1e-9 of an integer (i.e. heights are plotted counts/N)?  List of N reported.
P10 each double-flip value (4 heralded + 2 pooled) is within 2 binomial s.e. of the ideal 1/4
    (2 s.e. is a convention, z reported so the reader can apply another).
P11 order symmetry (the note's temporal-order test): pooled two-flip patterns 011,101,110 and
    one-flip patterns 001,010,100 pairwise equal within 2 s.e. (multinomial difference s.e.); and
    a 4-dof chi-square of the exchangeable model on the 8 flip words, p by simulation (20000 draws).
P12 instance NOT in the note: double flip on reads 2-4 (herald b1, event b2!=b1, b3==b1), both
    series, both rails: within 2 s.e. of 1/4.
P13 classical models: (a) in class (exchangeable mixture) reproduces the 8 flip-word table exactly
    (expected to fail unless orders are exactly equal: max residual reported);
    (b) just outside class (independent flips with tick-dependent q1,q2,q3) max residual reported;
    (c) classical lookup model (hidden variable = the 4-bit word) reproduces all 16 exactly.
"""
import sys, re, zlib, json, hashlib, tarfile, io, math, random, statistics
from fractions import Fraction as Fr
from pathlib import Path
SEED=20261114
src, filed, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
if out.exists(): sys.exit("refuse to overwrite "+str(out))
R={"seed":SEED,"predicates":{}}
def P(name, ok, qualifying=None, **kw):
    R["predicates"][name]=dict(passed=bool(ok), qualifying=qualifying, **kw)
raw=src.read_bytes(); a=hashlib.sha256(raw).hexdigest()
pdf=tarfile.open(fileobj=io.BytesIO(raw)).extractfile("Figure5.pdf").read(); f=hashlib.sha256(pdf).hexdigest()
P("P1", a=="60e88b33bd94d8a65fec0b3151d7afff75149e1be2dbd7a8c6f1dd2875d98557" and f=="40a36cbe3dc423241c604932f61cbc7a4e146eb4306e47d7b34ac685f47bd512", archive=a, figure=f)
texts=[]
for m in re.finditer(rb"stream\r?\n", pdf):
    e=pdf.find(b"endstream", m.end())
    try: texts.append(zlib.decompress(pdf[m.end():e]).decode("latin1"))
    except Exception: pass
BASE=Fr("238.156"); num=r"(-?\d+(?:\.\d+)?)"
bars={"B":[], "S":[]}; segs=[]
for t in texts:
    for x,y,w,h,op in re.findall(num+" "+num+" "+num+" "+num+r" re\s+([BSf])\b", t):
        x,y,w,h=map(Fr,(x,y,w,h))
        if op in "BS" and h<0 and abs(y+h+BASE)<=Fr("0.001") and 6<w<8: bars[op].append((x,-h,w))
    for x1,y1,x2,y2 in re.findall(num+" "+num+" m "+num+" "+num+" l", t):
        x1,y1,x2,y2=map(Fr,(x1,y1,x2,y2))
        if x1==x2 and y1!=y2: segs.append((x1,-y1,-y2))
for k in bars: bars[k].sort()
ok2=all(len(v)==16 and all(a[0]<b[0] for a,b in zip(v,v[1:])) for v in bars.values())
P("P2", ok2, counts={k:len(v) for k,v in bars.items()})
SCALE=16*Fr("14.855")
J=json.loads(filed.read_text())
names={"B":"initially_and_finally_detected","S":"initially_detected"}
rng=random.Random(SEED)
maxd=0; res={}
for k,v in bars.items():
    H=[b[1] for b in v]; tot=sum(H); words=[format(i,"04b") for i in range(16)]
    p={w:h/tot for w,h in zip(words,H)}
    S={}; res[names[k]]=S
    d=max(abs(float(p[w])-J[names[k]]["words"][w]["frequency"]) for w in words); maxd=max(maxd,d)
    S["raw_sum_minus_1"]=float(tot/SCALE-1); S["raw_sum_pt"]=str(tot)
    S["distinct_heights"]=len(set(H)); S["height_diffs_sorted_pt"]=[float(b-a) for a,b in zip(sorted(set(H)),sorted(set(H))[1:])]
    # error bars -> N
    Ns=[]; q=0; eb={}
    for (x,h,w),wd in zip(v,words):
        c=[s for s in segs if abs(s[0]-(x+w/2))<=Fr("0.01") and abs((s[1]+s[2])/2+ (BASE-h) - 0)<=Fr("0.002") ] if False else \
          [s for s in segs if abs(s[0]-(x+w/2))<=Fr("0.01") and abs((s[1]+s[2])/2-(BASE-h))<=Fr("0.002")]
        if c:
            q+=1; half=abs(c[0][1]-c[0][2])/2/SCALE; pr=h/SCALE
            n=float(pr*(1-pr)/half**2); Ns.append(n); eb[wd]=dict(half_width=float(half), N_binomial=n)
    S["errorbars_matched"]=q; S["errorbars"]=eb
    N=statistics.median(Ns) if Ns else None
    S["N_est"]=dict(min=min(Ns),median=N,max=max(Ns)) if Ns else None
    # lattice
    lat=[n for n in range(200,50001) if all(abs(float(h/SCALE)*n-round(float(h/SCALE)*n))<=n*0.0005/237.68+1e-9 for h in H)]
    S["count_lattice_N"]=lat[:40]; S["count_lattice_total"]=len(lat)
    # statistics
    def pr(f): return sum(x for w,x in p.items() if f(w))
    ev={}
    for r in "01":
        den=pr(lambda w:w[0]==r)
        ev["first_flip|"+r]=(pr(lambda w:w[0]==r and w[1]!=r),den)
        ev["double_flip|"+r]=(pr(lambda w:w[0]==r and w[1]!=r and w[2]==r),den)
        den2=pr(lambda w:w[1]==r)
        ev["reads2-4_double_flip|b1="+r]=(pr(lambda w:w[1]==r and w[2]!=r and w[3]==r),den2)
    ev["pooled_double"]=(pr(lambda w:w[0]!=w[1] and w[2]==w[0]),Fr(1))
    ev["pooled_reads2-4_double"]=(pr(lambda w:w[1]!=w[2] and w[3]==w[1]),Fr(1))
    S["P6_identity"]= ev["pooled_double"][0]==pr(lambda w:w[0]==w[2])-pr(lambda w:w[0]==w[1]==w[2])
    S["stats"]={}
    for nm,(nu,de) in ev.items():
        val=nu/de; fv=float(val)
        # reading resolution: +-0.0005pt each height, worst case first order
        dres=float((Fr("0.0005")/tot)*(8*(1-val)*0+ (4 if 'double' in nm and 'pooled' not in nm else 8))/de*2)
        se=math.sqrt(fv*(1-fv)/(N*float(de))) if N else None
        S["stats"][nm]=dict(value=fv, denominator=float(de), reading_resolution_bound=dres, se_binomial=se,
                            z_vs_quarter=((fv-0.25)/se if se and 'double' in nm else None),
                            z_vs_half=((fv-0.5)/se if se and 'first' in nm else None))
    fw={}
    for w,x in p.items():
        c="".join("0" if a==b else "1" for a,b in zip(w,w[1:])); fw[c]=fw.get(c,0)+x
    S["flip_words"]={c:float(x) for c,x in sorted(fw.items())}
    pairs={}
    for grp in (("011","101","110"),("001","010","100")):
        for i in range(3):
            for j in range(i+1,3):
                a_,b_=float(fw[grp[i]]),float(fw[grp[j]]); se=math.sqrt((a_+b_-(a_-b_)**2)/N)
                pairs[grp[i]+"-"+grp[j]]=dict(diff=a_-b_, se=se, z=(a_-b_)/se)
    S["order_pairs"]=pairs
    # exchangeable fit: average within flip count
    fit={c:float(sum(fw[d_] for d_ in fw if d_.count("1")==c.count("1"))/sum(1 for d_ in fw if d_.count("1")==c.count("1"))) for c in fw}
    chi=sum(N*(float(fw[c])-fit[c])**2/fit[c] for c in fw)
    cs=sorted(fw); wts=[fit[c] for c in cs]; n=int(round(N)); ge=0; T=20000
    for _ in range(T):
        cnt=[0]*8
        for i in rng.choices(range(8),weights=wts,k=n): cnt[i]+=1
        m={}
        for c,x in zip(cs,cnt): m.setdefault(c.count("1"),[]).append(x)
        ch=sum((x-sum(m[c.count("1")])/len(m[c.count("1")]))**2/(sum(m[c.count("1")])/len(m[c.count("1")])) for c,x in zip(cs,cnt))
        ge+= ch>=chi
    S["exchangeable_fit"]=dict(max_abs_residual=max(abs(float(fw[c])-fit[c]) for c in fw), chi2_4dof=chi, p_sim=ge/T, N_used=n)
    # tick-dependent independent flips: q_t = marginal flip rate at tick t
    qs=[float(sum(x for c,x in fw.items() if c[t]=="1")) for t in range(3)]
    ind={c:math.prod(qs[t] if c[t]=="1" else 1-qs[t] for t in range(3)) for c in fw}
    S["tick_dependent_independent_flips"]=dict(q=qs, max_abs_residual=max(abs(float(fw[c])-ind[c]) for c in fw),
        chi2_4dof=sum(N*(float(fw[c])-ind[c])**2/ind[c] for c in fw))
    S["lookup_model_exact"]= (sum(p.values())==1)
R["series"]=res
P("P3", maxd<=1e-12, max_abs_diff=maxd)
P("P4", all(abs(s["raw_sum_minus_1"])<=16*0.0005/237.68 for s in res.values()), residuals={k:s["raw_sum_minus_1"] for k,s in res.items()}, bound=16*0.0005/237.68)
I=res["initially_detected"]["stats"]; Fn=res["initially_and_finally_detected"]["stats"]
quoted=[(I["first_flip|0"],"0.5080"),(I["double_flip|0"],"0.2528"),(I["first_flip|1"],"0.4716"),(I["double_flip|1"],"0.2386"),(I["pooled_double"],"0.2456"),
        (Fn["first_flip|0"],"0.4946"),(Fn["double_flip|0"],"0.2610"),(Fn["first_flip|1"],"0.5017"),(Fn["double_flip|1"],"0.2508"),(Fn["pooled_double"],"0.2559"),
        (I["double_flip|0"],"0.25284"),(Fn["double_flip|0"],"0.26101"),(I["double_flip|1"],"0.23865"),(Fn["double_flip|1"],"0.25082")]
bad=[(q,s["value"]) for s,q in quoted if f"{s['value']:.{len(q)-2}f}"!=q]
P("P5", not bad, qualifying=len(quoted), failed=bad)
P("P6", all(s["P6_identity"] for s in res.values()))
her=[(k,n,s) for k,S in res.items() for n,s in S["stats"].items() if n.startswith(("first_flip|","double_flip|"))]
P("P7a", all(s["reading_resolution_bound"]<5e-6 for _,_,s in her), qualifying=len(her), worst=max(s["reading_resolution_bound"] for _,_,s in her))
P("P7b", all(s["se_binomial"]<5e-6 for _,_,s in her), qualifying=len(her), smallest_se=min(s["se_binomial"] for _,_,s in her), largest_se=max(s["se_binomial"] for _,_,s in her), hypothesis="binomial error bars (assumed for Fig. 5)")
P("P8", all(S["errorbars_matched"]==16 for S in res.values()), qualifying=sum(S["errorbars_matched"] for S in res.values()), N={k:S["N_est"] for k,S in res.items()})
P("P9", all(S["count_lattice_total"]>0 for S in res.values()), lattice={k:(S["count_lattice_total"],S["count_lattice_N"][:12]) for k,S in res.items()})
t10=[(k,n,s["value"],s["z_vs_quarter"]) for k,S in res.items() for n,s in S["stats"].items() if n in("double_flip|0","double_flip|1","pooled_double")]
P("P10", all(abs(z)<2 for *_,z in t10), qualifying=len(t10), cases=t10, failed=[c for c in t10 if abs(c[3])>=2])
t11=[(k,n,d["diff"],d["z"]) for k,S in res.items() for n,d in S["order_pairs"].items()]
P("P11", all(abs(z)<2 for *_,z in t11), qualifying=len(t11), failed=[c for c in t11 if abs(c[3])>=2], exchangeable={k:S["exchangeable_fit"] for k,S in res.items()})
t12=[(k,n,s["value"],s["z_vs_quarter"]) for k,S in res.items() for n,s in S["stats"].items() if "reads2-4" in n]
P("P12", all(abs(z)<2 for *_,z in t12), qualifying=len(t12), cases=t12, failed=[c for c in t12 if abs(c[3])>=2])
P("P13a", all(S["exchangeable_fit"]["max_abs_residual"]==0 for S in res.values()), residual={k:S["exchangeable_fit"]["max_abs_residual"] for k,S in res.items()})
P("P13b", all(S["tick_dependent_independent_flips"]["max_abs_residual"]<1e-12 for S in res.values()), detail={k:S["tick_dependent_independent_flips"] for k,S in res.items()})
P("P13c", all(S["lookup_model_exact"] for S in res.values()))
with out.open("x") as o: json.dump(R,o,indent=1); o.write("\n")
for k,v in R["predicates"].items(): print(k, "PASS" if v["passed"] else "FAIL", "qualifying=",v["qualifying"])
