"""Independent exact check of 'One adjacent swap stores the first direction in site parity'.

Written from the note's text only (not from the author's checker). Exact integers and
Fractions; no tolerances. Run:  python3 -I -B own_parity_check.py OUTDIR
The result file is opened with mode 'x' and is never overwritten. Seed 20261113.
A failed predicate does not abort: it is counted and its instance is kept in the file.

Conventions (stated because the note leaves one open):
  rail 0 = R, rail 1 = L. Tick: (u,v) at y -> u+v on (y+1,R), u-v on (y-1,L).
  h = resumed free ticks, t = h+1 native ticks. b = 1 iff physical y = h (mod 2).
  h0(u,v) = (u+v)^2 / (2(u^2+v^2)) is 0/0 at a dark site; the note gives no value there.
  ADDED CONVENTION: 1/2, and every time marker mass meets a dark site under h0 the
  event is counted ("h0_undefined_events"), so the reader sees whether it mattered.
  h_r(y) = 1/2 + u v / sum_{|z-y|<=r} s(z), 1/2 when the sum vanishes (note: r = 1).

PREDICATES, FIXED BEFORE THE FIRST RUN
P1  Line, word oracle. For t = 1..16, D_t(b,x,c) from explicit enumeration of all 2^t
    direction words (sign -1 per L-after-L step). Routed field A_t must satisfy
    A_t(y,c) = D_t(b, y-b, c) with b = [y = h mod 2] at every port of the window
    y in [-t-2, t+3], and {(x+b,c): D} must equal A_t as a map.
P1b Line, tagged-field oracle (two sectors propagated separately), t = 1..300: same.
P1c Left sector on sites of parity h+1, right sector on parity h, supports disjoint,
    t = 1..300.
P2  Ring. Hypothesis: N even and N >= 4. For qualifying N in {4,6,8,10,12,20} and
    t = 1..60: A_t (mod N) equals the wrapped tagged oracle under the parity decoding.
    Non-qualifying N in {2,3,5,7,9} are run too and their outcome is kept (measured).
P3  On-site law, routed launch, t = 1..40: marker mass at every port = A_t^2 / 2^t;
    h0_undefined_events = 0.
P4  Sharp controls, free ticks only. Hypothesis per instance: the field is on sites
    of one parity (tested at launch and at every tick). Predicate: the h0 and h1
    marker distributions are identical at every depth.
    a  single-port launches (0,R), (0,L), depth 40
    b  one-site two-rail launches (u,v) in [-3,3]^2 minus (0,0), depth 20
    c  300 random integer fields on even sites of [-6,6], marker mass = s(y)/sum s,
       depth 16
    f  the blind hold launch (tick, idle slot, free ticks), depth 40
    Measured only (no predicate): d  single-parity field with marker mass placed at
    random sites of either parity (not matching); e  300 random two-parity fields.
P5  Routed detector. t=3: site 2 = (1,1), site 1 = (1,0), site 3 dark; markers of
    both laws identical at t = 1,2,3; every populated site at t = 1,2 has at most one
    nonzero rail; parent mass at site 2 = 1/4; h0 = 1, h1 = 5/6.
    t=4: port (1,L) decodes to (b=1,x=0,L); on-site mass 0; radius-one mass 1/24; raw
    tally 0. For t = 1..40 under both laws the mass on parity-h sites is 1/2 and on
    parity-(h+1) sites is 1/2.
    Measured only: every port at t=4 where the laws differ; total variation by depth.
P6  Depth three. Blind tally at (-1,L) = 0, made of words LRL (+1) and RLL (-1) and
    no others. Routed: (-1,L) = +1, (0,L) = -1, on-site masses 1/8 each, sum 1/4.
P7  Range. Ports moved to (-D,L),(+D,R) by outward swaps; layers = D-1. Hypothesis
    per instance (D,H,r): 2D-2H > r. Predicate: for h <= H the radius-r marker masses
    on the right arm equal those of the right arm alone (same tally 1, mass 1/2), and
    the gap between arm supports is >= 2D-2H. D in 1..8, H in 1..6, r in 0..3.
    Non-qualifying instances are run and kept (measured).
P8  100 random sign splitters (out_R = a u + b v, out_L = c u + d v, signs drawn per
    site and tick), sharp launch, 12 ticks, no swap: all occupied sites on one parity.
"""
import itertools
import json
import random
import sys
from fractions import Fraction as F
from pathlib import Path

