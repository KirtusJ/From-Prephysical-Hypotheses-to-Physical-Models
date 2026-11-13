"""Finite physical-site courier for a two-body departure gain. All path counts are exact.

Run python -B check_local_mediator.py results. The ring alphabet per site is blank
or a token carrying one counter value. The prepared ancilla is the vacuum.
"""

import argparse
import json
from hashlib import sha256
from itertools import product
from math import comb, exp, pi, sin
from pathlib import Path

from check_cycle_interaction import count_table


EMPTY = -1
DIRECTIONS = (1, -1)


def emitter(register, b):
    """On B's occupied site, swap blank and token(0); fix every nonzero token."""
    out = list(register)
    if out[b] == EMPTY:
        out[b] = 0
    elif out[b] == 0:
        out[b] = EMPTY
    return tuple(out)


def local_round(y, register, a, gains, order, direction=1, increment=True):
    """A reads only its own physical site. Then every cell streams to its neighbour."""
    n = len(register)
    z = register[a]
    if z != EMPTY:
        y = (y+gains[z]) % order
    out = [EMPTY]*n
    for site, token in enumerate(register):
        if token != EMPTY:
            out[(site+direction) % n] = (token+int(increment)) % n
    return y, tuple(out)


def mediate(a, b, y, register, gains, order, rounds=None, direction=1, increment=True):
    n = len(register)
    register = emitter(register, b)
    for _ in range(n if rounds is None else rounds):
        y, register = local_round(y, register, a, gains, order, direction, increment)
    return y, emitter(register, b)


def counts(size, depth):
    """Independent integer binomial expansion of the cyclic two-stay recurrence."""
    row = [0]*size
    for j in range(2*depth+1):
        row[(j-depth) % size] += comb(2*depth, j)
    return row


