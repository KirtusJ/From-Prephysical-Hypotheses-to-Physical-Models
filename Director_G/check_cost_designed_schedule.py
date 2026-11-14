"""Compare a cost-designed schedule with the original linear taper under both laws."""
from fractions import Fraction as Q
from mpmath import iv
from check_paired_exposure import cells, rates
from check_sequential_exposure import dec
from check_tapered_blocks import BLOCKS, BLOCK_SIZE, SCALE, gaussian_cdf

# Absolute integer score required at each of the 79 early checkpoints.
WIDTHS = (
    81, 81, 81, 80, 80, 80, 80, 80, 80, 80, 80, 79,
    79, 79, 79, 79, 79, 78, 78, 78, 78, 78, 77, 77,
    77, 77, 77, 76, 76, 76, 76, 75, 75, 75, 74, 74,
    74, 73, 73, 73, 72, 72, 71, 71, 71, 70, 70, 69,
    69, 68, 67, 67, 66, 66, 65, 64, 63, 63, 62, 61,
    60, 59, 58, 57, 56, 54, 53, 52, 50, 48, 46, 44,
    42, 40, 37, 33, 29, 24, 17,
)


def check(table, increments):
    mean = sum(p*z for p, z in zip(table, increments))
    var = sum(p*(z-mean)**2 for p, z in zip(table, increments))
    third = sum(p*abs(z-mean)**3 for p, z in zip(table, increments))
    sd = iv.sqrt(BLOCK_SIZE*var)
    eps = iv.mpf('0.475')*third/(var**iv.mpf('1.5')*iv.sqrt(BLOCK_SIZE))
    # F[j] is the integer upper approximation to the Gaussian Pr(rounded block <= j).
    F = {}
    for j in range(-202, 203):
        x = ((iv.mpf(j)+iv.mpf('0.5'))/20-BLOCK_SIZE*mean)/sd
        prob = gaussian_cdf(x)*SCALE
        upper = int(prob.b)+1
        assert upper - prob.a < 1300
        F[j] = min(SCALE, upper)
    # Interior bin and tail upper probabilities. All rounding points are
    # exact rationals, permitting integer arithmetic throughout the recursion.
    weight = {j: F[j]-F[j-1]+1300 for j in range(-200, 201)}
    assert len(WIDTHS) == BLOCKS-1 and max(WIDTHS) <= 100
    previous = [92-(43*i//BLOCKS) for i in range(1, BLOCKS)]
    for lower, schedule in [(True, previous), (False, WIDTHS)]:
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
        correction = BLOCKS*(BLOCKS-1)*eps
        if lower:
            pairs = BLOCK_SIZE*(iv.mpf(exposure)/SCALE-correction)
            print('previous mean lower', float(pairs.a))
            assert pairs > 2285993490000000
        else:
            risk = iv.mpf(error)/SCALE + BLOCKS*eps
            pairs = BLOCK_SIZE*(iv.mpf(exposure)/SCALE+correction)
            print('new error and mean upper', float(risk.b), float(pairs.b))
            assert risk < iv.mpf('0.04998137') and pairs < 2263615200000000



def main():
    iv.dps = 85
    candidates = []
    for s,g,l in rates():
        p,q = [cells(s,Q(1,10**8)*v) for v in (g,l)]
        z = [iv.ln(dec(a/b)) for a,b in zip(p,q)]
        candidates.append((sum(dec(a)*v for a,v in zip(p,z)),p,q,z))
    _,p,q,z = max(candidates, key=lambda row: row[0].a)
    check(list(map(dec,p)), z)
    check(list(map(dec,q)), [-v for v in z])


if __name__ == '__main__':
    main()
