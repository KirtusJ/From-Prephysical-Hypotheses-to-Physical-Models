"""Exact finite all-output CHSH score on a three-sheet, twelve-site radial walk.

Run python -B check_radial_bell.py results. All probabilities and the certified
correlations are rational; complex matrices independently check the implementation.
"""

import argparse
import json
from collections import defaultdict
from fractions import Fraction as F
from itertools import product
from math import pi, sqrt
from pathlib import Path

import numpy as np

from check_radial_records import X, Y, Z, matrix_for_run


RADIUS = 6
CAP = 24
COS = (F(1), F(-1, 2), F(-1, 2))
SIN_BY_ROOT3 = (F(0), F(-1, 2), F(1, 2))  # sin(4*pi*q/3)/sqrt(3)
PAULI = (X, Y, Z)

# Elements a+b*i*sqrt(3) represent all source and Pauli-pair expectation entries
# needed below, apart from a single real or imaginary Pauli Y factor.
def add(u, v):
    return u[0]+v[0], u[1]+v[1]


def mul(u, v):
    a, b = u
    c, d = v
    return a*c-3*b*d, a*d+b*c


def source_rows(contact):
    # Explicit integer three-step filter on a localized shared sheet followed by the
    # coherent two-walker return. After the filter the surviving characters are conjugate.
    filtered = defaultdict(int)
    for path in product((1, -1), repeat=3):
        x, c, sheet, sign = 0, 1, 0, 1
        for d in path:
            sheet = (sheet+x) % 3
            x += d
            sign *= -1 if c == d == -1 else 1
            c = d
        if (x, c) == (-1, -1):
            filtered[sheet] += sign
    output = defaultdict(int)
    for u, v in product((1, -1), repeat=2):
        for sheet, count in filtered.items():
            dest = (sheet+u+v+contact*int(u == v)) % 3
            output[(-u, -v, dest)] += count
    filtered_mass = sum(v*v for v in filtered.values())
    total = sum(v*v for v in output.values())
    zeta = ((F(1), F(0)), (F(-1, 2), F(-1, 2)), (F(-1, 2), F(1, 2)))
    psi = [tuple(v/2 for v in zeta[(a+b+contact*int(a == b)) % 3])
           for a, b in product((-1, 1), repeat=2)]

    # Independent projection of every literal common-sheet count, including filter phase.
    def transformed(values):
        ans = (F(0), F(0))
        for k, count in values:
            ans = add(ans, tuple(count*v for v in zeta[k]))
        return ans

    filtered_character = transformed(filtered.items())
    for index, (a, b) in enumerate(product((1, -1), repeat=2)):
        check = transformed((k, output.get((a, b, k), 0)) for k in range(3))
        expected = mul(filtered_character, tuple(2*v for v in psi[index]))
        assert check == expected

    # Coordinates are (T_ax, T_ay/sqrt(3), T_az); Alice uses just real Z and X.
    rows = []
    for alice in ("Z", "X"):
        entries = []
        for bob in ("X", "Y", "Z"):
            raw = (F(0), F(0))
            for i, amplitude in enumerate(psi):
                a, b = divmod(i, 2)
                target_a = 1-a if alice == "X" else a
                target_b = 1-b if bob in ("X", "Y") else b
                sign = (-1 if alice == "Z" and a == 1 else 1)
                if bob in ("Z", "Y") and b == 1:
                    sign = -sign
                partner = psi[2*target_a+target_b]
                component = mul((partner[0], -partner[1]), amplitude)
                raw = add(raw, tuple(sign*v for v in component))
            if bob == "Y":
                assert raw[0] == 0
                entries.append(-raw[1])  # Y|b> = i*(-1)^b |1-b>
            else:
                assert raw[1] == 0
                entries.append(raw[0])
        rows.append(tuple(entries))
    return tuple(rows), dict(filter_counts=[filtered.get(i, 0) for i in range(3)],
                             filter_probability=str(F(filtered_mass, 8)),
                             contact_probability_given_aligned_inputs=str(F(total, 16*filtered_mass)),
                             filter_times_aligned_contact_probability=str(F(total, 128)),
                             zero_mode_numerator=sum(filtered.values()),
                             alice_Z_row=[str(x) for x in rows[0]], alice_X_row=[str(x) for x in rows[1]])


