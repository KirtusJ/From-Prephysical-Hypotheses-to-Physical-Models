"""Prepare the low odd plane of an ordinary eight-cycle clock.

Run python -B check_clock_feedback.py results.  All display probabilities
and first-passage statistics use exact rationals or Q(sqrt(2)).
"""

import argparse
import json
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction as F
from pathlib import Path


@dataclass(frozen=True)
class Quad:
    """Real a+b*sqrt(2)."""

    a: F = F(0)
    b: F = F(0)

    def __add__(self, other):
        return Quad(self.a + other.a, self.b + other.b)

    def __sub__(self, other):
        return Quad(self.a - other.a, self.b - other.b)

    def __mul__(self, other):
        return Quad(self.a * other.a + 2 * self.b * other.b, self.a * other.b + self.b * other.a)

    def __truediv__(self, other):
        den = other.a**2 - 2 * other.b**2
        return Quad(
            (self.a * other.a - 2 * self.b * other.b) / den, (self.b * other.a - self.a * other.b) / den
        )

    def __pow__(self, n):
        out = ONE
        for _ in range(n):
            out = out * self
        return out

    def encode(self):
        return {"a": str(self.a), "b": str(self.b), "decimal": float(self.a) + 2**0.5 * float(self.b)}


ZERO = Quad()
ONE = Quad(F(1))
HALF = Quad(F(1, 2))
ROOT_TWO = Quad(F(0), F(1))
BRIGHT = Quad(F(1, 2), F(1, 4))
DARK = ONE - BRIGHT
GAINS = (0, 4, 0, 5, 0, 1, 0, 0)
DIR = (1, -1)
ORIGIN = (1, 0, 0, 0, 0, 0, 0, 0)
DIPOLE = (1, 0, 0, 0, -1, 0, 0, 0)


def shift(vector, displacement):
    return tuple(vector[(j - displacement) % 8] for j in range(8))


def add(a, b, sign):
    return tuple(x + sign * y for x, y in zip(a, b))


def norm2(vector):
    return sum(x * x for x in vector)


def alternating_sign(vector):
    return tuple((-1) ** j * a for j, a in enumerate(vector))


def pair_mass(vector, k):
    """Squared projection on {k,8-k}, using real autocorrelation."""
    cosines = [
        ONE,
        ROOT_TWO * HALF,
        ZERO,
        ZERO - ROOT_TWO * HALF,
        ZERO - ONE,
        ZERO - ROOT_TWO * HALF,
        ZERO,
        ROOT_TWO * HALF,
    ]
    q = ZERO
    for gap in range(8):
        term = sum(vector[i] * vector[(i + gap) % 8] for i in range(8))
        q = q + cosines[(k * gap) % 8] * Quad(F(term, 4))
    return q


def physical_ports(site, direction, vector):
    """Three literal signed H/shift ticks. Integer counts omit 1/sqrt(8)."""
    state = {(site, direction, j): a for j, a in enumerate(vector) if a}
    for _ in range(3):
        new = Counter()
        for (x, c, j), a in state.items():
            for d in DIR:
                new[(x + d) % 8, d, (j + GAINS[x]) % 8] += -a if c == d == -1 else a
        state = new
    return {(x, c): tuple(state.get((x, c, j), 0) for j in range(8)) for x in range(8) for c in DIR}


def sign_equivalent(a, b):
    return a == b or a == tuple(-v for v in b)


