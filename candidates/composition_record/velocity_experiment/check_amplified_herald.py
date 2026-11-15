"""Exact replay of the four-path Pell herald and its matched phase arms.

    python -I -B check_amplified_herald.py
    python -I -B check_amplified_herald.py --qiskit
    python -I -B check_amplified_herald.py --qasm amplified fresh.qasm

The direct and signed arms act on six wires. The twirled and matched-pi
exports add the same fair, unread wire. Export adds a blank pointer so that only the
coarse binary herald is measured. QASM export prepares sharp control/rail
00. The optional Qiskit test uses every input column and a coherent
superposition. No hardware data enter this replay.
"""
import argparse
from fractions import Fraction as F
from math import sqrt
from pathlib import Path
from runpy import run_path


reference = run_path(str(Path(__file__).with_name("check_heralded_gate_reference.py")))
require = reference["require"]
GOOD = tuple(i for i in range(64) if i & 0b11100 == 0)
ARMS = ("direct", "matched", "amplified", "twirled", "matched-pi")


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def isometry_numerators():
    """The four columns of V on clean inputs, in units of 1/sqrt(32)."""
    pair, capacity, _ = reference["parameters"](2)
    columns = [[0] * 64 for _ in range(4)]
    for branch, (a, b) in enumerate(pair):
        paths = reference["routed_columns"](a, b, capacity)
        for flag, rows in enumerate(paths):
            for path, matrix in enumerate(rows):
                for dst in range(4):
                    i = (branch << 5) + (flag << 4) + (path << 2) + dst
                    for src in range(4):
                        columns[src][i] = matrix[4 * dst + src]
    return columns


def reflect(columns, v):
    """I - 2 VP0 V*: the four columns have squared integer norm 32."""
    weights = [F(dot(v, c), 16) for c in columns]
    return [x - sum(w * c[i] for w, c in zip(weights, columns))
            for i, x in enumerate(v)]


def pieces(c):
    good = [v if i in GOOD else 0 for i, v in enumerate(c)]
    bad = [v - g for v, g in zip(c, good)]
    return good, bad


def captured(u, v):
    return sum(u[i] * v[i] for i in GOOD) / F(32)


def expected_columns(columns, arm):
    if arm == "direct":
        return columns
    ans = []
    for c in columns:
        good, bad = pieces(c)
        sign = -1 if arm == "amplified" else 1
        ans.append(reflect(columns, [sign * g + b for g, b in zip(good, bad)]))
    return ans


def check_exact():
    columns = isometry_numerators()
    matched = expected_columns(columns, "matched")
    amplified = expected_columns(columns, "amplified")
    for i, c in enumerate(columns):
        require(matched[i] == [-v for v in c], "phase-zero echo")
        # Every successful Kraus entry (both unresolved Pell labels) scales
        # by one constant; this proves channel equality on arbitrary spectators.
        require(all(amplified[i][j] == (-F(7, 4) if j in GOOD else F(1, 4)) * c[j]
                    for j in range(64)), "amplified clean-input isometry")
        for j, d in enumerate(columns):
            diag = int(i == j)
            require(dot(c, d) == 32 * diag and captured(c, d) == F(5, 16) * diag,
                    "full and success Gram")
            require(captured(amplified[i], amplified[j]) == F(245, 256) * diag,
                    "amplified success Gram")

    split = [tuple(reflect(columns, v) for v in pieces(c)) for c in columns]
    for i, (g, b) in enumerate(split):
        for j, (gj, bj) in enumerate(split):
            diag = int(i == j)
            require(captured(g, gj) == F(5, 16) * F(9, 64) * diag,
                    "returned success of a recorded good branch")
            require(captured(b, bj) == F(11, 16) * F(55, 64) * diag,
                    "returned success of a recorded bad branch")
            cross = captured(g, bj) + captured(b, gj)
            require(cross == -F(165, 512) * diag, "good/bad interference")
            # A source-independent physical marker couples g -> g |0>,
            # b -> b (overlap |0> + complement |1>). The components below
            # are real. For complex marker overlaps only the real part enters,
            # since the separate cross-Grams are equal and real here.
            require(captured(g, bj) == captured(b, gj), "real cross-Gram")
            for overlap, complement in ((1, 0), (-1, 0), (0, 1),
                                        (F(3, 5), F(4, 5)), (-F(3, 5), F(4, 5))):
                for sign in (1, -1):
                    first = [sign * x + overlap * y for x, y in zip(g, b)]
                    second = [sign * x + overlap * y for x, y in zip(gj, bj)]
                    actual = captured(first, second) + complement**2 * captured(b, bj)
                    require(actual == F(325 - 165 * sign * overlap, 512) * diag,
                            "explicit retained marker read")
    return columns


