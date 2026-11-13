"""Open brickwork walk on binary occupations. Exact Gaussian integer ports.

Run python -B check_occupation_contact.py OUTPUT_DIRECTORY.
"""

import argparse
import cmath
import json
from fractions import Fraction as F
from itertools import combinations, permutations
from math import acos, cos, exp, pi, sin, sqrt
from pathlib import Path

ZERO = (0, 0)
ONE = (1, 0)
TILTS = ((3, -4), (4, 3))


def add(u, v):
    return u[0] + v[0], u[1] + v[1]


def scale(n, u):
    return n * u[0], n * u[1]


def times_i(n, u):
    return -n * u[1], n * u[0]


def multiply(u, v):
    return u[0] * v[0] - u[1] * v[1], u[0] * v[1] + u[1] * v[0]


def magnitude(v):
    return v[0] ** 2 + v[1] ** 2


def sites(mask, N):
    return [i for i in range(N) if mask >> i & 1]


def masks(N, p):
    return [sum(1 << i for i in occ) for occ in combinations(range(N), p)]


def gate(raw, bond, tilt, contact):
    """The integer numerator includes x5 on empty as well as blocked bonds."""
    diag, imag = tilt
    out = {}

    def deposit(m, v):
        out[m] = add(out.get(m, ZERO), v)

    for bits, v in raw.items():
        local = (bits >> bond) & 3
        if local in (0, 3):
            deposit(bits, scale(5 * (contact if local == 3 else 1), v))
        else:
            deposit(bits, scale(diag, v))
            deposit(bits ^ (3 << bond), times_i(imag, v))
    return {m: v for m, v in out.items() if v != ZERO}


def slots(N, layer):
    return range(layer % 2, N - 1, 2)


def evolve(raw, N, layer, contact, *, adjoint=False):
    diag, imag = TILTS[layer % 2]
    bonds = slots(N, layer)
    for bond in reversed(bonds) if adjoint else bonds:
        raw = gate(raw, bond, (diag, -imag if adjoint else imag), contact)
    return raw


def single_layer(matrix, layer):
    """Independently construct the one-body layer with denominator 5 per layer."""
    N = len(matrix)
    diag, imag = TILTS[layer % 2]
    out = [[scale(5, v) for v in row] for row in matrix]
    for i in slots(N, layer):
        for col in range(N):
            x, y = matrix[i][col], matrix[i + 1][col]
            out[i][col] = add(scale(diag, x), times_i(imag, y))
            out[i + 1][col] = add(times_i(imag, x), scale(diag, y))
    return out


def minor(matrix, I, J):
    total = ZERO
    for perm in permutations(range(len(J))):
        inversions = sum(perm[i] > perm[j] for i, j in combinations(range(len(J)), 2))
        value = ((-1) ** inversions, 0)
        for row, col in zip(I, perm):
            value = multiply(value, matrix[row][J[col]])
        total = add(total, value)
    return total


def first_diff(a, b, alphabet):
    return next((m for m in alphabet if magnitude(a.get(m, ZERO)) != magnitude(b.get(m, ZERO))), None)


def census(N, p, depth, coherent):
    modes = masks(N, p)
    initials = combinations(modes, 2) if coherent else [(m,) for m in modes]
    earliest = None
    counts = [0] * (depth + 1)
    checked = 0
    for indices in initials:
        for phase in (ONE, (-1, 0), (0, 1)) if coherent else (ONE,):
            a = {indices[0]: ONE}
            if coherent:
                a[indices[1]] = phase
            b = a.copy()
            checked += 1
            for t in range(depth + 1):
                w = first_diff(a, b, modes)
                if w is not None:
                    counts[t] += 1
                    earliest = min(earliest, t) if earliest is not None else t
                a = evolve(a, N, t, 1)
                b = evolve(b, N, t, -1)
    assert not counts[0] and not counts[1] and (coherent or not counts[2])
    if p in (1, N) or N == 2:
        assert earliest is None
    return {
        "N": N,
        "particles": p,
        "source": "two_coordinate_superposition" if coherent else "localized",
        "input_count": checked,
        "relative_phases": [[1, 0], [-1, 0], [0, 1]] if coherent else None,
        "number_of_inputs_with_a_coordinate_difference_by_time": counts,
        "first_time_with_positive_coordinate_difference": earliest,
    }


