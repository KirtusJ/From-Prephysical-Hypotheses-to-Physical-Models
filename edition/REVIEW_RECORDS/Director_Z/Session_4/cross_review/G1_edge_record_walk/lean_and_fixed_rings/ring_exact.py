"""Reviewer's own exact-integer program for G1 fixed_ring_calibration.md.

Written by the cross-reviewer (Claude sub-agent), not derived from the author's
checker. Integer arithmetic and fractions only; no floats, no random numbers.

CONVENTIONS (stated before the first run)
  Ring sites 0..N-1. Port = (site x, rail), rail 0 = R, rail 1 = L.
  Launch: D_0(0,R) = 1, every other port 0.
  Step: totals (u,v) at site x send u+v to (x+1 mod N, R) and u-v to (x-1 mod N, L).
  "Occupied" port: total != 0. Zero is on the unoccupied side.
  Panel = all 2N ports of one ring at one tick. Normalized panel under a score f:
  p(port) = f(D)/sum_ports f(D). Two panels are "equal" when every port agrees
  as an exact fraction (cross-multiplied integers).
  square(k) = k*k. rival32(k) = 2*k*k if |k| == 32 else k*k.
  A predicate records pass True/False; a failed predicate is kept in the result
  file, never deleted, and does not stop the run. "measured" items have no
  pass/fail. The result file is opened with mode 'x' (refuses to overwrite).
  Where a predicate is of the form "for all t", the hypothesis that makes it
  non-vacuous is tested and its count reported (field "hypothesis").

PREDICATES (fixed before the first run)
 (a) rings 4 and 8, horizon T = 200
  A1  N=4: D_4 equals 4 * (launch translated by two sites).
  A2  N=4: D_{t+4}(x,r) = 4*D_t(x-2,r) for every port, t = 0..196.
  A3  N=4: each of ticks 0,1,2,3 has exactly one nonzero magnitude.
  A4  N=8: D_24 = 4096 * D_0.
  A5  N=8: D_{t+24} = 4096*D_t for every port, t = 0..176.
  A6  N=8: the ticks in 0..23 at which some port has magnitude 32 are exactly {12,13}.
  A7  N=8: at ticks 12 and 13 the set of nonzero magnitudes is exactly {32}.
  A8  N=8: for t = 24..200 every nonzero total is a multiple of 4096.
  A9  N in {4,8}: normalized panel(square) == normalized panel(rival32) at every
      tick 0..200. Hypothesis: magnitude 32 is actually occupied at some tick <= 200
      on that ring (ticks listed); if not, the predicate is vacuous on that ring.
  A10 N=4: every panel t = 0..200 has exactly one nonzero magnitude.
  A11 N=16: panel(square) != panel(rival32) at tick 13. Measured with it: all ticks
      <= 200 at which the two panels differ on N=16.
 (b) ring 16
  B1  N=16: the fields at ticks 1..13 from local propagation equal the fields from
      enumerating all 2^t signed move words (sign = (-1)^(number of adjacent L,L
      pairs, the launch rail R counting as the move before the first); site =
      (#R - #L) mod N; rail = last move).
  B2  tick 13: square normalizer = 8192.
  B3  tick 13: rival32 normalizer = 10240.
  B4  D_13(7,R) = +32.
  B5  tick 13: exactly two ports have magnitude 32 (ports recorded).
  B6  tick 13: at least one occupied port has magnitude != 32.
  B7  p_13(7,R) = 1/8 under square and 1/5 under rival32.
  B8  p_12(6,R)+p_12(6,L) = 73/512 under square and under rival32.
  B9  p_13(7,R)+p_13(5,L) = 73/512 under square and 137/640 under rival32.
  B10 tick 12: no port has magnitude 32 (hypothesis behind the equal entries of B8).
  B11 square: p_t(x,R)+p_t(x,L) = p_{t+1}(x+1,R)+p_{t+1}(x-1,L) for all x, t = 0..199.
  B12 rival32 violates that identity at (t=12, x=6). Measured with it: every (t,x)
      with t <= 40 where rival32 violates it.
 (c) parity
  C1  N in {4,8,16,32,64}: every total is even at every tick N/2+1 .. 400.
      (N = 64 is a parameter the note and the task do not report.)
  C2  measured: is some total odd at tick N/2 (is the cutoff sharp).
  C3  positive odd totals at ticks 0..N/2: ring 4 -> {1}; ring 8 -> {1,3}.
  C4  rings 4 and 8, ticks 0..400: the positive odd totals reached are exactly
      {1,3}, and +5 is never a signed total.
  C5  N in {3,4,5,6,8,12,16,32}, t = 1..64: D_t(.,R) mod 2 = X*(X+1/X)^(t-1) and
      D_t(.,L) mod 2 = (1/X)*(X+1/X)^(t-1) in F_2[X]/(X^N-1).
  C6  N in {4,8,16,32,64}: (X+1/X)^(N/2) = 0 in F_2[X]/(X^N-1).
  C7  measured: for N in {3,5,6,7,9,10,11,12} the last tick <= 400 with an odd total.
 (d) criterion
  D1  rings {4,8}, ticks 0..200, graph on nonzero signed totals with an edge when two
      totals occur in the same ring at the same tick: the component of +32 is a
      subset of {+32,-32} and does not contain +1; likewise for -32 if visited.
  D2  for every visited signed total v: [score doubled at the single signed value v
      preserves every normalized panel, rings {4,8}, t <= 200]  <=>  [component of v
      is {v}]. Count of v tested and of each side reported.
  D3  sufficiency: a score c_C * k^2 with a different positive rational constant on
      each component C (constant 1 on the component of +1) preserves every panel.
  D4  rings {4,8,16}, ticks 0..200: the component of +32 contains +1.
  D5  measured: magnitudes m visited on rings {4,8}, t <= 200, such that every panel
      containing magnitude m contains only magnitude m (doubling at |m| is then
      invisible on these rings up to the horizon).
 (e) exact parts of the unit-equation argument
  E1  N = 3..12: A^T A = A A^T = 2*I for the raw integer step matrix A (so A is
      normal and every eigenvalue has modulus sqrt 2).
  E5  for 0 <= a <= 800, 0 <= b <= 300, (a,b) != (0,0): 2^a != 9^b.
  E6  measured only: every occurrence of +3^j, j >= 1, as a signed port total on
      rings N = 3..12, ticks 0..400; also counts and last ticks for -3^j and for +1.
"""

