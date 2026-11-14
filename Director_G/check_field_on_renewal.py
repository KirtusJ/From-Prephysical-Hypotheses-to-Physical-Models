"""Field-on direction blocks, active-site renewal, and unpolarized Gaussian flight.

Run python -B check_field_on_renewal.py OUTDIR with NumPy. Output must be new.
The same character is kept on all retries. No return or holding ticks are used.
"""
import argparse
from collections import defaultdict
import json
import math
from pathlib import Path

import numpy as np


def require(ok, message):
    if not ok:
        raise ValueError(message)


def direct(m, charge, blocks, home, rail):
    """Apply the signed Hadamard and actual staircase at each visited ring site."""
    size = 4*m
    x = np.arange(size)
    kick = np.exp(-2j*np.pi*((charge*(x//2)) % m)/m)/math.sqrt(2)
    r = np.zeros(size, dtype=complex)
    l = r.copy()
    (r if rail == 1 else l)[home] = 1
    rows = []
    for j in range(1, blocks+1):
        for _ in range(2):
            r,l = np.roll((r+l)*kick,1), np.roll((r-l)*kick,-1)
        newrail = rail*(-1)**j
        keep, reject = (r,l) if newrail == 1 else (l,r)
        rows.append((keep.copy(), abs(reject)**2))
        reject.fill(0)
    return rows


def product_prefixes(m, charge, blocks):
    # q is the final momentum. In a j-block survival product its offsets are
    # h,3h,...,(2j-1)h. One new factor extends it to j+1.
    q = np.arange(4*m)*(2*np.pi/(4*m))
    h = charge*np.pi/m
    prod = np.ones(4*m)
    p = [1.0]
    for j in range(1,blocks+1):
        prod *= np.sin(q+(2*j-1)*h)
        p.append(float(np.mean(prod**2)))
    return q, prod, p


def predicted_amplitude(order, charge, j, home, rail, q, scalar):
    h = charge*np.pi/order
    displacement = -rail if j%2 else 0
    constant = -2*rail*(j//2)
    # The occupied spatial parity contributes j odd departures in 2j ticks.
    # Translation of the home takes the argument to the original input q+2jh.
    translated = np.exp(-1j*q*((home+displacement)%(4*order)))
    phase = (-1j)**j*np.exp(1j*h*(j-constant-2*j*home))
    return phase*translated*scalar


def small_oracles():
    results=[]
    for m in (3,4,5,8,11):
        for charge in (0,1,-1,m//2):
            max_wave = max_prob = max_balance = 0
            blocks = 5
            for home,rail in ((0,1),(0,-1),(1,1),(4*m-1,-1)):
                states = direct(m,charge,blocks,home,rail)
                previous = 1.0
                for j,(observed,reject) in enumerate(states,1):
                    q,scalar,p=product_prefixes(m,charge,j)
                    predicted=predicted_amplitude(m,charge,j,home,rail,q,scalar)
                    wave_error = float(np.linalg.norm(np.fft.fft(observed)-predicted)/math.sqrt(4*m))
                    max_wave=max(max_wave,wave_error)
                    max_prob=max(max_prob,abs(float(np.sum(abs(observed)**2))-p[-1]))
                    max_balance=max(max_balance,abs(previous-float(reject.sum())-p[-1]))
                    previous=p[-1]
            require(max(max_wave,max_prob,max_balance)<2e-12,"complete signed projected wave")
            results.append(dict(M=m,charge=charge,blocks=blocks,
                                max_absolute_wave_error=max_wave,max_probability_error=max_prob,
                                max_fail_plus_survival_error=max_balance))
    return results


def renewal_cdf(p, deadline):
    m = len(p)-1
    cdf = [0.0]*(deadline+1)
    for t in range(m,deadline+1):
        cdf[t] = p[-1]+sum((p[j-1]-p[j])*cdf[t-j] for j in range(1,m+1))
    return cdf


def finite_deadlines(order, charge, m, budget):
    """Branch recursion retains the ACTUAL failed site/rail and restarts there."""
    home = 4*order-1
    incoming = -1
    q,scalar,p = product_prefixes(order,charge,m)
    total = renewal_cdf(p,budget)
    active = [defaultdict(float) for _ in range(budget+1)]
    active[0][home,incoming] = 1.0
    done = np.zeros(budget+1)
    released_away = np.zeros(budget+1)
    cache = {}
    for elapsed, branches in enumerate(active):
        for (x,r),weight in branches.items():
            if (x,r) not in cache:
                cache[x,r] = direct(order,charge,m,x,r)
            for j,(passed,failed) in enumerate(cache[x,r],1):
                t=elapsed+j
                if t>budget:
                    break
                if j==m:
                    probability=float(np.sum(abs(passed)**2))*weight
                    done[t]+=probability
                    if x != home:
                        released_away[t]+=probability
                for new_x in np.flatnonzero(failed):
                    new_rail=r*(-1)**(j-1)
                    active[t][int(new_x),new_rail] += weight*float(failed[new_x])
    direct_cdf=np.cumsum(done)
    discrepancy=float(np.max(abs(direct_cdf-total)))
    require(discrepancy<2e-12,"full recorded failures versus scalar renewal")
    return dict(M=order,charge=charge,m=m,deadline_blocks=budget,prefix_survival=p,
                mean_moving_ticks=2*sum(p[:-1])/p[-1],
                single_attempt_survival=p[-1],release_cdf_native=direct_cdf.tolist(),
                release_cdf_renewal=total,timeout_at_deadline=1-total[-1],
                released_from_other_recorded_home=float(released_away.sum()),
                largest_cdf_difference=discrepancy)


def free_success(m):
    # Product avoids subtracting two log-gamma values at large m.
    return math.prod((2*j-1)/(2*j) for j in range(1,m+1))


def continuum_mean(lam, force):
    b=force**2*lam**3/3
    nodes,weights=np.polynomial.legendre.leggauss(32)
    integral=float(np.sum(weights*np.exp(-b*((nodes+1)/2)**6))/2)
    return 4*lam*math.exp(b)*integral


def scale_flight(order, charge, m, n, delta):
    size=4*order
    q,prod,p=product_prefixes(order,charge,m)
    h=charge*math.pi/order
    lam=m*delta**2
    time=n*delta**2
    force=charge
    # Fold both replica valleys and retain the measured momentum displacement.
    folded=(q+math.pi) % math.pi - math.pi/2
    weights=prod**2/np.sum(prod**2)
    pmean=float(np.sum(weights*folded)/delta)
    target_drift=-force*lam
    mean_time=2*delta**2*sum(p[:-1])/p[-1]
    predicted_time=continuum_mean(lam,force)
    survival_ratio=p[-1]/free_success(m)
    predicted_survival=math.exp(-force**2*lam**3/3)
    x=np.arange(size)
    x[x>=size//2]-=size
    stream=np.exp(-1j*q)
    # Nonzero/odd home tests are independent of the small exact word checks.
    settings=((0,1),(1,-1))
    flights=[]
    profiles=[]
    for home,rail in settings:
        source=predicted_amplitude(order,charge,m,home,rail,q,prod)
        source/=np.linalg.norm(source)
        r=source.copy() if rail==1 else np.zeros_like(source)
        l=source.copy() if rail==-1 else np.zeros_like(source)
        for _ in range(n):
            a,b=np.roll(r,-2*charge),np.roll(l,-2*charge)
            r,l=stream*(a+b)/math.sqrt(2), stream.conj()*(a-b)/math.sqrt(2)
        density=size*(abs(np.fft.ifft(r))**2+abs(np.fft.ifft(l))**2)
        # Recenter at the recorded retry home, preserving the true physical parity.
        density=np.roll(density,-home)
        profiles.append(density)
        mass=float(density.sum())
        parity_loss=float(density[(x%2)!=(n%2)].sum())
        require(abs(1-mass)<2e-10 and parity_loss<2e-12,"flight mass/parity")
        even_shift = 2 * max(1, round(0.85 / (2 * delta)))
        separation = even_shift * delta
        carrier_sign = (-1) ** (even_shift // 2)
        final_momentum = abs(r)**2 + abs(l)**2
        overlap = carrier_sign * np.sum(final_momentum * np.exp(1j * even_shift * q))
        expected_momentum = np.roll(abs(source)**2, -2 * charge * n)
        momentum_error = float(np.max(abs(final_momentum - expected_momentum)))
        require(momentum_error < 1e-10, "final momentum differs from the transported source")
        contrast_limit = math.exp(-separation**2 / (4 * lam)) * math.cos(
            force * (lam + time) * separation)
        cf=np.sum(density*np.exp(1j*delta*x))
        variance=(lam+time*time/lam)/2
        shift=force*(lam*time+time*time/2)
        reference=math.exp(-variance/2)*math.cos(shift)
        no_preparation_drift=math.exp(-variance/2)*math.cos(force*time*time/2)
        flights.append(dict(home=home,initial_rail=rail,terminal_mass=mass,parity_leak=parity_loss,
                            even_shift=even_shift,separation=separation,
                            corrected_overlap=[float(overlap.real),float(overlap.imag)],
                            limiting_real_overlap=contrast_limit,
                            real_overlap_error=abs(float(overlap.real)-contrast_limit),
                            exact_kick_max_error=momentum_error,
                            position_cf=[float(cf.real),float(cf.imag)],target_cf=reference,
                            cf_absolute_error=float(abs(cf-reference)),gaussian_centers=[-shift,shift],
                            within_ray_variance=variance,
                            incorrectly_ignored_prep_drift_cf=no_preparation_drift,
                            absolute_error_if_drift_ignored=float(abs(cf-no_preparation_drift))))
    reflection=float(np.sum(abs(profiles[0]-profiles[1][(-np.arange(size)) % size]))/2)
    require(reflection<2e-10,"mirror launch covariance")
    row=dict(M=order,charge=charge,m=m,n=n,delta=delta,lambda_actual=lam,time=time,
             survival=p[-1],free_success=free_success(m),survival_ratio=survival_ratio,
             target_ratio=predicted_survival,ratio_error=abs(survival_ratio-predicted_survival),
             mean_moving_physical_time=mean_time,time_limit=predicted_time,
             mean_time_error=abs(mean_time-predicted_time),folded_mean_p=pmean,
             predicted_p=target_drift,p_drift_error=abs(pmean-target_drift),
             differential_reflected_tv=reflection,flights=flights)
    return row,profiles[0]


def run():
    panel=[]
    comparisons=[]
    for m_order in (128,512,2048,8192):
        delta=(math.pi/m_order)**(1/3)
        m=2*round(1/(2*delta**2))
        n=round(.75/delta**2)
        positive=None
        for charge in (1,-1,0):
            row,profile=scale_flight(m_order,charge,m,n,delta)
            panel.append(row)
            if charge==1:
                positive=profile
            elif charge==-1:
                tv=float(np.sum(abs(positive-profile))/2)
                require(tv<2e-10,"conjugate position arrays")
                comparisons.append(dict(M=m_order,conjugate_tv=tv))
    deadlines=[finite_deadlines(order,s,m,10) for order in (4,7)
               for s in (0,1,-1,order//2) for m in (2,4)]
    return dict(scope="Permanent gain including failures. At first failed block, read site/rail "
                      "and start a new attempt at that recorded site and rail. Elapsed time is "
                      "two native ticks per block, excluding read/controller overhead. Large "
                      "rows are relative to the most recent sharp home, not the original home.",
                direct_wave=small_oracles(),finite_deadline=deadlines,fixed_action=panel,
                conjugation=comparisons)


if __name__ == "__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory",type=Path)
    directory=parser.parse_args().directory
    data=run()
    directory.mkdir(parents=True,exist_ok=True)
    with (directory/"field_on_renewal.json").open("x",encoding="utf8",newline="\n") as handle:
        json.dump(data,handle,separators=(",",":"),allow_nan=False)
        handle.write("\n")
