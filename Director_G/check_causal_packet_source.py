"""Bounded-speed dyadic parity-box preparation, inverse routing and triangle filter.

Run python -B check_causal_packet_source.py OUTPUT_DIRECTORY. Onsite gates are
real and coherent, and each physical stream advances exactly one site.
"""

import argparse
import cmath
import json
from collections import Counter
from fractions import Fraction
from itertools import pairwise
from math import ceil, pi, sin, sqrt, tan
from pathlib import Path


def compact(terms):
    return {cell: v for cell, v in terms.items() if v}


def h(state):
    out = Counter()
    for (x, c), v in state.items():
        out[x, 1] += v
        out[x, -1] += c * v
    return compact(out)


def swap(state, sites=None):
    return {(x, -c if sites is None or x in sites else c): v for (x, c), v in state.items()}


def stream(state, distance):
    for _ in range(distance):
        state = {(x + c, c): v for (x, c), v in state.items()}
    return state


def energy(state):
    return sum(v * v for v in state.values())


def tree(B, align=True):
    state = {(0, 1): 1}
    layers = []
    d = B // 2
    while d:
        centres = sorted({x for x, c in state})
        if align:
            assert all(c == 1 for x, c in state)
        if len(centres) > 1:
            assert all(v - u == 4 * d for u, v in pairwise(centres))
        lefts = {x - d for x in centres}
        state = stream(h(state), d)
        if align:
            state = swap(state, lefts)
        layers.append((d, lefts))
        d //= 2
    return state, layers


def gather(state, layers):
    for distance, lefts in reversed(layers):
        state = swap(state, lefts)
        # Reverse a stream with local rail exchange on both sides of a
        # positive-time stream. The global H is the same on the reverse route.
        state = swap(stream(swap(state), distance))
        state = h(state)
    return state


def spectrum(state, k):
    # Both final rails are orthogonal records, so they are summed in power.
    components = {1: 0j, -1: 0j}
    for (x, c), v in state.items():
        components[c] += v * cmath.exp(-1j * x * k)
    return sum(abs(v) ** 2 for v in components.values()) / energy(state)


def triangle_filter(box, layers, B):
    state = box
    failures = []
    for j, (d, _) in enumerate(layers, 1):
        state = h(stream(h(state), d))
        fail = {p: v for p, v in state.items() if p[1] == -1}
        state = {p: v for p, v in state.items() if p[1] == 1}
        failures.append(Fraction(energy(fail), B * 4**j))
    triangle = {(2 * (j - B + 1), 1): B - abs(j - B + 1) for j in range(2 * B - 1)}
    assert state == triangle
    success = Fraction(energy(state), B**3)
    assert success == Fraction(2 * B * B + 1, 3 * B * B) and sum(failures, success) == 1
    return state, failures, success


def deferred_flags(box, layers, triangle, failures, B):
    """Flags travel with the walker. New reversible 0<->j has an empty j input."""
    flags = {0: box}
    for j, (d, _) in enumerate(layers, 1):
        flags = {tag: h(stream(h(state), d)) for tag, state in flags.items()}
        switched = {}
        for tag, state in flags.items():
            for (x, c), v in state.items():
                dest = tag
                if c == -1 and tag in (0, j):
                    dest = j - tag
                switched.setdefault(dest, {})[x, c] = v
        flags = switched
    assert flags[0] == triangle
    observed = [Fraction(energy(flags.get(j, {})), B**3) for j in range(1, len(layers) + 1)]
    assert observed == failures
    assert sum(energy(state) for state in flags.values()) == B**3
    return {tag: str(Fraction(energy(state), B**3)) for tag, state in sorted(flags.items())}


def smooth_moment(state):
    # Parseval: |1-e^(2ik)|²=4 sin² k. Take a zero extension at both ends.
    assert all(c == 1 for x, c in state)
    support = {x for x, c in state}
    grad = sum(
        (state.get((x, 1), 0) - state.get((x - 2, 1), 0)) ** 2
        for x in support | {x + 2 for x in support}
    )
    return Fraction(grad, 4 * energy(state))


