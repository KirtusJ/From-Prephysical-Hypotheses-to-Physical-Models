"""Cross-review program for Director_G/Optical_walk_records_and_phase_labels.md.

Written from the note's text only; imports nothing from the author's code.
Exact arithmetic: amplitudes in Z[z]/(z^4+1), probabilities in Q(sqrt2)
(class Q2 below, exact sign and order). Seed 20261113. The result file is
opened with mode 'x' and is never overwritten.

Conventions (stated, because they decide signs): z=exp(i pi/4); launch
(H + L*V)/sqrt2 with L=-i=z^6 for the note's coin; Hadamard H'=h+v, V'=h-v
(unnormalised); at the origin both departures are multiplied by z^j; H
moves to x-1, V to x+1; ten ticks; common factor 2^-11 on squared moduli.
Embedding k in {1,3,5,7}: plate z^(jk), launch z^(6k), same walk.

PREDICATES, fixed before the first run
A1  j=3,k=1 origin amplitudes are H=(-12,-10,0,10), V=(0,10,12,10) in basis 1,z,z^2,z^3.
A2  return weights: 0:9/128, 45:51/128, 90:85/128, 180:85/128 for all k;
    135: 43/128+15r/64 for k=1,7 and 43/128-15r/64 for k=3,5 (r=sqrt2).
A3  total weight is exactly 1 for every (j in 0..7, k).
A4  (measured, no threshold) max |exact - complex128 matrix walk| over sites, j=3,4, k all; reported.
B1  for every k: 180-degree position profile is zero exactly on {-4,+4} among
    even sites -10..10, and the 135-degree profile is >0 on all eleven sites.
B2  site ratios R_x=p0 q_x/(q0 p_x), x!=0: for k=3,5 max = (6061-4142r)/11645,
    attained at x=+2 and x=-2; for k=1,7 max rounds to 1.18601 and min = 0.
B3  2000 seeded random site-efficiency vectors eta_x in {0..20}/20 per k.
    Hypothesis per instance: eta_0>0, sum_{x!=0} eta_x p_x >0, sum_{x!=0} eta_x q_x>0.
    For qualifying instances: O_p/O_q equals the note's displayed convex
    formula exactly and lies in [min R, max R]. Count qualifying/nonqualifying.
B4  mode level (x,pol): p_0H=p_0V and q_0H=q_0V for every k; no mode has
    p=0<q; for k=3,5 max off-origin mode ratio = (3-2r)/5; for k=1,7 it
    rounds to 1.32878.
B5  2000 seeded random mode-efficiency vectors, distinct eta for 0H and 0V.
    Hypothesis as in B3 with centre sum >0. Odds ratio lies in [min,max]
    of mode ratios. Count qualifying.
C1  setting-dependent multiplicative response: eta135_i = c_i*eta180_i with
    c_i in [1,Rc] (2000 seeded instances per Rc in {2,5,25,30}, k=3 and k=1).
    For qualifying instances O_p/O_q <= Rc * (max mode ratio). Also record
    the constructed extremal instance (centre c=Rc, best off mode c=1, all
    efficiency on that mode) and whether it equals Rc*max exactly.
C2  0.871/((3-2r)/5) > 25 (note: 'more than a factor of 25').
D1  from the stored chart extents (phase_defect_data.json, panel '3b inset'):
    centre odds ratio = 537/505; expanded range rounds to 0.871 and 1.299.
E1  (not reported in the note) all plates j=0..7 and both launch signs
    L=z^6,z^2 at ten ticks: return(j,L)=return(-j,conj L) exactly.
E2  (not reported) twelve ticks, j=3: returns for k=1,7 equal, k=3,5 equal,
    and the two pairs differ.
E3  (not reported) reference setting 90 instead of 180: record dark sites
    and the k=3,5 supremum of the site ratio; predicate: supremum < 0.871.
Failed predicates are kept in the result file; follow-ups get new names.
"""
import json, math, random, sys
from fractions import Fraction as F

