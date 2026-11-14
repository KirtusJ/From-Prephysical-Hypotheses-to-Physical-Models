"""Finite-law certificate for the 80-block rounded likelihood rule."""
from fractions import Fraction as Q
from mpmath import iv
from check_paired_exposure import cells, rates
from check_sequential_exposure import dec

BLOCKS = 80
BLOCK_SIZE = 50_000_000_000_000
SCALE = 10**22


def gaussian_cdf(x):
    # Outside 9 standard deviations, use the Gaussian Mills upper bound.
    if x > 9:
        return iv.mpf([1, 1]) - iv.mpf([0, '0.00000000000000000012'])
    if x < -9:
        return iv.mpf([0, '0.00000000000000000012'])
    term = x
    total = term
    for j in range(1, 190):
        term *= -x*x*(2*j-1)/(2*j*(2*j+1))
        total += term
    # The next integrated exponential term has magnitude below the current one.
    return (iv.mpf('0.5') +
            (total + iv.mpf([-1, 1])*abs(term))/iv.sqrt(2*iv.pi))


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
    live = {0: SCALE}
    error = exposure = 0
    for step in range(1, BLOCKS+1):
        exposure += sum(live.values())
        width = -(-(92*BLOCKS-43*step)//BLOCKS)  # ceil(92-43*step/80)
        if step == BLOCKS:
            # Negative score loses, zero uses a fair coin.
            error += sum(v*(F[-1-s]+F[-s]) for s,v in live.items())//(2*SCALE)+1
            break
        error += sum(v*F[-width-s] for s,v in live.items())//SCALE+1
        live = {y: sum(v*weight[y-s] for s,v in live.items())//SCALE+1
                for y in range(1-width, width)}
    risk = iv.mpf(error)/SCALE + BLOCKS*eps
    pairs = BLOCK_SIZE*(iv.mpf(exposure)/SCALE + BLOCKS*(BLOCKS-1)*eps)
    print('risk upper', float(risk.b), 'mean upper', float(pairs.b))
    assert risk < iv.mpf('0.04986114') and pairs < 2286235020000000


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
