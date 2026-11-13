"""Verification for Paired Preparations and Conditional Output Fidelity.
Requires NumPy and mpmath. The examples are algebraic checks, not device trials.
Research direction and responsibility: Kirtus Justus, 7 November 2026.
"""
import numpy as np
import mpmath as mp


def check(condition, description):
    if not condition:
        raise ArithmeticError(description)


def close(actual, expected, description):
    check(np.max(np.abs(np.asarray(actual) - expected)) < 2e-11, description)


def positive_sqrt(state):
    spectrum, eigenvectors = np.linalg.eigh(state)
    check(spectrum.min() >= -1e-11, "nonpositive input")
    return (eigenvectors * np.sqrt(np.maximum(spectrum, 0))) @ eigenvectors.conj().T


def fidelity(x, y):
    return np.linalg.svd(positive_sqrt(x) @ positive_sqrt(y), compute_uv=False).sum()


def choi_weight(kraus):
    return sum(np.linalg.norm(k[::2, ::2] + k[1::2, 1::2])**2 for k in kraus) / 8


def first_output(kraus, column):
    joint = kraus[:, :, column].T @ kraus[:, :, column].conj()
    rate = np.trace(joint).real
    return rate, np.trace(joint.reshape(2, 2, 2, 2), axis1=1, axis2=3) / rate


def witness(rho, sigma, g0, g1):
    """Build purifications attaining root fidelity, and a branch achieving equality."""
    left, right = positive_sqrt(rho), positive_sqrt(sigma)
    u, singular, vh = np.linalg.svd(left @ right)
    right = right @ vh.conj().T @ u.conj().T
    close(np.vdot(left, right), singular.sum(), "purification overlap")
    stinespring = np.zeros((4, 3, 4), dtype=complex)  # output, environment, input
    stinespring[::2, :2, 0] = np.sqrt(g0) * left
    stinespring[1::2, :2, 1] = np.sqrt(g1) * right
    h = (4 - g0 - g1) / 2
    stinespring[0, 2, 2] = stinespring[1, 2, 3] = np.sqrt(h)
    ks = stinespring.transpose(1, 0, 2)
    effect = sum(k.conj().T @ k for k in ks)
    close(effect, np.diag([g0, g1, h, h]), "normalized success effect")
    physical_scale = 1 / np.linalg.eigvalsh(effect).max()
    check(np.linalg.eigvalsh(np.eye(4) - physical_scale * effect).min() > -1e-12, "TNI")
    for col, state, g in [(0, rho, g0), (1, sigma, g1)]:
        rate, first = first_output(ks, col)
        close(rate, g, "relative success")
        close(first, state, "conditional first marginal")
    rhs = g0 + g1 - 2 * np.sqrt(g0 * g1) * fidelity(rho, sigma)
    close(8 * (1 - choi_weight(ks)), rhs, "sharp subspace deficit")
    return choi_weight(ks)


def test_witnesses():
    rho = np.array([[.55, .23j], [-.23j, .45]])
    sigma = np.array([[.23, .12], [.12, .77]])
    for g0, g1 in [(1, 1), (.8, 1.6), (1.5, 2.5), (.02, 1.3)]:
        witness(rho, sigma, g0, g1)
    weight = witness(np.diag([1., 0]), np.diag([0., 1]), .04, .04)
    close(weight, .99, "rare-arm counterexample")
    a, c = .5294729345035379, .96
    lo = 1 - a
    b = (c * np.sqrt(lo) + np.sqrt(1 - c*c) * np.sqrt(1-lo))**2
    weight = witness(np.diag([lo, 1-lo]), np.diag([b, 1-b]), 1, 1)
    close(weight, .99, "trace-distance endpoint")
    close(b-lo, .2729539614530983, "sharp first-marginal distance")
    print("Noncommuting marginal witnesses, TP witness and rare-arm counterexample verified.")


