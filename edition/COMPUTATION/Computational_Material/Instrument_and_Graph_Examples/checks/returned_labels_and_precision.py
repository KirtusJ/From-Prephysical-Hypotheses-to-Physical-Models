"""Check returned-label endpoint channels, edge-scale likelihoods and Gibbs distance."""
from itertools import product
import mpmath as mp
import sympy as sp


def require(condition, description):
    if not condition:
        raise ValueError(description)


def matrix_equal(left, right):
    return (left - right).applyfunc(sp.simplify) == sp.zeros(*left.shape)


def operation_checks(operators, q, expected_success):
    """Return normalized projection weight and all label-resolved output matrices."""
    rows, columns = operators[0].shape
    first_out = rows // q
    gram = sum((k.H * k for k in operators), sp.zeros(columns))
    require(matrix_equal(gram, sp.diag(*expected_success)), 'success effect')
    require(all(0 <= s <= 1 for s in expected_success), 'trace nonincrease')
    norm_sum = 0
    for k in operators:
        matches = sum((k[t::q, t::q] for t in range(q)), sp.zeros(first_out, columns // q))
        norm_sum += sp.trace(matches.H * matches)
    weight = sp.simplify(norm_sum / (q * sum(expected_success)))
    blocks = {}
    for i, t in product(range(columns), range(q)):
        parts = [k[t::q, i] for k in operators]
        blocks[i, t] = sum((v * v.H for v in parts), sp.zeros(first_out))
    return weight, blocks


def binary_endpoints():
    D = sp.Rational(1, 2)
    fidelity = sp.Rational(3, 20)
    success = [sp.Rational(5, 16), sp.Rational(13, 36)]
    basis0, basis1 = sp.eye(2).columnspace()
    direction = (3 * basis0 + 4 * basis1) / 5
    expected = {(0, 0): basis0 * basis0.H / 4, (0, 1): basis1 * basis1.H / 16,
                (1, 1): direction * direction.H / 4, (1, 0): basis1 * basis1.H / 9}
    require(expected[0, 0] * expected[1, 1] != expected[1, 1] * expected[0, 0],
            'noncommuting matching blocks')
    for sign in (-1, 1):
        matching, wrong0, wrong1 = (sp.zeros(4, 2) for _ in range(3))
        for o in range(2):
            matching[2*o, 0] = basis0[o] / 2
            matching[2*o+1, 1] = sign * direction[o] / 2
            wrong0[2*o+1, 0] = basis1[o] / 4
            wrong1[2*o, 1] = basis1[o] / 3
        w, blocks = operation_checks([matching, wrong0, wrong1], 2, success)
        require(w == (D + sign * 2 * fidelity) / (2 * sum(success)), 'binary endpoint')
        require(blocks == expected, 'returned-label marginals')
    print('Both analytic endpoints attained with identical noncommuting matching blocks and nonzero error flags.')


def orthogonal_and_incomplete_cases():
    copy = sp.zeros(4, 2)
    copy[0, 0] = copy[3, 1] = 1
    flip = sp.kronecker_product(sp.eye(2), sp.Matrix([[0, 1], [1, 0]])) * copy
    for fraction in (sp.S.Zero, sp.Rational(9, 10), sp.S.One):
        ops = [sp.sqrt(fraction) * copy, sp.sqrt(1 - fraction) * flip]
        w, blocks = operation_checks(ops, 2, [1, 1])
        require(w == fraction / 2, 'orthogonal return law')
        for b in (0, 1):
            require(matrix_equal(blocks[b, 0] + blocks[b, 1], sp.eye(2)[:, b] * sp.eye(2)[b, :]),
                    'orthogonal first marginals')
    for change in (0, 1):
        measured = sp.zeros(4); other = sp.zeros(4)
        measured[:, :2] = copy
        for b in range(2):
            other[b ^ change, 2 + b] = 1
        w, blocks = operation_checks([measured, other], 2, [1] * 4)
        require(w == sp.Rational(3 - 2 * change, 4), 'incomplete coverage')
        require(blocks[0, 0] == sp.diag(1, 0) and blocks[1, 1] == sp.diag(0, 1), 'same tested pair')
    print('Orthogonal return fraction gives w=fraction/2; two untested columns allow full weights 1/4 and 3/4.')


def three_labels():
    omega = (-1 + sp.I * sp.sqrt(3)) / 2
    for phases, expected_w in (([1, 1, 1], sp.Rational(3, 4)), ([1, omega, omega**2], 0)):
        matching = sp.zeros(6, 3)
        wrong = [sp.zeros(6, 3) for _ in range(3)]
        for b in range(3):
            matching[b, b] = sp.sqrt(3) * phases[b] / 2
            wrong[b][3 + (b + 1) % 3, b] = sp.Rational(1, 2)
        w, blocks = operation_checks([matching, *wrong], 3, [1] * 3)
        require(w == expected_w, 'three-label endpoint')
        for b in range(3):
            require(matrix_equal(blocks[b, b], sp.diag(sp.Rational(3, 4), 0)), 'matching block')
            require(blocks[b, (b + 1) % 3] == sp.diag(0, sp.Rational(1, 4)), 'wrong label')
    print('Three labels, fixed joint blocks: matching masses 3/4, both endpoints 0 and 3/4 attained.')


def edge_and_thermal():
    mp.mp.dps = 55
    for ratio in (mp.mpf('0.6'), mp.mpf('1.2'), mp.mpf('3')):
        divergence = mp.quad(lambda x: x * mp.exp(-x) * (-2 * mp.log(ratio) + (ratio - 1) * x),
                             [0, 1, mp.inf])
        require(abs(divergence - 2 * (ratio - 1 - mp.log(ratio))) < mp.mpf('1e-46'),
                'edge divergence from quadrature')
    # Rates 4g, shape 2 per successful scale. 8g times the sum has a chi-square law.
    n = 5
    for g in (mp.mpf(1) / 8, mp.mpf(103)):
        t = mp.mpf('0.73') / g
        gamma_cdf = mp.gammainc(2*n, 0, 4*g*t, regularized=True)
        chi_cdf = mp.gammainc((4*n)//2, 0, (8*g*t)/2, regularized=True)
        require(gamma_cdf == chi_cdf, 'pivot normalization')
    print('Edge-scale likelihood and relative-interval pivot verified.')

    beta = mp.mpf('1.7')
    width = mp.mpf('2.5')
    A = mp.diag([-width/4, width/4])
    def state(H):
        e = mp.expm(-beta * H)
        return e / sum(e[i, i] for i in range(H.rows))
    for V, equality in ((-2*A, True), (mp.matrix([[0, width/2], [width/2, 0]]), False)):
        rho, sigma = state(A), state(A + V)
        vals = mp.eigsy(rho - sigma, eigvals_only=True)
        distance = sum(abs(x) for x in vals) / 2
        gap = mp.tanh(beta * width/4) - distance
        require(abs(gap) < mp.mpf('1e-45') if equality else gap > mp.mpf('1e-5'),
                'Gibbs distance envelope')
    print('Finite Gibbs bound attained by swapped levels; a noncommuting case is strictly inside.')


if __name__ == '__main__':
    binary_endpoints()
    orthogonal_and_incomplete_cases()
    three_labels()
    edge_and_thermal()