import argparse
import json
from fractions import Fraction
from itertools import product
from pathlib import Path

RESULTS = []


def record(pid, statement, passed, detail=None, hypothesis=None):
    row = {"id": pid, "statement": statement, "pass": passed}
    if hypothesis is not None:
        row["hypothesis"] = hypothesis
    if detail is not None:
        row["detail"] = detail
    RESULTS.append(row)


def measured(pid, statement, detail):
    RESULTS.append({"id": pid, "statement": statement, "pass": "measured only", "detail": detail})


def launch(n):
    d = [[0, 0] for _ in range(n)]
    d[0][0] = 1
    return d


def step(d):
    n = len(d)
    new = [[0, 0] for _ in range(n)]
    for x in range(n):
        u, v = d[x]
        new[(x + 1) % n][0] += u + v
        new[(x - 1) % n][1] += u - v
    return new


def fields(n, last):
    out = [launch(n)]
    for _ in range(last):
        out.append(step(out[-1]))
    return out


def square(k):
    return k * k


def rival32(k):
    return 2 * k * k if abs(k) == 32 else k * k


def weights(d, score):
    w = [[score(u), score(v)] for u, v in d]
    return w, sum(a + b for a, b in w)


def panels_equal(d, score_a, score_b):
    wa, za = weights(d, score_a)
    wb, zb = weights(d, score_b)
    if za <= 0 or zb <= 0:
        return False
    return all(wa[x][r] * zb == wb[x][r] * za for x in range(len(d)) for r in (0, 1))


