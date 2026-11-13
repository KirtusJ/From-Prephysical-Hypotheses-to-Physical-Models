"""Deterministic controls for the signed walk, finite sheet lift and weak-field bound."""
import argparse
import csv
import json
import math
from pathlib import Path

import numpy as np


def velocity(k):
    return np.cos(k) / np.sqrt(1 + np.cos(k) ** 2)


def omega(k):
    return np.arcsin(np.sin(k) / np.sqrt(2))


def positive_eigenvector(k):
    # First column of the positive-real-part spectral projector, normalized.
    c, s = np.cos(k), np.sin(k)
    r = np.sqrt(1 + c * c)
    v = np.stack([r + c, c + 1j * s], axis=-1)
    return v / np.linalg.norm(v, axis=-1, keepdims=True)


def coin(a):
    u, v = a[..., 0], a[..., 1]
    return np.stack([u + v, u - v], axis=-1) / np.sqrt(2)


def fibre_step(a, k):
    return coin(a) * np.stack([np.exp(-1j*k), np.exp(1j*k)], axis=-1)


def ring_step(a, field):
    scattered = coin(a * field[:, None])
    return np.stack([np.roll(scattered[:, 0], 1), np.roll(scattered[:, 1], -1)], axis=-1)


def lift_step(a):
    # a[x,y,spin]. The outgoing sheet is y+x before the spatial shift.
    scattered = coin(a)
    scattered = np.stack([np.roll(row, x, axis=0) for x, row in enumerate(scattered)])
    return np.stack([np.roll(scattered[..., 0], 1, axis=0),
                     np.roll(scattered[..., 1], -1, axis=0)], axis=-1)


def lift_controls():
    rows = []
    for m in (3, 4, 5, 6, 8):
        n = 2*m
        for r in range(m):
            h = 2*np.pi*r/m
            sector = np.exp(1j*h*np.arange(m)) / np.sqrt(m)
            base = np.zeros((n, 2), dtype=complex)
            base[0, 0] = 1
            full = base[:, None, :] * sector[None, :, None]
            for t in range(1, 8):
                base = ring_step(base, np.exp(-1j*h*np.arange(n)))
                full = lift_step(full)
                err = np.max(np.abs(full - base[:, None, :] * sector[None, :, None]))
                item = dict(M=m, sector=r, step=t, max_amplitude_error=float(err),
                            norm_error=float(abs(np.linalg.norm(full)-1)))
                if t == 3:
                    item.update(right_record=float(np.abs(full[1, :, 0]) @ np.abs(full[1, :, 0])),
                                formula=float((1+np.cos(2*h))/4))
                rows.append(item)
        # Unprepared sheet. Tracing y must average the whole sector family.
        base = np.zeros((n, 2), complex)
        base[0, 0] = 1
        full = np.zeros((n, m, 2), float)
        full[0, 0, 0] = 1
        for _ in range(3):
            full = lift_step(full)
        mixture = np.mean([(1+np.cos(4*np.pi*r/m))/4 for r in range(m)])
        rows.append(dict(M=m, sector="localized_sheet", step=3,
                         right_record=float(np.sum(full[1,:,0]**2)), formula=float(mixture)))
    return rows


def ray_run(m, branch, width, k0, writer):
    # Each k fibre is propagated exactly as a two-component vector. The current
    # integrates the displacement on the line; there is no ring centroid unwrap.
    grid = np.arange(-512, 512) * (np.pi / 512)
    d = (grid-k0+np.pi) % (2*np.pi) - np.pi
    weights = np.exp(-0.5*(d/width)**2)
    weights /= np.sum(weights)
    h = 2*np.pi/m
    def band(k):
        u = positive_eigenvector(k)
        if branch == 1:
            return u
        return np.stack([-np.conj(u[:,1]), np.conj(u[:,0])], axis=1)
    state = band(grid)
    disp = 0.
    max_error = 0.
    for j in range(1, m+1):
        disp += weights @ (2 * np.real(np.conj(state[:,0])*state[:,1]))
        k = grid - j*h
        state = fibre_step(state,k)
        u = band(k)
        leakage = np.abs(u[:,0]*state[:,1] - u[:,1]*state[:,0])**2
        target = branch*(weights @ (omega(grid)-omega(k)))
        point = branch*float(omega(k0)-omega(k0-j*h))
        err = abs(h*disp-target)
        max_error = max(max_error, err)
        tau = j*h
        bound = min(2*tau, (4.5*tau + 16*tau*tau)*h)
        writer.writerow((m,branch,width,k0,j,h*disp,target,point,err,bound,
                         np.max(leakage),np.max(np.abs(np.sum(np.abs(state)**2,axis=1)-1))))
        if err > bound + 2e-12:
            raise ArithmeticError((m,branch,j,err,bound))
    return dict(period=m, branch=branch, width=width, k0=k0,
                max_scaled_error=max_error, max_error_in_sites=max_error/h)


def controls():
    rows = []
    for delta in (0.5, 0.25, 0.125, 0.0625):
        q = np.linspace(-delta, delta, 257)
        t = round(1/delta**2)
        band_phase = omega(-np.pi/2 + q) + np.pi/4
        exact = np.exp(-1j*t*band_phase)
        approximate = np.exp(-1j*t*q*q/2)
        error = float(np.max(np.abs(exact-approximate)))
        rows.append(dict(bandwidth=delta, steps=t, envelope_error=error, bound=t*delta**4/6))
    # The opposite band and an unsplit superposition have different velocities.
    k = 0.
    v = positive_eigenvector(np.array([k]))[0]
    w = np.array([-np.conj(v[1]),np.conj(v[0])])
    currents = [float(2*np.real(np.conj(u[0])*u[1])) for u in (v,w)]
    return rows, currents


