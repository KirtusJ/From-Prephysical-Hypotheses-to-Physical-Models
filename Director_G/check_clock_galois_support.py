"""Exact conditional Fourier support, finite norm bounds and a coherent bypass.

Run python -B check_clock_galois_support.py OUTPUT_DIRECTORY.
"""

import argparse
import cmath
import json
from fractions import Fraction
from functools import cache
from math import gcd, isqrt, prod, tau
from pathlib import Path


def trim(p):
    p = list(p)
    while p and not p[-1]:
        p.pop()
    return p


def divide(p, q):
    """Integer division by a monic polynomial in ascending coefficient order."""
    assert q[-1] == 1
    p = trim(p)
    quot = [0] * max(0, len(p) - len(q) + 1)
    while len(p) >= len(q):
        n = len(p) - len(q)
        v = p[-1]
        quot[n] = v
        for j, c in enumerate(q):
            p[n + j] -= v * c
        p = trim(p)
    return trim(quot), p


@cache
def phi(q):
    value = [-1] + [0] * (q - 1) + [1]
    for d in range(1, q):
        if q % d == 0:
            value, rem = divide(value, phi(d))
            assert not rem
    return tuple(value)


def determinant(rows):
    A = [r.copy() for r in rows]
    previous = 1
    sign = 1
    for j in range(len(A) - 1):
        pivot = next((i for i in range(j, len(A)) if A[i][j]), None)
        if pivot is None:
            return 0
        if pivot != j:
            A[pivot], A[j] = A[j], A[pivot]
            sign = -sign
        for i in range(j + 1, len(A)):
            for k in range(j + 1, len(A)):
                x = A[j][j] * A[i][k] - A[i][j] * A[j][k]
                assert x % previous == 0
                A[i][k] = x // previous
        previous = A[j][j]
    return sign * A[-1][-1]


def norm_real(b, q):
    """Full-field multiplication determinant is the square of the real norm."""
    f = phi(q)
    dim = len(f) - 1
    cols = []
    for k in range(dim):
        _, v = divide([0] * k + b, f)
        cols.append(v + [0] * (dim - len(v)))
    full = determinant(cols)  # determinant invariant under transpose
    assert full >= 0 and isqrt(full) ** 2 == full
    return isqrt(full)


def value(p, z):
    s = 0j
    for v in reversed(p):
        s = s * z + v
    return s