def mags(d):
    return sorted({abs(v) for pair in d for v in pair if v})


def signed_values(d):
    return {v for pair in d for v in pair if v}


def port_name(x, r):
    return f"{x}{'RL'[r]}"


def part_a():
    T = 200
    f4 = fields(4, T)
    f8 = fields(8, T)
    f16 = fields(16, T)
    target = [[0, 0] for _ in range(4)]
    target[2][0] = 4
    record("A1", "N=4: D_4 = 4 * launch translated by two sites", f4[4] == target,
           {"D_4": f4[4]})
    bad = [t for t in range(0, T - 3)
           if any(f4[t + 4][x][r] != 4 * f4[t][(x - 2) % 4][r] for x in range(4) for r in (0, 1))]
    record("A2", "N=4: D_{t+4}(x,r) = 4 D_t(x-2,r), t=0..196", not bad,
           {"ticks_tested": T - 3, "failing_ticks": bad})
    m4 = {t: mags(f4[t]) for t in range(4)}
    record("A3", "N=4: ticks 0..3 each have one nonzero magnitude",
           all(len(m) == 1 for m in m4.values()), {"magnitudes_by_tick": m4})
    record("A4", "N=8: D_24 = 4096 * D_0",
           f8[24] == [[4096 * v for v in pair] for pair in f8[0]], {"D_24": f8[24]})
    bad = [t for t in range(0, T - 23)
           if any(f8[t + 24][x][r] != 4096 * f8[t][x][r] for x in range(8) for r in (0, 1))]
    record("A5", "N=8: D_{t+24} = 4096 D_t, t=0..176", not bad,
           {"ticks_tested": T - 23, "failing_ticks": bad})
    hit = [t for t in range(24) if 32 in mags(f8[t])]
    record("A6", "N=8: magnitude 32 within ticks 0..23 occurs exactly at {12,13}",
           hit == [12, 13], {"ticks_with_32": hit,
                             "magnitudes_by_tick_0_23": {t: mags(f8[t]) for t in range(24)}})
    record("A7", "N=8: at ticks 12, 13 the nonzero magnitudes are exactly {32}",
           mags(f8[12]) == [32] and mags(f8[13]) == [32],
           {"tick12": f8[12], "tick13": f8[13]})
    bad = [t for t in range(24, T + 1) if any(v % 4096 for pair in f8[t] for v in pair)]
    record("A8", "N=8: t=24..200 every nonzero total is a multiple of 4096", not bad,
           {"failing_ticks": bad})
    for n, f in ((4, f4), (8, f8)):
        hyp = [t for t in range(T + 1) if 32 in mags(f[t])]
        diff = [t for t in range(T + 1) if not panels_equal(f[t], square, rival32)]
        record(f"A9[N={n}]", f"N={n}: panel(square) == panel(rival32) for t=0..200", not diff,
               {"ticks_where_panels_differ": diff},
               {"ticks_where_magnitude_32_is_occupied": hyp, "vacuous": not hyp})
    bad = [t for t in range(T + 1) if len(mags(f4[t])) != 1]
    record("A10", "N=4: every panel t=0..200 has exactly one nonzero magnitude", not bad,
           {"failing_ticks": bad})
    diff16 = [t for t in range(T + 1) if not panels_equal(f16[t], square, rival32)]
    hyp16 = [t for t in range(T + 1) if 32 in mags(f16[t])]
    record("A11", "N=16: panel(square) != panel(rival32) at tick 13", 13 in diff16,
           {"all_ticks_le_200_where_panels_differ": diff16},
           {"ticks_where_magnitude_32_is_occupied": hyp16})


def words_field(n, t):
    d = [[0, 0] for _ in range(n)]
    for word in product((0, 1), repeat=t):  # 0 = move R, 1 = move L
        prev = 0  # launch rail R
        sign = 1
        pos = 0
        for m in word:
            if prev == 1 and m == 1:
                sign = -sign
            pos += 1 if m == 0 else -1
            prev = m
        d[pos % n][word[-1]] += sign
    return d