def binary_square(x):
    return x*x / (x*x + (1-x)**2)


def check_binary_rules():
    s, t = F(5, 16), F(11, 256)  # Success of direct arm; failure of amplified arm.
    alpha = F(55, 128)
    mix = alpha * F(1, 2) + (1 - alpha) * binary_square(s)
    require(mix == s, "rival for singly scored herald")
    require(mix / 4 == F(5, 64), "rival with two separately scored fair thinning bits")
    require(alpha * F(1, 2) + (1 - alpha) * binary_square(s/4) != s/4,
            "single coarse thinned herald detects this rival")
    require(alpha * F(1, 2) + (1 - alpha) * binary_square(t) != t,
            "coherent amplification detects this rival")
    # For the log-odds comparison in either coherent intervention, r is the
    # ratio log(odds(failure))/log(11/5); these exact checks give 1<r<4<=s/u
    # for u below. The tangent then lies strictly below the upper endpoint.
    for u in (s/4, t):
        require((1-s)/s < (1-u)/u < ((1-s)/s)**4 and 4 <= s/u,
                "power-curve tangent endpoint certificate")

    disturbed = s * F(9, 64) + (1-s) * F(55, 64)
    require(disturbed == F(325, 512), "copied first herald")
    # Extreme exponents shared between both actual binary writes. If the
    # first write selected the less likely good/bad branch (-infinity), its
    # final good probability 9/64 is again the less likely output. For
    # +infinity the originally bad branch's final good is the likelier one.
    ordinary = F(2, 17)
    negative = (1 - ordinary) * s
    positive = (1 - ordinary) * (1-s)
    require(ordinary + negative + positive == 1
            and ordinary * s + negative == s
            and ordinary * disturbed + negative + positive == 1-t,
            "shared exponents spoof the unmatched direct vs amplified comparison")
    require((1-F(32, 55))*s + F(32, 55)*(1-t) == 1-s,
            "unresolved 32-of-55 phase control produces the complementary mass")
    # Fair phase control removes the cross term before the one pooled read.
    # For real marker overlap c in [0,1] the pi-arm failure is between t and
    # this common twirled failure x. A global tangent stays below the identity
    # when 1 < log(odds(t))/log(odds(x)) < x/t, with odds(v)=(1-v)/v.
    x = 1 - disturbed
    require(x == F(187, 512) and (1-x)/x < (1-t)/t < ((1-x)/x)**6
            and 6 < x/t, "fairly twirled and amplified two-arm certificate")
    # A negative relative mark phase and a negative exponent together can
    # spoof all three matched arms. Formula order: fair, pi, zero failures.
    counts = [0, 0, 0]
    for weight, exponent_sign, overlap in ((165, -1, -1), (22, -1, 1),
                                          (187, 1, 1), (138, 1, 0)):
        masses = (x, F(187-165*overlap, 512), F(187+165*overlap, 512))
        for i, mass in enumerate(masses):
            require(2*mass != 1, "extremum tie")
            if exponent_sign * (2*mass-1) > 0:
                counts[i] += weight
    require(counts == [187, 22, 352], "signed-phase and signed-power rival")
    # Finite counterexample obtained by solving the four linear equations
    # for the three ordinary rates and normalization. Check by substitution.
    finite_modes = (
        (-5, -1, F(35381824448281, 107701044426250)),
        (-5, 1, F(49244213021335161869859, 2651349046163136613126250)),
        (5, 1, F(8544600350, 24617672561)),
        (5, 0, F(7528471861, 24617672561)),
    )
    require(sum(w for _, _, w in finite_modes) == 1, "finite mixture normalization")
    rates = [F(0)] * 3
    for q, overlap, w in finite_modes:
        require(w > 0, "positive incidence for each finite mode")
        masses = (x, F(187-165*overlap, 512), F(187+165*overlap, 512))
        for i, mass in enumerate(masses):
            rates[i] += w * mass**q / (mass**q + (1-mass)**q)
    require(rates == [F(n, 512) for n in counts], "finite signed-power rival")


def zero_mask_phase(wires):
    """Diagonal reflection negative exactly when all named wires are zero."""
    turns = [f"x q[{i}];" for i in wires]
    args = ", ".join(f"q[{i}]" for i in wires)
    return [*turns, f"ctrl({len(wires)-1}) @ z {args};", *reversed(turns)]


