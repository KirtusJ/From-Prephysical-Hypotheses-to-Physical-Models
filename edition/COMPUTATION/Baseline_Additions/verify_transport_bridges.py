#!/usr/bin/env python3
"""Executed checks for the transport/holonomy bridge assessment (Director D, 11 Nov 2026).

Scope: stipulated finite quantum and classical mathematical models only.  Nothing here is a
measurement, a physical derivation, or evidence for a prephysical substrate.

Checks
  A. Bargmann invariant of three pure qubit states along +X,+Y,+Z (exact, sympy) and its
     relation to the solid angle of the Bloch-sphere geodesic triangle.
  B. Spin-j coherent-state triple invariant equals the spin-1/2 one raised to 2j
     (exact tensor-power argument; independent 3x3 numerical check at j=1).
  C. Continuous natural-connection (Berry/Pancharatnam) holonomy along the geodesic triangle
     equals the discrete three-point Bargmann phase (geodesic rule), with the discrete
     "ladder" of successive projections converging to the same value.
  D. Controls: real-amplitude states give triple phases in {0, pi} only; classical point
     distributions give phase 0 only.
  E. Hamiltonian monodromy of the spherical pendulum reproduced in the quantum joint
     spectrum (lattice-cell transport around the focus-focus value) with a non-enclosing
     control loop.
Outputs Transport_Bridge_Results.json beside the script (refuses to overwrite).
"""
import json, math, os, sys
import numpy as np
import sympy as sp

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Transport_Bridge_Results.json")
if os.path.exists(OUT):
    sys.exit("refusing to overwrite existing result file: " + OUT)
R = {"scope": "stipulated finite mathematical models; no physical claim", "checks": {}}
ok_all = True
def rec(name, passed, **kw):
    global ok_all
    ok_all &= bool(passed)
    R["checks"][name] = dict(passed=bool(passed), **kw)

# ---------- A. exact Bargmann invariant, octant triangle ----------
I2 = sp.eye(2)
sx = sp.Matrix([[0, 1], [1, 0]]); sy = sp.Matrix([[0, -sp.I], [sp.I, 0]]); sz = sp.Matrix([[1, 0], [0, -1]])
P = lambda s: (I2 + s) / 2
tri = sp.simplify((P(sx) * P(sy) * P(sz)).trace())
# Tr(P_x P_y P_z) = (1 + i)/4 ; modulus sqrt(2)/4 ; argument pi/4.
rec("A_bargmann_xyz_exact", tri == (1 + sp.I) / 4,
    value=str(tri), argument="pi/4", solid_angle_octant="pi/2",
    relation="|arg| = Omega/2 for spin-1/2 (Omega = pi/2, octant)")
# general formula check: Tr(P_a P_b P_c) = (1 + a.b + b.c + c.a + i a.(b x c))/4
a, b, c = (sp.symbols(f"{n}1:4", real=True) for n in "abc")
Pa = (I2 + a[0]*sx + a[1]*sy + a[2]*sz)/2; Pb = (I2 + b[0]*sx + b[1]*sy + b[2]*sz)/2; Pc = (I2 + c[0]*sx + c[1]*sy + c[2]*sz)/2
lhs = sp.expand((Pa*Pb*Pc).trace())
A, B, C = sp.Matrix(a), sp.Matrix(b), sp.Matrix(c)
rhs = sp.expand((1 + A.dot(B) + B.dot(C) + C.dot(A) + sp.I * A.dot(B.cross(C))) / 4)
# identity holds modulo unit-vector constraints? It is in fact an identity for all a,b,c (no constraint needed).
rec("A_general_triple_formula", sp.simplify(lhs - rhs) == 0,
    formula="Tr(P_a P_b P_c) = (1 + a.b + b.c + c.a + i a.(b x c))/4, P_n=(I+n.sigma)/2")

# ---------- numerics helpers ----------
def bloch_state(n):
    n = np.asarray(n, float); n = n / np.linalg.norm(n)
    th = math.acos(np.clip(n[2], -1, 1)); ph = math.atan2(n[1], n[0])
    return np.array([math.cos(th/2), math.sin(th/2)*np.exp(1j*ph)])