def prob(d, score, ports):
    w, z = weights(d, score)
    return Fraction(sum(w[x][r] for x, r in ports), z)


def part_b():
    n = 16
    f = fields(n, 200)
    bad = [t for t in range(1, 14) if words_field(n, t) != f[t]]
    record("B1", "N=16: propagation == signed-word enumeration, ticks 1..13", not bad,
           {"words_total": sum(2 ** t for t in range(1, 14)), "words_at_tick_13": 2 ** 13,
            "failing_ticks": bad})
    _, zs = weights(f[13], square)
    _, zr = weights(f[13], rival32)
    record("B2", "N=16 t=13: square normalizer = 8192", zs == 8192, {"value": zs})
    record("B3", "N=16 t=13: rival32 normalizer = 10240", zr == 10240, {"value": zr})
    record("B4", "D_13(7,R) = +32", f[13][7][0] == 32, {"value": f[13][7][0]})
    marked = [port_name(x, r) for x in range(n) for r in (0, 1) if abs(f[13][x][r]) == 32]
    record("B5", "t=13: exactly two ports have magnitude 32", len(marked) == 2,
           {"ports": marked, "signed_values": [f[13][x][r] for x in range(n) for r in (0, 1)
                                               if abs(f[13][x][r]) == 32]})
    others = sorted(abs(v) for pair in f[13] for v in pair if v and abs(v) != 32)
    record("B6", "t=13: some occupied port has magnitude != 32", bool(others),
           {"other_occupied_magnitudes": others, "field_13": f[13]})
    ps, pr = prob(f[13], square, [(7, 0)]), prob(f[13], rival32, [(7, 0)])
    record("B7", "p_13(7,R) = 1/8 (square), 1/5 (rival32)",
           ps == Fraction(1, 8) and pr == Fraction(1, 5), {"square": str(ps), "rival32": str(pr)})
    qs, qr = prob(f[12], square, [(6, 0), (6, 1)]), prob(f[12], rival32, [(6, 0), (6, 1)])
    record("B8", "p_12(6,R)+p_12(6,L) = 73/512 under both scores",
           qs == Fraction(73, 512) and qr == Fraction(73, 512),
           {"square": str(qs), "rival32": str(qr), "totals_at_site_6": f[12][6],
            "each_rail_square": [str(prob(f[12], square, [(6, 0)])),
                                 str(prob(f[12], square, [(6, 1)]))]})
    ds, dr = prob(f[13], square, [(7, 0), (5, 1)]), prob(f[13], rival32, [(7, 0), (5, 1)])
    record("B9", "p_13(7,R)+p_13(5,L) = 73/512 (square), 137/640 (rival32)",
           ds == Fraction(73, 512) and dr == Fraction(137, 640),
           {"square": str(ds), "rival32": str(dr),
            "daughter_totals": [f[13][7][0], f[13][5][1]]})
    record("B10", "N=16 t=12: no port has magnitude 32", 32 not in mags(f[12]),
           {"magnitudes_tick_12": mags(f[12]),
            "normalizers_tick_12": [weights(f[12], square)[1], weights(f[12], rival32)[1]]})

    def violations(score, last):
        out = []
        for t in range(last):
            for x in range(n):
                parent = prob(f[t], score, [(x, 0), (x, 1)])
                child = prob(f[t + 1], score, [((x + 1) % n, 0), ((x - 1) % n, 1)])
                if parent != child:
                    out.append([t, x])
        return out

    v = violations(square, 200)
    record("B11", "N=16 square: parent mass = daughter mass, all x, t=0..199", not v,
           {"blocks_tested": 200 * n, "violations": v})
    v = violations(rival32, 41)
    record("B12", "N=16 rival32 violates conservation at (t=12, x=6)", [12, 6] in v,
           {"all_violations_t_le_40_as_[t,x]": v})


