"""Exact replay of private feedback between two native herald writes.

    python -I -B check_private_herald_feedback.py
    python -I -B check_private_herald_feedback.py --qiskit

Eleven fair bits choose a private response type M and target T before the
science input. Only the second label Z and the six gate outputs are passed
on. The optional gate replay keeps an orthogonal first-label pointer X,
checks every Kraus entry and combines two target circuits with the actual
eleven-fair-bit weights. The flat and square rates concern this one input
herald mass. No hardware data enter either calculation.
"""
import argparse
from fractions import Fraction as F
from itertools import product
from math import sqrt
from pathlib import Path
from runpy import run_path

old = run_path(str(Path(__file__).with_name("check_amplified_herald.py")))
require = old["require"]
GOOD = F(5, 16)
LABEL = {True: GOOD, False: 1-GOOD}


def sector(v, good):
    g, b = old["pieces"](v)
    return g if good else b


def branch_columns():
    """Unnormalized maps for fixed (first label, reflection yes/no, final label)."""
    cols = old["isometry_numerators"]()
    branches = {}
    for x, feedback, z in product((False, True), repeat=3):
        actual = []
        # V* P_x V = s_x I on the prepared input. Acting with the
        # reflection on P_x V therefore subtracts 2 s_x V.
        gain = int(x == z) - (2*LABEL[x] if feedback else 0)
        for col in cols:
            written = sector(col, x)
            evolved = old["reflect"](cols, written) if feedback else written
            output = sector(evolved, z)
            require(output == [gain*y for y in sector(col, z)], "full private Kraus column")
            actual.append(output)
        for i in range(4):
            for j in range(4):
                require(old["dot"](actual[i], actual[j])/F(32) == gain**2*LABEL[z]*(i == j),
                        "input-independent fine record, including dark branches")
        branches[x, feedback, z] = actual, gain
    return branches


def controller(word):
    """Disjoint consecutive ranges of the uniform unsigned eleven-bit word."""
    if not 0 <= word < 2048:
        raise ValueError("controller requires an eleven-bit word")
    if word < 467:
        return "flat", True
    if word < 880:
        return "flat", False
    if word < 1053:
        return "square", True
    return "square", False


def rates_for_pairs(distribution, good_rates):
    """Both launches use independent X and fresh work given the shared state."""
    def rate(state, label):
        p = good_rates[state]
        return p if label else 1-p
    return {(a,b): sum(p*rate(state,a)*rate(state,b) for state,p in distribution.items())
            for a,b in product((False,True), repeat=2)}


def full_table(branches):
    """Every (eleven-bit word, authentic X, published Z), including dark outputs."""
    mass = {}
    cell_counts = {}
    public = {}
    for word in range(2048):
        m, target = controller(word)
        cell = (m, target)
        cell_counts[cell] = cell_counts.get(cell, 0) + 1
        for x, z in product((False, True), repeat=2):
            _, gain = branches[x, x != target, z]
            mass[word, x, z] = gain**2 * LABEL[z] / 2048
            key = (m, target, z)
            public[key] = public.get(key, 0) + mass[word,x,z]

    weights = {("flat",True):467, ("flat",False):413, ("square",True):173, ("square",False):995}
    require(cell_counts == weights, "controller thresholds and all multiplicities")
    require(sum(mass.values()) == 1 and sum(v==0 for v in mass.values()) == 2048,
            "complete 8192-outcome probability table")
    private_mass = {"flat": F(55,128), "square": F(73,128)}
    c_type = {"flat":F(1,2), "square":F(25,146)}
    c_target = {True:F(925,1024), False:F(45,1024)}
    require(c_type["square"] == GOOD**2/(GOOD**2+(1-GOOD)**2), "binary square response")
    for (m,target), count in weights.items():
        for z in (False,True):
            expected = c_target[target] if z else 1-c_target[target]
            require(public[m,target,z] == F(count,2048)*expected, "target-conditioned instrument")
    for z in (False,True):
        total = 0
        for m in private_mass:
            both_targets = sum(public[m,t,z] for t in (False,True))
            expected = c_type[m] if z else 1-c_type[m]
            require(both_targets == private_mass[m]*expected, "private response at this mass")
            total += both_targets
        # The full-column calculation established the same output isometry per
        # label for every hidden path. Only this scalar remains to be checked.
        require(total/LABEL[z] == 1, "public instrument equals original branch")

    fresh_target = rates_for_pairs(private_mass, c_type)
    same_target = rates_for_pairs(LABEL, c_target)
    # Fresh conditional T can be sampled by rejecting independent eleven-bit
    # words until their M matches the held M. Each accepted attempt starts
    # before its science input arrives; this controller has unbounded runtime.
    for (m,t), count in weights.items():
        require(F(count,2048)/private_mass[m] == F(count,880 if m=="flat" else 1168),
                "fresh T conditional on M")
    for a,b in product((False,True), repeat=2):
        iid = LABEL[a]*LABEL[b]
        sign = 1 if a==b else -1
        require(fresh_target[a,b]-iid == sign*F(495,18688), "hold M only")
        require(same_target[a,b]-iid == sign*F(166375,1048576), "hold both M and T")
    return mass


