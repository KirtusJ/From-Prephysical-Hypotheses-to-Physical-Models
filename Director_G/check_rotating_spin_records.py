"""Extract the 32 measured word frequencies from Huie et al., arXiv v4, Fig. 5(b)."""
import argparse
from fractions import Fraction
import hashlib
import io
import json
import math
from pathlib import Path
import re
from statistics import NormalDist, median
import tarfile
from urllib.request import urlopen
import zlib


SOURCE = "https://arxiv.org/src/2305.02926v4"
ARCHIVE_SHA = "60e88b33bd94d8a65fec0b3151d7afff75149e1be2dbd7a8c6f1dd2875d98557"
FIGURE_SHA = "40a36cbe3dc423241c604932f61cbc7a4e146eb4306e47d7b34ac685f47bd512"
JOURNAL = "https://harvest.aps.org/v2/journals/articles/10.1103/PRXQuantum.4.030337/fulltext"
JOURNAL_SHA = "2eaaff3dc1032e6b81f61cbf1d993b60c0f05a3eae14aadb05dc1532bf3cd685"
NUMBER = r"([-\d.]+)"


def require(value, message):
    if not value:
        raise ValueError(message)


def figure(source):
    require(hashlib.sha256(source).hexdigest() == ARCHIVE_SHA, "different arXiv source")
    with tarfile.open(fileobj=io.BytesIO(source), mode="r:gz") as archive:
        data = archive.extractfile("Figure5.pdf").read()
    require(hashlib.sha256(data).hexdigest() == FIGURE_SHA, "different figure")
    return data


def drawing(data, number):
    # These object references and their stream encodings belong to this pinned PDF.
    tag = str(number).encode("ascii")
    require(b"/x" + tag + b" " + tag + b" 0 R " in data, "missing drawing reference")
    header = re.search(rb"(?m)^" + tag + rb" 0 obj\n", data)
    start = data.index(b"\nstream\n", header.end()) + len(b"\nstream\n")
    end = data.index(b"\nendstream", start)
    return zlib.decompress(data[start:end]).decode("ascii")


def bars(data, first, style, stem_object):
    heights = []
    xs = []
    stems = re.findall(" ".join([NUMBER, NUMBER, "m", NUMBER, NUMBER, "l S Q"]), drawing(data, stem_object))
    require(len(stems) == 16, "expected sixteen uncertainty stems")
    half_widths = []
    for index in range(first, first + 16):
        body = drawing(data, index)
        rectangle = re.findall(r"([-\d.]+) ([-\d.]+) ([-\d.]+) ([-\d.]+) re\s+" + style, body)
        require(len(rectangle) == 1, "expected one measurement bar")
        x, top, width, height = map(Fraction, rectangle[0])
        require(height < 0 and 6 < width < 7, "unexpected rectangle")
        require(abs(top + height + Fraction("238.156")) <= Fraction("0.001"), "different baseline")
        xs.append(x)
        heights.append(-height)
        x1, y1, x2, y2 = map(Fraction, stems[index-first])
        require(x1 == x2 and y1 < y2, "expected a vertical error bar")
        # Styles identify each series. Match the centre more closely to this bar
        # than to its adjacent bins and to its top more closely than to either cap.
        require(abs(x1 - (x + width/2)) < width/2, "wrong word for uncertainty stem")
        require(y1 < top < y2, "uncertainty stem misses bar top")
        half_widths.append((y2-y1)/2)
    require(all(6 < b-a < 7 for a,b in zip(xs,xs[1:])), "word order")
    # The red marks plot 1/16. Their height gives an independent check on the simplex scale.
    require("35.297 -223.301 m 42.195 -223.301 l" in drawing(data,119), "reference level")
    require(abs(sum(heights) - 16 * Fraction("14.855")) < Fraction("0.02"), "probability scale")
    return heights, half_widths


def fit_counts(heights):
    # Match the integer search domain in Director Z's cross-review. Remainders
    # give exact distances in common units without float ties in the ranking.
    units = math.lcm(*(h.denominator for h in heights))
    ticks = [int(h * units) for h in heights]
    scale = sum(ticks)
    ranked = []
    for n in range(500, 8000):
        residues = [(n * t) % scale for t in ticks]
        worst = max(min(r, scale-r) for r in residues)
        ranked.append((worst, n))
    ranked.sort()
    n = ranked[0][1]
    counts = [round(Fraction(n * t, scale)) for t in ticks]
    require(sum(counts) == n, "nearest-bin table does not sum to fitted N")
    return counts, dict(search_inclusive=[500, 7999],
                        criterion="minimize max distance of N*p to an integer",
                        best_three=[dict(n=total, worst_bin_in_counts=worst / scale)
                                    for worst, total in ranked[:3]])


