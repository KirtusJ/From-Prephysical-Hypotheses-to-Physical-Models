"""Run python -B check_occupation_envelope.py OUTPUT_DIRECTORY (NumPy required)."""
import argparse
import json
import math
from itertools import combinations
from pathlib import Path

import numpy as np


CA, SA, CB, SB = 3/5, 4/5, 4/5, 3/5
KAPPA = 12/7
GAMMA = math.atan2(7,24)
LENGTH = 16.


def stencil(field,twist=1):
    a,b = field[:,0],field[:,1]
    c,d = CA*a-1j*SA*b, CA*b-1j*SA*a
    left,right = np.roll(d,1),np.roll(c,-1)
    left[0] *= twist
    right[-1] *= twist
    return np.column_stack((CB*c+1j*SB*left,CB*d+1j*SB*right))


def spectrum(n,anti):
    k = 2*np.pi*np.fft.fftfreq(n) + (np.pi/n if anti else 0.)
    k = (k+np.pi)%(2*np.pi)-np.pi
    z = np.exp(-1j*k)
    U = np.zeros((n,2,2),complex)
    U[:,0,0] = CA*CB+SA*SB*z
    U[:,1,1] = U[:,0,0].conjugate()
    U[:,0,1] = -1j*SA*CB+1j*CA*SB*z
    U[:,1,0] = -U[:,0,1].conjugate()
    omega = np.arccos((12/25)*(1+np.cos(k)))
    # Project the real band-center +X launch onto the e^{-i omega} band.
    pole = np.full((n,2),1/math.sqrt(2))
    u = (np.exp(1j*omega)[:,None]*pole-np.einsum('nij,nj->ni',U,pole))/(2j*np.sin(omega)[:,None])
    u /= np.linalg.norm(u,axis=1)[:,None]
    assert np.max(abs(np.einsum('nij,nj->ni',U,u)-np.exp(-1j*omega)[:,None]*u))<2e-14
    return k,U,omega,u


def fourier(x,anti,reverse=False):
    phase = np.exp(1j*np.pi*np.arange(len(x))/len(x)) if anti else np.ones(len(x))
    phase = phase.reshape((-1,)+(1,)*(x.ndim-1))
    if reverse:
        return phase*np.fft.ifft(x,axis=0,norm='ortho')
    return np.fft.fft(x*phase.conjugate(),axis=0,norm='ortho')


def wedge(v,w):
    return np.array([v[i]*w[j]-v[j]*w[i] for i,j in combinations(range(len(v)),2)])


def sector_gate(amps,coords,by_pair,i,j,c,s):
    # Direct occupation lift: local 00 & 11 are stationary, 10/01 mix.
    out = np.zeros_like(amps)
    for val,xy in zip(amps,coords):
        first,second = i in xy,j in xy
        if first==second:
            out[by_pair[xy]] += val
        else:
            new = tuple(sorted((set(xy)-{i,j})|({j} if first else {i})))
            out[by_pair[xy]] += c*val
            out[by_pair[new]] += 1j*s*val
    return out


def direct_controls():
    n = 8
    coords = list(combinations(range(2*n),2))
    by_pair = {p:i for i,p in enumerate(coords)}
    rows = []
    for ini in ((0,3),(0,1),(2,9),(0,2*n-1)):
        occ = np.zeros(len(coords),complex)
        occ[by_pair[ini]] = 1
        beams = np.eye(2*n,dtype=complex)[list(ini)].reshape(2,n,2)
        naive = beams.copy()
        for s in range(1,5):
            for j in range(n):
                occ = sector_gate(occ,coords,by_pair,2*j,2*j+1,CA,-SA)
            for j in range(n):
                occ = sector_gate(occ,coords,by_pair,2*j+1,(2*j+2)%(2*n),CB,SB)
            beams = np.array([stencil(x,-1) for x in beams])
            naive = np.array([stencil(x,1) for x in naive])
            twisted,ordinary = (wedge(*q.reshape(2,-1)) for q in (beams,naive))
            assert np.linalg.norm(occ-twisted)<2e-14 and abs(np.linalg.norm(occ)-1)<2e-14
            rows.append(dict(initial=list(ini),ticks=s,correct_sector_norm_error=float(np.linalg.norm(occ-twisted)),
                             untwisted_norm_error=float(np.linalg.norm(occ-ordinary)),
                             untwisted_sharp_TV=float(np.sum(abs(abs(occ)**2-abs(ordinary)**2))/2)))
    assert max(r['untwisted_norm_error'] for r in rows)>1
    fft = []
    f = np.arange(2*n).reshape(n,2)+1j*np.arange(2*n)[::-1].reshape(n,2)
    f = f/np.linalg.norm(f)
    for anti in (False,True):
        _,u,_,_ = spectrum(n,anti)
        ref = fourier(np.einsum('nij,nj->ni',u,fourier(f,anti)),anti,True)
        err = float(np.linalg.norm(stencil(f,-1 if anti else 1)-ref))
        assert err<2e-14
        fft.append(dict(antiperiodic=anti,one_step_error=err))
    return dict(ring_cells=n,sector_rows=rows,direct_stencil_vs_bloch=fft)


