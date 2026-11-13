"""Normalized real entanglement swapping with a specified endpoint-plane grade.

Run python -B check_independent_source_phase.py OUTPUT_DIRECTORY. Tables use
exact [a,b] coefficients for a+b/sqrt(2). Direct real-projector traces verify
each outcome independently before writing the exact reconstruction.
"""

import argparse
import json
from fractions import Fraction as F
from itertools import product
from math import sqrt
from pathlib import Path

import numpy as np

I = np.eye(2)
J = np.array([[0.0, -1.0], [1.0, 0.0]])
X = np.array([[0.0, 1.0], [1.0, 0.0]])
Z = np.diag([1.0, -1.0])
Q = -np.kron(J, J)
AXES = ("Z", "X", "Y")
PAIRS = (("Z", "X"), ("Z", "Y"), ("X", "Y"))
SIGNS = (1, -1)
OUTCOMES = tuple(product(SIGNS, repeat=2))
BELLS = ((0, 0), (1, 0), (0, 1), (1, 1))  # parity, phase: Phi+, Psi+, Phi-, Psi-
OBS = {"Z": np.kron(Z, I), "X": np.kron(X, I), "Y": np.kron(J, J)}


def bell(p, s):
    v = np.zeros((2, 2))
    for i in range(2):
        v[i, i ^ p] = (-1) ** (s * i) / sqrt(2)
    return v


def bsign(x, p, s):
    return {"Z": (-1) ** p, "X": (-1) ** s, "Y": -((-1) ** (p + s))}[x]


def factorize(grade_rho, swapped):
    """Tensor convention (Adata,Aplane,Cdata,Cplane)."""
    rho = np.kron(np.outer(swapped, swapped), grade_rho)
    return rho.reshape((2,) * 8).transpose(0, 2, 1, 3, 4, 6, 5, 7).reshape(16, 16)


def write_coeff(c):
    return [str(v) for v in c]


def numeric(c):
    return float(c[0]) + float(c[1]) / sqrt(2)


def effect_table():
    settings = []
    for j, x in enumerate(AXES):
        for z, (pair, orient) in enumerate(product(PAIRS, SIGNS)):
            i, l = pair
            alice = OBS[x]
            charlie = (OBS[i] + orient * OBS[l]) / sqrt(2)
            assert np.allclose(charlie @ charlie, np.eye(4)) and np.allclose(alice @ alice, np.eye(4))
            effects = [
                np.kron((np.eye(4) + a * alice) / 2, (np.eye(4) + c * charlie) / 2) for a, c in OUTCOMES
            ]
            assert np.allclose(sum(effects), np.eye(16))
            settings.append((j, z, x, pair, orient, effects))
    return settings


