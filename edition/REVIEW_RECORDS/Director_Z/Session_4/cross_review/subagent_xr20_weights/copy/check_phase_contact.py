"""At-contact comparison of two real planes and physical sheet reflections.

Run python -B check_phase_contact.py OUTPUT_DIRECTORY. Site and sheet ports use
integer signed histories and exact squared probabilities; Fourier diagnostics
provide a separate finite-sector check.
"""

import argparse
import cmath
import json
from collections import Counter
from fractions import Fraction as F
from math import cos, pi, sin
from pathlib import Path


def clean(v):
    return {p: x for p, x in v.items() if x}


def norm(v):
    return sum(x * x for x in v.values())


def apply(v, step):
    out = Counter()
    for p, x in v.items():
        dest, s = step(p)
        out[dest] += s * x
    return clean(out)


def combine(v, w, s):
    out = Counter(v)
    for p, x in w.items():
        out[p] += s * x
    return clean(out)


def overlap(v, step):
    w = apply(v, step)
    return F(sum(x * w.get(p, 0) for p, x in v.items()), norm(v))


def quarter(bit):
    return 1 - bit, 1 - 2 * bit


def qstep(p):
    y, i, z, j = p
    u, s = quarter(i)
    v, t = quarter(j)
    return (y, u, z, v), -s * t


def grade(v, sgn):
    # First H from pointer 0 makes both copies positive. Q acts only on
    # pointer 1. Terminal H sums or differences the amplitudes by pointer.
    return combine(v, apply(v, qstep), sgn)


def correct(v, q, plane, sheet):
    return apply(
        v, lambda p: ((p[0], p[1], (-p[2] if sheet else p[2]) % q, p[3]), 1 - 2 * p[3] if plane else 1)
    )


def prep(q, abc, depth):
    a, b, c = abc
    assert a * a + b * b == c * c
    src = {(0, 0): 1}
    for _ in range(depth):
        out = Counter()
        for (y, i), v in src.items():
            j, s = quarter(i)
            out[(y + 1) % q, i] += c * v
            out[y, i] += a * v
            out[y, j] += b * s * v
        src = clean(out)
    return src


def local_sine(q):
    def step(p):
        y, i, z, j = p
        v, t = quarter(j)
        return (y, i, (z - 1) % q, v), t

    return step


def joint_shift(q, r, da, db):
    return lambda p: (((p[0] + da) % q, p[1], (p[2] + db) % r, p[3]), 1)


def sectors(src, q):
    energy = norm(src)
    mass = {}
    for k in range(q):
        for s in (1, -1):
            # T|y>=|y+1> has eigenfunction exp(-2 pi i k y/q);
            # J's eigenvector with eigenvalue si is (1,-si)/sqrt(2).
            amp = sum(
                v * cmath.exp(2j * pi * k * y / q) * (1j * s if i else 1) for (y, i), v in src.items()
            )
            mass[k, s] = abs(amp) ** 2 / (2 * q * energy)
    assert abs(sum(mass.values()) - 1) < 1e-12
    return mass


def clock_trial(q, r, rotA, rotB, nA, nB):
    av, bv = prep(q, rotA, nA), prep(r, rotB, nB)
    src = {(y, i, z, j): u * v for (y, i), u in av.items() for (z, j), v in bv.items()}
    a, b = sectors(av, q), sectors(bv, r)
    E = norm(src)
    rows = []
    for flag in (1, -1):
        after = grade(src, flag)
        assert norm(after) == 2 * E and not grade(after, -flag)
        assert norm(grade(after, flag)) == 4 * norm(after)
        assert correct(apply(after, qstep), r, True, True) == {
            p: -x for p, x in apply(correct(after, r, True, True), qstep).items()
        }
        for label, zflip, reflect in (
            ("none", False, False),
            ("plane_only", True, False),
            ("sheet_only", False, True),
            ("both", True, True),
        ):
            zflip = zflip and flag == -1
            reflect = reflect and flag == -1
            end = correct(after, r, zflip, reflect)
            grade_out = overlap(end, qstep)
            assert grade_out == flag * (-1 if zflip else 1)
            merged = overlap(end, joint_shift(q, r, 1, 1))
            bsine = overlap(end, local_sine(r))
            pg = good = jc = ls = 0.0
            for (ka, sa), pa in a.items():
                for (kb, sb), pb in b.items():
                    if sa * sb != flag:
                        continue
                    prob = 2 * pa * pb
                    pg += prob
                    kf = (-kb if reflect else kb) % r
                    sf = -sb if zflip else sb
                    good += prob * (kf == sf % r)
                    jc += prob * cos(2 * pi * (ka / q + kf / r))
                    ls += prob * sf * sin(2 * pi * kf / r)
            assert (
                abs(pg - 1) < 1e-12
                and abs(float(merged) - jc) < 1e-12
                and abs(float(bsine) - ls) < 1e-12
            )
            rows.append(
                {
                    "flag": flag,
                    "feedforward": label,
                    "grade_after": str(grade_out),
                    "B_target_char_plane_probability": good,
                    "B_T_vs_J_contrast": str(bsine),
                    "both_strokes_vs_idle_cosine": str(merged),
                    "remaining_record_mass": "1/2",
                }
            )
    return {
        "orders": [q, r],
        "rational_rotations": [rotA, rotB],
        "bright_depths": [nA, nB],
        "local_joint_bright_heralds": [
            str(F(norm(src0), (2 * rot[2]) ** (2 * n)))
            for src0, rot, n in ((av, rotA, nA), (bv, rotB, nB))
        ],
        "before_contact_grade_contrast": str(overlap(src, qstep)),
        "before_joint_stroke_cosine": str(overlap(src, joint_shift(q, r, 1, 1))),
        "joint_same_grade_twice_without_reset": "1/2",
        "joint_same_named_grade_fresh_twice": "1/4",
        "unnormalized_local_inputs": [[[*k, v] for k, v in sorted(src0.items())] for src0 in (av, bv)],
        "after": rows,
    }


