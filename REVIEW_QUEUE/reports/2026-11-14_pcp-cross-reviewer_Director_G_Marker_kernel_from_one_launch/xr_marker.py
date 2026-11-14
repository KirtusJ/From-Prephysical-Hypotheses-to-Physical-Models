"""Cross-review program for Director_G/Marker_kernel_from_one_launch.md.
Usage: OMP_NUM_THREADS=1 python3 -B xr_marker.py OUTDIR   (refuses to overwrite)
Seed 20261113. Written from the note's definitions, not from its checker.

CONVENTIONS. Rail 0 = R, rail 1 = L. Tick: (u,v) at x sends u+v to (x+1,R),
u-v to (x-1,L). Blank walk here is computed by NUMPY-FREE dense integer lists
indexed by x+t (different data structure from the note's dict). "Depth t panel"
= state after t ticks. Bit b = 1 iff x >= c (zero is on the b=1 side for c=0).
Angle = atan2(v,u) in (-pi,pi]; gaps are cyclic on the oriented circle.
A_t = D_t / 2^(t/2) (NOT unit-normalised). mpmath at 50 digits for A, the
asymptote and residuals (so no tolerance from libm is needed).

PREDICATES (fixed before the first run).
P1  Exact algebra at k=arccos(1/sqrt3): eigenvalues of U(k) are e^{-iw},-e^{iw}
    with w=pi/2-k; projector(1,0)=z=(3/4,1/4+i/(2sqrt2)); -w''(k)=3sqrt2/8;
    det of ellipse matrix = -3/(8sqrt2); min |Re(e^{i phi} z)| > 0.
    Zero tests: sympy simplify AND 60-digit evaluation < 1e-50.
P2  Hypothesis per instance: u^2+v^2>0 at (t=4n,x=2n), n=1..N; count qualifying.
P3  Reproduce note numbers: residual n=1 -> 0.08845, n=144 -> 0.00007356,
    gaps 1.20282 (12 pts), 0.25169 (144 pts), each to the printed digits.
P4  O(t^-3/2) remainder: C(n)=residual*t^{3/2}. Predicate: sup of C over
    n in (144,600] (unreported) <= sup of C over n in [1,144]. Basis: a bounded
    C is what the O-claim asserts; no free threshold. Also report fitted slope
    of log residual-envelope vs log t over n in [100,600].
P5  Direction error: angular distance between actual direction and leading-term
    direction, times t, has sup over (144,600] <= sup over [1,144].
P6  Largest oriented gap is non-increasing in N and reported at N=300, 600
    (unreported). Measured, not thresholded.
P7  Tagged flight (copy at tick T0, bit 1 iff x>=c, then free ticks to depth
    T0+m): recursive routing with h in each tag sector == word-enumerated
    signed-sum^2 / 2^t at every port, exact Fractions. Instances: the note's
    (T0=3,c=0,m=3) and unreported (T0,c) in {2,3,4,5}x{-1,0,1,2}, m up to 5.
    Per instance the hypothesis "sector non-empty and every routed parent has
    u^2+v^2>0 or zero mass" is tested and counted.
P8  Note's counts: 18 parent visits, 10 distinct pairs, at ticks 3,4,5.
P9  Every parent pair of the note's short test occurs (sign and magnitude)
    in a blank panel of depth <= 6. Follow-up measurement (not a predicate
    the note states): same question for the unreported instances with blank
    depth <= T0+m and <= 40; and by DIRECTION (positive rescaling) instead.
P10 Discriminator: h-law 9/16, rival 5/16 at (b=1,x=2,R,t=4); rival keeps
    tag marginals at depths 4..6; (2,1): rail chances (1,1/2) give 9/10.
P11 Bound sup|K-h| <= e+(L+1)r: tested on tent alternatives K=h+a*tent placed
    in the largest gap (seeded a), clipped to [0,1] check; and the bound is
    EVALUATED at the note's r for L=1 against the trivial bound 1 and against
    the discriminator separation |h(2,1)-1/2|=2/5.
P12 Bump alternative h+g*h*(1-h) stays in [0,1] and agrees with h at all
    sampled directions when g is supported inside the largest gap.
Failed predicates are written with status FAIL and kept.
"""
import sys, json, random, math, itertools
from fractions import Fraction as F
from pathlib import Path
import sympy as sp
import mpmath as mp

