"""Finite incident accounting for a partially monitored strict prefix reference."""
import argparse
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path

from check_compact_bin_reflections import flight


def require(test, message):
    if not test:
        raise ValueError(message)


def threshold_fraction(bits):
    return F(int(bits or "0", 2), 1 << len(bits))


def complete_bounds(bits, stages, tolerance):
    """Sharp probability bounds from conditional continuation bands on reached incidents."""
    require(0 <= stages <= len(bits) and 0 <= tolerance <= F(1, 2), "bad horizon or tolerance")
    low, high = F(0), F(int("1" in bits[stages:]))
    left, right = F(1, 2)-tolerance, F(1, 2)+tolerance
    for bit in reversed(bits[:stages]):
        if bit == "0":
            low, high = left*low, right*high
        else:
            low, high = 1-right*(1-low), 1-left*(1-high)
    return low, high


def path_rate(bits, continuations, tail):
    live, hits = F(1), F(0)
    for digit, cont in zip(bits, continuations):
        hits += int(digit)*live*(1-cont)
        live *= cont
    return hits + live*tail


def square_response(p):
    return p*p/(p*p+(1-p)**2)


def audit_incidents(bits, incidents, records):
    """One entry per reached stage: certain stops, further continuations, first unread exits."""
    require(incidents > 0 and 0 <= len(records) <= len(bits), "bad incident table")
    live = incidents
    hits = residual = imputed = possible_unread_hits = lost = 0
    for k, (stop, cont, unread) in enumerate(records):
        require(all(type(x) is int and x >= 0 for x in (stop, cont, unread)) and
                stop + cont + unread == live, "incident conservation")
        digit = int(bits[k])
        parent, suffix = threshold_fraction(bits[k:]), threshold_fraction(bits[k+1:])
        hits += digit * stop
        residual += (cont-F(live-unread, 2))*(suffix-digit)
        imputed += unread*parent
        if "1" in bits[k:]:
            possible_unread_hits += unread
        live, lost = cont, lost+unread
    guide = threshold_fraction(bits)
    tail = threshold_fraction(bits[len(records):])
    require(hits + live*tail + imputed - incidents*guide == residual, "incident identity failed")
    return dict(hits=hits, still_live=live, first_unread=lost,
                completed_hit_count_interval=[hits, hits+possible_unread_hits+live*int(tail>0)],
                residual_per_incident=str(residual/incidents),
                guide_for_unread_per_incident=str(F(imputed, incidents)))


def exhaustive():
    checked = 0
    for depth in range(1, 6):
        for threshold in range(1 << depth):
            bits = format(threshold, f"0{depth}b")
            for k in range(depth+1):
                for radius in (F(0), F(1, 10), F(1, 2)):
                    endpoints = (F(1, 2)-radius, F(1, 2)+radius)
                    rates = [path_rate(bits, corners, tail)
                             for corners in product(endpoints, repeat=k)
                             for tail in {0, int("1" in bits[k:])}]
                    require(complete_bounds(bits,k,radius) == (min(rates), max(rates)), "corner optimum")
                    checked += 1
    # Enumerate all routing outcomes (stop, continue, unread) for three incidents
    # on up to three digits. A run reaches the next stage only through a recorded continuation.
    tables = 0
    def walk(bits, active, rows):
        nonlocal tables
        audit_incidents(bits, 3, rows)
        tables += 1
        if len(rows) == len(bits):
            return
        for stop in range(active+1):
            for cont in range(active-stop+1):
                walk(bits, cont, rows+[(stop,cont,active-stop-cont)])
    for number in range(8):
        walk(f"{number:03b}", 3, [])
    return dict(corner_panels=checked, incident_tables=tables)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    depth = 16
    state = flight(depth)
    total = sum(n*n for n in state.values())
    require(total == 1 << depth, "signed flight normalization")
    numer = sum(n*n for (x, _), n in state.items() if x >= 0)
    bits = format(numer, f"0{depth}b")
    p = threshold_fraction(bits)
    require(p == F(50377,65536), "position changed")
    q = square_response(p)
    rows = []
    for k in range(depth+1):
        tail = threshold_fraction(bits[k:])
        fair = complete_bounds(bits,k,F(0))
        tilted = complete_bounds(bits,k,F(1,100))
        rival = path_rate(bits, [F(1,2)]*k, square_response(tail))
        require(tilted[0] <= fair[0] <= rival <= fair[1] <= tilted[1], "nested bounds")
        rows.append(dict(depth=k, fair=[str(z) for z in fair], tilted=[str(z) for z in tilted],
                         square_then_read=str(rival)))
    require(next(r['depth'] for r in rows if F(r['tilted'][1]) < q) == 3, "first discriminating depth")
    require(complete_bounds(bits,3,F(1,100)) == (F(7399,10000), F(882351,1000000)), "three decisions")
    trial = [(65,61,2),(29,31,1),(14,16,1)]
    incident = audit_incidents(bits,128,trial)
    require(incident['completed_hit_count_interval'] == [94,114], "synthetic table")
    tied = audit_incidents("0100",4,[(0,4,0),(0,4,0),(0,0,4)])
    require(tied['completed_hit_count_interval'] == [0,0], "all remaining outcomes unmarked")
    # One hidden fair bit repeated as all sixteen digits. Only 000...0 hits.
    shared = [(int(address,2)<numer) for address in ("0"*depth,"1"*depth)]
    require(shared == [True, False] and p != F(sum(shared),2), "fair marginal counterexample")
    series = [
        dict(name="Sharp range, fair split",data=[[r['depth'],*r['fair']] for r in rows]),
        dict(name="Sharp range, one-percent split error",data=[[r['depth'],*r['tilted']] for r in rows]),
        dict(name="Pooled-square hybrid",data=[[r['depth'],r['square_then_read'],r['square_then_read']] for r in rows]),
    ]
    plot = dict(title="A monitored reference after sixteen walk steps", provenance="model",
                source="Signed Hadamard walk, sharp right rail, positions x >= 0, tick 16",
                x_label="Monitored prefix digits", y_label="Hit probability",
                x_domain=[0,16], y_domain=[0,1], series=series)
    output = dict(ticks=depth, numerator=numer, total=total, bits=bits, mass=str(p),
                  unmonitored_square=str(q), rows=rows,
                  synthetic=dict(incidents=128, rows=trial, **incident), zero_suffix=tied,
                  shared_fair_digit=str(F(sum(shared),2)), sweep=exhaustive(), plot=plot)
    with args.output.open("x",encoding="utf-8",newline="\n") as out:
        json.dump(output, out, indent=2)
        out.write("\n")


if __name__ == "__main__":
    main()