def logical():
    # (y,i,z,j) = arbitrary idle A spectator, A plane, B data, B plane.
    # Realification of qubit (1,i)/sqrt(2), initially A's plane is |0>.
    src = {(0, 0, 0, 0): 1, (0, 0, 1, 1): 1}
    blank = {(0, 0, 0, 0): 1}

    def observable(p):
        y, i, z, j = p
        u, s = quarter(i)
        v, t = quarter(z)
        return (y, u, v, j), s * t

    rows = []
    for g in (1, -1):
        pre = grade(src, g)
        assert norm(pre) == 2 * norm(src)
        if g == -1:
            pre = correct(pre, 2, True, False)
        assert overlap(pre, qstep) == 1 and overlap(pre, observable) == g
        # Produce logical data after alignment: H splits the data coordinate,
        # controlled J on the shared positive plane inserts the phase i.
        post = grade(blank, g)
        if g == -1:
            post = correct(post, 2, True, False)
        after = Counter(post)
        for (y, i, z, j), v in post.items():
            u, s = quarter(i)
            after[y, u, 1, j] += s * v
        assert overlap(after, observable) == 1
        rows.append(
            {
                "flag": g,
                "precontact_encoded_plus_i_contrast": str(overlap(pre, observable)),
                "postcontact_encoded_plus_i_contrast": str(overlap(after, observable)),
                "positive_grade_after": str(overlap(pre, qstep)),
            }
        )
    # Partial transpose on B of the Bell projector: a/b spectator vector
    # (|01>-|10>)/sqrt(2) witnesses non-positivity of this extension.
    rho = {(0, 0, 0, 0): F(1, 2), (1, 1, 1, 1): F(1, 2), (0, 0, 1, 1): F(1, 2), (1, 1, 0, 0): F(1, 2)}
    pt = {(s, v, t, u): x for (s, u, t, v), x in rho.items()}
    psi = {(0, 1): 1, (1, 0): -1}
    e = sum(psi.get((s, u), 0) * v * psi.get((t, w), 0) for (s, u, t, w), v in pt.items()) / 2
    assert e == F(-1, 2)
    return {"fixed_Y_port": rows, "anchored_Bell_partial_transpose_antisymmetric_expectation": str(e)}


def mixed_controls():
    q = 8
    av = prep(q, (3, 4, 5), 3)
    bv = prep(q, (3, 4, 5), 5)
    branches = []
    # Input coins and translations are unresolved classical labels. Shift
    # and rotate the second copy of each local state with signed permutations.
    for ia, pa in enumerate((F(1, 3), F(2, 3))):
        for ib, pb in enumerate((F(2, 5), F(3, 5))):
            va = {((y + ia) % q, i ^ ia): v * ((1 - 2 * i) if ia else 1) for (y, i), v in av.items()}
            vb = {((y + 3 * ib) % q, i ^ ib): v * ((1 - 2 * i) if ib else 1) for (y, i), v in bv.items()}
            product = {(y, i, z, j): v * w for (y, i), v in va.items() for (z, j), w in vb.items()}
            branches.append((pa * pb, product))
    results = []
    for mode, grade_prior in (
        ("independent_mixed", None),
        ("locked_positive", F(1)),
        ("locked_negative", F()),
        ("precorrelated_mixture", F(3, 4)),
    ):
        sources = []
        for p, v in branches:
            if grade_prior is None:
                sources.append((p, v))
            else:
                for g, pr in ((1, grade_prior), (-1, 1 - grade_prior)):
                    if pr:
                        sources.append((p * pr, grade(v, g)))
        pg = F()
        bsin = F()
        post_sin = F()
        post_grade = F()
        for p, v in sources:
            bsin += p * overlap(v, local_sine(q))
            for g in (1, -1):
                post = grade(v, g)
                mass = p * F(norm(post), 4 * norm(v))
                if not mass:
                    continue
                if g == 1:
                    pg += mass
                else:
                    post = correct(post, q, True, True)
                post_grade += mass * overlap(post, qstep)
                post_sin += mass * overlap(post, local_sine(q))
        expected = F(1, 2) if grade_prior is None else grade_prior
        assert pg == expected and post_grade == 1 and bsin == post_sin
        results.append(
            {
                "source": mode,
                "precontact_plus_grade_probability": str(pg),
                "all_outcomes_corrected_grade_contrast": str(post_grade),
                "B_sine_before_and_after": str(bsin),
            }
        )
    return results