def synchronous_source(contact, ideal_filter):
    """Literal joint steps from (0,R) twice on one localized sheet. Bob's words are classical records."""
    rows = []
    fixed_total = F(0)
    zeta = ((F(1), F(0)), (F(-1, 2), F(-1, 2)), (F(-1, 2), F(1, 2)))

    def weighted_sum(values):
        result = (F(0), F(0))
        for k, value in enumerate(values):
            result = add(result, tuple(value*z for z in zeta[k]))
        return result

    for word in product((1, -1), repeat=3):
        subset = [0]*3
        for alice in product((1, -1), repeat=3):
            a = b = k = 0
            ca = cb = 1
            sign = 1
            for d, e in zip(alice, word):
                k = (k+a+b) % 3
                sign *= (-1)**(int(ca == d == -1)+int(cb == e == -1))
                a, b, ca, cb = a+d, b+e, d, e
            if (a, ca) == (-1, -1):
                subset[k] += sign
        # Separate arithmetic for the measured Bob route's signed sheet permutation.
        b = bob_offset = 0
        cb = bob_sign = 1
        for e in word:
            bob_offset += b
            bob_sign *= -1 if cb == e == -1 else 1
            b += e
            cb = e
        shifted = [bob_sign*ideal_filter[(k-bob_offset) % 3] for k in range(3)]
        filtered_probability = F(sum(v*v for v in subset), 4**3)
        assert subset == shifted and filtered_probability == F(1, 32)
        record = dict(bob_word="".join("R" if d == 1 else "L" for d in word),
                      bob_site=b, bob_direction=cb, bob_sheet_shift_mod_3=bob_offset % 3,
                      bob_relative_sign=bob_sign, signed_filter_counts=subset,
                      filter_and_word_probability=str(filtered_probability),
                      unconditional_bob_word_probability="1/8",
                      bob_at_minus_one=(b == -1), source_contribution="0")
        if b == -1:
            # One simultaneous observed ++ hop to (0,R;0,R) at tick 4.
            # The departure sum is -2, both switch factors for output R are positive.
            landed = [subset[(k+2) % 3] for k in range(3)]
            amplitudes = defaultdict(int)
            for u, v, sheet in product((1, -1), (1, -1), range(3)):
                # Both split at 0 on tick 5 and return via -u,-v on tick 6.
                dest = (sheet+u+v+contact*int(u == v)) % 3
                amplitudes[-u, -v, dest] += landed[sheet]
            mass = F(sum(x*x for x in amplitudes.values()), 4**6)
            phase = weighted_sum(landed)
            ports = []
            for d, e in product((1, -1), repeat=2):
                port = [amplitudes[d, e, k] for k in range(3)]
                expected = mul(phase, zeta[(-d-e+contact*int(d == e)) % 3])
                assert weighted_sum(port) == expected
                ports.append(port)
            assert mass == F(1, 512)
            fixed_total += mass
            record.update(signed_counts_after_joint_hop=landed, contact_output_RR_RL_LR_LL=ports,
                          source_contribution=str(mass), per_port_character_identity=True)
        rows.append(record)
    return dict(ticks=6, alice_bob_start="0,R; 0,R; common localized sheet",
                filter_probability_all_bob_records=str(sum(F(r["filter_and_word_probability"]) for r in rows)),
                probability_bob_at_minus_one_given_filter="3/8", joint_R_hop_probability="1/4",
                contact_return_probability="1/4", fixed_source_probability=str(fixed_total),
                fixed_source_histories=sum(F(r["source_contribution"]) > 0 for r in rows), bob_histories=rows)


