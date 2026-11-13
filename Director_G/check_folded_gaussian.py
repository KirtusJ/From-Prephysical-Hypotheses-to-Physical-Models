"""Run python -B check_folded_gaussian.py OUTPUT_DIRECTORY (NumPy).

Sharp (0,R); copy each second-tick direction to a fresh bit, never the site.
The selected word switches at every block. Even m leaves R. The flight tick n
is counted from release. Keep both physical rails and the shell x=n (mod 2).
"""
import argparse
import cmath
import json
import math
from collections import Counter
from fractions import Fraction as F
from itertools import product
from pathlib import Path

from check_flight_window import fly, spectral_flight
import numpy as np


BLOCKS = {"all": None, "center": (-1.0, 1.0), "right": (0.5, 1.5)}


def signed_records(m):
    """Enumerate all 2^(2m) physical words and record the unobserved site coherently."""
    records = Counter()
    for directions in product((0, 1), repeat=2*m):
        tag = directions[1::2]
        x = 2*m-2*sum(directions)
        sign = (-1)**sum(a*b for a, b in zip(directions, directions[1:]))
        records[tag, x] += sign
    accepted = tuple((j+1) % 2 for j in range(m))
    success = {(x, 0): a for (tag, x), a in records.items() if tag == accepted and a}
    formula = {(2*j-m, 0): (-1)**(m-j)*math.comb(m, j) for j in range(m+1)}
    assert success == formula
    assert sum(a*a for a in records.values()) == 4**m
    assert sum(a*a for a in success.values()) == math.comb(2*m, m)
    return records, success


def exact(m):
    records, success = signed_records(m)
    accepted_word = "".join("L" if j % 2 == 0 else "R" for j in range(m))
    history = []
    for word in product((0, 1), repeat=m):
        v = [records[word, x] for x in range(-2*m, 2*m+1)]
        history.append(dict(word="".join("RL"[c] for c in word), site_raw=v, score=sum(x*x for x in v)))
    flights = []
    for n in range(6):
        state = fly(success, n)
        den = math.comb(2*m, m)*2**n
        bound = m+n
        ports = [(x, c) for x in range(-bound, bound+1) for c in range(2)]
        amplitudes = [state.get(k, 0) for k in ports]
        tag_mass = [sum(z*z for (x, rail), z in state.items() if rail == c) for c in (0, 1)]
        assert sum(tag_mass) == den
        assert all((x-n) % 2 == 0 for x, c in state)
        # Two independent controls: keep the release site as part of the detector
        # record, or acquire site and rail after every microscopic step.
        sharp = fly({(0, 0): 1}, n)
        dephased = Counter()
        for (site, c), amp in success.items():
            for (x, rail), z in sharp.items():
                dephased[site+x, rail] += amp**2*z**2
        assert sum(dephased.values()) == den
        flights.append(dict(n=n, bound=bound, raw=amplitudes, conditional_denominator=den,
                            rail_scores=tag_mass, contrast=F(tag_mass[0]-tag_mass[1], den),
                            occupied_parity=n % 2, release_site_read_scores=[dephased[k] for k in ports],
                            release_site_read_TV=F(sum(abs(z*z-dephased[k]) for k,z in zip(ports,amplitudes)),2*den)))
    return dict(m=m, block_word=accepted_word, prefix_bound=2*m, prefix_denominator=4**m,
                all_record_rows=history, accept_score=math.comb(2*m, m),
                success_mass=F(math.comb(2*m, m),4**m), every_microscopic_site_read_acceptance=F(1,2**m),
                release_variance_scaled=F(m,2*m-1), flight=flights)


