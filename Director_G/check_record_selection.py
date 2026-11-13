"""Finite tests for record conditioning and the real algebra on a holonomy plane."""
import argparse
import csv
import json
import math
from itertools import product
from pathlib import Path

import numpy as np

from check_walk import lift_step, ring_step

ETA = 0.01


def block_operators():
    # Integer path coefficients, with the common factor 1/sqrt(8) omitted.
    blocks = {}
    for incoming in (1, -1):
        outcomes = {}
        for word in product((1, -1), repeat=3):
            site, displacement, sign, channel = 0, 0, 1, incoming
            for outgoing in word:
                displacement += site
                if channel == outgoing == -1:
                    sign *= -1
                site += outgoing
                channel = outgoing
            polynomial = outcomes.setdefault((site, channel), {})
            polynomial[displacement] = polynomial.get(displacement, 0) + sign
        blocks[incoming] = outcomes
    return blocks


def record_controls():
    blocks = block_operators()
    rows = []
    for m in (3, 5, 7, 8, 15):
        n = 4*m
        for incoming, outcomes in blocks.items():
            for origin in (0, n-2):
                for r in range(m):
                    h = 2*np.pi*r/m
                    sheet = np.exp(1j*h*np.arange(m)) / np.sqrt(m)
                    state = np.zeros((n, m, 2), complex)
                    state[origin, :, int(incoming == -1)] = sheet
                    for _ in range(3):
                        state = lift_step(state)
                    checks = []
                    for (dx, channel), poly in outcomes.items():
                        amplitude = sum(v*np.exp(-1j*h*(a+3*origin)) for a,v in poly.items()) / np.sqrt(8)
                        vec = state[(origin+dx) % n, :, int(channel == -1)]
                        checks.append(float(np.max(np.abs(vec-amplitude*sheet))))
                    same = state[(origin+incoming) % n, :, int(incoming == -1)]
                    other = state[(origin-incoming) % n, :, int(incoming == 1)]
                    measured = [np.vdot(same,same).real, np.vdot(other,other).real]
                    predicted = [np.cos(h)**2/2, np.sin(h)**2/2]
                    rows.append(dict(M=m,sector=r,incoming=incoming,origin=origin,
                                     amplitude_error=max(checks),law_error=float(np.max(np.abs(np.subtract(measured,predicted)))),
                                     norm_error=float(abs(np.vdot(state,state).real-1))))
    return rows


def preparation_controls():
    summary, trajectory = [], []
    for m in (3,5,7,15,31,63,127):
        indices = np.arange(m)
        r = (m-1)//2
        theta = 2*np.pi*r*indices/m
        pair = np.sqrt(2/m)*np.stack([np.cos(theta),np.sin(theta)],axis=1)
        c = np.cos(2*np.pi*indices/m)**2
        d = np.sin(2*np.pi*indices/m)**2
        target_fraction = 2*np.sin(np.pi/m)**2/m
        if m == 3:
            horizon = 0
        else:
            ratio = (math.cos(2*np.pi/m)/math.cos(np.pi/m))**2
            horizon = math.ceil(math.log(ETA*target_fraction/(1-ETA))/math.log(ratio))
        sheet = (np.roll(np.eye(1,m)[0],1)-np.roll(np.eye(1,m)[0],-1))/np.sqrt(2)
        log_probability = -math.log(4)
        for s in range(horizon+1):
            # Translation and overall sign do not affect the norm or pair weight.
            weights = d * c**s
            predicted_mass = float(weights[[r,m-r]].sum()/weights.sum())
            branch_log = -(s+1)*math.log(2)+math.log(float(weights.sum()/m))
            mass = float(np.sum((pair.T @ sheet)**2))
            trajectory.append((m,s,mass,log_probability/math.log(10),
                               abs(mass-predicted_mass),abs(branch_log-log_probability)))
            if s < horizon:
                next_sheet = (np.roll(sheet,1)+np.roll(sheet,-1))/np.sqrt(8)
                norm = np.linalg.norm(next_sheet)
                log_probability += 2*math.log(norm)
                sheet = next_sheet/norm
        q = math.sin(math.pi/m)**2
        # Hellinger affinity and likelihood-ratio bound for all other classes.
        k = math.ceil(math.log((m-1)/2/ETA)/(-math.log(np.cos(math.pi/m))))
        acceptance = 1-(m-1)/2*np.cos(math.pi/m)**k
        summary.append(dict(M=m,dense_records=horizon+1,posterior_mass=mass,
                            log10_record_probability=log_probability/math.log(10),
                            informative_samples=k,conditional_classification_error_bound=1-acceptance,
                            first_arrival_mean_blocks=2*k,
                            target_prior=2/m,zero_target_affinity=np.sqrt(1-q)))
    return summary, trajectory


