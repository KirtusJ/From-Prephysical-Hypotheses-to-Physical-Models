"""A finite two-source test of the A position read and its speed-one cone.

Run python -B check_moving_source_records.py results. A prepared two-particle
plus-band sector is evolved on the ring; the sender is changed before flight.
All angles, speeds and times are in the units of the periodic-interaction model.
"""
import argparse
import json
from math import pi, sqrt
from pathlib import Path
import platform

from check_periodic_force import field_shape, modes, plus_section, vector_norm
from check_folded_pair import joint_walk_step, spectral_walk_step
import numpy as np


SIZES = (32, 64, 96, 128)
EXPLORATORY_SIZES = (192, 256)
SOURCE_CENTRES = (pi / 2, pi)
BINS = ((1 / 64, 17 / 32), (-0.4, 0.18))
TARGET_TIME = 1.0
SPEED = 1.0


def packet(size, epsilon, centre, section):
    """Normalized zero-central-momentum envelope on the band at -pi/2."""
    ell = modes(size)
    amplitudes = np.exp(-epsilon * ell**2 / 2 - 1j * ell * centre)
    amplitudes /= vector_norm(amplitudes)
    coefficients = amplitudes[:, None] * section
    spinor = np.fft.ifft(np.roll(coefficients, -size // 4, axis=0), axis=0, norm="ortho")
    return spinor, float(epsilon * np.sum(ell * abs(amplitudes)**2))


def region(sites, bounds, radius, closed):
    """Periodic interval or its closed continuous angular dilation."""
    lo, hi = bounds
    centre = (hi + lo) / 2
    distance = abs((sites - centre + pi) % (2 * pi) - pi)
    half_width = (hi - lo) / 2 + radius
    return distance <= half_width if closed else distance < half_width


def cone_record(left, right, mask):
    # The B reduction on an occupation patch is vacuum plus its restricted
    # one-particle ket. The vacuum block is orthogonal to the particle block.
    u, v = left[mask].ravel(), right[mask].ravel()
    p, q = float(np.vdot(u, u).real), float(np.vdot(v, v).real)
    overlap = np.vdot(u, v)
    radicand = (p + q)**2 - 4 * abs(overlap)**2
    if radicand < -1e-14:
        raise ArithmeticError("Invalid Gram discriminant")
    distance = (abs(p - q) + sqrt(max(0.0, radicand))) / 2
    # Independently diagonalize the restricted particle block. Include the
    # one-dimensional vacuum block, which has eigenvalue q-p.
    difference = np.outer(u, u.conj()) - np.outer(v, v.conj())
    eig_distance = float((abs(p-q) + np.sum(abs(np.linalg.eigvalsh(difference)))) / 2)
    if abs(eig_distance-distance) > 1e-12 or distance > max(p,q)+1e-12:
        raise ArithmeticError("Two cone-distance evaluations disagree")
    return {"site_count": int(np.count_nonzero(mask)),
            "B_mass_pi_over_2": p, "B_mass_pi": q,
            "inner_product_real": float(overlap.real), "inner_product_imag": float(overlap.imag),
            "trace_distance": distance, "eigenvalue_check_abs_error": abs(eig_distance-distance)}


def trial_size(size):
    a = 2*pi/size
    epsilon = delta = sqrt(a)
    tau = epsilon*delta**2
    steps = round(TARGET_TIME/tau)
    elapsed = steps*tau
    sheet_order = size**3+1
    sites = a*np.arange(size)
    section = plus_section(size)
    observer, observer_p = packet(size, epsilon, 0.0, section)
    sources = [packet(size, epsilon, centre, section) for centre in SOURCE_CENTRES]
    masks = [region(sites, b, 0, False) for b in BINS]
    cones = [cone_record(sources[0][0], sources[1][0], region(sites, b, SPEED*elapsed, True))
             for b in BINS]
    diagnostics = []
    comparisons = []
    for kappa in (0, 1):
        desired_angle = kappa*delta**2*field_shape(size)
        gain = np.rint(sheet_order*desired_angle/(2*pi)).astype(np.int64)
        implemented_angle = 2*pi*gain/sheet_order
        departure = np.exp(-1j*implemented_angle)
        probabilities = []
        for centre, (source, source_p) in zip(SOURCE_CENTRES, sources):
            state = (observer[:, None, :, None]*source[None, :, None, :]).reshape(size, size, 4)
            initial_mass = float(np.sum(abs(state)**2))
            initial_prob = [float(np.sum(abs(state[mask])**2)) for mask in masks]
            direct = joint_walk_step(state, departure)
            fourier = spectral_walk_step(state, departure)
            step_error = vector_norm(direct-fourier)
            if step_error > 2e-12:
                raise ArithmeticError("Real-space and Fourier first steps disagree")
            state = direct
            for _ in range(1, steps):
                state = joint_walk_step(state, departure)
            full_flight_difference = None
            if size == EXPLORATORY_SIZES[0] and kappa == 1:
                for _ in range(1, steps):
                    fourier = spectral_walk_step(fourier, departure)
                full_flight_difference = vector_norm(state-fourier)
                if full_flight_difference > 2e-12:
                    raise ArithmeticError("Full first exploratory flight differs in Fourier space")
            A_marginal = np.sum(abs(state)**2, axis=(1, 2))
            final_mass = float(A_marginal.sum())
            if max(abs(initial_mass-1), abs(final_mass-1)) > 2e-12:
                raise ArithmeticError("Normalized walk lost mass")
            final_prob = [float(A_marginal[mask].sum()) for mask in masks]
            probabilities.append(final_prob)
            diagnostics.append({"kappa": kappa, "B_centre": centre, "initial_probability_sum": initial_mass,
                                "final_probability_sum": final_mass, "initial_bin_probabilities": initial_prob,
                                "A_mean_envelope_momentum": observer_p, "B_mean_envelope_momentum": source_p,
                                "first_step_Fourier_check_norm": step_error,
                                "full_Fourier_flight_check_norm": full_flight_difference,
                                "final_bin_probabilities": final_prob})
        for bin_id, cone in enumerate(cones):
            left, right = probabilities[0][bin_id], probabilities[1][bin_id]
            gap = abs(left-right)
            excess = gap-cone["trace_distance"]
            if kappa == 0 and gap > 2e-12:
                raise ArithmeticError("A free read changed with the remote preparation")
            comparisons.append({"kappa": kappa, "bin_index": bin_id,
                                "A_bin_probability_B_pi_over_2": left, "A_bin_probability_B_pi": right,
                                "signed_probability_difference": left-right, "binary_total_variation": gap,
                                "excess_over_speed_one_cone_trace_bound": excess,
                                "same_clock_maximum_error_lower_bound": max(0.0, excess)/2})
    return {"N":size, "epsilon":epsilon, "delta":delta, "spacing":a, "tau":tau, "ticks":steps,
            "attained_time":elapsed, "geometric_cone_radius":SPEED*elapsed, "sheet_order":sheet_order,
            "max_attractive_rounding_angle_error":float(np.max(abs(implemented_angle-desired_angle))),
            "single_sector_state_complex_entries":4*size**2,
            "bins":[{"endpoints":list(b), "read_site_count":int(mask.sum()), "initial_cone":cone}
                    for b, mask, cone in zip(BINS, masks, cones)],
            "flights":diagnostics, "comparisons":comparisons}


def main(output):
    rows = [trial_size(size) for size in (*SIZES, *EXPLORATORY_SIZES)]
    result = {
        "protocol":"Fixed unit-speed comparison, shrinking-action torus sequence, target flight time 1. The same A input and gate sequence are used for both B centres at each coupling and size.",
        "read":"One final A position projection in each predeclared open bin, periodic modulo 2*pi. Both probabilities are computed on the same unmeasured state. No intermediate read, rejection, or postselection.",
        "cone":"Use the closed continuous T_N-neighborhood of the entire open bin's closure before selecting lattice sites. This includes every possible speed-one backward support and can exceed the dilation of occupied read sites on a coarse grid.",
        "input":"Product of two normalized periodic Fourier Gaussians exp(-epsilon*l^2/2) with zero central momentum in the sampled positive-curvature tensor band. The coin spinors, including their phases, enter the B cone reductions.",
        "physical_assumptions":"The selected sheet character and localized band packets are supplied as initial resources. Their physical preparation time and success probability are unknown. All other local inputs and auxiliaries must be identical in the cone. The reported times begin after preparation.",
        "interaction":"Integer gain round((N^3+1)*delta^2*kappa*(1-cos(Y_A-Y_B))/(2*pi)); one prepared sheet character exp(-2*pi*i*g/(N^3+1)). Each coin H tensor H, departure phase and pair of conditional shifts is unitary; full mass equals one algebraically.",
        "finite_interpretation":"The B vacuum/one-particle trace distance bounds this binary read in any speed-one model obeying the physical input and detector premises. Positive excess supplies a finite lower bound of half the excess on maximum model-to-target error over the two inputs. A nonpositive excess yields zero lower bound. Finite values have no extrapolated TV claim.",
        "roundoff":"IEEE binary64 amplitudes (complex128). Normalization, free-source invariance and the independent first-step transform are checked to 2e-12; the B cone eigenvalue calculation is checked to 1e-12. Reported lower bounds use numerical evaluations.",
        "primary_sizes":list(SIZES), "exploratory_sizes":list(EXPLORATORY_SIZES),
        "followup":"After observing the four primary sizes, the same two detector bins, time rule and source preparations were kept for two larger rings. The exploratory sizes were selected together before either larger flight.",
        "runtime":{"python":platform.python_version(), "numpy":np.__version__}, "sizes":rows}
    output.mkdir(parents=True, exist_ok=True)
    destination = output/"moving_source_records.json"
    destination.write_bytes((json.dumps(result, indent=2, allow_nan=False)+"\n").encode())
    print(destination)
    for row in rows:
        print(row["N"], "T", round(row["attained_time"], 6),
              [(b["bin_index"], round(b["binary_total_variation"], 6),
                round(b["excess_over_speed_one_cone_trace_bound"], 6))
               for b in row["comparisons"] if b["kappa"] == 1])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    main(parser.parse_args().output)
