"""Compact coherent four-arm reference for a real two-rail effect."""


def analyzer_reference(effect, scale):
    """Return integer (input R, input L) rows in [miss, hit], in units 1/sqrt(4S).

    The effect triple gives the R diagonal, cross term and L diagonal in
    units of 1/S. A positive X or Z sign marks its positive eigenrail.
    The returned prefix intervals are half-open on the 4S-address ruler.
    """
    aa, ab, bb = effect
    if any(type(v) is not int for v in (aa, ab, bb, scale)):
        raise ValueError("effect numerators and scale must be integers")
    if scale < 1 or scale & (scale - 1):
        raise ValueError("scale must be a positive power of two")
    if not (0 <= aa <= scale and 0 <= bb <= scale
            and ab * ab <= min(aa * bb, (scale - aa) * (scale - bb))):
        raise ValueError("effect must lie between zero and the identity")

    total = 4 * scale
    shared = 2 * abs(ab) + abs(aa - bb)
    weights = {"hit": scale + aa + bb - shared,
               "miss": 3 * scale - aa - bb - shared,
               "X": 4 * abs(ab), "Z": 2 * abs(aa - bb)}
    signs = {"X": (ab > 0) - (ab < 0),
             "Z": (aa > bb) - (aa < bb)}
    if sum(weights.values()) != total or min(weights.values()) < 0:
        raise ArithmeticError("analyzer arm weights do not partition the input")

    # Put X first, so both ends of its interval are multiples of four.
    # Every maximal dyadic X leaf then has width at least four, giving
    # an even numerator before its final H(tensor)H acts on coin and blank.
    intervals = []
    end = 0
    for arm in ("X", "Z", "hit", "miss"):
        if weights[arm]:
            intervals.append((end, end + weights[arm], arm))
            end += weights[arm]

    leaves = []
    bins = [[], []]
    unresolved = [(0, total)]
    branch_h = parity_h = walsh = 0
    while unresolved:
        start, size = unresolved.pop()
        arm = next((name for low, high, name in intervals
                    if low <= start and start + size <= high), None)
        if arm is None:
            half = size // 2
            unresolved.extend([(start + half, half), (start, half)])
            branch_h += 1
            continue

        exponent = size.bit_length() - 1
        copies = 1 + exponent % 2
        numerator = 1 << (exponent // 2)
        # A parity H on an early leaf and a fresh zero slot gives two
        # identical positive rows with integral numerator at the same scale.
        parity_h += copies - 1
        leaves.append(dict(start=start, size=size, arm=arm,
                           copies=copies, numerator=numerator))
        for _ in range(copies):
            if arm == "X":
                if numerator % 2:
                    raise ArithmeticError("X Walsh leaf needs an even numerator")
                half = numerator // 2
                walsh += 1
                for eigenvalue in (1, -1):
                    out = int(eigenvalue == signs["X"])
                    bins[out].extend([(half, eigenvalue * half)] * 2)
            else:
                for eigenvalue, row in ((1, (numerator, 0)),
                                        (-1, (0, numerator))):
                    out = int(arm == "hit" or
                              (arm == "Z" and eigenvalue == signs["Z"]))
                    bins[out].append(row)

    # One label H is applied to each input coin rail. Each counted Walsh
    # is one addressed four-mode gate, equivalently four two-mode H gates.
    gates = dict(prefix_label_H=branch_h, parity_label_H=parity_h,
                 addressed_two_mode_H=2 * (branch_h + parity_h),
                 addressed_four_mode_Walsh=walsh,
                 total_if_only_two_mode_H=2 * (branch_h + parity_h) + 4 * walsh)
    for rows, expected in zip(bins, ((3 * scale - 2 * aa, -2 * ab, 3 * scale - 2 * bb),
                                     (scale + 2 * aa, 2 * ab, scale + 2 * bb))):
        gram = (sum(r*r for r, _ in rows), sum(r*l for r, l in rows),
                sum(l*l for _, l in rows))
        if gram != expected:
            raise ArithmeticError(f"bin Gram {gram} differs from {expected}")
    return dict(weights=weights, signs=signs, leaves=leaves, bins=bins, gates=gates)