SEED = 20261113


class Q2:
    __slots__ = ("a", "b")

    def __init__(s, a=0, b=0):
        s.a, s.b = F(a), F(b)

    def __add__(s, o): o = q2(o); return Q2(s.a + o.a, s.b + o.b)
    __radd__ = __add__
    def __sub__(s, o): o = q2(o); return Q2(s.a - o.a, s.b - o.b)
    def __mul__(s, o): o = q2(o); return Q2(s.a*o.a + 2*s.b*o.b, s.a*o.b + s.b*o.a)
    __rmul__ = __mul__
    def __truediv__(s, o):
        o = q2(o); n = o.a*o.a - 2*o.b*o.b
        return s * Q2(o.a/n, -o.b/n)
    def sign(s):
        sa, sb = (s.a > 0) - (s.a < 0), (s.b > 0) - (s.b < 0)
        if sa == sb or sb == 0: return sa
        if sa == 0: return sb
        d = s.a*s.a - 2*s.b*s.b
        return sa * ((d > 0) - (d < 0))
    def __eq__(s, o): o = q2(o); return s.a == o.a and s.b == o.b
    def __lt__(s, o): return (s - o).sign() < 0
    def __le__(s, o): return (s - o).sign() <= 0
    def __gt__(s, o): return (s - o).sign() > 0
    def __ge__(s, o): return (s - o).sign() >= 0
    def __float__(s): return float(s.a) + float(s.b)*math.sqrt(2)
    def __repr__(s): return f"{s.a}+{s.b}r"
    __hash__ = None


def q2(x): return x if isinstance(x, Q2) else Q2(x)


def zmul(p, e):
    p = list(p)
    for _ in range(e % 8):
        p = [-p[3], p[0], p[1], p[2]]
    return tuple(p)

def zadd(p, q): return tuple(a + b for a, b in zip(p, q))
def zsub(p, q): return tuple(a - b for a, b in zip(p, q))

def modsq(p):
    out = [0]*4
    for i, a in enumerate(p):
        for j, b in enumerate(p):
            per, r = divmod((i - j) % 8, 4)
            out[r] += a*b*(-1)**per
    assert out[2] == 0 and out[3] == -out[1]
    return Q2(out[0], out[1])          # z - z^3 = +sqrt2


def walk(plate, launch, ticks=10):
    """returns dict (x,pol)->Z[z] amplitude, pol 0=H,1=V; factor 2^-(ticks+1)/2 omitted"""
    st = {(0, 0): (1, 0, 0, 0), (0, 1): zmul((1, 0, 0, 0), launch)}
    for _ in range(ticks):
        new = {}
        for x in {x for x, _ in st}:
            h = st.get((x, 0), (0,)*4); v = st.get((x, 1), (0,)*4)
            e = plate if x == 0 else 0
            new[(x - 1, 0)] = zmul(zadd(h, v), e)
            new[(x + 1, 1)] = zmul(zsub(h, v), e)
        st = new
    return st


def modes(plate, launch, ticks=10):
    d = F(1, 2**(ticks + 1))
    return {m: modsq(a) * d for m, a in walk(plate, launch, ticks).items()}

def sites(md):
    out = {}
    for (x, _), w in md.items():
        out[x] = out.get(x, Q2()) + w
    return out

def emb(j, k, ticks=10): return modes((j*k) % 8, (6*k) % 8, ticks)


def float_walk(plate, launch, ticks=10):
    z = complex(math.cos(math.pi/4), math.sin(math.pi/4))
    st = {(0, 0): 1/math.sqrt(2), (0, 1): z**launch/math.sqrt(2)}
    for _ in range(ticks):
        new = {}
        for x in {x for x, _ in st}:
            h = st.get((x, 0), 0); v = st.get((x, 1), 0)
            ph = z**plate if x == 0 else 1
            new[(x - 1, 0)] = ph*(h + v)/math.sqrt(2)
            new[(x + 1, 1)] = ph*(h - v)/math.sqrt(2)
        st = new
    out = {}
    for (x, _), a in st.items():
        out[x] = out.get(x, 0) + abs(a)**2
    return out


