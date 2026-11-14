#!/usr/bin/env python3
"""Follow-up to attack_s7.py, written after its predicates F4 and F6 FAILED for q = 8 (kept in Attack_S7_Results.json):
on the Z1-F ring with N = q = 8 all four faithful characters gave the same tables, and every unit of Z_8 is induced by an
automorphism of the carrier with switching.  Conjecture from that failure: psi_k and psi_(k+q/2) give the same rule when
q is a multiple of 4 (the extra gain (-1)^x is a switching times the constant -1 per step), so the rule classes among
norm-preserving characters are the orbits of k -> -k and k -> k + q/2.
Conventions and exact arithmetic as in attack_s7.py (its definitions are loaded from the source, up to its first section mark).
Ring of N sites, q | N, field multiple f; vertex 2x+s; start (0,R).

Predicates, fixed before the first run (prediction in brackets):
 G1  For (q,N) in (4,4),(8,8),(12,12),(16,16),(4,8),(8,16),(5,5),(5,10),(6,6),(10,10),(6,12): the classes of norm-preserving
     characters with equal exact tables P_t(y), t <= 12, are exactly the orbits of k -> -k and (if 4 | q) k -> k + q/2.  [pass]
 G2  Number of classes that contain a faithful character: q=4: 1, q=8: 1, q=12: 1, q=16: 2, q=5: 2, q=6: 1, q=10: 2.  [pass]
 G3  Equal tables means equal rule: for two characters in one class, ||v^k_S||^2 = ||v^l_S||^2 on 300 pseudo-random events
     (fixed seed) of lengths 1..8 for (q,N) = (8,8) and (12,12).  [pass]
 G4  A non-faithful norm-preserving character whose field multiple is 0 or q/2 modulo q gives exactly the tables of the
     signed ring Z1-R of the same length (no force): (q,N) = (5,5) k=5; (6,6) k=3; (10,10) k=5.  [pass]
 G5  q = 12, N = 12: the non-faithful class {3,9} has tables different from the faithful class and equal to those of the
     faithful class of q = 4 on the ring of 12 sites (field 2 pi/4).  [pass]
Writes Attack_S7_Followup_Results.json; refuses to overwrite.  Seed fixed.
"""
import json, math, os, random, sys
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "Attack_S7_Followup_Results.json")
if os.path.exists(OUT): sys.exit("refusing to overwrite " + OUT)
src = open(os.path.join(HERE, "attack_s7.py")).read().split("# ======================= B:")[0]
src = src.replace('if os.path.exists(OUT): sys.exit("refusing to overwrite " + OUT)', "")
exec(src); OUT = os.path.join(HERE, "Attack_S7_Followup_Results.json")
random.seed(20261113); R = {"seed": 20261113}; T = 12

