#!/usr/bin/env python3
"""Chaos harness, step 1: copy the three targets, plant one mutant per folder, write PREDICTIONS.json BEFORE any run.
Never writes outside its own folder.  No random choice of mutation site is made (sites are fixed by hand); seed
20261113 is recorded for form only."""
import os, shutil, hashlib, json, sys
W = os.path.dirname(os.path.abspath(__file__))
REPO = "/home/user/From-Prephysical-Hypotheses-to-Physical-Models/REVIEW_QUEUE"
N2 = "2026-11-13_pcp-challenger_G10_prop-abund_cor-abund"; P2 = "challenge_prop_abund_cor_abund"
N3 = "2026-11-13_pcp-micro-review_G10_cor-composition_cor-return"; P3 = "micro_cor_composition_cor_return"
SRC = dict(lib=f"{REPO}/lib/pcplib.py", p2=f"{REPO}/reports/{N2}/{P2}.py", p3=f"{REPO}/reports/{N3}/{P3}.py",
           r2=f"{REPO}/reports/{N2}/{P2}_results.json", r3=f"{REPO}/reports/{N3}/{P3}_results.json")
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
DIG = {k: sha(v) for k, v in SRC.items()}

# id, file, old, new, description, true statement made false?, prediction
M = [
 ("L01", "lib", "    return Poly(co[::-1], _x).rem(_phi[q]).is_zero if any(co) else True", "    return True",
  "zero_sum always True", "yes",
  "P2: no predicate (baseline h1 = 261/261, every built carrier already passes; K2's zero-sum half goes vacuous) -> SURVIVE; P3: CA (norm-preserving characters become 0..7) and RC (non-unitary characters in U)"),
 ("L02", "lib", "            if com and not zero_sum(com, L): return None", "            pass",
  "norm_preserving skips the orthogonality test", "yes", "P2: SURVIVE (h1 already 261/261); P3: CA, RC"),
 ("L03", "lib", "    return g, [l % g for l in lev]", "    return 1, [0 for l in lev]",
  "period returns 1 and one class", "yes", "P2: H (with_r_ne_r0 = 0), C2 (none found); X1 would but is already not met in the baseline; P3: CA (r//r0 = 1)"),
 ("L04", "lib", "S[i].append(idx[(z, gadd(g, E[z][y], mod))])", "S[i].append(idx[(z, g)])",
  "lift drops the gain in the successor", "yes", "P2: H (no carrier strongly connected; h1_and_h2 = 0), B1 (pairs = 0), K1; P3: CA (not strongly connected), RC (no carriers)"),
 ("L05", "lib", "    cur = {start: 1}; out = [cur]\n", "    cur = {start: 1}; out = []\n",
  "walk_counts drops length 0 (index t now holds length t+1)", "yes", "P2: SURVIVE (B1, C1 are existence over lengths, B2 holds at every length, X1 already not met); P3: not called -> SURVIVE"),
 ("L06", "lib", "    def conj(self, a):\n        out = self.zero()", "    def conj(self, a):\n        return a\n        out = self.zero()",
  "Ring.conj returns its argument", "yes", "P2: K4 (a^2 is not a solution; baseline K4 met) ; K3 changes but is already not met; P3: Ring not used -> SURVIVE"),
 ("L07", "lib", "def N(self, a): return self.mul(a, self.conj(a))", "def N(self, a): b = self.mul(a, self.conj(a)); return self.mul(b, b)",
  "Ring.N returns |a|^4", "yes", "P2: K4 (|a|^4 does not solve the equations); K3 should NOT notice (keys are in bijection with |a|^2); P3: SURVIVE (not used)"),
 ("L08", "lib", "ev < 1e-9 * max", "ev < 1e-3 * max", "null_space threshold 1e-9 -> 1e-3", "yes", "P2, P3: null_space is not called by either program -> SURVIVE, result bytes identical"),
 ("L09", "lib", "ev < 1e-9 * max", "ev < 1e-15 * max", "null_space threshold 1e-9 -> 1e-15", "yes", "P2, P3: not called -> SURVIVE, result bytes identical"),
 ("L10", "lib", "    return reach(S) and reach(R)", "    return True",
  "strongly_connected always True", "yes", "P2: crash in period (level None on unreachable vertices) or A3; N1 changes but is already not met; P3: CA unaffected, RC carriers 29 -> 30, possibly crash-free -> SURVIVE in P3"),
 ("L11", "lib", "tuple((u + v) % m for u, v, m in zip(a, b, mod))", "tuple((u + v) for u, v, m in zip(a, b, mod))",
  "gadd ignores the modulus entirely", "yes", "P2: crash (KeyError in lift), not a predicate; P3: crash in the return-bound part (block_carrier + lift); CA uses hand-written gains reduced mod 8 so lift on E8 also crashes"),
 ("L12", "lib", "tuple((u + v) % m for u, v, m in zip(a, b, mod))", "tuple((u + v) % mod[0] for u, v, m in zip(a, b, mod))",
  "gadd reduces every component by the first modulus", "yes", "P2: A3 or H/h1 on groups Z2xZ4, Z2xZ6, Z4xZ2 (or KeyError for Z4xZ2); P3: cyclic groups only -> EQUIVALENT there"),
 ("L13", "lib", "def null_dim(M, gap=1e6):", "def null_dim(M, gap=1e1):", "null_dim gap 1e6 -> 1e1", "yes",
  "P2: SURVIVE (recorded gaps are 1e14..1e16, far above both); bytes identical; P3 not called"),
 ("L14", "lib", "def null_dim(M, gap=1e6):", "def null_dim(M, gap=1e15):", "null_dim gap 1e6 -> 1e15", "yes",
  "P2: K3 failure count changes (gaps 1e14..1e15 now give dim 0) but K3 is already not met in the baseline -> predicate verdict unchanged, SURVIVE at predicate level; rerun-compare notices"),
 ("L15", "lib", "else: g = math.gcd(g, lev[v] + 1 - lev[u])", "else: g = math.gcd(g, lev[v] - lev[u])",
  "period: closed-walk length off by one", "yes", "P2: A2/A3 or H or a ZeroDivision crash (g = 0); P3: CA (r)"),
 ("L16", "lib", "    if len(degs) != 1: return None", "    pass",
  "norm_preserving skips the equal out-degree test", "yes", "P2, P3: every carrier built is regular -> SURVIVE, bytes identical"),
 ("L17", "lib", "    return reach(S) and reach(R)", "    return reach(S)",
  "strongly_connected tests forward reachability only", "yes", "P2, P3: all lifts are d-in d-out regular, where forward reachability implies strong connectivity -> SURVIVE, bytes identical"),
 ("P01", "p2", "min(dd[y1].values()) >= 25 and min(dd[y2].values()) >= 25", "min(dd[y1].values()) <= 25 and min(dd[y2].values()) <= 25",
  "program 2, B1: count comparison reversed (>= N becomes <= N)", "yes", "B1 fails for carriers where the full coset first appears with counts above 25 (large groups); if short lengths already show the coset with small counts it SURVIVES"),
 ("P02", "p2", "        if r % r0: fails[\"A2\"] += 1", "        if r0 % r: fails[\"A2\"] += 1",
  "program 2, A2: divisibility reversed (r divides r0)", "yes", "A2 fails on the 17 carriers with r != r0"),
 ("Q01", "p3", "eqs.add(sp.expand(a * X[0] * Y[0] + c * X[1] * Y[1] - (", "eqs.add(sp.expand(a * X[0] * Y[0] - c * X[1] * Y[1] - (",
  "program 3, CD: sign of the c term in the multiplicativity equation", "yes", "CD (solutions become (0,0),(1,0),(0,-1)); CE too"),
 ("Q02", "p3", "        if vec[0] > d ** (t - 1): viol += 1", "        if vec[0] > d ** t: viol += 1",
  "program 3, RB: bound weakened from d^(t-1) to d^t", "yes", "RB cannot fail (N_t <= d^t always); equality_cases is counted on a separate line and stays 7432 -> SURVIVE, bytes identical; RE is a constant, not computed"),
 ("R01", "r3", '"equality_cases": 7432', '"equality_cases": 7433', "stored result of program 3: one digit", "record altered", "rerun and byte comparison"),
 ("R02", "r2", '"with_r_ne_r0": 17', '"with_r_ne_r0": 18', "stored result of program 2: one digit", "record altered", "rerun and byte comparison"),
]
pred = {}
os.makedirs(f"{W}/mutants", exist_ok=True)
def lay(root):
    os.makedirs(f"{root}/lib", exist_ok=True); os.makedirs(f"{root}/reports/{N2}", exist_ok=True); os.makedirs(f"{root}/reports/{N3}", exist_ok=True)
    shutil.copy(SRC["lib"], f"{root}/lib/pcplib.py"); shutil.copy(SRC["p2"], f"{root}/reports/{N2}/{P2}.py"); shutil.copy(SRC["p3"], f"{root}/reports/{N3}/{P3}.py")
