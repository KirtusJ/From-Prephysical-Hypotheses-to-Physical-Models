"""Exact local-bit and sink readouts on a physical signed clock. No external data."""

import argparse
import json
from collections import Counter
from fractions import Fraction
from itertools import pairwise, product
from pathlib import Path

M = 5
DIR = (1, -1)
SETTINGS = {"both": DIR, "R": (1,), "L": (-1,)}


def add_term(v, c, d, signed):
    return -v if signed and c == d == -1 else v


def weight(v, signed):
    return v * v if signed else v


def force_launch(k=1, marked=0, signed=True):
    state = {(0, 1, marked): 1}
    for _ in range(2):
        out = Counter()
        for (x, c, y), v in state.items():
            for d in DIR:
                out[x + d, d, (y + k * x) % M] += add_term(v, c, d, signed)
        state = out
    assert len(state) == 4 and sum(weight(v, signed) for v in state.values()) == 4
    return state


def initial_live(signed, launch_site=0):
    # Retain distinct old base modes b throughout, including at the detector.
    return {
        (x, c, y, 1, 0): v for (x, c, y), v in force_launch(marked=launch_site, signed=signed).items()
    }


def probe_tick(state, signed, stride=1):
    out = Counter()
    for (x, c, y, r, b), v in state.items():
        for d in DIR:
            out[x, c, (y + d * stride) % M, d, b] += add_term(v, r, d, signed)
    return {key: v for key, v in out.items() if v}


def contact(state, marker, rails):
    # Real, reversible controlled-X on a carried bit: all old base modes
    # retain their labels. A final common stream is a permutation as well.
    return {(x, c, y, d, b ^ int(y == marker and d in rails)): v for (x, c, y, d, b), v in state.items()}


def bit_bins(state, signed):
    return [sum(weight(v, signed) for (*_, b), v in state.items() if b == i) for i in (0, 1)]


def direct_words(t, marker, rails, signed, operation):
    # Independent direction-word enumeration. In sink mode each captured
    # prefix ends the flight; later words sharing that prefix are not counted.
    live = Counter()
    seen = set()
    sink = Counter()
    for a, c in product(DIR, repeat=2):
        old = (a + c, c)
        seed = a % M
        old_sign = -1 if signed and a == c == -1 else 1
        for word in product(DIR, repeat=t):
            sites = [(seed + sum(word[: h + 1])) % M for h in range(t)]
            hits = [h for h, (y, d) in enumerate(zip(sites, word)) if y == marker and d in rails]
            if operation == "sink" and hits:
                h = hits[0] + 1
                prefix = word[:h]
                identity = (old, prefix)
                if identity in seen:
                    continue
                seen.add(identity)
                negative = sum(p == q == -1 for p, q in pairwise((1,) + prefix))
                sink[h, old, prefix[-1]] += old_sign * ((-1) ** negative if signed else 1)
            else:
                d = word[-1] if word else 1
                y = sites[-1] if sites else seed
                negative = sum(p == q == -1 for p, q in pairwise((1,) + word))
                b = len(hits) % 2 if operation == "parity" else int(bool(hits) and hits[-1] == t - 1)
                live[*old, y, d, b] += old_sign * ((-1) ** negative if signed else 1)
    if operation != "sink":
        return bit_bins(live, signed)
    bins = [sum(weight(v, signed) for (h, _, _), v in sink.items() if h == i) for i in range(1, t + 1)]
    return bins, sum(weight(v, signed) for v in live.values())


def terminal_and_parity(marker, rails, signed, horizon):
    state = initial_live(signed)
    parity = dict(state)
    results = []
    for t in range(1, horizon + 1):
        den = 4 * 2**t
        state = probe_tick(state, signed)
        marked = contact(state, marker, rails)
        assert contact(marked, marker, rails) == state
        # Read after the extra *unconditional streaming-only* tick, so every
        # walker moves while the hit bit, and hence its marginal, survives.
        streamed = {(x, c, (y + d) % M, d, b): v for (x, c, y, d, b), v in marked.items()}
        terminal = bit_bins(marked, signed)
        assert bit_bins(streamed, signed) == terminal
        parity = contact(probe_tick(parity, signed), marker, rails)
        par = bit_bins(parity, signed)
        assert sum(terminal) == sum(par) == den
        assert terminal == direct_words(t, marker, rails, signed, "terminal")
        assert par == direct_words(t, marker, rails, signed, "parity")
        results.append([t, den, *terminal, *par])
    return results