def causal():
    rows = []
    for distance in range(13):
        meet = distance // 2
        posA, posB = 0, distance
        steps = 0
        while (posA, posB) != (meet, meet):
            posA += int(posA < meet)
            posB -= int(posB > meet)
            steps += 1
        assert steps == (distance + 1) // 2
        rows.append(
            {
                "initial_distance": distance,
                "first_midpoint_contact": steps,
                "time_return_both_tokens": 2 * steps,
                "remote_B_waits_at_home": distance,
            }
        )
    return rows


def main():
    cases = [clock_trial(8, 8, (3, 4, 5), (3, 4, 5), r, r) for r in (0, 1, 4, 12)]
    cases += [
        clock_trial(5, 8, (5, 12, 13), (3, 4, 5), 5, 8),
        clock_trial(8, 8, (3, 4, 5), (3, -4, 5), 4, 4),
    ]
    return {
        "clock_resources": cases,
        "mixed_and_prelocked_sources": mixed_controls(),
        "logical_data": logical(),
        "causal_schedules": causal(),
        "instrument": "A fresh control H, controlled signed permutation Q=-J_A tensor J_B, and H give (I +/- Q)/2 with a single grade bit, with both planes and sheets unresolved. Repeated read of the same grade is certain. An independently prepared product of real density operators (including local spectators) has zero Q mean since each local J is skew, so each grade has probability 1/2. For entangled or prealigned references use p_grade=(1+grade*<Q>)/2. q=8 exact algebraic source limit is a sharp matched pair; all native finite rational rows include actual positive tails.",
        "correction": "On the negative grade Z_B=diag(1,-1) anticommutes with J_B, yielding the positive grade. The cyclic reflection F_B|y>=|-y> also reverses k and conjugates the held translation T_B to its inverse; Z_B F_B therefore preserves the k_B=s_B target with both labels flipped. The positive branch is unchanged. This preserves the graded-sector calibration probabilities, not arbitrary finite amplitudes or the resource's full prior purification; both flag branches are retained classically. A held oriented B stroke and an address reflection around the chosen fiducial are physical controls. For ideal independent calibrated clocks the joint cosine before contact is cos(alpha)cos(beta); after the full correction it is cos(alpha+beta) in both grades. Plane-only correction leaves cos(alpha-beta) on the negative branch and flips the local sine. For finite imperfect preparation errors in the local labels, union bounds give contrast error <=2(eta_A+eta_B) for independent product resources; finite rows verify all posterior angles directly.",
        "logical_limit": "Real product encoded v_A,v_B splits into equal positive and negative grades. Using a real-basis multiplication map on the positive space yields the usual complex tensor product; the negative branch followed by the B-plane reflection encodes v_A tensor conjugate(v_B). An ordinary Z on the real/imaginary coordinate is a physical orthogonal operation on that local real representation. Undoing arbitrary conjugation as a complex channel relative to an already fixed external complex spectator would act as a transpose on the system density and fail complete positivity. These statements concern different interfaces. Known real data, known state-specific corrections, or encoding logical data after aligning blank resource registers evade that data obstruction. Operations commuting with common J preserve the chosen space; generic physically real local operations need not preserve the code.",
        "locality": "Contact Q acts on the two transported plane coordinates. Local controlled correction on B in this implementation includes its sheet, which must travel with it or receive the classical grade at B; if reflection uses only nearest sheet hops, reflecting every coordinate around 0 can cost order q in sheet diameter. Causal rows suppose unit-speed base transport, permitted local storage, and instantaneous on-site comparison/gates. At separation D first joint light cones overlap at ceil(D/2) ticks, or D if B stays at home. Returned outputs and flags are available at both homes by 2 ceil(D/2) ticks for the midpoint schedule. Exact mandatory one-step walkers starting at odd separation have opposite parity forever at equal times unless a hold, offset launch time or adjacent-edge contact is supplied. Shared preexisting correlations can align selected records but furnish neither an instantaneous signaling operation nor a transport-free remote Q.",
        "prior_work": ["A_rational_plane_for_cyclic_phase.md", "Records_and_complex_structure.md"],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    directory = parser.parse_args().directory
    result = main()
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "phase_contact.json").write_text(
        json.dumps(result, separators=(",", ":")) + "\n", encoding="utf8", newline="\n"
    )
    print(
        len(result["clock_resources"]),
        "prepared pairs, two logical grades,",
        len(result["causal_schedules"]),
        "causal distances.",
    )
