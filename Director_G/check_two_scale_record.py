"""Two position clocks on a single continuously forced, rail-heralded walker.

Run with NumPy: python -B check_two_scale_record.py NEW_DIRECTORY
Terminal rows are unnormalized per incident character; the census restores
the localized-sheet prior. All clocks count physical signed Hadamard steps.
"""
import argparse
from collections import defaultdict
from fractions import Fraction
import json
import math
from pathlib import Path

import numpy as np

from check_same_flight_sheet_selection import even_nearest, require


def interval_probability(mean, variance, lower, upper):
    scale = math.sqrt(2*variance)
    return (math.erf((upper-mean)/scale) - math.erf((lower-mean)/scale))/2


def reference(lam, tau, aperture):
    variance = (lam + tau*tau/lam)/2
    shift = lam*tau + tau*tau/2
    return {side:0.5*interval_probability(sign*shift,variance,*aperture)
            for side,sign in (("minus",-1),("plus",1))}


def scales(order, overrides=None):
    dq = (math.pi/order)**(1/3)
    dc = (math.pi/order)**(1/4)
    m,nq,nc = overrides or (even_nearest(0.5*order**(2/3)),
                             even_nearest(1/dq**2),even_nearest(1/dc**3))
    return dq,dc,m,nq,nc


def geometry(order, overrides, aperture):
    dq,dc,m,nq,nc = scales(order,overrides)
    radius = 2*m+nq+nc
    require(radius < 2*order, "full cone wraps the physical ring")
    x = np.arange(-radius,radius+1)
    tau,t = nq*dq**2,nc*dc**3
    center,r = t*t/2,t*t/8
    early = (dq*x>aperture[0]) & (dq*x<aperture[1])
    late = np.array([abs(dc**2*x+center)<=r,abs(dc**2*x-center)<=r])
    late = np.vstack((late,~np.any(late,axis=0)))
    require(np.all(late.sum(axis=0)==1), "terminal bins must partition the sites")
    info = dict(M=order,m=m,nq=nq,nc=nc,delta_q=dq,delta_c=dc,
                microscopic_position="x relative to the initial sharp well",
                early_aperture_open=list(aperture),lambda_q_attained=m*dq*dq,
                quantum_elapsed_after_source=tau,classical_elapsed_after_mask=t,
                source_quantum_duration=2*m*dq*dq,source_classical_duration=2*m*dc**3,
                early_flight_classical_duration=nq*dc**3,
                late_tube_centers=[-center,center],late_tube_radius=r,
                early_reachable_pass_sites=x[early & (abs(x)<=2*m+nq) & ((x-nq)%2==0)].tolist(),
                late_reachable_minus_sites=x[late[0] & ((x-nq-nc)%2==0)].tolist(),
                late_reachable_plus_sites=x[late[1] & ((x-nq-nc)%2==0)].tolist(),
                continuum_unit_target=reference(0.5*math.pi**(2/3),1,aperture),
                gaussian_at_attained_quantum_clock=reference(m*dq*dq,tau,aperture))
    return x, early, late, info


def advance(r,l,kick,steps):
    for _ in range(steps):
        outgoing_r=(r+l)*kick
        outgoing_l=(r-l)*kick
        r[...,1:]=outgoing_r[...,:-1]
        l[...,:-1]=outgoing_l[...,1:]
        r[...,0]=0
        l[...,-1]=0


def squared(r,l):
    return abs(r)**2 + abs(l)**2


def late_bins(density, late):
    return np.array([np.sum(density[...,mask],axis=-1) for mask in late]).T


