"""Finite integer-path checks for a coherently retained direction qubit.

Run python -B check_coin_qubit.py results. Gate words below are in temporal order.
"""

import argparse
import json
from itertools import product
from math import pi, sqrt
from pathlib import Path

import numpy as np


I = np.eye(2)
X = np.array([[0, 1], [1, 0]])
Y = np.array([[0, -1j], [1j, 0]])
Z = np.diag([1, -1])
H = np.array([[1, 1], [1, -1]])/sqrt(2)
PAULI = (X, Y, Z)


def serial(z):
    return np.stack((np.asarray(z).real, np.asarray(z).imag), axis=-1).tolist()


def matrix_error(a, b):
    return float(np.linalg.norm(a-b))


def advance_raw(state, order, g_sign):
    """Integer Hadamard numerators on literal (position, direction, cyclic sheet)."""
    result = {}
    for (site, old, sheet), count in state.items():
        for direction in (1, -1):
            key = (site+direction, direction, (sheet+g_sign*site) % order)
            signed = -count if old == direction == -1 else count
            result[key] = result.get(key, 0) + signed
    return result


def path_counts(order, k, gain=1):
    sheet_matrices = np.zeros((order, 2, 2), dtype=int)
    for column, initial in enumerate((1, -1)):
        state = {(0, initial, 0): 1}
        for t in range(1, 2*k+1):
            state = advance_raw(state, order, gain)
            distance = t if t <= k else 2*k-t
            direction = 1 if t <= k else -1
            allowed = {(distance, direction), (-distance, -direction)}
            state = {v: c for v, c in state.items() if v[:2] in allowed}
        for (_, direction, sheet), count in state.items():
            sheet_matrices[sheet, int(direction == -1), column] = count
    expected = np.zeros_like(sheet_matrices)
    sign = (-1)**(k-1)
    expected[gain*k*k % order, 1, :] = sign
    expected[-gain*k*k % order, 0, :] = (sign, -sign)
    return sheet_matrices, bool(np.array_equal(sheet_matrices, expected))


def gate(order, k, winding=1, gain=1):
    counts, structural = path_counts(order, k, gain)
    angle = 2*pi*winding/order
    rotations = np.exp(-1j*angle*np.arange(order))
    raw = np.einsum("y,yoc->oc", rotations, counts)/2**k
    attenuation = 2**(0.5-k)
    scalar_phase = (-1)**(k-1)
    unitary = scalar_phase*X @ np.diag(np.exp(-1j*angle*gain*k*k*np.array([1, -1]))) @ H
    return raw, unitary, dict(k=k, integer_paths_match=structural, sheet_numerators=counts.tolist(),
                              raw_matrix=serial(raw), predicted_unfitted_error=matrix_error(raw, attenuation*unitary),
                              success=attenuation**2,
                              state_independence_error=matrix_error(raw.conj().T@raw, attenuation**2*I))


def word_matrix(order, word, winding=1, gain=1):
    result = I
    for k in word:
        result = gate(order, k, winding, gain)[0] @ result
    return result


def probe(order, words, winding=1, gain=1):
    """Pauli expectation axes and unconditioned success on individual probes."""
    probes = []
    matrices = []
    for word in words:
        raw = word_matrix(order, word, winding, gain)
        success = np.trace(raw.conj().T@raw).real/2
        observable = raw.conj().T@Z@raw/success
        axis = np.array([np.trace(p@observable).real/2 for p in PAULI])
        matrices.append(axis)
        probes.append(dict(word=list(word), success=float(success), axis=axis.tolist()))
    return np.array(matrices), probes


def bloch(rho):
    return np.array([np.trace(rho@p).real for p in PAULI])


def dephased_return(rho, order, winding=1):
    raw = word_matrix(order, (1,), winding)
    # Keeping and subsequently discarding the arm label removes interference
    # between terminal directions. Preserve the herald probability, then normalize.
    coherent = raw@rho@raw.conj().T
    return np.diag(np.diag(coherent))/np.trace(coherent)


def read_word_on_lift(order, seed, preparation, analyzer, winding, label_arms=False):
    """Propagate every two-arm amplitude on actual cyclic sheets before reading either port."""
    paths = [(0, seed, 0, (), 1/sqrt(order))]
    paths = [(x, c, y, record, q*np.exp(2j*pi*winding*y/order))
             for x, c, _, record, q in paths for y in range(order)]
    for j, k in enumerate(preparation+analyzer):
        for t in range(1, 2*k+1):
            distance = t if t <= k else 2*k-t
            out_direction = 1 if t <= k else -1
            allowed = {(distance, out_direction), (-distance, -out_direction)}
            next_paths = []
            for x, c, sheet, record, amplitude in paths:
                for d in (1, -1):
                    if (x+d, d) in allowed:
                        tag = (d,) if label_arms and j >= len(preparation) and t == 1 else ()
                        sign = -1 if d == c == -1 else 1
                        next_paths.append((x+d, d, (sheet+x) % order, record+tag, amplitude*sign/sqrt(2)))
            paths = next_paths
    amplitudes = {}
    for _, c, sheet, record, q in paths:
        key = (c, sheet, record)
        amplitudes[key] = amplitudes.get(key, 0)+q
    return np.array([sum(abs(q)**2 for (c, _, _), q in amplitudes.items() if c == d) for d in (1, -1)])


