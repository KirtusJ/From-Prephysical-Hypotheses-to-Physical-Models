"""Cross-review program for pr259 four_preparations_at_one_site.md.
Usage: PYTHONPATH=<cvxpy dir> python3 -I xr_bypass.py <velocity_experiment dir> <results dir> <out.json>
Refuses to overwrite out.json. Seed 259. Measure-and-prepare (MP) optimum computed as the
qubit->qubit entanglement-breaking SDP: Choi J>=0, J^{T_B}>=0 (PPT = separable for 2x2), tr_B J = I.
Tolerances: SDP solver accuracy; we use 1e-5 (Clarabel default gaps ~1e-8; 1e-5 is a margin, stated).

PREDICATES (fixed before first run):
 P0a  BB84 uniform, MP optimum = 0.75 +- 1e-5.  P0b six-state uniform MP optimum = 2/3 +- 1e-5.
 P0c  same SDP without PPT constraint (all channels) gives 1 +- 1e-5 for BB84.
 P1   For 200 random imperfect sources (states sigma_j = random mixed states near |j>, random prior q),
      after checking the hypothesis per instance (sigma_j PSD, trace 1, q a distribution, no side register),
      MP optimum <= 3/4 + TV(q,u) + sqrt(ebar) + 1e-5. Report how many qualify and the max slack used.
 P2   y-tilt family (+-x tilted toward +y, +-z tilted toward -y by angle d; within the note's assumptions,
      no side info): there is d with bypass ebar <= 0.02 whose MP optimum >= 226560354573/274877906944.
 P3   Side-register model (basis bit leaked to the memory with probability p, else the wrong basis):
      bypass statistics equal the ideal ones (ebar = 0, TV = 0) for every p, and MP score = (1+p)/2;
      score exceeds the 7-write value for p > 0.6484.  (Assumption-violating; shows bypass blindness.)
 P4   Independent float aggregation (own code, author's step list) of the four-label Pauli score
      reproduces 226560354573/274877906944 at m=7 to 1e-12; also reported at m=5 and m=9 (unreported).
 P5   Extra-copy prediction 1/4 + A/2 at m=7 within 3 binomial sigma of 5424/8192; ideal A within
      3 sigma of 6749/8192.
 P6   Native-record leakage check on stored ideal records: encoder label (I,J,Z,X) independent of the
      preparation (basis,sign): chi-square p-value > 0.001 in both stored files.
"""
import sys, json, gzip, math
from pathlib import Path
from runpy import run_path
from fractions import Fraction
import numpy as np, cvxpy as cp
from scipy.stats import chi2_contingency

vel, resdir, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
if out.exists():
    raise SystemExit("refusing to overwrite " + str(out))
rng = np.random.default_rng(259)
I2 = np.eye(2); X = np.array([[0,1],[1,0]]); Y = np.array([[0,-1j],[1j,0]]); Z = np.diag([1.,-1])
def bloch(v): return 0.5*(I2 + v[0]*X + v[1]*Y + v[2]*Z)
ideal = [np.array(v,float) for v in ([0,0,1],[0,0,-1],[1,0,0],[-1,0,0])]   # R, L, +, -
tests = [bloch(v) for v in ideal]          # trusted matching-basis 'correct sign' projectors
def ptB(M):
    return cp.vstack([cp.hstack([M[0:2,0:2].T, M[0:2,2:4].T]), cp.hstack([M[2:4,0:2].T, M[2:4,2:4].T])]) if False else None
def mp_opt(states, q, tests, ppt=True):
    J = cp.Variable((4,4), hermitian=True)  # Choi, order in(x)out
    W = sum(qj*np.kron(s.T, T) for qj, s, T in zip(q, states, tests))
    cons = [J >> 0, cp.partial_trace(J, [2,2], axis=1) == I2]
    if ppt: cons.append(cp.partial_transpose(J, [2,2], axis=1) >> 0)
    pr = cp.Problem(cp.Maximize(cp.real(cp.trace(W @ J))), cons); pr.solve(solver="CLARABEL")
    return float(pr.value)
R = {}
def rec(k, v, ok):
    R[k] = {"value": v, "pass": bool(ok)}; print(k, "PASS" if ok else "FAIL", v)
b = mp_opt([bloch(v) for v in ideal], [.25]*4, tests); rec("P0a_bb84_mp", b, abs(b-.75) < 1e-5)
six = ideal + [np.array([0,1.,0]), np.array([0,-1.,0])]
s6 = mp_opt([bloch(v) for v in six], [1/6]*6, [bloch(v) for v in six]); rec("P0b_six_mp", s6, abs(s6-2/3) < 1e-5)
c = mp_opt([bloch(v) for v in ideal], [.25]*4, tests, ppt=False); rec("P0c_bb84_all", c, abs(c-1) < 1e-5)
def bypass(states, q):
    e = [1-float(np.real(np.trace(T@s))) for T, s in zip(tests, states)]
    eb = sum(qj*ej for qj, ej in zip(q, e)); tv = 0.5*sum(abs(qj-.25) for qj in q)
    return eb, tv