def analytic(x,a,eps,x0,p0,t):
    width = np.sqrt(eps)
    spread = 1+1j*t
    envelope = np.exp(-(x-x0-p0*t)**2/(2*width**2*spread))/np.sqrt(spread)
    phase = np.exp(1j*(p0*(x-x0)-p0*p0*t/2)/eps)
    return np.sqrt(a)*(np.pi*eps)**(-.25)*envelope*phase


def detnorm(v,w):
    return float(np.vdot(v,v).real*np.vdot(w,w).real-abs(np.vdot(v,w))**2)


def wedge_error(pair,comparison):
    v,w = pair
    x,y = comparison
    cross = np.vdot(v,x)*np.vdot(w,y)-np.vdot(v,y)*np.vdot(w,x)
    cross /= math.sqrt(detnorm(v,w)*detnorm(x,y))
    return math.sqrt(max(0.,2*(1-cross.real)))


def joint(pair,x,half_window,length):
    v,w = pair
    mass = detnorm(v,w)
    # The two rays may occupy different sublattices of the same physical cell.
    vr = np.sum(abs(v)**2,axis=1)
    wr = np.sum(abs(w)**2,axis=1)
    cr = np.sum(v.conjugate()*w,axis=1)
    same = np.sum(vr*wr-abs(cr)**2)/mass
    labels = np.floor((x+length/2)*2).astype(int)
    bins = int(length*2)
    av,bv,cv = (np.array([np.sum(arr[labels==i]) for i in range(bins)]) for arr in (vr,wr,cr))
    rows = []
    total = 0.
    for i,j in combinations(range(bins),2):
        q = (av[i]*bv[j]+av[j]*bv[i]-2*(cv[i]*cv[j].conjugate()).real)/mass
        rows.append(float(q))
        total += q
    for i in range(bins):
        q = (av[i]*bv[i]-abs(cv[i])**2)/mass
        rows.append(float(q))
        total += q
    assert abs(total-1)<2e-12 and min(rows)>-1e-14 and -1e-14<same<1
    # At the crossing the two target intervals coincide, permitting both in it.
    left,right = half_window
    masks = [abs(x-c)<.5 for c in (left,right)]
    a,b = masks
    if left==right:
        inside = (sum(vr[a])*sum(wr[a])-abs(sum(cr[a]))**2)/mass
    else:
        assert not np.any(a&b)
        inside = (sum(vr[a])*sum(wr[b])+sum(vr[b])*sum(wr[a])-2*(sum(cr[a])*sum(cr[b]).conjugate()).real)/mass
    return np.array(rows),float(same),float(inside)


def regional_real_lifts(v,w,labels,bins):
    """Evaluate an unordered pair in each bin, all amplitudes in the real bond gauge."""
    def sums(values):
        return np.array([values[labels==i].sum() for i in range(bins)])
    def grouped(y,z,conjugate):
        u = y.conjugate() if conjugate else y
        return sums(np.sum(u*z,axis=1))
    def antisym(A,B,C,D):
        full = A[:,None]*B+B[:,None]*A-C[:,None]*D-D[:,None]*C
        full[np.diag_indices(bins)] *= .5
        i,j = np.triu_indices(bins)
        return full[i,j]
    def hermitian(y,z):
        cross = grouped(y,z,True)
        return antisym(grouped(y,y,True),grouped(z,z,True),cross,cross.conjugate()).real
    original = hermitian(v,w)
    # Restricted bilinear (no conjugation) products give the cross term
    # between the positive band Slater and its conjugate after a position read.
    vv,ww,vw = grouped(v,v,False),grouped(w,w,False),grouped(v,w,False)
    bilinear = antisym(vv,ww,vw,vw)
    aligned = original+bilinear.real             # norms of sqrt(2) Re(v wedge w)
    independent = hermitian(np.sqrt(2)*v.real,np.sqrt(2)*w.real)
    masses = [float(row.sum()) for row in (original,aligned,independent)]
    assert min(masses)>.01 and min(min(row) for row in (original,aligned,independent))>-2e-13
    return [row/m for row,m in zip((original,aligned,independent),masses)],masses