def qasm(arm, measure=False):
    # Every elementary instruction in the supplied V is a self-inverse
    # H, X, controlled X or controlled Z. Its reverse implements V*.
    header, body = reference["small_qasm"](False).split("qubit[6] q;\n")
    operations = body.splitlines()
    lines = [header.rstrip(), "qubit[6] q;"]
    if arm in ("twirled", "matched-pi"):
        lines += ["qubit tag;"]
    if measure:
        lines += ["qubit pointer;", "bit herald;"]
    lines.extend(operations)
    if arm != "direct":
        if arm in ("twirled", "matched-pi"):
            lines += ["h tag;"]
        if arm in ("amplified", "matched-pi"):
            lines.extend(zero_mask_phase((2, 3, 4)))
        elif arm == "twirled":
            turns = [f"x q[{i}];" for i in (2, 3, 4)]
            lines += [*turns, "ctrl(3) @ z q[2], q[3], q[4], tag;",
                      *reversed(turns)]
        lines.extend(reversed(operations))
        lines.extend(zero_mask_phase((2, 3, 4, 5)))
        lines.extend(operations)
    if measure:
        # Retain the other six wires, and do not measure their path codes.
        turns = [f"x q[{i}];" for i in (2, 3, 4)]
        lines += [*turns, "ctrl(3) @ x q[2], q[3], q[4], pointer;",
                  *reversed(turns), "herald = measure pointer;"]
    return "\n".join(lines) + "\n"


def check_qiskit(columns):
    from qiskit import qasm3
    from qiskit.quantum_info import Statevector

    for arm in ARMS:
        if arm in ("twirled", "matched-pi"):
            first = expected_columns(columns, "matched" if arm == "twirled" else "amplified")
            phase_pi = expected_columns(columns, "amplified")
            targets = [[v/sqrt(2) for v in left + right]
                       for left, right in zip(first, phase_pi)]
        else:
            targets = expected_columns(columns, arm)
        size = len(targets[0])
        unitary = qasm3.loads(qasm(arm))
        probe = qasm3.loads(qasm(arm, measure=True))
        require(probe.count_ops().get("measure") == 1
                and probe.find_bit(probe.data[-1].qubits[0]).index == size.bit_length()-1,
                "only the isolated herald wire is measured")
        pointer = probe.remove_final_measurements(inplace=False)
        inputs = [[int(i == j) for i in range(4)] for j in range(4)]
        inputs.append([1/sqrt(2), 0, 0, 1j/sqrt(2)])
        for src in inputs:
            expected = [sum(src[i] * targets[i][j] for i in range(4)) / sqrt(32)
                        for j in range(size)]
            bare = Statevector(src + [0]*(size-4)).evolve(unitary).data
            require(max(abs(a-b) for a, b in zip(bare, expected)) < 2e-10,
                    "coherent QASM columns")
            marked = Statevector(src + [0]*(2*size-4)).evolve(pointer).data
            for j, amplitude in enumerate(expected):
                yes, no = j+size, j
                occupied, empty = (yes, no) if (j % 64) in GOOD else (no, yes)
                require(abs(marked[occupied] - amplitude) < 2e-10
                        and abs(marked[empty]) < 2e-10, "pointer basis and erasure")
    print("Qiskit checked all five exports, including identical wire layouts for twirled and matched-pi.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--qiskit", action="store_true", help="check the exported circuits with Qiskit")
    parser.add_argument("--qasm", nargs=2, metavar=("ARM", "NEW_FILE"),
                        help="export " + ", ".join(ARMS) + " with a single herald read")
    args = parser.parse_args()
    columns = check_exact()
    check_binary_rules()
    print("Direct and phase-zero echo: 5/16. Phase-pi echo: 245/256. Same successful channel.")
    print("Copied flag: good -> 9/64, bad -> 55/64. Either echo -> 325/512.")
    print("Marker overlap c: phase-zero/pi success = (325 -/+ 165 Re(c))/512.")
    print("Fair unresolved phase: failure 187/512 at every overlap; ideal amplified failure 11/256.")
    print("Separate thinning rival, unmatched signed-power rival and tangent certificates verified.")
    if args.qiskit:
        check_qiskit(columns)
    if args.qasm:
        arm, name = args.qasm
        if arm not in ARMS:
            parser.error("ARM must be one of " + ", ".join(ARMS))
        with Path(name).open("x", encoding="ascii", newline="\n") as stream:
            stream.write(qasm(arm, measure=True))


if __name__ == "__main__":
    main()
