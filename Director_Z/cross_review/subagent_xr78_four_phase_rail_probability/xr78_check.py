"""xr78 cross-review program for Director_G/Four_phase_rail_probability.md.
Written from the note's definitions, not from its checker. Seed 78. Refuses to overwrite.
Revision 1: the first run crashed in P2 before writing any result (probabilities of general
panels lie in Q(sqrt2), my rational() raised); only the number type was changed (class R2),
no predicate or prediction. The crashed version is kept as xr78_check_v0_crashed.py.

PREDICATES (fixed before the first run; predictions in brackets).
Exact (Fractions, or the field Q(zeta_8) for spinors; ranks computed mod p = 2^61-1,
which gives rank_Q >= rank_p; upper bounds on rank come from the analytic null space).

P1  Ten-tick panel, alpha = pi/4, spinors in Q(zeta_8), ticks U_k = D(zeta^k) H:
    all four words have 10 ticks; |psi_R|^2 = (1,3/4,1/2,3/4); z = (1,1/2,0,1/2);
    density matrices rho0+rho2 == rho1+rho3 (the four points are a square: HYPOTHESIS);
    Born pair means 3/4,3/4; cubic pair means 3/4, 9/16; discrepancy 3/16.
P2  (not in the note) All 64 panels A = H D(a pi/4) H, V = H D(b pi/4) H, a,b in 0..7:
    hypothesis rho0+rho2 == rho1+rho3 tested per panel, number qualifying reported;
    for each qualifying panel the Born discrepancy is 0. Cubic discrepancies listed;
    [prediction: nonzero cubic discrepancy only when a is odd].
P3  Clifford null: every word of <= 6 ticks with phases in quarter turns (k even) from R
    has z in {-1,0,1}, hence cubic == Born on it. With eighth phases some word has
    z outside {-1,0,1}. [prediction: true, true]
P4  Square geometry of eq (1): for a = z, |u| = c^2 with rational c from Pythagorean
    pairs, both signs b: quarter turns about n (n.(b a) = c) starting at b a give axial
    coordinates (b, u, 2u-b, u) exactly.
P5  Degrees surviving the square condition. Function space = polynomials of degree <= Dg
    restricted to the sphere (dimension (Dg+1)^2). Defect functional on a square:
    f(s0)+f(s2)-f(s1)-f(s3). N random rational squares (rational axis n, rational s0,
    exact quarter turns); hypothesis per square: |s_j|=1 all j, s0+s2 == s1+s3,
    s0.n == s1.n; number qualifying reported.
    P5a all squares: nullity == 4 for Dg = 8 and Dg = 10 (10 not in the note). [4, 4]
    P5b squares on great circles only (s0 perpendicular to n): nullity [37 for Dg=8,
        56 for Dg=10] i.e. every odd function plus constants survives: NON-affine survivors.
    P5c squares about the single axis z only: nullity [61 for Dg=8] (all components
        with m not = 2 mod 4 survive).
    P5d per degree l = 0..8: harmonic projection basis; number of the 2l+1 real harmonics
        of degree l whose defect vanishes on all sampled squares [3 of 3 for l=1, 1 of 1 for
        l=0, and 0 nontrivial combination for l>=2: nullity within degree l is 0].
P6  Constants of eq (3): int_{-1}^{1} |1+3u| du / 2 == 5/3; int (1+3u)/2 == 1;
    int (1+3u) u /2 == 1.
P7  Stability constant (floating point, grid). For F = P_l(z), l = 2..8: fit is 0 so the
    departure is sup|P_l| = 1; eps_grid = max over a grid of squares of the pair-mean
    difference. eps_grid <= true eps, so 1/eps_grid >= true ratio: if 1/eps_grid <= 10/3
    the bound holds for that F. Predicate: ratio_upper <= 10/3 for each l (a failure is
    a candidate violation and is kept). No tolerance is used: the inequality is one-sided
    and the grid error only makes the test harder to pass.
    Also recorded (analytic, not a predicate): F = affine + c 1_{p} gives departure c
    and eps = c/2, ratio 2; so the best constant lies in [2, 10/3].
P8  Tilted affine detector: w.z = 1-2 eta gives endpoint error eta and |w-z|^2/4 == eta,
    for eta in several rationals. Post-selection 5/6 and biased switch (7/8, 3/4).
P9  Dyadic orbit identity under (2): for u = m/64, the cubic detector's departure from
    the Born line equals sum_j 2^-j defect_j exactly, orbit ends at +-1.
"""
import sys, json, random, itertools, math
from fractions import Fraction as Q
from pathlib import Path