def continuum_block(tau, block):
    q = 1+1j*tau
    if block is None:
        return 1.0, 1/cmath.sqrt(q)
    lo, hi = block
    mass = (math.erf(hi/abs(q))-math.erf(lo/abs(q)))/2
    # Composite Simpson's rule, 1000 panels, for the bounded-block continuum reference.
    y = np.linspace(lo, hi, 1001)
    vals = np.exp(-y*y/q)/(math.sqrt(math.pi)*q)
    integral = (hi-lo)/3000*(vals[0]+vals[-1]+4*sum(vals[1:-1:2])+2*sum(vals[2:-1:2]))
    return mass, complex(integral)


def wave_grid(m, maximum_n):
    nring = 1 << (2*(m+maximum_n)+2).bit_length()
    x = np.arange(nring)
    x = np.where(x < nring//2,x,x-nring)
    k = 2*np.pi*np.fft.fftfreq(nring)
    spinor = np.zeros((2,nring))
    center = math.comb(m,m//2)
    for j in range(m+1):
        spinor[0,(2*j-m) % nring] = (-1)**j*(math.comb(m,j)/center)
    spinor /= np.linalg.norm(spinor)
    normalized_transform = np.fft.fft(spinor[0])
    expected = (-1)**(m//2)*np.sin(k)**m
    assert np.max(abs(normalized_transform/np.max(abs(normalized_transform))-expected)) < 1e-11
    return x, k, spinor


def numerical(m, goal):
    n0 = m*goal
    x, k, source = wave_grid(m,n0+3)
    Y = x/math.sqrt(m)
    quadratures = {label: [] for label in BLOCKS}
    rows = []
    for n in range(n0,n0+4):
        tau = n/m
        state = spectral_flight(source,n,k)
        pr = abs(state)**2
        total = pr.sum(axis=0)
        normalization_residual=float(total.sum()-1)
        parity_leakage=float(total[(x-n) % 2 != 0].sum())
        assert abs(normalization_residual)<1e-11
        assert parity_leakage < 1e-18
        mean = float(Y @ total)
        var = float((Y-mean)**2 @ total)
        sharp = np.zeros_like(source)
        sharp[0,0]=1
        sharp_final = abs(spectral_flight(sharp,n,k))**2
        # A sharp release-site label destroys interference between different x.
        # Its global coin mass equals that of any of the translated sharp flights.
        sharp_contrast = float(np.sum(sharp_final[0]-sharp_final[1]))
        sharp_mean = float(Y @ sharp_final.sum(axis=0))
        sharp_var = float((Y-sharp_mean)**2 @ sharp_final.sum(axis=0))
        source_var = float(Y**2 @ (source[0]**2))
        values = {}
        for label, interval in BLOCKS.items():
            mask = np.ones(len(Y),dtype=bool) if interval is None else (Y>=interval[0]) & (Y<=interval[1])
            mass,j = continuum_block(tau,interval)
            raw = float((pr[0,mask]-pr[1,mask]).sum())
            phase = (-1j)**(n % 4)
            values[label] = dict(rail_mass=[float(pr[c,mask].sum()) for c in (0,1)],
                                 contrast=raw, predicted_mass=mass, J=[j.real,j.imag],
                                 predicted_raw=(phase*j).real,
                                 no_parity_factor_control=((1j)**(n % 4)*j).real)
            quadratures[label].append(raw)
        if m >= 32 and goal > 0:
            expected_sign = (1,-1,-1,1)[n % 4]
            assert expected_sign*values["all"]["contrast"] > 0
        rows.append(dict(n=n, phase=n % 4, tau=tau, normalization_residual=normalization_residual,
                         inaccessible_parity_mass=parity_leakage, physical_mean=mean, variance=var,
                         continuum_variance=(1+tau*tau)/2, blocks=values,
                         release_site_read_global_contrast=sharp_contrast,
                         release_site_read_variance=source_var+sharp_var))
    pairs = {}
    for label, v in quadratures.items():
        _, expected = continuum_block(goal,BLOCKS[label])
        pairs[label] = dict(from_first_two=v[:2],from_next_two=[-v[2],-v[3]],
                            reference_at_common_limiting_time=[expected.real,expected.imag])
    return dict(m=m, delta=1/math.sqrt(m), prep_ticks=2*m, prep_scaled_duration=2,
                signed_Fourier_lobe_factor=(-1)**(m//2), acceptance=math.comb(2*m,m)/(4**m),
                N=len(x), goal_tau=goal, flight=rows, adjacent_tick_reconstruction=pairs)


def direct_crosscheck(m):
    _, success = signed_records(m)
    x,k,source = wave_grid(m,5)
    errors=[]
    for n in range(6):
        raw=fly(success,n)
        expected=np.zeros_like(source)
        denominator=math.sqrt(math.comb(2*m,m)*2**n)
        for (site,rail), a in raw.items():
            expected[rail,site % len(x)]=a/denominator
        error=float(np.max(abs(expected-spectral_flight(source,n,k))))
        assert error < 1e-12
        errors.append(error)
    return dict(m=m, max_signed_amplitude_errors_n0_through_5=errors)


def main():
    panel = [(m,tau) for m in (8,32,128,512) for tau in (0,1,2)]
    return dict(predicates_before_run=[
        "Enumerate every microscopic signed path for m=2,4,6 with every second-tick rail labelled. Verify all tag scores sum to 4^m, and the alternating tag equals the signed binomial vector and central-binomial acceptance.",
        "Keep every exact port through n=5 plus the site-resolved comparison. The Fourier source equals the signed sin^m filter. Unitary conservation and occupied parity are tested.",
        "At m=8,32,128,512 and tau=0,1,2 test free ticks m*tau through m*tau+3; at finite m the four ticks have different actual tau. Retain finite deviations, full-space and two bounded-block readings, and the wrong odd-phase sign."],
        conventions="even m ends R. Arrays all_record_rows use consecutive sites -2m..2m and the final rail named by the tag. Flight arrays use every site -bound..bound, each ordered R,L. Conditional flight probabilities are raw²/conditional_denominator. Multiply by success_mass for joint probabilities. Zero entries and failed tags retained.",
        model="Common square score on complete pointer-labelled raw signed tallies. Preparations use a direction copy coherent across sites, with no route label inside a record. Fresh launch for each terminal tick. A site-and-rail record at every step resolves each full path and gives success 2^-m. An additional retained release-site read gives a mixture of translated sharp R flights.",
        scaling="Y=x/sqrt(m), tau=n/m measured from release. The m two-step blocks also consume 2m steps, or 2 time units on this clock. The signed Fourier multiplier of the even-m word is (-1)^(m/2) sin(k)^m, a real common sign that squares to +1 even in g². Four tests per limiting time include the occupied parity x=n mod 2. Full-space contrast Re[(-i)^n(1+i tau)^(-1/2)]. Quadratures of g² refer to the chosen calibrated phase, not an arbitrary unknown global phase.",
        numeric_precision="Finite floating results are serialized at Python round-trip precision, including signed roundoff and exact zeros. The complete exact path vector cross-check requires maximum amplitude error <1e-12. FFT norm and normalized source-transform errors must be <1e-11 and inaccessible-parity probability <1e-18. The analytic whole-space reference is closed form; bounded intervals use composite Simpson integration with 1000 panels.",
        independent_exact_Fourier_check=[direct_crosscheck(m) for m in (2,4,6)],
        exact=[exact(m) for m in (2,4,6)], numeric=[numerical(m,tau) for m,tau in panel])


if __name__ == "__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output",type=Path)
    dest=parser.parse_args().output
    result=main()
    dest.mkdir(parents=True,exist_ok=True)
    (dest/"folded_gaussian.json").write_bytes((json.dumps(result,default=str,allow_nan=False,separators=(",",":"))+"\n").encode("utf-8"))
    print("Verified full direction-labelled paths for 3 short sources and 48 free-flight quadrature panels.")
