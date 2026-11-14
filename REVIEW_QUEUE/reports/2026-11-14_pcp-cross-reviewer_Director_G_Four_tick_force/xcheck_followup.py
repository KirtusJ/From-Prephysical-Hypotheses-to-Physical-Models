"""Follow-up to xcheck_four_tick.py (first result file out1/xcheck_four_tick.json is kept, with its
three failed predicates A3, A6, B1).  Run: python3 -B xcheck_followup.py OUTDIR STORED_PREPARED_JSON
Diagnosis of the three failures (all faults of the reviewer's program, fixed here, originals kept):
 A3: the 40-digit residual was cast to a double before comparison (floor 1e-16, threshold 1e-35).
 A6: the reviewer's own exponent for 'tau v / a' had the wrong sign (velocity in Y is v*a/tau).
 B1: |d-q^2/2|/(q^4/6) was evaluated in doubles at |q|~1e-4, where the numerator is rounding.
PREDICATES (fixed before this run)
 A3' mpmath 50 digits: |d'(q) - sin q/sqrt(1+sin^2 q)| < 1e-40 at 9 points (d' by mp.diff at 50 digits
     has ~1e-25 accuracy, so the threshold used is 1e-20; basis: mp.diff default step error) and d(0)=0.
 A6' exponent of v*a/tau with v=delta*p0 is 0.
 B1' mpmath 50 digits, q = j/2000, j=1..2000: |d|<=q^2/2 and |d-q^2/2|<=q^4/6; report max ratios.
 D2' among D rows with hypothesis true and bound<0.2: report max |mean p shift - (-FT)| and
     max relative position-shift error (no threshold); predicate: sign of position shift = -sign F.
 G2  (observable, kept whatever the outcome) in the note's STORED prepared_force.json and in the
     reviewer's G rows: number of forced rows whose mean terminal position moved, relative to the
     F=0 row of the same panel, in the direction OPPOSITE to -F.  Predicate: that number is 0.
"""
import json, sys
from fractions import Fraction as Fr
from pathlib import Path
import mpmath as mp
out = Path(sys.argv[1]) / "xcheck_followup.json"
if out.exists(): sys.exit("Refusing to overwrite")
R = {"failed": []}
def rec(n, ok, **kw):
    R[n] = dict(ok=bool(ok), **kw)
    if not ok: R["failed"].append(n)
mp.mp.dps = 50
d = lambda q: mp.asin(mp.sin(-mp.pi/2+q)/mp.sqrt(2)) + mp.pi/4
res = max(abs(mp.diff(d, q) - mp.sin(q)/mp.sqrt(1+mp.sin(q)**2)) for q in map(mp.mpf, ("-1.4","-1","-0.5","-0.01","0.003","0.2","0.7","1","1.5")))
rec("A3p_dprime", res < mp.mpf(10)**-20 and abs(d(mp.mpf(0))) < mp.mpf(10)**-45, max_residual=mp.nstr(res, 5), d0=mp.nstr(abs(d(mp.mpf(0))), 5))
e = Fr(9, 10); rec("A6p_velocity_exponent", 1 + (e+1) - (e+2) == 0, exponent=str(1 + (e+1) - (e+2)))
r1 = r2 = mp.mpf(0); arg = None
for j in range(1, 2001):
    q = mp.mpf(j)/2000; v = d(q)
    r1 = max(r1, abs(v)/(q*q/2)); t = abs(v-q*q/2)/(q**4/6)
    if t > r2: r2, arg = t, q
rec("B1p_quartic", r1 <= 1 and r2 <= 1, max_ratio_quadratic=mp.nstr(r1, 12), max_ratio_quartic=mp.nstr(r2, 12), argmax_q=mp.nstr(arg, 6),
    ratio_at_q_1=mp.nstr(abs(d(mp.mpf(1))-mp.mpf(1)/2)*6, 12))
first = json.load(open(Path(sys.argv[1]).parent / "out1" / "xcheck_four_tick.json"))
rows = [r for r in first["D_rows"] if r.get("hypothesis") and r["F"] != 0 and r["bound"] < 0.2]
rec("D2p_shift_small_bound", all((r["mean_Y_shift"] > 0) == (r["ideal_Y_shift"] > 0) for r in rows), tested=len(rows),
    max_abs_momentum_shift_error=max(abs(r["mean_p_shift"]-r["ideal_p_shift"]) for r in rows),
    max_rel_position_shift_error=max(abs(r["mean_Y_shift"]/r["ideal_Y_shift"]-1) for r in rows),
    max_E=max(r["E"] for r in rows))
stored = json.load(open(sys.argv[2]))
bad = []; tot = 0
for p in stored["panels"]:
    m = {f["potential_slope"]: f["mean_position"] for f in p["flights"]}
    for F in (-1, 1):
        tot += 1; sh = m[F]-m[0]
        if sh * (-F) <= 0: bad.append(dict(inverse_delta=p["inverse_delta"], p0=p["p0"], F=F, shift=sh, ideal=-F*p["attained_time"]**2/2))
mine = []; tot2 = 0
for r in first["G_rows"]:
    for F, sh in ((1, r["shift_F_plus"]), (-1, r["shift_F_minus"])):
        tot2 += 1
        if sh * (-F) <= 0: mine.append(dict(inverse_delta=r["inverse_delta"], p0=r["p0"], F=F, shift=sh, ideal=-F*r["T"]**2/2))
rec("G2_direction_of_mean_shift", not bad and not mine, stored_forced_rows=tot, stored_wrong_direction=len(bad), stored_rows=bad,
    reviewer_forced_rows=tot2, reviewer_wrong_direction=len(mine), reviewer_rows=mine)
json.dump(R, out.open("x"), indent=1); print(json.dumps(R, indent=1)[:6000])