def absorbing(marker, rails, signed, horizon):
    live = initial_live(signed)
    sink = {}
    first = []
    survivors = []
    bin_rails = []
    for t in range(1, horizon + 1):
        arrived = probe_tick(live, signed)
        live = {}
        for (x, c, y, d, b), v in arrived.items():
            if y == marker and d in rails:
                # A permutation swaps active and empty time-bin modes with
                # identical spectator and probe rail. Outgoing bins never return.
                key = (t, x, c, d)
                assert key not in sink
                sink[key] = v
            else:
                live[x, c, y, d, b] = v
        by_dir = [
            sum(weight(v, signed) for (h, _, _, d), v in sink.items() if h == t and d == r) for r in DIR
        ]
        bin_rails.append(by_dir)
        first.append(sum(by_dir))
        survivors.append(sum(weight(v, signed) for v in live.values()))
        den = 4 * 2**t
        assert sum(v * 2 ** (t - h) for h, v in enumerate(first, 1)) + survivors[-1] == den
    assert direct_words(horizon, marker, rails, signed, "sink") == (first, survivors[-1])
    return {
        "first_capture_numerators": first,
        "first_capture_by_R_L_numerators": bin_rails,
        "survival_numerators": survivors,
        "time_denominators": [4 * 2**t for t in range(1, horizon + 1)],
    }


def readout_controls(rows):
    ps = [Fraction(rows[name][-1][3], rows[name][-1][1]) for name in ("signed", "count")]
    controls = []
    for false_positive, false_negative in (
        (0, 0),
        (Fraction(1, 100), Fraction(1, 20)),
        (Fraction(1, 2), Fraction(1, 2)),
        (1, 1),
    ):
        observed = [false_positive + (1 - false_positive - false_negative) * p for p in ps]
        controls.append(
            {
                "false_positive": str(false_positive),
                "false_negative": str(false_negative),
                "signed_click": str(observed[0]),
                "count_click": str(observed[1]),
                "count_minus_signed": str(observed[1] - observed[0]),
            }
        )
    return controls