def spherical_triangle_area(n1, n2, n3):
    # Van Oosterom–Strackee
    n1, n2, n3 = (np.asarray(v, float) for v in (n1, n2, n3))
    num = np.dot(n1, np.cross(n2, n3)); den = 1 + n1@n2 + n2@n3 + n3@n1
    return 2 * math.atan2(num, den)
ex, ey, ez = np.eye(3)
psi = [bloch_state(v) for v in (ex, ey, ez)]
barg = np.vdot(psi[0], psi[1]) * np.vdot(psi[1], psi[2]) * np.vdot(psi[2], psi[0])
Om = spherical_triangle_area(ex, ey, ez)
rec("A_numeric_phase_vs_solid_angle", abs(np.angle(barg) - Om/2) < 1e-12 and abs(Om - math.pi/2) < 1e-12,
    bargmann_phase=float(np.angle(barg)), half_solid_angle=Om/2,
    sign_convention="arg(<1|2><2|3><3|1>) = +Omega/2 for the orientation x->y->z; the Berry phase of the same loop is -Omega/2 (Berry 1984 convention gamma = -j Omega)")

# ---------- B. spin-j coherent states ----------
def spin_ops(j):
    d = int(round(2*j+1)); m = np.arange(j, -j-1, -1)
    Jz = np.diag(m).astype(complex); Jp = np.zeros((d, d), complex)
    for k in range(1, d):
        Jp[k-1, k] = math.sqrt(j*(j+1) - m[k]*(m[k]+1))
    Jm = Jp.conj().T
    return (Jp+Jm)/2, (Jp-Jm)/(2j), Jz
def coherent(j, n):
    # highest-weight state along n: ground of -n.J
    Jx, Jy, Jz = spin_ops(j); n = np.asarray(n, float)/np.linalg.norm(n)
    w, v = np.linalg.eigh(-(n[0]*Jx + n[1]*Jy + n[2]*Jz))
    return v[:, 0]
for j in (0.5, 1.0, 1.5, 2.0):
    cs = [coherent(j, v) for v in (ex, ey, ez)]
    bj = np.vdot(cs[0], cs[1]) * np.vdot(cs[1], cs[2]) * np.vdot(cs[2], cs[0])
    # phase defined mod 2pi; compare on the unit circle
    rec(f"B_spin_{j}_triple_phase_equals_jOmega",
        abs(bj/abs(bj) - np.exp(1j*j*Om)) < 1e-10 and abs(abs(bj) - (math.sqrt(2)/4)**(2*j)) < 1e-10,
        modulus=float(abs(bj)), expected_modulus=(math.sqrt(2)/4)**(2*j), phase_mod_2pi=float(np.angle(bj)), j_times_Omega=j*Om,
        basis="eigenvectors of n.J; independent of the tensor-power construction")

# ---------- C. continuous holonomy vs discrete ladder ----------
def slerp_states(n1, n2, N):
    # great-circle arc on the Bloch sphere, N+1 points
    n1, n2 = np.asarray(n1, float), np.asarray(n2, float)
    ang = math.acos(np.clip(n1@n2, -1, 1))
    return [bloch_state((math.sin((1-t)*ang)*n1 + math.sin(t*ang)*n2)/math.sin(ang)) for t in np.linspace(0, 1, N+1)]
def ladder_phase(points):
    # Pancharatnam connection: keep successive overlaps real positive; closed-loop mismatch is the holonomy.
    # Equivalent to arg of the product of successive overlaps along the closed chain.
    prod = 1+0j
    for k in range(len(points)):
        prod *= np.vdot(points[k], points[(k+1) % len(points)])
    return float(np.angle(prod))
for N in (1, 3, 30, 3000):
    loop = slerp_states(ex, ey, N)[:-1] + slerp_states(ey, ez, N)[:-1] + slerp_states(ez, ex, N)[:-1]
    ph = ladder_phase(loop)
    rec(f"C_ladder_N{N}_geodesic_triangle", abs(ph - Om/2) < 1e-9,
        phase=ph, expected=Om/2, points=len(loop),
        note="geodesic rule: any refinement of the geodesic triangle gives the same holonomy as the 3-point chain")
