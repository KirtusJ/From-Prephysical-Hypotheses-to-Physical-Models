"""Fixed-action infinitesimal generator and spectrum controls for a local string.

Run python -B check_string_band.py OUTPUT_DIRECTORY. Requires NumPy.
The moving packets and the exact dressed-link history check are separate tests.
"""

import argparse
import json
import math
import os
from fractions import Fraction
from pathlib import Path

os.environ["OPENBLAS_NUM_THREADS"] = "1"
import numpy as np


LENGTH = 8.
GAMMA = math.atan2(7, 24)
KAPPA = 12 / 7
REST = np.array([1, 1], dtype=complex) / math.sqrt(2)


def one_body(k):
    u = np.array([[.8, .6j*np.exp(-1j*k)], [.6j*np.exp(1j*k), .8]])
    u = u @ np.array([[.6, -.8j], [-.8j, .6]])
    omega = math.acos(12*(1 + math.cos(k))/25)
    projected = (np.exp(1j*omega)*REST - u@REST) / (2j*math.sin(omega))
    projected /= np.linalg.norm(projected)
    assert np.linalg.norm(u@projected-np.exp(-1j*omega)*projected) < 1e-13
    return u, projected, omega


def wedge(v, w):
    return (np.outer(v, w)-np.outer(w, v))/math.sqrt(2)


def sampled_derivative(cells):
    # Antiperiodic single-mode Fourier momenta make the two-occupation walk
    # periodic. This finite periodic diagnostic uses the shortest-distance
    # potential. Its purpose is to test local consistency, not the line limit.
    m = sigma = 1.
    eps = .5
    a = LENGTH/cells
    tau = m*KAPPA*a*a/eps
    j = np.arange(cells)
    x = (j[:, None] + np.array([0., .5]))*a
    xx=x.ravel()
    sep=np.abs(xx[:, None]-xx[None, :])
    sep=np.minimum(sep,LENGTH-sep)
    modes=[]
    momenta=[]
    for ell in (-1, 1):
        k=(2*ell+1)*math.pi/cells
        u, spin, om=one_body(k)
        source=np.exp(1j*k*j[:,None])/math.sqrt(cells)
        p=eps*k/a
        momenta.append(p)
        modes.append(dict(dressed=(source*spin).ravel(),rest=(source*REST).ravel(),
                          next_dressed=(source*(u@spin)).ravel(),next_rest=(source*(u@REST)).ravel()))
    m1,m2=modes
    kinetic=sum(p*p/(2*m) for p in momenta)
    target=-1j*(kinetic+sigma*sep)/eps*wedge(m1["rest"],m2["rest"])
    kick=np.exp(-1j*tau*sigma*sep/eps)
    measurements={}
    for label in ("dressed","rest"):
        old=wedge(m1[label],m2[label])
        updated=np.exp(2j*GAMMA)*wedge(m1["next_"+label],m2["next_"+label])
        evolved=kick*updated
        residual=(evolved-old)/tau-target
        assert abs(np.linalg.norm(evolved)-1.) < 2e-13
        measurements[label] = float(np.linalg.norm(residual))
    return dict(cells=cells, cell_pitch=a, time_step=tau, momenta=momenta,
                norm_defect_of_generator=measurements)


def sturm_count(n, dx, energy):
    # Inertia of the dimensionless Dirichlet operator -d²/dr²+r by LDL.
    off=-1./dx**2
    pivot=2/dx**2+dx-energy
    negatives=int(pivot<0)
    for j in range(2,n+1):
        if abs(pivot) < 1e-200:
            pivot=-1e-200
        pivot=2/dx**2+j*dx-energy-off*off/pivot
        negatives+=int(pivot<0)
    return negatives


def airy_levels(n):
    box=18.
    dx=box/(n+1)
    levels=[]
    for k in range(1,4):
        low,high=0.,9.
        for _ in range(52):
            mid=(low+high)/2
            if sturm_count(n,dx,mid)<k:
                low=mid
            else:
                high=mid
        levels.append((high+low)/2)
    return dict(interior=n, rmax=box, spacing=dx, levels=levels)


