"""Compare a pooled site predicate with a persistent sharp site record."""
from argparse import ArgumentParser
from itertools import product
import json
from pathlib import Path


ZERO_BLOCK = ((0, 0), (0, 0))
INPUT_BASIS = ((1, 0), (0, 1))


def check(condition, message):
    if not condition:
        raise ValueError(message)


def forward(state, ticks, ring):
    """Propagate the integer numerator of the two source-to-rail rows at each site."""
    for _ in range(ticks):
        after = {}
        for site, ((a, b), (c, d)) in state.items():
            outgoing = ((site + 1, 0, (a + c, b + d)), (site - 1, 1, (a - c, b - d)))
            for destination, rail, row in outgoing:
                if ring:
                    destination %= ring
                # The oriented shift has exactly one predecessor per destination and rail.
                after.setdefault(destination, [(0, 0), (0, 0)])[rail] = row
        state = after
    return state


def split_rows(early, total, ring):
    middle = forward({0: INPUT_BASIS}, early, ring)
    return {site: forward({site: block}, total - early, ring) for site, block in middle.items()}


def signed_words(early, total, ring):
    """Separate complete signed direction histories without matrix propagation."""
    rows = {}
    for word in product((0, 1), repeat=total):
        site = early - 2 * sum(word[:early])
        final_site = total - 2 * sum(word)
        if ring:
            site, final_site = site % ring, final_site % ring
        row = rows.setdefault(site, {}).setdefault(final_site, [[0, 0], [0, 0]])[word[-1]]
        for source in (0, 1):
            flips = sum(previous * current for previous, current in zip((source,) + word, word))
            row[source] += (-1) ** flips
    return rows


def outer(a, b):
    """Upper triangle of a real signed row's Gram matrix."""
    return a * a, a * b, b * b


def sum_grams(matrices):
    return tuple(map(sum, zip((0, 0, 0), *matrices)))


def panel(early, total, ring, mask, events):
    rows = split_rows(early, total, ring)
    word_rows = signed_words(early, total, ring)
    sites = sorted(rows)
    final_sites = sorted({y for outgoing in rows.values() for y in outgoing})
    cells = []
    for flag, final_site, rail in product((0, 1), final_sites, (0, 1)):
        contributions = {}
        for site in sites:
            row = rows[site].get(final_site, ZERO_BLOCK)[rail]
            check(tuple(row) == tuple(word_rows[site].get(final_site, ZERO_BLOCK)[rail]), "signed-word sum")
            if (site in mask) == bool(flag):
                contributions[site] = row
        a = sum(row[0] for row in contributions.values())
        b = sum(row[1] for row in contributions.values())
        cells.append(dict(flag=flag, site=final_site, rail=rail, site_rows=contributions,
                          pooled=outer(a, b),
                          lookup=sum_grams(outer(*row) for row in contributions.values())))
    for key in ("pooled", "lookup"):
        total_effect = sum_grams(cell[key] for cell in cells)
        check(total_effect == (2**total, 0, 2**total), "complete read on original launches")
    chosen = [cell for cell in cells if (cell["flag"], cell["site"], cell["rail"]) in events]
    check(len(chosen) == len(events), "selected ports exist")
    check(sum_grams(cell["pooled"] for cell in chosen) == (0, 0, 0), "dark effect")
    numerator = 2 ** (total - 4)
    check(sum_grams(cell["lookup"] for cell in chosen) == (numerator, 0, numerator),
          "scalar one-sixteenth effect")
    return dict(ticks=[early, total], geometry=ring or "line", sites_in_mask=sorted(mask),
                selected_ports=sorted(events), denominator=2**total, cells=cells)


def shortest_line():
    """For each mask collect all identically dark final rows and test sharp-label rank."""
    result = []
    for total in range(2, 7):
        masks, rank_two = 0, 0
        for early in range(1, total):
            rows = split_rows(early, total, None)
            sites = sorted(rows)
            for mask in product((0, 1), repeat=len(sites)):
                masks += 1
                dark = []
                for flag, final_site, rail in product((0, 1), range(-total, total + 1, 2), (0, 1)):
                    subset = [rows[site].get(final_site, ZERO_BLOCK)[rail]
                              for site, bit in zip(sites, mask) if bit == flag]
                    if sum(a for a, b in subset) == sum(b for a, b in subset) == 0:
                        dark.extend(outer(a, b) for a, b in subset)
                a, b, c = sum_grams(dark)
                rank_two += int(a * c > b * b)
        check(rank_two == (2 if total == 6 else 0), "number of separating masks")
        result.append(dict(total_ticks=total, masks_tested=masks, rank_two_masks=rank_two))
    return result


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    destination = parser.parse_args().output
    rail_events = {(1, 0, 0), (0, 0, 1)}
    position_events = {(1, site, rail) for site, rail in product((2, 6), (0, 1))}
    results = dict(line=panel(3, 6, None, {-3, 1}, rail_events),
                   eight_ring=panel(3, 6, 8, {1, 5}, rail_events),
                   eight_ring_position_only=panel(4, 10, 8, {0, 4}, position_events),
                   line_search=shortest_line())
    with destination.open("x", encoding="utf8", newline="\n") as out:
        json.dump(results, out, indent=2)
        out.write("\n")


if __name__ == "__main__":
    main()
