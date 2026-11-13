"""Synchronized rational reflections, oblivious retry, and a held bypass port.

Run python -B check_rational_bypass.py OUTPUT_DIRECTORY. A Walsh packet uses
k globally matched H layers; omitted denominators are restored in every record.
"""

import argparse
import json
from fractions import Fraction as F
from math import gcd, sqrt
from pathlib import Path


def triples(size):
    u, v = 1, 1
    for _ in range(size):
        m, n = u + v, v
        a, b, c = m * m - n * n, 2 * m * n, m * m + n * n
        assert a * a + b * b == c * c and abs(a - b) == gcd(a, b) == 1
        yield a, b, c
        u, v = u + 2 * v, u + v


def capacity(a, b):
    return 1 << (a + b - 1).bit_length()


def walsh(state, k):
    # Layout [junk flag][logical coordinate][index]. Every mode sees the same H layer.
    width = 1
    while width < k:
        for start in range(0, len(state), 2 * width):
            for i in range(start, start + width):
                j = i + width
                state[i], state[j] = state[i] + state[j], state[i] - state[j]
        width *= 2


def transform(state, a, b, c, k):
    data = state.copy()
    walsh(data, k)
    perm = [0] * len(data)
    for idx, value in enumerate(data):
        block, l = divmod(idx, k)
        junk, x = divmod(block, 4)
        if x < 2:
            if l < a:
                value *= 1 - 2 * x
            elif l < a + b:
                x ^= 1
            else:
                junk ^= 1
        elif l >= c:
            junk ^= 1
        perm[(4 * junk + x) * k + l] = value
    walsh(perm, k)
    return perm


def projected(state, k, passed):
    return [v if (i in (0, k, 2 * k, 3 * k)) == passed else 0 for i, v in enumerate(state)]


def project4(state, k):
    return [state[i * k] for i in range(4)]


def norm(state):
    return sum(v * v for v in state)


def applied(raw, a, b, c):
    x, y, z, w = raw
    return [a * x + b * y, b * x - a * y, c * z, c * w]


def aligned(got, want):
    j = next(i for i, x in enumerate(want) if x)
    return got[j] != 0 and all(v * want[j] == t * got[j] for v, t in zip(got, want))


def literal(a, b, c, raw, pairs):
    k = capacity(a, b)
    start = [0] * (8 * k)
    for i, v in enumerate(raw):
        start[i * k] = v
    E = norm(start)
    desired = applied(raw, a, b, c)
    p = F(c * c, k * k)
    scale = k * k
    after = transform(start, a, b, c, k)
    assert transform(after, a, b, c, k) == [k * k * v for v in start]
    assert project4(after, k) == desired and norm(after) == E * scale
    remaining = {"0": projected(after, k, False)}
    attempts = [{"output_tick": 1, "success_histories": {"1": str(p)}, "survivor_mass": str(1 - p)}]
    for round_id in range(1, pairs + 1):
        again = {}
        success = {}
        scale *= k**4
        for hist, failed in remaining.items():
            back = transform(failed, a, b, c, k)  # W*=W; action is still positive time.
            for y in (True, False):
                middle = projected(back, k, y)
                if y:
                    assert aligned(project4(middle, k), raw)
                arrived = transform(middle, a, b, c, k)
                got = project4(arrived, k)
                assert aligned(got, desired)
                word = hist + str(int(y))
                success[word + "1"] = F(norm(got), E * scale)
                again[word + "0"] = projected(arrived, k, False)
        remaining = again
        total = sum(F(norm(v), E * scale) for v in again.values())
        assert total == (1 - p) * (1 - 2 * p * (1 - p)) ** round_id
        assert total + sum(success.values()) == (1 - p) * (1 - 2 * p * (1 - p)) ** (round_id - 1)
        attempts.append(
            {
                "output_tick": 2 * round_id + 1,
                "success_histories": {s: str(v) for s, v in success.items()},
                "survivor_mass": str(total),
            }
        )
    counts = [
        sum(after[(4 * flag + x) * k + l] ** 2 for x in range(4)) for flag in range(2) for l in range(k)
    ]
    return attempts, [F(v, E * k * k) for v in counts]