def record_run(N, p, start, depth):
    modes = masks(N, p)
    initial_norm = sum(map(magnitude, start.values()))
    identity = [[ONE if i == j else ZERO for j in range(N)] for i in range(N)]
    one = identity
    a = start.copy()
    b = start.copy()
    conjugate = {j: (v[0], -v[1]) for j, v in start.items()}
    alt_conjugate = conjugate.copy()
    den = 1
    rows = []
    for t in range(depth + 1):
        output = []
        for m in modes:
            occ = sites(m, N)
            det = ZERO
            for n, w in start.items():
                cols = sites(n, N)
                coeff = minor(one, occ, cols)
                if p >= 2:
                    assert minor(one, occ, [cols[1], cols[0], *cols[2:]]) == scale(-1, coeff)
                    assert minor(one, occ, [cols[0], cols[0], *cols[2:]]) == ZERO
                det = add(det, multiply(w, coeff))
            va, vb = a.get(m, ZERO), b.get(m, ZERO)
            assert scale(5 ** (t * p), va) == scale(den, det)
            assert conjugate.get(m, ZERO) == (va[0], -va[1]) and alt_conjugate.get(m, ZERO) == (
                vb[0],
                -vb[1],
            )
            output.append(
                [
                    occ,
                    va,
                    vb,
                    str(F(magnitude(va), initial_norm * den * den)),
                    str(F(magnitude(vb), initial_norm * den * den)),
                ]
            )
        assert (
            sum(map(magnitude, a.values()))
            == sum(map(magnitude, b.values()))
            == initial_norm * den * den
        )
        for sign, data in ((1, a), (-1, b)):
            reverse = data
            for k in reversed(range(t)):
                reverse = evolve(reverse, N, k, sign, adjoint=True)
            assert reverse == {m: scale(den**2, v) for m, v in start.items()}
        rows.append(
            {"layers": t, "all_port_numerator_denominator_before_initial_norm": den, "ports": output}
        )
        one = single_layer(one, t)
        a = evolve(a, N, t, 1)
        b = evolve(b, N, t, -1)
        # Within a layer reversal of bond order has no effect (disjoint gates);
        # applying the adjoint in chronological layer order conjugates coefficients.
        conjugate = evolve(conjugate, N, t, 1, adjoint=True)
        alt_conjugate = evolve(alt_conjugate, N, t, -1, adjoint=True)
        den *= 5 ** len(slots(N, t))
    return {
        "N": N,
        "particles": p,
        "input_sites_coefficients": [[sites(m, N), v] for m, v in start.items()],
        "input_squared_norm": initial_norm,
        "history": rows,
    }


def which_record():
    src = {5: ONE}
    rows = []
    for sign in (1, -1):
        v = evolve(evolve(src, 3, 0, sign), 3, 1, sign)
        paths = []
        total = ZERO
        incoherent = 0
        for m in masks(3, 2):
            w = evolve({m: v.get(m, ZERO)}, 3, 2, sign).get(5, ZERO)
            paths.append([sites(m, 3), w])
            total = add(total, w)
            incoherent += magnitude(w)
        assert total == ((-44 if sign == 1 else 116), 0) and incoherent == 7696
        rows.append(
            {
                "contact_sign": sign,
                "middle_occupations_and_return_numerators": paths,
                "coherent": str(F(magnitude(total), 15625)),
                "middle_occupation_read_unresolved": str(F(incoherent, 15625)),
            }
        )
    return rows


def plucker():
    rows = []
    for sign in (1, -1):
        state = evolve(evolve({5: ONE}, 4, 0, sign), 4, 1, sign)

        def v(i, j, amplitudes=state):
            return amplitudes.get((1 << i) | (1 << j), ZERO)

        poly = add(
            add(multiply(v(0, 1), v(2, 3)), scale(-1, multiply(v(0, 2), v(1, 3)))),
            multiply(v(0, 3), v(1, 2)),
        )
        assert (poly == ZERO) == (sign == 1)
        rows.append(
            {
                "contact_sign": sign,
                "w01w23_minus_w02w13_plus_w03w12": poly,
                "polynomial_denominator": 5**6,
            }
        )
    return rows


def gauged(raw, N):
    """D dagger: one factor of -i per odd occupied site."""
    phases = (ONE, (0, -1), (-1, 0), (0, 1))
    return {
        m: multiply(phases[sum(i % 2 for i in sites(m, N)) % 4], v) for m, v in raw.items() if v != ZERO
    }