def sample_rate(k, n):
    p = k/n
    z = NormalDist().inv_cdf(0.975)
    denom = 1 + z*z/n
    centre = (p + z*z/(2*n))/denom
    width = z*math.sqrt(p*(1-p)/n + z*z/(4*n*n))/denom
    return dict(fitted_events=k, fitted_trials=n, rate=p, iid_se=math.sqrt(p*(1-p)/n),
                marginal_wilson_95=[centre-width, centre+width])


def count_statistics(counts):
    words = {format(i,"04b"): k for i,k in enumerate(counts)}
    rails = {}
    orders = {}
    for word, count in words.items():
        seq = "".join(str(int(a != b)) for a, b in zip(word, word[1:]))
        orders[seq] = orders.get(seq, 0) + count
    for rail in "01":
        selected = {w:k for w,k in words.items() if w[0] == rail}
        d = sum(k for w,k in selected.items() if w[1] != rail and w[2] == rail)
        rails[rail] = sample_rate(d, sum(selected.values()))
    n = sum(counts)
    contrasts = {}
    for a,b in (("011","101"),("011","110"),("101","110")):
        p, q = orders[a]/n, orders[b]/n
        contrasts[a+" minus "+b] = dict(difference=p-q, multinomial_se=math.sqrt((p+q-(p-q)**2)/n))
    pooled = sample_rate(sum(r["fitted_events"] for r in rails.values()),n)
    return dict(rail_double_flips=rails, pooled_double_flip=pooled, two_flip_order_contrasts=contrasts)


def publication_comparison(pdf, arxiv, counts):
    require(hashlib.sha256(pdf).hexdigest() == JOURNAL_SHA, "different journal PDF")
    header = re.search(rb"\b130 0 obj\b",pdf)
    start = pdf.index(b"stream",header.end()) + 6
    text = zlib.decompress(pdf[start:pdf.index(b"endstream",start)].lstrip(b"\r\n")).decode("latin1")
    panel = text.split("344.609 495.4 124.106 72.9 re\nf\n",1)[1]
    solid, rest = panel.split("[.53575 .88338 ]0 d\n",1)
    dotted, after = rest.split("\ns\nQ\n",1)
    label_text = re.findall(r"\bBT\b(.*?)\bET\b",after,re.S)[:16]
    labels = ["".join(re.findall(r"\(([01]+)\)Tj",block)) for block in label_text]
    require(labels == [format(i,"04b") for i in range(16)], "journal bin order")
    filled = re.findall(" ".join([NUMBER,NUMBER,NUMBER,NUMBER,"re\nf"]),solid)
    point = NUMBER + " " + NUMBER
    outline = re.findall(point + " m\n" + (point + " l\n") * 3 + point + " l", dotted)
    require(len(filled) == len(outline) == 16, "journal figure rectangle count")
    solid_h = []
    dotted_h = []
    for rectangle, path in zip(filled,outline):
        x,y,width,height = map(Fraction,rectangle)
        x0,y0,x1,y1,x2,y2,x3,y3,x4,y4 = map(Fraction,path)
        require(x0 == x3 == x4 and x1 == x2 and y0 == y1 == y4 and y2 == y3 < y0,
                "journal dotted rectangle geometry")
        require(abs(x0-x) < width/2 and abs(y-y2) < Fraction("0.002"), "journal bars misaligned")
        solid_h.append(height)
        dotted_h.append(y0-y2)
    results = {}
    for name,H in (("initially_detected",dotted_h),("initially_and_finally_detected",solid_h)):
        frequencies = [float(h/sum(H)) for h in H]
        errors = [p-arxiv[name]["words"][word]["frequency"] for p,word in zip(frequencies,labels)]
        fitted, fit = fit_counts(H)
        require(fitted == counts[name], "journal and preprint round to different tables")
        results[name] = dict(frequencies=frequencies, max_abs_frequency_difference=max(map(abs,errors)),
                             count_fit=fit, same_fitted_counts=True)
    return dict(url=JOURNAL, sha256=JOURNAL_SHA, figure="page 6, Fig. 5(b)", comparison=results)


