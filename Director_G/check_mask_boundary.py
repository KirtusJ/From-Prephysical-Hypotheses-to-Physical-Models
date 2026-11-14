"""Compare entire signed endpoint multisets for three pulse orders at and above period 11."""

import argparse
import json
import random
from collections import Counter
from pathlib import Path

from check_position_mask_preparation import make_schedule, require


def pulse_rows(target, ordering, seed):
    p, q, r, s = target
    walls = {0, 4, 6, 10}
    pulses = [(0, True)] * s + [(0, False)] * r + [(6, True)] * p + [(6, False)] * q
    if ordering == "B":
        pulses.sort(key=lambda item: -item[0])
    if ordering == "C":
        random.Random(seed).shuffle(pulses)
    canonical = make_schedule((p, q), (r, s))
    rows = canonical[:8]
    for base, positive in pulses:
        for d in ((1, 2, 2, 3) if positive else (1, 2, 3)):
            rows.append(walls | {base+d})
        rows.extend((walls, walls))
    rows.extend(canonical[-7:])
    require(len(rows) == 15 + 6*(p+s) + 5*(q+r), "wrong elapsed tick count")
    if ordering == "A":
        require(rows == canonical, "production compiler differs from ordered schedule")
    return rows


def native_tally(rows, size):
    # Propagate in absolute physical sites. Keep both signs even if they cancel.
    state = Counter({(0, "R", 1): 1})
    for t, layer in enumerate(rows, 1):
        allowed = {t-2*d for d in layer}
        if size:
            allowed = {x % size for x in allowed}
        after = Counter()
        for (x, rail, sign), n in state.items():
            for daughter, dx in (("R", 1), ("L", -1)):
                y = (x+dx) % size if size else x+dx
                if y in allowed:
                    gain = -sign if rail == daughter == "L" else sign
                    after[y, daughter, gain] += n
        state = after
    return state


def run():
    # A first, B reversed, C reproducibly shuffled. All failures are retained.
    seed = 392211
    rng = random.Random(seed)
    targets = [(0, 0, 0, 0), (0, 1, 0, 1), (17, 8, 4, 19)]
    for peak in (4, 8, 17):
        for column in range(4):
            targets.append(tuple(peak if j == column else 0 for j in range(4)))
        targets.append((peak,) * 4)
    targets.extend(tuple(rng.randrange(24) for _ in range(4)) for _ in range(12))
    panels = []
    for size in (None, 11, 22, 13, 24):
        for order in "ABC":
            failures = []
            for i, target in enumerate(targets):
                rows = pulse_rows(target, order, seed+i)
                end = len(rows)-20 if size is None else (len(rows)-20) % size
                expected = Counter({(end, *cell): n for cell, n in
                                    zip((("R", 1), ("R", -1), ("L", 1), ("L", -1)), target) if n})
                observed = native_tally(rows, size)
                if observed != expected:
                    failures.append(dict(target_index=i, ticks=len(rows), site=end,
                                         all_nonzero_ports=[[*key, n] for key, n in sorted(observed.items())]))
            if order == "A" or size not in (11, 22):
                require(not failures, "failure in the scope of the preparation theorem")
            else:
                require(failures, "missing adverse pulse-order control")
            panels.append(dict(circumference=size, ordering=order, cases=len(targets),
                               matched=len(targets)-len(failures), failures=failures))
    return dict(predicates="A completes source 0 before source 6, B reverses them, C shuffles "
                "individual pulses. A matches every target on line and all named rings. All "
                "orders match on line and periods above 11. B and C each have some mismatches "
                "at period 11. Compare every terminal well, rail, sign and multiplicity.",
                seed=seed, target_order=["R+", "R-", "L+", "L-"],
                targets=targets, panels=panels)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    dest = parser.parse_args().directory
    result = run()
    dest.mkdir(parents=True, exist_ok=True)
    with (dest / "mask_boundary.json").open("x", encoding="utf8", newline="\n") as out:
        json.dump(result, out, separators=(",", ":"))
        out.write("\n")
