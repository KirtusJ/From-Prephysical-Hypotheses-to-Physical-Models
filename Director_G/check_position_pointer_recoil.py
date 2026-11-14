"""Reproduce finite complete pointer reads and a free-band Gaussian recoil series."""

from argparse import ArgumentParser
import json
from math import pi
from pathlib import Path

import numpy as np

from check_walk import omega, positive_eigenvector


def need(ok, message):
    if not ok:
        raise ValueError(message)


def free(field, times):
    """Exact free fibre powers on a cyclic base, using both spectral projectors."""
    k = 2 * pi * np.fft.fftfreq(len(field))
    basis = positive_eigenvector(k)
    state = np.fft.fft(field, axis=0, norm="ortho")
    plus = basis * np.sum(basis.conj() * state, axis=1)[:, None]
    minus = state - plus
    phase = np.exp(-1j * times * omega(k))
    result = plus * phase[:, None] + minus * ((-1)**times * phase.conj())[:, None]
    return np.fft.ifft(result, axis=0, norm="ortho")


def mass(state):
    return np.sum(np.abs(state)**2, axis=1)


def direct_step(state):
    return np.column_stack((np.roll(state[:, 0]+state[:, 1],1),
                            np.roll(state[:, 0]-state[:, 1],-1))) / np.sqrt(2)


def finite_pointer():
    n = 13
    x = np.arange(n)
    state = np.zeros((n, 2), dtype=complex)
    state[[0, 3, 7]] = ((1, 1j), (-2j, 3), (.5j, -1))
    state /= np.linalg.norm(state)
    for _ in range(3):
        state = direct_step(state)
    need(np.linalg.norm(free(state, 1)-direct_step(state)) < 2e-14, "rail convention")
    g = np.exp(-2 * np.sin(pi*x/n)**2) * np.exp(1j*(.31*x+.79*np.cos(2*pi*x/n)))
    g /= np.linalg.norm(g)
    rows = []
    for h in (0, 2):
        g_phase = g * np.exp(2j*pi*h*x/n)
        joint = np.array([mass(free(state*g_phase[(z-x) % n, None], 4)) for z in x])
        kicks = np.abs(np.fft.fft(g_phase, norm="ortho"))**2
        terminal = sum(weight*mass(free(state*np.exp(-2j*pi*j*x/n)[:, None], 4))
                       for j, weight in enumerate(kicks))
        position = abs(g_phase)**2
        first = np.array([np.dot(mass(state), position[(z-x) % n]) for z in x])
        residual = float(np.max(np.abs(terminal-joint.sum(axis=0))))
        need(residual < 3e-14 and np.max(np.abs(first-joint.sum(axis=1))) < 3e-14
             and abs(joint.sum()-1) < 3e-14, "both joint marginals and all outcomes")
        rows.append(dict(phase_mode=h, joint=joint.tolist(), first=first.tolist(),
                         kick_terminal=terminal.tolist(), max_terminal_residual=residual))
    first_gap = np.max(np.abs(np.array(rows[0]["first"])-rows[1]["first"]))
    terminal_tv = .5*np.sum(np.abs(np.array(rows[0]["kick_terminal"])-rows[1]["kick_terminal"]))
    need(first_gap < 3e-14 and terminal_tv > .01, "invisible pointer phase changes next read")
    return dict(wells=n, four_tick_joint_laws=rows, first_max_gap=float(first_gap),
                second_tv=float(terminal_tv))


def packet_trial(delta):
    eps = delta
    a = eps * delta
    L = round(32/a)
    k = 2*pi*np.fft.fftfreq(L)
    p = ((k+pi/2+pi) % (2*pi)-pi)/delta
    f = np.exp(-(p-.4)**2/(4*eps)) * (np.abs(p) < 2)
    spin = positive_eigenvector(k) * f[:, None]
    initial = np.fft.ifft(spin/np.linalg.norm(spin), axis=0, norm="ortho")
    x = (np.arange(L)+L//2) % L - L//2
    Y = x*a
    t1, t2 = round(.5/(eps*delta**2)), round(1/(eps*delta**2))
    elapsed = (t2-t1)*eps*delta**2
    final_time = t2*eps*delta**2
    before = free(initial, t1)
    nodes, weights = np.polynomial.hermite.hermgauss(24)
    xi = 2.
    nominal = np.exp(1j*xi*.4*final_time)
    result = []
    for setting, w, kappa in (("broad", np.sqrt(eps), 0.), ("critical", eps, 0.),
                               ("critical_phase", eps, .75)):
        total = np.zeros(L)
        for node, weight in zip(nodes, weights):
            kick = -(eps/w)*(kappa+node/np.sqrt(2))
            after = free(before*np.exp(1j*kick*Y/eps)[:, None], t2-t1)
            total += weight/np.sqrt(pi)*mass(after)
        observed = np.dot(total, np.exp(1j*xi*Y))
        ref = nominal*np.exp(-1j*xi*elapsed*eps*kappa/w-(xi*elapsed*eps/(2*w))**2/2)
        # This is a finite periodic simulation with a sawtooth coordinate choice.
        # Its tails are retained; the line theorem does not assume periodic coordinates.
        edge_mass = float(total[np.abs(Y)>15].sum())
        need(abs(total.sum()-1) < 3e-12, "all terminal weights included")
        result.append(dict(setting=setting, pointer_width=float(w), characteristic=[observed.real,observed.imag],
                           comparison=[ref.real,ref.imag], difference=float(abs(observed-ref)), edge_mass=edge_mass))
    return dict(delta=delta, epsilon=eps, sites=L, early_tick=t1, late_tick=t2, xi=xi, rows=result)


def run():
    finite = finite_pointer()
    trials = [packet_trial(1/n) for n in (4, 6, 8, 12, 16)]
    for j in range(3):
        need(trials[-1]["rows"][j]["difference"] < trials[0]["rows"][j]["difference"],
             "endpoint comparison across displayed sequence")
    return dict(finite_exact_channel_binary64=finite, free_band=trials,
                gaussian_quadrature_order=24, quadrature_standard_deviation=.5)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    path = parser.parse_args().output
    output = run()
    with path.open("x", encoding="utf-8", newline="\n") as dest:
        json.dump(output, dest, indent=2, allow_nan=False)
        dest.write("\n")