def summarize(heights):
    bins = {format(i, "04b"): h for i,h in enumerate(heights)}
    total = sum(heights)
    first_flip = {}
    double_flip = {}
    for rail in "01":
        group = {word: h for word,h in bins.items() if word[0] == rail}
        exposure = sum(group.values())
        first_flip[rail] = sum(h for w,h in group.items() if w[0] != w[1]) / exposure
        double_flip[rail] = sum(h for w,h in group.items() if w[0] != w[1] and w[2] == w[0]) / exposure
    same02 = sum(h for w,h in bins.items() if w[0] == w[2]) / total
    all_same = sum(h for w,h in bins.items() if w[0] == w[1] == w[2]) / total
    double = sum(h for w,h in bins.items() if w[0] != w[1] and w[2] == w[0]) / total
    require(double == same02 - all_same, "event partition")
    flip_words = {}
    for word, height in bins.items():
        changes = "".join("0" if x == y else "1" for x, y in zip(word, word[1:]))
        flip_words[changes] = flip_words.get(changes, 0) + height / total
    order_spread = {}
    for flips in (1, 2):
        group = [p for sequence,p in flip_words.items() if sequence.count("1") == flips]
        order_spread[str(flips)] = float(max(group) - min(group))
    return dict(words={w: dict(pdf_height=str(h), frequency=float(h/total)) for w,h in bins.items()},
                first_flip_given_initial_bit={k:float(v) for k,v in first_flip.items()},
                double_flip_given_initial_bit={k:float(v) for k,v in double_flip.items()},
                pooled_flip_words={w:float(p) for w,p in sorted(flip_words.items())},
                within_flip_count_order_spread=order_spread,
                endpoint_same=float(same02), first_three_same=float(all_same), two_flips=float(double))


def load_input(path, url):
    if path is not None:
        return path.read_bytes()
    with urlopen(url, timeout=30) as response:
        return response.read()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path, help="new output JSON file")
    parser.add_argument("--source", type=Path, help="local copy of the pinned arXiv source tar.gz")
    parser.add_argument("--journal", type=Path, help="local copy of the pinned journal PDF")
    args = parser.parse_args()
    data = figure(load_input(args.source, SOURCE))
    results = dict(source=SOURCE, source_sha256=ARCHIVE_SHA, figure_sha256=FIGURE_SHA,
                   figure="Figure5.pdf panel (b), first to last read in displayed bit order",
                   unit="approximations from plotted heights", shot_denominators=None,
                   author_reported_panel_b_totals=None,
                   fit_scope="Candidate integer tables. Model-based uncertainty assumes these totals and independent trajectories.")
    counts = {}
    for name,first,style,stem in (("initially_and_finally_detected",81,"B",116),("initially_detected",97,"S",113)):
        H, half_widths = bars(data,first,style,stem)
        series = summarize(H)
        results[name] = series
        fitted, series["count_fit"] = fit_counts(H)
        counts[name] = fitted
        effective_ns = []
        for row,half,k in zip(series["words"].values(),half_widths,fitted):
            p = row["frequency"]
            half_p = float(half/sum(H))
            effective_n = p*(1-p)/half_p**2
            row.update(pdf_stem_half_height=str(half), plotted_half_width=half_p,
                       implied_n_if_binomial_se=effective_n, fitted_count=k)
            effective_ns.append(effective_n)
        series["implied_n_if_binomial_se"] = dict(min=min(effective_ns), median=median(effective_ns), max=max(effective_ns))
        series["iid_fitted_table"] = count_statistics(fitted)
    survivors = counts["initially_and_finally_detected"]
    initial = counts["initially_detected"]
    lost = [a-s for a,s in zip(initial,survivors)]
    require(min(lost) >= 0 and sum(lost) > 0, "incompatible nested fitted cohorts")
    a = results["initially_detected"]["iid_fitted_table"]["pooled_double_flip"]
    s = results["initially_and_finally_detected"]["iid_fitted_table"]["pooled_double_flip"]
    rejected = sample_rate(a["fitted_events"]-s["fitted_events"],sum(lost))
    lost_fraction = sum(lost)/sum(initial)
    results["nested_tables_if_fits_are_counts"] = dict(
        rejected_word_counts={format(i,"04b"):k for i,k in enumerate(lost)},
        rejected_pooled_double_flip=rejected, survivor_minus_initial=s["rate"]-a["rate"],
        se_given_cohort_sizes=lost_fraction*math.hypot(s["iid_se"],rejected["iid_se"]))
    results["journal"] = publication_comparison(load_input(args.journal,JOURNAL),results,counts)
    with args.output.open("x", encoding="utf8", newline="\n") as out:
        json.dump(results, out, indent=2)
        out.write("\n")


if __name__ == "__main__":
    main()
