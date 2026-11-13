"""Exact checks of coherent returns, residual ambiguity and calibrated flag readout."""
from itertools import product
from sympy import I, Matrix, Rational, diag, eye, ones, simplify, sqrt, trace, zeros


def require(condition, description):
    if not condition:
        raise ArithmeticError(description)


def same(left, right, description):
    diff = left - right
    if isinstance(diff, Matrix):
        require(diff.applyfunc(simplify) == zeros(*diff.shape), description)
    else:
        require(simplify(diff) == 0, description)


def output(kraus, vector):
    result = zeros(kraus[0].rows)
    for k in kraus:
        out = k * vector
        result += out * out.H
    return result


def weight(kraus, q):
    success = sum(trace(k.H * k) for k in kraus)
    matching = 0
    for k in kraus:
        partial = sum((k[t::q, t::q] for t in range(q)), zeros(k.rows//q, k.cols//q))
        matching += trace(partial.H * partial)
    return simplify(matching / (q * success))


def pair_family():
    tau = [diag(1, 0), diag(Rational(1, 4), Rational(3, 4)), diag(0, 1)]
    x = ones(3, 1) / sqrt(3)
    partial_projection = Matrix([1, 1, 0, 0, 0, 0]) / sqrt(2)
    flat_effect = diag(x * x.H, x * x.H)
    for u, v in product((1, -1, I), repeat=2):
        k0 = diag(1, u / Rational(2), 0).col_join(zeros(3))
        k1 = zeros(3).col_join(diag(0, v * sqrt(3) / 2, 1))
        ks = [k0, k1]
        same(k0.H*k0 + k1.H*k1, eye(3), 'trace preservation')
        for b, t in enumerate(tau):
            basis = eye(3)[:, b]
            same(output(ks, basis), Matrix.diag(*[c * basis*basis.H for c in t.diagonal()]),
                 'complete basis output')
        coherent = output(ks, x)
        y = (partial_projection.H * coherent * partial_projection)[0]
        same(y, abs(1 + u / Rational(2))**2 / 6, 'selected coherent click')
        w = weight(ks, 3)
        same(9*w, 6*y + abs(1 + v*sqrt(3)/2)**2, 'residual contribution')
        same(trace(flat_effect * coherent), w, 'identifying coherent click')
        if u == v and u in (-1, 1):
            same(w, (2 - sqrt(3))/9 if u == -1 else (4+sqrt(3))/9, 'global endpoint')
            same(y, Rational(1, 24) if u == -1 else Rational(3, 8), 'endpoint readout')
    print('Exact three-label basis outputs, coherent clicks, both endpoints and residual width 2*sqrt(3)/9.')


def phase_average():
    # An admissible operation with wrong flags and input-dependent success.
    k = Matrix([[1, 1], [2, 1]]) / 4
    require((eye(2) - k.H*k).is_positive_definite, 'trace nonincrease')
    S = trace(k.H*k)
    D = sum(abs(k[b,b])**2 for b in range(2))
    w = weight([k], 2)
    z = (-1 + sqrt(3)*I)/2
    def flat_y(phase):
        x = Matrix([1, phase])/sqrt(2)
        amplitude = (x.H*k*x)[0]
        return simplify(amplitude.conjugate()*amplitude)
    flat = simplify(sum(flat_y(phase) for phase in (1, z, z.conjugate())) / 3)
    same(4*flat, 2*S*w + S-D, 'cubic phase average')
    signs = (flat_y(1)+flat_y(-1))/2
    require(simplify(4*signs - (2*S*w+S-D)) != 0, 'real-sign control')
    # Check the actual state-ensemble average independently of the identity proof.
    states = [(eye(2)[:, b], Rational(1,6)) for b in range(2)]
    states += [(Matrix([1, phase])/sqrt(2), Rational(2,9)) for phase in (1,z,z.conjugate())]
    unconditional, unweighted_conditional = 0, 0
    for x, probability in states:
        out = output([k], x)
        click = simplify((x.H*out*x)[0])
        unconditional += probability*click
        unweighted_conditional += probability*click/trace(out)
    same(unconditional, S/2*(1+2*w)/3, 'average gate fidelity convention')
    require(simplify(unweighted_conditional - unconditional/(S/2)) != 0, 'success-only averaging control')
    for q in (2, 3, 4):
        # Character differences of ordered pairs must be distinct modulo three.
        seen = set()
        for b, t in product(range(q), repeat=2):
            if b != t:
                exps = tuple((int(j == b)-int(j == t)) % 3 for j in range(q))
                require(exps not in seen, 'phase character alias')
                seen.add(exps)
    print('Cubic phase identity, weighted design and failure of real signs and unweighted postselection verified.')


def calibrated_dual():
    H = Matrix([[3, 1], [1, 3]])/4
    observed = [Matrix([3,5])/8, Matrix([1,3])/4]
    lifted = [H.inv()*state for state in observed]
    matches = Matrix([lifted[0][0], lifted[1][1]])
    same(matches, Matrix([Rational(1,4), 1]), 'calibrated matching masses')
    for sign in (-1, 1):
        amp = Matrix([Rational(1,2),sign])
        X = amp * amp.H
        for b in range(2):
            same(X[b,b], matches[b], 'primal diagonal')
        g = Matrix([1+2*sign, 1+Rational(1,2)*sign])
        require((sign*(diag(*g) - ones(2))).is_positive_semidefinite, 'dual semidefinite bounds')
        dual_value = 0
        for b in range(2):
            y = H.T.inv()*eye(2)[:, b]*g[b]
            same(H.T*y,eye(2)[:,b]*g[b],'dual report coefficients')
            dual_value += y.dot(observed[b])
        same(dual_value, trace(ones(2)*X), 'dual attains primal objective')
        same(dual_value / 4, Rational(1,16) if sign == -1 else Rational(9,16), 'calibrated interval')
    # An X-basis readout cannot be represented by a classical report law on Z populations.
    plus = Matrix([1, 1])/sqrt(2)
    minus = Matrix([1, -1])/sqrt(2)
    same((plus*plus.H).diagonal(), (minus*minus.H).diagonal(), 'same flag populations')
    same(abs((plus.H*plus)[0])**2 - abs((plus.H*minus)[0])**2, 1, 'coherent readout separates')
    print('Calibrated imperfect binary flag: attainable [1/16,9/16], with exact dual certificates.')


if __name__ == '__main__':
    pair_family()
    phase_average()
    calibrated_dual()