def physical(a, b, c):
    runs = []
    examples = ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1), (2, -3, 4, -1))
    for raw in examples:
        logs, coords = literal(a, b, c, raw, 2)
        runs.append((logs, coords))
        assert logs == runs[0][0]
    tv = sum(abs(x - y) for x, y in zip(runs[0][1], runs[2][1])) / 2
    assert tv > 0
    return {
        "triple": [a, b, c],
        "tested_inputs": examples,
        "coarse_record_histories_identical_for_all_inputs": runs[0][0],
        "first_detailed_flag_probabilities_acted_and_idle": list(
            zip(map(str, runs[0][1]), map(str, runs[2][1]))
        ),
        "detailed_first_read_TV_acted_vs_idle": str(tv),
    }


def clock_port(a, b, c, sign):
    state = [1] + [0] * 7
    for pairs in (((0, 4),), ((0, 2), (4, 6)), ((2, 1), (6, 5))):
        new = [c * v for v in state]
        for x, y in pairs:
            new[x] = sign * (a * state[x] + b * state[y])
            new[y] = sign * (b * state[x] - a * state[y])
        state = new
    placed = [0] * 8
    for i, j, s in ((0, 0, 1), (4, 4, -1), (2, 1, 1), (1, 3, -1), (6, 5, -1), (5, 7, 1)):
        placed[j] = s * state[i]
    E = norm(placed)
    assert E == c**6
    rows = []
    for stride in (0, 1, 3):
        output = [
            [F((x + s * placed[(j - stride) % 8]) ** 2, 4 * E) for j, x in enumerate(placed)]
            for s in (1, -1)
        ]
        assert sum(sum(port) for port in output) == 1
        rows.append({"held_stride": stride, "plus": str(sum(output[0])), "minus": str(sum(output[1]))})
    return rows


def selector(a, b, c, sa, second):
    """First control H, branch reference and candidate, final H. Input data |0>."""
    x, y = sa * a, sa * b
    aa, bb, cc, sb = second
    positive = [
        F((cc * x + sb * c * aa) ** 2, 4 * c * c * cc * cc),
        F((cc * y + sb * c * bb) ** 2, 4 * c * c * cc * cc),
    ]
    negative = [
        F((cc * x - sb * c * aa) ** 2, 4 * c * c * cc * cc),
        F((cc * y - sb * c * bb) ** 2, 4 * c * c * cc * cc),
    ]
    contrast = sum(positive) - sum(negative)
    assert contrast == F(sa * sb * (a * aa + b * bb), c * cc) and sum(positive + negative) == 1
    return str(contrast)


