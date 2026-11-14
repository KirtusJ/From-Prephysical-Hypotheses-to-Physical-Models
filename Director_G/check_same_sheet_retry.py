"""Compare recorded same-sheet retries with a fresh-sheet restart and fair counting.

Run python -B check_same_sheet_retry.py OUTDIR. Only the Python standard
library is needed. A block is two Hadamard ticks and one opposite-rail read.
"""
import argparse
from collections import defaultdict
from fractions import Fraction
import json
import math
from pathlib import Path


def require(ok, message):
    if not ok:
        raise ValueError(message)


def near(a, b, message):
    # The finite oracle uses integers. Its independent Fourier transform and
    # the renewal calculation use binary64 on small, explicitly listed rings.
    require(abs(a - b) < 2e-12, f"{message}: {a} vs {b}")


def prefix_probabilities(order, charge, length):
    size = 4 * order
    sine_sq = [math.sin(2 * math.pi * i / size)**2 for i in range(size)]
    for i in (0, size // 2):
        sine_sq[i] = 0.0
        sine_sq[i + order] = 1.0
    factors = [1.0] * size
    prefix = [1.0]
    for j in range(1, length + 1):
        offset = 2 * (2*j - 1) * charge
        factors = [a * sine_sq[(i + offset) % size] for i, a in enumerate(factors)]
        prefix.append(math.fsum(factors) / size)
    return prefix


def renewal(prefix, cap):
    """Start times of attempts before the first success, counted in blocks."""
    m = len(prefix) - 1
    failed = [prefix[j-1] - prefix[j] for j in range(1, m+1)]
    require(min(failed) >= 0.0, "failure clock mass")
    starts = [1.0]
    done = [0.0]
    for t in range(1, cap+1):
        starts.append(math.fsum(starts[t-j] * failed[j-1] for j in range(1, min(m, t)+1)))
        new_success = starts[t-m] * prefix[m] if t >= m else 0.0
        done.append(done[-1] + new_success)
    return starts, done


def tick(order, amplitudes):
    """One signed, unnormalized tick on (well, rail, sheet) on the actual ring."""
    destination = defaultdict(int)
    for (x, rail, y), signed in amplitudes.items():
        new_y = (y + x//2) % order
        destination[((x+1) % (4*order), 1, new_y)] += signed
        destination[((x-1) % (4*order), -1, new_y)] += rail * signed
    return {coord: a for coord, a in destination.items() if a}


def sector_masses(order, amplitudes, phases):
    """The probability numerator in every Fourier sector, before 4^-elapsed."""
    by_port = defaultdict(dict)
    for (x, rail, y), a in amplitudes.items():
        by_port[x, rail][y] = a
    weights = []
    for charge in range(order):
        weights.append(math.fsum(abs(sum(a*phases[(charge*y) % order] for y, a in sheets.items()))**2
                                 for sheets in by_port.values()) / order)
    return weights


def physical_tree(order, m, cap, x0, launch_rail):
    phases = [complex(math.cos(2*math.pi*i/order), math.sin(2*math.pi*i/order)) for i in range(order)]
    releases = [0] * (cap+1)
    timeouts = 0
    by_sector = [[0.0] * order for _ in range(cap+1)]
    homes = defaultdict(int)
    release_leaves = timeout_leaves = 0
    start = {(x0, launch_rail, 0): 1}
    stack = [(0, 0, x0, launch_rail, start)]
    while stack:
        t, streak, home, rail, state = stack.pop()
        t += 1
        passed = {}
        failed = defaultdict(dict)
        for coord, a in tick(order, tick(order, state)).items():
            x, out_rail, y = coord
            if out_rail == -rail:
                passed[coord] = a
            else:
                failed[x][coord] = a
        if passed:
            if streak+1 == m:
                raw = sum(a*a for a in passed.values())
                releases[t] += raw
                homes[home] += raw * 4**(cap-t)
                weights = sector_masses(order, passed, phases)
                for s, mass in enumerate(weights):
                    by_sector[t][s] += mass / 4**t
                release_leaves += 1
            elif t == cap:
                timeouts += sum(a*a for a in passed.values())
                timeout_leaves += 1
            else:
                stack.append((t, streak+1, home, -rail, passed))
        for x, state_after_read in failed.items():
            if t == cap:
                timeouts += sum(a*a for a in state_after_read.values())
                timeout_leaves += 1
            else:
                # Preserve the sheet amplitude profile at the observed site.
                stack.append((t, 0, x, rail, state_after_read))
    cumulative = []
    total = Fraction()
    for t, v in enumerate(releases):
        total += Fraction(v, 4**t)
        cumulative.append(str(total))
    timeout = Fraction(timeouts, 4**cap)
    require(total + timeout == 1, "full original launch denominator")
    max_sector_error = 0.0
    for s in range(order):
        _, expected = renewal(prefix_probabilities(order, s, m), cap)
        for t in range(cap+1):
            actual = math.fsum(row[s] for row in by_sector[:t+1])
            max_sector_error = max(max_sector_error, abs(actual - expected[t]/order))
            near(actual, expected[t]/order, "resolved cumulative sector law")
    return dict(M=order, m=m, cap_blocks=cap, sharp_home=x0, sharp_rail=launch_rail,
                exact_prep_cdf=cumulative, exact_timeout=str(timeout),
                success_by_last_attempt_home={str(x): str(Fraction(w, 4**cap)) for x,w in sorted(homes.items())},
                release_leaves=release_leaves, timeout_leaves=timeout_leaves,
                joint_release_per_sector_by_block=by_sector, max_sector_cdf_error=max_sector_error)


def order_panel(order):
    m = 2 * max(1, round(order**(2/3) / 4))  # lambda=1/2, nearest even
    budgets = [m, 2*m, 4*m, 8*m]
    all_prefixes = [prefix_probabilities(order, s, m) for s in range(order)]
    mean_prefix = [math.fsum(p[j] for p in all_prefixes)/order for j in range(m+1)]
    _, fresh_cdf = renewal(mean_prefix, budgets[-1])
    count_prefix = [2.0**(-j) for j in range(m+1)]
    _, count_cdf = renewal(count_prefix, budgets[-1])
    sectors = []
    for s, p in enumerate(all_prefixes):
        starts, cdf = renewal(p, budgets[-1])
        e_length = math.fsum(p[:-1])
        stats = []
        for H in budgets:
            started = math.fsum(starts[:H])
            eligible = math.fsum(starts[:H-m+1])
            near(cdf[H], eligible*p[m], "eligible attempts times success")
            # Finish a last started attempt if it would extend past H.
            require(started*e_length <= H+m+1e-10, "Wald extended-attempt cap")
            stats.append(dict(release=cdf[H], expected_starts=started,
                              expected_eligible_starts=eligible,
                              mean_elapsed_blocks=math.fsum(1-q for q in cdf[:H])))
        sectors.append(dict(s=s, prefix_survival=p, mean_attempt_blocks=e_length, budgets=stats))
    aggregates = []
    for index,H in enumerate(budgets):
        ready = [row["budgets"][index]["release"] for row in sectors]
        average = math.fsum(ready) / order
        # With replacement after each failure, conditioning on a completed
        # attempt gives weights proportional to one-attempt probabilities.
        unit = (ready[1] + ready[-1]) / order
        fresh_unit = fresh_cdf[H]*(all_prefixes[1][-1]+all_prefixes[-1][-1])/(order*mean_prefix[-1])
        aggregates.append(dict(cap_blocks=H, uniform_prep=average, uniform_timeout=1-average,
                               uniform_genuine_unit_prep=unit, unit_given_prep=unit/average,
                               replace_sheet_after_failure_prep=fresh_cdf[H],
                               replace_sheet_after_failure_genuine_unit=fresh_unit,
                               persistent_count_prep=count_cdf[H]))
        if H == m:
            near(average, fresh_cdf[H], "same first attempt on both devices")
        if H == 8*m:
            require(fresh_cdf[H] > average, "fresh-sheet control separates at tested cap")
    return dict(M=order, m=m, lambda_actual=m/order**(2/3), budgets_blocks=budgets,
                count_single_attempt=count_prefix[-1], settings=sectors, totals=aggregates)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    dest = parser.parse_args().directory
    dest.mkdir(parents=True, exist_ok=True)
    path = dest / "same_sheet_retry.json"
    if path.exists():
        parser.exit(2, f"Refusing to overwrite {path}\n")
    oracle = [physical_tree(order, m, cap, x, rail)
              for order, m, cap in ((3,2,6), (4,2,6), (5,4,7))
              for x, rail in ((0,1), (4*order-1,-1))]
    require(any(any(int(x) != row["sharp_home"] for x in row["success_by_last_attempt_home"])
                for row in oracle), "successful retries away from original home")
    rows = [order_panel(n) for n in (16,17,32,33,64,65,128,129)]
    report = dict(scope="Same localized sheet, ordinary unsigned coordinate squares after signed propagation. "
                       "Only failed rail tests resolve position. Release means the end of preparation. "
                       "Terminal flight tubes require a separate calculation; no observations are used.",
                  conventions="lambda=1/2; nearest even positive m; deadlines in two-tick blocks. "
                              "Original launches include timeouts. Fair count and a new localized sheet on "
                              "each failed attempt are separate controls. The small physical oracle keeps "
                              "unreduced integer amplitudes, divided in probability by four per block. "
                              "Finite sector probabilities and the renewal arithmetic use binary64.",
                  small_physical_trees=oracle, all_sector_preparations=rows)
    with path.open("x", encoding="utf8", newline="\n") as handle:
        json.dump(report, handle, indent=2, allow_nan=False)
        handle.write("\n")


if __name__ == "__main__":
    main()