def real_lift_reads(orb,steps,x,length,target,fine):
    v,w = [v*np.array([1,-1j])*np.exp(-1j*steps*GAMMA) for v in orb]
    labels = np.floor((x+length/2)*2).astype(int)
    (p,a,b),mass = regional_real_lifts(v,w,labels,int(length*2))
    sep = np.array([int(1 if abs(q-target[0])<.5 else
                        2 if abs(q-target[1])<.5 else 0) for q in x])
    packet_windows,_ = regional_real_lifts(v,w,sep,3)
    i,j = np.triu_indices(3)
    accepted = (i==1)&(j==(1 if target[0]==target[1] else 2))
    # Contact determinant at the two scalar modes of a SINGLE cell.
    cross = v[:,0]*w[:,1]-v[:,1]*w[:,0]
    ir = 2*(v[:,0].real*w[:,1].real-v[:,1].real*w[:,0].real)
    same = [float(np.sum(abs(cross)**2)/mass[0]),float(2*np.sum(cross.real**2)/mass[1]),
            float(np.sum(ir**2)/mass[2])]
    info = dict(unresolved_cell_preparation_order=['positive_band','aligned_real','independent_real'],
                raw_squares_before_normalization=mass,occupancy_same_cell=same,
                accepted_ray_windows=[float(row[accepted].sum()) for row in packet_windows],
                coarse_TV_aligned_vs_complex=float(np.sum(abs(p-a))/2),
                coarse_TV_independent_vs_aligned=float(np.sum(abs(b-a))/2))
    if fine:
        # Equal individual cells in the collision core and two tail bins.
        radius = .25
        inside = np.where((x>=-radius)&(x<radius))[0]
        bins = len(inside)+2
        labels = np.where(x<-radius,0,bins-1)
        labels[inside] = np.arange(1,bins-1)
        vals,_ = regional_real_lifts(v,w,labels,bins)
        i,j = np.triu_indices(bins)
        info['contact_resolution']=dict(interior_cell_count=int(len(inside)),interval=[-radius,radius],
            includes_two_exterior_bins=True,all_unordered_bin_count=len(i),
            TV_aligned_vs_complex=float(np.sum(abs(vals[0]-vals[1]))/2),
            TV_independent_vs_aligned=float(np.sum(abs(vals[2]-vals[1]))/2),
            first_six_separation_masses=[[float(row[(i>0)&(j<bins-1)&(j-i==d)].sum())
                                        for d in range(6)] for row in vals],
            all_inside_mass=[float(row[(i>0)&(j<bins-1)].sum()) for row in vals])
    return info


def real_stencil(f,twist):
    a,b = f[:,0],f[:,1]
    c,d = CA*a+SA*b,-SA*a+CA*b
    l,r = np.roll(d,1),np.roll(c,-1)
    l[0] *= twist
    r[-1] *= twist
    return np.column_stack((CB*c-SB*l,CB*d+SB*r))