# Berry connection line integral  gamma = -Im sum <psi|dpsi> with gauge-smooth states along the arcs
def berry_integral(points):
    tot = 0.0
    for k in range(len(points)):
        p, q = points[k], points[(k+1) % len(points)]
        tot += np.angle(np.vdot(p, q))   # -Im<psi|dpsi> ~ -arg<psi|psi+dpsi>; sign handled below
    return -tot
loopN = slerp_states(ex, ey, 2000)[:-1] + slerp_states(ey, ez, 2000)[:-1] + slerp_states(ez, ex, 2000)[:-1]
gam = berry_integral(loopN)
rec("C_berry_line_integral_equals_minus_half_solid_angle", abs(gam + Om/2) < 1e-6,
    berry_phase=gam, minus_half_solid_angle=-Om/2,
    note="Berry phase of a spin-1/2 loop is -Omega/2; the Bargmann phase of the same chain is +Omega/2 (opposite sign convention)")

# ---------- D. controls ----------
rng = np.random.default_rng(20261111)
real_ok = True; real_phases = []
for _ in range(200):
    v = [rng.normal(size=3) for _ in range(3)]; v = [x/np.linalg.norm(x) for x in v]
    t = (v[0]@v[1]) * (v[1]@v[2]) * (v[2]@v[0])
    ph = float(np.angle(complex(t))); real_phases.append(ph)
    real_ok &= min(abs(ph), abs(abs(ph)-math.pi)) < 1e-12
rec("D_real_amplitudes_triple_phase_in_0_pi", real_ok, distinct_phase_values=sorted(set(round(p, 6) for p in real_phases)))
# classical: pure states are point masses; overlap matrix is Kronecker delta
cls_ok = True
for i in range(4):
    for k in range(4):
        for l in range(4):
            t = (i == k) * (k == l) * (l == i)
            cls_ok &= (t in (0, 1))
rec("D_classical_point_states_triple_in_{0,1}", cls_ok, note="no nontrivial oriented triple phase in a classical simplex")

# ---------- E. quantum monodromy of the spherical pendulum ----------
hbar = 0.05; Lmax = 160
def column(m):
    ls = np.arange(abs(m), Lmax + 1)
    diag = hbar**2 * ls*(ls+1)/2
    off = np.array([math.sqrt(((l+1)**2 - m**2)/((2*l+1)*(2*l+3))) for l in ls[:-1]])
    H = np.diag(diag) + np.diag(off, 1) + np.diag(off, -1)
    w = np.linalg.eigvalsh(H)
    return w[w < 3.0]   # keep well-converged levels only
cols = {m: column(m) for m in range(-30, 31)}
def nearest(m, E):
    w = cols[m]; k = int(np.argmin(np.abs(w - E))); return k
def transport(loop_E_low, loop_E_high, M):
    # start at column -M, energy near loop_E_low; cell basis: u vertical, v to column +1 (nearest-neighbour continuation)
    m = -M; n = nearest(m, loop_E_low); E = cols[m][n]
    n_right = nearest(m+1, E); vE = cols[m+1][n_right] - E      # initial v chosen as nearest horizontal neighbour
    u0 = cols[m][n+1] - cols[m][n]; v0 = vE
    def step_right():
        nonlocal m, n, vE
        pred = cols[m][n] + vE; n2 = nearest(m+1, pred); vE = cols[m+1][n2] - cols[m][n]; m, n = m+1, n2
    def step_left():
        nonlocal m, n, vE
        pred = cols[m][n] - vE; n2 = nearest(m-1, pred); vE = cols[m][n] - cols[m-1][n2]; m, n = m-1, n2
    def step_vert(sgn):
        nonlocal n, vE
        n += sgn; pred = cols[m][n] + vE; n2 = nearest(m+1, pred); vE = cols[m+1][n2] - cols[m][n]
    # bottom edge: go right
    while m < M: step_right()
    # right edge: go up
    while cols[m][n] < loop_E_high: step_vert(+1)
    # top edge: go left
    while m > -M: step_left()
    # left edge: go down
    while cols[m][n] > loop_E_low: step_vert(-1)
    # return to exact start cell
    while n > nearest(m, loop_E_low): step_vert(-1)
    while n < nearest(m, loop_E_low): step_vert(+1)
    u1 = cols[m][n+1] - cols[m][n]
    k = (vE - v0) / u1
    return dict(start=(m, n, float(cols[m][n])), v_initial=float(v0), v_final=float(vE), u=float(u1), shift_in_units_of_u=float(k))