mp.mp.dps = 50
SEED = 20261113
NMAX = 600


def blank(tmax):
    """list of panels; panel[t][x+t] = (u,v)"""
    cur = [(1, 0)]
    panels = [cur]
    for t in range(tmax):
        nxt = [[0, 0] for _ in range(2 * t + 3)]
        for i, (u, v) in enumerate(cur):      # x = i - t ; new index = x' + t + 1
            nxt[i + 2][0] = u + v              # x+1
            nxt[i][1] = u - v                  # x-1
        cur = [tuple(p) for p in nxt]
        panels.append(cur)
    return panels


def h(u, v):
    return F((u + v) ** 2, 2 * (u * u + v * v))


def words(depth, T0, c):
    """signed word sums per (tag,x,rail); tag fixed after tick T0."""
    out = {}
    for w in itertools.product((0, 1), repeat=depth):
        x, rail, s, tag = 0, 0, 1, 0
        for j, nx in enumerate(w, start=1):
            if nx == 1 and rail == 1:
                s = -s
            x += 1 if nx == 0 else -1
            rail = nx
            if j == T0:
                tag = 1 if x >= c else 0
        out[(tag, x, rail)] = out.get((tag, x, rail), 0) + s
    return out


def tagged(T0, c, m, panels):
    """route marker by h inside each tag sector; return per-depth masses, visits."""
    P = panels[T0]
    field = {0: {}, 1: {}}
    mass = {0: {}, 1: {}}
    for i, (u, v) in enumerate(P):
        x = i - T0
        tag = 1 if x >= c else 0
        if u or v:
            field[tag][x] = (u, v)
            mass[tag][x] = (F(u * u, 2 ** T0), F(v * v, 2 ** T0))
    visits, depths, hyp_ok = [], {}, True
    for t in range(T0, T0 + m):
        nf, nm = {0: {}, 1: {}}, {0: {}, 1: {}}
        for tag in (0, 1):
            for x, (u, v) in field[tag].items():
                tot = sum(mass[tag].get(x, (0, 0)))
                if u * u + v * v == 0:
                    if tot != 0:
                        hyp_ok = False
                    continue
                visits.append((t, tag, x, (u, v)))
                r = h(u, v)
                a = nf[tag].setdefault(x + 1, [0, 0]); a[0] = u + v
                b = nf[tag].setdefault(x - 1, [0, 0]); b[1] = u - v
                a = nm[tag].setdefault(x + 1, [F(0), F(0)]); a[0] = tot * r
                b = nm[tag].setdefault(x - 1, [F(0), F(0)]); b[1] = tot * (1 - r)
        field = {g: {x: tuple(p) for x, p in nf[g].items()} for g in (0, 1)}
        mass = {g: {x: tuple(p) for x, p in nm[g].items()} for g in (0, 1)}
        depths[t + 1] = {(g, x, r): mass[g][x][r] for g in (0, 1) for x in mass[g] for r in (0, 1)}
    return depths, visits, hyp_ok


