"""Candidate Z10 "Slow Clock": exact instances. STIPULATED CANDIDATE FOR DISPROOF; nothing here is a claim about the world.

Signed two-rail line (sign -1 on a left step that follows a left step), sharp start at (0,R), running free.
eps(v), n(v): signed sum and number of the walks of length T ending at v. Interfering chances p = eps^2 / sum eps^2;
counting chances p_c = n / 2^T. Age: Lambda(T) = sum p log2 n; Lambda_c(T) = sum p_c log2 n.
c* = (1/(pi sqrt 2)) * integral over (-pi/2, pi/2) of h((1 + sin(t)/sqrt 2)/2) / (1 - sin(t)^2/2) dt, h the binary entropy.
PREDICATES fixed before the first run (15 November 2026):
 K1  Lambda(1) = Lambda(2) = 0 and Lambda(T) > Lambda(T-1) for every T from 3 to 600 (the age starts at tick 3 and
     then rises at every tick).
 K2  Lambda(T) <= T - 1 for every T from 1 to 600.
 K3  the rate Lambda(T)/T is below c* for every T from 1 to 600.
 K4  c* computed by Simpson's rule with 100,000 and with 200,000 panels agrees to 10^-12, and the weight
     1/(pi sqrt 2 (1 - sin^2/2)) integrates to 1 within 10^-12 (the weight is a probability density).
Reported, no predicate: the table of rates and gaps at T = 50, 100, 150, ..., 600 for the plot.
Usage: python3 slow_clock_instances.py RESULT.json  (refuses to overwrite)."""
import sys, os, json, math
from decimal import Decimal, getcontext
getcontext().prec = 60
OUT = sys.argv[1]; assert not os.path.exists(OUT)
def h(x): return 0.0 if x <= 0 or x >= 1 else -(x * math.log2(x) + (1 - x) * math.log2(1 - x))
def g(t): return h((1 + math.sin(t) / math.sqrt(2)) / 2) / (1 - math.sin(t) ** 2 / 2)
def simpson(f, a, b, n):
    hh = (b - a) / n; s = f(a) + f(b)
    for i in range(1, n): s += (4 if i % 2 else 2) * f(a + i * hh)
    return s * hh / 3
k = math.pi * math.sqrt(2)
c1 = simpson(g, -math.pi / 2, math.pi / 2, 100000) / k; c2 = simpson(g, -math.pi / 2, math.pi / 2, 200000) / k
w = simpson(lambda t: 1 / (1 - math.sin(t) ** 2 / 2), -math.pi / 2, math.pi / 2, 200000) / k
LN2 = Decimal(2).ln(); C = Decimal(repr(c2)); st = {(0, 0): (1, 1)}; lam = {0: Decimal(0)}; lamc = {}
for T in range(1, 601):
    new = {}
    for (x, r), (sg, n) in st.items():
        for y, r2, flip in ((x + 1, 0, 1), (x - 1, 1, -1 if r == 1 else 1)):
            a, b = new.get((y, r2), (0, 0)); new[(y, r2)] = (a + sg * flip, b + n)
    st = new; wq = sum(s * s for s, n in st.values())
    lam[T] = sum((Decimal(s * s) / wq) * (Decimal(n).ln() / LN2) for s, n in st.values() if s)
    lamc[T] = sum((Decimal(n) / Decimal(2) ** T) * (Decimal(n).ln() / LN2) for s, n in st.values())
E = Decimal(10) ** -40
K1 = lam[1] == 0 and lam[2] == 0 and all(lam[T] > lam[T - 1] + E for T in range(3, 601))
K2 = all(lam[T] <= T - 1 + E for T in range(1, 601))
K3 = all(lam[T] / T < C for T in range(1, 601))
K4 = abs(c1 - c2) < 1e-12 and abs(w - 1) < 1e-12
rep = {"argv": sys.argv[1:], "c_star": c2, "c_star_half_panels": c1, "weight_integral": w,
       "table": [[T, str(lam[T] / T)[:12], str(C - lam[T] / T)[:12], str(lamc[T] / T)[:12]] for T in range(50, 601, 50)],
       "first_ages": [[T, str(lam[T])[:18]] for T in range(1, 9)], "predicates": {"K1": K1, "K2": K2, "K3": K3, "K4": K4}}
json.dump(rep, open(OUT, "x"), indent=1); print(rep["predicates"], c2); [print(r) for r in rep["table"][::3]]; print(rep["first_ages"])
