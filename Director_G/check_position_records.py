"""Position-space flights with a finite causal cone and selective coarse records."""

import argparse
import csv
import json
from decimal import Decimal, localcontext
from itertools import product
from math import comb, pi, sqrt
from pathlib import Path

import numpy as np


def step(state, phase):
    right = phase * state[:, 0]
    left = phase * state[:, 1]
    out = np.zeros_like(state)
    out[1:, 0] = (right[:-1]+left[:-1])/sqrt(2)
    out[:-1, 1] = (right[1:]-left[1:])/sqrt(2)
    return out


def mass(state):
    return float(np.sum(abs(state)**2))


def prepare(length, x, blocks, phase):
    state = np.zeros((length, 2), dtype=np.complex128)
    state[x == 0, 0] = 1
    for i in range(blocks):
        state = step(step(state, phase), phase)
        state[:, i % 2] = 0
    success = mass(state)
    return state/sqrt(success), success


def flight(order, sign, switched):
    delta = (pi/order)**0.25
    blocks = 2*round(delta**(-2.5)/2)
    switch = round(0.75/delta**3)
    reads = [round(t/delta**3) for t in (1.4, 2.3, 3.0)]
    radius = 2*blocks+reads[-1]+2
    x = np.arange(-radius, radius+1)
    Y = x*delta**2
    phase = np.exp(-1j*sign*pi/order*x)
    inverse = np.conj(phase)
    start, success = prepare(len(x), x, blocks, phase)

    def advance(state, low, high):
        for n in range(low, high):
            state = step(state, inverse if switched and n >= switch else phase)
        return state

    nodes = {"": start}
    nominal_states = {}
    # Uniform coordinate bins fixed before the flight. Track two nominated words
    # directly. Completeness gives the probability of every other word combined.
    width, offset = 0.75, 0.18
    bins = np.floor((Y-offset)/width).astype(int)
    ray_bins = {s: [] for s in (-1, 1)}
    gap_error = 0.
    coherence = {}
    previous = 0
    for read_index, end in enumerate(reads):
        time = end*delta**3
        centre = time*time/2 - (max(0.,time-switch*delta**3)**2 if switched else 0.)
        for s in (-1, 1):
            target = int(np.floor((s*centre-offset)/width))
            ray_bins[s].append(target)
            continued = advance(nominal_states.get(s, start), previous, end)
            nominal_states[s] = continued*(bins == target)[:, None]
        children = {}
        for word, state in nodes.items():
            evolved = advance(state, previous, end)
            for symbol, mask in (("L", x < 0), ("R", x >= 0)):
                observed = evolved*mask[:, None]
                children[word+symbol] = observed
                if read_index == 0:
                    # Spatial translation by two has exactly zero expectation after
                    # a full site read with the label subsequently erased.
                    coherence[symbol] = float(abs(np.vdot(observed[2:], observed[:-2]))/mass(observed))
            gap_error = max(gap_error, abs(mass(evolved)-mass(state)),
                            abs(mass(children[word+"L"])+mass(children[word+"R"])-mass(state)))
        previous, nodes = end, children
    assert ray_bins[-1][0] != ray_bins[1][0]
    ray_prob = [mass(nominal_states[s]) for s in (-1, 1)]
    rows = [(word, mass(state), float(Y @ np.sum(abs(state)**2, axis=1)))
            for word, state in sorted(nodes.items())]
    return rows, dict(order=order, sign=sign, switched=switched, delta=delta,
                      blocks=blocks, preparation_success=success, steps=reads,
                      switch_step=(switch if switched else None), attained_times=[n*delta**3 for n in reads],
                      sign_word_total=sum(r[1] for r in rows), maximum_norm_or_partition_error=gap_error,
                      coherent_two_site_overlap=coherence, site_dephased_two_site_overlap=0,
                      bin_width=width, bin_offset=offset, two_bin_words=[ray_bins[-1], ray_bins[1]],
                      two_word_probabilities=ray_prob, all_other_bin_words_probability=1-sum(ray_prob))