def main(dest, phase_json):
    rng = random.Random(SEED)
    R = {"seed": SEED, "predicates": {}, "records": {}}
    P, rec = R["predicates"], R["records"]
    r2 = Q2(0, 1)
    KS = (1, 3, 5, 7)

    w = walk(3, 6)
    P["A1"] = dict(ok=(w[(0, 0)] == (-12, -10, 0, 10) and w[(0, 1)] == (0, 10, 12, 10)),
                   H=w[(0, 0)], V=w[(0, 1)])
    exp = {0: Q2(F(9, 128)), 1: Q2(F(51, 128)), 2: Q2(F(85, 128)), 4: Q2(F(85, 128))}
    table, ok = {}, True
    for j in (0, 1, 2, 3, 4):
        for k in KS:
            v = sites(emb(j, k))[0]
            table[f"{45*j},{k}"] = [repr(v), float(v)]
            want = exp[j] if j != 3 else (Q2(F(43, 128), F(15, 64)) if k in (1, 7) else Q2(F(43, 128), F(-15, 64)))
            ok &= (v == want)
    P["A2"] = dict(ok=ok, table=table)
    P["A3"] = dict(ok=all(sum(sites(emb(j, k)).values(), Q2()) == 1 for j in range(8) for k in KS))
    dev = 0.0
    for j in (3, 4):
        for k in KS:
            ex = sites(emb(j, k)); fl = float_walk((j*k) % 8, (6*k) % 8)
            dev = max(dev, max(abs(float(ex[x]) - fl.get(x, 0)) for x in ex))
    P["A4"] = dict(measured_max_abs_deviation=dev, ok=None)

    ev = list(range(-10, 11, 2))
    b1, dark = True, {}
    prof = {}
    for k in KS:
        p, q = sites(emb(3, k)), sites(emb(4, k))
        prof[k] = (p, q)
        dark[k] = [x for x in ev if q.get(x, Q2()) == 0]
        b1 &= dark[k] == [-4, 4] and all(p.get(x, Q2()) > 0 for x in ev)
    P["B1"] = dict(ok=b1, dark_sites_180=dark)

    def ratios(p, q, centre_keys):
        p0 = sum((p[c] for c in centre_keys), Q2()); q0 = sum((q[c] for c in centre_keys), Q2())
        return {m: (p0*q[m])/(q0*p[m]) for m in p if m not in centre_keys and p[m] > 0}, p0, q0

    site_r, b2 = {}, True
    for k in KS:
        rr, _, _ = ratios(*prof[k], [0])
        site_r[k] = rr
        mx = max(rr.values(), key=float); mn = min(rr.values(), key=float)
        assert all(v <= mx and v >= mn for v in rr.values())
        arg = sorted(x for x, v in rr.items() if v == mx)
        rec[f"site_ratios_k{k}"] = {str(x): [repr(v), float(v)] for x, v in sorted(rr.items())}
        if k in (3, 5):
            b2 &= mx == (Q2(6061) - 4142*r2)/11645 and arg == [-2, 2]
        else:
            b2 &= round(float(mx), 5) == 1.18601 and mn == 0
        rec[f"site_max_k{k}"] = [repr(mx), float(mx), arg]
    P["B2"] = dict(ok=b2)

    def trial(p, q, centre, eta_p, eta_q):
        num_p = sum((eta_p[c]*p[c] for c in centre), Q2()); num_q = sum((eta_q[c]*q[c] for c in centre), Q2())
        off = [m for m in p if m not in centre]
        den_p = sum((eta_p[m]*p[m] for m in off), Q2()); den_q = sum((eta_q[m]*q[m] for m in off), Q2())
        if not (num_p > 0 and num_q > 0 and den_p > 0 and den_q > 0):
            return None
        return (num_p/den_p)/(num_q/den_q), den_p, off

    b3 = dict(qualifying=0, nonqualifying=0, formula_fail=0, range_fail=0)
    for k in KS:
        p, q = prof[k]; rr = site_r[k]
        lo, hi = min(rr.values(), key=float), max(rr.values(), key=float)
        for _ in range(2000):
            eta = {x: F(rng.randint(0, 20), 20) for x in ev}
            t = trial(p, q, [0], eta, eta)
            if t is None: b3["nonqualifying"] += 1; continue
            b3["qualifying"] += 1
            val, den_p, off = t
            form = sum((eta[x]*p[x]*rr[x] for x in off), Q2())/den_p
            b3["formula_fail"] += not (val == form)
            b3["range_fail"] += not (lo <= val <= hi)
    b3["ok"] = b3["formula_fail"] == 0 and b3["range_fail"] == 0 and b3["qualifying"] > 0
    P["B3"] = b3

    mode_r, b4, mprof = {}, True, {}
    for k in KS:
        p, q = emb(3, k), emb(4, k)
        mprof[k] = (p, q)
        b4 &= p[(0, 0)] == p[(0, 1)] and q[(0, 0)] == q[(0, 1)]
        b4 &= not any(p[m] == 0 and q[m] > 0 for m in p)
        rr, _, _ = ratios(p, q, [(0, 0), (0, 1)])
        mode_r[k] = rr
        mx = max(rr.values(), key=float)
        assert all(v <= mx for v in rr.values())
        arg = sorted(m for m, v in rr.items() if v == mx)
        rec[f"mode_max_k{k}"] = [repr(mx), float(mx), [list(m) for m in arg]]
        rec[f"mode_zero_p_k{k}"] = [list(m) for m in p if p[m] == 0]
        rec[f"mode_dark_180_k{k}"] = sorted(list(m) for m in q if q[m] == 0)
        if k in (3, 5): b4 &= mx == (Q2(3) - 2*r2)/5
        else: b4 &= round(float(mx), 5) == 1.32878
    P["B4"] = dict(ok=b4)

    b5 = dict(qualifying=0, nonqualifying=0, range_fail=0)
    for k in KS:
        p, q = mprof[k]; rr = mode_r[k]
        lo, hi = min(rr.values(), key=float), max(rr.values(), key=float)
        for _ in range(2000):
            eta = {m: F(rng.randint(0, 20), 20) for m in p}
            t = trial(p, q, [(0, 0), (0, 1)], eta, eta)
            if t is None: b5["nonqualifying"] += 1; continue
            b5["qualifying"] += 1
            b5["range_fail"] += not (lo <= t[0] <= hi)
    b5["ok"] = b5["range_fail"] == 0 and b5["qualifying"] > 0
    P["B5"] = b5

    c1 = dict(qualifying=0, nonqualifying=0, bound_fail=0, extremal={})
    for k in (3, 1):
        p, q = mprof[k]; rr = mode_r[k]
        hi = max(rr.values(), key=float); best = max(rr, key=lambda m: float(rr[m]))
        for Rc in (2, 5, 25, 30):
            worst = 0.0
            for _ in range(2000):
                e180 = {m: F(rng.randint(0, 20), 20) for m in p}
                e135 = {m: e180[m]*(1 + F(rng.randint(0, 100), 100)*(Rc - 1)) for m in p}
                t = trial(p, q, [(0, 0), (0, 1)], e135, e180)
                if t is None: c1["nonqualifying"] += 1; continue
                c1["qualifying"] += 1
                c1["bound_fail"] += not (t[0] <= Rc*hi)
                worst = max(worst, float(t[0]))
            e180 = {m: F(0) for m in p}; e180[(0, 0)] = e180[(0, 1)] = F(1); e180[best] = F(1)
            e135 = dict(e180); e135[(0, 0)] = e135[(0, 1)] = F(Rc)
            t = trial(p, q, [(0, 0), (0, 1)], e135, e180)
            c1["extremal"][f"k{k},Rc{Rc}"] = dict(value=float(t[0]), bound=float(Rc*hi),
                                                  equals_bound=bool(t[0] == Rc*hi), random_max=worst)
    c1["ok"] = c1["bound_fail"] == 0
    P["C1"] = c1
    alt_mode = (Q2(3) - 2*r2)/5; alt_site = (Q2(6061) - 4142*r2)/11645
    P["C2"] = dict(ok=bool(Q2(F(871, 1000))/alt_mode > 25),
                   needed_contrast_mode_low=float(Q2(F(871, 1000))/alt_mode),
                   needed_contrast_site_low=float(Q2(F(871, 1000))/alt_site),
                   needed_contrast_mode_centre=float(Q2(F(537, 505))/alt_mode))

    d = json.load(open(phase_json))
    panel = [x for x in d["digitized_secondary"] if x["panel"] == "3b inset"][0]
    y0, v0, y1, v1 = panel["y_calibration"]
    ext = {r["phase_degrees"]: r["symbol_y_extent"] for r in panel["readings"]}
    def odds(pix):
        pr = v0 + (F(str(y0)) - pix)*F(str(v1 - v0))/(F(str(y0)) - F(str(y1)))
        return pr/(1 - pr)
    a, b = ext[135], ext[180]
    cen = odds(F(a[0] + a[1], 2))/odds(F(b[0] + b[1], 2))
    lo = odds(a[1] + 2)/odds(b[0] - 2); hi = odds(a[0] - 2)/odds(b[1] + 2)
    P["D1"] = dict(ok=(cen == F(537, 505) and round(float(lo), 3) == 0.871 and round(float(hi), 3) == 1.299),
                   extents=ext, centre=str(cen), low=float(lo), high=float(hi))
    pr = F(66, 100); pq = F(5, 8)
    rec["printed135_over_plotted180_odds"] = {
        "0.660": float((pr/(1 - pr))/(pq/(1 - pq))),
        "0.672": float((F(672, 1000)/F(328, 1000))/(pq/(1 - pq))),
        "0.648": float((F(648, 1000)/F(352, 1000))/(pq/(1 - pq)))}

    e1, tab = True, {}
    for L in (6, 2):
        for j in range(8):
            v = sites(modes(j, L))[0]
            tab[f"plate{45*j},launch_z{L}"] = [repr(v), float(v)]
            e1 &= v == sites(modes((-j) % 8, (-L) % 8))[0]
    P["E1"] = dict(ok=e1, returns=tab)
    r12 = {k: sites(emb(3, k, 12))[0] for k in KS}
    P["E2"] = dict(ok=bool(r12[1] == r12[7] and r12[3] == r12[5] and not (r12[1] == r12[3])),
                   returns={k: [repr(v), float(v)] for k, v in r12.items()})
    e3 = {}
    for k in KS:
        p, q = sites(emb(3, k)), sites(emb(2, k))
        rr, _, _ = ratios(p, q, [0])
        mx = max(rr.values(), key=float)
        e3[k] = dict(dark_90=[x for x in ev if q.get(x, Q2()) == 0], max=[repr(mx), float(mx)],
                     argmax=sorted(x for x, v in rr.items() if v == mx), min=float(min(rr.values(), key=float)))
    P["E3"] = dict(ok=bool(all(e3[k]["max"][1] < 0.871 for k in (3, 5))), detail=e3)

    met = sorted(n for n, v in P.items() if v["ok"] is True)
    failed = sorted(n for n, v in P.items() if v["ok"] is False)
    R["summary"] = dict(met=met, failed=failed, measured_only=sorted(n for n, v in P.items() if v["ok"] is None))
    with open(dest, "x") as fh:
        json.dump(R, fh, indent=1, default=str)
    print(json.dumps(R["summary"]))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
