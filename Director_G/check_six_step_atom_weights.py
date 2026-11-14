"""Read the seven reported wells, statistical caps and curves in Karski Fig. 6.3."""
import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path

SOURCE = "https://quantum-technologies.iap.uni-bonn.de/assets/pdf/thesis/phd/michal-karski-phdthesis.pdf"
DIGEST = "6db91b0bc0fd99baeac4b435f97c90fc663d9884a82c5af3e319bd6610ddf7b0"
WELLS = list(range(-3, 4))
BLUE = (0.423584, 0.552734, 0.773438)
BLACK = (0.0, 0.0, 0.0)
RED = (0.800781, 0.121582, 0.0274963)
PINK = (0.976562, 0.156982, 0.568359)
GREEN = (0.0, 0.364746, 0.168701)


def require(test, message):
    if not test:
        raise ValueError(message)


def extract(page):
    frames = sorted(page.rects, key=lambda box: box['x0'])
    require(len(frames) == 3, "expected three panel frames")
    zero = round(frames[0]['bottom'], 3)
    major_ticks = sorted({round(line['top'], 3) for line in page.lines
                          if abs(line['x0'] - frames[0]['x0']) < 0.01
                          and 3.8 < line['width'] < 4.0 and line['height'] == 0})
    require(len(major_ticks) == 5 and major_ticks[-1] == zero, "expected five major ticks")
    scale = (zero - major_ticks[0]) / 0.4

    def probability(y):
        return round((zero - y) / scale, 7)

    rows = []
    for frame in frames:
        curves = [c for c in page.curves if frame['x0'] < c['x0'] and c['x1'] < frame['x1']]
        histogram, = [c for c in curves if c['stroking_color'] == BLUE]
        bars = []
        for p1, p2 in zip(histogram['pts'], histogram['pts'][1:]):
            x1, y = p1
            x2, y2 = p2
            if abs(y - y2) > 1e-5 or x2 <= x1:
                continue
            center = (x1 + x2) / 2
            # The curve and cap centers are rounded independently in the source drawing.
            segments = [l for l in page.lines if l['stroking_color'] == BLACK
                        and l['height'] == 0 and 4.7 < l['width'] < 5.1
                        and abs((l['x0'] + l['x1']) / 2 - center) < 0.05]
            require(len(segments) == 2, "expected both error caps at the bar center")
            caps = sorted(probability(l['top']) for l in segments)
            value = probability(y)
            require(caps[0] < value < caps[1], "statistical caps do not bracket center")
            bars.append({"probability": value, "cap_lo": caps[0], "cap_hi": caps[1]})
        require(len(bars) == 7, "expected seven measured wells")
        row = {"bars": bars}
        for name, color in [('ideal', RED), ('dephasing', PINK), ('fair_paths', GREEN)]:
            for curve in curves:
                if curve['stroking_color'] == color:
                    points = curve['pts']
                    if len(points) == 9:  # plotted zero guides at both ends
                        points = points[1:-1]
                    require(len(points) == 7, "unexpected number of curve values")
                    row[name] = [probability(y) for x, y in points]
        rows.append(row)
    return dict(zip(('symmetric', 'spin_one', 'delayed_control'), rows)), major_ticks


def flight(start):
    """Signed numerators. Odd shifts send spin zero right, even shifts send it left."""
    state = {(0, start): 1}
    for t in range(6):
        sign = 1 if t % 2 == 0 else -1
        next_state = {}
        for (x, incoming), amplitude in state.items():
            for outgoing in (0, 1):
                direction = sign if outgoing == 0 else -sign
                term = -amplitude if (incoming, outgoing) == (0, 1) else amplitude
                destination = (x + direction, outgoing)
                next_state[destination] = next_state.get(destination, 0) + term
        state = next_state
    return [[state.get((2*j, r), 0) for r in (0, 1)] for j in WELLS]


def predictions(weights_a, weights_b):
    output = {}
    # For each spin, the coefficient is an unnormalised detected weight.
    for rule in ('ordinary', 'site_squared', 'rail_squared'):
        def coefficients(row):
            if rule == 'site_squared':
                return [u * sum(row) for u in row]
            if rule == 'rail_squared':
                return [u*u for u in row]
            return row

        at = []
        for j in (-2, 2):
            a = coefficients(weights_a[j+3])
            b = coefficients(weights_b[j+3])
            ratios = [y/x for x, y in zip(a, b)]
            at.append((sum(b)/sum(a), min(ratios), max(ratios)))
        left, right = at
        output[rule] = {"spin_blind": str(right[0]/left[0]),
                        "fixed_spin_gains": [str(right[1]/left[2]), str(right[2]/left[1])]}
    return output


def analyze(path):
    require(hashlib.sha256(path.read_bytes()).hexdigest() == DIGEST, "unexpected source PDF")
    import pdfplumber
    with pdfplumber.open(path) as pdf:
        rows, ticks = extract(pdf.pages[199])
    zero, one = flight(0), flight(1)
    # Equal-amplitude components in quadrature. The propagator is real.
    a = [[Fraction(u*u+v*v, 2) for u,v in zip(ur,vr)] for ur,vr in zip(zero,one)]
    b = [[Fraction(v*v) for v in row] for row in one]
    for row_name, weights in [('symmetric', a), ('spin_one', b)]:
        require(sum(map(sum, weights)) == 64, "signed flight lost norm")
        for m, y in zip(map(sum, weights), rows[row_name]['ideal']):
            require(abs(float(m/64)-y) < 0.0003, "flight differs from published ideal curve")
    for mass, y in zip((1, 6, 15, 20, 15, 6, 1), rows['delayed_control']['fair_paths']):
        require(abs(mass/64-y) < 0.0003, "control differs from fair paths")
    def odds(setting):
        bars = rows[setting]['bars']
        return bars[5]['probability']/bars[1]['probability']
    return {"source_url": SOURCE, "pdf_sha256": DIGEST, "pdf_page_one_based": 200,
            "figure": "6.3", "wells_in_lambda_over_two": WELLS,
            "axis_major_ticks_top_origin_pdf_points_at_0p4_to_zero": ticks,
            "probability_denominator": "plotted normalized positions, eligible detected atoms",
            "panels":rows, "flight_basis_columns_over_eight":{"spin_zero": zero, "spin_one": one},
            "right_left_double_odds_from_plotted_heights": round(odds('spin_one')/odds('symmetric'), 6),
            "ideal_double_odds": predictions(a,b)}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pdf', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    result = analyze(args.pdf)
    args.output.write_bytes((json.dumps(result, indent=2, ensure_ascii=False) + '\n').encode('utf8'))