def f2_power(n, m):
    """(X + 1/X)^m in F_2[X]/(X^N - 1) as a bitmask; bit x = coefficient of X^x."""
    full = (1 << n) - 1

    def rotl(p):
        return ((p << 1) | (p >> (n - 1))) & full

    def rotr(p):
        return ((p >> 1) | ((p & 1) << (n - 1))) & full

    p = 1
    for _ in range(m):
        p = rotl(p) ^ rotr(p)
    return p, rotl, rotr


def part_c():
    T = 400
    cache = {}

    def fld(n):
        if n not in cache:
            cache[n] = fields(n, T)
        return cache[n]

    for n in (4, 8, 16, 32, 64):
        f = fld(n)
        cut = n // 2 + 1
        bad = [t for t in range(cut, T + 1) if any(v % 2 for pair in f[t] for v in pair)]
        record(f"C1[N={n}]", f"N={n}: all totals even for t={cut}..{T}", not bad,
               {"ticks_tested": T + 1 - cut, "ticks_with_an_odd_total": bad})
        measured(f"C2[N={n}]", f"N={n}: some total odd at tick N/2={n // 2}",
                 {"odd_total_exists_at_cutoff_minus_one": any(v % 2 for pair in f[n // 2] for v in pair)})
    odd4 = sorted({v for t in range(0, 3) for v in signed_values(fld(4)[t]) if v > 0 and v % 2})
    odd8 = sorted({v for t in range(0, 5) for v in signed_values(fld(8)[t]) if v > 0 and v % 2})
    record("C3", "positive odd totals, ticks 0..N/2: ring 4 -> {1}, ring 8 -> {1,3}",
           odd4 == [1] and odd8 == [1, 3], {"ring4": odd4, "ring8": odd8})
    allodd = sorted({v for n in (4, 8) for t in range(T + 1) for v in signed_values(fld(n)[t])
                     if v > 0 and v % 2})
    five = [[n, t] for n in (4, 8) for t in range(T + 1) if 5 in signed_values(fld(n)[t])]
    negodd = sorted({v for n in (4, 8) for t in range(T + 1) for v in signed_values(fld(n)[t])
                     if v < 0 and v % 2})
    record("C4", "rings 4, 8, t=0..400: positive odd totals are exactly {1,3}; +5 never occurs",
           allodd == [1, 3] and not five,
           {"positive_odd_totals": allodd, "occurrences_of_+5_as_[N,t]": five,
            "negative_odd_totals_for_information": negodd})
    bad = []
    for n in (3, 4, 5, 6, 8, 12, 16, 32):
        f = fld(n)
        for t in range(1, 65):
            s, rotl, rotr = f2_power(n, t - 1)
            rpoly, lpoly = rotl(s), rotr(s)
            for x in range(n):
                if (f[t][x][0] % 2) != ((rpoly >> x) & 1) or (f[t][x][1] % 2) != ((lpoly >> x) & 1):
                    bad.append([n, t, x])
    record("C5", "F_2 representation of both rails, N in {3,4,5,6,8,12,16,32}, t=1..64", not bad,
           {"cases": 8 * 64, "mismatches_[N,t,x]": bad[:20], "mismatch_count": len(bad)})
    vals = {n: f2_power(n, n // 2)[0] for n in (4, 8, 16, 32, 64)}
    record("C6", "(X+1/X)^(N/2) = 0 in F_2[X]/(X^N-1), N in {4,8,16,32,64}",
           all(v == 0 for v in vals.values()), {"bitmask_by_N": vals})
    info = {}
    for n in (3, 5, 6, 7, 9, 10, 11, 12):
        f = fld(n)
        odd_ticks = [t for t in range(T + 1) if any(v % 2 for pair in f[t] for v in pair)]
        info[n] = {"last_tick_le_400_with_an_odd_total": max(odd_ticks),
                   "number_of_ticks_with_an_odd_total": len(odd_ticks)}
    measured("C7", "rings that are not powers of two: odd totals at late ticks", info)


class DSU:
    def __init__(self):
        self.p = {}

    def find(self, a):
        self.p.setdefault(a, a)
        while self.p[a] != a:
            self.p[a] = self.p[self.p[a]]
            a = self.p[a]
        return a

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.p[rb] = ra


def components(panel_list):
    dsu = DSU()
    for d in panel_list:
        vals = sorted(signed_values(d))
        for v in vals:
            dsu.find(v)
        for v in vals[1:]:
            dsu.union(vals[0], v)
    comp = {}
    for v in list(dsu.p):
        comp.setdefault(dsu.find(v), set()).add(v)
    return {v: frozenset(c) for c in comp.values() for v in c}


def part_d():
    T = 200
    f4, f8, f16 = fields(4, T), fields(8, T), fields(16, T)
    panels = f4 + f8
    comp = components(panels)
    c32 = sorted(comp.get(32, ()))
    cm32 = sorted(comp.get(-32, ()))
    ok = (32 in comp and set(c32) <= {32, -32} and 1 not in c32
          and (-32 not in comp or (set(cm32) <= {32, -32} and 1 not in cm32)))
    record("D1", "rings {4,8}, t<=200: component of +32 (and -32) is inside {+32,-32}, without +1",
           ok, {"component_of_+32": c32, "component_of_-32": cm32,
                "size_of_component_of_+1": len(comp[1]),
                "number_of_vertices": len(comp), "number_of_components": len(set(comp.values()))})
    mismatch, singles, nonsingles = [], 0, 0
    for v in sorted(comp):
        def doubled(k, v=v):
            return 2 * k * k if k == v else k * k
        preserved = all(panels_equal(d, square, doubled) for d in panels if v in signed_values(d))
        single = comp[v] == frozenset([v])
        singles += single
        nonsingles += not single
        if preserved != single:
            mismatch.append(str(v))
    record("D2", "doubling at one signed value v preserves all panels <=> component(v) = {v}",
           not mismatch, {"mismatches": mismatch},
           {"values_tested": len(comp), "singleton_components": singles,
            "values_in_larger_components": nonsingles})
    comps = sorted(set(comp.values()), key=lambda c: (min(abs(v) for v in c), min(c)))
    const = {}
    for i, c in enumerate(comps):
        k = Fraction(1) if 1 in c else Fraction(i + 9, 7)
        for v in c:
            const[v] = k

    def comp_score(k):
        return const[k] * k * k if k else 0

    bad = [i for i, d in enumerate(panels) if not panels_equal(d, square, comp_score)]
    record("D3", "score constant*k^2 with a different constant per component preserves all panels",
           not bad, {"panels_tested": len(panels), "failing_panel_indices": bad,
                     "distinct_constants_used": len(set(const.values()))})
    comp3 = components(f4 + f8 + f16)
    record("D4", "rings {4,8,16}, t<=200: component of +32 contains +1", 1 in comp3[32],
           {"size_of_component_of_+32": len(comp3[32]),
            "smallest_members": sorted(comp3[32], key=abs)[:12]})
    isolated = []
    allm = sorted({m for d in panels for m in mags(d)})
    for m in allm:
        if all(mags(d) == [m] for d in panels if m in mags(d)):
            where = [[4 if i <= T else 8, i if i <= T else i - (T + 1)]
                     for i, d in enumerate(panels) if m in mags(d)]
            isolated.append({"magnitude": str(m), "panels_[N,t]": where})
    measured("D5", "magnitudes on rings {4,8}, t<=200, that only ever fill a panel alone",
             {"count": len(isolated), "first_20": isolated[:20],
              "all_magnitudes_below_5000": [e["magnitude"] for e in isolated if int(e["magnitude"]) < 5000]})


def step_matrix(n):
    dim = 2 * n
    a = [[0] * dim for _ in range(dim)]
    for x in range(n):
        r_out = 2 * ((x + 1) % n)
        l_out = 2 * ((x - 1) % n) + 1
        a[r_out][2 * x] += 1
        a[r_out][2 * x + 1] += 1
        a[l_out][2 * x] += 1
        a[l_out][2 * x + 1] -= 1
    return a


def part_e():
    out = {}
    ok = True
    for n in range(3, 13):
        a = step_matrix(n)
        dim = 2 * n
        at = [list(r) for r in zip(*a)]
        ata = [[sum(at[i][k] * a[k][j] for k in range(dim)) for j in range(dim)] for i in range(dim)]
        aat = [[sum(a[i][k] * at[k][j] for k in range(dim)) for j in range(dim)] for i in range(dim)]
        two = [[2 * (i == j) for j in range(dim)] for i in range(dim)]
        # the matrix must also reproduce the propagation used elsewhere
        d = launch(n)
        vec = [v for pair in d for v in pair]
        same = True
        for _ in range(12):
            d = step(d)
            vec = [sum(a[i][k] * vec[k] for k in range(dim)) for i in range(dim)]
            same = same and vec == [v for pair in d for v in pair]
        good = ata == two and aat == two and same
        ok = ok and good
        out[n] = {"AtA_is_2I": ata == two, "AAt_is_2I": aat == two,
                  "matrix_reproduces_propagation_12_ticks": same}
    record("E1", "N=3..12: A^T A = A A^T = 2I (A normal, all |eigenvalue| = sqrt 2)", ok, out)
    hits = [[a, b] for a in range(801) for b in range(301) if (a, b) != (0, 0) and 2 ** a == 9 ** b]
    record("E5", "2^a != 9^b for 0<=a<=800, 0<=b<=300, (a,b) != (0,0)", not hits, {"hits": hits})
    T = 400
    pow3 = {3 ** j: j for j in range(1, 260)}
    table = {}
    for n in range(3, 13):
        f = fields(n, T)
        plus, minus, ones = [], [], []
        for t in range(T + 1):
            for x in range(n):
                for r in (0, 1):
                    v = f[t][x][r]
                    if v in pow3:
                        plus.append({"t": t, "port": port_name(x, r), "value": str(v), "j": pow3[v]})
                    elif -v in pow3:
                        minus.append({"t": t, "port": port_name(x, r), "value": str(v), "j": pow3[-v]})
                    elif v == 1:
                        ones.append(t)
        table[n] = {
            "plus_3^j_occurrences": plus,
            "distinct_j_plus": sorted({e["j"] for e in plus}),
            "last_tick_plus": max((e["t"] for e in plus), default=None),
            "minus_3^j_count": len(minus),
            "distinct_j_minus": sorted({e["j"] for e in minus}),
            "last_tick_minus": max((e["t"] for e in minus), default=None),
            "plus_one_count": len(ones),
            "last_tick_plus_one": max(ones, default=None),
        }
    measured("E6", "occurrences of +3^j (j>=1) as signed port totals, N=3..12, t=0..400", table)


def main():
    parser = argparse.ArgumentParser(description="Reviewer exact-integer check; see module docstring.")
    parser.add_argument("output", type=Path)
    output = parser.parse_args().output
    with output.open("x", encoding="utf-8") as stream:  # refuses to overwrite
        part_a()
        part_b()
        part_c()
        part_d()
        part_e()
        met = [r["id"] for r in RESULTS if r["pass"] is True]
        failed = [r["id"] for r in RESULTS if r["pass"] is False]
        meas = [r["id"] for r in RESULTS if r["pass"] == "measured only"]
        json.dump({"summary": {"met": len(met), "failed": len(failed), "measured_only": len(meas),
                               "failed_ids": failed},
                   "results": RESULTS}, stream, indent=1, sort_keys=True)
        stream.write("\n")
    print(f"met {len(met)} failed {len(failed)} measured-only {len(meas)}; failed ids: {failed}")


if __name__ == "__main__":
    main()
