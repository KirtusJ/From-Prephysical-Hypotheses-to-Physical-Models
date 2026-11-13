"""Fixed localized sheet, resolved reads, and terminal coarsening.

Run python -B check_sheet_coarsening.py OUTPUT_DIRECTORY. Standard library.
Squared and count columns use the same signed path enumeration. Probabilities
for an arbitrary phase-blind mixture follow by linear interpolation.
"""
import argparse
import json
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path


def words(order, ticks, sheet=0):
    result = []
    for directions in product("RL", repeat=ticks):
        x, rail, j, sign = 0, "R", sheet, 1
        trail = [(x, rail, j)]
        for out in directions:
            j = (j+x//2) % order
            if rail == out == "L":
                sign = -sign
            x = (x+(1 if out == "R" else -1)) % (4*order)
            rail = out
            trail.append((x, rail, j))
        result.append(("".join(directions), sign, trail))
    return result


def advance(state, order, inverse=False):
    """Pair each signed transition with its transpose on the full lifted basis."""
    out = defaultdict(lambda: [0,0])
    for (x, rail, j), (count, amp) in state.items():
        if inverse:
            old = (x-(1 if rail == "R" else -1)) % (4*order)
            for prev in "RL":
                dest = (old, prev, (j-old//2) % order)
                out[dest][0] += count
                out[dest][1] += -amp if prev == rail == "L" else amp
        else:
            for new in "RL":
                dest = ((x+(1 if new == "R" else -1))%(4*order), new, (j+x//2)%order)
                out[dest][0] += count
                out[dest][1] += -amp if new == rail == "L" else amp
    return dict(out)


def local_values(subset, order):
    """Raw masses for a subset ending at ONE base port.

    Independent equal-weight Fourier evaluation via character orthogonality:
    the sum of z^(s*h) over s is order if h=0 modulo order, else zero.
    """
    cells = Counter()
    amplitudes = Counter()
    for _, sign, trail in subset:
        j = trail[-1][2]
        cells[j] += 1
        amplitudes[j] += sign
    count = sum(cells.values())
    fine = sum(v*v for v in amplitudes.values())
    corr = Counter()
    for _, sign, trail in subset:
        for _, other, path in subset:
            corr[(trail[-1][2]-path[-1][2])%order] += sign*other
    assert count == len(subset) and fine == corr[0]
    return count, fine, corr


def exhaustive_local(order, ticks):
    groups = defaultdict(list)
    records = words(order, ticks)
    for rec in records:
        groups[rec[2][-1][:2]].append(rec)
    complete_count = complete_square = subsets = 0
    bad_single_character = 0
    witness = None
    for base, group in sorted(groups.items()):
        for size in range(len(group)+1):
            for subset in combinations(group,size):
                count, fine, corr = local_values(subset, order)
                subsets += 1
                # k=0 is an allowed, sign-sensitive (nonuniform) character.
                zero_character = sum(corr.values())
                if zero_character != fine:
                    bad_single_character += 1
                    if witness is None:
                        witness = dict(port=base, words=[rec[0] for rec in subset],
                                       resolved_square=fine, purely_zero_frequency=zero_character)
                if size == len(group):
                    complete_count += count
                    complete_square += fine
    denominator = 2**ticks
    assert complete_count == complete_square == denominator
    state = {(0,"R",0):(1,1)}
    for _ in range(ticks):
        state = advance(state, order)
    w = defaultdict(lambda:[0,0])
    for _, sign, trail in records:
        w[trail[-1]][0] += 1
        w[trail[-1]][1] += sign
    assert dict(w) == {key:list(value) for key,value in state.items()}
    dark = sorted(pos for pos, (c,s) in state.items() if c and not s)
    return dict(order=order, ticks=ticks, word_count=denominator, occupied_base_ports=len(groups),
                all_subsets_at_each_base_port=subsets, fully_resolved_last_ports=len(state),
                raw_total_count=complete_count, raw_total_signed_square=complete_square,
                dark_reached_ports=dark, incompatible_k0_subsets=bad_single_character,
                first_nonuniform_k0_control=witness)


def pair_constraints(order):
    # Obtain every off-diagonal difference at ONE actual base port and
    # the matched-sheet opposite-sign control from a single signed DP.
    # Store one word per signed endpoint, retaining a concrete subset witness.
    found = {(0,'R',0,1):''}
    for t in range(1,8*order+12):
        nxt = {}
        for (x, rail, j, s), word in found.items():
            for out in "RL":
                key = ((x+(1 if out=='R' else -1))%(4*order),out,(j+x//2)%order,
                       -s if rail==out=='L' else s)
                nxt.setdefault(key,word+out)
        found = nxt
        ready = [(x,rail) for x in range(t%2,4*order,2) for rail in 'RL'
                 if all((x,rail,j,s) in found for j in range(order) for s in (-1,1))]
        if ready:
            break
    assert ready
    x,rail = ready[0]
    def w(j,s):
        return found[x,rail,j,s]
    controls = []
    for j in range(1,order//2+1):
        rows = [w(0,1), w(j,1)]
        controls.append(dict(lag=j, positive_words=rows, sheets=[0,j], resolved_raw_count=2,
                             resolved_raw_square=2,
                             base_law="2+2*C(lag), after singleton normalization"))
    return dict(order=order, depth=t, pos=x, rail=rail, opposite_sign_same_sheet=[w(0,1),w(0,-1)],
                equal_sheet_raw_count=2, equal_sheet_raw_square=0, distinct_sheet_controls=controls,
                folded_weights_per_unit_square_fraction=[
                    str(Fraction(1 if s == 0 or 2*s==order else 2,order)) for s in range(order//2+1)])


def base_marginal(order):
    state={(0,'R',0):(1,1)}
    first=None
    rows=[]
    for tick in range(1,7):
        state=advance(state,order)
        ports=defaultdict(lambda:[0,0])
        for (x,rail,_),(count,amp) in state.items():
            ports[x,rail][0]+=count
            ports[x,rail][1]+=amp*amp
        if first is None and any(c!=q for c,q in ports.values()):
            first=tick
        rows.append(dict(tick=tick,denominator=2**tick,
                         port_count_and_square=[[x,rail,*pair] for (x,rail),pair in sorted(ports.items())]))
    base_five=next(row[2:] for row in rows[4]['port_count_and_square'] if row[:2]==[1,'R'])
    assert base_five==[6,0 if order==3 else 6 if order==4 else 4]
    assert first==(6 if order==4 else 5)
    if order==4:
        assert [2,'L',5,3] in rows[5]['port_count_and_square']
    return dict(order=order,first_distinguishable_base_marginal=first,horizons=rows)


def record_tag(trail, kind, tick):
    x, rail, j = trail[tick]
    return {"none": (), "position": (x,), "base_port": (x,rail), "sheet": (j,),
            "complete": (x,rail,j)}[kind]


def marked_trials(order, start_sheet):
    tracks = words(order,5,start_sheet)
    end = (1,"R",(start_sheet-1)%order)
    expected = [("LRRLR",1),("RLLRR",-1)]
    at_end = sorted((s,p) for s,p,trail in tracks if trail[-1]==end)
    assert at_end == expected
    rows = []
    for kind in ("none","position","base_port","sheet","complete"):
        for when in (1,2,3,4):
            hist = defaultdict(lambda: [0,0])
            for _,sign,trail in tracks:
                q = hist[record_tag(trail,kind,when),trail[-1]]
                q[0] += 1
                q[1] += sign
            # Independent projector propagation, including every read outcome.
            state = {(0,"R",start_sheet):(1,1)}
            for _ in range(when):
                state = advance(state,order)
            states = defaultdict(dict)
            for coord,v in state.items():
                # A one-frame trajectory is sufficient to evaluate this projector.
                states[record_tag([coord],kind,0)][coord] = v
            for _ in range(when,5):
                states = {tag:advance(v,order) for tag,v in states.items()}
            assert {(tag,pos):row for tag,v in states.items() for pos,row in v.items()} == hist
            totals = defaultdict(lambda:[0,0])
            ports = defaultdict(lambda:[0,0])
            for (tag,pos),(n,z) in hist.items():
                totals[tag][0] += n
                totals[tag][1] += z*z
                if pos==end:
                    ports[tag] = [n,z*z]
            common = [sum(v[j] for v in totals.values()) for j in range(2)]
            assert common == [32,32]
            target = [sum(v[j] for v in ports.values()) for j in range(2)]
            assert target[0] == 2 and target[1] in (0,2)
            joint = [dict(tag=tag,tag_mass=val,joint_marked_port=ports[tag])
                     for tag,val in sorted(totals.items())]
            rows.append(dict(intermediate=kind,tick=when,all_mark_numerators=target,
                             selective_records=joint, denominator=32))
    indexed = {(r['intermediate'],r['tick']):r['all_mark_numerators'] for r in rows}
    assert indexed['none',1] == indexed['position',2] == [2,0]
    assert indexed['position',1] == indexed['sheet',2] == [2,2]
    return dict(order=order, initial_sheet=start_sheet, target=end, words=at_end,
                count_and_squared_columns=True, rows=rows)


def echoed(order, forward_ticks):
    start = (0,'R',0)
    state = {start:(1,1)}
    for _ in range(forward_ticks):
        state=advance(state,order)
    predicted_count_return=sum(c*c for c,_ in state.values())
    for _ in range(forward_ticks):
        state=advance(state,order,inverse=True)
    den=4**forward_ticks
    assert state[start][0]==predicted_count_return
    assert state[start][1]**2==den and sum(s*s for c,s in state.values())==den
    assert sum(c for c,s in state.values())==den and 0 < predicted_count_return < den
    return dict(order=order, forward_ticks=forward_ticks, reverse_ticks=forward_ticks,
                return_count=str(Fraction(predicted_count_return,den)),return_signed_square="1",
                complete_return_read=[[x,d,j,c,s*s] for (x,d,j),(c,s) in sorted(state.items())],
                denominator=den)


def phase_prepared_input(order):
    # Additional source: same site/sheet, incoming amplitudes (1,±1)/sqrt(2).
    # The explicitly stipulated hidden count branch selects either initial rail
    # with probability 1/2. No such preparation is needed for the five-tick port.
    tests=[]
    for rel in (1,-1):
        state=advance({(0,'R',0):(1,1),(0,'L',0):(1,rel)},order)
        reads={d:[c,z*z] for (_,d,_),(c,z) in state.items()}
        assert reads['R']==[2,(1+rel)**2] and reads['L']==[2,(1-rel)**2]
        tests.append(dict(relative_sign=rel,count_and_square_numerators=reads,denominator=4))
    return tests


def counting_return_control(order):
    # One outgoing edge per desired last direction. Pure count cannot put
    # more than half its probability in any single resolved port after a hop.
    start=(0,'R',0)
    state={start:(1,1)}
    rows=[]
    for tick in range(1,49):
        state=advance(state,order)
        den=2**tick
        n,z=state.get(start,(0,0))
        assert max(c for c,_ in state.values())*2 <= den
        assert sum(c for c,_ in state.values())==sum(s*s for _,s in state.values())==den
        if tick%2==0:
            rows.append([tick,n,z*z,den])
    return dict(order=order,even_horizons_count_and_square_return=[row for row in rows],
                odd_return_zero_by_parity=True,all_ports_count_mass_at_most_half_through=48)


def main():
    local=[exhaustive_local(m,t) for m in (3,4,5,6,8) for t in range(7)]
    assert all(not row['dark_reached_ports'] for row in local if row['ticks']<5)
    assert all(row['dark_reached_ports'] for row in local if row['ticks']==5)
    assert all(row['incompatible_k0_subsets'] for row in local if row['ticks']>=4)
    return dict(conventions="4M base ring; floor(x/2) mod M at departure, signed Hadamard negative on L->L. Initialized (0,R,j0). Counts and squares are raw and use denominator 2^t for t ticks except where a source denominator is specified.",
                formal_scope="Equality for arbitrary common final history subsets with optional grouping of terminal sheet labels. Arbitrary word masks are mathematical events; the five-tick resolved port uses the full native walk and no word selection. Local powerset checks suffice for all unions across distinct base endpoints by terminal additivity.",
                positive_family="The normalized resolved rule is c' N+(1-c') D^2 at each lifted endpoint. Terminal marginalization gives c' N+(1-c') sum_j D_j^2. Same-sheet opposite signs force c=c'; distinct-sheet same signs force C(h)=0 for h nonzero. The folded base weights are (1-c) times the sizes of the conjugacy pairs divided by M. No assignment of weights within conjugate pairs is observable here.",
                residual_count="Every convex mixture, including pure counting of uniform direction histories, preserves continuation on all subsets and commutes with terminal coarsening. The native five-tick port separates them with P=c/16. Actual sharp extinction or an additional physical cancellation premise would select c=0. The combinatorial presence of opposite signs alone does not.",
                local_power_sets=local,
                single_port_constraints=[pair_constraints(m) for m in range(3,13)],
                sheet_blind_terminal_by_horizon=[base_marginal(m) for m in range(3,13)],
                registered_and_forgotten=[marked_trials(m,j) for m,j in ((3,0),(4,1),(5,0),(6,4),(8,0))],
                instrument_scope="Every selective row is a joint mass, including zeroes; condition by dividing the marked joint numerator by that tag's total for the chosen hypothesis. A nonselective read sums over retained orthogonal tag values. A purely terminal summation differs from adding an intermediate tag and coherently propagating afterwards.",
                extra_inverse_control=[echoed(5,n) for n in (1,2,5)],
                inverse_scope="The inverse uses the transposed shifts and coin in reverse order. Signed forward/inverse columns give deterministic return. The count circuit retains positive weight on other ports. Treating a physical reversal as equivalent to doing nothing in all record laws is additional operational input; mere forward continuation does not assert that the inverse schedule exists or is equivalent.",
                unmodified_forward_return=[counting_return_control(m) for m in (3,4,5,6)],
                recurrence_scope="For any positive horizon the fair count mass of one full port is at most one half. The c-mixture thus has return at most 1-c/2. On a finite graph powers of the unitary U^2 return arbitrarily close to identity, without a separate inverse control; no practical time bound or near-perfect measured revival is asserted by this finite census.",
                additional_signed_source_control=phase_prepared_input(5))


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output",type=Path)
    folder=parser.parse_args().output
    data=main()
    folder.mkdir(parents=True,exist_ok=True)
    (folder/"sheet_coarsening.json").write_bytes((json.dumps(data,separators=(",",":"))+"\n").encode())
    print("Checked",len(data['local_power_sets']),"power-set families and",len(data['registered_and_forgotten']),"mid-read trials.")