def finite(B):
    box, layers = tree(B)
    assert box == {(x, 1): 1 for x in range(1 - B, B, 2)} and energy(box) == B
    assert gather(box, layers) == {(0, 1): B}
    marked = dict(box)
    marked[1 - B, 1] *= -1
    gathered = gather(marked, layers)
    assert gathered.get((0, 1), 0) == B - 2 and energy(gathered) == B * B
    wrong, _ = tree(B, False)
    triangle, fails, q = triangle_filter(box, layers, B)
    flags = deferred_flags(box, layers, triangle, fails, B)
    assert smooth_moment(box) == Fraction(1, 2 * B)
    assert smooth_moment(triangle) == Fraction(3, 2 * (2 * B * B + 1))
    residual = 0.0
    alt = {p: (-1) ** ((p[0] + B - 1) // 2) * v for p, v in box.items()}
    grid = 8 * B + 1
    for i in range(grid):
        k = 2 * pi * i / grid
        s = sin(B * k) / sin(k) if i else B
        residual = max(
            residual,
            abs(spectrum(box, k) - s * s / B),
            abs(spectrum(triangle, k) - s**4 / energy(triangle)),
            abs(spectrum(alt, k) - spectrum(box, k + pi / 2)),
        )
    assert residual < 1e-9
    return {
        "B": B,
        "tree_elapsed_streams": B - 1,
        "tree_radius_sites": B - 1,
        "reverse_gather_target_probability": "1",
        "one_leaf_sign_flip_gather_probability": str(Fraction((B - 2) ** 2, B**2)),
        "no_left_endpoint_alignment_R_mass": str(
            Fraction(sum(v * v for (x, c), v in wrong.items() if c == 1), B)
        ),
        "complete_triangle_rail_R": [[x, v] for (x, c), v in sorted(triangle.items())],
        "triangle_first_failed_masses": [str(x) for x in fails],
        "single_terminal_first_failure_flag_masses_zero_means_pass": flags,
        "triangle_herald": str(q),
        "triangle_streams_and_radius": 2 * (B - 1),
        "triangle_E_sin_squared": str(smooth_moment(triangle)),
        "unresolved_permanent_route_tag_density_at_k0_over_coherent_peak": str(Fraction(1, B)),
        "box_E_sin_squared": str(smooth_moment(box)),
        "sampled_spectral_sup_residual": residual,
    }


def scaling(K, power):
    eps = 2.0 ** (-K)
    tau = eps**power
    # c=1. Take the first binary width at least sqrt(eps)/tau.
    B = 2 ** ceil((power - 0.5) * K)
    d = eps**0.25 * tau / eps
    bound = min(1.0, 2 / (pi * B * tan(d))) if d < pi / 2 else 0.0
    pos = 2 * (B - 1) * tau
    return {
        "epsilon": eps,
        "tau": tau,
        "B": B,
        "finite_data_or_formula": "formula",
        "physical_box_radius_and_duration": pos / 2,
        "physical_triangle_radius_and_duration": pos,
        "box_p_threshold": eps**0.25,
        "box_tail_probability_bound": bound,
        "triangle_p_RMS_upper": pi * eps / tau * sqrt(3 / (8 * (2 * B * B + 1))),
        "triangle_herald": str(Fraction(2 * B * B + 1, 3 * B * B)),
        "position_RMS_upper": pos,
        "older_DO_duration": 2 * round(eps / tau**2) * tau,
    }


def main():
    return {
        "finite_literal": [finite(2**s) for s in range(8)],
        "scale_formulas": [scaling(K, p) for p in (2, 3) for K in range(2, 11)],
        "source": "Field off. Initially localized R. For d=B/2,B/4,...,1 apply global H and stream d ticks. Use a site-addressed rail X on the known left endpoints of every occupied centre, including after the final stage. Centres are 4d apart, and no active endpoints collide. The inverse reuses the same sites and H with X-stream-X in positive time. Each leaf has amplitude 1/sqrt(B) on R and no retained route bit. A permanent tag makes its momentum density flat. The small B=1 control has no split or read.",
        "filter": "Starting on the positive box append independent global H, d zero-field stream steps, global H, and an R-only coherent pass report for each d. This convolves each survivor with (T^d+T^(-d))/2 without resolving the base. All first failures and the positive joint herald have squared-record probabilities. The unnormalized final coefficients are triangular divided by B^(3/2); the herald tends to 2/3. No renormalization of failed flights is implicit.",
        "deferred": "A co-moving record has labels 0 through log2(B). At stage j, L controls the permutation interchanging the virgin label 0 with j. There is no incident j branch at that stage. Subsequent unconditional streams and H leave earlier fail labels separate. A single final label read recovers every first failure or the clean triangular success. The read can be postponed through a process acting identically on each label when only the joint final data are needed.",
        "analysis": "Folded kappa=distance(k,{0,pi}) on the Brillouin circle. Uniform box has density sin²(Bk)/(B sin²k) against dk/(2pi), hence P(kappa>q)<=2*cot(q)/(pi B) for 0<q<pi/2. Positive triangular vector satisfies E sin²k=3/[2(2B²+1)] and kappa<=pi|sin k|/2. For hop distance c*tau and p=epsilon*kappa/(c*tau), choose the first dyadic B >=sqrt(epsilon)/(c*tau). Both preparations have compact physical radius and streaming duration O(sqrt(epsilon)) for fixed c. The box gives weak concentration; the triangle gives momentum RMS O(sqrt(epsilon)) at herald probability greater than 2/3. Parity makes the two identical folded momentum peaks. The box/triangle acts identically on a coherent preexisting sheet state when no operation couples to it. Preparation supplies a scalar R-rail envelope, not the subsequent prepared spinor or phase sector.",
        "assumptions": "Predetermined position-selective left-endpoint exchanges are physical control inputs. The filter also needs a synchronized global rail-only pass or equivalent coherent pointer, preserving position coherence. If local gate/report slots take O(tau) each, O(log B) such slots add o(sqrt(epsilon)) (tau log B=o(sqrt(epsilon))). Immediate broadcast of a global success outcome is not assumed; comparison/feedback to a fixed central point must be given causal time, bounded by the packet scale for parallel local wiring and an appropriate coherent detector. Fresh ancilla or route erasure must be realized without measuring the base. Preparation on a zero-field line is independently required, and this construction does not make a nonlocal sheet-register operation local.",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    directory = parser.parse_args().directory
    result = main()
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "causal_packet_source.json").write_text(
        json.dumps(result, separators=(",", ":")) + "\n", encoding="utf8"
    )
    print(
        len(result["finite_literal"]),
        "literal sizes and",
        len(result["scale_formulas"]),
        "scaling rows.",
    )
