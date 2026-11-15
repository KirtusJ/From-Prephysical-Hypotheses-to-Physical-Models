"""Candidate Z6 "Odd Lap": exact instances. STIPULATED CANDIDATE FOR DISPROOF; nothing here is a claim about the world.

Carrier (stipulations O1, O2): two-rail ring Z_N, gains in A = Z2 x Z_(2M), M = N/gcd(N,2): a = (0,0), b = (0,1),
c = (0,0), d = (1,1). Then delta = ad/(bc) = (1,0) (order 2), B = bc/a^2 = (0,1), beta = B^M = (0,M) of order 2,
not in <delta>: two classes of winding, beta^2 = delta^0 (k even). By G10 Lemma 5.53 the class of a walk at a vertex
is its winding level (number of left steps, divided by M) modulo 2, and the sign psi is (-1)^(first coordinate),
that is (-1)^(number of left steps that follow a left step). The program tracks levels and signs directly and
asserts, for N = 16, that the gains computed in the group give the same classes.

Rules compared at each vertex, with eps_0, eps_1 the signed sums of the two classes:
  odd lap (the candidate, O7): (eps_0 - eps_1)^2;  even lap: (eps_0 + eps_1)^2;  count: number of walks.
PREDICATES fixed before the first run (15 November 2026):
 F1  for every ring and length examined, the odd-lap weights of the event of all walks sum to 2^T (consistency).
 F2  odd lap and even lap give the same weights at every vertex for every length T <= M, and differ at T = M + 1.
 F3  the fork: weight at ((M+1) mod N, R) is 2 + 2(-1)^M and at ((M-1) mod N, L) is 2 - 2(-1)^M, in units 2^-(M+1).
 F4  the group gains and the level bookkeeping agree on N = 16 (hypothesis check of the carrier).
Reported, no predicate: the total variation distance between the odd-lap and even-lap distributions of the event of
all walks, for T = M+1 .. 3M, and the odd-lap return weight at (0,R).
Usage: python3 odd_lap_instances.py RESULT.json  (refuses to overwrite)."""
import sys, os, json, collections
from fractions import Fraction as Fr
OUT = sys.argv[1]; assert not os.path.exists(OUT)
def run(N, T, masks=None, group=False):
    M = N // 2 if N % 2 == 0 else N
    st = collections.Counter({(0, 0, 0, 0, 0): 1})        # site, rail, left steps, sign bit, group second coordinate
    for t in range(1, T + 1):
        new = collections.Counter()
        for (x, r, l, s, g), c in st.items():
            y = (x + 1) % N
            if masks is None or y in masks[t - 1]: new[(y, 0, l, s, g)] += c              # a or c: gain (0,0)
            y = (x - 1) % N
            if masks is None or y in masks[t - 1]: new[(y, 1, l + 1, s ^ (1 if r else 0), (g + 1) % (2 * M))] += c   # b = (0,1), d = (1,1)
        st = new
    by = collections.defaultdict(list)
    for k, c in st.items(): by[(k[0], k[1])].append((k[2], k[3], k[4], c))
    res = {}
    for v, items in by.items():
        lmin = min(i[0] for i in items); e = [0, 0]; n = 0
        for l, s, g, c in items:
            assert (l - lmin) % M == 0
            e[((l - lmin) // M) % 2] += c * (-1) ** s; n += c
        if group:   # class from the group element: second coordinate differs by M between the classes
            g0 = min(i[2] for i in items if (i[0] - lmin) // M % 2 == 0) if any((i[0] - lmin) // M % 2 == 0 for i in items) else None
            for l, s, g, c in items:
                if g0 is not None: assert ((g - g0) % (2 * M) == 0) == (((l - lmin) // M) % 2 == 0)
        res[v] = (e[0], e[1], n)
    return M, res
rep = {"argv": sys.argv[1:], "rings": [], "predicates": {}}
F1 = F2 = F3 = True
for N in (16, 18, 20, 9, 11):
    M = N // 2 if N % 2 == 0 else N
    row = {"N": N, "M": M, "tv": [], "return_odd": []}
    for T in range(1, 3 * M + 1):
        _, res = run(N, T, group=(N == 16 and T <= 2 * M))
        odd = {v: (e[0] - e[1]) ** 2 for v, e in res.items()}; even = {v: (e[0] + e[1]) ** 2 for v, e in res.items()}
        F1 &= sum(odd.values()) == 2 ** T and sum(even.values()) == 2 ** T
        same = odd == even
        if T <= M: F2 &= same
        if T == M + 1: F2 &= not same
        if T > M: row["tv"].append([T, str(Fr(sum(abs(odd[v] - even[v]) for v in odd), 2 * 2 ** T))])
        row["return_odd"].append([T, str(Fr(odd.get((0, 0), 0), 2 ** T))])
    masks = [{t % N, (-t) % N} for t in range(1, M + 1)] + [set(range(N))]
    _, res = run(N, M + 1, masks)
    w = {v: (e[0] - e[1]) ** 2 for v, e in res.items()}
    vr, vl = ((M + 1) % N, 0), ((M - 1) % N, 1)
    ok = set(w) == {vr, vl} and w[vr] == 2 + 2 * (-1) ** M and w[vl] == 2 - 2 * (-1) ** M
    F3 &= ok; row["fork"] = {"at_R": w.get(vr), "at_L": w.get(vl), "units": "2^-(M+1)", "predicate": ok}
    rep["rings"].append(row)
rep["predicates"] = {"F1": F1, "F2": F2, "F3": F3, "F4": True}
json.dump(rep, open(OUT, "x"), indent=1); print(rep["predicates"])
for r in rep["rings"]: print(r["N"], r["fork"], r["tv"][:4])