SEED = 78
P = (1 << 61) - 1
results = {"seed": SEED, "predicates": []}


def record(name, qualifying, passed, failed, detail=None):
    results["predicates"].append(dict(name=name, qualifying=qualifying, passed=passed,
                                      failed=failed, detail=detail))


# ---------- Q(zeta_8): a0 + a1 z + a2 z^2 + a3 z^3, z^4 = -1 ----------
class Z8:
    __slots__ = ("c",)

    def __init__(self, c):
        self.c = tuple(Q(x) for x in c)

    def __add__(self, o):
        return Z8([a + b for a, b in zip(self.c, o.c)])

    def __sub__(self, o):
        return Z8([a - b for a, b in zip(self.c, o.c)])

    def __mul__(self, o):
        r = [Q(0)] * 4
        for i, a in enumerate(self.c):
            for j, b in enumerate(o.c):
                k = i + j
                if k >= 4:
                    r[k - 4] -= a * b
                else:
                    r[k] += a * b
        return Z8(r)

    def conj(self):
        a0, a1, a2, a3 = self.c
        return Z8([a0, -a3, -a2, -a1])

    def __eq__(self, o):
        return self.c == o.c

    def rational(self):
        if any(self.c[1:]):
            raise ArithmeticError("not rational")
        return self.c[0]


def zpow(k):
    k %= 8
    c = [0, 0, 0, 0]
    c[k % 4] = 1 if k < 4 else -1
    return Z8(c)


INV_SQRT2 = Z8([0, Q(1, 2), 0, Q(-1, 2)])  # (zeta - zeta^3)/2
assert INV_SQRT2 * INV_SQRT2 == Z8([Q(1, 2), 0, 0, 0])


def tick(psi, k):
    """U_k = D(zeta^k) H on (R, L) amplitudes."""
    a, b = psi
    return (INV_SQRT2 * (a + b), zpow(k) * INV_SQRT2 * (a - b))


def run(word):
    psi = (Z8([1, 0, 0, 0]), Z8([0, 0, 0, 0]))
    for k in word:
        psi = tick(psi, k)
    return psi


def rho(psi):
    a, b = psi
    return (a * a.conj(), a * b.conj(), b * a.conj(), b * b.conj())


def pR(psi):
    """|psi_R|^2 as a real number: Fraction if rational, else string 'p+q*sqrt2' (Q(sqrt2))."""
    return real(psi[0] * psi[0].conj())


def real(v):
    a0, a1, a2, a3 = v.c
    if a2 != 0 or a1 != -a3:
        raise ArithmeticError("not real")
    return R2(a0, a1)


class R2:
    """a + b sqrt2, exact."""
    def __init__(self, a, b=0):
        self.a, self.b = Q(a), Q(b)

    def _c(self, o):
        return o if isinstance(o, R2) else R2(o)

    def __add__(self, o):
        o = self._c(o); return R2(self.a + o.a, self.b + o.b)
    __radd__ = __add__

    def __sub__(self, o):
        o = self._c(o); return R2(self.a - o.a, self.b - o.b)

    def __rsub__(self, o):
        return self._c(o) - self

    def __mul__(self, o):
        o = self._c(o); return R2(self.a * o.a + 2 * self.b * o.b, self.a * o.b + self.b * o.a)
    __rmul__ = __mul__

    def __truediv__(self, k):
        return R2(self.a / k, self.b / k)

    def __pow__(self, n):
        r = R2(1)
        for _ in range(n):
            r = r * self
        return r

    def __eq__(self, o):
        o = self._c(o); return self.a == o.a and self.b == o.b

    def __hash__(self):
        return hash((self.a, self.b))

    def __repr__(self):
        return str(self.a) if self.b == 0 else "%s+%s*sqrt2" % (self.a, self.b)