def real_layer(raw, N, t, sign):
    """Real orientation on a bond ordered by its left then right site."""
    d, s = (3, 4) if t % 2 == 0 else (4, 3)
    for j in slots(N, t):
        out = {}
        for mask, v in raw.items():
            local = (mask >> j) & 3
            val = 5 * (-1 if local == 3 and sign == -1 else 1) if local in (0, 3) else d
            out[mask] = add(out.get(mask, ZERO), scale(val, v))
            if local in (1, 2):
                dest = mask ^ (3 << j)
                out[dest] = add(out.get(dest, ZERO), scale(s if local == 2 else -s, v))
        raw = {m: w for m, w in out.items() if w != ZERO}
    return raw


def norm2(raw):
    return sum(magnitude(v) for v in raw.values())


def real_controls():
    records = []
    cases = (
        (3, {5: ONE}),
        (3, {3: ONE, 6: ONE}),
        (3, {3: ONE, 5: (0, 1)}),
        (4, {3: ONE, 5: ONE, 10: (2, -1)}),
        (5, {21: ONE, 14: (-1, 2)}),
    )
    for N, orig in cases:
        for sign in (1, -1):
            v = orig.copy()
            w = gauged(v, N)
            wrong = v.copy()
            mismatch = []
            den = 1
            for t in range(5):
                assert w == gauged(v, N)
                keys = v.keys() | wrong.keys()
                tv = sum(abs(magnitude(v.get(m, ZERO)) - magnitude(wrong.get(m, ZERO))) for m in keys)
                mismatch.append(str(F(tv, 2 * den * den * norm2(orig))))
                v = evolve(v, N, t, sign)
                w = real_layer(w, N, t, sign)
                wrong = real_layer(wrong, N, t, sign)
                den *= 5 ** len(slots(N, t))
            records.append(
                {
                    "N": N,
                    "sign": sign,
                    "complex_source": [[sites(m, N), v] for m, v in orig.items()],
                    "correct_real_chart_source": [[sites(m, N), v] for m, v in gauged(orig, N).items()],
                    "TV_if_source_not_transformed_0_to_4": mismatch,
                }
            )
    assert any(any(F(t) > 0 for t in r["TV_if_source_not_transformed_0_to_4"]) for r in records)
    assert all(
        F(t) == 0
        for r in records
        if len(r["complex_source"]) == 1
        for t in r["TV_if_source_not_transformed_0_to_4"]
    )
    N = 4
    orig = {3: ONE, 5: ONE, 10: (2, -1), 12: (-3, 2)}
    w = gauged(orig, N)
    real = {m: (v[0], 0) for m, v in w.items()}
    imag = {m: (v[1], 0) for m, v in w.items()}
    frontier = {"": (orig, real, imag, 1)}
    for t in range(4):
        children = {}
        for hist, (src, rx, iy, den) in frontier.items():
            sign = -1 if hist.endswith("1") else 1
            src = evolve(src, N, t, sign)
            rx = real_layer(rx, N, t, sign)
            iy = real_layer(iy, N, t, sign)
            for bit in (0, 1):

                def selected(d, b=bit, site=t):
                    return {m: v for m, v in d.items() if (m >> site) & 1 == b}

                children[hist + str(bit)] = (
                    selected(src),
                    selected(rx),
                    selected(iy),
                    den * 5 ** len(slots(N, t)),
                )
        frontier = children
    den0 = norm2(orig)
    transcripts = []
    for hist, (src, rx, iy, den) in frontier.items():
        px, py, p = (F(norm2(s), den0 * den**2) for s in (rx, iy, src))
        assert px + py == p
        transcripts.append([hist, str(px), str(py), str(p)])
    assert sum(F(t[-1]) for t in transcripts) == 1
    return {
        "all_input_gauge_checks": records,
        "two_real_sources_prior": list(map(str, (F(norm2(real), den0), F(norm2(imag), den0)))),
        "adaptive_site_reads_all_transcripts_real_imaginary_joint_and_total": transcripts,
    }


def stripe_step(v):
    """Periodic real-gauge unitary for the single-particle Bloch check."""
    N = len(v)
    result = list(v)
    for t, (d, s) in enumerate(((3 / 5, 4 / 5), (4 / 5, 3 / 5))):
        for j in range(t, N, 2):
            k = (j + 1) % N
            x, y = result[j], result[k]
            result[j], result[k] = d * x + s * y, -s * x + d * y
    return result