def native_oracle():
    rows = []
    for x, h in ((0, 4), (2, 1)):
        for c in DIR:
            kernels = physical_ports(x, c, ORIGIN)
            predicted = {}
            for port, poly in kernels.items():
                terms = [(j, v) for j, v in enumerate(poly) if v]
                if not terms:
                    continue
                if len(terms) == 1:
                    kind = "null"
                else:
                    kind = "bright" if terms[0][1] == terms[1][1] else "dark"
                    assert (terms[0][0] - terms[1][0]) % 8 in (h, (-h) % 8)
                    expected = ((x + c) % 8, c) if kind == "bright" else ((x - c) % 8, -c)
                    assert port == expected
                predicted[port] = kind
                rows.append(
                    {
                        "centre": x,
                        "incoming": c,
                        "h": h,
                        "port": port,
                        "kind": kind,
                        "signed_translations": terms,
                    }
                )
            assert Counter(predicted.values()) == {"bright": 1, "dark": 1, "null": 4}
            # Verify every column, plus a coherent signed clock, on the same graph.
            for vector in [shift(ORIGIN, s) for s in range(8)] + [(2, -1, 3, 0, -4, 1, 1, -2), DIPOLE]:
                result = physical_ports(x, c, vector)
                assert sum(norm2(v) for v in result.values()) == 8 * norm2(vector)
                for port, poly in kernels.items():
                    assert result[port] == tuple(
                        sum(poly[j] * vector[(y - j) % 8] for j in range(8)) for y in range(8)
                    )
                assert all(
                    norm2(result[p]) == norm2(vector) for p, k in predicted.items() if k == "null"
                )
            if h == 4:
                for offset in range(8):
                    ports = physical_ports(x, c, shift(ORIGIN, offset))
                    for p, kind in predicted.items():
                        if kind == "null":
                            continue
                        vector = ports[p]
                        i = next(i for i, v in enumerate(vector) if v)
                        assert abs(vector[i]) == 1 and abs(vector[(i + 4) % 8]) == 1
                        if kind == "bright":
                            v = list(vector)
                            v[(i + 4) % 8] *= -1
                            vector = tuple(v)
                        assert sign_equivalent(vector, shift(DIPOLE, i))
            else:
                low = pair_mass(DIPOLE, 1)
                for p, kind in predicted.items():
                    vector = physical_ports(x, c, DIPOLE)[p]
                    expected = {"bright": BRIGHT * HALF, "dark": DARK * HALF, "null": Quad(F(1, 8))}[
                        kind
                    ]
                    assert pair_mass(vector, 1) / Quad(F(8)) == low * expected
                    assert pair_mass(alternating_sign(vector), 1) == pair_mass(vector, 3)
    return rows


def conditional_threshold(m, cap, p):
    """Q(sqrt(2)) finite random walk with two absorbing verdicts."""
    live = {0: ONE}
    plus = minus = ZERO
    for _ in range(cap):
        next_live = {}
        for tally, mass in live.items():
            for move, share in ((1, p), (-1, ONE - p)):
                k = tally + move
                v = mass * share
                if k == m:
                    plus = plus + v
                elif k == -m:
                    minus = minus + v
                else:
                    next_live[k] = next_live.get(k, ZERO) + v
        live = next_live
    pending = sum(live.values(), ZERO)
    assert plus + minus + pending == ONE
    return plus, minus, pending


def literal_tree(m, cap):
    """No Fourier sampling in the evolution. Keep every informative read sequence."""
    # Conditional on an informative native port, K=(I +/- T)/2 after
    # stripping a common sign/translation. These commute with subsequent
    # probes; a known translation changes D only by an overall sign.
    live = [(0, DIPOLE)]
    low_good = low_bad = ZERO
    good = bad = F(0)
    for t in range(1, cap + 1):
        next_live = []
        den = 2 * 4**t
        for tally, v in live:
            for direction in DIR:
                w = add(v, shift(v, 1), direction)
                new_tally = tally + direction
                if abs(new_tally) < m:
                    next_live.append((new_tally, w))
                elif new_tally == m:
                    good += F(norm2(w), den)
                    low_good = low_good + pair_mass(w, 1) / Quad(F(den))
                else:
                    bad += F(norm2(w), den)
                    corrected = alternating_sign(w)
                    low_bad = low_bad + pair_mass(corrected, 1) / Quad(F(den))
        live = next_live
    pending = F(sum(norm2(v) for _, v in live), 2 * 4**cap)
    assert good + bad + pending == 1
    return good, bad, pending, low_good, low_bad


