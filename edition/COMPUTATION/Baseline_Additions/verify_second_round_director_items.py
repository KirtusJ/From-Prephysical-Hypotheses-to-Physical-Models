#!/usr/bin/env python3
"""Part F of the computations for edition Z2. Independent recomputation of items in the second packets of Directors A, B and G."""
import json, math, numpy as np, sympy as sp
from scipy.linalg import null_space
import importlib.util
spec = importlib.util.spec_from_file_location("abc", __import__("os").path.join(__import__("os").path.dirname(__import__("os").path.abspath(__file__)), "transition_geometry_lib.py")); lib = importlib.util.module_from_spec(spec); spec.loader.exec_module(lib)
R, ok = {}, {}
# F1 Director A (A2): directed 3-cycle, C = P - P^T, C^2 = -3 on the zero-sum plane (exact)
P = sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]]); C = P - P.T; Q = sp.eye(3) - sp.ones(3, 3) / 3
ok["F1_C_squared_is_minus_3_on_contrast_plane"] = (C * C + 3 * Q) == sp.zeros(3, 3)
# F2 Director A (A2): Gram determinant 1 - (p12+p23+p31) + 2 sqrt(p12 p23 p31) cos(phi)
a, b, c, ph = sp.symbols('a b c phi', positive=True)
G = sp.Matrix([[1, a, c * sp.exp(-sp.I * ph)], [a, 1, b], [c * sp.exp(sp.I * ph), b, 1]])
ok["F2_gram_determinant_formula"] = sp.simplify(sp.expand_complex(G.det()) - (1 - a**2 - b**2 - c**2 + 2 * a * b * c * sp.cos(ph))) == 0
# F3 Director B (B2): CP^2 triangles with moduli 1/2 and Bargmann phase phi = 0 and 2 pi/3: equal determinant holonomy, different phases;
#    the fan of thin triangles (paper G7, Proposition 4.6) separates them
def triple(phi):
    Gm = np.array([[1, .5, .5 * np.exp(-1j * phi)], [.5, 1, .5], [.5 * np.exp(1j * phi), .5, 1]])
    w, v = np.linalg.eigh(Gm); V = (v * np.sqrt(np.clip(w, 0, None))).conj().T      # columns are the vectors
    return [V[:, i] / np.linalg.norm(V[:, i]) for i in range(3)]
rows = []
for phi in (0.0, 2 * math.pi / 3):
    vs = triple(phi); Qb = null_space(vs[0].conj().reshape(1, 3)); bg = lib.barg(vs)
    T = lib.hol_matrix(vs, Qb); f, _ = lib.fan_phase(vs, Qb, 32)
    rows.append(dict(phi=phi, pair_probabilities=[float(abs(np.vdot(vs[i], vs[(i + 1) % 3])) ** 2) for i in range(3)], arg_B=float(np.angle(bg)),
                     det_holonomy=[float(np.linalg.det(T).real), float(np.linalg.det(T).imag)], fan_recovered_phase=float(np.angle(f))))
R["F3_B2_branch_pair"] = rows
ok["F3_equal_determinants_distinct_phases_separated_by_fan"] = (abs(complex(*rows[0]["det_holonomy"]) - complex(*rows[1]["det_holonomy"])) < 1e-10
    and abs(rows[0]["fan_recovered_phase"] - 0) < 1e-10 and abs(rows[1]["fan_recovered_phase"] - 2 * math.pi / 3) < 1e-10)
# F4 Director G (second packet): interpolated composites K_t
t = sp.symbols('t', nonnegative=True)
bell = sp.Rational(1, 2) * (1 + t)                      # sup over K_t of Tr(P rho) = (1-t) * 1/2 + t
prodE = 1 - (1 - bell) ** 2                             # Tr E (rho_t x rho_t), E = 1 - (1-P)x(1-P)
bound = (1 - t) * sp.Rational(3, 4) + t                 # sup over (1-t) Sep_4 + t D_4
ok["F4_gap_is_t(1-t)/4"] = sp.simplify(prodE - bound - t * (1 - t) / 4) == 0
# numerical confirmation of the two suprema used: product states give pair fidelity <= 1/2, hence Tr E <= 3/4
rng = np.random.default_rng(7); Pb = np.zeros((4, 4)); Pb[np.ix_([0, 3], [0, 3])] = .5
best = 0
for _ in range(20000):
    q = [rng.normal(size=2) + 1j * rng.normal(size=2) for _ in range(4)]; q = [x / np.linalg.norm(x) for x in q]
    f1 = np.vdot(np.kron(q[0], q[1]), Pb @ np.kron(q[0], q[1])).real; f2 = np.vdot(np.kron(q[2], q[3]), Pb @ np.kron(q[2], q[3])).real
    best = max(best, 1 - (1 - f1) * (1 - f2))
R["F4_max_E_on_sampled_product_states"] = float(best)
ok["F4_product_states_bound_three_quarters"] = best <= 0.75 + 1e-12
tt = 0.5; rho = (1 - tt) * np.diag([1.0, 0, 0, 0]) + tt * Pb
Z = np.diag([1.0, -1]); X = np.array([[0, 1.0], [1, 0]]); B0 = (Z + X) / 2 ** .5; B1 = (Z - X) / 2 ** .5
chsh = np.kron(Z, B0) + np.kron(Z, B1) + np.kron(X, B0) - np.kron(X, B1)
R["F4_chsh_at_half"] = float(np.trace(rho @ chsh).real)
ok["F4_chsh_is_sqrt2(1+t)"] = abs(R["F4_chsh_at_half"] - 2 ** .5 * 1.5) < 1e-12
R["ok"] = ok; ok = {k: bool(v) for k, v in ok.items()}; R["ok"] = ok; json.dump(R, open("Second_Round_Director_Items_Results.json", "w"), indent=1)
for k, v in ok.items(): print(("PASS " if v else "FAIL ") + k)
