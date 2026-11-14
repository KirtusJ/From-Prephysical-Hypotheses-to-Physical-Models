"""Replay complete pointer reads on a cycle and a two-pointer band comparison."""

from argparse import ArgumentParser
from itertools import product
import json
from pathlib import Path

import numpy as np

from check_walk import omega, positive_eigenvector


def require(condition, message):
    if not condition:
        raise ValueError(message)


def advance(state, ticks, kind):
    """Propagate a momentum-indexed field with one rail axis at the end."""
    n = state.shape[-2]
    k = 2 * np.pi * np.fft.fftfreq(n)
    if kind == "quadratic":
        # Odd n; this is the exact unit-time free shear over the finite field.
        j = np.arange(n)
        inverse_two = pow(2, -1, n)
        return state * np.exp(-2j * np.pi * (ticks*inverse_two*j*j % n)/n)[:, None]
    basis = positive_eigenvector(k)
    plus = basis * np.sum(basis.conj()*state, axis=-1, keepdims=True)
    phase = np.exp(-1j * ticks * omega(k))[:, None]
    return plus*phase + (state-plus)*((-1)**ticks*phase.conj())


def direct_read(source, pointers, kind):
    n = len(source)
    x = np.arange(n)
    out = np.zeros((n, n, n))
    def flight(state):
        return np.fft.ifft(advance(np.fft.fft(state, axis=0, norm="ortho"),
                                   1, kind), axis=0, norm="ortho")
    for a, b in product(x, repeat=2):
        # The joint input G is allowed to be entangled. The unread second
        # pointer is still a coordinate at the time of the first read.
        first = np.stack([flight(source*pointers[(a-x) % n, j, None]) for j in x])
        after_second = first[(b-x) % n, x, :]
        out[a, b] = np.sum(abs(flight(after_second))**2, axis=1)
    require(abs(out.sum()-1) < 3e-13, "original launch denominator")
    labels = (x[:, None, None] - 2*x[None, :, None] + x[None, None, :]) % n
    histogram = np.bincount(labels.ravel(), weights=out.ravel(), minlength=n)
    return histogram, out


def cycle_panels():
    n = 7
    x = np.arange(n)
    root = np.exp(2j*np.pi/n)
    i, j = np.meshgrid(x, x, indexing="ij")
    ptr = (1+.4*np.cos(2*np.pi*(i-j)/n))*root**(i*j+i+2*j)
    ptr /= np.linalg.norm(ptr)
    sources = []
    for loc, rail in [(0, 0), (2, 1)]:
        source = np.zeros((n, 2), complex)
        source[loc, rail] = 1
        sources.append(source)
    source = np.stack([root**(x*x)+.5*root**(2*x), root**(3*x)], axis=-1)
    sources.append(source/np.linalg.norm(source))
    rows = {}
    all_cells = []
    for kind in ("quadratic", "walk"):
        rows[kind] = []
        for h in (0, 1):
            histograms = []
            for source in sources:
                hist, cells = direct_read(source,ptr*root**(h*j),kind)
                histograms.append(hist)
                all_cells.append(dict(propagator=kind, middle_phase=h, source=len(histograms)-1,
                                      cells=cells.tolist()))
            rows[kind].append([a.tolist() for a in histograms])
    shear = np.array(rows["quadratic"])
    require(np.max(abs(shear[:, 1:]-shear[:, :1])) < 2e-13, "exact shear cancels source")
    require(np.max(abs(shear[1]-np.roll(shear[0],-1,axis=-1))) < 2e-13,
            "second pointer phase shifts the contrast by minus one")
    # A single coined tick is not the Newtonian low-band propagator.
    walk = np.array(rows["walk"])
    source_gap = .5 * sum(abs(walk[0,0]-walk[0,2]))
    require(source_gap > .001, "finite coined walk retains launch dependence")
    return dict(wells=n, histograms=rows, finite_walk_source_tv=float(source_gap),
                joint_records=all_cells)


def band_panel(m, p0):
    # Torus of physical circumference 2pi. Integer characters eliminate
    # interpolation at all three output coordinates and retain both bands.
    eps = 1/m
    n = round(2*np.pi*m*m/4)*4
    delta = 2*np.pi/(n*eps)
    ticks = round(1/(eps*delta**2))
    interval = ticks*eps*delta**2
    p = ((2*np.pi*np.fft.fftfreq(n)+1.5*np.pi) % (2*np.pi)-np.pi)/delta
    f = np.exp(-(p-p0)**2/(4*eps)) * (abs(p-p0)<2)
    source = f[:,None]*positive_eigenvector(2*np.pi*np.fft.fftfreq(n))
    source /= np.linalg.norm(source)
    # Discrete pointer momenta l on the torus, scaled momenta q=eps*l.
    ls = np.arange(-2*m,2*m+1)
    q = eps*ls
    g0 = np.exp(-q*q + .25j*q*q)
    g1 = np.exp(-(q-.4)**2/.6 + .6j*q*q)
    g0 /= np.linalg.norm(g0)
    g1 /= np.linalg.norm(g1)
    characteristic = 0j
    # In the expectation of exp(i(Z0-2 Z1+Y)), pointer
    # momenta go to (i+1,j-2) and final data momentum goes up one.
    first = {int(i):advance(np.roll(source,-int(i),axis=0),ticks,"walk")
             for i in ls}
    for a,i in enumerate(ls[:-1]):
        for b,j in enumerate(ls[2:],2):
            ket = advance(np.roll(first[int(i)],-int(j),axis=0),ticks,"walk")
            bra = advance(np.roll(first[int(i+1)],-int(j-2),axis=0),ticks,"walk")
            overlap = np.vdot(bra,np.roll(ket,1,axis=0))
            characteristic += (g0[a+1]*g1[b-2]).conjugate() * g0[a]*g1[b]*overlap
    # The two finite-width contributions combine as a Weyl quadrature.
    # exp(i[-2Z1-interval*P1]) maps j to j-2 with
    # the midpoint phase -interval*eps*(j-1).
    quadrature = (np.vdot(g0[1:],g0[:-1]) *
                  np.vdot(g1[:-2],g1[2:]*np.exp(-1j*interval*eps*(ls[2:]-1))))
    target = sum(abs(g1)**2 * np.exp(-1j*interval*q))
    values = [characteristic,quadrature,target]
    return dict(m=m,delta=delta,epsilon=eps,sites=n,ticks=ticks,interval=interval,p0=p0,
                characteristic_quadrature_impulse=[[float(v.real),float(v.imag)] for v in values],
                band_residual=float(abs(characteristic-quadrature)),
                pointer_resolution_effect=float(abs(quadrature-target)))


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("output",type=Path)
    path = parser.parse_args().output
    result = dict(cycle=cycle_panels(),
                  band=[band_panel(m,p) for p in (-.5,.7) for m in (4,8,12)])
    for start in (0,3):
        rows=result["band"][start:start+3]
        require(rows[-1]["band_residual"] < rows[0]["band_residual"],"coined flight approaches shear")
        require(rows[-1]["pointer_resolution_effect"] < rows[0]["pointer_resolution_effect"],
                "vanishing pointer imprecision")
    with path.open("x",encoding="utf8",newline="\n") as dest:
        json.dump(result,dest,indent=2,allow_nan=False)
        dest.write("\n")


if __name__ == "__main__":
    main()
