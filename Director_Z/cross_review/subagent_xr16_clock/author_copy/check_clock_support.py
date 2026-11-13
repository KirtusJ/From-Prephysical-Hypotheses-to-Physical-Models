"""Sharp finite clock support bounds and eight-sheet optical transfers."""
import argparse
import cmath
import hashlib
import json
import math
from fractions import Fraction as F
from pathlib import Path


def phase_transfer(seed, launch, plate, depth):
    """Sum signed paths by physical (site, coin, sheet). All ticks share a denominator."""
    m = len(seed)
    states = {(0, c, (j + c*launch) % m): v for c in (0, 1) for j, v in enumerate(seed) if v}
    for _ in range(depth):
        after = {}
        for (x, c, j), v in states.items():
            sheet = (j + plate*(x == 0)) % m
            for dest in (0, 1):
                mode = (x + 2*dest - 1, dest, sheet)
                after[mode] = after.get(mode, 0) + (-v if c == dest == 1 else v)
        states = after
    den = sum(v*v for v in states.values())
    assert den == 2**(depth+1)*sum(v*v for v in seed)
    bins = {}
    for (x, _, _), v in states.items():
        bins[x] = bins.get(x, 0) + v*v
    return {x:F(w, den) for x,w in sorted(bins.items())}


def transfer_trials():
    seed = [1,0,0,0,-1,0,0,0]
    rows = []
    for n in range(13):
        s = sum(v*v for v in seed)
        adjacent = 2*sum(v*seed[j-1] for j,v in enumerate(seed))
        ports = phase_transfer(seed, 6, 3, 10)
        assert ports[0] == F(688*s + 480*adjacent, 2048*s)
        varying = {setting:phase_transfer(seed,6,setting,10)[0] for setting in range(5)}
        assert [varying[i] for i in (0,1,2,4)] == [F(i,128) for i in (9,51,85,85)]
        other = phase_transfer(seed, 18, 9, 10)
        assert other[0] == F(688*s - 480*adjacent, 2048*s)
        # Change only one of launch and plate, or conjugate both conventions.
        mixed = [phase_transfer(seed,l,g,10)[0] for l,g in ((18,3),(6,9))]
        assert mixed == [F(51,128)]*2 and phase_transfer(seed,-6,-3,10) == ports
        rows.append(dict(pluses=n, signed_seed=seed, joint_herald=str(F(s,4**(n+1))),
                         return_by_plate={str(i):str(w) for i,w in varying.items()},
                         complete_positions={str(x):str(w) for x,w in ports.items()},
                         swapped_pair=str(other[0]), single_setting_changes=list(map(str,mixed))))
        seed = [a+seed[j-1] for j,a in enumerate(seed)]
    return rows


def capacity(m, length):
    if length == m:
        return 1.
    return (length + abs(math.sin(math.tau*length/m))/math.sin(math.tau/m))/m


def support_trials():
    # Compare the closed expression with the actual Fourier projection of
    # explicit extremal real cosine/sine vectors on each interval.
    checks = []
    for m in list(range(3,34)) + [64,128,256]:
        residuals = []
        min_length = None
        for length in range(1,m+1):
            roots = [cmath.exp(1j*math.tau*j/m) for j in range(length)]
            # Reflection about the centre diagonalizes the real restricted Gram.
            centre = cmath.exp(-1j*math.pi*(length-1)/m)
            actual = []
            for vec in ([ (z*centre).real for z in roots],[(z*centre).imag for z in roots]):
                mass = sum(v*v for v in vec)
                if mass:
                    actual.append(2*abs(sum(z*v for z,v in zip(roots,vec)))**2/(m*mass))
            lam = capacity(m,length)
            residuals.append(abs(max(actual)-lam))
            # Identifies strict crossing away from roundoff. Proof handles equality.
            if min_length is None and lam > .5+1e-12:
                min_length = length
        expected = m//2 if m%2 else m//2+1
        assert min_length == expected and max(residuals) < 2e-14
        checks.append(dict(M=m, all_lengths=m, first_strict_majority_length=min_length,
                           one_site_capacity=2/m, maximum_extremizer_residual=max(residuals)))
    return checks


def clock_family():
    # Choose exact weak field 2*pi/M, F=2*pi, delta=2^-b,
    # epsilon=delta (semiclassical) or 1 (fixed action). Then M=1/(epsilon*delta^3).
    rows = []
    for fixed_action in (True, False):
        for b in range(1,9):
            delta = F(1,2**b)
            eps = F(1) if fixed_action else delta
            m = int(1/(eps*delta**3))
            tick = eps*delta**2
            n = m//4
            assert m%4 == 0 and 2*n-1 < m//2 < 2*n+1
            assert n*tick == 1/(4*delta)
            rows.append(dict(M=m, delta=str(delta), epsilon=str(eps), tau=str(tick),
                             ticks_necessary_for_majority=n, preparation_time_at_least=str(n*tick),
                             upper_at_one_earlier_tick=capacity(m,2*n-1)))
    return rows


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("output", type=Path)
    args = p.parse_args()
    result = dict(physical_eight_sheet=transfer_trials(), arc_concentration=support_trials(),
                  uniform_force_family=clock_family(),
                  comparison="Every output distribution is conditioned on the stated seed. The sheet support cone is a distinct, explicitly local cost model. The exact extremal arc bound covers states in its cone and grants every amplitude on the arc; reachability of the extremizer is a separate condition.")
    args.output.mkdir(parents=True, exist_ok=True)
    dest = args.output/"clock_support.json"
    dest.write_bytes((json.dumps(result,indent=2)+"\n").encode())
    print(dest, hashlib.sha256(dest.read_bytes()).hexdigest())