def synchronous_routing():
    """Exact first-hit probability within eight observed simultaneous ticks from any same-parity pair."""
    size = 2*RADIUS
    probabilities = {}
    for x0, y0 in product(range(size), repeat=2):
        if (x0-y0) % 2:
            continue
        active = {(x0, y0): 1}
        hits = 0
        for t in range(1, 9):
            next_pairs = defaultdict(int)
            hits *= 4
            for (x, y), count in active.items():
                for d, e in product((1, -1), repeat=2):
                    if x == y == size-1 and d == e == 1:
                        hits += count
                    else:
                        next_pairs[(x+d) % size, (y+e) % size] += count
            active = next_pairs
        assert hits+sum(active.values()) == 4**8
        probabilities[(x0, y0)] = F(hits, 4**8)
    minimum = min(probabilities.values())
    return dict(same_parity_start_pairs=len(probabilities), checked_block_length=8,
                minimum_hit_probability=str(minimum),
                minimizers=[list(p) for p, value in probabilities.items() if value == minimum],
                mean_tick_upper_bound=str(8/minimum), eventual_route_probability="1",
                accepted_source_probability="1/16",
                tail_bound="P(no completed directed joint arrival after 8j ticks) <= (1-p_min)^j",
                scope="All contemporaneous one-step direction records retained before settings, contact off. "
                      "A recorded step acts by a common signed sheet translation and two independent fair directions.")


def excursions(cap):
    # Disjoint radius transcripts can be merged by the exact data that determine
    # the normalized arm gate, up to scalar phase. q is the +arm departure sum.
    active = {(1, 1, 0, 1): F(1)}
    meetings = defaultdict(F)
    for ticks in range(1, cap):
        interior = defaultdict(F)
        for (r, direction, q, parity), prob in active.items():
            for d in (-1, 1):
                r_new = r+d
                q_new = (q+r) % 3
                # Exactly one of the two mirrored arms incurs LL when the outward
                # increment repeats. Their relative sign is the product of the signs.
                s_new = -parity if direction == d else parity
                if r_new in (0, RADIUS):
                    meetings[(d, q_new, s_new)] += prob/2
                else:
                    interior[(r_new, d, q_new, s_new)] += prob/2
        active = interior
    timeout = sum(active.values())
    assert sum(meetings.values())+timeout == 1
    return meetings, timeout


def scores(vector, key):
    x, y_over_root3, z = vector
    direction, q, parity = key
    signed_x = parity*(COS[q]*z + 3*SIN_BY_ROOT3[q]*y_over_root3)
    signed_z = direction*x
    return {"X": signed_x, "Z": signed_z}


def choose_local(choices):
    # Prefer direct Z when tied; an X read uses one additional unmasked step.
    basis = "Z" if abs(choices["Z"]) >= abs(choices["X"]) else "X"
    sign = 1 if choices[basis] >= 0 else -1
    return basis, sign


def certificate(cap, source, policy_source):
    alice_z, alice_x = source
    target = tuple(a+b for a, b in zip(*policy_source))
    meeting_masses, timeout = excursions(cap)
    corrs = [[F(0), -alice_z[0]], [F(0), -alice_x[0]]]  # B1 reads -X immediately.
    decisions = []
    for key, mass in sorted(meeting_masses.items()):
        basis, sign = choose_local(scores(target, key))
        for i, row in enumerate(source):
            corrs[i][0] += mass*sign*scores(row, key)[basis]
        decisions.append(dict(last_radial_increment=key[0], departure_sum_mod_3=key[1],
                              relative_arm_sign=key[2], probability=str(mass),
                              read=basis, output_multiplier=sign))
    # At timeout the sign of site displacement reveals the earliest H output.
    # The two open arms carry equal attenuation. Hence the arm read implements X
    # at the original meeting exactly, with either port orientation selectable.
    for i, row in enumerate(source):
        corrs[i][0] -= timeout*row[0]
    S = corrs[0][0]+corrs[0][1]+corrs[1][0]-corrs[1][1]
    return S, dict(cap=cap, physical_tick_cap=cap+1, timeout_probability=str(timeout),
                   total_probability=str(timeout+sum(meeting_masses.values())), groups=decisions,
                   correlations=[[str(p) for p in row] for row in corrs],
                   probabilities_equal=[[str((1+p)/2) for p in row] for row in corrs],
                   CHSH=str(S), CHSH_decimal=float(S), margin=str(S-2))