def panel(a, b):
    """A = H D_a H (ticks 0,0,a,0), phase j (ticks 0,2j), V = H D_b H (ticks 0,0,b,0)."""
    words = [[0, 0, a, 0] + [0, 2 * j] + [0, 0, b, 0] for j in range(4)]
    psis = [run(w) for w in words]
    rr = [rho(p) for p in psis]
    square = all((rr[0][i] + rr[2][i]) == (rr[1][i] + rr[3][i]) for i in range(4))
    probs = [pR(p) for p in psis]
    z = [2 * p - 1 for p in probs]
    cubic = [(1 + x ** 3) / 2 for x in z]
    return dict(words=words, square=square, born=probs, z=z, cubic=cubic,
                born_disc=(probs[0] + probs[2]) / 2 - (probs[1] + probs[3]) / 2,
                cubic_disc=(cubic[0] + cubic[2]) / 2 - (cubic[1] + cubic[3]) / 2)


def p1():
    r = panel(1, -1)
    checks = dict(
        ten_ticks=all(len(w) == 10 for w in r["words"]),
        square_hypothesis=r["square"],
        born=r["born"] == [1, Q(3, 4), Q(1, 2), Q(3, 4)],
        z=r["z"] == [1, Q(1, 2), 0, Q(1, 2)],
        born_means=[(r["born"][0] + r["born"][2]) / 2, (r["born"][1] + r["born"][3]) / 2] == [Q(3, 4)] * 2,
        cubic=r["cubic"] == [1, Q(9, 16), Q(1, 2), Q(9, 16)],
        cubic_disc=r["cubic_disc"] == Q(3, 16))
    f = [k for k, v in checks.items() if not v]
    record("P1 ten-tick panel", 1 if r["square"] else 0, len(checks) - len(f), f,
           dict(born=r["born"], cubic=r["cubic"], cubic_disc=r["cubic_disc"]))


def p2():
    qual = passed = 0
    failed, cub = [], {}
    for a in range(8):
        for b in range(8):
            r = panel(a, b)
            if not r["square"]:
                continue
            qual += 1
            if r["born_disc"] == 0:
                passed += 1
            else:
                failed.append((a, b, str(r["born_disc"])))
            cub["a%d,b%d" % (a, b)] = r["cubic_disc"]
    nonzero = sorted(k for k, v in cub.items() if v != 0)
    pred = all((int(k[1]) % 2 == 1) for k in nonzero)
    record("P2 64 panels: Born discrepancy 0 on every qualifying square", qual, passed, failed,
           dict(cubic_nonzero_count=len(nonzero), cubic_values=sorted(set(str(v) for v in cub.values())),
                prediction_nonzero_only_for_odd_a=pred,
                cubic_zero_with_odd_a=sorted(k for k, v in cub.items() if v == 0 and int(k[1]) % 2 == 1)))


def p3():
    bad, n = [], 0
    for L in range(0, 7):
        for w in itertools.product((0, 2, 4, 6), repeat=L):
            n += 1
            z = 2 * pR(run(w)) - 1
            if not any(z == t for t in (-1, 0, 1)):
                bad.append((w, str(z)))
    record("P3a quarter-phase words <=6 ticks have z in {-1,0,1}", n, n - len(bad), bad[:20])
    found = None
    for L in range(0, 6):
        for w in itertools.product(range(8), repeat=L):
            z = 2 * pR(run(w)) - 1
            if not any(z == t for t in (-1, 0, 1)):
                found = (w, str(z))
                break
        if found:
            break
    record("P3b some eighth-phase word has z outside {-1,0,1}", 1, 1 if found else 0,
           [] if found else ["none found up to 5 ticks"], dict(first=found))


# ---------- vectors ----------
def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def quarter(n, v):
    d = dot(n, v)
    c = cross(n, v)
    return tuple(d * n[i] + c[i] for i in range(3))


