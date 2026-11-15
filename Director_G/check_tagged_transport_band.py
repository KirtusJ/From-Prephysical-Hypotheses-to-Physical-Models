"""Replay the native two-tick filter and terminal position reads on the signed line."""

import cmath
import math
from fractions import Fraction

I = ((1, 0), (0, 1))
X = ((0, 1), (1, 0))
S = ((1, 1), (1, -1))
ROOT2 = math.sqrt(2)


def scaled(a, m):
    return tuple(tuple(a * x for x in row) for row in m)


def added(m, n):
    return tuple(tuple(x + y for x, y in zip(r, s)) for r, s in zip(m, n))


def adj(m):
    return tuple(tuple(z.conjugate() for z in col) for col in zip(*m))


def mul(m, n):
    return tuple(tuple(sum(x * y for x, y in zip(r, c)) for c in zip(*n)) for r in m)


def require(test, message):
    if not test:
        raise ArithmeticError(message)


def close(m, n, tol=5e-12):
    err = max(abs(x-y) for r, s in zip(m, n) for x, y in zip(r, s))
    require(err <= tol, f"matrix residual {err}")


def passing_filter(b):
    # Integer path amplitudes, with a common 1/2 removed per pair.
    rail = {0: (1, 0)}
    for _ in range(b):
        for tick in range(2):
            moved = {}
            for pos, (right, left) in rail.items():
                moved.setdefault(pos+1, [0, 0])[0] += right + left
                moved.setdefault(pos-1, [0, 0])[1] += right - left
            rail = moved
        rail = {pos: (right, 0) for pos, (right, _) in rail.items() if right}
    weights = {pos: right**2 for pos, (right, _) in rail.items()}
    total = math.comb(2*b, b)
    require(rail == {2*j: (math.comb(b, j), 0) for j in range(b+1)}, "filter amplitudes")
    require(sum(weights.values()) == total, "filter yield")
    require(sum(x*p for x, p in weights.items()) == b*total, "prepared centre")
    require(sum((x-b)**2*p for x, p in weights.items())*(2*b-1) == b**2*total, "width")
    return Fraction(total, 4**b)


def tagged_columns(m, tau):
    # A terminal history with m more tau than -tau signs acts by a scalar
    # multiple of this integer matrix. Sum its two squared columns for I/2.
    base = added(scaled(2, I), scaled(tau, S))
    k = I
    for _ in range(m):
        k = mul(base, k)
    square = mul(k, adj(k))
    trace = square[0][0] + square[1][1]
    rho = scaled(Fraction(1, trace), square)
    eta = (1-(3-2*ROOT2)**(2*m))/(1+(3-2*ROOT2)**(2*m))
    close(rho, scaled(0.5, added(I, scaled(tau*eta/ROOT2, S))))
    require(rho[0][0] + rho[1][1] == 1, "normalized conditional rail")
    return k, trace, eta


def fibre(k):
    phase = cmath.exp(-1j*k)
    return ((phase/ROOT2, phase/ROOT2), (phase.conjugate()/ROOT2, -phase.conjugate()/ROOT2))


def speed(k):
    c = math.cos(k)
    return c/math.sqrt(1+c*c)


def projector(k):
    d = math.sqrt(1+math.cos(k)**2)
    c = speed(k)
    off = cmath.exp(-1j*k)/d
    return scaled(0.5, ((1+c, off), (off.conjugate(), 1-c)))


def off_diagonal_solver(k, y):
    p = projector(k)
    cross = mul(mul(p, y), added(I, scaled(-1, p)))
    omega = math.asin(math.sin(k)/ROOT2)
    a = 1/(-cmath.exp(2j*omega)-1)
    term = scaled(a, cross)
    return added(term, adj(term))


