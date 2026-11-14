"""Exact two-mode unitary evolution and persistent first-flip controls."""
import argparse
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path


def check(condition, why):
    if not condition:
        raise ValueError(why)


def add(z,w):
    return (z[0]+w[0],z[1]+w[1])


def mul(z,w):
    return (z[0]*w[0]-z[1]*w[1],z[0]*w[1]+z[1]*w[0])


def star(z):
    return (z[0],-z[1])


def scale(k,z):
    return (k*z[0],k*z[1])


def norm(z):
    return z[0]**2+z[1]**2


def gaussian_panels():
    # Rational stereographic coordinates cover exact SU(2) matrices up to one pole.
    rows=[]
    for v in product((-2,0,1),repeat=3):
        n=sum(x*x for x in v)
        w,x,y,z=[F(k,1+n) for k in (1-n,*[2*k for k in v])]
        u=(w,x)
        b=(y,z)
        q=norm(b)
        r=4*w*w
        check(norm(u)+q==1,"unitarity")
        R,L=(F(1),F(0)),(F(0),F(0))
        polynomials=[F(0),F(1)]
        rates=[]
        for t in range(1,9):
            R,L=add(mul(u,R),mul(b,L)),add(scale(-1,mul(star(b),R)),mul(star(u),L))
            check(norm(R)+norm(L)==1,"norm preservation")
            check(norm(L)==q*polynomials[t]**2,"exact line element vs characteristic recurrence")
            rates.append(norm(L))
            polynomials.append(2*w*polynomials[-1]-polynomials[-2])
        # Sum postmeasurement joint probabilities for actual initial R, measured L then final R.
        first_lower=scale(-1,star(b))
        joint=norm(mul(b,first_lower))
        check(joint==q*q,"monitored record")
        for a in (F(0),F(1,3),F(1),F(3,2),F(2)):
            score=rates[2]+2*(1-a)*rates[1]+(a*a-1)*rates[0]
            check(score==q*(r-a)**2,"characteristic variance")
        rows.append(dict(stereographic=v,q=q,r=r,left=rates,joint=joint))
    return rows


def intensity_factor_series(r, clocks):
    """Squared U_{t-1}(sqrt(r)/2) with no numerical square roots."""
    factors=[F(0),F(1),r]
    for _ in range(3,clocks+1):
        factors.append((r-2)*factors[-1]-factors[-2]+2)
    return factors[1:clocks+1]


def rates(components,c,ticks):
    ans=[c/2]*ticks
    flip=c/4
    for mass,q,r in components:
        check(mass>=0 and 0<=q<=1 and 0<=r<=4*(1-q),"invalid physical component")
        ans=[p+mass*q*h for p,h in zip(ans,intensity_factor_series(r,ticks))]
        flip+=mass*q*q
    check(c+sum(mass for mass,q,r in components)==1,"not a mixture")
    return ans,flip


def compare(name,a,components,c,monitored=None):
    L,flip=rates(components,c,24)
    if monitored is not None:
        flip=monitored
    score=L[2]+2*(1-a)*L[1]+(a*a-1)*L[0]
    balance=flip-L[0]+F(1,4)
    wantW=sum(z*q*(r-a)**2 for z,q,r in components)+c*((a-1)**2+1)/2
    wantD=sum(z*(q-F(1,2))**2 for z,q,r in components)
    check(score==wantW,"mixture score")
    check((balance==wantD)==(monitored is None),"stable vs resampled flip")
    return dict(label=name,target_trace_squared=a,components=components,count=c,
                free_left=L,monitored_L_then_R=flip,W=score,D=balance)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_directory",type=Path)
    out=parser.parse_args().output_directory
    s=F(1,2)
    rows=[]
    for a in (F(0),F(1,4),F(1),F(3,2),F(19,10),F(2)):
        ideal=compare("balanced_target",a,[(F(1),s,a)],F(0))
        rows.append(ideal)
        if a<2:
            delta=(2-a)/8
            coins=[(s,s-delta,a),(s,s+delta,a)]
            matched=compare("unbalanced_pair",a,coins,F(0))
            check(matched["free_left"]==ideal["free_left"] and matched["D"]==delta**2,
                  "all-clock finite alias and resolving intervention")
            rows.append(matched)
            resampled=sum(w1*w2*q1*q2 for w1,q1,_ in coins for w2,q2,_ in coins)
            redrawn=compare("coin_redrawn_after_record",a,coins,F(0),monitored=resampled)
            check(redrawn["W"]==redrawn["D"]==0,"intervention-disturbance counterexample")
            rows.append(redrawn)
    rows.extend([compare("invisible_diagonal",F(3,2),[(1,F(0),F(4))],F(0)),
                 compare("fair_count",F(3,2),[],F(1)),
                 compare("mixed_with_count",F(3,2),[(s,F(1,3),F(2)),(F(1,4),s,F(3,2))],F(1,4))])
    check(rows[-3]["W"]==0 and rows[-3]["D"]==F(1,4),"diagonal loophole")
    reduced_checks=[]
    for row in rows:
        if row["label"]=="coin_redrawn_after_record":
            continue
        a=row["target_trace_squared"]
        L=row["free_left"]
        if a>1:
            fewer=L[2]+2*(1-a)*L[1]+(a*a-1)*(row["monitored_L_then_R"]+F(1,4))
            check(fewer==row["W"]+(a*a-1)*row["D"] and
                  ((fewer==0)==(row["W"]==0 and row["D"]==0)), "three-setting certificate")
            reduced_checks.append(dict(label=row["label"],a=a,three_setting_score=fewer))
        check((L[1]==1)==(row["count"]==0 and
              all((q==s and r==2) for w,q,r in row["components"] if w)),"single-setting endpoint")
    cubic=next(r for r in rows if r["label"]=="unbalanced_pair" and r["target_trace_squared"]==F(3,2))
    lossy=cubic["monitored_L_then_R"]*F(64,65)
    check(lossy==F(1,4),"missed joint records can imitate target")
    p2,p3=cubic["free_left"][1:3]
    cubic_direct=p3-p2+F(5,4)*(lossy+F(1,4))
    check(cubic_direct==0,"false three-setting zero")
    result=dict(gaussian_matrix_replay=gaussian_panels(),mixtures=rows,
                reduced_certificates=reduced_checks,
                missing_joint_records=dict(true=cubic["monitored_L_then_R"],
                                          efficiency=F(64,65),observed=lossy),
                physical_feasibility="0<=q<=1; 0<=r<=4(1-q)")
    out.mkdir(exist_ok=True,parents=True)
    with (out/"unknown_two_mode_coin.json").open("x",encoding="utf8",newline="\n") as f:
        json.dump(result,f,indent=2,default=str)
        f.write("\n")


if __name__=="__main__":
    main()