qual = 0; worst = -1; viol = []
for n in range(200):
    eps = rng.uniform(0, 0.3)
    states = []
    for v in ideal:
        w = v + eps*rng.normal(size=3); w *= min(1, 1/np.linalg.norm(w)) * rng.uniform(0.8, 1)
        states.append(bloch(w))
    q = rng.dirichlet([20]*4)
    okhyp = all(np.linalg.eigvalsh(s).min() > -1e-12 and abs(np.trace(s)-1) < 1e-12 for s in states) and abs(q.sum()-1) < 1e-12
    if not okhyp: continue
    qual += 1
    eb, tv = bypass(states, q); A = mp_opt(states, q, tests); bound = .75+tv+math.sqrt(eb)
    worst = max(worst, (A-.75)/(tv+math.sqrt(eb)) if tv+eb > 0 else 0)
    if A > bound+1e-5: viol.append([n, A, bound])
rec("P1_bypass_bound", {"qualifying": qual, "violations": viol, "max_fraction_of_slack_used": worst}, qual > 0 and not viol)
target = 226560354573/274877906944
tilt = []
for d in np.linspace(0, 0.6, 61):
    st = []
    for k, v in enumerate(ideal):
        sgn = 1 if k >= 2 else -1
        st.append(bloch(np.cos(d)*v + np.sin(d)*np.array([0, sgn, 0])))
    eb, tv = bypass(st, [.25]*4); A = mp_opt(st, [.25]*4, tests)
    tilt.append([float(d), eb, A, .75+math.sqrt(eb)])
hit = [t for t in tilt if t[2] >= target]
rec("P2_tilt_reaches_7write_with_ebar<=0.02", {"first_hit": hit[0] if hit else None, "table_every_5": tilt[::5]}, bool(hit) and hit[0][1] <= 0.02)
# P3: side register. Bypass reads only rail: marginal per label = ideal pure state for any p.
p3 = []
for p in (0, .5, .6484, .65, 1):
    st = [bloch(v) for v in ideal]; eb, tv = bypass(st, [.25]*4)
    p3.append([p, eb, tv, (1+p)/2])
rec("P3_side_register", p3, all(r[1] < 1e-12 and r[2] == 0 for r in p3) and (1+.6485)/2 > target > (1+.6483)/2)
# P4 own aggregation
steps = run_path(str(vel/"check_record_messages.py"))["read_steps"]()
def four(m):
    st = {(1.0, 0.0, 1): 1.0}
    for _ in range(m):
        nx = {}
        for (a, c, s), w in st.items():
            for g, h, dr in steps:
                nrm = math.hypot(g, h)
                u = (g*a - h*dr*c)/nrm; v = (h*a + g*dr*c)/nrm
                ang = math.atan2(v, u) % math.pi
                key = (round(math.cos(ang), 12), round(math.sin(ang), 12), s*dr)
                nx[key] = nx.get(key, 0) + w*(g*g+h*h)/128
        st = nx
    return sum(w*max(a*a, c*c) for (a, c, _), w in st.items()), sum(st.values())
f7, tot = four(7); f5, _ = four(5); f9, _ = four(9)
rec("P4_four_label", {"m5": f5, "m7": f7, "m9": f9, "nsteps": len(steps), "mass7": tot}, abs(f7-target) < 1e-12)
def z(k, n, p): return (k/n - p)/math.sqrt(p*(1-p)/n)
zc, zx = z(6749, 8192, target), z(5424, 8192, .25+target/2)
rec("P5_replays", {"z_coherent": zc, "z_copy": zx, "pred_copy": .25+target/2}, abs(zc) < 3 and abs(zx) < 3)
lab = run_path(str(vel/"four_state_records.py"))["position_label"]
p6 = {}
for name in ("coherent", "copied"):
    d = json.load(gzip.open(resdir/f"four_state_{name}_8192.json.gz", "rt"))
    m = d["blocks"]; tab = np.zeros((4, 4))
    for wd, cnt in d["counts"].items():
        bits = int(wd, 2); prep = 2*(bits & 1) + ((bits >> 1) & 1)
        L = lab(steps, [(bits >> (2+3*j)) & 7 for j in range(m)])
        tab[prep, "IJZX".index(L)] += cnt
    chi, pv, _, _ = chi2_contingency(tab); p6[name] = {"table": tab.tolist(), "p": pv}
rec("P6_label_independent_of_prep", p6, all(v["p"] > 1e-3 for v in p6.values()))
with open(out, "x") as fh: json.dump(R, fh, indent=1)