def dirac_derivative(cells, reverse_mass=False):
    s,d=.8,.6
    eps=.5
    a=LENGTH/cells
    tau=s*a  # c=mu=1
    # This use has an exact trigonometric gate; the paper gives the rational
    # small-angle replacement with the same limiting generator.
    gamma=tau/eps*(-1 if reverse_mass else 1)
    beta=math.atan2(s,d)-gamma
    C,B=math.cos(beta),math.sin(beta)
    X=np.array([[0,1],[1,0]],complex)
    Y=np.array([[0,-1j],[1j,0]],complex)
    Z=np.diag([1.,-1.])
    j=np.arange(cells)
    raw, stepped, targets=[],[],[]
    for ell,vec in [(-1,np.array([1.,0.])),(1,np.array([0.,1.]))]:
        k=(2*ell+1)*math.pi/cells
        p=eps*k/a
        U=(C*np.eye(2)+1j*B*(math.cos(k)*X+math.sin(k)*Y))@(d*np.eye(2)-1j*s*X)
        plane=np.exp(1j*k*j[:,None])/math.sqrt(cells)
        raw.append((plane*vec).ravel())
        stepped.append((plane*(U@vec)).ravel())
        targets.append((plane*((X+p*(s*Z-d*Y))@vec)).ravel())
    xx=(j[:,None]+np.array([0.,.5])).ravel()*a
    diff=np.abs(xx[:,None]-xx[None,:])
    potential=np.minimum(diff,LENGTH-diff)
    start=wedge(*raw)
    target=-1j/eps*(wedge(targets[0],raw[1])+wedge(raw[0],targets[1])+potential*start)
    after=np.exp(-1j*tau*potential/eps)*wedge(*stepped)
    assert abs(np.linalg.norm(after)-1.)<1e-13
    return dict(cells=cells,tau=tau,reverse_mass=reverse_mass,
                residual=float(np.linalg.norm((after-start)/tau-target)),
                cone_speed=a/tau)


def spectrum_classes(cells):
    # Sorted Z2 charges all have identical charge. Flux occupies alternating
    # intervals, rather than the sum of independent attractive pair potentials.
    from itertools import combinations
    rows=[]
    for pos in combinations(range(cells),4):
        flux=[sum(x<=edge for x in pos)%2 for edge in range(cells-1)]
        occupied=sum(flux)
        assert occupied==pos[1]-pos[0]+pos[3]-pos[2]
        rows.append([list(pos),occupied,sum(b-a for a,b in combinations(pos,2))])
    return rows


def reference_echo():
    """Exact path sum for two differential links, with normalized output ports.

    The two balanced real splitters supply a factor of 1/2 on each
    recombining path. The common link commutes through the preparation undo.
    """
    near, far = (0, 1), (0, 3)
    masks = [set(range(*pair)) for pair in (near, far)]
    additional = sorted(masks[1] - masks[0])
    assert masks[0] <= masks[1] and additional == [1, 2]
    rows = []
    for grade, blank in [
        ("independent", [1, 0, 0, 0]),
        ("aligned", [1, 0, 0, -1]),
        ("anti_aligned", [1, 0, 0, 1]),
    ]:
        for signs in [(1, 1), (-1, -1), (-1, 1), (1, -1)]:
            rotated = list(blank)
            denominator = 1
            for link, sign in zip(additional, signs):
                mask = 1 << (link - 1)
                next_state = [3 * value for value in rotated]
                for i, value in enumerate(rotated):
                    next_state[i ^ mask] += sign * (-4 if i & mask else 4) * value
                rotated = next_state
                denominator *= 5
            norm = sum(v * v for v in blank)
            rows_for_tag = []
            for keep_tag in (False, True):
                ports = []
                for port in (1, -1):
                    if keep_tag:
                        squares = sum((denominator * a)**2 + b*b for a,b in zip(blank, rotated))
                    else:
                        squares = sum((denominator * a + port * b)**2 for a,b in zip(blank, rotated))
                    ports.append(Fraction(squares, 4 * denominator**2 * norm))
                assert sum(ports) == 1
                rows_for_tag.append([str(v) for v in ports])
            expected = {"independent": Fraction(17, 25), "aligned": Fraction(9, 25),
                        "anti_aligned": Fraction(1)}
            effective = grade
            if signs[0] != signs[1] and grade != "independent":
                effective = "anti_aligned" if grade == "aligned" else "aligned"
            assert Fraction(rows_for_tag[0][0]) == expected[effective]
            assert rows_for_tag[1] == ["1/2", "1/2"]
            rows.append(dict(source=grade, signs=signs, untagged=rows_for_tag[0], tagged=rows_for_tag[1]))
    return dict(paths=[near, far], bright=[0, 1], dark=[0, 2],
                energized=[sorted(m) for m in masks], records=rows)


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("directory",type=Path)
    out=parser.parse_args().directory
    out.mkdir(parents=True,exist_ok=True)
    data=dict(generator=[sampled_derivative(n) for n in (16,32,64,128,256)],
              dirac=[dirac_derivative(n,rev) for n in (16,32,64,128,256) for rev in (False,True)],
              airy=[airy_levels(n) for n in (90,180,360,720)],
              four_charges=spectrum_classes(8),
              reference_echo=reference_echo(),
              scope="Generator norm on one finite periodic low-mode column, including both sublattice offsets. "
                    "Relative levels use a separate finite-difference Sturm count on the reduced continuum half-line in a truncated box. "
                    "The levels are not a fit to laboratory data or a theorem of spectral convergence of the Floquet walk.")
    (out/"string_band.json").write_bytes((json.dumps(data,indent=2)+"\n").encode())