def threshold_results():
    rows = []
    for m, cap in ((1, 3), (2, 8), (3, 10), (4, 12), (6, 30), (8, 48)):
        lo = conditional_threshold(m, cap, BRIGHT)
        hi = conditional_threshold(m, cap, DARK)
        assert lo[0] == hi[1] and lo[1] == hi[0] and lo[2] == hi[2]
        stop = ONE - lo[2]
        # Given the stopped tally, every compatible prefix has the same
        # likelihood ratio (p/(1-p))^m. Symmetry cancels the irrational tails.
        eps = ONE / (ONE + (BRIGHT / DARK) ** m)
        assert lo[1] == eps * stop and lo[2].b == 0
        literal = cap <= 12
        if literal:
            good, bad, pending, low_good, low_bad = literal_tree(m, cap)
            assert good == bad == stop.a / 2 and pending == lo[2].a
            assert low_good == low_bad == lo[0] * HALF
        expected = ROOT_TWO * Quad(F(m)) * (ONE - eps * Quad(F(2)))
        rows.append(
            {
                "threshold": m,
                "informative_cap": cap,
                "literal_sheet_tree_checked": literal,
                "low_posterior_error_each_stopped_branch": eps.encode(),
                "mean_informative_reads_uncapped": expected.encode(),
                "mean_native_three_tick_attempts_uncapped": (expected * Quad(F(2))).encode(),
                "finite_joint": {
                    "stop_low_verdict": (stop * HALF).encode(),
                    "stop_high_verdict": (stop * HALF).encode(),
                    "timeout": lo[2].encode(),
                    "corrected_low": lo[0].encode(),
                    "corrected_high": lo[1].encode(),
                },
                "reset_only_complete_attempt_accept_any_low_verdict_after_odd_parity": (
                    stop * Quad(F(1, 4))
                ).encode(),
                "reset_only_accept_by_four_capped_rounds": str(1 - (1 - stop.a / 4) ** 4),
            }
        )
    return rows


def clock_deadline(threshold, tick_cap, oracle):
    """Exact fixed elapsed-time law. Three-tick blocks are never read early."""
    ports = {
        (s, c): [
            (r["kind"], tuple(r["port"])) for r in oracle if r["centre"] == s and r["incoming"] == c
        ]
        for s in (0, 2)
        for c in DIR
    }
    verdicts = {}
    null = Quad(F(1, 8))
    for initial, bright in (("low", BRIGHT), ("high", DARK)):
        # The hidden-plane coin is independent of the parity outcomes after
        # sign repair. Thus it can equivalently be drawn before the first tick.
        layers = [{} for _ in range(tick_cap + 1)]
        layers[0][(0, 0, 1, 0)] = ONE
        absorbed = {1: ZERO, -1: ZERO}
        for tick, layer in enumerate(layers):
            for (centre, x, c, votes), weight in layer.items():
                if x != centre:
                    moves = [(1, (x + d) % 8, d, centre, votes, HALF) for d in DIR]
                else:
                    moves = []
                    for kind, (u, d) in ports[centre, c]:
                        if kind == "null":
                            moves.append((3, u, d, centre, votes, null))
                        elif centre == 0:
                            moves.append((3, u, d, 2, 0, Quad(F(1, 4))))
                        else:
                            up = kind == "bright"
                            moves.append(
                                (
                                    3,
                                    u,
                                    d,
                                    2,
                                    votes + (1 if up else -1),
                                    HALF * (bright if up else ONE - bright),
                                )
                            )
                for dt, u, d, s, v, p in moves:
                    arrival = tick + dt
                    if arrival > tick_cap:
                        continue
                    branch_mass = weight * p
                    if abs(v) == threshold:
                        sign = 1 if v > 0 else -1
                        absorbed[sign] = absorbed[sign] + branch_mass
                    else:
                        key = (s, u, d, v)
                        layers[arrival][key] = layers[arrival].get(key, ZERO) + branch_mass
        verdicts[initial] = absorbed
    first, second = verdicts["low"], verdicts["high"]
    plus = HALF * (first[1] + second[1])
    minus = HALF * (first[-1] + second[-1])
    right = HALF * (first[1] + second[-1])
    wrong = HALF * (first[-1] + second[1])
    timeout = ONE - plus - minus
    eps = ONE / (ONE + (BRIGHT / DARK) ** threshold)
    assert right + wrong + timeout == ONE and wrong == eps * (plus + minus)
    assert all(q.b == 0 for q in (plus, minus, timeout))
    return {
        "threshold": threshold,
        "hard_total_walk_ticks": tick_cap,
        "initial_base": [0, 1],
        "stop_low_verdict": plus.encode(),
        "stop_high_verdict": minus.encode(),
        "pending": timeout.encode(),
        "corrected_low_and_stopped": right.encode(),
        "corrected_high_and_stopped": wrong.encode(),
        "convention": "A probe that cannot complete by this integer tick is pending. All measured "
        "routing hops, parity, probe nulls, both classifications and each three-tick "
        "block are counted. Auxiliary sign masks are instantaneous controls in this model.",
    }