def ring(q, N, f=1):
    M = q * 2 // math.gcd(q, 2); idx = lambda x, s: 2 * (x % N) + s
    succ = {idx(x, s): [(idx(x + 1, 0), (-f * x * (M // q)) % M),
                        (idx(x - 1, 1), (-f * x * (M // q) + (M // 2 if s == 1 else 0)) % M)] for x in range(N) for s in (0, 1)}
    return succ, M
def signed_ring_tables(N, T):
    succ = {2 * x + s: [(2 * ((x + 1) % N), 0), (2 * ((x - 1) % N) + 1, 1 if s == 1 else 0)] for x in range(N) for s in (0, 1)}
    return succ, tables(succ, 1, 2, Cyc(2), T)
def classes_of(q, N):
    succ, M = ring(q, N); cyc = Cyc(M)
    npk = [k for k in range(M) if norm_pres(succ, k, M, cyc)]; tab = {k: tables(succ, k, M, cyc, T) for k in npk}
    cl = {}
    for k in npk: cl.setdefault(json.dumps([[list(tab[k][t][v]) for v in sorted(succ)] for t in range(T + 1)]), []).append(k)
    return succ, M, cyc, npk, tab, sorted(cl.values())
def orbits(npk, q, M):
    seen = set(); out = []
    for k in npk:
        if k in seen: continue
        orb = {k}; grow = True
        while grow:
            new = {(-x) % M for x in orb}
            if q % 4 == 0: new |= {(x + q // 2) % M for x in orb}
            grow = not new <= orb; orb |= new
        orb &= set(npk); seen |= orb; out.append(sorted(orb))
    return sorted(out)
R["G1"] = {}; R["G2"] = {}
expect = {4: 1, 8: 1, 12: 1, 16: 2, 5: 2, 6: 1, 10: 2}
for q, N in ((4, 4), (8, 8), (12, 12), (16, 16), (4, 8), (8, 16), (5, 5), (5, 10), (6, 6), (10, 10), (6, 12)):
    succ, M, cyc, npk, tab, cl = classes_of(q, N); orb = orbits(npk, q, M)
    faithful = [k for k in npk if math.gcd(k, M) == 1]; nf = sum(1 for c in cl if any(k in faithful for k in c))
    R["G1"][f"q={q},N={N}"] = dict(M=M, norm_preserving=npk, faithful=faithful, classes_by_tables=cl, orbits=orb, passed=cl == orb)
    R["G2"][f"q={q},N={N}"] = dict(classes_with_a_faithful_character=nf, expected=expect[q], passed=nf == expect[q])
R["G1"]["passed"] = all(v["passed"] for v in R["G1"].values()); R["G2"]["passed"] = all(v["passed"] for v in R["G2"].values())

def walks(succ, t, M):
    W = [((0,), 0)]
    for _ in range(t): W = [(w + (y,), (g + h) % M) for w, g in W for y, h in succ[w[-1]]]
    return W
def sq(S, k, M, cyc):
    by = {}
    for w, g in S: by.setdefault(w[-1], [0] * M)[(k * g) % M] += 1
    tot = [0] * M
    for v in by.values():
        for i, c in enumerate(cyc.norm2(v)): tot[i] += c
    return cyc.red(tot)
R["G3"] = {}
for q in (8, 12):
    succ, M, cyc, npk, tab, cl = classes_of(q, q); ok = True; n = 0; pools = {t: walks(succ, t, M) for t in range(1, 9)}
    for _ in range(300):
        t = random.randint(1, 8); S = random.sample(pools[t], random.randint(1, min(len(pools[t]), 24))); n += 1
        for c in cl: ok &= len({sq(S, k, M, cyc) for k in c}) == 1
    R["G3"][f"q={q}"] = dict(events=n, classes=cl, passed=bool(ok))
R["G3"]["passed"] = all(v["passed"] for v in R["G3"].values())

R["G4"] = {}
for q, k in ((5, 5), (6, 3), (10, 5)):
    succ, M, cyc, npk, tab, cl = classes_of(q, q); s2, t2 = signed_ring_tables(q, T)
    same = all(abs(fval(cyc, tab[k][t][v], 2 ** t) - t2[t][v][0] / 2 ** t) < 1e-12 for t in range(T + 1) for v in succ)
    exact = all(tuple(tab[k][t][v][1:]) == tuple([0] * (len(tab[k][t][v]) - 1)) and tab[k][t][v][0] == t2[t][v][0]
                for t in range(T + 1) for v in succ)
    R["G4"][f"q={q},k={k}"] = dict(norm_preserving=k in npk, equal_to_signed_ring_exact=bool(exact), equal_decimal=bool(same),
                                   passed=bool(k in npk and exact))
R["G4"]["passed"] = all(v["passed"] for v in R["G4"].values())

s12, M12, c12, np12, tab12, cl12 = classes_of(12, 12); s4, M4, c4, np4, tab4, cl4 = classes_of(4, 12)
eq = all(abs(fval(c12, tab12[3][t][v], 2 ** t) - fval(c4, tab4[1][t][v], 2 ** t)) < 1e-12 for t in range(T + 1) for v in s12)
R["G5"] = dict(classes_q12=cl12, class_3_differs_from_class_1=tab12[3] != tab12[1], class_3_equals_q4_field_decimal_1e_12=bool(eq),
               note="comparison between two cyclotomic rings is done in decimals, tolerance 1e-12 on numbers that are sums of at most 2^12 cosines with integer coefficients (rounding error about 1e-13)",
               passed=bool(tab12[3] != tab12[1] and eq))
R["summary"] = {k: R[k]["passed"] for k in ("G1", "G2", "G3", "G4", "G5")}
json.dump(R, open(OUT, "w"), indent=1, default=str); print(json.dumps(R["summary"], indent=1))
for k, v in R["G1"].items():
    if k != "passed": print(k, v["classes_by_tables"], v["orbits"])