def tomography(order, winding=1, gain=1):
    words = [(), (1,), (1, 1)]
    axes, probes = probe(order, words, winding, gain)
    sources = []
    density_matrices = []
    for seed, word in ((0, ()), (1, ()), (0, (1,)), (0, (1, 1))):
        v = word_matrix(order, word, winding, gain)[:, seed]
        weight = float(np.vdot(v, v).real)
        rho = np.outer(v, v.conj())/weight
        density_matrices.append(rho)
        readouts = []
        for analyzer in words:
            operation = word_matrix(order, analyzer, winding, gain)
            branch = operation@rho@operation.conj().T
            ports = np.diag(branch).real
            expectation = float((ports[0]-ports[1])/sum(ports))
            evidence = dict(raw_port_probabilities=ports.tolist(), expectation=expectation)
            if gain == 1:
                lifted = read_word_on_lift(order, 1-2*seed, word, analyzer, winding)/weight
                tagged = read_word_on_lift(order, 1-2*seed, word, analyzer, winding, label_arms=True)/weight
                evidence.update(literal_lift_port_error=float(np.max(abs(ports-lifted))),
                                arm_tagged_ports=tagged.tolist(),
                                arm_tagged_expectation=float((tagged[0]-tagged[1])/sum(tagged)))
            readouts.append(evidence)
        rhs = [r["expectation"] for r in readouts]
        reconstructed = np.linalg.lstsq(axes, rhs, rcond=1e-12)[0]
        sources.append(dict(seed="RL"[seed], word=list(word), preparation_yield=weight,
                            bloch=bloch(rho).tolist(), port_readouts=readouts,
                            reconstruction_error=float(np.linalg.norm(reconstructed-bloch(rho)))))
    gram = np.array([[np.trace(a@b).real for a in density_matrices] for b in density_matrices])
    plus_y = (I+Y)/2
    minus_y = (I-Y)/2
    dephased_pairs = []
    for rho in (plus_y, minus_y):
        current = rho
        expectations = []
        for _ in range(3):
            expectations.append(float(np.trace(Z@current).real))
            current = dephased_return(current, order, winding)
        dephased_pairs.append(expectations)
    return dict(M=order, winding=winding, gain=gain, probes=probes, preparations=sources,
                analyzer_rank=int(np.linalg.matrix_rank(axes, tol=1e-10)),
                analyzer_determinant=float(np.linalg.det(axes)),
                source_gram=gram.tolist(), source_gram_determinant=float(np.linalg.det(gram)),
                dephased_Y_witness_expectations=dephased_pairs)


def contact_source(order, winding, contact):
    # Start both qubits at 0 in R. Contact gain acts on the second departure only.
    state = {(0, 0, 1, 1, 0): 1}
    for tick in (1, 2):
        after = {}
        for (a, b, old1, old2, sheet), count in state.items():
            gain = a+b+(contact if tick == 2 and a == b else 0)
            for d1, d2 in product((1, -1), repeat=2):
                if tick == 2 and (a+d1 != 0 or b+d2 != 0):
                    continue
                sign = (-1)**(int(old1 == d1 == -1)+int(old2 == d2 == -1))
                key = (a+d1, b+d2, d1, d2, (sheet+gain) % order)
                after[key] = after.get(key, 0)+sign*count
        state = after
    coeff = np.zeros((2, 2), complex)
    h = 2*pi*winding/order
    for (_, _, d1, d2, sheet), count in state.items():
        coeff[int(d1 == -1), int(d2 == -1)] += count*np.exp(-1j*h*sheet)/4
    local = word_matrix(order, (1,), winding)[:, 0]
    analytic = np.outer(local, local)*np.exp(-1j*h*contact*I)
    return coeff, matrix_error(coeff, analytic)


