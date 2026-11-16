"""Certify a randomized terminal-attenuation test of the five-site walk."""
import json
from fractions import Fraction as Q
from pathlib import Path
from runpy import run_path

HERE = Path(__file__).resolve().parent
shared = run_path(str(HERE / 'check_split_readout.py'))
counts, require = shared['counts'], shared['require']
timing = json.loads((HERE / 'single_port_timing_output.json').read_text())[0]
FULL = Q(78, 125)
ETA = Q(49, 50)
SIZE = Q(1, 20)
GRID = 10**12


def upper_tail(row, den, cutoff):
    return Q(sum(row[cutoff:]), den)


def timing_cutoff(m, endpoint):
    row, den = counts(m, endpoint)
    so_far = 0
    for k in range(m, -1, -1):
        so_far += row[k]
        if 20 * so_far > den:
            return k + 1
    raise ValueError('cutoff search failed')


def design(n, optical_cutoff, override):
    p0 = Q(timing['null_ceiling'])
    p1 = Q(timing['ideal_floor'])
    p_minus = 1 - Q(timing['always_click'])
    success = ETA*p1 + (1-ETA)*p_minus
    g = Q(49, 100)
    # The best classical score is FULL + (1-FULL)*(1-g)*y,
    # where y^51 = [g*(1-FULL)/FULL]^49. Compare by raising to integer powers.
    cap = Q('.683392808')
    root_power = (g*(1-FULL)/FULL)**49
    coefficient = (1-FULL)*(1-g)
    require(((cap-FULL)/coefficient)**51 > root_power, 'classical ceiling too low')
    require(((cap-Q(1,10**9)-FULL)/coefficient)**51 < root_power,
            'classical ceiling unexpectedly loose')
    photon = FULL*ETA + (1-FULL)*(1-Q(51,100)*ETA)
    contaminated_cap = cap + (1-cap)*override
    field_size = upper_tail(*counts(n, contaminated_cap), optical_cutoff)
    attenuation_power = upper_tail(*counts(n, photon), optical_cutoff)
    m_counts, denominator = counts(n, FULL)
    # Round each conditional term outwards before averaging the randomized allocation.
    # This keeps the maximum rounding charge for the average below one grid unit.
    time_low = time_size = 0
    cuts = []
    for m, count in enumerate(m_counts):
        cutoff = timing_cutoff(m, p0)
        cuts.append(cutoff)
        size = upper_tail(*counts(m, p0), cutoff)
        lower = upper_tail(*counts(m, success), cutoff)
        require(size <= SIZE, 'conditional timing size')
        if cutoff:
            require(upper_tail(*counts(m, p0), cutoff-1) > SIZE, 'wrong cutoff')
        time_low += count * (lower*GRID//1)
        time_size += count * -((-size*GRID)//1)
    time_low = Q(time_low, denominator*GRID)
    time_size = Q(time_size, denominator*GRID)
    joint = time_low + attenuation_power - 1
    require(field_size < SIZE and joint > Q(95,100), 'joint targets')
    # A source told the setting can choose a bright full-setting pulse
    # and vacuum on every attenuated trial. Its bright-pulse miss probability is .01.
    leaked = 1 - FULL*Q('.01')
    require(leaked > cap and upper_tail(*counts(n, leaked),optical_cutoff)>Q('.999'),
            'setting-disclosure adverse control')
    # For half transmission, every mixture of classical pulse intensities has
    # P(full empty) >= P(half empty)^2. A lossy single photon violates it even
    # when the prespecified 158-shot decision is too insensitive at low efficiency.
    eta = Q(3,10)
    mean, second = 1-eta/2, 1-eta
    require(mean**2>second,'strict semiclassical inequality even for a weak source')
    return dict(
        preparations=n, history_conditional_override_ceiling=str(override), full_probability=str(FULL), optical_success_floor=str(photon),
        attenuation_at_least=optical_cutoff, field_size_ceiling=-((-field_size*GRID)//1),
        attenuation_power_floor=attenuation_power*GRID//1,
        timing_size_ceiling=-((-time_size*GRID)//1), timing_power_floor=time_low*GRID//1,
        joint_power_floor=joint*GRID//1, grid=GRID, timing_cutoffs_by_full_count=cuts
    )


if __name__ == '__main__':
    result = [design(158, 118, Q(0)), design(180, 135, Q(1, 100))]
    print(json.dumps(result, indent=2))
