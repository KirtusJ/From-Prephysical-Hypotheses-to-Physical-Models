"""Bound expected checkpoints from the one-step errors of a backward recursion."""
from mpmath import iv
from check_finer_checkpoints import PREVIOUS, WIDTHS, selected_laws
from check_tapered_blocks import SCALE, gaussian_cdf


def expected_checks(table, increments, widths, units):
    blocks = len(widths)+1
    size = 4_000_000_000_000_000//blocks
    mean = sum(p*z for p,z in zip(table,increments))
    variance = sum(p*(z-mean)**2 for p,z in zip(table,increments))
    third = sum(p*abs(z-mean)**3 for p,z in zip(table,increments))
    sd = iv.sqrt(size*variance)
    epsilon = iv.mpf('0.475')*third/(variance*sd)
    radius = 2*max(widths)
    cdf = {}
    for j in range(-radius-1, radius+1):
        x = ((iv.mpf(j)+iv.mpf('0.5'))/units-size*mean)/sd
        interval = gaussian_cdf(x)*SCALE
        cdf[j] = min(SCALE, int(interval.b)+1)
        assert cdf[j]-interval.a < 1300
    weights = {j:cdf[j]-cdf[j-1] for j in range(-radius,radius+1)}
    assert min(weights.values()) >= 0

    # A live score immediately before the last block pays exactly one check.
    values = {s:SCALE for s in range(1-widths[-1],widths[-1])}
    variations = 0
    for i in range(len(widths)-1,-1,-1):
        sequence = [0,*values.values(),0]
        variations += sum(abs(y-x) for x,y in zip(sequence,sequence[1:]))
        prior = widths[i-1] if i else 1
        values = {s:SCALE+sum(weights[y-s]*v for y,v in values.items())//SCALE
                  for s in range(1-prior,prior)}
    center = iv.mpf(values[0])/SCALE
    residual = (epsilon+iv.mpf(1300)/SCALE)*variations/SCALE + iv.mpf(blocks)/SCALE
    return center + iv.mpf([-1,1])*residual


def main():
    iv.dps = 85
    block = 25_000_000_000_000
    for table, increments in selected_laws():
        old = expected_checks(table,increments,PREVIOUS,20)
        new = expected_checks(table,increments,WIDTHS,40)
        assert new.a > old.b and 2*old.a > new.b

        def crossover(a,b):
            return block*(2*a-b)/(b-a)

        low, high = crossover(old.a,new.b), crossover(old.b,new.a)
        print('checks',float(old.a),float(old.b),float(new.a),float(new.b))
        print('crossover',float(low.a),float(high.b))
        assert low > 179696180000 and high < 195420320000


if __name__ == '__main__':
    main()
