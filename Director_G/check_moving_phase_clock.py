"""Check an always-hopping phase clock in physical coordinates, including readout aliases."""
import argparse
import cmath
import hashlib
import json
import math
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path

from check_clock_support import phase_transfer


def neighbors(state, ring, selected, physical):
    out = defaultdict(int)
    for (x, c, j), amp in state.items():
        bit = selected(x,c)
        step = (2*bit-1) if physical else bit
        out[x,c,(j+step)%ring] += amp
    return out


def fixed_time(state, stage, ring, physical, fixed):
    # Extra right-moving stream permits a single decoder at all logical boundaries.
    after = neighbors(state,ring,stage,physical)
    if fixed:
        return {(x,c,(j+1)%ring):w for (x,c,j),w in after.items()}
    return after


def decoded(state, size, time, fixed):
    result = {}
    for (x,c,y),v in state.items():
        offset = (y + (0 if fixed else time)) % (2*size)
        assert offset % 2 == 0
        result[x,c,offset//2] = v
    return result


def optical(seed, plate, fixed):
    # One independent path sum contains signed data at every physical tick.
    size = len(seed)
    state = {(0,c,2*j):v for j,v in enumerate(seed) for c in (0,1) if v}
    logical = {(0,c,j):v for j,v in enumerate(seed) for c in (0,1) if v}
    t = 0
    def transport(bit):
        nonlocal state, logical, t
        state = fixed_time(state, bit, 2*size, True, fixed)
        logical = fixed_time(logical, bit, size, False, False)
        t += 1
        assert decoded(state,size,t,fixed) == logical
    def coin_and_base_stream(s):
        after = defaultdict(int)
        for (x,c,j),v in s.items():
            for dest in (0,1):
                after[x+2*dest-1,dest,j] += -v if c == dest == 1 else v
        return after
    for _ in range(6):
        transport(lambda x,c:c)
    for _ in range(10):
        for _ in range(plate):
            transport(lambda x,c:int(x == 0))
        # Coin + base transport are local in sheet. Run them during a common
        # left hop (and a right return for fixed frame), hence no sheet rest.
        state, logical = coin_and_base_stream(state), coin_and_base_stream(logical)
        transport(lambda x,c:0)
    ports = defaultdict(int)
    for (x,_,_),v in state.items():
        ports[x] += v*v
    total = sum(ports.values())
    table = {x:F(w,total) for x,w in ports.items()}
    assert table == phase_transfer(seed,6,plate,10)
    return dict(plate=plate, fixed=fixed, transport_ticks=t*(2 if fixed else 1),
                return_at_zero=str(table[0]), position={str(x):str(w) for x,w in sorted(table.items())})


def spectral_test(m,t,k):
    physical = [0j]*(2*m)
    for j in range(m):
        physical[(2*j-t)%(2*m)] = cmath.exp(1j*math.tau*k*j/m)/math.sqrt(m)
    w = [abs(sum(v*cmath.exp(-1j*math.tau*n*x/(2*m)) for x,v in enumerate(physical)))**2/(2*m)
         for n in range(2*m)]
    exact = [F(1,2) if n%m == k%m else F(0) for n in range(2*m)]
    assert max(abs(a-b) for a,b in zip(w,exact)) < 2e-13
    edge_overlap = sum(v.conjugate()*physical[(i-1)%(2*m)] for i,v in enumerate(physical))
    assert edge_overlap == 0
    return dict(M=m,time=t,logical_mode=k,
                occupied_physical_modes=[n for n,a in enumerate(exact) if a],
                physical_unit_pair_weight=str(exact[1]+exact[-1]))


def motor_permutation(m, branch, physical_pos, motor):
    # On the initialized motor=0 sector: first hop is left/right according
    # to retained branch, second hop right. Each pulse remains invertible on
    # the complete motor space. Stream +1 for motor 0, -1 for motor 1.
    ring = 2*m
    motor ^= (1-branch)
    first = (physical_pos + (1-2*motor))%ring
    motor ^= (1-branch)
    return first,(first+1-2*motor)%ring,motor


def motor_control(m):
    dest = set()
    for branch in (0,1):
        for pos in range(2*m):
            for motor in (0,1):
                mid,end,ret = motor_permutation(m,branch,pos,motor)
                assert (mid-pos)%(2*m) in (1,2*m-1) and (end-mid)%(2*m) in (1,2*m-1)
                assert end == (pos+(1-2*motor)*2*branch)%(2*m) and ret == motor
                dest.add((branch,end,ret))
    assert len(dest) == 8*m
    return dict(M=m, complete_permutation_size=len(dest), clean_motor_input=0,
                opposite_motor_transports_the_inverse=True)


def run():
    rows=[]
    seed=[1,0,0,0,-1,0,0,0]
    for n in range(4):
        rows.append(dict(seed_plus_count=n,schedules=[optical(seed,p,f) for p in (0,1,2,3,4) for f in (False,True)]))
        seed=[v+seed[j-1] for j,v in enumerate(seed)]
    return dict(optical=rows, alias_tests=[spectral_test(m,t,k) for m in (3,4,5,8,11,16)
                for t in (0,1,2*m+1) for k in (0,1,m-1)],
                complete_motor=[motor_control(m) for m in (3,4,5,8,16)],
                inputs="Xue comparison codes previously calibrated odd seeds. Base coin and shift share a common sheet hop at each of ten base ticks. The initial coin split is supplied at the launch boundary. The fixed-frame schedule doubles every streamed tick.")


if __name__ == "__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output",type=Path)
    args=parser.parse_args()
    args.output.mkdir(parents=True,exist_ok=True)
    dest=args.output/"moving_phase_clock.json"
    dest.write_bytes((json.dumps(run(),indent=2)+"\n").encode())
    print(dest,hashlib.sha256(dest.read_bytes()).hexdigest())
