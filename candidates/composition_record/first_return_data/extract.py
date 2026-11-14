"""Read the pinned Zenodo JSON as data. Write job headers and raw word counts."""

import argparse
import hashlib
import json
import math
import re
from pathlib import Path


SHA256 = "2ea7433dc7e4a00ec203af9e84690ce2f915966dbe12ae1079be6d0e071ce3d4"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def check_circuit(entry):
    lines = entry["circuit"]["qasm3"].splitlines()
    body = lines[lines.index("bit[20] c;"):]
    match = re.fullmatch(r"rxx\(([^)]+)\) q\[1\], q\[2\];", body[3])
    require(match is not None, "missing first link rotation")
    angle = match.group(1)
    if "pi" in angle:
        symbolic = re.fullmatch(r"(?:(\d+)\*)?pi(?:/(\d+))?", angle)
        require(symbolic is not None, "unknown symbolic angle")
        radians = int(symbolic[1] or 1) * math.pi / int(symbolic[2] or 1)
    else:
        radians = float(angle)
    require(math.isclose(radians, entry["J"], rel_tol=1e-14), "inconsistent angles")
    expected = ["bit[20] c;", "qubit[3] q;", "x q[0];"]
    for tick in range(20):
        for links in ("q[1], q[2]", "q[0], q[1]"):
            for gate in ("rxx", "ryy"):
                expected.append(f"{gate}({angle}) {links};")
        expected.append(f"c[{tick}] = measure q[0];")
    require(body == expected, "unexpected preparation, gate order, or read order")
    return angle


def extract(source, destination):
    require(source.stat().st_size == 57_271_744, "unexpected source size")
    raw = source.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == SHA256, "source SHA-256 mismatch")
    dataset = json.loads(raw)
    entries = sorted(dataset["entries"].items(), key=lambda job: job[1]["J"])
    require(len(entries) == 99, "expected 99 angles")

    # Exclusive creation protects both the published data and previous outputs.
    with destination.open("x", encoding="ascii", newline="\n") as out:
        for ordinal, (job, entry) in enumerate(entries, start=1):
            meta = entry["job_meta"]
            require((meta["status"], meta["primitive_id"]) == ("DONE", "sampler"), job)
            require(math.isclose(entry["J"], ordinal * math.pi / 50, rel_tol=1e-14), job)
            angle = check_circuit(entry)
            require(len(entry["counts"]) == 1 and set(entry["counts"][0]) == {"c"}, job)
            counts = entry["counts"][0]["c"]
            require(sum(counts.values()) == 40_000, job)
            out.write(f"job\t{job}\t{entry['J']}\t{angle}\n")
            for word, count in counts.items():
                require(re.fullmatch("[01]{20}", word) and type(count) is int and count > 0, job)
                out.write(f"{word}\t{count}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    extract(args.source, args.destination)