SEED = 20261113
R, L = 0, 1


def tick(field, N=None):
    out = {}
    sites = {y for y, _ in field}
    for y in sites:
        u, v = field.get((y, R), 0), field.get((y, L), 0)
        yr, yl = y + 1, y - 1
        if N is not None:
            yr %= N
            yl %= N
        out[(yr, R)] = out.get((yr, R), 0) + u + v
        out[(yl, L)] = out.get((yl, L), 0) + u - v
    return {p: a for p, a in out.items() if a != 0}


def s_of(field, y):
    return field.get((y, R), 0) ** 2 + field.get((y, L), 0) ** 2


def marker_step(field, mass, r, counter, N=None):
    """r = 0 is the on-site law h0 (with the added 1/2 convention), r >= 1 is h_r."""
    out = {}
    for y in sorted({y for y, _ in mass}):
        m = mass.get((y, R), 0) + mass.get((y, L), 0)
        if m == 0:
            continue
        u, v = field.get((y, R), 0), field.get((y, L), 0)
        if r == 0:
            if u == 0 and v == 0:
                counter["h0_undefined_events"] += 1
                frac = F(1, 2)
            else:
                frac = F((u + v) ** 2, 2 * (u * u + v * v))
        else:
            zs = range(y - r, y + r + 1)
            den = sum(s_of(field, z % N if N is not None else z) for z in zs)
            frac = F(1, 2) if den == 0 else F(1, 2) + F(u * v, den)
        assert 0 <= frac <= 1
        yr, yl = y + 1, y - 1
        if N is not None:
            yr %= N
            yl %= N
        out[(yr, R)] = out.get((yr, R), 0) + m * frac
        out[(yl, L)] = out.get((yl, L), 0) + m * (1 - frac)
    return {p: a for p, a in out.items() if a != 0}


def word_oracle(t):
    D = {}
    for w in itertools.product("RL", repeat=t):
        x, rail, amp = 0, R, 1
        for ch in w:
            if ch == "R":
                x += 1
                rail = R
            else:
                x -= 1
                if rail == L:
                    amp = -amp
                rail = L
        key = (1 if w[0] == "R" else 0, x, rail)
        D[key] = D.get(key, 0) + amp
    return {k: a for k, a in D.items() if a != 0}


def routed_start(N=None):
    f = tick({(0, R): 1}, N)
    a, b = (1 % N, R) if N else (1, R), (2 % N, R) if N else (2, R)
    fa, fb = f.get(a, 0), f.get(b, 0)
    g = {p: v for p, v in f.items() if p not in (a, b)}
    if fb:
        g[a] = g.get(a, 0) + fb
    if fa:
        g[b] = g.get(b, 0) + fa
    return g


class Pred:
    def __init__(self, name):
        self.name, self.qualified, self.not_qualified = name, 0, 0
        self.met, self.failed, self.failures = 0, 0, []

    def check(self, ok, info):
        if ok:
            self.met += 1
        else:
            self.failed += 1
            if len(self.failures) < 40:
                self.failures.append(info)

    def dump(self):
        return {"predicate": self.name, "instances_qualifying": self.qualified,
                "instances_not_qualifying": self.not_qualified, "checks_met": self.met,
                "checks_failed": self.failed, "failures_kept": self.failures}


def S(d):
    return {f"{k}": str(v) for k, v in sorted(d.items())}


def single_parity(field):
    return len({y % 2 for y, _ in field}) <= 1


