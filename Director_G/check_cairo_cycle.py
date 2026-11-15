"""Replay Figure 8 of Razzoli et al. (2024). Pass DTQW_n3.pdf to check the transcription."""
import argparse
import hashlib
import json
from math import sqrt
from pathlib import Path

FIGURE_SHA256 = "33c0ef932753d080717d343f30f77c758b90936d161a62120571f6a4c78b4a21"
RECORD = Path(__file__).parent / "results" / "cairo_cycle_figure8.json"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def transfer_matrices(ticks):
    # Site matrices map the two possible initial coin columns to final coin rows.
    # Omit the common factor 2**(-t/2) so all path additions are exact.
    sites = [(1, 0, 0, 1)] + [(0, 0, 0, 0)] * 7
    for _ in range(ticks):
        updated = []
        for site in range(8):
            a, b, c, d = sites[(site + 1) % 8]
            e, f, g, h = sites[(site - 1) % 8]
            updated.append((a + c, b + d, e - g, f - h))
        sites = updated
    return sites


def walk_effects(ticks):
    return [(a*a + c*c, a*b + c*d, b*b + d*d) for a, b, c, d in transfer_matrices(ticks)]


def ideal_positions(ticks):
    rail_zero = (2 + sqrt(3)) / 4
    return [(rail_zero * left + (1 - rail_zero) * right) / (2**ticks)
            for left, _, right in walk_effects(ticks)]


def extract(figure):
    import pymupdf

    require(hashlib.sha256(figure.read_bytes()).hexdigest() == FIGURE_SHA256,
            "Expected DTQW_n3.pdf from arXiv:2402.01854v2")
    with pymupdf.open(figure) as doc:
        drawings = doc[0].get_drawings()
    red = (1., 0., 0.)
    black = (0., 0., 0.)
    bars = [item["rect"] for item in drawings if item["type"] == "f"
            and item["fill"] == red and 8 < item["rect"].width < 10]
    navy = [item["rect"] for item in drawings if item["type"] == "f"
            and item["fill"][2] > item["fill"][1] > item["fill"][0]
            and 8 < item["rect"].width < 10]
    vertical = [item["rect"] for item in drawings if item["type"] == "s"
                and item["color"] == black and item["rect"].width == 0]
    frames = [rect for rect in vertical if 135 < rect.height < 140]
    require((len(bars), len(navy), len(frames)) == (72, 30, 18), "Panel (b) layout changed")
    rows = []
    ideal_bars = []
    used = set()
    for ticks in range(9):
        row = bars[8*ticks:8*ticks + 8]
        frame = min(frames, key=lambda rect: abs(rect.x0 - row[0].x0) + abs(rect.y1 - row[0].y1))
        require(all(abs(bar.y1 - frame.y1) < .02 for bar in row), "Bar baseline")
        require(all(35 < row[i+1].x0 - row[i].x0 < 37 for i in range(7)), "Site ordering")
        navy_row = []
        for bar, expected in zip(row, ideal_positions(ticks)):
            matches = [i for i, rect in enumerate(navy)
                       if abs(rect.x1 - bar.x0) < .02 and abs(rect.y1 - bar.y1) < .02]
            require(len(matches) == int(expected > 0), "Ideal bar at unexpected site")
            if matches:
                index, = matches
                navy_row.append(round(navy[index].height / frame.height, 6))
                used.add(index)
            else:
                navy_row.append(0.)
        ideal_bars.append(navy_row)
        rows.append([round(bar.height / frame.height, 6) for bar in row])
    require(len(used) == len(navy), "Unmatched ideal bars")
    plot, = [rect for rect in vertical if rect.height > 500 and rect.x0 < 200]
    circles = [item["rect"] for item in drawings if item["type"] == "fs" and item["fill"] == red
               and plot.y0 < item["rect"].y0 and item["rect"].y1 < 470]
    require(len(circles) == 30, "Panel (a) marker count")
    require(all(32 < b.x0 - a.x0 < 33 for a, b in zip(circles, circles[1:])), "Time ordering")
    fidelities = [round((plot.y1 - (r.y0 + r.y1)/2) / plot.height, 6) for r in circles]
    return {"figure_sha256": FIGURE_SHA256, "cairo_opt_sites_0_to_7_by_tick_0_to_8": rows, "plotted_ideal_sites": ideal_bars,
            "cairo_opt_hellinger_fidelity_by_tick_0_to_29": fidelities}


def check(data):
    rows = data["cairo_opt_sites_0_to_7_by_tick_0_to_8"]
    fid = data["cairo_opt_hellinger_fidelity_by_tick_0_to_29"]
    require(data["figure_sha256"] == FIGURE_SHA256 and len(rows) == 9 and len(fid) == 30, "Record shape")
    navy = data["plotted_ideal_sites"]
    require(len(navy) == 9 and all(len(row) == 8 for row in navy), "Plotted ideal rows")
    require(all(0 <= v <= 1 for v in fid), "Fidelity range")
    panel_gaps = []
    ideal_gaps = []
    for t, row in enumerate(rows):
        require(len(row) == 8 and all(0 <= p <= 1 for p in row), "Invalid row")
        require(abs(sum(row) - 1) < .0002, "Row sum outside plot precision")
        calculated = sum(sqrt(p*q) for p, q in zip(row, ideal_positions(t)))**2
        panel_gaps.append(calculated - fid[t])
        ideal_gaps.extend(abs(p-q) for p, q in zip(ideal_positions(t), navy[t]))
    # With the paper's coin in quadrature, the real column cross term vanishes.
    # At t=8 each component has twice the unsigned integer coefficient at t=6.
    for m6, m8 in zip(transfer_matrices(6), transfer_matrices(8)):
        require(all(4*a*a == b*b for a, b in zip(m6, m8)), "Full bitstring comparison")
    for site in (0, 4):
        require(walk_effects(4)[site] == (2, 0, 2), "Four-tick null effect")
    for t in (6, 8):
        numerators = [1, 0, 1, 0, 5, 0, 1, 0]
        require(walk_effects(t) == [(n*2**(t-3), 0, n*2**(t-3)) for n in numerators], "Repeated table")
    require(walk_effects(24) == [(2**24, 0, 2**24)] + [(0, 0, 0)]*7, "Position return")
    tv = sum(abs(a-b) for a, b in zip(rows[6], rows[8])) / 2
    print("Fidelity reconstructed from panel (b) minus panel (a) by tick:",
          [round(value, 6) for value in panel_gaps])
    print(f"Largest ideal-bar residual against analytic probabilities: {max(ideal_gaps):.6f}")
    print(f"Tick 4 site 4 minus site 0: {rows[4][4] - rows[4][0]:.6f}")
    print(f"Tick 6 vs tick 8 TV: {tv:.6f}; half: {tv/2:.6f}")
    print(f"Site 4 change: {rows[8][4] - rows[6][4]:.6f}")
    print(f"Displayed return fidelities at ticks 0 and 24: {fid[0]:.6f}, {fid[24]:.6f}")
    print(f"Largest plotted row-sum residual: {max(abs(sum(r)-1) for r in rows):.6f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("figure", type=Path, nargs="?")
    parser.add_argument("--write-transcription", action="store_true")
    args = parser.parse_args()
    if args.write_transcription and args.figure is None:
        parser.error("--write-transcription requires the authors' figure")
    record = extract(args.figure) if args.figure else json.loads(RECORD.read_text())
    check(record)
    if args.write_transcription:
        RECORD.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    elif args.figure:
        require(record == json.loads(RECORD.read_text()), "Published extraction differs from transcription")
