"""Integer replay for two forward walks and a shared F5 record."""
import argparse
from collections import defaultdict
from fractions import Fraction
from itertools import product
import json
from pathlib import Path


RESULT = Path(__file__).with_name("results") / "two_walk_memory.json"
MODES = ("coherent", "first_copy", "reset")
MASK = {-3: 1, -1: -1, 1: 1, 3: -1}


def one_particle_rows(ticks):
    """Labeled paths from the two first-hop outputs, with integer amplitudes."""
    modes = defaultdict(lambda: [0, 0])
    for incoming in (0, 1):
        for word in product((0, 1), repeat=ticks):
            site = 1 if incoming == 0 else -1
            rail, sign = incoming, 1
            for step in word:
                if rail == step == 1:
                    sign = -sign
                site += 1 if step == 0 else -1
                rail = step
            modes[site, rail][incoming] += sign
    effects = defaultdict(lambda: [0, 0, 0])
    for (site, _), (a, b) in modes.items():
        effect = effects[site]
        effect[0] += a*a
        effect[1] += a*b
        effect[2] += b*b
    return dict(sorted(effects.items()))


def advance(state):
    """One simultaneous tick of the two separate physical walks."""
    nxt = defaultdict(int)
    for (x, a, y, b, memory, env), amplitude in state.items():
        for da, db in product((0, 1), repeat=2):
            xp = x + (1 if da == 0 else -1)
            yp = y + (1 if db == 0 else -1)
            flip = (a == da == 1) != (b == db == 1)
            nxt[xp, da, yp, db, memory, env] += -amplitude if flip else amplitude
    return nxt


def prepare(mode):
    # One free forward tick at each right-rail source.
    paths = advance({(0, 0, 0, 0, 0, 0): 1})
    state = defaultdict(int)
    for (x, a, y, b, _, _), amplitude in paths.items():
        first_write = int(a == 0)
        env = first_write if mode in ("first_copy", "reset") else 0
        memory = 0 if mode == "reset" else first_write
        memory = (memory + int(b == 0) - 1) % 5
        state[x, a, y, b, memory, env] += amplitude
    return state


def measure(state, ticks):
    # Codes in ascending order (++,+-,-+,--) with all trials included.
    rows = [[0] * 4 for _ in (0, 1)]
    for (x, _, y, _, memory, _), amplitude in state.items():
        sx, sy = (MASK[x], MASK[y]) if ticks == 3 else (x, y)
        index = 2*int(sx < 0) + int(sy < 0)
        rows[int(memory != 0)][index] += amplitude**2
    denominator = 4**ticks
    assert sum(map(sum, rows)) == denominator
    p, q, r, s = rows[0]
    return {"denominator": denominator, "success_sign_pairs": rows[0],
            "failure_sign_pairs": rows[1],
            "herald_probability": str(Fraction(sum(rows[0]), denominator)),
            "success_weighted_correlation": str(Fraction(p-q-r+s, denominator))}


def simulate(mode):
    state = prepare(mode)
    direct = measure(state, 1)
    delayed = measure(advance(advance(state)), 3)
    assert direct["herald_probability"] == delayed["herald_probability"] == "1/2"
    value = (Fraction(delayed["success_weighted_correlation"])
             - Fraction(direct["success_weighted_correlation"]))
    return {"immediate": direct, "delayed": delayed, "score": str(value)}


def report():
    panel = {mode: simulate(mode) for mode in MODES}
    assert [panel[m]["score"] for m in MODES] == ["5/8", "1/2", "0"]
    effects = [one_particle_rows(tick) for tick in (0, 1, 2)]
    assert all(cross == 0 for clock in effects[:2] for _, cross, _ in clock.values())
    assert list(effects[2].values()) == [[0, 0, 1], [1, -1, 2], [2, 1, 1], [1, 0, 0]]
    signs = {mask: [sum(sign*row[i] for sign, row in zip(mask, effects[2].values()))
                    for i in range(3)] for mask in product((-1, 1), repeat=4)}
    assert signs[tuple(MASK.values())] == [0, 2, 0]
    assert max(abs(row[1]) for row in signs.values()) == 2
    # Compare the tensor-product effect prediction with independent joint evolution.
    for mode in MODES:
        z_corr = -Fraction(1, 2) if mode != "reset" else 0
        mask_corr = Fraction(1, 8) if mode == "coherent" else 0
        assert Fraction(panel[mode]["immediate"]["success_weighted_correlation"]) == z_corr
        assert Fraction(panel[mode]["delayed"]["success_weighted_correlation"]) == mask_corr
    return {"one_walk_gram_rows_RR_RL_LL": [{str(x): row for x, row in e.items()} for e in effects],
            "two_tick_mask_grams": [{"site_signs": list(s), "gram": g} for s,g in signs.items()],
            "effect_denominators": [1, 2, 4], "joint_pair_order": ["++", "+-", "-+", "--"],
            "models": panel}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--write", action="store_true", help="replace the stored result")
    args = p.parse_args()
    answer = json.dumps(report(), indent=2) + "\n"
    if args.write:
        RESULT.write_bytes(answer.encode("utf-8"))
    else:
        assert RESULT.read_bytes() == answer.encode("utf-8")
        print("Checked both flags, both clocks, three memory dynamics, and all site masks.")


if __name__ == "__main__":
    main()