def run():
    rng = random.Random(SEED)
    res, measured = {}, {}

    # ---------------- P1, P1b, P1c
    p1, p1b, p1c = Pred("P1"), Pred("P1b"), Pred("P1c")
    A = routed_start()
    sec = {1: {(1, R): 1}, 0: {(-1, L): 1}}          # tagged sectors after tick one
    for t in range(1, 301):
        h = t - 1
        Dt = {(b, x, c): a for b in (0, 1) for (x, c), a in sec[b].items()}
        oracles = [(p1b, Dt)]
        if t <= 16:
            oracles.append((p1, word_oracle(t)))
            p1.qualified += 1
        p1b.qualified += 1
        for pred, D in oracles:
            pred.check({(x + b, c): a for (b, x, c), a in D.items()} == A, {"t": t, "map": "mismatch"})
            bad = 0
            for y in range(-t - 2, t + 4):
                b = 1 if (y - h) % 2 == 0 else 0
                for c in (R, L):
                    if A.get((y, c), 0) != D.get((b, y - b, c), 0):
                        bad += 1
            pred.check(bad == 0, {"t": t, "ports_wrong": bad})
        p1c.qualified += 1
        left = {x for x, _ in sec[0]}
        right = {x + 1 for x, _ in sec[1]}
        p1c.check(all((y - h - 1) % 2 == 0 for y in left) and all((y - h) % 2 == 0 for y in right)
                  and not (left & right), {"t": t})
        A = tick(A)
        sec = {b: tick(sec[b]) for b in (0, 1)}
    res["P1"], res["P1b"], res["P1c"] = p1.dump(), p1b.dump(), p1c.dump()

    # ---------------- P2 ring
    p2 = Pred("P2")
    ring_measured = {}
    for N in (4, 6, 8, 10, 12, 20, 2, 3, 5, 7, 9):
        qual = N % 2 == 0 and N >= 4
        A = routed_start(N)
        f1 = tick({(0, R): 1}, N)
        sec = {1: {p: a for p, a in f1.items() if p[1] == R}, 0: {p: a for p, a in f1.items() if p[1] == L}}
        first_fail = None
        nfail = 0
        for t in range(1, 61):
            h = t - 1
            wrapped = {}
            for b in (0, 1):
                for (x, c), a in sec[b].items():
                    k = ((x + b) % N, c)
                    wrapped[k] = wrapped.get(k, 0) + a
            wrapped = {k: a for k, a in wrapped.items() if a}
            ok = wrapped == A
            if N % 2 == 0:
                for y in range(N):
                    b = 1 if (y - h) % 2 == 0 else 0
                    for c in (R, L):
                        if A.get((y, c), 0) != sec[b].get(((y - b) % N, c), 0):
                            ok = False
            else:  # no parity on an odd ring: test disjoint site supports of the two sectors
                ok = ok and not ({(x + 1) % N for x, _ in sec[1]} & {x % N for x, _ in sec[0]})
            if qual:
                p2.check(ok, {"N": N, "t": t})
            elif not ok:
                nfail += 1
                first_fail = first_fail or t
            A = tick(A, N)
            sec = {b: tick(sec[b], N) for b in (0, 1)}
        if qual:
            p2.qualified += 1
        else:
            p2.not_qualified += 1
            ring_measured[str(N)] = {"depths_failing_of_60": nfail, "first_failing_depth": first_fail}
    res["P2"] = p2.dump()
    measured["ring_not_qualifying"] = ring_measured

    # ---------------- P3 and P5 (routed launch, both laws)
    p3, p5 = Pred("P3"), Pred("P5")
    cnt0, cnt1 = {"h0_undefined_events": 0}, {"h0_undefined_events": 0}
    A = routed_start()
    m0 = {p: F(1, 2) for p in A}
    m1 = dict(m0)
    p3.qualified = p5.qualified = 1
    tv, dark_port_mass, differ_t4 = {}, {}, {}
    for t in range(1, 41):
        h = t - 1
        p3.check(m0 == {p: F(a * a, 2 ** t) for p, a in A.items()}, {"t": t})
        for name, m in (("h0", m0), ("h1", m1)):
            even = sum(v for (y, c), v in m.items() if (y - h) % 2 == 0)
            p5.check(even == F(1, 2) and sum(m.values()) == 1, {"t": t, "law": name, "parity_h_mass": str(even)})
        if t <= 3:
            p5.check(m0 == m1, {"t": t, "what": "markers agree before the split"})
        if t <= 2:
            p5.check(all(A.get((y, R), 0) == 0 or A.get((y, L), 0) == 0 for y, _ in A), {"t": t, "what": "two rails lit"})
        if t == 3:
            site = lambda y: (A.get((y, R), 0), A.get((y, L), 0))
            p5.check(site(2) == (1, 1), {"t": 3, "site2": site(2)})
            p5.check(site(1) == (1, 0), {"t": 3, "site1": site(1)})
            p5.check(site(3) == (0, 0), {"t": 3, "site3": site(3)})
            p5.check(m0.get((2, R), 0) + m0.get((2, L), 0) == F(1, 4), {"t": 3, "parent": "not 1/4"})
            den = s_of(A, 1) + s_of(A, 2) + s_of(A, 3)
            p5.check(F(1, 2) + F(1 * 1, den) == F(5, 6), {"h1": "not 5/6"})
            p5.check(F((1 + 1) ** 2, 2 * 2) == 1, {"h0": "not 1"})
        if t == 4:
            p5.check((1 - h) % 2 == 0, {"decode": "b not 1"})
            p5.check(m0.get((1, L), 0) == 0, {"t": 4, "onsite(1,L)": str(m0.get((1, L), 0))})
            p5.check(m1.get((1, L), 0) == F(1, 24), {"t": 4, "radius1(1,L)": str(m1.get((1, L), 0))})
            p5.check(A.get((1, L), 0) == 0, {"t": 4, "tally(1,L)": A.get((1, L), 0)})
            for p in sorted(set(m0) | set(m1)):
                if m0.get(p, 0) != m1.get(p, 0):
                    differ_t4[str(p)] = [str(m0.get(p, 0)), str(m1.get(p, 0)), A.get(p, 0)]
        tv[t] = str(sum(abs(m0.get(p, 0) - m1.get(p, 0)) for p in set(m0) | set(m1)) / 2)
        dark_port_mass[t] = str(sum(v for p, v in m1.items() if A.get(p, 0) == 0))
        m0 = marker_step(A, m0, 0, cnt0)
        m1 = marker_step(A, m1, 1, cnt1)
        A = tick(A)
    p3.check(cnt0["h0_undefined_events"] == 0, {"h0_undefined_events": cnt0["h0_undefined_events"]})
    res["P3"], res["P5"] = p3.dump(), p5.dump()
    measured["routed_t4_ports_where_laws_differ [onsite, radius1, raw tally]"] = differ_t4
    measured["routed_total_variation_h0_vs_h1_by_depth"] = tv
    measured["routed_radius1_mass_on_ports_with_zero_tally_by_depth"] = dark_port_mass

    # ---------------- P4 sharp controls
    def compare(field, mass, depth, hold_first=False):
        """returns (qualifies, equal_at_all_depths, first_diff, h0_undefined_events)"""
        c0, c1 = {"h0_undefined_events": 0}, {"h0_undefined_events": 0}
        ma, mb = dict(mass), dict(mass)
        qual, eq, first = single_parity(field), True, None
        for d in range(1, depth + 1):
            ma = marker_step(field, ma, 0, c0)
            mb = marker_step(field, mb, 1, c1)
            field = tick(field)
            if hold_first and d == 1:
                pass  # idle slot: field and both markers held at their ports
            qual = qual and single_parity(field)
            if ma != mb and eq:
                eq, first = False, d
        return qual, eq, first, c0["h0_undefined_events"]

    def family(name, instances, depth, predicate=True, hold_first=False):
        p = Pred(name)
        und = 0
        equal_nonqual = differ_nonqual = 0
        for label, field, mass in instances:
            qual, eq, first, u = compare(field, mass, depth, hold_first)
            und += u
            if qual:
                p.qualified += 1
                p.check(eq, {"instance": label, "first_depth_differing": first})
            else:
                p.not_qualified += 1
                equal_nonqual += eq
                differ_nonqual += (not eq)
        d = p.dump()
        d["h0_undefined_events"] = und
        d["not_qualifying_equal"], d["not_qualifying_differ"] = equal_nonqual, differ_nonqual
        d["depth"] = depth
        if not predicate:
            d["status"] = "measured only"
        return d

    inst_a = [("(0,R)", {(0, R): 1}, {(0, R): F(1)}), ("(0,L)", {(0, L): 1}, {(0, L): F(1)})]
    inst_b = [(f"u={u},v={v}", {k: a for k, a in (((0, R), u), ((0, L), v)) if a}, {(0, R): F(1)})
              for u in range(-3, 4) for v in range(-3, 4) if (u, v) != (0, 0)]

    def rand_field(sites):
        while True:
            f = {(y, c): rng.randint(-3, 3) for y in sites for c in (R, L)}
            f = {p: a for p, a in f.items() if a}
            if f:
                return f

    inst_c = []
    for i in range(300):
        f = rand_field(range(-6, 7, 2))
        tot = sum(a * a for a in f.values())
        inst_c.append((f"c{i}", f, {p: F(a * a, tot) for p, a in f.items()}))
    inst_d = []
    for i in range(300):
        f = rand_field(range(-6, 7, 2))
        ys = [rng.randint(-7, 7) for _ in range(4)]
        m = {}
        for y in ys:
            m[(y, R)] = m.get((y, R), 0) + F(1, 4)
        inst_d.append((f"d{i}", f, m))
    inst_e = []
    for i in range(300):
        f = rand_field(range(-6, 7))
        tot = sum(a * a for a in f.values())
        inst_e.append((f"e{i}", f, {p: F(a * a, tot) for p, a in f.items()}))
    blind = tick({(0, R): 1})
    inst_f = [("blind hold after tick one", blind, {p: F(1, 2) for p in blind})]
    res["P4a"] = family("P4a single-port launches", inst_a, 40)
    res["P4b"] = family("P4b one-site two-rail launches", inst_b, 20)
    res["P4c"] = family("P4c random single-parity fields, matching marker", inst_c, 16)
    res["P4f"] = family("P4f blind hold launch", inst_f, 40)
    measured["P4d single-parity field, marker mass not matching"] = family("P4d", inst_d, 16, predicate=False)
    measured["P4e random fields on both parities (hypothesis violated on purpose)"] = family("P4e", inst_e, 16, predicate=False)

    # ---------------- P6 depth three
    p6 = Pred("P6")
    p6.qualified = 1
    contrib = {}
    for w in itertools.product("RL", repeat=3):
        x, rail, amp = 0, R, 1
        for ch in w:
            if ch == "R":
                x, rail = x + 1, R
            else:
                x -= 1
                amp = -amp if rail == L else amp
                rail = L
        if (x, rail) == (-1, L):
            contrib["".join(w)] = amp
    p6.check(contrib == {"LRL": 1, "RLL": -1}, {"words_into_(-1,L)": contrib})
    B = tick(tick(tick({(0, R): 1})))
    p6.check(B.get((-1, L), 0) == 0, {"blind(-1,L)": B.get((-1, L), 0)})
    A = tick(tick(routed_start()))
    p6.check(A.get((-1, L), 0) == 1 and A.get((0, L), 0) == -1, {"routed": [A.get((-1, L), 0), A.get((0, L), 0)]})
    c = {"h0_undefined_events": 0}
    m = {p: F(1, 2) for p in routed_start()}
    f = routed_start()
    for _ in range(2):
        m = marker_step(f, m, 0, c)
        f = tick(f)
    p6.check(m.get((-1, L), 0) == F(1, 8) and m.get((0, L), 0) == F(1, 8), {"masses": [str(m.get((-1, L), 0)), str(m.get((0, L), 0))]})
    p6.check(m.get((-1, L), 0) + m.get((0, L), 0) == F(1, 4), {"sum": "not 1/4"})
    res["P6"] = p6.dump()

    # ---------------- P7 range
    p7 = Pred("P7")
    nonqual = {"equal": 0, "differ": 0, "examples_differ": []}
    for D in range(1, 9):
        f = tick({(0, R): 1})
        layers = 0
        pos = 1
        while pos < D:   # one layer: (pos,R)->(pos+1,R) and (-pos,L)->(-pos-1,L), disjoint swaps
            f = {((y + 1, c) if c == R else (y - 1, c)): a for (y, c), a in f.items()}
            pos += 1
            layers += 1
        ok_layers = layers == D - 1 and f == {(D, R): 1, (-D, L): 1}
        for H in range(1, 7):
            for r in range(0, 4):
                qual = 2 * D - 2 * H > r
                left, one = {(-D, L): 1}, {(D, R): 1}
                two = dict(f)
                mt, mo = {p: F(1, 2) for p in two}, {(D, R): F(1, 2)}
                c = {"h0_undefined_events": 0}
                same, gap_ok = True, True
                for h in range(0, H + 1):
                    gap = min(y for y, _ in one) - max(y for y, _ in left)
                    if gap < 2 * D - 2 * H:
                        gap_ok = False
                    if {p: mt.get(p, 0) for p in mo} != mo:
                        same = False
                    if h < H:
                        mt = marker_step(two, mt, r, c)
                        mo = marker_step(one, mo, r, c)
                        two, one, left = tick(two), tick(one), tick(left)
                if qual:
                    p7.qualified += 1
                    p7.check(same and gap_ok and ok_layers, {"D": D, "H": H, "r": r, "same": same, "gap_ok": gap_ok, "layers": layers})
                else:
                    p7.not_qualified += 1
                    if same:
                        nonqual["equal"] += 1
                    else:
                        nonqual["differ"] += 1
                        if len(nonqual["examples_differ"]) < 12:
                            nonqual["examples_differ"].append({"D": D, "H": H, "r": r})
    res["P7"] = p7.dump()
    measured["P7 instances with 2D-2H <= r (hypothesis not met)"] = nonqual

    # ---------------- P8 random sign splitters
    p8 = Pred("P8")
    for i in range(100):
        f = {(0, R): 1}
        ok = True
        for _ in range(12):
            out = {}
            for y in {y for y, _ in f}:
                u, v = f.get((y, R), 0), f.get((y, L), 0)
                a, b, c, d = (rng.choice((-1, 1)) for _ in range(4))
                out[(y + 1, R)] = out.get((y + 1, R), 0) + a * u + b * v
                out[(y - 1, L)] = out.get((y - 1, L), 0) + c * u + d * v
            f = {p: x for p, x in out.items() if x}
            ok = ok and single_parity(f)
        p8.qualified += 1
        p8.check(ok, {"instance": i})
    res["P8"] = p8.dump()

    totals = {"checks_met": sum(v["checks_met"] for v in res.values()),
              "checks_failed": sum(v["checks_failed"] for v in res.values())}
    return {"program": "own_parity_check.py", "seed": SEED, "predicates_fixed_in_docstring": True,
            "added_convention": "h0 := 1/2 at a dark site; events counted", "predicates": res,
            "measured_only": measured, "totals": totals}


def main():
    outdir = Path(sys.argv[1])
    out = run()
    outdir.mkdir(parents=True, exist_ok=True)
    with (outdir / "own_parity_result.json").open("x", encoding="utf8", newline="\n") as fh:
        json.dump(out, fh, indent=1)
        fh.write("\n")
    print(json.dumps(out["totals"]))


if __name__ == "__main__":
    main()