def gate_qasm(target):
    """Fixed private settings. The saved first-label pointer is never erased."""
    header, body = old["reference"]["small_qasm"](False).split("qubit[6] q;\n")
    gates = body.splitlines()
    turns = [f"x q[{i}];" for i in (2, 3, 4)]

    def write(name):
        return [*turns, f"ctrl(3) @ x q[2], q[3], q[4], {name};", *reversed(turns)]

    ops = [header.rstrip(), "qubit[6] q;", "qubit first;", "qubit second;",
           *gates, *write("first")]
    # V* and V cancel on the branch whose saved X already matches T.
    # The middle sign is applied only for clean work ancillas and X != T.
    clean = ["x q[2];", "x q[3];", "x q[4];", "x q[5];"]
    if target:
        clean.append("x first;")
    ops += [*reversed(gates), *clean, "ctrl(4) @ z q[2], q[3], q[4], q[5], first;",
            *reversed(clean), *gates]
    return "\n".join([*ops, *write("second")])+"\n"


def qiskit_check(branches, table):
    from qiskit import QuantumCircuit, qasm3
    from qiskit.quantum_info import Statevector

    fair = QuantumCircuit(11)
    fair.h(range(11))
    pattern = Statevector.from_instruction(fair).probabilities()
    require(max(abs(v-1/2048) for v in pattern) < 1e-12, "eleven independent fair pattern bits")
    raw = {}
    for target in (False,True):
        program = qasm3.loads(gate_qasm(target))
        for i in range(4):
            wave = Statevector.from_int(i, 256).evolve(program).data
            for x, z in product((False,True), repeat=2):
                # register order (from high bit): second, first, q[5:0].
                start = 128*int(z) + 64*int(x)
                out = wave[start:start+64]
                cols, _ = branches[x, x != target, z]
                require(max(abs(v-w/sqrt(32)) for v,w in zip(out,cols[i])) < 2e-10,
                        "all recorded-pointer QASM amplitudes")
                if i == 0:
                    raw[target, x, z] = sum(abs(v)**2 for v in out)
    for (word, x, z), p in table.items():
        _, target = controller(word)
        value = pattern[word]*raw[target, x, z]
        require(abs(value-float(p)) < 2e-11, "Qiskit complete private-record table")
    print("Qiskit: 2,048 output amplitudes and all 8,192 fair-pattern/X/Z probabilities verified.")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--qiskit", action="store_true", help="also propagate the eight-wire recorded circuit")
    args = ap.parse_args()
    branches = branch_columns()
    table = full_table(branches)
    print("Eleven-bit pattern/X/Z: 6,144 bright and 2,048 dark. Public good rate = 5/16.")
    print("Good given flat: 1/2. Good given square: 25/146. Branch isometries agree in both.")
    print("GG excess: shared M with fresh conditional T = 495/18688; shared M and T = 166375/1048576.")
    if args.qiskit:
        qiskit_check(branches, table)


if __name__ == "__main__":
    main()