def orientation_tests():
    rows = []
    for m in (5,7,15,31):
        for r in range(1,(m+1)//2):
            h = 2*np.pi*r/m
            n = 2*m
            for angle in (0, np.pi/2, -np.pi/2):
                state = np.zeros((n,2),complex)
                state[0,0] = 1/np.sqrt(2)
                state[2,0] = np.exp(1j*angle)/np.sqrt(2)
                conjugate_fields = []
                for field in (h,-h):
                    current = state.copy()
                    for _ in range(2):
                        current = ring_step(current,np.exp(-1j*field*np.arange(n)))
                    conjugate_fields.append(float(abs(current[0,1])**2))
                prediction = [(1-np.cos(angle-2*field))/4 for field in (h,-h)]
                rows.append(dict(M=m,r=r,angle=angle,probabilities=conjugate_fields,
                                 error=float(np.max(np.abs(np.subtract(conjugate_fields,prediction))))))
    return rows


def algebra_controls():
    rows = []
    j = np.array([[0.,-1.],[1.,0.]])
    for m in (3,5,7,15):
        n, r = 2*m, (m-1)//2
        h = 2*np.pi*r/m
        # Build the real directed edge transports in the two-dimensional plane.
        d = 2*n
        z = np.zeros((2*d,2*d))
        for x in range(n):
            angle = -h*x
            rotation = np.cos(angle)*np.eye(2)+np.sin(angle)*j
            for cin,cout in product(range(2),repeat=2):
                to = (x+(1 if cout==0 else -1)) % n
                row, col = 2*(2*to+cout), 2*(2*x+cin)
                sign = -1 if cin==cout==1 else 1
                z[row:row+2,col:col+2] = sign*rotation/np.sqrt(2)
        def edge(out, start):
            return z[2*out:2*out+2,2*start:2*start+2]
        e00, e1r = 0, 2
        e0l, eneg = 1, 2*(n-1)+1
        # The diamond RLR / LRR from (0,R) to (1,R).
        p = edge(e1r,e0l) @ edge(e0l,e1r) @ edge(e1r,e00)
        back_r = 0
        q = edge(e1r,back_r) @ edge(back_r,eneg) @ edge(eneg,e00)
        loop = 8*q.T @ p
        orientation = (loop-loop.T)/(-2*np.sin(2*h))
        rows.append(dict(M=m,base_dimension=d,complex_dimension_of_matrices=d*d,
                         real_dimension_of_algebra=2*d*d,
                         orthogonal_error=float(np.max(np.abs(z.T @ z-np.eye(2*d)))),
                         loop_error=float(np.max(np.abs(orientation-j))),
                         complex_commutator=float(np.max(np.abs(z@np.kron(np.eye(d),j)-np.kron(np.eye(d),j)@z)))))
    return rows


def composite_controls():
    j=np.array([[0,-1],[1,0]],int)
    eye=np.eye(2,dtype=int)
    a,b,c = (np.kron(np.kron(j,eye),eye),np.kron(np.kron(eye,j),eye),np.kron(np.kron(eye,eye),j))
    # j embedded at each vertex; -j_i*j_j distinguishes aligned signs.
    h = [-a@b,-b@c,-c@a]
    rows=[]
    for signs in product((1,-1),repeat=3):
        scaled = np.eye(8,dtype=int)
        for sign,operator in zip(signs,h):
            scaled=scaled@(np.eye(8,dtype=int)+sign*operator)
        assert np.array_equal(scaled@scaled,8*scaled)
        rows.append(dict(edge_signs=signs,rank=int(np.trace(scaled)//8),
                         balanced=np.prod(signs).item()==1))
    return rows


def classification_controls():
    # Exact distribution of the sufficient count, in log arithmetic (no sampling).
    rows = []
    for m in (3, 5, 7, 15, 31, 63, 127):
        classes = (m-1)//2 + 1
        angles = np.pi*np.arange(classes)/m
        k = math.ceil(math.log((classes-1)/ETA)/(-math.log(np.cos(np.pi/m))))
        counts = np.arange(k+1)
        log_binom = np.array([math.lgamma(k+1)-math.lgamma(l+1)-math.lgamma(k-l+1) for l in counts])
        log_likelihood = np.full((classes, k+1), -np.inf)
        log_likelihood[0,0] = 0
        for i,t in enumerate(angles[1:],1):
            log_likelihood[i] = 2*counts*np.log(np.sin(t))+2*(k-counts)*np.log(np.cos(t))
        labels = np.argmax(log_likelihood,axis=0)
        accept = labels==1
        accept_per_class = []
        errors = []
        for i,likelihood in enumerate(log_likelihood):
            probs = np.exp(likelihood+log_binom)
            accept_per_class.append(float(probs[accept].sum()))
            errors.append(float(probs[labels!=i].sum()))
        prior = np.full(classes,2/m)
        prior[0]=1/m
        accepted = np.asarray(accept_per_class) @ prior
        rows.append(dict(M=m,k=k,error_by_class=errors,accept_by_class=accept_per_class,
                         union_bound=(classes-1)*np.cos(np.pi/m)**k,
                         approval_probability=float(accepted),
                         target_fraction_on_approval=float(accept_per_class[1]*prior[1]/accepted),
                         normalization_residual=float(np.max(np.abs(np.exp(log_likelihood+log_binom).sum(axis=1)-1)))))
    return rows


def synchronized_walk_controls():
    rows=[]
    for m in (3,5,7,15):
        h=np.pi*(m-1)/m
        n=4*m
        psi=np.zeros((n,n,2,2),complex)
        psi[0,0,0,0]=1
        sites=np.arange(n)
        for _ in range(3):
            psi *= np.exp(-1j*h*(sites[:,None]+sites[None,:]))[:,:,None,None]
            a=psi.copy()
            for i,j in product(range(2),repeat=2):
                mixed=sum((-1)**(i*u+j*v)*a[:,:,u,v]/2 for u,v in product(range(2),repeat=2))
                psi[:,:,i,j]=np.roll(mixed,(1-2*i,1-2*j),axis=(0,1))
        full=float(abs(psi[1,1,0,0])**2)
        # Diagonal lift of the very same update, with the SAME single sheet.
        real=np.zeros((n,n,m,2,2))
        real[0,0,:,0,0]=np.sqrt(2/m)*np.cos(h*np.arange(m))
        for _ in range(3):
            incoming=np.empty_like(real)
            for x,y in product(range(n), repeat=2):
                incoming[x,y]=np.roll(real[x,y],x+y,axis=0)
            for i,j in product(range(2),repeat=2):
                coin=sum((-1)**(i*u+j*v)*incoming[:,:,:,u,v]/2 for u,v in product(range(2),repeat=2))
                real[:,:,:,i,j]=np.roll(coin,(1-2*i,1-2*j),axis=(0,1))
        observed=float(np.sum(real[1,1,:,0,0]**2))
        rows.append(dict(M=m,measured=observed,complex_product=full,
                         factorized=((1+np.cos(2*h))/4)**2,full_norm=float(np.linalg.norm(real))))
    return rows



def shared_interaction_controls():
    rows=[]
    for m in (3,5,7,15,31,63):
        n=2*m
        r=(m-1)//2
        h=2*np.pi*r/m
        positions=np.array([0,2])
        # A one-step incoming coin maps to outgoing R at each site.
        coin_r=np.ones(2)/np.sqrt(2)
        sector=np.sqrt(2/m)*np.cos(h*np.arange(m))
        for coupling in (0,1,m):
            output=np.zeros((2,2,m,2,2))
            for a,x in enumerate(positions):
                for b,y in enumerate(positions):
                    offset=x+y+coupling*int(x==y)
                    incoming=np.roll(sector,offset)[:,None,None]*np.outer(coin_r,coin_r)[None,:,:]/2
                    for i,j in product(range(2),repeat=2):
                        output[a,b,:,i,j]=sum((-1)**(i*u+j*v)*incoming[:,u,v]/2
                                              for u,v in product(range(2),repeat=2))
            # The four survivors end at (x+1,y+1), R,R. Decode the real plane.
            coords=np.stack([sector,np.sqrt(2/m)*np.sin(h*np.arange(m))])
            coefficients=np.einsum("sy,aby->abs",coords,output[:,:,:,0,0])
            amplitude=coefficients[:,:,0]-1j*coefficients[:,:,1]
            determinant=abs(np.linalg.det(amplitude))
            purity=float(np.trace(np.linalg.matrix_power(amplitude@amplitude.conj().T,2)).real)
            contact_angle=coupling*h
            rows.append(dict(M=m,coupling=coupling,ring=n,determinant=float(determinant),
                             predicted_determinant=float(abs(np.sin(contact_angle))/2),
                             reduced_purity=purity,expected_purity=float(1-0.5*np.sin(contact_angle)**2),
                             off_channel_norm=float(np.linalg.norm(output[:,:,:,1,:])+np.linalg.norm(output[:,:,:,0,1])),
                             conditional_target="complex bipartite pure state under the shared-plane identification"))
    return rows



def parity_controls():
    rows = []
    n, m = 10, 5
    h=np.pi*(m-1)/m
    field=np.exp(-1j*h*np.arange(n))
    plus=np.zeros((n,2),complex)
    plus[0,0]=plus[1,0]=1/np.sqrt(2)
    minus=plus.copy()
    minus[1,0]*=-1
    probe=plus.copy()
    overlap_contrast=float(abs(np.vdot(probe,plus))**2-abs(np.vdot(probe,minus))**2)
    step=np.column_stack([ring_step(e.reshape(n,2),field).ravel() for e in np.eye(2*n)])
    scores=[]
    for t in range(21):
        if t:
            plus=ring_step(plus,field)
            minus=ring_step(minus,field)
        read=np.max(np.abs(np.abs(plus)**2-np.abs(minus)**2))
        q=np.linalg.matrix_power(step,t)
        for amplitudes in q:
            effect=np.outer(amplitudes.conj(),amplitudes)
            scores.append(np.r_[effect.real.ravel(),effect.imag.ravel()])
        rank=None
        if t in (0,1,3,10,20):
            values=np.linalg.svd(np.stack(scores),compute_uv=False)
            rank=int(np.count_nonzero(values>1e-9))
        contrast=overlap_contrast if t==0 else None
        rows.append(dict(time=t,site_record_error=float(read),effect_rank=rank,
                         real_embedding_rank_cutoff=1e-9,complex_dimension=2*n,
                         contrast_in_cross_parity_projector_at_preparation=contrast))
    return rows



def main(out):
    out.mkdir(parents=True,exist_ok=True)
    rows=record_controls()
    preparations,trajectory=preparation_controls()
    orientations=orientation_tests()
    algebras=algebra_controls()
    composites=composite_controls()
    classifiers=classification_controls()
    shared_sheet=synchronized_walk_controls()
    interaction=shared_interaction_controls()
    parity=parity_controls()
    tests = {
        "all_three_step_blocks":max(r["amplitude_error"] for r in rows)<1e-12,
        "three_class_law":max(max(r["law_error"],r["norm_error"]) for r in rows)<1e-12,
        "posterior_propagation":max(x[4] for x in trajectory)<1e-11,
        "branch_probability":max(x[5] for x in trajectory)<2e-8,
        "prepared_pair":all(r["posterior_mass"]>=1-ETA for r in preparations),
        "identification_bound":all(r["conditional_classification_error_bound"]<=ETA+1e-14 for r in preparations),
        "real_and_referenced_phase":all(x["error"]<1e-12 for x in orientations),
        "real_and_complex_matrix_blocks":max(max(x[k] for k in ("orthogonal_error","loop_error","complex_commutator")) for x in algebras)<1e-12,
        "triangle_synchronization":all(x["rank"]==(2 if x["balanced"] else 0) for x in composites),
        "classifier_full_sampling_law":all(max(x["error_by_class"])<=x["union_bound"]+1e-10
                                          and x["normalization_residual"]<1e-8 for x in classifiers),
        "one_shared_sheet_product":all(max(abs(x["measured"]-x[k]) for k in ("complex_product","factorized"))<1e-12
                                       and abs(x["full_norm"]-1)<1e-12 for x in shared_sheet),
        "collision_interaction":all(abs(x["determinant"]-x["predicted_determinant"])<1e-12
                                    and abs(x["reduced_purity"]-x["expected_purity"])<1e-12
                                    and x["off_channel_norm"]<1e-12 for x in interaction),
        "parity_invisible_to_full_records":all(row["site_record_error"]<1e-12 for row in parity)
                                            and abs(parity[0]["contrast_in_cross_parity_projector_at_preparation"]-1)<1e-12,
    }
    with (out/"record_branch_trials.csv").open("w",newline="",encoding="utf8") as f:
        w=csv.writer(f)
        w.writerow(("M","constructive_records_after_first","target_mass","log10_joint_probability",
                    "fourier_mass_residual","natural_log_probability_residual"))
        w.writerows(trajectory)
    report=dict(checks=tests, record_law=rows,preparation=preparations,
                orientation=orientations,algebra=algebras,triangles=composites,
                classifiers=classifiers,shared_sheet=shared_sheet,interaction=interaction,parity=parity)
    (out/"record_selection.json").write_text(json.dumps(report,indent=1,allow_nan=False)+"\n",encoding="utf8")
    print(tests, "branch rows",len(trajectory))
    if not all(tests.values()):
        raise SystemExit(1)


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("output",type=Path)
    main(parser.parse_args().output)