def positive_spinor(k):
    z = cmath.exp(-1j * k)
    v = (3 / 5, -4 / 5)  # the first intracell real rotation acting on |0>
    uv = (4 / 5 * v[0] - 3 / 5 * z * v[1], 3 / 5 * z.conjugate() * v[0] + 4 / 5 * v[1])
    omega = acos(12 / 25 * (1 + cos(k)))
    denom = 2j * sin(omega)
    raw = ((cmath.exp(1j * omega) - uv[0]) / denom, -uv[1] / denom)
    E = sqrt(sum(abs(t) ** 2 for t in raw))
    return [t / E for t in raw], omega


def band_pairs():
    cells = 96
    N = 2 * cells
    snapshot = []
    for centre in (11, -15):
        modes = range(centre - 7, centre + 8)
        coeff = {m: exp(-(((m - centre) / 3.5) ** 2)) for m in modes}
        normalization = sqrt(cells * sum(w * w for w in coeff.values()))

        def packet(n, weights=coeff, normalizer=normalization):
            v = [0j] * N
            for m, w in weights.items():
                k = 2 * pi * m / cells
                spin, omega = positive_spinor(k)
                for x in range(cells):
                    phase = cmath.exp(1j * (k * x - n * omega)) * w / normalizer
                    v[2 * x] += phase * spin[0]
                    v[2 * x + 1] += phase * spin[1]
            return v

        target = packet(0)
        real = [t.real * sqrt(2) for t in target]
        imag = [t.imag * sqrt(2) for t in target]
        assert (
            max(
                abs(sum(t * t for t in target)),
                abs(sum(x * x for x in real) - 1),
                abs(sum(x * x for x in imag) - 1),
                abs(sum(x * y for x, y in zip(real, imag))),
            )
            < 1e-12
        )
        k = 2 * pi * centre / cells
        omega = positive_spinor(k)[1]
        velocity = 12 / 25 * sin(k) / sin(omega)
        conjugate_velocity = -12 / 25 * sin(-k) / sin(positive_spinor(-k)[1])
        assert velocity == conjugate_velocity
        for n in range(7):
            theory = packet(n)
            residual = max(abs(x - y) for x, y in zip(theory, target))
            assert residual < 1e-12
            mixture = [(x * x + y * y) / 2 for x, y in zip(real, imag)]
            delta = [abs(x) ** 2 for x in target]
            assert max(abs(x - y) for x, y in zip(mixture, delta)) < 1e-12
            assert all(max(x * x, y * y) <= 2 * p + 1e-12 for x, y, p in zip(real, imag, delta))
            snapshot.append(
                {
                    "center_mode": centre,
                    "cycles": n,
                    "complex_positive_band_velocity_cells_per_cycle": velocity,
                    "opposite_band_negative_momentum_velocity": conjugate_velocity,
                    "real_component_TV_from_full_orbital": sum(
                        abs(x * x - p) for x, p in zip(real, delta)
                    )
                    / 2,
                    "imag_component_TV_from_full_orbital": sum(
                        abs(x * x - p) for x, p in zip(imag, delta)
                    )
                    / 2,
                    "two_real_mixture_max_probability_residual": max(
                        abs(x - y) for x, y in zip(mixture, delta)
                    ),
                    "spectral_vs_literal_amplitude_sup_residual": residual,
                }
            )
            target, real, imag = map(stripe_step, (target, real, imag))
    return snapshot


