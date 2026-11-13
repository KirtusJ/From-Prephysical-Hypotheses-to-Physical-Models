"""Check the full Fourier amplitudes and measured flights for signed preparation blocks."""

import argparse
import json
import platform
from itertools import product
from math import comb, pi
from pathlib import Path

import numpy as np

from check_position_records import flight, mass, step


SCHEDULES = ("constant", "quarters", "alternating")
PROFILE_TOLERANCE = 2e-13
MASS_TOLERANCE = 2e-12


def block_signs(blocks, schedule):
    if schedule == "constant":
        return [1] * blocks
    if schedule == "alternating":
        return [(-1) ** j for j in range(blocks)]
    if schedule == "quarters" and blocks % 4 == 0:
        q = blocks // 4
        return [1] * q + [-1] * (2 * q) + [1] * q
    raise ValueError("use a named schedule and four complete quarters for 'quarters'")


def offsets(signs):
    suffix = 0
    result = []
    for sign in reversed(signs):
        result.append(2 * suffix + sign)
        suffix += sign
    return result[::-1]


def moments_match(signs, values, schedule):
    # Integer numerators of the mean and population variance, denominators m and m².
    m = len(signs)
    moment1 = sum(values)
    moment2 = m * sum(value**2 for value in values) - moment1**2
    expected1 = sum((2 * j + 1) * s for j, s in enumerate(signs))
    if moment1 != expected1:
        return False
    if schedule == "constant":
        return moment1 == m**2 and 3 * moment2 == m**2 * (m**2 - 1)
    if schedule == "quarters":
        return moment1 == 0 and 12 * moment2 == m**2 * (m**2 - 4)
    if schedule == "alternating":
        return moment1 == m * signs[-1] and moment2 == 0
    # An independent difference identity for the population variance.
    return moment2 == sum((a - b)**2 for j, a in enumerate(values) for b in values[:j])


def literal_preparation(x, signs, h, start):
    state = np.zeros((len(x), 2), dtype=complex)
    state[x == 0, start] = 1
    for j, s in enumerate(signs):
        phase = np.exp(-1j * s * h * x)
        state = step(step(state, phase), phase)
        state[:, (start + j) % 2] = 0
    return state


def spectral_control(signs, h, schedule, start=0):
    m = len(signs)
    values = offsets(signs)
    directions = [(1 - 2*start) * (-1)**j for j in range(1, m+1)]
    displacement = sum(directions)
    # Each output-direction phase uses the momentum after its block.
    phase_units = sum(d * (a - s) for d, a, s in zip(directions, values, signs))
    x = np.arange(-2*m-2, 2*m+3)
    state = literal_preparation(x, signs, h, start)
    k = np.linspace(-pi, pi, 127, endpoint=False)
    transform = np.exp(-1j * k[:, None] * x)
    output = (start + m) % 2
    literal = transform @ state[:, output]
    profile = np.prod(np.sin(k[:, None] + h*np.array(values)), axis=1)
    predicted = (-1j)**m * np.exp(-1j*(displacement*k + phase_units*h)) * profile

    # Re-evaluate the odd-block, wrong-channel comparison used by the interrupted checker.
    right = transform @ state[:, 0]
    fitted = np.vdot(profile, right) / np.vdot(profile, profile)
    row = dict(
        schedule=schedule, signs=list(signs), blocks=m, h=h, start="RL"[start],
        output="RL"[output], displacement=displacement, phase_coefficient=phase_units,
        mean_offset=sum(values)/m, offset_variance=float(np.var(values)),
        mean_and_variance=moments_match(signs, values, schedule),
        profile_residual=float(np.max(abs(literal-predicted))),
        other_channel_max=float(np.max(abs(state[:, 1-output]))),
        yield_ratio=mass(state)/(comb(2*m, m)/4**m),
        former_right_channel_fit_modulus=float(abs(fitted)),
    )
    if schedule == "alternating":
        zero_field = literal_preparation(x, signs, 0., start)
        origin_direction = 1 - 2*start
        # Fourier shift k -> k+s_m*h is modulation exp(-i*s_m*h*x) in position.
        phase = np.exp(-1j*h*(origin_direction*m + signs[-1]*x))
        row["alternating_state_residual"] = float(np.max(abs(state - phase[:, None]*zero_field)))
    return row