def staircase():
    law = {}
    # Distinct base positions through 5 stay inside C32; order 11 also
    # avoids sheet aliasing within the requested (1,R) endpoint.
    for signed in (True, False):
        s = {(0, 1, 0): 1}
        for _ in range(5):
            out = Counter()
            for (x, c, y), v in s.items():
                for d in DIR:
                    out[x + d, d, (y + x // 2) % 11] += add_term(v, c, d, signed)
            s = out
        full = {k: weight(v, signed) for k, v in s.items() if v}
        assert sum(full.values()) == 32
        law["signed" if signed else "count"] = {
            "terminal_bits_no_yes": [32 - full.get((1, 1, 10), 0), full.get((1, 1, 10), 0)],
            "endpoint_1R_sheet_numerators": [full.get((1, 1, y), 0) for y in range(11)],
        }
    witnesses = []
    for word in product(DIR, repeat=5):
        x = y = 0
        for d in word:
            y += x // 2
            x += d
        if (x, word[-1], y % 11) == (1, 1, 10):
            s = (-1) ** sum(c == d == -1 for c, d in pairwise((1,) + word))
            witnesses.append({"directions": word, "sheet_displacement": y, "sign": s})
    assert len(witnesses) == 2 and sum(w["sign"] for w in witnesses) == 0
    assert law["signed"]["terminal_bits_no_yes"] == [32, 0] and law["count"]["terminal_bits_no_yes"] == [
        30,
        2,
    ]
    return {
        "gain": "floor(x/2) on the centred base of C32, initial (0,R,0), C11 sheet. Terminal "
        "flip at the single complete physical cell (1,R,-1 mod 11).",
        "five_tick_denominator": 32,
        "two_histories": witnesses,
        "laws": law,
    }


def main():
    settings = {}
    for marker in (0, 1):
        for rail, dirs in SETTINGS.items():
            name = f"marker{marker}_{rail}"
            rows = {}
            sinks = {}
            for signed, label in ((True, "signed"), (False, "count")):
                rows[label] = terminal_and_parity(marker, dirs, signed, 5)
                sinks[label] = absorbing(marker, dirs, signed, 5)
            settings[name] = {
                "ticks": rows,
                "sink": sinks,
                "terminal_bit_readout_error_controls": readout_controls(rows),
            }
    correct = settings["marker0_R"]["ticks"]
    assert correct["signed"][-1][3] == 0 and correct["count"][-1][3] == 20
    parity = settings["marker0_L"]["ticks"]
    assert parity["signed"][-1][5] == 28 and parity["count"][-1][5] == 48
    sink = settings["marker0_both"]["sink"]
    assert (
        sink["signed"]["first_capture_numerators"][-1] == 0
        and sink["count"]["first_capture_numerators"][-1] == 8
    )
    # A fresh uniformly randomized marker reads 1/M of *selected rail*
    # occupancy. With both rails selected this is 1/M for each law.
    lost = {}
    hidden = []
    for signed, label in ((True, "signed"), (False, "count")):
        s = initial_live(signed)
        for _ in range(5):
            s = probe_tick(s, signed)
        lost[label] = {
            rail: str(Fraction(sum(bit_bins(contact(s, j, dirs), signed)[1] for j in range(M)), M * 128))
            for rail, dirs in SETTINGS.items()
        }
        assert lost[label]["both"] == "1/5"
        if signed:
            for (x, c, _), initial in force_launch().items():
                hidden.append(
                    {
                        "old_mode": [x, c],
                        "force_amplitude_numerator": initial,
                        "terminal_marked_R_L_signed_numerators": [
                            s.get((x, c, 0, d, 0), 0) for d in DIR
                        ],
                    }
                )
        else:
            for row in hidden:
                x, c = row["old_mode"]
                row["terminal_marked_R_L_word_counts"] = [s.get((x, c, 0, d, 0), 0) for d in DIR]
        # A genuine co-translation preserves the click law even though a
        # misaligned marker generally changes it.
        translated = initial_live(signed, launch_site=2)
        for _ in range(5):
            translated = probe_tick(translated, signed)
        assert bit_bins(contact(translated, 2, (1,)), signed) == bit_bins(contact(s, 0, (1,)), signed)
    return {
        "setup": "Physical C5 sheet; two native force ticks g(x)=x from (0,R,0). The four orthogonal "
        "old position/coin modes retain their labels. A separate initialized R probe coin then takes "
        "five ordinary +/-1, signed H, sheet steps. A detector couples only to the named physical "
        "cell and selected arriving rail(s); all other coordinates are unread. Counterfactual counting "
        "propagates history multiplicities and divides by 2 per H. The signed law squares the summed "
        "real amplitudes separately in each complete cell. Both use the same routing and detector.",
        "readout": "A terminal controlled-X flips a carried zero bit at the chosen site and rail(s). "
        "Afterwards every walker can continue through a common streaming-only step; only the bit is "
        "read. The port-conditioned permutation is local on each sheet fibre. If old bases are separate "
        "physical places, the marker coupling must be present there or the modes coherently brought to "
        "one device. Marker placement, gating/clock, clean bit and readout of that bit are supplied.",
        "row_columns": [
            "probe_ticks",
            "denominator",
            "terminal_no",
            "terminal_yes",
            "parity_even",
            "parity_odd",
        ],
        "instruments": "Always-on XOR measures visit parity without intermediate read. The sink swaps "
        "a hit on each tick into distinct initially blank outgoing modes carrying time and rails. "
        "A finite stopped sink and a reversible single-bit OR are different: overwriting two inputs "
        "by one output loses reversibility, so a destructive sink pays a reservoir/reset cost. "
        "All first bins and no-capture probability are retained. Numerators use the denominators "
        "for their actual number of H layers, including the initial two force layers.",
        "settings": settings,
        "terminal_origin_5_by_orthogonal_force_mode": hidden,
        "uniform_independent_false_marker_t5": lost,
        "readout_error_equation": "With false-positive f and false-negative g, click frequency is "
        "f+(1-f-g)p. Rates here are illustrative settings, not a measured detector calibration.",
        "staircase": staircase(),
        "claim_scope": "This comparison is already on an explicitly supplied "
        "physical signed lift and record instrument. If the normalized rule is a mixture with counting "
        "weight a and this physical signed-square weight 1-a, marker0_R at probe time five has mass "
        "5a/32. The experiment cannot distinguish the odd-character labels on all-real gates, does "
        "not determine other multiset weights without their instrument model, and does not derive "
        "the squared-coordinate probability law from the detector circuit.",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()
    out = main()
    args.directory.mkdir(parents=True, exist_ok=True)
    (args.directory / "local_clock_detector.json").write_text(
        json.dumps(out, indent=2) + "\n", encoding="utf-8"
    )
    print(
        "Verified six settings, three complete detector instruments, two record rules and the staircase port."
    )