def test_general_branches():
    rng = np.random.default_rng(1341)
    for rank in (1, 2, 5):
        for _ in range(16):
            ks = rng.normal(size=(rank,4,4)) + 1j*rng.normal(size=(rank,4,4))
            ks *= 2 / np.linalg.norm(ks)
            g0, r0 = first_output(ks, 0)
            g1, r1 = first_output(ks, 1)
            rhs = g0 + g1 - 2 * np.sqrt(g0*g1) * fidelity(r0, r1)
            check(8*(1-choi_weight(ks)) + 1e-11 >= rhs, "branch inequality")
            for projector in [np.diag([1,0]), np.array([[.5,-.5j],[.5j,.5]])]:
                rates = [np.trace(r @ projector).real for r in (r0, r1)]
                x,y = np.array([rates[0], 1-rates[0]]), np.array([rates[1], 1-rates[1]])
                deficit = np.sum((np.sqrt(g0*x) - np.sqrt(g1*y))**2)
                check(deficit <= 8*(1-choi_weight(ks))+1e-11, "binary probability test")
    print("48 complex Kraus-array checks and two common effects passed.")


def check_submitted_distance():
    # An independent non-diagonal joint-output fixture.
    i, j = np.indices((4, 4))
    unitary = np.exp(2j * np.pi * i * j / 4) / 2
    spectrum = np.array([.47, .31, .18, .04])
    m = spectrum[0]
    other = unitary @ np.diag([np.sqrt(m), 1., 1., 1.])
    operators = [other]
    for n in range(1, 4):
        jump = np.zeros((4, 4), dtype=complex)
        jump[:, 0] = np.sqrt(spectrum[n]) * unitary[:, n]
        operators.append(jump)
    close(sum(k.conj().T @ k for k in operators), np.eye(4), "TP distance witness")
    state = sum(np.outer(k.ravel(), k.ravel().conj()) for k in operators) / 4
    pure = np.outer(unitary.ravel(), unitary.ravel().conj()) / 4
    expected = (1-m + np.sqrt((1-m)**2 + 12*(1-np.sqrt(m))**2))/8
    close(np.abs(np.linalg.eigvalsh(state-pure)).sum()/2, expected, "distance extremizer")
    close(4*state.reshape(4,4,4,4)[:,0,:,0], unitary @ np.diag(spectrum) @ unitary.conj().T,
          "joint output for distance witness")
    print("Complex joint-output distance extremizer verified.")


def certify_numbers():
    iv = mp.iv
    iv.dps = 58
    s, h, q = iv.mpf(131)/320, iv.mpf(99)/100, iv.mpf(81711338569043)/224995905216000
    a = s + (iv.sqrt(s*h) - iv.sqrt(q))**2/(1-h) + iv.mpf('.06')/13
    c = iv.mpf('.96')
    def cap(x):
        return (c*iv.sqrt(x) + iv.sqrt(1-c*c)*iv.sqrt(1-x))**2
    def enclose(value, lo, hi):
        check(value.a > iv.mpf(lo) and value.b < iv.mpf(hi), "outward enclosure")
    beta = 1 - (iv.sqrt(iv.mpf('3.92'))-1)**2
    m0, old_m1 = a+beta, cap(a+beta)
    t_old = (2+m0+old_m1)/4
    d_min = (1-m0+iv.sqrt((1-m0)**2+12*(1-iv.sqrt(m0))**2))/8
    enclose(old_m1, '.8246170805237347', '.8246170805237348')
    enclose(t_old**2+(1-t_old)**2, '.7428654659689598', '.7428654659689599')
    enclose(d_min, '.1730027896903658', '.1730027896903659')
    a1 = cap(a)
    total = (2+a+a1+iv.mpf('.04'))/4
    enclose(a1, '.7931841836963266', '.7931841836963267')
    enclose(cap(1-a)-(1-a), '.2729539614530982', '.2729539614530983')
    enclose(total**2 + (1-total)**2, '.7321043027225949', '.7321043027225950')
    split = iv.mpf('.022229575038')
    for bound in (cap(a+split), a1+iv.mpf('.04')-split):
        check(bound.b < iv.mpf('.810954608659'), "neighbor joint eigenvalue cap")
    print("Certified caps: local difference 0.272954; neighbor eigenvalue 0.810954608659; Choi purity 0.732104302723.")


if __name__ == "__main__":
    test_witnesses()
    test_general_branches()
    check_submitted_distance()
    certify_numbers()