def experiment(nu, settings):
    plane = (np.eye(4) + float(nu) * Q) / 4
    assert np.min(np.linalg.eigvalsh(plane)) >= -1e-14 and np.isclose(np.trace(plane), 1)
    assert np.allclose(np.trace(plane.reshape(2, 2, 2, 2), axis1=1, axis2=3), I / 2)
    assert np.isclose(np.trace(Q @ plane), float(nu))
    # A,B1,B2,C. Bob contracts the actual B1,B2 coordinates, retaining
    # the unnormalized (joint with his outcome) A,C vector.
    source = np.kron(bell(0, 0).flatten(), bell(0, 0).flatten()).reshape(2, 2, 2, 2)
    assert np.isclose(np.vdot(source, source), 1)
    states = []
    for p, s in BELLS:
        swapped = np.einsum("ijkl,jk->il", source, bell(p, s)).flatten()
        assert np.allclose(swapped, bell(p, s).flatten() / 2)
        full = factorize(plane, swapped)
        grade = [factorize((P @ plane @ P), swapped) for g in SIGNS for P in [(np.eye(4) + g * Q) / 2]]
        assert np.allclose(sum(grade), full) and np.isclose(np.trace(full), 0.25)
        states.append((full, grade))
    outputs = []
    score = [F()] * 3
    score_grade = [[F()] * 3 for g in SIGNS]
    for j, z, x, pair, orient, effects in settings:
        d = 1 if x == pair[0] else orient if x == pair[1] else 0
        joint_total = F()
        bell_rows = []
        for (p, s), (full, grades) in zip(BELLS, states):
            coeff = []
            grade_coeff = [[], []]
            for (a, c), eff in zip(OUTCOMES, effects):
                # Raw joint probability P(a,b,c | x,z), so its offset is 1/16.
                v = a * c * bsign(x, p, s) * d
                nums = (F(1, 16), F(v, 16) * (nu if x == "Y" else 1))
                assert abs(np.trace(eff @ full) - numeric(nums)) < 2e-14
                joint_total += nums[0]
                coeff.append(write_coeff(nums))
                if d:
                    score[z // 2] += a * c * bsign(x, p, s) * d * nums[1]
                split = []
                for gi, (g, grho) in enumerate(zip(SIGNS, grades)):
                    mass = (1 + g * nu) / 2
                    cond = (F(1, 16), F(v * (g if x == "Y" else 1), 16))
                    branch = tuple(t * mass for t in cond)
                    assert abs(np.trace(eff @ grho) - numeric(branch)) < 2e-14
                    split.append(branch)
                    grade_coeff[gi].append(write_coeff(branch))
                    if d:
                        score_grade[gi][z // 2] += a * c * bsign(x, p, s) * d * branch[1]
                assert tuple(sum(t) for t in zip(*split)) == nums
            assert sum(F(v[1]) for v in coeff) == 0
            bell_rows.append({"b": [p, s], "all_grades": coeff, "grade_joint": grade_coeff})
        assert joint_total == 1
        outputs.append({"x": j + 1, "z": z + 1, "bell_rows": bell_rows})
    assert score == [4, 2 * (1 + nu), 2 * (1 + nu)] and sum(score) == 4 * (2 + nu)
    cond_scores = []
    for gi, g in enumerate(SIGNS):
        mass = (1 + g * nu) / 2
        normed = [t / mass for t in score_grade[gi]] if mass else None
        assert normed is None or normed == [4, 2 * (1 + g), 2 * (1 + g)]
        cond_scores.append(
            {
                "grade": g,
                "mass": str(mass),
                "joint_CHSH_numerators": list(map(str, score_grade[gi])),
                "conditional_CHSH_numerators": list(map(str, normed)) if normed is not None else None,
            }
        )
    return {
        "nu": str(nu),
        "full_table": outputs,
        "CHSH_numerators_over_sqrt2": list(map(str, score)),
        "score_numerator_over_sqrt2": str(sum(score)),
        "grades": cond_scores,
    }


def partition():
    # Two local reference collections, each internally grade-correlated.
    # Q projects one selected plane from each source collection. Marginal Q
    # across the source cut is zero for all real local source states.
    rho_plus = (np.eye(4) + Q) / 4
    rows = []
    for a, c in product((1, 2), repeat=2):
        left = I / 2 if a == 1 else rho_plus
        right = I / 2 if c == 1 else rho_plus
        joint = np.kron(left, right)
        cut = -np.kron(np.kron(np.eye(2 ** (a - 1)), J), np.kron(J, np.eye(2 ** (c - 1))))
        grade = np.trace(cut @ joint)
        assert abs(grade) < 1e-14 and np.isclose(np.trace(joint), 1)
        rows.append({"left_planes": a, "right_planes": c, "cross_cut_grade": "0"})
    return rows


def main():
    settings = effect_table()
    return {
        "states": [experiment(nu, settings) for nu in map(F, (-1, 0, F(1, 2), 1))],
        "partitions": partition(),
        "table_encoding": "Each fixed (x,z) stores P(a,b,c | x,z) jointly, without normalization by Bob success. The four endpoint outcomes are (+,+),(+,-),(-,+),(-,-). Each number [r,s] is exactly r+s/sqrt(2). grade_joint lists raw probabilities including grade flag in order +1,-1. Grade-conditional probabilities are grade_joint divided by its stated grade mass when positive; a zero-mass conditional law is undefined. All scores use units of 1/sqrt(2).",
        "convention": "Alice x=1,2,3: Z,X,Y. Charlie z=1..6: (Z+X,Z-X,Z+Y,Z-Y,X+Y,X-Y)/sqrt(2). Bob (p,s) labels (Phi+,Psi+,Phi-,Psi-)=(00,10,01,11), parity then phase. The scoring sign for an included axis is its coefficient sign in Charlie's combination times the complex Bell correlation sign Z=(-1)^p, X=(-1)^s, Y=-(-1)^(p+s), times a*c. This is the Renou endpoint convention. Wu et al. put the six settings at Alice and the three at Claire, so transposing endpoint names and using Bell names avoids an integer-label ambiguity.",
        "apparatus": "Two real data Bell pairs AB1 and B2C, Bob's complete real Bell measurement, and endpoint plane state (I+nu Q)/4, Q=-J tensor J. Alice/Charlie use X,Z on their respective data only and Y=J_data tensor J_plane. Plane eigenvalues are (1+nu)/4 twice, (1-nu)/4 twice; marginals are I/2. At nu=0 both sources are independent across the full source cut. For nonzero nu, the data sources are still a product but the stipulated endpoint plane state supplies extra real correlations across that cut. Any separable real mixture across the cut has zero Q mean because every local density has zero J trace. Conditioning on a distinguished relative grade requires access to an additional joint measurement or common resource, and no such conditioning is used in the all-grade score. The calculation does not optimize over real network devices, estimate an observed grade, or fit experimental frequencies.",
        "primary_sources": {
            "Renou et al., network witness and real-source constraints": "https://doi.org/10.1038/s41586-021-04160-4",
            "Dian Wu et al., strict-locality optical experiment": "https://doi.org/10.1103/PhysRevLett.129.140401",
            "Wu et al., open methods and endpoint convention": "https://arxiv.org/abs/2201.04177",
        },
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    out = parser.parse_args().directory
    data = main()
    out.mkdir(parents=True, exist_ok=True)
    (out / "independent_source_phase.json").write_bytes(
        (json.dumps(data, separators=(",", ":")) + "\n").encode()
    )
    print(
        len(data["states"]),
        "plane states;",
        4 * 3 * 6 * 4 * 4,
        "unconditional and",
        2 * 4 * 3 * 6 * 4 * 4,
        "grade-resolved probabilities.",
    )