def check_fibres():
    for k in [-math.pi, -1.9, -math.pi/2, -0.47, 0, 0.38, math.pi/2, 2.4]:
        u, p = fibre(k), projector(k)
        w = scaled(speed(k), added(scaled(2, p), scaled(-1, I)))
        close(mul(u, p), scaled(cmath.exp(-1j*math.asin(math.sin(k)/ROOT2)), p))
        close(mul(p, p), p)
        eps = 1e-5
        dp = scaled(0.5/eps, added(projector(k+eps), scaled(-1, projector(k-eps))))
        for y, rhs in ((X, added(X, scaled(-1, w))), (dp, dp)):
            c = off_diagonal_solver(k, y)
            close(added(mul(mul(adj(u), c), u), scaled(-1, c)), rhs, 2e-10)
        du = scaled(0.5/eps, added(fibre(k+eps), scaled(-1, fibre(k-eps))))
        diag = scaled(1j, mul(adj(u), du))
        close(diag, X, 3e-10)
    for tau in [-1, 1]:
        kt, tr, _ = tagged_columns(3, tau)
        rho = scaled(1/tr, mul(kt, adj(kt)))
        for k in (-math.pi/2, math.pi/2):
            r = mul(rho, projector(k))
            require(abs(r[0][0]+r[1][1] - 0.5) < 1e-14, "edge retains both bands")


def terminal(b, m, n, h, tau):
    k, tr, eta = tagged_columns(m, tau)
    gnorm = math.sqrt(math.comb(2*b, b)*tr)
    centre = b + tau*sum(speed(-j*h) for j in range(1, n+1))
    # Pad with n physical sites on each side. Each step applies the phase
    # at DEPARTURE, then H, then the +1/-1 shifts; no periodic wrap.
    width = 2*b+2*n+1
    phase = [cmath.exp(-1j*h*(a-n))/ROOT2 for a in range(width)]
    total = mean = sqerr = 0.0
    for rail_col in range(2):
        right, left = [0j]*width, [0j]*width
        for j in range(b+1):
            scalar = math.comb(b, j)/gnorm
            right[n+2*j] = scalar*k[0][rail_col]
            left[n+2*j] = scalar*k[1][rail_col]
        for tick in range(n):
            next_right, next_left = [0j]*width, [0j]*width
            for a in range(n-tick, n+2*b+tick+1, 2):
                next_right[a+1] = phase[a]*(right[a]+left[a])
                next_left[a-1] = phase[a]*(right[a]-left[a])
            right, left = next_right, next_left
        for a, (r, l) in enumerate(zip(right, left)):
            weight = abs(r)**2 + abs(l)**2
            pos = a-n
            total += weight
            mean += weight*pos
            sqerr += weight*((pos-centre)/n)**2
    require(abs(total-1) < 2e-12, "lost terminal position mass")
    width_term = b/math.sqrt(2*b-1)/n
    if h == 0:
        bound = width_term + ROOT2/n + math.sqrt(1-eta+(2*eta-1)/(4*(b+1)))
    else:
        leak = (1-eta)/2 + eta/(4*(b+1))
        bound = width_term+4/n+16*abs(h)+32*n*h*h+math.sqrt(2*leak)+math.pi/(2*math.sqrt(2*b+2))
    rms = math.sqrt(sqerr)
    require(rms <= bound+2e-12, f"terminal error {rms} exceeds {bound}")
    return (mean-b)/n, (centre-b)/n, rms, bound


def main():
    p = Fraction(1)
    first_aborts = []
    for b in range(1, 33):
        next_p = passing_filter(b)
        first_aborts.append(p-next_p)
        p = next_p
        require(sum(first_aborts) + 2*(p/2) == 1, "original-launch accounting")
    check_fibres()
    print("B m N h tau   observed_mean_speed predicted_mean_speed normalized_RMS bound")
    for b, m, n, impulse in ((1, 1, 6, 0), (32, 3, 192, 0), (48, 4, 320, 0.45), (48, 4, 320, 2.4)):
        for h in sorted({impulse/n, -impulse/n}):
            for tau in (1, -1):
                obs, pred, rms, bound = terminal(b, m, n, h, tau)
                print(f"{b} {m} {n} {h:+.6f} {tau:+d} {obs:+.8f} {pred:+.8f} {rms:.8f} {bound:.8f}")


if __name__ == "__main__":
    main()