def flight_control():
    rows = []
    for order in (127, 509, 2039, 8191):
        delta = (pi/order)**0.25
        blocks = 4*round(delta**(-2.5)/4)
        reference_yield = comb(2*blocks, blocks)/4**blocks
        for schedule in SCHEDULES:
            signs = block_signs(blocks, schedule)
            branches, metrics = flight(order, 1, True, preparation_signs=signs)
            word_mass = {word: probability for word, probability, _ in branches}
            expected_mass = word_mass["LLR"] + word_mass["RRL"]
            rows.append(dict(
                M=order, delta=delta, blocks=blocks, schedule=schedule,
                preparation_success=metrics["preparation_success"], zero_field_yield=reference_yield,
                yield_ratio=metrics["preparation_success"]/reference_yield, sign_words=word_mass,
                switch_word_mass=expected_mass, off_word_mass=sum(
                    prob for word, prob in word_mass.items() if word not in ("LLR", "RRL")
                ),
                switch_step=metrics["switch_step"], attained_switch=metrics["switch_step"]*delta**3,
                read_steps=metrics["steps"], attained_times=metrics["attained_times"],
                total=metrics["sign_word_total"], partition_error=metrics["maximum_norm_or_partition_error"],
                switch_words_have_majority=bool(expected_mass > 0.5),
            ))
    return rows


def main(output):
    output.mkdir(parents=True, exist_ok=True)
    profiles = [
        spectral_control(block_signs(m, schedule), h, schedule, start)
        for m in (1, 2, 3, 4, 5, 8, 16, 32)
        for h in (0., 0.017, -0.031, 0.73)
        for schedule in SCHEDULES if schedule != "quarters" or m % 4 == 0
        for start in (0, 1)
    ]
    diverse = [
        spectral_control(signs, 0.37, "all_sign_words", start)
        for m in range(1, 7) for signs in product((1, -1), repeat=m) for start in (0, 1)
    ]
    collision = spectral_control([1, 1], pi/2, "constant")
    alternating_half_turn = spectral_control([1, -1], pi/2, "alternating")
    flights = flight_control()
    all_profiles = profiles + diverse
    alternating = [r for r in profiles if r["schedule"] == "alternating"]
    checks = dict(
        offset_moments=all(r["mean_and_variance"] for r in all_profiles),
        literal_profile=all(r["profile_residual"] < PROFILE_TOLERANCE and
                            r["other_channel_max"] < PROFILE_TOLERANCE for r in all_profiles),
        alternating_full_state=all(r["alternating_state_residual"] < PROFILE_TOLERANCE for r in alternating),
        alternating_yield=all(abs(r["yield_ratio"]-1) < MASS_TOLERANCE for r in alternating+[
            row for row in flights if row["schedule"] == "alternating"
        ]),
        all_history_mass=all(abs(r["total"]-1) < MASS_TOLERANCE and
                             r["partition_error"] < MASS_TOLERANCE for r in flights),
        two_block_half_turn_alias=all(abs(r["yield_ratio"]-1) < MASS_TOLERANCE
                                     for r in (collision, alternating_half_turn)),
    )
    odd_probe = next(r for r in profiles if r["start"] == "R" and r["blocks"] == 5
                     and r["schedule"] == "constant" and r["h"] == 0.017)
    report = dict(
        runtime=dict(python=platform.python_version(), numpy=np.__version__),
        tolerances=dict(profile=PROFILE_TOLERANCE, mass=MASS_TOLERANCE),
        checks=checks, profiles=profiles, exhaustive_small_sign_words=diverse, finite_reversals=flights,
        adverse_controls=dict(
            earlier_checker_sha256="e04c785a549694ca30718afedc8ba7569f9e7018a2ffda9220ebad2057e4adc9",
            earlier_four_predicates_passed=True, earlier_even_profiles=36,
            earlier_fitted_residual_max=1.7377739072730912e-15,
            nonunique_yield_maximum=dict(h=pi/2, constant_two_block_ratio=collision["yield_ratio"],
                                         alternating_two_block_ratio=alternating_half_turn["yield_ratio"]),
            odd_right_channel_extension=dict(
                inputs="m=5, h=0.017, constant, initial R; original right-channel-only comparison",
                original_observed_fit_modulus=0.0, original_observed_fitted_residual=0.0,
                rerun_fit_modulus=odd_probe["former_right_channel_fit_modulus"],
                tested_unit_modulus=abs(odd_probe["former_right_channel_fit_modulus"]-1) < PROFILE_TOLERANCE,
                actual_output=odd_probe["output"], corrected_unfitted_residual=odd_probe["profile_residual"],
            ),
            finite_switch_word_majority=dict(threshold="LLR + RRL > 0.5, descriptive finite benchmark",
                                            passed=sum(r["switch_words_have_majority"] for r in flights),
                                            trials=len(flights)),
        ),
    )
    (output/"field_echo.json").write_text(json.dumps(report, indent=2, allow_nan=False)+"\n", encoding="utf8")
    print("Numerical identity and completeness checks", checks)
    print("Observed finite reversal majorities", report["adverse_controls"]["finite_switch_word_majority"])
    if not all(checks.values()):
        raise SystemExit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    main(parser.parse_args().output)