def bell(order, winding=1, contact=1):
    # Each party uses a six-tick local program, including any outcome sign relabeling.
    # These words were chosen in an exploratory search with the source at h=+2*pi/M.
    settings = ([((1, 1, 1), 1), ((3,), 1), ((1, 1, 1), 1), ((1, 2), -1)]
                if order == 3 else [((2, 1), 1), ((3,), 1), ((2, 1), -1), ((3,), -1)])
    coeff, contact_error = contact_source(order, winding, contact)
    source_success = float(np.vdot(coeff, coeff).real)
    psi = coeff.flatten()/sqrt(source_success)
    analyzers = []
    for word, port_sign in settings:
        k = word_matrix(order, word, winding)
        success = np.trace(k.conj().T@k).real/2
        output = port_sign*k.conj().T@Z@k/success
        analyzers.append((k, float(success), output, port_sign))
    data = []
    for a, b in product(range(2), repeat=2):
        ka, pa, oa, sa = analyzers[a]
        kb, pb, ob, sb = analyzers[2+b]
        ports = (abs(np.kron(ka, kb)@coeff.flatten())**2).reshape(2, 2)
        signed = sa*sb*(ports[0, 0]+ports[1, 1]-ports[0, 1]-ports[1, 0])
        accepted = float(signed/ports.sum())
        # On each side output +1 if its local mask fails; source herald predates choices.
        full = float(np.vdot(psi, np.kron(pa*oa+(1-pa)*I, pb*ob+(1-pb)*I)@psi).real)
        data.append(dict(settings=[a, b], local_success=[pa, pb], total_accept=float(ports.sum()),
                         unconditioned_port_table=ports.tolist(), on_both_pass=accepted, local_failure_plus_one=full))
    chsh = lambda key: float(sum(mult*r[key] for mult, r in zip((1, 1, 1, -1), data)))
    return dict(M=order, winding=winding, contact_gain=contact, raw_source=serial(coeff),
                source_success=source_success, source_formula_error=contact_error,
                local_settings=[dict(word=list(w), output_sign=s, ticks=2*sum(w)) for w, s in settings],
                trials=data, CHSH_both_local_gates_pass=chsh("on_both_pass"),
                CHSH_all_local_trials_after_source_herald=chsh("local_failure_plus_one"))


def main(output):
    output.mkdir(parents=True, exist_ok=True)
    gates, comparisons = [], []
    for order in (3, 5):
        for winding in (1, -1):
            matrices = {}
            for k in range(1, 9):
                raw, expected, row = gate(order, k, winding)
                matrices[k] = raw/2**(0.5-k)
                gates.append(dict(M=order, winding=winding, **row))
            for j, k in ((1, 2), (1, 3), (2, 5), (3, 8)):
                ratio = matrices[k]@matrices[j].conj().T
                angle = 2*pi*winding*(k*k-j*j)/order
                exact = (-1)**(k-j)*np.diag(np.exp(1j*angle*np.array([1, -1])))
                comparisons.append(dict(M=order, winding=winding, k=k, j=j,
                                        ratio_Uk_Uj_adjoint=serial(ratio), unfitted_error=matrix_error(ratio, exact)))
    tomos = [tomography(m, sign) for m, sign in product((3, 5), (1, -1))]
    zero = tomography(3, 1, 0)
    bells = [bell(m, s, g) for m, s, g in product((3, 5), (1, -1), (0, 1))]
    checks = dict(
        integer_paths=all(r["integer_paths_match"] for r in gates),
        unfitted_complex_matrices=all(r["predicted_unfitted_error"] < 1e-13 for r in gates),
        input_independent_success=all(r["state_independence_error"] < 1e-13 for r in gates),
        matrix_ratios=all(r["unfitted_error"] < 1e-13 for r in comparisons),
        three_analyzers=all(r["analyzer_rank"] == 3 for r in tomos),
        zero_gain_loses_quadrature=zero["analyzer_rank"] == 2,
        four_preparation_gram_M3=all(abs(r["source_gram_determinant"]-3/16) < 1e-12
                                     for r in tomos if r["M"] == 3),
        preparation_readbacks=all(p["reconstruction_error"] < 1e-12 for t in tomos
                                  for p in t["preparations"]),
        full_lift_readbacks=all(e["literal_lift_port_error"] < 1e-12 for t in tomos for p in t["preparations"]
                                for e in p["port_readouts"]),
        arm_tag_changes_coherent_read=all(abs(t["preparations"][2]["port_readouts"][2]["expectation"]-
                                              t["preparations"][2]["port_readouts"][2]["arm_tagged_expectation"])
                                          > 0.05 for t in tomos),
        dephased_quadratures_indistinguishable=all(np.max(abs(np.diff(r["dephased_Y_witness_expectations"],
                                                                     axis=0))) < 1e-13 for r in tomos),
        contact_source_formula=all(r["source_formula_error"] < 1e-13 for r in bells),
        postselected_CHSH=all((r["CHSH_both_local_gates_pass"] > 2+1e-9) == bool(r["contact_gain"]) for r in bells),
        all_local_trials_CHSH=all(abs(r["CHSH_all_local_trials_after_source_herald"]) < 2+1e-12 for r in bells),
    )
    report = dict(checks=checks, gates=gates, ratios=comparisons, tomography=tomos,
                  zero_gain_control=zero, contact_tests=bells,
                  scope="Exact integer path aggregation with numerical character evaluation. Heralded qubit tomography "
                        "uses deterministic expectations, without finite-shot sampling. Bell settings were chosen "
                        "using the logical source; setting-dependent local filters condition the reported witness.")
    (output/"coin_qubit.json").write_text(json.dumps(report, indent=2, allow_nan=False)+"\n", encoding="utf8")
    print(checks)
    if not all(checks.values()):
        raise SystemExit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    main(parser.parse_args().output)