def projection_control():
    # Compare unnormalized disturbance and success for overlapping real subspaces.
    rows = []
    for angle, count in product((0., 0.02, 0.3, 1.3), (1, 2, 7, 64)):
        v = np.array([1., 0.])
        state = v.copy()
        budget = 0.
        for j in range(count):
            alpha = angle*np.cos(j)
            u = np.array([np.cos(alpha), np.sin(alpha)])
            budget += np.sin(alpha)**2
            state = u*(u @ state)
        rows.append(dict(angle=angle, count=count, budget=float(budget), loss=1-mass(state),
                         disturbance_squared=mass(state-v)))
    return rows


def accepted_yield_controls():
    # Synthetic class channels exercise the likelihood and acceptance inequalities
    # without a floating-point trigonometric approximation to a physical sheet angle.
    rows = []
    with localcontext() as ctx:
        ctx.prec = 65
        for k in (4, 12, 32, 80, 160):
            qs = [Decimal(0), Decimal("0.10"), Decimal("0.35")]
            prior = [Decimal(1)/5, Decimal(2)/5, Decimal(2)/5]
            eta = Decimal("0.035")
            acceptance = good_mass = Decimal(0)
            for count in range(k+1):
                weights = [w*comb(k,count)*(q**count if count else 1)*
                           ((1-q)**(k-count) if count < k else 1) for q,w in zip(qs,prior)]
                total = sum(weights)
                if weights[1] >= (1-eta)*total:
                    acceptance += total
                    good_mass += weights[1]
            h_error = sum((prior[1]*prior[j]).sqrt()*
                          ((qs[1]*qs[j]).sqrt()+((1-qs[1])*(1-qs[j])).sqrt())**k for j in (0,2))
            lower = prior[1]-((1-eta)/eta).sqrt()*h_error
            rows.append(dict(k=k, acceptance=str(acceptance), target_in_accepted=str(good_mass),
                             lower_bound=str(lower), upper_bound=str(prior[1]/(1-eta)),
                             agrees=bool(lower <= good_mass+Decimal("1e-60") and
                                         acceptance <= prior[1]/(1-eta)+Decimal("1e-60"))))
    return rows


def main(output):
    output.mkdir(parents=True, exist_ok=True)
    flights, conjugation = [], 0.
    with (output/"position_histories.csv").open("w", encoding="utf8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(("M", "effective_initial_sign", "reverse_field", "side_word", "joint_probability",
                         "joint_first_moment_at_last_read"))
        for order, switched in product((127, 509, 2039, 8191), (False, True)):
            reference = None
            for sign in (-1, 1):
                rows, metrics = flight(order, sign, switched)
                numbers = np.array([row[1:] for row in rows])
                if reference is not None:
                    conjugation = max(conjugation, float(np.max(abs(numbers-reference))))
                reference = numbers
                flights.append(metrics)
                writer.writerows((order, sign, switched, *row) for row in rows)
    control = projection_control()
    checks = dict(sign_probability_total=all(abs(f["sign_word_total"]-1)<2e-12 for f in flights),
                  unitary_and_record_norms=all(f["maximum_norm_or_partition_error"]<2e-12 for f in flights),
                  conjugate_sheet_agreement=(conjugation < 2e-12),
                  bin_word_complement=all(0 <= f["all_other_bin_words_probability"] <= 1 for f in flights),
                  retained_site_coherence=all(min(f["coherent_two_site_overlap"].values())>0.1 for f in flights),
                  sequential_bound=all(r["disturbance_squared"] <= r["budget"]+1e-13 and
                                       r["loss"] <= 4*r["budget"]+1e-13 for r in control))
    accepts = accepted_yield_controls()
    checks["posterior_yield_inequalities"] = all(row["agrees"] for row in accepts)
    report = dict(checks=checks, synthetic_posterior_controls=accepts, flights=flights, conjugation_maximum=conjugation, projection_control=control)
    (output/"position_records.json").write_text(json.dumps(report, indent=2, allow_nan=False)+"\n",encoding="utf8")
    print(checks)
    if not all(checks.values()):
        raise SystemExit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    main(parser.parse_args().output)