def rat_unit(rng):
    t, s = Q(rng.randint(-40, 40), rng.randint(1, 40)), Q(rng.randint(-40, 40), rng.randint(1, 40))
    d = t * t + s * s + 1
    return (2 * t / d, 2 * s / d, (t * t + s * s - 1) / d)


def square(n, s0):
    v = [s0]
    for _ in range(3):
        v.append(quarter(n, v[-1]))
    return v


def is_square(n, v):
    return (all(dot(s, s) == 1 for s in v) and dot(n, n) == 1
            and tuple(a + b for a, b in zip(v[0], v[2])) == tuple(a + b for a, b in zip(v[1], v[3]))
            and dot(n, v[0]) == dot(n, v[1]) and quarter(n, v[3]) == v[0])


def p4():
    qual = ok = 0
    failed = []
    for (p, q, r) in [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29), (4, 3, 5), (12, 5, 13)]:
        for b in (1, -1):
            c = Q(p, r)
            u = b * c * c
            n = (Q(q, r), Q(0), b * c)  # n.(b z) = c
            v = square(n, (Q(0), Q(0), Q(b)))
            if not is_square(n, v):
                continue
            qual += 1
            zc = [s[2] for s in v]
            if zc == [b, u, 2 * u - b, u]:
                ok += 1
            else:
                failed.append((str(c), b, [str(x) for x in zc]))
    record("P4 axial coordinates (b,u,2u-b,u)", qual, ok, failed)


# ---------- rank mod p ----------
def fmod(x):
    return x.numerator % P * pow(x.denominator % P, P - 2, P) % P


def monos(Dg):
    return [(i, j, k) for k in (0, 1) for i in range(Dg + 1) for j in range(Dg + 1 - i) if i + j + k <= Dg]


def row(v, basis, Dg):
    r = [0] * len(basis)
    for sgn, s in zip((1, -1, 1, -1), v):
        x, y, z = (fmod(t) for t in s)
        px = [1]
        py = [1]
        for _ in range(Dg):
            px.append(px[-1] * x % P)
            py.append(py[-1] * y % P)
        for idx, (i, j, k) in enumerate(basis):
            val = px[i] * py[j] % P
            if k:
                val = val * z % P
            r[idx] = (r[idx] + sgn * val) % P
    return r


def rank_mod(rows):
    rows = [r[:] for r in rows]
    rank = 0
    ncol = len(rows[0])
    for col in range(ncol):
        piv = next((i for i in range(rank, len(rows)) if rows[i][col]), None)
        if piv is None:
            continue
        rows[rank], rows[piv] = rows[piv], rows[rank]
        inv = pow(rows[rank][col], P - 2, P)
        pr = [x * inv % P for x in rows[rank]]
        rows[rank] = pr
        for i in range(len(rows)):
            if i != rank and rows[i][col]:
                f = rows[i][col]
                ri = rows[i]
                rows[i] = [(a - f * b) % P for a, b in zip(ri, pr)]
        rank += 1
    return rank


def make_squares(rng, N, kind):
    out, tried = [], 0
    while len(out) < N:
        tried += 1
        if kind == "all":
            n, s0 = rat_unit(rng), rat_unit(rng)
        elif kind == "zaxis":
            n, s0 = (Q(0), Q(0), Q(1)), rat_unit(rng)
        else:  # great circle: s0 perpendicular to n, rational: s0 = normalised cross is not
            # rational in general; use n = quarter-turn image construction instead:
            a = rat_unit(rng)
            # rotate the equatorial square (1,0,0),(0,1,0),.. by the rational rotation
            # taking z to a (Householder composed with a reflection in z)
            w = (a[0], a[1], a[2] - 1)
            ww = dot(w, w)
            if ww == 0:
                continue
            def rot(v, w=w, ww=ww):
                v = (v[0], v[1], -v[2])
                d = 2 * dot(w, v) / ww
                return tuple(v[i] - d * w[i] for i in range(3))
            th = Q(rng.randint(-30, 30), rng.randint(1, 30))
            e = ((1 - th * th) / (1 + th * th), 2 * th / (1 + th * th), Q(0))
            n, s0 = rot((Q(0), Q(0), Q(1))), rot(e)
            n = tuple(-x for x in n) if dot(cross(rot((Q(1), Q(0), Q(0))), rot((Q(0), Q(1), Q(0)))), n) < 0 else n
        v = square(n, s0)
        if is_square(n, v) and (kind != "great" or dot(n, s0) == 0):
            out.append(v)
    return out, tried


