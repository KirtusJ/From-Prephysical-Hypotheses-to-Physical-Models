"""Find terminal echo words U D U in the six pinned ion GST count tables."""
import argparse
from collections import defaultdict
from decimal import Decimal
from fractions import Fraction
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import re
from urllib.request import urlopen

from check_ion_phase_records import REMOTE, SOURCES, pooled, require, upper


# Images of (+X,+Y,+Z) under the nominal positive quarter turns.
ROTATIONS = {"Gx": (1, 3, -2), "Gy": (-3, 2, 1), "Gi": (1, 2, 3)}
TOKENS = re.compile(r"(?:\(((?:G[ixy])+)\)\^(\d+)|(G[ixy]))")
BLOCKS = ("GyGx", "GxGy")
IDENTITY = (1, 2, 3)


def action(frame, axis):
    return frame[abs(axis) - 1] * (1 if axis > 0 else -1)


def compose(first, second):
    """Apply first then second, the file's chronological word order."""
    return tuple(action(second, axis) for axis in first)


@lru_cache(maxsize=None)
def rotation(word):
    frame = IDENTITY
    for start in range(0, len(word), 2):
        gate = ROTATIONS[word[start:start + 2]]
        frame = compose(frame, gate)
    return frame


def power(frame, n):
    result = IDENTITY
    while n:
        if n % 2:
            result = compose(result, frame)
        frame = compose(frame, frame)
        n //= 2
    return result


@lru_cache(maxsize=None)
def parse_word(label):
    if label == "{}":
        return "", IDENTITY
    end = 0
    parts = []
    frame = IDENTITY
    for token in TOKENS.finditer(label):
        require(token.start() == end, "unsupported syntax " + label)
        raw, exponent, single = token.groups()
        base, count = (raw, int(exponent)) if single is None else (single, 1)
        parts.append(base * count)
        frame = compose(frame, power(rotation(base), count))
        end = token.end()
    require(end == len(label), "incomplete syntax " + label)
    return "".join(parts), frame


def load(filename, folder):
    if folder:
        data = (folder / filename).read_bytes()
    else:
        with urlopen(REMOTE + filename, timeout=30) as response:
            data = response.read()
    require(hashlib.sha256(data).hexdigest() == SOURCES[filename], filename)
    echo = []
    controls = defaultdict(list)
    all_rows = defaultdict(list)
    block = BLOCKS[0]
    wanted = {"", "GxGx", block, block * 2, block * 3}
    for line_no, source in enumerate(data.decode("utf8").split("\n"), 1):
        if not source.strip() or source.startswith("#"):
            continue
        label, plus, total, *rest = source.split()
        word, frame = parse_word(label)
        k, n = Decimal(plus), Decimal(total)
        require(k == int(k) and n == int(n) and 0 <= k <= n and n > 0, "counts")
        row = dict(line=line_no, label=label, plus=int(k), total=int(n), trailing_fields=rest)
        all_rows[word].append(row)
        if word in wanted:
            controls[word].append(row)
        if "Gi" in word:
            continue
        for block_name in BLOCKS:
            if len(word) <= 2 * len(block_name) or not (word.startswith(block_name) and word.endswith(block_name)):
                continue
            # The signed-axis Clifford action has exponent 12. Strip the two outer blocks.
            back = power(rotation(block_name), 11)
            require(compose(back, rotation(block_name)) == IDENTITY, "inverse")
            midpoint = compose(compose(back, frame), back)
            if midpoint[2] == 3 and midpoint != IDENTITY:
                require(midpoint == rotation(word[len(block_name):-len(block_name)]), "literal middle")
                echo.append(dict(**row, block=block_name, length=len(word)//2,
                                 midpoint_x_axis=midpoint[0], final_z_axis=frame[2]))
    return dict(controls=dict(controls), nonidentity_diagonal_echoes=echo), all_rows


def bounds(data, shortest, family):
    block = BLOCKS[0]
    rows = data["controls"]
    echo = [r for r in data["nonidentity_diagonal_echoes"] if r["block"] == block
            and r["midpoint_x_axis"] == -1 and r["length"] == shortest]
    if not echo:
        return None
    tables = [rows[""], rows[block * 2], echo, rows[block * 3], rows["GxGx"]]
    samples = [pooled(row) for row in tables]
    fractions = [Fraction(k, n) for k, n in samples]
    # Per date: lower and upper null, lower free-2, lower echo, upper free-3, lower bright control.
    tail = 0.05 / (6 * family)
    def lower(i):
        k, n = samples[i]
        return max(0., 1 - upper(n-k, n, tail))
    def high(i):
        return upper(*samples[i], tail)
    a_low, a_high = lower(0), high(0)
    y2_low, e_low, y3_high, h_low = lower(1), lower(2), high(3), lower(4)
    require(h_low > a_high, "contrast unresolved on a selected panel")
    # A positive contrast follows from the bright control exceeding a pure-R null.
    # L2+LE >= (y2+yE-2A)/(1-A); D=(1-L2-LE)/4.
    d_cap = min(0.25, (1+a_high-y2_low-e_low)/(4*(1-a_high)))
    # For B >= h_low and A in [a_low,a_high], maximize the ratio at a_low when y3_high<h_low.
    l3_cap = min(1., (y3_high-a_low)/(h_low-a_low)) if y3_high < h_low else 1.
    require(d_cap >= 0 and l3_cap >= 0, "confidence region incompatible with model")
    return dict(counts=samples, bright_rate_fractions=[str(v) for v in fractions],
                families=family, one_sided_tail=tail, intervals=dict(null_low=a_low,
                null_high=a_high, free2_low=y2_low, echo_low=e_low, free3_high=y3_high, bright_low=h_low),
                D_upper=d_cap, L3_upper=l3_cap, fair_upper=min(1,2*l3_cap))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_directory", type=Path)
    parser.add_argument("--inputs", type=Path)
    args = parser.parse_args()
    loaded = {name: load(name, args.inputs) for name in SOURCES}
    data = {name: panels for name, (panels, _) in loaded.items()}
    candidates = [r["length"] for result in data.values() for r in result["nonidentity_diagonal_echoes"]
                  if r["block"] == BLOCKS[0] and r["midpoint_x_axis"] == -1]
    shortest = min(candidates)
    focus = {parse_word(r["label"])[0][len(BLOCKS[0]):-len(BLOCKS[0])]
             for result in data.values() for r in result["nonidentity_diagonal_echoes"]
             if r["length"] == shortest and r["block"] == BLOCKS[0] and r["midpoint_x_axis"] == -1}
    require(len(focus) == 1, "shortest sign plate has more than one pulse spelling")
    mid = next(iter(focus))
    require(rotation(mid) == (-1,-2,3), "midpoint sign")
    require(all(rotation(name)[2] != 3 for name in BLOCKS), "nontrivial outer block")
    for name, (record, rows) in loaded.items():
        record["bounds"] = bounds(record, shortest, len(data))
        record["same_midpoint_calibrations"] = {p + mid + a: rows.get(p + mid + a, [])
                                               for p in ("", "Gx", "Gy") for a in ("", "Gx", "Gy")}
    result = dict(source_hashes=SOURCES, shortest_sign_word_length=shortest, midpoint=mid, datasets=data)
    args.output_directory.mkdir(parents=True, exist_ok=True)
    with (args.output_directory / "ion_phase_echo.json").open("x", encoding="utf8", newline="\n") as stream:
        json.dump(result, stream, indent=2)
        stream.write("\n")


if __name__ == "__main__":
    main()