def row(name, polys, q, k, depth=None, initial_energy=None):
    m = len(polys[0])
    assert all(len(p) == m for p in polys) and q > 2 and m % q == 0 and gcd(k, q) == 1
    e = sum(v * v for p in polys for v in p)
    assert e > 0
    # Physical Laurent autocorrelation; residue mod q gives an integer
    # representative for B = sum |P(primitive qth root)|².
    autocorr = [0] * q
    for p in polys:
        for j, v in enumerate(p):
            for l, w in enumerate(p):
                autocorr[(j - l) % q] += v * w
    norm = norm_real(autocorr, q)
    reps = [j for j in range(1, (q + 1) // 2) if gcd(j, q) == 1]
    s = len(reps)
    exact = []
    numerical = []
    for j in reps:
        polynomials = []
        for p in polys:
            shifted = [0] * q
            for i, v in enumerate(p):
                shifted[i * j % q] += v
            polynomials.append(divide(shifted, phi(q))[1])
        exact.append(any(polynomials))
        z = cmath.exp(1j * tau * j / q)
        numerical.append(sum(abs(value(p, z)) ** 2 for p in polys))
    assert exact == [norm > 0] * s
    assert abs(prod(numerical) - norm) < 1e-7 * max(1, norm)
    u = Fraction(m * e, 2)
    idx = reps.index(min(k % q, -k % q))
    target = numerical[idx] / float(u)
    result = {
        "case": name,
        "M": m,
        "order": q,
        "target_representative": k,
        "depth": depth,
        "integer_rows": polys,
        "energy": e,
        "support_by_folded_primitive": dict(zip(reps, exact)),
        "primitive_B_by_representative": numerical,
        "positive_real_norm": norm,
        "U": str(u),
        "target_weight": target,
    }
    if depth is not None:
        assert e <= 2**depth * initial_energy
        result["initial_integer_energy"] = initial_energy
        result["joint_record_probability"] = str(Fraction(e, 2**depth * initial_energy))
    if s > 1 and norm:
        eta = 1 - target
        normalized_rhs = Fraction(norm * (s - 1) ** (s - 1), 1) / u**s
        assert (1 - eta) * eta ** (s - 1) + 1e-13 >= float(normalized_rhs)
        result["lower_bound_on_(1-e)*e^(s-1)"] = str(normalized_rhs)
        if depth is not None:
            result["bound_from_depth_alone"] = str(
                Fraction((s - 1) ** (s - 1), 1) / Fraction(m * 2**depth * initial_energy, 2) ** s
            )
        occupied = [i for i, v in enumerate(polys[0]) if v]
        if len(polys) == 1:
            degree = occupied[-1] - occupied[0]
            H = max(map(abs, polys[0]))
            result["degree_after_origin_shift"] = degree
            result["height"] = H
            result["wrong_pair_weight_lower_from_degree_height"] = str(
                Fraction(2, m * (degree + 1) * H**2 * ((degree + 1) * H) ** (2 * (s - 1)))
            )
            lower = Fraction(result["wrong_pair_weight_lower_from_degree_height"])
            assert all(v / float(u) + 1e-14 >= float(lower) for i, v in enumerate(numerical) if i != idx)
    return result


def signed_permuted_branch(m):
    p = [[int(y == 0) for y in range(m)], [0] * m]
    energies = []
    for t in range(1, 6):
        rotated = [[0] * m for _ in p]
        for y in range(m):
            for c, sgn in ((0, 1), (1, -1)):
                v = p[0][y] + sgn * p[1][y]
                dest = (y + c + t) % m
                if (dest + t) % 5 == 0:
                    v = -v
                if t == 3 and (dest + c) % 4 == 2:
                    v = 0
                rotated[c][dest] = v
        p = rotated
        energies.append(sum(v * v for r in p for v in r))
    return p, energies


def bypass_read(placed, hsign, stride):
    """Use the actual sign on both H blocks and the same positive scalar denominator."""
    m = len(placed)
    # Denominator 4 after first H; 4 sqrt(2) after the terminal H.
    split = [(hsign * a, hsign * b) for a, b in placed]
    shifted = [split[(y - stride) % m] for y in range(m)]
    probs = []
    port_bins = []
    for s in (1, -1):
        amps = [(hsign * (a + s * c), hsign * (b + s * d)) for (a, b), (c, d) in zip(split, shifted)]
        bins = [(Fraction(a * a + 2 * b * b, 32), Fraction(2 * a * b, 32)) for a, b in amps]
        prob = tuple(sum(r[i] for r in bins) for i in (0, 1))
        probs.append(prob)
        port_bins.append([list(map(str, r)) for r in bins])
    overlap = tuple(
        Fraction(
            sum(
                (a * c + 2 * b * d, a * d + b * c)[i]
                for (a, b), (c, d) in zip(placed, placed[-stride:] + placed[:-stride])
            ),
            8,
        )
        for i in (0, 1)
    )
    assert tuple(x - y for x, y in zip(*probs)) == overlap
    assert tuple(x + y for x, y in zip(*probs)) == (1, 0)
    sign = hsign * (1 if stride == 1 else -1)
    assert probs == [(Fraction(1, 2), Fraction(sign, 4)), (Fraction(1, 2), Fraction(-sign, 4))]
    return {
        "source_and_both_read_H_sign": hsign,
        "controlled_physical_stride": stride,
        "source_numerator": placed,
        "ports_plus_minus_in_a_plus_b_sqrt2": [list(map(str, r)) for r in probs],
        "signed_overlap_coefficients": list(map(str, overlap)),
        "complete_port_and_sheet_weights": port_bins,
    }


def bypass(n, hsign=1):
    """A global coin layer splits each listed pair; unlisted modes coherently idle.

    Coordinates carry exact (a,b) for (a+b sqrt(2))/sqrt(2)^clock.
    """
    state = [(int(i == 0), 0) for i in range(n)]
    words = []
    for pairs in ([(0, 4)], [(0, 2), (4, 6)], [(2, 1), (6, 5)]):
        nxt = [(2 * b, a) for a, b in state]
        for i, j in pairs:
            a, b = state[i]
            c, d = state[j]
            nxt[i], nxt[j] = (hsign * (a + c), hsign * (b + d)), (hsign * (a - c), hsign * (b - d))
        state = nxt
        words.append(state)
    # At depth two keep one leaf of the second splitter and one other.
    # Place the two untouched amplitudes on antipodes, distribute the four
    # deeper leaves on odd sites, and set the real cosine's signs.
    placed = [(0, 0)] * 8
    for src, dst, sgn in ((0, 0, 1), (4, 4, -1), (2, 1, 1), (1, 3, -1), (6, 5, -1), (5, 7, 1)):
        a, b = state[src]
        placed[dst] = (sgn * a, sgn * b)
    assert placed == [(0, 1), (hsign, 0), (0, 0), (-hsign, 0), (0, -1), (-hsign, 0), (0, 0), (hsign, 0)]
    assert sum(a * a + 2 * b * b for a, b in placed) == 8 and sum(a * b for a, b in placed) == 0
    supports = []
    for k in range(8):
        # Embed sqrt(2)=zeta_8+zeta_8^(-1) in the ordinary physical field.
        poly = [0] * 8
        for y, (a, b) in enumerate(placed):
            poly[k * y % 8] += a
            poly[(k * y + 1) % 8] += b
            poly[(k * y - 1) % 8] += b
        supports.append(bool(divide(poly, phi(8))[1]))
    active = {1, 7} if hsign == 1 else {3, 5}
    assert supports == [k in active for k in range(8)]
    return {
        "numerator_per_layer": words,
        "placed_A_plus_B_sqrt2": placed,
        "denominator": "sqrt(2)^3",
        "exact_support": supports,
        "readouts": [bypass_read(placed, hsign, d) for d in (1, 3)],
        "embedding_fixing_sqrt2": "At order 8 only k=1,7 are in the faithful orbit of 1 under the subgroup fixing sqrt(2). Twisting both final coefficients and Fourier labels also preserves zeros.",
    }


def seeded_control(m):
    # H with fresh sample rail, cyclic shift on L, H and select +/-.
    state = [int(y == 0) for y in range(m)]
    out = []
    for t, shift in enumerate([m // 2, 1, 1, 1, 1, 1, 1], 1):
        s = -1 if t == 1 else 1
        state = [v + s * state[(y - shift) % m] for y, v in enumerate(state)]
        out.append(row("dipole_then_unit_plus", [state], m, 1, 2 * t, 1))
    return out


def degree_controls():
    rows = []
    for q in (3, 4, 5, 6, 8, 9, 12, 16, 32, 64):
        f = phi(q)
        assert not divide(f, f)[1] and divide(f[:-1], f)[1]
        coeff = [0] * q
        coeff[1] = coeff[-1] = 1
        # Projector off-diagonal entry is (z+z^-1)/q. Its numerator
        # is rational iff its degree-<phi(q) representation is constant.
        rep = divide(coeff, f)[1]
        rational = len(rep) <= 1
        assert rational == (q in (3, 4, 6))
        rows.append(
            {
                "order": q,
                "first_degree_permitting_zero": len(f) - 1,
                "sharp_zero_polynomial": f,
                "truncated_polynomial_survives": True,
                "scaled_adjacent_pair_projector_entry_remainder": rep,
                "pair_projector_rational": rational,
            }
        )
    return rows


def main():
    cases = []
    for m in (3, 4, 5, 6, 8, 9, 10, 12, 15, 16, 20, 24, 32):
        p, energies = signed_permuted_branch(m)
        for q in range(3, m + 1):
            if m % q == 0:
                cases.append(row("addressed_signed_H_branch", p, q, 1, 5, 1))
        cases[-1]["branch_energy_after_layers"] = energies
        dip = [int(y == 0) + int(y == m // 2) for y in range(m)]
        if m % 2 == 0:
            cases.append(row("half_turn_even_control", [dip], m, 1, 2, 1))
    for m in (8, 16, 32):
        cases += seeded_control(m)
    # Monomial, primitive-zero, and s=1 corrections remain visible above.
    sharp = row("five_sheet_norm_sharp", [[0, 1, 0, 0, -1]], 5, 1)
    assert sharp["positive_real_norm"] == 5
    cases.append(sharp)
    return {
        "cases": cases,
        "degree_and_projector_controls": degree_controls(),
        "coherent_bypass_M8": bypass(8),
        "negative_sqrt2_bypass_and_read_M8": bypass(8, -1),
        "embedding_read_scope": "Readouts include the source, controlled translated arm and both fully synchronous readout H blocks. H changes to -H on acted blocks in the negative embedding; I stays I on coherent bypass wires. Reversing the sign on BOTH readout H blocks cancels, but the input source preserves a relative sign. The held physical T gives distinct plus-port laws in Q(sqrt(2)); replacing T by T^3 in the negative case restores the ordinary law. This is a finite model discriminator for different fixed relative acted/idle phases with held generator and readout. A global simultaneous relabeling is a different comparison. No observed physical event, absolute phase measurement or extension to other field elements is inferred.",
        "scope": "Each accepted coordinate transcript has integer coordinate numerator up to one common scalar. Uniform signed H layers, signed permutations (also addressed), coordinate projectors and rational matrices preserve the rational ray; common path-depth parity suffices after clearing dyadic denominators. Distinct classical branches with differing depths are summed in positive mass; postselection and almost-sure finite stopping cannot yield exact zero leakage from positive target weight. Unmeasured interfering bypass depths of different parity may leave the rational-ray class. Integer initial numerator is assumed for depth estimates; in a general rational circuit height after clearing denominators is a separate resource.",
        "bound": "Let q>2 be the order of a target on a sheet of size M, s=phi(q)/2, E=sum_{a,y} v_ay^2 and U=M E/2. For integer P_a, the totally nonnegative real algebraic integer B=sum P_a(zeta_q)P_a(zeta_q^-1) has s nonnegative conjugates b_i, all positive if any is. Their product N is a positive integer. Pair mass = b_i/U. For unwanted fraction e outside the target pair, sum_{j!=i} b_j<=U e, hence (1-e)e^(s-1)>=N(s-1)^(s-1)/U^s for s>1 by AM-GM. Actual depth t bounds E<=2^t E0 with normalized complete signed-H layers, signed permutations and contracting coordinate masks. A positive unit-norm source with t finite cannot approach exact purity without increasing resources. For one polynomial of degree D after shifting its origin and coefficient height H, b_j<=((D+1)H)^2 and E<=(D+1)H². Each other primitive pair has mass >=2/[M(D+1)H² ((D+1)H)^(2(s-1))]. Degree <phi(q) alone precludes primitive zeros for a nonzero polynomial. Rescaling an integer numerator by a common factor weakens height-only bounds; the norm-sensitive ratio is invariant.",
        "exceptions": "s=1 (q=3,4,6) has one primitive pair and no obstruction to purity within that block; e=1 is possible when the entire order is killed. A rational projector onto the whole primitive subspace is possible even if the individual pair projector is irrational. For M=2^ell>=8 the pair-projector entry 2cos(2pi/M)/M is irrational: 2cos is a real algebraic integer strictly between 1 and 2. A byte of measurement data or a bit permuting the target convention does not itself supply a tagged primitive pair.",
        "precedence": "Native_preparations_and_probability_embeddings.md already proves the full order-support obstruction, positive mixture corollary and sharp five-sheet inequality. Preparing_a_phase_clock.md already gives the M=8 instance and finite-stopping caveat. This checker adds an all-order multi-component norm/height/depth inequality and explicit bypass control. The obstruction concerns exact purity, not high-accuracy positive-yield preparation or evidence for an absolute embedding.",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    directory = parser.parse_args().directory
    result = main()
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "clock_galois_support.json").write_text(
        json.dumps(result, separators=(",", ":")) + "\n", encoding="utf8"
    )
    print(len(result["cases"]), "order/record checks and one exact M=8 bypass.")
