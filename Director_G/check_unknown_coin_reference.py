"""Two-column transfer of four coherent helper arms to a compact Pauli reference."""
import argparse
import json
from fractions import Fraction as Q
from hashlib import sha256
from pathlib import Path

from check_two_column_transport import (
    certify, check, diag, gram, inverse, midpoint, minus, positive, times, walk, zeros,
)
from walk_analyzer_reference import analyzer_reference
from unknown_coin_rates import rate_controls


def axis_inverse(rows):
    """Pick exact dyadic pivot rows independently for the two retained source rails."""
    answer = zeros(len(rows))
    pivots = []
    for i in range(2):
        p = next((j for j, row in enumerate(rows)
                  if row[1-i] == 0 and abs(row[i]) > 0 and abs(row[i]) & (abs(row[i])-1) == 0), None)
        check(p is not None, "target needs an axis-only power-of-two row for each coin input")
        answer[p][i] = Q(1, rows[p][i])
        pivots.append([p, rows[p][i]])
    check(gram(rows, answer) == diag(1), "target inverse on actual output rows")
    return answer, pivots


def from_rows(rows):
    return gram(rows, rows) if rows else diag(0)


def frame_sha(z):
    data = json.dumps(z, default=str, separators=(",", ":")).encode()
    return sha256(data).hexdigest()


def run_panel(ticks, chosen):
    s = 1 << ticks
    blocks = walk(ticks)
    check(set(chosen) <= blocks.keys(), "chosen sites must be present at this clock")
    full = [r for site in sorted(blocks) for r in blocks[site]]
    check(gram(full, full) == diag(s), "full two-input flight isometry")
    parts = [[r for site in sorted(blocks) if int(site in chosen) == i for r in blocks[site]]
             for i in range(2)]
    effect = from_rows(parts[1])
    aa, ab, bb = effect[0][0], effect[0][1], effect[1][1]
    ref = analyzer_reference((aa, ab, bb), s)
    bins = []
    for outcome in range(2):
        # In each protected sector the matching forced arm contains all original rows.
        src = full+parts[outcome]+parts[outcome]
        dst = ref["bins"][outcome]
        h = gram(src, src)
        part_gram = from_rows(parts[outcome])
        expected = [[s+2*part_gram[0][0], 2*part_gram[0][1]],
                    [2*part_gram[1][0], s+2*part_gram[1][1]]]
        check(h == expected == gram(dst, dst), "shared flag-sector Gram")
        right_x = [[Q(a, s), Q(b, s)] for a, b in full]+zeros(2*len(parts[outcome]))
        check(gram(src, right_x) == diag(1), "full-flight inverse survives the two copies")
        right_y, pivots = axis_inverse(dst)
        cross = minus(h, diag(s))
        ideal_slack = minus(h, times(times(cross, times(inverse(h), cross)), diag(2)))
        check(positive(ideal_slack), "strictly positive slack at delta=S")
        z, grid, residual = midpoint(src, dst, s, digit_padding=True,
                                     right_x=right_x, right_y=right_y)
        replay = certify(src, dst, z, s)
        bins.append(dict(flag=outcome, gram=h, source_rows=len(src), reference_rows=len(dst),
                         target_pivots=pivots, ideal_slack=ideal_slack, rounding_grid=grid,
                         exact_slack=residual, padded_slots=replay["slots"],
                         reflection_gates=replay["gates_per_reflection"],
                         midpoint_rows=len(z), midpoint_sha256=frame_sha(z),
                         both_original_columns_reversed=replay["all_columns_reversed"]))
    return dict(ticks=ticks, sites=sorted(chosen), scale=s, effect=[aa,ab,bb],
                analyzer_weights=ref["weights"], analyzer_signs=ref["signs"],
                emitted_leaves=ref["leaves"], preparation_gates=ref["gates"], bins=bins)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    output = parser.parse_args().output
    cases = {
        "empty_0": (0, []), "full_0": (0,[0]),
        "plus_one_3": (3,[1]), "minus_one_3": (3,[-1]), "mirror_3": (3,[-1,1]),
        "plus_three_7": (7,[3]), "nonnegative_12": (12,list(range(0,13,2))),
    }
    panels = {label:run_panel(t, chosen) for label,(t,chosen) in cases.items()}
    p, m = panels["plus_one_3"], panels["minus_one_3"]
    check(p["effect"] == [5,1,1] and m["effect"] == [1,-1,5], "two signed three-tick effects")
    check(p["analyzer_weights"] == m["analyzer_weights"]
          and p["analyzer_signs"] == {"X":1,"Z":1} and m["analyzer_signs"] == {"X":-1,"Z":-1},
          "opposite named signs, identical mixture weights")
    check(panels["mirror_3"]["effect"] == [6,0,6], "unknown coin scalar shell")
    check(panels["nonnegative_12"]["effect"][1] != 0, "nontrivial twelve-tick cross term")
    controls = rate_controls()
    source_rows = [r["input_numerators"] for r in controls["signed_endpoints"] if r["site"] == 1]
    check(gram(source_rows, source_rows) == [[5, 1], [1, 1]], "independent rate-control walk")
    output.mkdir()
    (output/"unknown_coin_reference.json").write_bytes(
        (json.dumps(dict(panels=panels, rate_controls=controls,
                         scale_convention="integer rows divided by sqrt(4S)"),
                    default=str, indent=2)+"\n").encode()
    )


if __name__ == "__main__":
    main()
