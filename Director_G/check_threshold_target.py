"""Exact checks for the hidden threshold between two routed masses."""
import json
from fractions import Fraction as Q
from pathlib import Path


def main():
    menu = json.loads((Path(__file__).parent / "results/echo_probability_map.json").read_text())["finite_menu"]
    den = int(menu["mass_denominator"])
    left = {Q(int(item["numerator"]), den) for item in menu["routed_left_half_masks"]}
    nodes = sorted(left | {1 - x for x in left} | {Q(1, 2)})
    h, a, b = max((y - x, x, y) for x, y in zip(nodes, nodes[1:]) if y <= Q(1, 2))
    assert h == max(y - x for x, y in zip(nodes, nodes[1:]))
    assert len(nodes) == 67 and a < Q(1, 4) < b
    mid = (a + b) / 2

    # Midpoint quadrature integrates affine functions exactly on each side of the midpoint.
    n = 64
    targets = []
    first = {s: Q(0) for s in [a + h*i/n for i in range(n+1)]}
    paired = Q(0)
    for i in range(n):
        t = a + h * Q(2*i+1, 2*n)

        def response(s):
            if s > Q(1, 2):
                return 1-response(1-s)
            if not a < s < b:
                return s
            return b if s > t or (s == t and t <= mid) else a

        assert all(response(x) == x for x in nodes)
        for s in first:
            first[s] += response(s)/n
        target = t if t <= mid else 1-t
        targets.append(response(target)-target)
        paired += (response(mid)-mid)**2/n
    assert all(first[s] == s for s in first)
    assert sum(targets)/n == 3*h/4
    assert paired == h*h/4
    for name, value in [('left', a), ('right', b), ('gap', h), ('selected_bias', 3*h/4), ('midpoint_pair_score', paired)]:
        print(f"{name}: {value} ({float(value):.12g})")


if __name__ == "__main__":
    main()