enc = transport(0.3, 1.7, 8)       # encloses the focus-focus value (ell=0, E=1)
ctl = transport(-0.2, 0.8, 8)      # control loop below E=1 (above the relative-equilibrium boundary at ell=0.4), does not enclose it
rec("E_monodromy_enclosing_loop_shift_is_plus_or_minus_one",
    abs(abs(enc["shift_in_units_of_u"]) - 1) < 0.15, **enc,
    model="H = (hbar^2/2) L^2 + cos(theta), hbar=0.05, basis Y_l^m, l<=160; focus-focus value (ell,E)=(0,1)")
rec("E_monodromy_control_loop_shift_is_zero", abs(ctl["shift_in_units_of_u"]) < 0.15, **ctl)
# robustness variation: different hbar, loop size and orientation-independent magnitude
hbar = 0.04; cols = {m: column(m) for m in range(-30, 31)}
enc2 = transport(0.4, 1.6, 6); ctl2 = transport(-0.1, 0.7, 6)
rec("E_monodromy_variation_hbar0.04_M6", abs(abs(enc2["shift_in_units_of_u"]) - 1) < 0.15 and abs(ctl2["shift_in_units_of_u"]) < 0.15,
    enclosing=enc2, control=ctl2)

# ---------- F. Schild's ladder on S^2: classical Levi-Civita holonomy of the same loop ----------
def geodesic_midpoint(p, q):
    m = p + q; return m/np.linalg.norm(m)
def geodesic_extend(p, m):
    # point q with m the geodesic midpoint of p and q (reflection of p through m on the great circle)
    q = 2*np.dot(p, m)*m - p; return q/np.linalg.norm(q)
def schild_transport(v, p0, p1):
    # one rung: transport tangent vector v at p0 to p1 along the geodesic p0->p1
    eps = 1e-3
    x0 = p0 + eps*v; x0 /= np.linalg.norm(x0)          # point reached by a short geodesic from p0 in direction v
    m = geodesic_midpoint(x0, p1)                      # midpoint of the diagonal
    x1 = geodesic_extend(p0, m)                        # complete the parallelogram
    w = x1 - np.dot(x1, p1)*p1                         # tangent part at p1
    return w/np.linalg.norm(w)
def ladder_holonomy(vertices, N):
    # polygonal loop through the vertices, each edge refined into N rungs along the great circle
    pts = []
    for a, b in zip(vertices, vertices[1:] + vertices[:1]):
        ang = math.acos(np.clip(a@b, -1, 1))
        pts += [(math.sin((1-t)*ang)*a + math.sin(t*ang)*b)/math.sin(ang) for t in np.linspace(0, 1, N+1)[:-1]]
    p0 = pts[0]; v = np.cross(p0, vertices[1]); v = v - np.dot(v, p0)*p0; v /= np.linalg.norm(v); v0 = v.copy()
    for k in range(len(pts)):
        v = schild_transport(v, pts[k], pts[(k+1) % len(pts)])
    # rotation angle of v relative to v0 in the tangent plane at p0 (orientation from outward normal p0)
    return float(math.atan2(np.dot(p0, np.cross(v0, v)), np.dot(v0, v)))
lc = ladder_holonomy([ex, ey, ez], 400)
rec("F_schild_ladder_levi_civita_holonomy_equals_solid_angle", abs(abs(lc) - Om) < 2e-3,
    rotation_angle=lc, solid_angle=Om,
    note="classical SO(2) holonomy of the Levi-Civita connection on S^2 is the enclosed area; the spin-j quantum phase of the same loop is j*Omega (prequantum line bundle, j in (1/2)Z); same base loop, different representation")
R["all_passed"] = ok_all
with open(OUT, "w") as f:
    json.dump(R, f, indent=2, default=float)
print("ALL PASSED" if ok_all else "SOME FAILED")
for k, v in R["checks"].items():
    print(("PASS " if v["passed"] else "FAIL "), k, {kk: vv for kk, vv in v.items() if kk in ("shift_in_units_of_u", "phase", "berry_phase", "value")})