def p5(rng):
    for Dg, N in ((8, 260), (10, 320)):
        basis = monos(Dg)
        dim = len(basis)
        assert dim == (Dg + 1) ** 2
        for kind, pred in (("all", 4), ("great", {8: 37, 10: 56}[Dg]), ("zaxis", {8: 61, 10: None}[Dg])):
            sq, tried = make_squares(rng, N, kind)
            rk = rank_mod([row(v, basis, Dg) for v in sq])
            nul = dim - rk
            ok = (pred is None) or nul == pred
            record("P5 Dg=%d squares=%s nullity (predicted %s)" % (Dg, kind, pred), len(sq),
                   1 if ok else 0, [] if ok else ["nullity %d" % nul],
                   dict(dim=dim, rank_mod_p=rk, nullity=nul, generated=tried))
    # P5d: per degree, restrict to harmonic polynomials of exact degree l (kernel of Laplacian
    # on homogeneous polynomials), evaluated on the squares.
    sq, _ = make_squares(rng, 120, "all")
    per = {}
    fails = []
    for l in range(0, 9):
        hom = [(i, j, l - i - j) for i in range(l + 1) for j in range(l + 1 - i)]
        index = {m: t for t, m in enumerate(hom)}
        # Laplacian matrix: hom degree l -> hom degree l-2
        low = [(i, j, l - 2 - i - j) for i in range(l - 1) for j in range(l - 1 - i)] if l >= 2 else []
        lidx = {m: t for t, m in enumerate(low)}
        lap = [[0] * len(hom) for _ in low]
        for m, t in index.items():
            for ax in range(3):
                if m[ax] >= 2:
                    mm = list(m)
                    mm[ax] -= 2
                    lap[lidx[tuple(mm)]][t] = (lap[lidx[tuple(mm)]][t] + m[ax] * (m[ax] - 1)) % P
        ev = []
        for v in sq:
            r = [0] * len(hom)
            for sgn, s in zip((1, -1, 1, -1), v):
                x, y, z = (fmod(t) for t in s)
                for t, (i, j, k) in enumerate(hom):
                    r[t] = (r[t] + sgn * pow(x, i, P) * pow(y, j, P) * pow(z, k, P)) % P
            ev.append(r)
        rl = rank_mod(lap) if lap else 0
        harm_dim = len(hom) - rl
        rboth = rank_mod(lap + ev)
        surv = len(hom) - rboth  # harmonic polynomials of degree l with zero defect on all squares
        per[l] = dict(harmonic_dim=harm_dim, surviving_dim=surv)
        want = harm_dim if l <= 1 else 0
        if harm_dim != 2 * l + 1 or surv != want:
            fails.append((l, harm_dim, surv))
    record("P5d per-degree survivors l=0..8 (predicted 1,3,0,0,0,0,0,0,0)", len(sq), 9 - len(fails), fails, per)


def p6():
    # exact piecewise integrals
    def I(lo, hi, c0, c1):  # int (c0 + c1 u)
        return c0 * (hi - lo) + c1 * (hi * hi - lo * lo) / 2
    absint = (-I(Q(-1), Q(-1, 3), Q(1), Q(3)) + I(Q(-1, 3), Q(1), Q(1), Q(3))) / 2
    m0 = I(Q(-1), Q(1), Q(1), Q(3)) / 2
    m1 = (Q(1) * 0 + Q(3) * Q(2, 3)) / 2  # int (u + 3u^2) = 0 + 2
    checks = dict(abs_mean=absint == Q(5, 3), m0=m0 == 1, m1=m1 == 1)
    f = [k for k, v in checks.items() if not v]
    record("P6 constants of eq (3)", 1, 3 - len(f), f, dict(abs_mean=absint, ten_thirds=2 * absint))


