#!/usr/bin/env python3
"""Self-test of pcplib.py with known answers and NEGATIVE controls (inputs on which each test must say no).
Proposed by the chaos run of 14 November 2026: seven planted library errors passed the queue programs because no
program feeds the library an input on which the wrong function differs.  Run: python3 pcplib_selftest.py ; exit 0 = pass.
Thresholds: the null_space cases sit at relative eigenvalue 1e-8 (must be kept) and exact 0 (must be dropped);
the null_dim cases at singular-value ratios 1e3 (below the gap 1e6: dimension 0) and 1e13 (above: dimension 1)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pcplib as L
T = []
def t(name, got, want): T.append((name, got == want, got, want))
t("gadd reduces each component by its own modulus", L.gadd((1, 3), (1, 3), (2, 4)), (0, 2))
t("zero_sum yes: 1 + zeta_2", L.zero_sum([0, 1], 2), True)
t("zero_sum no: 1 + 1", L.zero_sum([0, 0], 2), False)
H = [[(0,), (0,)], [(0,), (1,)]]
t("norm_preserving yes: Hadamard block, k = 1", L.norm_preserving(H, (2,), (1,)), 2)
t("norm_preserving no: trivial character", L.norm_preserving(H, (2,), (0,)), None)
Eirr = [[(0,), (0,), None, None], [(0,), (1,), None, None], [None, None, (0,), None], [None, None, None, (0,)]]
t("norm_preserving no: unequal out-degrees", L.norm_preserving(Eirr, (2,), (1,)), None)
idx, S = L.lift(H, (2,))
t("lift adds the gain", sorted(S[idx[(1, (0,))]]), sorted([idx[(0, (0,))], idx[(1, (1,))]]))
t("strongly_connected yes: 3-cycle", L.strongly_connected([[1], [2], [0]]), True)
t("strongly_connected no: 0 -> 1, 1 -> 1 (forward reach is everything)", L.strongly_connected([[1], [1]]), False)
t("strongly_connected no: 0 -> 0, 1 -> 0", L.strongly_connected([[0], [0]]), False)
t("period of a 3-cycle", L.period([[1], [2], [0]]), (3, [0, 1, 2]))
t("period with a loop", L.period([[0, 1], [0]])[0], 1)
wc = L.walk_counts([[0, 1], [0]], 0, 3)
t("walk_counts lengths 0..3", [dict(c) for c in wc], [{0: 1}, {0: 1, 1: 1}, {0: 2, 1: 1}, {0: 3, 1: 2}])
R = L.Ring(4)
t("Ring.conj of zeta_4", R.conj((0, 1)), (0, -1))
t("Ring.N of 1 + zeta_4", R.N((1, 1)), (2, 0))
R3 = L.Ring(3)
t("Ring.N of 1 - zeta_3", R3.N((1, -1)), (3, 0))
t("null_space keeps relative eigenvalue 1e-8", L.null_space([{0: 10 ** 4}, {1: 1}], 3)[0], 1)
t("null_space zero_col", L.null_space([{0: 10 ** 4}, {1: 1}], 3, zero_col=2)[0], 0)
rng = np.random.RandomState(20261113); B = rng.randint(-1000, 1001, size=(20, 40)); C = rng.randint(-1000, 1001, size=(60, 20)) @ B
t("null_space of a rank-20 integer system in 40 unknowns", L.null_space([{j: int(v) for j, v in enumerate(r)} for r in C], 40)[0], 20)
t("null_dim: ratio 1e3 is not a gap", L.null_dim(np.diag([1.0, 1e-3]))[0], 0)
t("null_dim: ratio 1e13 is a gap", L.null_dim(np.diag([1.0, 1.0, 1e-13]))[0], 1)
t("null_dim: exact kernel", L.null_dim(np.array([[1.0, 1.0], [2.0, 2.0]]))[0], 1)
bad = [x for x in T if not x[1]]
for name, ok, got, want in T: print("ok  " if ok else "FAIL", name, "" if ok else f"got {got!r}, want {want!r}")
print(f"{len(T) - len(bad)} of {len(T)} pass"); sys.exit(1 if bad else 0)