if not os.path.exists(f"{W}/base"):
    lay(f"{W}/base")
    shutil.copy(SRC["r2"], f"{W}/base/reports/{N2}/{P2}_results.STORED.json"); shutil.copy(SRC["r3"], f"{W}/base/reports/{N3}/{P3}_results.STORED.json")
for (mid, which, old, new, desc, falsified, prediction) in M:
    root = f"{W}/mutants/{mid}"
    if os.path.exists(root): sys.exit(f"{root} exists; refusing to overwrite")
    lay(root)
    tgt = {"lib": f"{root}/lib/pcplib.py", "p2": f"{root}/reports/{N2}/{P2}.py", "p3": f"{root}/reports/{N3}/{P3}.py",
           "r2": f"{root}/reports/{N2}/{P2}_results.STORED_MUTANT.json", "r3": f"{root}/reports/{N3}/{P3}_results.STORED_MUTANT.json"}[which]
    txt = open(SRC[which]).read()
    if txt.count(old) != 1: sys.exit(f"{mid}: site occurs {txt.count(old)} times")
    txt = txt.replace(old, new)
    if which in ("lib", "p2", "p3"): txt = f"# MUTANT {mid}: {desc}\n" + txt      # JSON carries MUTANT in its file name
    open(tgt, "w").write(txt)
    pred[mid] = dict(file=which, target=os.path.relpath(tgt, W), original_sha256=DIG[which], mutant_sha256=sha(tgt), change=desc,
                     old=old, new=new, true_statement_made_false=falsified, prediction_before_run=prediction)
json.dump(dict(seed=20261113, note="sites chosen by hand, no random choice", originals=DIG, mutants=pred), open(f"{W}/PREDICTIONS.json", "x"), indent=1)
print(len(M), "mutants planted")