def p7():
    import numpy as np
    from numpy.polynomial import legendre
    th = np.linspace(0, math.pi, 181)[:, None, None]      # axis tilt from z
    c0 = np.linspace(-1, 1, 201)[None, :, None]            # latitude of square about n
    ph = np.linspace(0, math.pi / 2, 91)[None, None, :]
    A = c0 * np.cos(th)
    B = np.sqrt(np.clip(1 - c0 ** 2, 0, None)) * np.sin(th)
    out, fails = {}, []
    for l in range(2, 9):
        co = [0] * l + [1]
        f = lambda z: legendre.legval(z, co)
        d = (f(A + B * np.cos(ph)) + f(A - B * np.cos(ph)) - f(A - B * np.sin(ph)) - f(A + B * np.sin(ph))) / 2
        eps = float(np.abs(d).max())
        ratio = 1.0 / eps
        out[l] = dict(eps_grid=eps, ratio_upper=ratio)
        if not ratio <= 10 / 3:
            fails.append((l, ratio))
    out["point_perturbation"] = "F = affine + c*1_{p}: departure c, eps = c/2, ratio 2 (analytic)"
    record("P7 stability ratio <= 10/3 for P_l, l=2..8 (float grid, one-sided)", 7, 7 - len(fails), fails, out)


def p8():
    fails, n = [], 0
    for eta in (Q(1, 100), Q(9, 25), Q(1, 8), Q(1, 2), Q(3, 1000)):
        n += 1
        wz = 1 - 2 * eta
        Fz, Fm = (1 + wz) / 2, (1 - wz) / 2
        d2 = (2 - 2 * wz) / 4  # |w - z|^2 / 4
        if not (1 - Fz == eta and Fm == eta and d2 == eta):
            fails.append(str(eta))
    born = [1, Q(3, 4), Q(1, 2), Q(3, 4)]
    post = (born[0] * 1 + born[2] * Q(1, 2)) / (1 + Q(1, 2))
    biased = [Q(3, 4) * born[0] + Q(1, 4) * born[2], Q(3, 4) * born[1] + Q(1, 4) * born[3]]
    if post != Q(5, 6):
        fails.append("post %s" % post)
    if biased != [Q(7, 8), Q(3, 4)]:
        fails.append("biased %s" % biased)
    record("P8 tilted detector, post-selection 5/6, biased switch", n + 2, n + 2 - len(fails), fails,
           dict(post=post, biased=biased))


def p9():
    fails, n = [], 0
    cub = lambda t: (1 + t ** 3) / 2
    lin = lambda t: (1 + t) / 2
    for m in range(-64, 65):
        u = Q(m, 64)
        n += 1
        t, acc, w, steps = u, Q(0), Q(1), 0
        while abs(t) != 1 and steps < 50:
            b = 1 if t >= 0 else -1
            child = 2 * t - b
            acc += w * (cub(t) - (cub(Q(b)) + cub(child)) / 2)
            w /= 2
            t = child
            steps += 1
        if abs(t) != 1 or acc != cub(u) - lin(u):
            fails.append(str(u))
    record("P9 dyadic orbit identity m/64", n, n - len(fails), fails)


def main():
    out = Path(sys.argv[1])
    rng = random.Random(SEED)
    for fn in (p1, p2, p3, p4, lambda: p5(rng), p6, p7, p8, p9):
        fn()
    bad = [p["name"] for p in results["predicates"] if p["failed"]]
    results["failed_predicates"] = bad
    with out.open("x", encoding="utf8", newline="\n") as fh:
        json.dump(results, fh, indent=1, default=str)
        fh.write("\n")
    for p in results["predicates"]:
        print("%-75s qual=%s pass=%s fail=%s" % (p["name"][:75], p["qualifying"], p["passed"], len(p["failed"])))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