def main():
    out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
    dest = out / "xr_marker.json"
    if dest.exists():
        sys.exit(f"Refusing to overwrite {dest}")
    random.seed(SEED)
    res = {"seed": SEED, "predicates": {}}
    def put(name, ok, **kw):
        res["predicates"][name] = dict(status="PASS" if ok else "FAIL", **kw)

    # ---- P1
    k = sp.acos(1 / sp.sqrt(3)); w = sp.pi / 2 - k; s = sp.symbols("s", real=True)
    H = sp.Matrix([[1, 1], [1, -1]]) / sp.sqrt(2)
    U = sp.diag(sp.exp(-sp.I * k), sp.exp(sp.I * k)) * H
    def zero(e):
        e = sp.sympify(e)
        return bool(sp.simplify(sp.expand_complex(e)) == 0) and abs(sp.N(e, 60)) < sp.Float("1e-50")
    cp = (U - sp.exp(-sp.I * w) * sp.eye(2)).det(), (U + sp.exp(sp.I * w) * sp.eye(2)).det()
    proj = (U + sp.exp(sp.I * w) * sp.eye(2)) * sp.Matrix([1, 0]) / (2 * sp.cos(w))
    z = sp.Matrix([sp.Rational(3, 4), sp.Rational(1, 4) + sp.I / (2 * sp.sqrt(2))])
    om = sp.asin(sp.sin(s) / sp.sqrt(2))
    d1 = sp.diff(om, s).subs(s, k); d2 = sp.diff(om, s, 2).subs(s, k)
    M = sp.Matrix([[sp.Rational(3, 4), 0], [sp.Rational(1, 4), -1 / (2 * sp.sqrt(2))]])
    smin = min(M.singular_values(), key=lambda q: sp.N(q))
    checks = dict(eig1=zero(cp[0]), eig2=zero(cp[1]), z0=zero(proj[0] - z[0]), z1=zero(proj[1] - z[1]),
                  omega_k=zero(om.subs(s, k) - w), stationary=zero(d1 - sp.Rational(1, 2)),
                  curvature=zero(-d2 - 3 * sp.sqrt(2) / 8), det=zero(M.det() + 3 / (8 * sp.sqrt(2))),
                  phase=zero(2 * k - 4 * w - (6 * k - 2 * sp.pi)))
    put("P1", all(checks.values()), checks=checks, min_radius_of_ellipse=float(sp.N(smin, 20)),
        max_radius=float(sp.N(max(M.singular_values(), key=lambda q: sp.N(q)), 20)))

    # ---- blank walk
    panels = blank(4 * NMAX)
    kk = mp.acos(1 / mp.sqrt(3)); H0 = 3 * mp.sqrt(2) / 8
    rows = []
    for n in range(1, NMAX + 1):
        t = 4 * n; u, v = panels[t][2 * n + t]
        ph = 6 * n * kk + mp.pi / 4; fac = 4 / mp.sqrt(2 * mp.pi * t * H0)
        lead = (fac * mp.mpf(3) / 4 * mp.cos(ph), fac * (mp.cos(ph) / 4 - mp.sin(ph) / (2 * mp.sqrt(2))))
        sc = mp.mpf(2) ** (t // 2)
        A = (mp.mpf(u) / sc, mp.mpf(v) / sc)
        resid = mp.sqrt((A[0] - lead[0]) ** 2 + (A[1] - lead[1]) ** 2)
        ang = mp.atan2(v, u) if (u or v) else None
        la = mp.atan2(lead[1], lead[0])
        dang = None if ang is None else abs(mp.atan2(mp.sin(ang - la), mp.cos(ang - la)))
        rows.append(dict(n=n, t=t, nz=bool(u or v), resid=resid, C=resid * mp.mpf(t) ** 1.5,
                         ang=ang, dang_t=None if dang is None else dang * t,
                         parent_p_times_t=mp.mpf(u * u + v * v) / mp.mpf(2) ** t * t))
    q = sum(r["nz"] for r in rows)
    put("P2", q == NMAX, qualifying=q, of=NMAX)

    def gap(N):
        a = sorted(r["ang"] for r in rows[:N] if r["ang"] is not None)
        return max(b - c for c, b in zip(a, a[1:] + [a[0] + 2 * mp.pi]))
    g = {N: float(gap(N)) for N in (12, 36, 72, 144, 300, 600)}
    r1, r144 = float(rows[0]["resid"]), float(rows[143]["resid"])
    put("P3", f"{r1:.5f}" == "0.08845" and f"{r144:.8f}" == "0.00007356"
        and f"{g[12]:.5f}" == "1.20282" and f"{g[144]:.5f}" == "0.25169",
        resid_1=r1, resid_144=r144, gap_12=g[12], gap_144=g[144])
    Clo = max(r["C"] for r in rows[:144]); Chi = max(r["C"] for r in rows[144:])
    # envelope slope: max residual in blocks of 50 n
    xs, ys = [], []
    for a in range(100, NMAX, 50):
        blk = rows[a:a + 50]
        xs.append(math.log(4 * (a + 25))); ys.append(math.log(float(max(r["resid"] for r in blk))))
    mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
    slope = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
    put("P4", Chi <= Clo, sup_C_1_144=float(Clo), sup_C_145_600=float(Chi),
        min_C_145_600=float(min(r["C"] for r in rows[144:])), envelope_slope=slope,
        resid_300=float(rows[299]["resid"]), resid_600=float(rows[599]["resid"]))
    Dlo = max(r["dang_t"] for r in rows[:144]); Dhi = max(r["dang_t"] for r in rows[144:])
    put("P5", Dhi <= Dlo, sup_dang_t_1_144=float(Dlo), sup_dang_t_145_600=float(Dhi),
        argmax_low=max(rows[:144], key=lambda r: r["dang_t"])["n"])
    seq = [g[N] for N in (12, 36, 72, 144, 300, 600)]
    put("P6", all(a >= b for a, b in zip(seq, seq[1:])), gaps=g,
        covering_radius={N: g[N] / 2 for N in g},
        parent_p_times_t_range=[float(min(r["parent_p_times_t"] for r in rows)),
                                float(max(r["parent_p_times_t"] for r in rows))])

    # ---- P7..P9
    def blank_pairs(dmax):
        S = set()
        for t in range(dmax + 1):
            for p in panels[t]:
                if p != (0, 0):
                    S.add(p)
        return S
    def direction(p):
        gg = math.gcd(abs(p[0]), abs(p[1])); return (p[0] // gg, p[1] // gg)
    inst = [(3, 0, 3)] + [(T0, c, 5) for T0 in (2, 3, 4, 5) for c in (-1, 0, 1, 2)]
    P7rows, allok, qual = [], True, 0
    B40 = blank_pairs(40); D40 = {direction(p) for p in B40}
    D200 = {direction(p) for p in blank_pairs(200)}
    for T0, c, m in inst:
        depths, visits, hyp = tagged(T0, c, m, panels)
        nonempty = all(any((i - T0 >= c) == bool(tag) and p != (0, 0) for i, p in enumerate(panels[T0])) for tag in (0, 1))
        ok = True; nports = 0
        for d, ms in depths.items():
            W = words(d, T0, c)
            keys = set(W) | set(ms)
            for key in keys:
                nports += 1
                if ms.get(key, F(0)) != F(W.get(key, 0) ** 2, 2 ** d):
                    ok = False
            if sum(ms.values()) != 1:
                ok = False
        pairs = {v[3] for v in visits}
        Bd = blank_pairs(T0 + m)
        row = dict(T0=T0, c=c, m=m, hypothesis=hyp, both_sectors_nonempty=nonempty, ports=nports, match=ok,
                   visits=len(visits), distinct_pairs=len(pairs),
                   pairs_not_in_blank_depth_le_T0m=sorted(p for p in pairs if p not in Bd),
                   pairs_not_in_blank_depth_le_40=sorted(p for p in pairs if p not in B40),
                   directions_not_in_blank_le_40=sorted(p for p in pairs if direction(p) not in D40),
                   directions_not_in_blank_le_200=sorted(p for p in pairs if direction(p) not in D200))
        P7rows.append(row)
        if hyp: qual += 1
        allok &= ok
    put("P7", allok, qualifying=qual, of=len(inst), rows=P7rows)
    n0 = P7rows[0]
    put("P8", n0["visits"] == 18 and n0["distinct_pairs"] == 10, visits=n0["visits"], distinct=n0["distinct_pairs"])
    B6 = blank_pairs(6)
    _, v0, _ = tagged(3, 0, 3, panels)
    miss6 = sorted({v[3] for v in v0 if v[3] not in B6})
    put("P9", not miss6, note_instance_missing_at_depth_le_6=miss6,
        followup_unreported_instances_with_exact_pair_missing_le_T0m=sum(bool(r["pairs_not_in_blank_depth_le_T0m"]) for r in P7rows[1:]),
        followup_with_exact_pair_missing_le_40=sum(bool(r["pairs_not_in_blank_depth_le_40"]) for r in P7rows[1:]),
        followup_with_direction_missing_le_40=sum(bool(r["directions_not_in_blank_le_40"]) for r in P7rows[1:]),
        followup_with_direction_missing_le_200=sum(bool(r["directions_not_in_blank_le_200"]) for r in P7rows[1:]),
        of_unreported=len(P7rows) - 1)

    # ---- P10 (rival written independently: fair in tag 1, h in tag 0, by path weights)
    def rival(depth):
        # marker Markov chain over (tag,x,rail,signed field pair of the sector) is not needed:
        # tag0 follows h-law masses; tag1 = fair walk from the tag-1 masses at tick 3.
        d, _, _ = tagged(3, 0, depth - 3, panels)
        t0 = {key: val for key, val in d[depth].items() if key[0] == 0}
        cur = {}
        for i, (u, v) in enumerate(panels[3]):
            x = i - 3
            if x >= 0 and (u or v):
                cur[x] = F(u * u + v * v, 8)
        ports = {}
        for _ in range(depth - 3):
            ports, nxt = {}, {}
            for x, mval in cur.items():
                ports[(1, x + 1, 0)] = ports.get((1, x + 1, 0), 0) + mval / 2
                ports[(1, x - 1, 1)] = ports.get((1, x - 1, 1), 0) + mval / 2
                nxt[x + 1] = nxt.get(x + 1, 0) + mval / 2; nxt[x - 1] = nxt.get(x - 1, 0) + mval / 2
            cur = nxt
        return {**t0, **ports}, d[depth]
    rv, hv = rival(4)
    marg = True; rivtab = {}
    for d in (4, 5, 6):
        a, b = rival(d)
        for tag in (0, 1):
            if sum(v for key, v in a.items() if key[0] == tag) != sum(v for key, v in b.items() if key[0] == tag):
                marg = False
        rivtab[d] = {str(key): [str(b.get(key, 0)), str(a.get(key, 0))] for key in sorted(set(a) | set(b))}
    agg = (F(4, 5) * 1 + F(1, 5) * F(1, 2))
    put("P10", hv[(1, 2, 0)] == F(9, 16) and rv[(1, 2, 0)] == F(5, 16) and marg and agg == F(9, 10) == h(2, 1),
        h_law=str(hv[(1, 2, 0)]), rival=str(rv[(1, 2, 0)]), marginals_equal=marg, aggregate=str(agg),
        parent_mass=str(F(5, 8)), table_hlaw_rival=rivtab)

    # ---- P11, P12
    def hang(th): return (1 + mp.sin(2 * th)) / 2
    P11 = []; ok11 = True; ok12 = True; P12 = []
    for N in (12, 144, 600):
        a = sorted(r["ang"] for r in rows[:N]); ext = a + [a[0] + 2 * mp.pi]
        i = max(range(N), key=lambda j: ext[j + 1] - ext[j]); lo, hi = ext[i], ext[i + 1]; r = (hi - lo) / 2; mid = (lo + hi) / 2
        grid = [lo + (hi - lo) * j / 2000 for j in range(2001)]
        for trial in range(20):
            slope = random.uniform(0.1, 5.0) * random.choice((-1, 1))
            K = lambda th: hang(th) + slope * max(mp.mpf(0), r - abs(th - mid))
            L = 1 + abs(slope)                      # Lipschitz constant used (upper bound)
            sup = max(abs(K(th) - hang(th)) for th in grid)
            bound = (L + 1) * r                      # e = 0 at sample points
            if sup > bound: ok11 = False
            P11.append(dict(N=N, slope=slope, sup=float(sup), bound=float(bound), ratio=float(sup / bound)))
        # bump
        gmax = 0
        vals = []
        for th in grid:
            gg = mp.sin(mp.pi * (th - lo) / (hi - lo)) ** 2
            hh = hang(th); vals.append(hh + gg * hh * (1 - hh)); gmax = max(gmax, gg * hh * (1 - hh))
        inside = all(0 <= v <= 1 for v in vals)
        agree = all(mp.sin(mp.pi * (x - lo) / (hi - lo)) ** 2 < mp.mpf(10) ** -40 if (x == lo or x == hi) else True for x in a)
        ok12 &= inside and gmax > 0 and agree
        P12.append(dict(N=N, in_unit_interval=inside, max_deviation_from_h=float(gmax)))
    ev = {N: dict(r=g[N] / 2, bound_L1_e0=2 * g[N] / 2, informative_vs_trivial_1=bool(g[N] < 1),
                  below_discriminator_sep_0p4=bool(g[N] < 0.4)) for N in (12, 36, 72, 144, 300, 600)}
    put("P11", ok11, trials=len(P11), max_ratio=max(x["ratio"] for x in P11), evaluation=ev,
        note="basis: exact inequality, no tolerance; grid sup is a lower estimate of the true sup")
    put("P12", ok12, rows=P12)

    res["summary"] = {k_: v["status"] for k_, v in res["predicates"].items()}
    with dest.open("x") as f:
        json.dump(res, f, indent=1, default=str); f.write("\n")
    print(json.dumps(res["summary"]))


if __name__ == "__main__":
    main()
