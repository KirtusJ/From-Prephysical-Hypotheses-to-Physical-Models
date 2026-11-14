"""Compare 160 finer-score checkpoints against the previous 80-checkpoint rule."""
from fractions import Fraction as Q
from mpmath import iv
from check_paired_exposure import cells, rates
from check_sequential_exposure import dec
from check_tapered_blocks import SCALE, gaussian_cdf

from check_cost_designed_schedule import WIDTHS as PREVIOUS

WIDTHS = (
    164, 164, 163, 163, 163, 163, 163, 163, 163, 163, 163, 162,
    162, 162, 162, 162, 162, 162, 161, 161, 161, 161, 161, 161,
    161, 160, 160, 160, 160, 160, 160, 159, 159, 159, 159, 159,
    159, 158, 158, 158, 158, 158, 157, 157, 157, 157, 157, 156,
    156, 156, 156, 156, 155, 155, 155, 155, 154, 154, 154, 154,
    153, 153, 153, 152, 152, 152, 152, 151, 151, 151, 150, 150,
    150, 149, 149, 149, 148, 148, 148, 147, 147, 146, 146, 146,
    145, 145, 144, 144, 143, 143, 143, 142, 142, 141, 141, 140,
    140, 139, 138, 138, 137, 137, 136, 136, 135, 134, 134, 133,
    132, 132, 131, 130, 129, 129, 128, 127, 126, 125, 124, 124,
    123, 122, 121, 120, 119, 118, 117, 115, 114, 113, 112, 111,
    109, 108, 106, 105, 103, 102, 100, 99, 97, 95, 93, 91,
    89, 86, 84, 81, 78, 75, 72, 69, 65, 61, 56, 51,
    44, 36, 26,
)


def check(table, increments, schedule, scale, lower):
    blocks = len(schedule)+1
    block_size = 4_000_000_000_000_000//blocks
    assert blocks*block_size == 4_000_000_000_000_000
    mean = sum(p*z for p, z in zip(table, increments))
    var = sum(p*(z-mean)**2 for p, z in zip(table, increments))
    third = sum(p*abs(z-mean)**3 for p, z in zip(table, increments))
    sd = iv.sqrt(block_size*var)
    eps = iv.mpf('0.475')*third/(var**iv.mpf('1.5')*iv.sqrt(block_size))
    # F[j] is the integer upper approximation to the Gaussian Pr(rounded block <= j).
    F = {}
    for j in range(-2*max(schedule)-2, 2*max(schedule)+2):
        x = ((iv.mpf(j)+iv.mpf('0.5'))/scale-block_size*mean)/sd
        prob = gaussian_cdf(x)*SCALE
        upper = int(prob.b)+1
        assert upper - prob.a < 1300
        F[j] = min(SCALE, upper)
    # Interior bin and tail upper probabilities. All rounding points are
    # exact rationals, permitting integer arithmetic throughout the recursion.
    weight = {j: F[j]-F[j-1]+1300 for j in range(-2*max(schedule), 2*max(schedule)+1)}
    live = {0: SCALE}
    error = exposure = 0
    for width in (*schedule, 0):
        exposure += sum(live.values())
        if not width:
            error += sum(v*(F[-1-s]+F[-s]) for s,v in live.items())//(2*SCALE)+1
            break
        error += sum(v*F[-width-s] for s,v in live.items())//SCALE+1
        live = {
            y: (sum(v*max(0, weight[y-s]-2600) for s,v in live.items())//SCALE
                if lower else sum(v*weight[y-s] for s,v in live.items())//SCALE+1)
            for y in range(1-width,width)
        }
    correction = blocks*(blocks-1)*eps
    if lower:
        pairs = block_size*(iv.mpf(exposure)/SCALE-correction)
        print('previous mean lower', float(pairs.a))
        assert pairs > 2263373670000000
    else:
        risk = iv.mpf(error)/SCALE + blocks*eps
        pairs = block_size*(iv.mpf(exposure)/SCALE+correction)
        print('new error and mean upper', float(risk.b), float(pairs.b))
        assert risk < iv.mpf('0.04999529') and pairs < 2255410570000000




def main():
    iv.dps = 85
    candidates = []
    for s,g,l in rates():
        p,q = [cells(s,Q(1,10**8)*v) for v in (g,l)]
        z = [iv.ln(dec(a/b)) for a,b in zip(p,q)]
        candidates.append((sum(dec(a)*v for a,v in zip(p,z)),p,q,z))
    _,p,q,z = max(candidates, key=lambda row: row[0].a)
    for table, increments in [(p,z), (q,[-v for v in z])]:
        check(list(map(dec,table)), increments, PREVIOUS, 20, True)
        check(list(map(dec,table)), increments, WIDTHS, 40, False)


if __name__ == '__main__':
    main()