def profiles(n):
    oriented = [2*t*t+3*t-1 for t in range(n)]
    cases = [("oriented_polynomial", oriented), ("zero", [0]*n)]
    extra = None
    if n % 2 == 0:
        depth, scale = n*n, 7
        integer_counts = count_table(n, depth)
        binomial = counts(n, depth)
        assert integer_counts == binomial
        top = integer_counts[0]-integer_counts[n//2]
        gains = [(4*scale*(integer_counts[0]-v)+top)//(2*top) for v in integer_counts]
        cases.append(("symmetric_cycle_counts", gains))
        extra = dict(depth=depth, scale=scale, counts=integer_counts, normalization=top,
                     binomial_recurrence_exact=True, sum_equals_four_to_depth=sum(integer_counts)==4**depth)
    return cases, extra


def accumulate(dest, cell, value):
    dest[cell] = dest.get(cell, 0)+value


def prune(state):
    return {key: v for key, v in state.items() if v}


def ideal_step(state, n, order, gains):
    """Direct signed coordinate oracle: all four two-coin paths at every departure."""
    output = {}
    for (a, b, ca, cb, y), amplitude in state.items():
        shifted = (y+gains[(a-b) % n]) % order
        for da, db in product(DIRECTIONS, repeat=2):
            sign = (-1)**(int(ca == da == -1)+int(cb == db == -1))
            cell = ((a+da) % n, (b+db) % n, da, db, shifted)
            accumulate(output, cell, sign*amplitude)
    return prune(output)


def courier_step(state, gains, order):
    """Independent two-stage coin scatter, followed by both spatial shifts."""
    moved = {}
    for (a, b, ca, cb, y, register), amplitude in state.items():
        shifted, outgoing = mediate(a, b, y, register, gains, order)
        for da in DIRECTIONS:
            sign = -1 if da == ca == -1 else 1
            accumulate(moved, (a, b, da, cb, shifted, outgoing), sign*amplitude)
    output = {}
    n = len(gains)
    for (a, b, da, cb, y, register), amplitude in moved.items():
        for db in DIRECTIONS:
            sign = -1 if db == cb == -1 else 1
            accumulate(output, ((a+da) % n, (b+db) % n, da, db, y, register), sign*amplitude)
    return prune(output)


def coherent_state(n, order, signed_dense):
    if not signed_dense:
        return {(0, n//2, 1, -1, 0): 1}
    state = {}
    for a,b,ca,cb,y in product(range(n),range(n),DIRECTIONS,DIRECTIONS,range(order)):
        value = (11*a + 3*b + 5*(ca == -1) + 2*(cb == -1) + 7*y) % 13 - 6
        if value:
            state[(a,b,ca,cb,y)] = value
    return state


def path_digest(state):
    return sha256(json.dumps(sorted(state.items()),separators=(",", ":")).encode("ascii")).hexdigest()


def compare_walks(n, order, gains, signed_dense):
    direct = coherent_state(n, order, signed_dense)
    initial_mass = sum(a*a for a in direct.values())
    vacuum = (EMPTY,)*n
    physical = {(*key, vacuum): v for key, v in direct.items()}
    trials = []
    for macrostep in range(1, 4):
        direct = ideal_step(direct, n, order, gains)
        physical = courier_step(physical, gains, order)
        residual = sum(v*v for key, v in physical.items() if key[-1] != vacuum)
        decoded = {key[:-1]:v for key,v in physical.items() if key[-1] == vacuum}
        union = set(direct)|set(decoded)
        error = max(abs(direct.get(k,0)-decoded.get(k,0)) for k in union)
        mass = sum(v*v for v in physical.values())
        trials.append(dict(macrostep=macrostep, occupied_joint_outputs=len(decoded),
                           maximum_signed_count_error=error, nonvacuum_squared_count=residual,
                           signed_coordinate_sha256=path_digest(decoded), squared_count=mass,
                           norm_exact=(mass == initial_mass*4**macrostep)))
    return dict(input="dense signed integer counts" if signed_dense else "one localized site pair and sheet",
                initial_squared_count=initial_mass, trials=trials)


def finite_case(n, order):
    vacuum = (EMPTY,)*n
    cases, arithmetic = profiles(n)
    records = []
    for name,gains in cases:
        checked = 0
        differences = []
        walk_columns = 0
        walk_failures = []
        for a,b,y in product(range(n),range(n),range(order)):
            actual = mediate(a, b, y, vacuum, gains, order)
            expected = ((y+gains[(a-b) % n]) % order, vacuum)
            if actual != expected:
                differences.append([a,b,y])
            checked += 1
            for ca,cb in product(DIRECTIONS, repeat=2):
                key = (a,b,ca,cb,y)
                direct = ideal_step({key: 1}, n, order, gains)
                lifted = {(*out,vacuum): value for out,value in direct.items()}
                physical = courier_step({(*key,vacuum): 1}, gains, order)
                if physical != lifted:
                    walk_failures.append(key)
                walk_columns += 1
        walks = [compare_walks(n, order, gains, dense) for dense in (False, True)]
        records.append(dict(profile=name, gains=gains, basis_site_sheet_inputs=checked,
                            basis_failures=differences, full_walk_basis_columns=walk_columns,
                            full_walk_basis_failures=walk_failures,
                            walk_tests=walks))
    return dict(N=n, M=order, cases=records, count_construction=arithmetic)


def inverse_round(y, register, a, gains, order):
    n = len(register)
    previous = tuple(EMPTY if off == EMPTY else (off-1) % n for off in register[1:]+register[:1])
    token = previous[a]
    return (y-(0 if token == EMPTY else gains[token])) % order, previous


def whole_space_test():
    n, order = 3, 5
    gains = [1, -2, 4]
    round_columns = full_columns = 0
    e_ok = r_ok = f_ok = True
    for a,b in product(range(n), repeat=2):
        images = set()
        for register in product(range(EMPTY,n), repeat=n):
            e_ok &= emitter(emitter(register,b),b) == register
            for y in range(order):
                after = local_round(y, register, a, gains, order)
                r_ok &= inverse_round(*after, a, gains, order) == (y, register)
                round_columns += 1
                images.add(mediate(a, b, y, register, gains, order))
                full_columns += 1
        f_ok &= len(images) == order*(n+1)**n
    return dict(N=n, M=order, register_states_per_position_pair=(n+1)**n,
                round_columns=round_columns, circuit_columns=full_columns,
                emitter_involution=e_ok, round_inverse=r_ok, circuit_injective=f_ok)


def adverse_controls():
    n, order = 5, 11
    g = [2*j*j+3*j-1 for j in range(n)]
    even = [min(j,n-j)**2 for j in range(n)]
    vacuum = (EMPTY,)*n
    reports=[]
    for label,gains,options in [("wrong_orientation",g,dict(direction=-1)),
                                ("wrong_orientation_symmetric_table",even,dict(direction=-1)),
                                ("omitted_final_round",g,dict(rounds=n-1)),
                                ("counter_stuck_at_zero",g,dict(increment=False))]:
        wrong_gain = nonvac = 0
        example = None
        for a,b in product(range(n), repeat=2):
            actual, register = mediate(a,b,0,vacuum,gains,order,**options)
            expected = gains[(a-b) % n] % order
            wrong_gain += actual != expected
            nonvac += register != vacuum
            if example is None and (actual != expected or register != vacuum):
                example = dict(A=a,B=b,actual_sheet=actual,expected_sheet=expected,ancilla=list(register))
        reports.append(dict(case=label, trials=n*n, wrong_sheet=wrong_gain, nonvacuum=nonvac, first_mismatch=example))
    busy=[]
    for label,reg in [("zero_token_at_emitter",(0,EMPTY,EMPTY,EMPTY,EMPTY)),
                      ("nonzero_token_at_emitter",(2,EMPTY,EMPTY,EMPTY,EMPTY)),
                      ("one_token_away_from_emitter",(EMPTY,3,EMPTY,EMPTY,EMPTY))]:
        bad=0
        examples=[]
        for a in range(n):
            y,out=mediate(a,0,0,reg,g,order)
            error=(y != g[a]%order)
            bad+=error
            examples.append(dict(A=a,sheet=y,expected_clean_gain=g[a]%order,ancilla_restored=(out==reg)))
        busy.append(dict(case=label,register=list(reg),wrong_sheet=bad,cases=examples))
    # Blindly resetting the symbol, even at B, merges two orthogonal tag states.
    forced_erase=lambda _tag: EMPTY
    return dict(wrong_schedules=reports,busy_inputs=busy,
                forced_erase_counterexample=dict(distinct_tags=[0,1],same_output=forced_erase(0)==forced_erase(1)))


def causal_control():
    n, order = 8, 11
    a = n//2
    vacuum = (EMPTY,)*n
    gains = [k+1 for k in range(n)]
    traces=[]
    # Compare B at 0 and B at 7. The global start difference is confined to those sites.
    # Relative to A=4 their minimal ring distances are 4 and 3. Moving right,
    # however, their directed distances are 4 and 5, respectively.
    for b in (0,7):
        register=emitter(vacuum,b)
        y=0
        trace=[]
        for t in range(n):
            sites=[j for j,u in enumerate(register) if u!=EMPTY]
            trace.append(dict(t=t, token_site=sites[0], counter=register[sites[0]], y_before_collision=y))
            y, register=local_round(y, register, a, gains, order)
            trace[-1]["y_after_collision"]=y
        traces.append(dict(B=b,A=a,rounds=trace))
    first=next(t for t in range(n) if traces[0]["rounds"][t]["y_after_collision"] !=
               traces[1]["rounds"][t]["y_after_collision"])
    return dict(N=n, M=order, tests=traces, first_local_sheet_difference_round=first,
                distance_to_input_difference=min(4,3), direct_oracle_sheet_outputs_at_t0=[gains[4],gains[5]],
                nearest_neighbour_streaming=all(r["token_site"]==(case["B"]+r["t"])%n and
                                               r["counter"]==r["t"] for case in traces for r in case["rounds"]),
                no_precone_signal=first>=3)


def pair_flow(a, b, va, vb, kappa, elapsed, steps):
    """Velocity Verlet on the lifted physical coordinates, with equal masses."""
    dt = elapsed / steps
    for _ in range(steps):
        half_impulse = -0.5 * dt * kappa * sin(a - b)
        va += half_impulse
        vb -= half_impulse
        a += dt * va
        b += dt * vb
        half_impulse = -0.5 * dt * kappa * sin(a - b)
        va += half_impulse
        vb -= half_impulse
    return a, b, va, vb


def moving_packets():
    # Compact phase-space inputs. All sixteen sign combinations have mass 1/16.
    width = 1 / 1024
    lower, upper = 1 / 64, 17 / 32
    times = (0.25, 0.5, 1.0)
    coarse, fine = 256, 1024
    nearest_sender = pi / 2 - width - upper
    controls = [
        ("attractive", 1, 1, (pi / 2, pi)),
        ("zero_force", 0, 1, (pi / 2, pi)),
        ("opposite_force", -1, 1, (pi / 2, pi)),
        ("time_reversed", 1, -1, (pi / 2, pi)),
        ("same_sender", 1, 1, (pi / 2, pi / 2)),
        ("initial_read", 1, 0, (pi / 2, pi)),
    ]
    rows = []
    for label, kappa, time_direction, senders in controls:
        for duration in (times[:1] if time_direction == 0 else times):
            elapsed = time_direction * duration
            sources = []
            for center in senders:
                center_a = pair_flow(0, center, 0, 0, kappa, elapsed, fine)[0]
                a_values = []
                refinement_error = 0.0
                for offsets in product((-width, width), repeat=4):
                    a, db, va, vb = offsets
                    initial = (a, center + db, va, vb)
                    low = pair_flow(*initial, kappa, elapsed, coarse)
                    high = pair_flow(*initial, kappa, elapsed, fine)
                    refinement_error = max(refinement_error, *(abs(x-y) for x,y in zip(low,high)))
                    a_values.append(high[0])
                # In the four-component sup norm the vector field is 2-Lipschitz
                # for |kappa|<=1. Width*exp(2|t|) encloses all input perturbations.
                drift = width * exp(2 * abs(elapsed))
                if kappa == 0 or center == pi:
                    lo = hi = 0.0
                else:
                    # |r(t)-r(0)|<=t^2, so |q_A''(t)-kappa|<=t^2.
                    # Double integration gives t^4/12; also |q_A(t)|<=t^2/2.
                    leading = elapsed**2 / 2
                    lo, hi = leading - elapsed**4 / 12, leading
                    if kappa < 0:
                        lo, hi = -hi, -lo
                lo -= drift
                hi += drift
                inside = lower < lo and hi < upper
                outside = hi < lower or upper < lo
                # All these intervals stay within (-pi,pi), so the fixed bin
                # has just one relevant lift on the circle.
                sharp_mass = 1 if inside else 0 if outside else None
                mass = sum(lower < v < upper for v in a_values) / len(a_values)
                sources.append(dict(B_center=center, A_center=center_a, sample_count=len(a_values),
                                    A_sample_range=[min(a_values),max(a_values)], A_analytic_enclosure=[lo,hi],
                                    bin_probability=mass, bin_probability_analytic=sharp_mass,
                                    coarse_fine_state_sup_difference=refinement_error))
            probabilities = [s["bin_probability"] for s in sources]
            rows.append(dict(case=label, elapsed=elapsed, speed_one_radius=abs(elapsed),
                             gap_beyond_backward_cone=nearest_sender-abs(elapsed), sources=sources,
                             binary_read_total_variation=abs(probabilities[0]-probabilities[1])))
    groups = {label:[r for r in rows if r["case"]==label] for label,*_ in controls}
    checks = dict(
        attraction_separates=all(r["binary_read_total_variation"]==1 for r in groups["attractive"]),
        null_and_opposite_controls=all(r["binary_read_total_variation"]==0 for key in
                                       ("zero_force","opposite_force","same_sender","initial_read") for r in groups[key]),
        time_reversal_preserves_position_separation=all(
            r["binary_read_total_variation"]==1 and all(
                abs(s["A_center"]-t["A_center"]) < 1e-13 for s,t in zip(r["sources"],f["sources"]))
            for r,f in zip(groups["time_reversed"],groups["attractive"])),
        sampled_enclosures_and_probabilities=all(
            s["A_analytic_enclosure"][0] <= s["A_sample_range"][0] <= s["A_sample_range"][1] <= s["A_analytic_enclosure"][1]
            and s["bin_probability"] == s["bin_probability_analytic"] for r in rows for s in r["sources"]),
        refinements_agree=all(s["coarse_fine_state_sup_difference"]<2e-5 for r in rows for s in r["sources"]),
        sender_support_outside_read_cone=all(r["gap_beyond_backward_cone"]>0 for r in rows))
    return dict(checks=checks, trials=rows, packet_half_width=width, fixed_A_read_bin=[lower,upper],
                min_distance_read_bin_to_changed_sender_support=nearest_sender,
                speed_assumption=1, coarse_and_fine_steps=[coarse,fine],
                witness="A, B move with unit masses and opposite forces, relative acceleration -2 kappa sin(A-B). "
                        "Each compact classical ensemble assigns equal normalized mass to the endpoints of four "
                        "independent initial position and velocity intervals. The analytic enclosures cover their "
                        "entire Cartesian product. The binary read has total variation one at positive coupling. "
                        "A common local prediction for its two probabilities then has worst-case error at least 1/2.",
                clock="Elapsed time is the signed classical flow parameter. A hypothetical local process with physical "
                      "speed v has backward radius v*abs(elapsed). Distances are physical torus lengths. No "
                      "identification with the parked courier's N rounds or a microscopic tick duration is assumed.",
                scope="Point trajectories and finite classical ensembles. Quantum packet propagation and finite "
                      "walk approximation are separate questions.")


def main(output):
    output.mkdir(parents=True, exist_ok=True)
    cases=[finite_case(n,m) for n,m in ((3,5),(4,7),(5,11),(6,7))]
    whole=whole_space_test()
    adverse=adverse_controls()
    lightcone=causal_control()
    profiles=[entry for case in cases for entry in case["cases"]]
    trajectories=[trial for entry in profiles for walk in entry["walk_tests"] for trial in walk["trials"]]
    negative={r["case"]:r for r in adverse["wrong_schedules"]}
    checks=dict(exact_basis_gain_and_reset=all(not r["basis_failures"] for r in profiles),
                full_walk_on_every_basis_input=all(r["full_walk_basis_columns"]==4*r["basis_site_sheet_inputs"]
                                                    and not r["full_walk_basis_failures"] for r in profiles),
                signed_counts_all_macrosteps=all(r["maximum_signed_count_error"]==r["nonvacuum_squared_count"]==0
                                                 and r["norm_exact"] for r in trajectories),
                count_profile_arithmetic=all(c["count_construction"]["sum_equals_four_to_depth"] for c in cases
                                             if c["count_construction"] is not None),
                complete_register_permutation=all(whole[k] for k in ("emitter_involution","round_inverse","circuit_injective")),
                orientation_witness=negative["wrong_orientation"]["wrong_sheet"]>0 and
                                    negative["wrong_orientation_symmetric_table"]["wrong_sheet"]==0,
                short_route_leaves_token=negative["omitted_final_round"]["nonvacuum"]==25,
                stalled_counter_changes_gain=negative["counter_stuck_at_zero"]["wrong_sheet"]>0,
                busy_workspace_changes_target=all(case["wrong_sheet"]>0 for case in adverse["busy_inputs"]),
                forced_erase_noninjective=adverse["forced_erase_counterexample"]["same_output"],
                lightcone_control=lightcone["no_precone_signal"] and lightcone["nearest_neighbour_streaming"])
    result=dict(checks=checks, finite_rings=cases, full_register_test=whole, adverse_controls=adverse,
                causal_witness=lightcone,
                conventions="Blanks carry -1; token counters are 0..N-1. A carries the cyclic sheet and B controls "
                            "the local blank/zero-token swap. The two walkers stay at their recorded or coherently "
                            "superposed sites during the circuit. Moving A then carries its sheet with it.",
                scope="Integer coherent signed counts and a reversible physical-site token register; no observation "
                      "of courier position or stored counter. One nearest-neighbour move per round, plus local "
                      "emission and absorption. A programmable cyclic counter, message alphabet, idle controls "
                      "and gain table per ring are supplied. This checks macro-operation equivalence without "
                      "identifying physical durations or supplying a uniform gate alphabet.")
    result["moving_packets"] = moving_packets()
    dest=output/"local_mediator.json"
    dest.write_text(json.dumps(result,indent=2,allow_nan=False)+"\n",encoding="utf8")
    print(checks,len(profiles),"gain profiles;",len(trajectories),"coherent signed walk comparisons")
    if not all(checks.values()) or not all(result["moving_packets"]["checks"].values()):
        raise SystemExit(1)


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("output",type=Path)
    main(parser.parse_args().output)