def independent_real_read_controls():
    spin = np.array([1,-1j])/np.sqrt(2)
    z = np.array([1,1])[:,None]*spin/np.sqrt(2)
    q = np.array([1j,-1j])[:,None]*spin/np.sqrt(2)
    cells,_ = regional_real_lifts(z,q,np.arange(2),2)
    assert np.allclose(cells,[[0,1,0],[0,1,0],[.25,.5,.25]],atol=2e-15)
    n = 8
    k,_,omega,u = spectrum(n,True)
    modes = [np.exp(-1j*k*j)*(1+.1*np.sin(k*j)) for j in (1,4)]
    spin_gauge = np.array([1,-1j])
    primed = [fourier(s[:,None]*u,True,True)*spin_gauge/np.linalg.norm(s) for s in modes]
    real_input = [np.sqrt(2)*s.real for s in primed]
    labels = np.arange(n)
    sites = list(combinations(range(2*n),2))
    rows = []
    for ticks in range(5):
        (pos,ali,ind),_ = regional_real_lifts(*primed,labels,n)
        full = wedge(*(s.ravel() for s in primed))
        direct = [abs(full)**2,2*full.real**2,wedge(*(s.ravel() for s in real_input))**2]
        deltas = []
        for literal,derived in zip(direct,(pos,ali,ind)):
            bins = np.zeros((n,n))
            for (i,j),v in zip(sites,literal):
                bins[i//2,j//2] += v
            deltas.append(float(np.max(abs(bins[np.triu_indices(n)]/bins.sum()-derived))))
        assert max(deltas)<2e-14
        assert max(np.linalg.norm(np.sqrt(2)*v.real-w) for v,w in zip(primed,real_input))<2e-14
        ref = [stencil(v*spin_gauge.conjugate(),-1)*spin_gauge for v in primed]
        real_input = [real_stencil(v,-1) for v in real_input]
        primed = [real_stencil(v,-1) for v in primed]
        assert max(np.linalg.norm(v-w) for v,w in zip(primed,ref))<2e-14
        rows.append(dict(tick=ticks,max_sharp_cell_errors=deltas))
    return dict(frozen_two_cell_bins_order=['00','01','11'],
                positive_and_aligned_exact=['0','1','0'],independent_exact=['1/4','1/2','1/4'],
                explicit_mode_determinants_and_gauged_stencil=rows)


def case(eps,a,length=LENGTH):
    n = round(length/a)
    tau = KAPPA*a*a/eps  # m=1
    x = (np.arange(n)-n//2)*a
    k,U,omega,spin = spectrum(n,True)
    launches = [(-1.,1.),(1.,-1.)]
    wave = [analytic(x,a,eps,q,p,0.) for q,p in launches]
    wave = [v/np.linalg.norm(v) for v in wave]
    modes = [fourier(w,True) for w in wave]
    base_vec = np.array([1.,1.])/math.sqrt(2)
    mis = [float(np.linalg.norm(v[:,None]*(spin-base_vec))) for v in modes]
    overlap = abs(np.vdot(wave[0],wave[1]))
    fields = []
    for multiple in (0,1,2):
        steps = round(multiple/tau)
        t = steps*tau
        # The center-phase e^{i steps gamma} is included before norm comparison.
        phase = np.exp(-1j*steps*(omega-GAMMA))
        orb = [fourier(v[:,None]*spin*phase[:,None],True,True) for v in modes]
        theory = [analytic(x,a,eps,q,p,t)[:,None]*base_vec for q,p in launches]
        ref = [v/np.linalg.norm(v) for v in theory]
        centers = sorted(q+p*t for q,p in launches)
        # Equal-window test at the nominal encounter; O(tau) offset is recorded.
        target = [0.,0.] if multiple==1 else centers
        vals,same,inside = joint(orb,x,target,length)
        raw,ref_same,ref_in = joint(ref,x,target,length)
        coarse_tv = float(np.sum(abs(vals-raw))/2)
        e2 = wedge_error(orb,ref)
        assert coarse_tv<=e2+2e-7
        boundary = [float(np.sum(abs(v[abs(x)>=length/2-1])**2)) for v in orb]
        images = []
        image_tail_bounds = []
        for q,p in launches:
            periodized = sum((-1)**j * analytic(x+j*length,a,eps,q,p,t)
                             for j in range(-2,3))
            images.append(float(np.linalg.norm(periodized-analytic(x,a,eps,q,p,t))))
            # Uniform bound over the interval; two tails, using successive
            # Gaussian image ratios starting at the third shell.
            d = 2.5*length-abs(q+p*t)
            denom = 2*eps*(1+t*t)
            ratio = np.exp(-(2*d*length+length**2)/denom)
            peak = (np.pi*eps)**(-.25)/(1+t*t)**.25
            image_tail_bounds.append(float(2*np.sqrt(length)*peak*np.exp(-d*d/denom)/(1-ratio)))
        quad = np.exp(-1j*steps*KAPPA*k*k/2)
        pe = [float(np.linalg.norm(v*(phase-quad))) for v in modes]
        lifts = real_lift_reads(orb,steps,x,length,target,
                                fine=eps==.125 and length==LENGTH and multiple==1)
        assert abs(lifts['accepted_ray_windows'][0]-inside)<5e-13
        fields.append(dict(nominal_time=multiple,microperiods=steps,measured_time=t,
                           sorted_free_centers=centers,cell_orbital_norms=[float(np.linalg.norm(v)) for v in orb],
                           scalar_analytic_sample_norms=[float(np.linalg.norm(v)) for v in theory],
                           demodulated_orbital_norm_errors=[float(np.linalg.norm(u-v)) for u,v in zip(orb,ref)],
                           lattice_vs_quadratic_phase_error=pe,slater_norm_error=e2,coarse_position_TV=coarse_tv,
                           same_cell_probability=same,reference_same_cell_probability=ref_same,
                           probability_in_half_unit_ray_windows=inside,reference_in_window=ref_in,
                           boundary_strip_single_particle_masses=boundary,real_preparations=lifts,
                           norm_of_first_two_alternating_image_pairs=images,
                           norm_bound_remaining_images_binary64=image_tail_bounds,
                           joint_coarse_probabilities=vals.tolist(),analytic_joint_coarse_probabilities=raw.tolist()))
    return dict(eps=eps,cell_pitch=a,period=tau,torus_cells=n,circumference=length,
                maximum_dependency_cells_per_period=1,
                physical_cell_cone_speed=a/tau,single_band_source_edge_spinor_errors=mis,
                input_orbital_overlap=float(overlap),quadratic_remainder_scale=a*a/eps**3,reads=fields)


def main(directory):
    direct = direct_controls()
    runs = [case(eps,a) for eps,a in ((.25,.125),(.25,.0625),(.25,.03125),(.25,.015625),
                                       (.125,.125**2/2),(.0625,.0625**2/2),
                                       (.03125,.03125**2/2))]
    runs.append(case(.25,.0625,4.))
    data = dict(
        units='One pitch a per cell, two scalar modes (L,R) per cell. One period is first the intra-cell layer then the neighboring R_j,L_(j+1) layer. Four one-mode-sector amplitudes use cos alpha=3/5, sin alpha=4/5, cos beta=4/5, sin beta=3/5. Vacuum and double occupation have amplitude 1. Signed complex mode gates, a shared realification if implemented on a real carrier, and the Born readout are supplied. There is no compiled microscopic implementation in this checker.',
        free_fermion_identity='The adjacent 00, one-mode s, 11 gates with double phase det(s)=1 are the exterior-power lift in the spatially ordered scalar-mode occupation basis on the line. Periodic local occupation closure on the two-particle sector needs a minus sign in the boundary one-particle hopping used in its exterior power. The direct finite-ring controls show the error from ignoring this sign.',
        continuum='cos omega=(12/25)(1+cos k), gamma=atan2(7,24), kappa=omega_second(0)=12/7. On the negative-exponent branch the carrier-removed eigenvalue is exp(-i(omega-gamma)); near zero omega-gamma=kappa*k^2/2+O(k^4). For mass one, tau=kappa*a^2/eps. At fixed physical momentum cutoff the accumulated phase error is O_T(a^2/eps^3); freezing the smooth normalized eigenvector costs O(a/eps). For the Gaussian center momenta +/-1, width O(sqrt(eps)), a=o(eps^(3/2)) suffices. Fixed-epsilon convergence recovers the free Schrodinger evolution of each orbital and hence its antisymmetric two-particle image. The ordered chamber has a Dirichlet node at microscopic coincidence. Unordered positions concentrate on the pair of free centers as eps tends to zero, including the common meeting point. Individually sorted particle labels do not represent trajectories of two tagged particles. The moving pitch/period makes the strict microscopic speed diverge for this family.',
        table='The grid is the two-particle periodic occupation sector, computed via antiperiodic Fourier modes; the comparison is the unperiodized exact line Gaussian sampled on the same centers. The first two pairs of translated alternating images and a Gaussian-series bound for all remaining images quantify finite-volume effects in the continuum reference; tiny bounds can underflow in binary64. Finite periodicity is not identical to the line. All 528 probabilities per main snapshot, or 36 for the short circumference adverse control, are present for both the walk and analytic reference. In order: first i<j lexicographic, then i=j, for physical bins of width 1/2. The two sublattices are unresolved. At nominal time 1 the test window is |x|<1/2 for both particles. At the other times both disjoint radius-1/2 center windows must be occupied.',
        real_gauge='The diagonal mode gauge (even,odd)=(1,-i) turns both bond matrices into real plane rotations. The conjugate band accompanies a real preparation. Compare the pure aligned real state proportional to Re(v wedge w) with the independent real-orbital Slater Re(v) wedge Re(w). The full e^{-i n gamma} carrier per orbital is restored before taking real parts. Conjugate sectors are globally orthogonal for the spectral preparations but may interfere under restricted coordinate projections. At constant spin (1,-i)/sqrt(2) the aligned sectors are orthogonal after summing each cell pair. Independent orbitals replace the local complex overlaps by their real parts and can alter unresolved joint contact. Independent real orbital packets still concentrate on the sorted rest-frame free rays in the semiclassical family; a Slater occupation source and coherent spatially extended packet preparation are assumed.',
        direct_controls=direct,real_preparation_controls=independent_real_read_controls(),quadratic_and_joint_rows=runs)
    directory.mkdir(parents=True,exist_ok=True)
    (directory/'occupation_envelope.json').write_bytes((json.dumps(data,separators=(',',':'))+'\n').encode())


if __name__=='__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('output',type=Path)
    main(p.parse_args().output)