def main():
    oracle = native_oracle()
    threshold = threshold_results()
    assert pair_mass(ORIGIN, 1) == Quad(F(1, 4))
    assert pair_mass(DIPOLE, 1) == pair_mass(DIPOLE, 3) == ONE
    # A resolved cell at the end of any rejected trial resets the spectrum,
    # even if that rejected amplitude had already been nearly all high.
    rejected = DIPOLE
    for _ in range(4):
        rejected = add(rejected, shift(rejected, 1), -1)
    resolved = [F(a * a, norm2(rejected)) for a in rejected]
    assert sum(resolved) == 1
    assert all(pair_mass(shift(ORIGIN, j), 1) == Quad(F(1, 4)) for j in range(8))
    # The reindexing j -> 3j exchanges low and high as D does on odd k;
    # it is not a translate of the physical clock and not a cycle isometry.
    permutation = [(3 * j) % 8 for j in range(8)]
    assert not any(permutation == [(j + s) % 8 for j in range(8)] for s in range(8))
    # Bound the fully clocked finite protocol with no discarded outcomes.
    # Every horizon below counts all stages; the looser physical-clock bound
    # includes all measured hops to each comparison centre.
    m, cap, B, R = 4, 12, 16, 256
    per_stage = F(1, 2) ** B
    # Exact worst probability to miss a fixed site in R routed hops.
    misses = [0] + [1] * 7
    for _ in range(R):
        misses = [0] + [misses[(j - 1) % 8] + misses[(j + 1) % 8] for j in range(1, 8)]
    routing_bound = F(max(misses), 2**R)
    attempts = (1 + cap) * B
    informative_deadline_failure = (1 + cap) * per_stage
    routing_deadline_failure = attempts * routing_bound
    timeout = conditional_threshold(m, cap, BRIGHT)[2].a
    conservative_fail = min(F(1), timeout + informative_deadline_failure + routing_deadline_failure)
    return {
        "clock": "Ordinary clock T|j>=|j+1 mod 8>, with T^8=I. All clocks below are integer walk ticks. "
        "The bank is not the minus-twisted T^8=-I clock.",
        "fixed_native_graph": {
            "sites": 8,
            "clock_size": 8,
            "departure_shifts": GAINS,
            "oracle": oracle,
            "basis_and_coherent_checks": "Both incoming directions at both centres, eight clock basis "
            "columns, an odd dipole and one fully signed unequal vector.",
        },
        "protocol": "At centre 0 take complete three-tick port reads until informative (difference 4). "
        "Four nulls have probability 1/8 each and only translate. For a localized launch the "
        "bright/even and dark/odd informative outcomes have equal chances. Flip the sign of "
        "one tracked occupied clock cell on the even branch. Both now have the same odd dipole "
        "up to sign/translation. Route to centre 2; on each informative difference-1 probe, "
        "add +1 for bright and -1 for dark, retrying all nulls. At +m stop; at -m apply "
        "D|j>=(-1)^j|j> then stop. Route to each requested centre after previous probes by "
        "reading every single base hop; these act by a known translation and sign. All "
        "four null outcomes, verdict signs, and deadlines are counted. Coherences and "
        "orientation inside conjugate pairs are not claimed to be standardized.",
        "algebra": "Low k={1,7}; high={3,5}. In the odd sector an informative bright probability is "
        "(2+sqrt(2))/4 or its complement. The untouched sector is a sampling representation. "
        "Each stopped branch has the same residual high weight epsilon, and each verdict "
        "has marginal probability 1/2 in the symmetric initial odd ensemble. In JSON a,b "
        "encode a+b sqrt(2). A finite cap records the surviving mass jointly.",
        "threshold_trials": threshold,
        "resolved_cell_restart_control": {
            "input": "odd dipole following four consecutive informative dark outcomes",
            "signed_clock_integers": rejected,
            "high_weight_before_coordinate_read": (
                pair_mass(rejected, 3) / Quad(F(norm2(rejected)))
            ).encode(),
            "coordinate_read_probabilities": [str(p) for p in resolved],
            "low_weight_after_each_occupied_resolved_cell": "1/4",
            "relative_state_each_new_parity_probe": "Localized at its actual read coordinate; measuring "
            "the clock is essential for the reset-only procedure.",
        },
        "exact_elapsed_clock_trials": [
            clock_deadline(2, deadline, oracle) for deadline in (12, 36, 72, 120)
        ],
        "never_stop_or_dark_record_controls": {
            "initial_low_mass": "1/4",
            "odd_dipole_low_mass": "1/2",
            "no_high_correction_low_mass_given_any_stop": "1/2",
            "translation_only_target_success_bound": "From a localized clock and no clock read, "
            "repreparation, or symmetry-breaking mixing, sum of target weights over any "
            "stopped prefixes is at most 1/4. If accepted purity is >=1-eps, success "
            "is at most (1/4)/(1-eps). Character-preserving controls commute with the projector.",
            "reset_only": "At even parity or high verdict read the actual clock coordinate and repeat "
            "from that physical coordinate. Every basis clock is Fourier-uniform; no translation "
            "back to the origin is needed for these weights. Without caps a complete round succeeds "
            "with probability 1/4; first at round r has mass (3/4)^(r-1)/4, full eventual "
            "yield, mean four rounds. In a capped informative tree p=Pr(stop)/4 and (1-p)^r "
            "survive r whole attempts if timeouts also reset. The returned low weight is 1-eps.",
            "parity_only_retry": "Without the sparse sign, coordinate-read and retry the even half. "
            "After r uncapped parity trials fail with probability 2^-r.",
            "finite_exact_purity": "On every finite homogeneous-clock branch a localized input gives "
            "integer coefficients times one common scalar. If the clock polynomial vanishes at "
            "a primitive eighth root for k=3 it is divisible over Q by X^4+1, also killing k=1. "
            "Apply to each unresolved base component. A finite or almost-sure finite stopping "
            "record cannot prepare a nonzero exactly pure low state. The epsilon limit costs time.",
        },
        "resources": {
            "parity_sign": "One sign inversion of either occupied j or j+4, selected using the "
            "known translation offset (or a fixed address plus translation control).",
            "high_to_low_sign": "Flip the signs on sites 1,3,5,7. This is an actual clock-position "
            "operation. It cannot arise from translations alone since D T = -T D.",
            "permutation_alternative": permutation,
            "physical_reindexing": "j->3j conjugates T to T^3. "
            "This is an extra wire permutation, not a power of a locked T. The fixed-gain graph "
            "above keeps its drive unchanged; a resolved clock-coordinate read plus restarts "
            "also works without either sign or a drive rewire.",
            "routing": "For any routed hop the measured base direction is fair. A specified site "
            "has mean hitting time j(8-j)<=16; in any four hops the chance to have hit it is at "
            "least 1/16. These ticks and the three-tick native blocks are separate from the "
            "informative-sample count. Clock sign operations, read electronics and reset costs "
            "are not assigned a fabricated duration.",
        },
        "finite_physical_deadline_example": {
            "threshold": m,
            "maximum_informative_samples": cap,
            "native_attempts_per_informative_read": B,
            "maximum_routing_hops_per_visit": R,
            "maximum_walk_ticks_including_parity": attempts * (R + 3),
            "threshold_timeout": str(timeout),
            "bound_on_any_null_deadline": str(informative_deadline_failure),
            "bound_on_any_routing_deadline": float(routing_deadline_failure),
            "total_timeout_union_upper": float(conservative_fail),
            "scope": "Union bounds; successful physical deadlines may select different path "
            "lengths, but routing factors and nulls are sector-independent conditional "
            "on informative signs. Posterior bounds hold for each successful transcript.",
        },
        "flight_scope": "A sheet-blind sector-preserving flight compares with its own normalized projected "
        "low state (or oriented-launch laws known to coincide) with TV <= epsilon. For the uniform "
        "g(x)=x field on an even ring, changing k by 4 adds pi to the field and gives identical "
        "position/coin counts by the spatial parity gauge. An eight-clock example is finite; "
        "no classical limiting scaling or oriented complex-state preparation follows.",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()
    result = main()
    args.directory.mkdir(parents=True, exist_ok=True)
    (args.directory / "clock_feedback.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf8"
    )
    print(
        "Verified",
        len(result["fixed_native_graph"]["oracle"]),
        "nonzero native kernels and",
        len(result["threshold_trials"]),
        "stopping trials.",
    )