def main():
    census_rows = [
        census(N, p, 4, coherent)
        for N in range(2, 7)
        for p in sorted({1, 2, min(3, N), N})
        for coherent in (False, True)
    ]
    examples = [
        record_run(3, 2, {5: ONE}, 5),
        record_run(3, 2, {3: ONE, 6: ONE}, 5),
        record_run(3, 2, {3: ONE, 5: (0, 1)}, 4),
        record_run(4, 2, {5: ONE}, 5),
        record_run(5, 3, {21: ONE}, 5),
        record_run(6, 3, {21: ONE, 42: (0, -1)}, 5),
    ]
    assert examples[0]["history"][3]["ports"][1][-2:] == ["1936/15625", "13456/15625"]
    assert examples[1]["history"][2]["ports"][0][-2:] == ["512/625", "32/625"]
    return {
        "date_free_rerun": "python -B check_occupation_contact.py OUTPUT_DIRECTORY",
        "real_gauge_and_record_controls": real_controls(),
        "finite_periodic_one_body_paired_band_packets": band_pairs(),
        "real_source_scope": "On a chain let D multiply a configuration by i^(number on odd sites). In D-dagger coordinates both alternating nearest bond matrices in left-to-right basis are [[c,s],[-s,c]] (s=4/5 or 3/5). Vacuum, local double occupation and all real diagonal readouts retain their rules. A sharply occupied launch changes only by a global phase. If psi in this chart is x+i y, every native terminal or adaptive occupation-read history has real Kraus matrix K and probability ||Kx||^2+||Ky||^2. Preparing x or y normalized with probabilities ||x||^2 and ||y||^2 for a normalized psi reproduces all those records. This is a classical mixture of real coherent states, not an assertion of efficient preparation or of agreement on arbitrary independently held phase-sensitive analyzers. A component could be zero for general psi; remove it from the mixture.",
        "real_ray_scope": "For a scalar positive-band state in a gapped symmetric chart, complex conjugation in the real coordinate gauge changes k to -k and e^(-i omega(k)) to e^(+i omega(-k)). The conjugate sector is orthogonal and both components of the complex orbital have equal norm 1/sqrt(2), including a many-body state in the exterior product of that band. Eigenphase odd-sign reversal and k reversal give identical group velocity. Each normalized real component puts at most twice the full positive-band probability outside any event, so either inherits weak concentration of the ordered rays. The mixture retains all occupation probabilities even for non-concentrated quantum states; a single real component can have different finite interference fringes. A generally fully localized site cannot be assumed to have prepared a narrow one-band packet. The illustrative periodic single-particle mode packets test real recurrent propagation, not convergence rates or the preparation of an arbitrary orbital from a single launch.",
        "basis": "Increasing mode labels on an open chain 0..N-1. A binary occupation has no repeated site. Even bonds (0,1),(2,3),... precede odd bonds (1,2),(3,4),...; uncovered end modes are untouched. Pairs (u,v) in the integer data mean u+iv. Divide each amplitude by the stated history denominator times sqrt(initial squared norm).",
        "law": "Each two-mode gate has vacuum numerator 5, one-occupant block 3I-4iX or 4I+3iX, and doubly-occupied numerator 5*contact_sign, all over 5. One-body blocks have determinant +1. For contact_sign=+1 the full evolution is the exterior power, independently checked from determinants of chronological one-body products. For sign=-1 each active bond contributes a controlled occupation phase on |11>; disjoint bonds commute and one-body behavior is identical. Both laws preserve exclusion and norm. Overall conjugation of all gates AND launch data preserves every coordinate probability; reverse time uses the conjugate-transpose gates in inverse layer order.",
        "minimality": "Within each layer the two laws differ by a diagonal product of signs on the doubly occupied disjoint bonds. This phase commutes with that layer. It leaves its own coordinate measurement unchanged for every coherent input. On a localized input the initial layer's sign is also global. Thus no one-layer terminal coordinate distinguishes arbitrary inputs, or two-layer terminal coordinate distinguishes localized inputs for any chain length. In the two-mode two-particle space the dimension is one. Three open modes attain both bounds; one-body sectors never distinguish. Terminal coordinate records made after intermediate full occupation reads must sum incoherently across the recorded histories.",
        "evidence_scope": "Four-mode Pluecker control detects genuine departure from the manifold of single two-fermion Slater states. It is stronger than a port difference on three modes, where any pure two-fermion vector is decomposable. Both finite laws are local occupation rules; these examples alone imply neither a unique exchange principle nor a continuum interaction, scattering strength, or statistics of other particles.",
        "port_columns": [
            "occupied_sites",
            "determinant_lift_numerator",
            "minus_contact_numerator",
            "determinant_probability",
            "minus_contact_probability",
        ],
        "census": census_rows,
        "full_output_examples": examples,
        "middle_record_control": which_record(),
        "four_mode_single_Slater_control": plucker(),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    directory = parser.parse_args().directory
    data = main()
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "occupation_contact.json").write_bytes(
        (json.dumps(data, separators=(",", ":")) + "\n").encode()
    )
    print(len(data["census"]), "censuses and", len(data["full_output_examples"]), "complete runs.")