def main():
    collection = list(triples(15))
    record = []
    last_error = 1.0
    for j, (a, b, c) in enumerate(collection):
        k = capacity(a, b)
        p = F(c * c, k * k)
        gap = 1 / (c * sqrt(1 + sqrt(1 - 1 / (2 * c * c))))
        assert F(1, 8) < p <= F(25, 49) and 0 < gap < last_error
        last_error = gap
        plus, minus = clock_port(a, b, c, 1), clock_port(a, b, c, -1)
        assert F(plus[1]["plus"]) + F(minus[1]["plus"]) == 1
        smooth = (a + b) / (sqrt(2) * c)
        assert abs(gap**2 - 2 * (1 - smooth)) < 1e-15
        controls = [selector(a, b, c, 1, (*collection[max(0, j - 1)], s)) for s in (1, -1)]
        target = (2 + sqrt(2)) / 4
        assert abs(float(F(plus[1]["plus"])) - target) <= 3 * gap + 1e-14
        record.append(
            {
                "triple": [a, b, c],
                "K": k,
                "index_H_layers_per_W": 2 * (k.bit_length() - 1),
                "single_pass_success": str(p),
                "retry_pair_success_after_failure": str(2 * p * (1 - p)),
                "expected_W_or_adjoint_calls": str(1 + 1 / p),
                "operator_norm_gap_to_specified_positive_H_block": gap,
                "positive_program_full_clock": plus,
                "negative_program_full_clock": minus,
                "rational_reference_contrasts_to_previous_positive_and_negative": controls,
                "candidate_fixed_positive_or_negative_H_contrast": [smooth, -smooth],
            }
        )
    return {
        "programs": record,
        "related_primary_methods": {
            "linear combinations of unitaries": "https://arxiv.org/abs/1202.5822",
            "alternating verifier and inverse measurements": "https://cs.uwaterloo.ca/~watrous/Papers/QuantumArthurMerlinGames.pdf",
            "prior repeat-until-success synthesis in a different library": "https://arxiv.org/abs/1311.1074",
        },
        "literal_retry_checks": [physical(*t) for t in collection[:3]],
        "construction": "Uniform K=2^k mode index, one blank validity bit, signed permutation SELECT, then inverse Walsh. Every coordinate sees k H before and k H after. On the acted block use a labels for Z and b labels for X; on the idle block c labels for I. All other labels act by a reversible flip of the validity bit. Measure only the common projector onto the index-zero AND flag-zero subspace vs its complete complement; never reveal selector or data. Kraus K_pass=((aZ+bX) direct sum cI)/K has K_pass* K_pass=(c/K)^2 I for all inputs and spectators. A signed permutation using predicates l<a,l<a+b,l<c is a supplied coherent control; at the abstract bit level comparisons have O(log K) bit complexity given reversible work, without requiring K independently supplied real analog rotations. The literal check uses 8K total coordinates.",
        "rate": "With u+v sqrt(2)=(1+sqrt(2))^t, t>=1, m=u+v, n=v, (a,b,c)=(m²-n²,2mn,m²+n²). The legs differ by one and c grows asymptotically by 3+2sqrt(2) per step. Rational normalized matrix U=(aZ+bX)/c is orthogonal; scalar cI makes its direct sum coherent. Since X,Z anticommute, ||U-H||²=2-sqrt(2)(a+b)/c=1/[c²(1+sqrt(1-1/(2c²)))]. Therefore k=O(log(1/error)), K=O(1/error), and 1/8<p<=25/49 independent of precision. Location/connectivity and implementation clock cost of the predicate, Walsh matchings and coarse records are extra assumptions.",
        "recovery": "For every unit input |v> put G=|0>U|v>, B=(I-P)W|0,v>/sqrt(1-p). Because projected W has constant singular value sqrt(p), W and W* act between two state-independent pairs of subspaces as the same 2x2 orthogonal rotation, tensored with the preserved logical v. From a coarse failure apply W* and test the initial ancilla; if its outcome is zero it returns |v> and the next W succeeds with p. If it is nonzero the next W succeeds with 1-p. In either case a subsequent failure returns B up to a scalar. Each recovery pair succeeds with 2p(1-p). After 1+2l uses the failure probability is (1-p)(1-2p(1-p))^l, with mean 1+1/p uses; indefinite iteration halts almost surely, with no fixed deterministic deadline. Reading all failure labels can reveal logical-sector information, invalidating this correction. Recovery requires a coherent yes/no projector onto the whole failed space, including the initially unknown input's spectator. These are normalized squared law statements.",
        "identification": "Every finite complete physical port of a rational program is rational, invariant under both embeddings; conditioning and recovery preserve that invariance. Both the choice of positive rational triples and deliberately negating the acted matrix are operationally distinguishable settings. In the ordinary real operational metric their read probabilities converge to (2 +/- sqrt(2))/4, under either embedding on any finite transcript. Given a fixed physical selector phase and a separate device claimed to implement H direct sum I, an equal-path comparison with the accepted rational reference has contrast +/- (a+b)/(sqrt(2)c) on acted input, or a common idle branch gives the usual held-T clock test. Assuming an actual target is the operational limit of the positive sequence singles out its ordinary representation by continuity on this completion. Signed finite records alone neither require an external device to have this relative phase nor equate its formal algebraic name with that limit.",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    out = parser.parse_args().directory
    result = main()
    out.mkdir(parents=True, exist_ok=True)
    (out / "rational_bypass.json").write_text(
        json.dumps(result, separators=(",", ":")) + "\n", encoding="utf8"
    )
    print(
        len(result["programs"]),
        "rational programs,",
        len(result["literal_retry_checks"]),
        "literal coherent retry blocks.",
    )