def holonomy_controls():
    rows = []
    for m in (3, 5, 7, 9, 15, 31, 63):
        shifts = np.roll(np.eye(m), 2, axis=0)
        eigenvalues, vectors = np.linalg.eigh(2*np.eye(m) - shifts - shifts.T)
        pair = vectors[:, 1:3]
        projector = pair @ pair.T
        r = (m-1)//2
        theta = 2*np.pi*r*np.arange(m)/m
        # Cosine kernel on the real pair for the first nonzero eigenvalue.
        expected = (2/m)*np.cos(theta[:, None]-theta[None, :])
        dipole = (np.eye(m)[:, 0]-np.eye(m)[:, 2])/np.sqrt(2)
        initial = np.zeros((2*m, 2), complex)
        initial[0] = [0.5, 0.5j]
        initial[1] = [0.5j, -0.5]
        strong, weak = initial.copy(), initial.copy()
        x = np.arange(2*m)
        # The weak comparator ring length is 2M, compatible with pi/M.
        for step in range(1, 10):
            strong = ring_step(strong,np.exp(-2j*np.pi*r*x/m))
            weak = ring_step(weak,np.exp(1j*np.pi*x/m))
            rows.append(dict(M=m,step=step,selected_r=r,
                             probability_error=float(np.max(np.abs(np.abs(strong)**2-np.abs(weak)**2))),
                             projector_error=float(np.max(np.abs(projector-expected))),
                             dipole_success=float(np.linalg.norm(pair.T @ dipole)**2),
                             predicted_success=float(4*np.sin(np.pi/m)**2/m)))
    return rows


def filter_controls():
    rows = []
    for m in (3, 5, 7, 15, 31, 63):
        r = (m-1)//2
        theta = 2*np.pi*r*np.arange(m)/m
        pair = np.sqrt(2/m)*np.stack([np.cos(theta),np.sin(theta)],axis=1)
        state = (np.eye(m)[:,0]-np.eye(m)[:,2])/np.sqrt(2)
        p = 4*np.sin(np.pi/m)**2/m
        a1 = np.cos(np.pi/m)**2
        a2 = 0. if m==3 else np.cos(2*np.pi/m)**2
        distance = 0.01
        target = 0 if m==3 else math.ceil(math.log(math.sqrt((1-p)/p)/distance)
                                              / math.log(a1/a2))
        for step in range(target+1):
            probability = float(state @ state)
            coordinates = pair.T @ state
            err = float(np.linalg.norm(state-pair @ coordinates) / np.sqrt(probability))
            bound = math.sqrt(max(0,1-p)/p)*(a2/a1)**step
            lower = p*a1**(2*step)
            rows.append(dict(M=m,round=step,cutoff=target,leakage_amplitude=err,
                             bound=bound,success=probability,lower_success=lower))
            state = (2*state + np.roll(state,2) + np.roll(state,-2))/4
    return rows



def main(directory):
    directory.mkdir(parents=True, exist_ok=True)
    lifts = lift_controls()
    envelopes, currents = controls()
    holonomies = holonomy_controls()
    filters = filter_controls()
    with (directory/"filter_trials.csv").open("w",newline="",encoding="utf8") as f:
        writer = csv.DictWriter(f,fieldnames=list(filters[0]))
        writer.writeheader()
        writer.writerows(filters)
    with (directory/"ray_trials.csv").open("w", newline="", encoding="utf8") as f:
        writer = csv.writer(f)
        writer.writerow(("period","branch","width","k0","step","scaled_displacement",
                         "averaged_ray","central_ray","scaled_error","analytic_bound",
                         "max_fibre_leakage_probability","max_norm_error"))
        rays = [ray_run(m, sign, width, k, writer)
                for m in (32,64,128,256,512) for sign,k in ((1,1.),(-1,-0.8))
                for width in (0.03,0.15)]
    predicates = {
        "lift_all_steps":all(r.get("max_amplitude_error",0)<1e-12 for r in lifts),
        "three_step_record_and_mixture":all(abs(r["right_record"]-r["formula"])<1e-12
                                             for r in lifts if "right_record" in r),
        "lift_norm":all(r.get("norm_error",0)<1e-12 for r in lifts),
        "free_envelope_bound":all(r["envelope_error"] <= r["bound"]+1e-12 for r in envelopes),
        "opposite_sign_velocities":np.allclose(currents,[1/np.sqrt(2),-1/np.sqrt(2)]),
        "all_ray_steps_within_bound":True,
        "odd_cover_holonomy_modes":all(r["projector_error"]<1e-11 for r in holonomies),
        "parity_field_alias":all(r["probability_error"]<1e-12 for r in holonomies),
        "dipole_cost":all(abs(r["dipole_success"]-r["predicted_success"])<1e-12 for r in holonomies),
        "filter_certificate":all(r["leakage_amplitude"] <= r["bound"]+1e-10 and
                                 r["success"] >= r["lower_success"]-1e-12 for r in filters),
        "filter_target":all(r["leakage_amplitude"] <= 0.01+1e-12 for r in filters
                            if r["round"]==r["cutoff"]),
    }
    report = dict(precision="binary64; numerical quadrature; bounds in the accompanying proof",
                  predicates=predicates, lift_trials=lifts, free_envelope=envelopes,
                  opposite_band_currents=currents, ray_summary=rays, holonomy_trials=holonomies)
    (directory/"checks.json").write_text(json.dumps(report,indent=1,allow_nan=False)+"\n",encoding="utf8")
    print(predicates, len(lifts), len(rays), "ray trajectories")
    if not all(predicates.values()):
        raise SystemExit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("directory",type=Path)
    main(parser.parse_args().directory)

