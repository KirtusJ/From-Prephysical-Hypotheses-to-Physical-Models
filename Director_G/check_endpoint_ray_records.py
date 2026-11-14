"""Check protected word pooling, changed conditional reads and a repeated-probe limit.

Before running: require path enumeration to agree with independent iterative signed
propagation on all reachable side words. Check the binary flag under two response
rules, including empty and full events. For increasing K check the exact rational
prefix probabilities, an enclosure of the deferred square-root read and its approach
to certainty. The finite line test is a grouped-instrument check, not a ray simulation.
"""

import argparse
import json
from collections import defaultdict
from fractions import Fraction as Q
from itertools import product
from pathlib import Path


def require(predicate, description):
    if not predicate:
        raise ValueError(description)


def read_side(position):
    return "L" if position < 0 else "R"


def squared_rule(p):
    return p**2 / (p**2 + (1-p)**2)


def dyadic_bracket(p, bits=24):
    scale = 1 << bits
    lo, remainder = divmod(p.numerator * scale, p.denominator)
    return [lo, lo + bool(remainder)]


def root_read_bracket(p, bits=24):
    """g(p) <= k/L exactly when p(L-k)^2 <= (1-p)k^2."""
    scale = 1 << bits
    lo, hi = 0, scale
    while lo < hi:
        k = (lo + hi) // 2
        if p * (scale-k)**2 <= (1-p) * k**2:
            hi = k
        else:
            lo = k + 1
    exact = p * (scale-lo)**2 == (1-p) * lo**2
    return [lo if exact else lo-1, lo]


def walk_controls():
    reads = {2, 4, 6}
    # Each full coordinate is (word, position, rail). A left-after-left turn is negative.
    active = {("", 0, "R"): 1}
    for t in range(1, 7):
        after = defaultdict(int)
        for (word, x, old), count in active.items():
            for new, step in (("L", -1), ("R", 1)):
                at = x+step
                label = word + (read_side(at) if t in reads else "")
                after[label, at, new] += -count if old == new == "L" else count
        active = after

    enumerated = defaultdict(int)
    for path in product("LR", repeat=6):
        x, sign, old, word = 0, 1, "R", ""
        for t, new in enumerate(path, 1):
            x += 1 if new == "R" else -1
            if old == new == "L":
                sign = -sign
            if t in reads:
                word += read_side(x)
            old = new
        enumerated[word, x, old] += sign
    require(dict(active) == dict(enumerated), "signed path and projector recurrence")
    words = ["".join(word) for word in product("LR", repeat=3)]
    weights = {word: sum(v*v for (w, _, _), v in active.items() if w == word)
               for word in words}
    total = sum(weights.values())
    require(total == 2**6, "register-copy norm on complete words")
    keep = {"LLL", "RRR"}
    pooled = Q(sum(weights[w] for w in keep), total)
    sequential = {word: Q(1) for word in words}
    for word in words:
        prefix = ""
        for label in word:
            prior = sum(n for w, n in weights.items() if w.startswith(prefix))
            prefix += label
            following = sum(n for w, n in weights.items() if w.startswith(prefix))
            if prior == 0:
                require(sequential[word] == 0, "null prefix cannot acquire weight")
                break
            sequential[word] *= squared_rule(Q(following, prior))
    require(sum(sequential.values()) == 1, "physical sequential word distribution")
    live = sum(sequential[w] for w in keep)
    require(live != squared_rule(pooled), "real-time versus deferred comparison")
    for p in (Q(0), Q(1, 2), Q(1)):
        require(squared_rule(p) == p and root_read_bracket(p) == dyadic_bracket(p),
                "empty, midpoint or full flag")
    return {
        "launch": "one R at 0; L means x < 0; reads after ticks 2, 4, 6",
        "reference_denominator": total,
        "all_reference_word_numerators": weights,
        "normalized_square_sequential_words": {w: str(p) for w, p in sequential.items()},
        "nominated_words": sorted(keep),
        "reference_pass": str(pooled),
        "deferred_normalized_square_pass": str(squared_rule(pooled)),
        "sequential_normalized_square_pass": str(live),
    }


def repeated_probes():
    rows = []
    for k in (3, 4, 8, 16, 32, 64, 128, 256):
        error = Q(1, 1+(k-1)**2)
        root_error = Q(1, k)
        require(error*(1-root_error)**2 == (1-error)*root_error**2, "root-response law")
        reference_fail = 1-(1-error)**k
        live_pass = (1-root_error)**k
        deferred = root_read_bracket(reference_fail)
        require(reference_fail <= k*error, "total reference leakage")
        require(live_pass < Q(3, 8), "real-time success stays below 3/8")
        if rows:
            require(deferred[1] < rows[-1]["terminal_root_fail"][0],
                    "terminal rejection decreases across listed probe counts")
        rows.append({"k": k, "one_probe_error": str(error),
                     "reference_fail": dyadic_bracket(reference_fail),
                     "live_root_pass": dyadic_bracket(live_pass),
                     "terminal_root_fail": deferred})
    return {"enclosure_denominator": 2**24, "rows": rows}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    target = parser.parse_args().output
    result = {"forward_walk": walk_controls(), "repeated_probes": repeated_probes()}
    with target.open("xb") as output:
        output.write((json.dumps(result, indent=2) + "\n").encode("utf-8"))