def finite_row(charge, x, early, late, info, hidden=False, launch_rail=1):
    order,m,nq,nc=(info[key] for key in ("M","m","nq","nc"))
    kick=np.exp(-2j*math.pi*((charge*(x//2))%order)/order)/math.sqrt(2)
    r=np.zeros(x.size,dtype=complex)
    l=np.zeros_like(r)
    (r if launch_rail==1 else l)[x.size//2]=1
    first_fail=[]
    for block in range(1,m+1):
        advance(r,l,kick,2)
        rejected=l if launch_rail*(-1)**block==1 else r
        first_fail.append(float(np.vdot(rejected,rejected).real))
        rejected.fill(0)
    survival=float(squared(r,l).sum())
    require(survival>0,"finite sample underflow in the rail word")
    advance(r,l,kick,nq)
    # The two rows are the orthogonal Boolean pointer outcomes. Respect both coins.
    rr=np.stack((np.where(early,r,0),np.where(~early,r,0)))
    ll=np.stack((np.where(early,l,0),np.where(~early,l,0)))
    advance(rr,ll,kick,nc)
    bins=late_bins(squared(rr,ll),late)
    no_read=late_bins(squared(rr.sum(axis=0),ll.sum(axis=0)),late)
    balance=abs(sum(first_fail)+float(bins.sum())-1)
    require(balance<5e-10 and abs(survival-float(no_read.sum()))<5e-10,
            "first-fail, two pointer bins and all terminal outcomes must balance")
    cond=bins/survival
    untagged = no_read / survival
    out=dict(s=charge,launch_rail=launch_rail,survival=survival,
             first_fail=first_fail,early_pass=float(bins[0].sum()),
             quantum_then_classical=bins.tolist(),conditional_on_source=cond.tolist(),
             no_early_read_conditional_late=untagged.tolist(),
             mass_error=balance)
    if abs(charge)==1:
        predicted=np.array(list(info["continuum_unit_target"].values()))
        out["unit_limit_residual_early_pass_late_minus_plus"]=(cond[0,:2]-predicted).tolist()
        out["early_pass_limit_residual"]=float(cond[0].sum()-predicted.sum())
    if hidden:
        # Keep the two amplitudes at each recorded passing site coherent; trace
        # different sites only after applying the same further physical flight.
        hidden_bins=np.zeros(3)
        for j in np.flatnonzero(early & (squared(r,l)>0)):
            rc=np.zeros_like(r)
            lc=np.zeros_like(l)
            rc[j],lc[j]=r[j],l[j]
            advance(rc,lc,kick,nc)
            hidden_bins+=late_bins(squared(rc,lc),late)
        require(abs(float(hidden_bins.sum()-bins[0].sum()))<5e-12,
                "late site tags changed the earlier pass weight")
        out["site_copied_pass_final_joint"]=hidden_bins.tolist()
        out["site_copied_pass_conditional_on_source"]=(hidden_bins/survival).tolist()
        out["coherent_minus_site_copied_given_source"]=((bins[0]-hidden_bins)/survival).tolist()
    return out


def panel(order, charges=None, aperture=(0,2), hidden=False, overrides=None, launch_rail=1):
    x,early,late,info=geometry(order,overrides,aperture)
    full=charges is None
    if full:
        charges=range(order//2+1)
    rows=[finite_row(s,x,early,late,info,hidden,launch_rail) for s in charges]
    info.update(all_folded_labels=full,rows=rows)
    if full:
        multiplicity=[1 if (2*row["s"])%order==0 else 2 for row in rows]
        require(sum(multiplicity)==order,"incorrect number of incident sheet characters")
        aggregate=sum(w*np.array(row["quantum_then_classical"]) for w,row in zip(multiplicity,rows))/order
        incident_unit=2*np.array(rows[1]["quantum_then_classical"])/order
        pass_sides=aggregate[0,:2]
        first_fail=sum(w*np.array(row["first_fail"]) for w,row in zip(multiplicity,rows))/order
        info["original_localized_sheet"]=dict(
            first_fail=first_fail.tolist(),joint=aggregate.tolist(),true_unit_joint=incident_unit.tolist(),
            unit_fraction_at_early_yes_and_final_sides=[
                float(u/p) if p else None for u,p in zip(incident_unit[0,:2],pass_sides)],
            check_total=float(first_fail.sum()+aggregate.sum()))
        if hidden:
            mixture=sum(w*np.array(row["site_copied_pass_final_joint"]) for w,row in zip(multiplicity,rows))/order
            info["original_localized_sheet"]["site_copied_pass_final_joint"]=mixture.tolist()
    return info


def exact_history(order, info, hidden):
    """Integer path amplitudes at the original clock addresses, with a pointer."""
    aperture=info["early_aperture_open"]
    x,early,late,_=geometry(order,(info["m"],info["nq"],info["nc"]),aperture)
    radius=len(x)//2
    m,nq=info["m"],info["nq"]
    state={(0,1,0,None):1}
    failures=[]
    for tick in range(1,radius+1):
        new=defaultdict(int)
        for (j,c,y,record),z in state.items():
            ny=(y+j//2)%order
            for d in (1,-1):
                point=j+d
                tag=record
                if tick==2*m+nq:
                    yes=bool(early[radius+point])
                    tag=(yes,point if hidden and yes else None)
                new[point,d,ny,tag]+= -z if c==d==-1 else z
        if tick<=2*m and tick%2==0:
            keep=(-1)**(tick//2)
            failures.append(Fraction(sum(z*z for (_,c,_,_),z in new.items() if c!=keep),2**tick))
            new={k:z for k,z in new.items() if k[1]==keep and z}
        state=new
    bins=[[0,0,0],[0,0,0]]
    for (point,_,_,(yes,_)),z in state.items():
        idx=int(np.flatnonzero(late[:,radius+point])[0])
        bins[0 if yes else 1][idx]+=z*z
    den=2**radius
    require(sum(failures)+Fraction(sum(map(sum,bins)),den)==1,"integer total")
    return dict(denominator=den,numerators=bins,first_fail=[str(f) for f in failures])


def exact_controls():
    controls=[]
    for order in (29,30):
        data=panel(order,aperture=(0,2),hidden=True,overrides=(2,4,6))
        entry=dict(M=order,m=2,nq=4,nc=6,early_sites=data["early_reachable_pass_sites"],
                   late_minus=data["late_reachable_minus_sites"],late_plus=data["late_reachable_plus_sites"])
        for copy,key in ((False,"coherent"),(True,"site_copied")):
            exact=exact_history(order,data,copy)
            actual=np.array(data["original_localized_sheet"]["joint"])
            if copy:
                actual[0]=data["original_localized_sheet"]["site_copied_pass_final_joint"]
            err=float(np.max(abs(actual-np.array(exact["numerators"])/exact["denominator"])))
            require(err<2e-12,"signed sheet histories disagree with projected-fibre mixture")
            entry[key]=dict(**exact,max_joint_error=err)
        require(entry["coherent"]["numerators"]!=entry["site_copied"]["numerators"],"chosen hidden-site control is blind")
        controls.append(entry)
    return controls


def fair_count(order):
    """Each rail read restricts the last of the block's two fair choices.
    Over even m switches the imposed last increments cancel, leaving a
    binomial sum of m free increments at release, conditional on the word.
    """
    x,early,late,info=geometry(order,None,(0,2))
    m,nq,nc=(info[k] for k in ("m","nq","nc"))
    radius=x.size//2
    bins=np.zeros((2,3))
    for k in range(m+nq+1):
        point=2*k-m-nq
        p=math.comb(m+nq,k)/2**(m+nq)
        for j in range(nc+1):
            dest=point+2*j-nc
            mask=0 if early[radius+point] else 1
            column=int(np.flatnonzero(late[:,radius+dest])[0])
            bins[mask,column]+=p*math.comb(nc,j)/2**nc
    require(abs(bins.sum()-1)<2e-12,"conditional count total")
    return dict(M=order,m=m,survival=2.0**(-m),
                conditional_on_word=bins.tolist(),joint=(bins*2.0**(-m)).tolist())


def run():
    census=[panel(order,hidden=order<=65) for order in (32,33,64,65,128,129,256,257)]
    unit=[panel(order,[1,-1,0,2,order//2]) for order in (1024,1025,8192,8193,32768)]
    sign_controls=[]
    for order in (65,512,1025):
        a=panel(order,[1,-1],hidden=True)
        b=panel(order,[1],aperture=(-2,0),hidden=True,launch_rail=-1)
        original=np.array(a["rows"][0]["quantum_then_classical"])
        conjugate=np.array(a["rows"][1]["quantum_then_classical"])
        mirror=np.array(b["rows"][0]["quantum_then_classical"])[:,[1,0,2]]
        err=float(max(np.max(abs(original-conjugate)),np.max(abs(original-mirror))))
        require(err<5e-12,"conjugate sector or reflected aperture/launch/side")
        sign_controls.append(dict(positive_and_conjugate=a,reflected_left=b,max_joint_error=err))
    return dict(settings=dict(F=1,lambda_M_scale=0.5,early_target_time=1,late_target_time=1,
                              early_interval="0 < delta_q*x < 2 (strict)",
                              late_tube_centers="±T_n²/2",late_radius="T_n²/8 (inclusive)",
                              row_order=["early pass","early fail"],column_order=["late minus tube","late plus tube","other"],
                              site_copy="copy individual site only on a passing early membership outcome; preserve rails within a site",
                              predicates="mass, sign conjugacy, reflected launch/coordinates, exact signed integer-history comparison; no approximation-quality threshold"),
                exact_lift=exact_controls(),fair_count=[fair_count(q) for q in (32,33,64,65,128,129,256,257)],
                census=census,selected_large_orders=unit,
                sign_controls=sign_controls)


if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("destination",type=Path)
    out=ap.parse_args().destination/"two_scale_record.json"
    if out.exists():
        raise FileExistsError(out)
    result=run()
    out.parent.mkdir(parents=True,exist_ok=True)
    with out.open("x",encoding="utf-8",newline="\n") as stream:
        json.dump(result,stream,indent=2,allow_nan=False)
        stream.write("\n")