def literal_dictionary(cap):
    """Unmerged small-tree test of return gates and timeout side effects on both origins."""
    phase = np.exp(-2j*pi/3)
    residuals = []
    for start in (0, RADIUS):
        def visit(state, path):
            t = len(path)-1
            r = path[-1]
            arrived = t > 0 and r in (0, RADIUS)
            if arrived or t == cap:
                directions = np.diff(path)
                parity = (-1)**sum(int(d == prev) for d, prev in zip(directions, directions[1:]))
                q = sum(path[:-1]) % 3
                probability = 2.**(1-t)
                if arrived:
                    site = (start+r) % (2*RADIUS)
                    u = np.stack([state[(site, direction)] for direction in (1, -1)])/sqrt(probability)
                    key = int(directions[-1]), q, parity
                    analytic = matrix_for_run(path, 3)
                    residuals.append(float(np.linalg.norm(u-analytic)))
                    for basis, matrix in (("X", X), ("Z", Z)):
                        predicted = np.array([float(scores(v, key)[basis]) for v in
                                              ((1, 0, 0), (0, F(1, 3), 0), (0, 0, 1))])
                        # For physical unit y, use y/sqrt(3)=1/sqrt(3).
                        predicted[1] *= sqrt(3)
                        measured = u.conj().T@matrix@u
                        residuals.append(float(np.linalg.norm(measured-sum(z*p for z, p in zip(predicted, PAULI)))))
                else:
                    right, left = np.zeros((2, 2), complex), np.zeros((2, 2), complex)
                    for (site, _), amps in state.items():
                        if (site-start) % (2*RADIUS) < RADIUS:
                            right += np.outer(amps.conj(), amps)
                        else:
                            left += np.outer(amps.conj(), amps)
                    residuals.extend([float(np.linalg.norm((right+left)/probability-np.eye(2))),
                                      float(np.linalg.norm((right-left)/probability-X))])
                return
            grouped = defaultdict(dict)
            for (site, c), amps in state.items():
                for d in (1, -1):
                    out = (site+d) % (2*RADIUS)
                    delta = (out-start) % (2*RADIUS)
                    key = min(delta, 2*RADIUS-delta)
                    value = amps*phase**(site % 3)*(-1 if c == d == -1 else 1)/sqrt(2)
                    grouped[key][(out, d)] = grouped[key].get((out, d), 0)+value
            for radius, child in grouped.items():
                visit(child, path+[radius])

        visit({(start, 1): np.array([1., 0.]), (start, -1): np.array([0., 1.])}, [0])
    return max(residuals)


def source_crosscheck(solution):
    # Full four-spinor source evaluated against the summed physical effects, with
    # no use of the exact Pauli-row values or the endpoint score expression.
    checks = []
    for orientation in (1, -1):
        phase = np.exp(-2j*pi*orientation/3)
        psi = np.array([phase**(a+b+int(a == b))/2 for a, b in product((-1, 1), repeat=2)])
        bob = -float(F(solution["timeout_probability"]))*X.astype(complex)
        for group in solution["groups"]:
            q = group["departure_sum_mod_3"]
            e = group["relative_arm_sign"]
            perm = X if group["last_radial_increment"] == -1 else np.eye(2)
            u = perm@np.diag([phase**q, e*phase**(-q)])@np.array([[1, 1], [1, -1]])/sqrt(2)
            observable = X if group["read"] == "X" else Z
            bob += float(F(group["probability"]))*group["output_multiplier"]*(u.conj().T@observable@u)
        computed = np.array([[np.vdot(psi, np.kron(a, b)@psi).real for b in (bob, -X)] for a in (Z, X)])
        exact = np.array([[float(F(entry)) for entry in row] for row in solution["correlations"]])
        checks.append(float(np.max(abs(computed-exact))))
    return max(checks)


