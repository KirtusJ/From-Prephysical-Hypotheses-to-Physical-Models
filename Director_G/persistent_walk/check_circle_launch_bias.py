"""Bound the launch polarization from four conditional optical-circle orders."""
from argparse import ArgumentParser
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
from runpy import run_path
import json

import fitz

HERE = Path(__file__).resolve().parent
journal = run_path(str(HERE / 'check_journal_circle_order.py'))
figure, require, orders = journal['figure'], journal['require'], journal['ORDERS']

# For I, X, Y, Z, encode the nonzero entry of each row as a power of i.
PAULI_PHASE = ((0, 0), (0, 0), (3, 1), (0, 2))
REAL, IMAG = (1, 0, -1, 0), (0, 1, 0, -1)


def transfer(t, numerators):
    """Map (1, rx, ry, rz) to Pauli coefficients of B rho B†, using integers."""
    out = []
    for i in range(4):
        coeffs = []
        for j in range(4):
            real = imag = 0
            for k in range(2):
                left = k ^ int(i in (1, 2))
                for e in range(2):
                    right = e ^ int(j in (1, 2))
                    # B's diagonal entries are real and its off-diagonal entries imaginary.
                    phase = (PAULI_PHASE[i][k] + int(left != e) +
                             PAULI_PHASE[j][e] - int(k != right)) % 4
                    weight = numerators[left][e] * numerators[k][right]
                    real += REAL[phase] * weight
                    imag += IMAG[phase] * weight
            require(imag == 0, 'nonreal Pauli coefficient')
            coeffs.append(F(real, 2**(t+2)))  # unitary scale and both factors of 1/2
        out.append(coeffs)
    return out


def transfers():
    walk = figure['walk']
    columns = [walk['launch'](10, j) for j in range(2)]
    by_site = {}
    for t in range(max(row[0] for row in orders)+1):
        if any(row[0] == t for row in orders):
            for m in (0, 4):
                ((a, ai), (cr, c)), ((br, b), (d, di)) = [col[(m-2) % 10] for col in columns]
                require((ai, cr, br, di) == (0, 0, 0, 0), 'unexpected rail phases')
                by_site[t,m] = transfer(t, ((a,b), (c,d)))
        columns = [walk['step'](col, 'Hprime') for col in columns]
    return by_site


def weight_map(by_site, m):
    return [[sum(w*(int(m == hi)-int(m == lo))*by_site[t,m][i][j]
                 for t,lo,hi,w in orders) for j in range(4)] for i in range(4)]


def intensity(by_site, t, m, z):
    state = [row[0] + z*row[3] for row in by_site[t,m]]
    # The test analyzers before the common division by four.
    analyzer = (F(3,2), 0, 0, F(1,2)) if m == 0 else ((3+z)/2, 0, -3*z, F(-1,2))
    return 2*sum(h*p for h,p in zip(analyzer, state))


def coefficients(by_site, t, lo, hi):
    # Both factors are affine in z. Interpolation is an exact polynomial identity.
    def gap(z):
        return intensity(by_site,t,hi,z) - intensity(by_site,t,lo,z)
    zero, plus, minus = (gap(F(z)) for z in (0, 1, -1))
    return zero, (plus-minus)/2, (plus+minus)/2-zero


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('journal_pdf', type=Path)
    args = parser.parse_args()
    require(sha256(args.journal_pdf.read_bytes()).hexdigest() == figure['PDF_SHA'],
            'different journal bytes')
    with fitz.open(args.journal_pdf) as doc:
        band = journal['legend'](doc[7])
        colors = journal['panel_colors'](doc, doc[7])['experiment']
    bands = {key:band(color,4) for key,color in colors.items()}
    gaps = journal['gaps'](bands)
    require(gaps == [F(n,256) for n in (1,8,7,24)], 'display order gaps')
    by_site = transfers()
    eight_times = [[0,0,0,0], [0,2057,0,0], [0,0,1826,-3301], [0,0,1244,1826]]
    for m, sign in ((0,1), (4,-1)):
        actual = weight_map(by_site, m)
        require(all(8*actual[i][j] == sign*eight_times[i][j]
                    for i in range(4) for j in range(4)), 'weighted transfer')
    polys = [coefficients(by_site,t,lo,hi) for t,lo,hi,_ in orders]
    require(polys == [(0,F(1,8),0), (0,F(17,128),-F(11,32)),
                      (0,F(1,512),-F(67,256)), (0,F(767,32768),F(499,16384))],
            'order polynomials')
    end = F(1,134)
    for intercept, slope, curvature in polys:
        require(intercept == 0 and slope > 0 and slope+curvature*end >= 0, 'open interval signs')
    def pair(t, z):
        return intensity(by_site,t,0,z), intensity(by_site,t,4,z)
    lower, upper = pair(8, end)
    require(lower == upper and pair(8, 2*end)[0] < pair(8, 2*end)[1], 'round-eight crossing')
    require(1+end/2-3*end > 0 and 2+end/2+3*end < 4, 'effect bounds')
    witness = end/2
    for t,lo,hi,_ in orders:
        require(0 < intensity(by_site,t,lo,witness) < intensity(by_site,t,hi,witness),
                'interior positive order')

    a,b = eight_times[2][2:]
    c,d = eight_times[3][2:]
    trace = a*a+b*b+c*c+d*d
    det = a*d-b*c
    # For positive determinant, (s1 ± s2)^2 = trace ± 2 det.
    require(det > 0 and trace-2*det == 2057**2 and trace+2*det == 33994129,
            'singular values')
    total = sum(w*g for (_,_,_,w),g in zip(orders,gaps))
    require(total == F(97557,256), 'weighted display gap')
    print(json.dumps(dict(
        journal_minimum_gaps=list(map(str,gaps)),
        weighted_site_zero_map_times_eight=eight_times,
        unscaled_order_polynomials_constant_linear_quadratic=[list(map(str,p)) for p in polys],
        witness_open_upper_endpoint=str(end),
        witness_order_gaps_with_effects_at_z_1_over_268=[
            str((intensity(by_site,t,hi,witness)-intensity(by_site,t,lo,witness))/4)
            for t,lo,hi,_ in orders],
        lower_block_squared_singular_value_sum=trace, lower_block_determinant=det,
        maximum_score_per_unit_radius='(2057 + sqrt(33994129))/8',
        weighted_minimum_display_gap=str(total)),indent=2))


if __name__ == '__main__':
    main()