def main(out):
    out.mkdir(parents=True, exist_ok=True)
    source, facts = source_rows(1)
    product_source, control_source = source_rows(0)
    synchronous = synchronous_source(1, facts["filter_counts"])
    synchronous_control = synchronous_source(0, control_source["filter_counts"])
    routing = synchronous_routing()
    scores_by_cap = [certificate(cap, source, source)[1] for cap in (2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, CAP)]
    best, final = certificate(CAP, source, source)
    control, product_control = certificate(CAP, product_source, source)
    literal_error = literal_dictionary(8)
    signed_source_error = source_crosscheck(final)
    checks = dict(aligned_source_factors=facts["filter_times_aligned_contact_probability"] == "1/16",
                  fixed_synchronous_source=synchronous["fixed_source_probability"] == "3/512" and
                                           synchronous["fixed_source_histories"] == 3 and
                                           len(synchronous["bob_histories"]) == 8,
                  synchronous_no_contact_control=synchronous_control["fixed_source_probability"] == "3/512",
                  synchronous_all_route_access=routing["same_parity_start_pairs"] == 72 and
                                               F(routing["minimum_hit_probability"]) > 0,
                  source_correlation_exact=source == ((F(-3, 4), F(-1, 4), F(0)),
                                                      (F(1, 4), F(-1, 4), F(-3, 4))),
                  all_branches_counted=all(x["total_probability"] == "1" for x in scores_by_cap),
                  literal_finite_tree=literal_error < 2e-13,
                  summed_effect_both_orientations=signed_source_error < 2e-13,
                  finite_all_output_CHSH=best == F(134503435, 67108864) and best > 2,
                  zero_contact_same_policy=abs(control) <= 2,
                  shorter_cap_retained=scores_by_cap[-3]["CHSH_decimal"] < 2)
    report = dict(checks=checks, radius=RADIUS, ring_sites=12, sheet_order=3, source=facts,
                  fixed_synchronous_source=synchronous, all_accepted_synchronous_routing=routing,
                  signed_y_coordinate="Second coordinate stores physical Pauli-Y coefficient divided by sqrt(3).",
                  labels="Rows Alice Z, X. Columns Bob B0, B1. S=E00+E01+E10-E11.",
                  policy="B1 reads -X by side after the first split. B0 measures radius through cap 24. "
                         "At a meeting read the signed X or Z specified by the table, breaking ties toward Z. "
                         "If the interior cap is reached, read the signed side as -X of the segment input. "
                         "Stopped parties have already emitted a binary result; no idle unitary is needed.",
                  literal_tree_max_residual=literal_error, summed_bob_effect_max_residual=signed_source_error,
                  certificate=final,
                  shorter_cap_results=[{k: r[k] for k in ("cap", "timeout_probability", "CHSH", "CHSH_decimal")}
                                       for r in scores_by_cap[:-1]],
                  no_contact_source=control_source, no_contact_fixed_synchronous_source=synchronous_control,
                  no_contact_same_policy=product_control,
                  scope="Exact model prediction conditioned on a source herald preceding both setting choices. "
                        "Every post-herald run contributes. The physical assumptions of Bell testing were not measured.")
    (out/"radial_bell.json").write_text(json.dumps(report, indent=2, allow_nan=False)+"\n", encoding="utf8")
    print(checks, "S =", best, "contact off =", control)
    if not all(checks.values()):
        raise SystemExit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    main(parser.parse_args().output)
