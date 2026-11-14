"""Exact Q(sqrt(2)) checks for the three-word real-embedding comparison."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
try:
    import addressed_write_test as walk
finally:
    sys.path.pop(0)


def require(condition, message):
    if not condition:
        raise ArithmeticError(message)


def conjugate(x):
    return (x[0], -x[1])


def greater(x, y):
    return walk.sign(walk.sub(x, y)) > 0


def main():
    weights = walk.ordinary_word_weights()
    require(weights == walk.enumerate_paths(walk.circuit()), "path replay mismatch")
    occupied = {word: w for word, w in weights.items() if w != walk.ZERO}
    require(len(occupied) == 27, "occupied word count")
    require(all(greater(w, walk.ZERO) and greater(conjugate(w), walk.ZERO)
                for w in occupied.values()), "support differs between embeddings")
    prefix_mass = {}
    for word, weight in occupied.items():
        for length in range(4):
            prefix = word[:length]
            prefix_mass[prefix] = walk.add(prefix_mass.get(prefix, walk.ZERO), weight)
    require(prefix_mass[()] == (512, 0), "total mass")
    require(all(len({w for h, w in prefix_mass.items() if h[:-1] == p and h})
                == 3 for p in prefix_mass if len(p) < 3),
            "canonical sibling values are not all distinct")

    chosen = (2, 3, 1)
    for d in (1, 2):
        prefix = chosen[:d]
        siblings = [v for k, v in prefix_mass.items()
                    if len(k) == d and k[:-1] == prefix[:-1] and k != prefix]
        require(len(siblings) == 2, "prefix support count")
        require(all(greater(conjugate(prefix_mass[prefix]), conjugate(v)) for v in siblings),
                "selected prefix is not the unique conjugate maximum")
    require(all(greater(conjugate(occupied[chosen]), conjugate(v))
                for w, v in occupied.items() if w != chosen),
            "selected leaf is not the unique global conjugate maximum")
    l, m, h = (occupied[(2, 3, j)] for j in (1, 3, 0))
    require((l, m, h) == ((86, -60), (18, -8), (40, 4)), "selected masses")
    require(greater(h, m) and greater(m, l), "canonical ordering")
    require(greater(conjugate(l), conjugate(h)) and greater(conjugate(l), conjugate(m)),
            "conjugate maximum changed")
    require(greater(walk.mul(l, h), walk.mul(m, m)), "theta < 1/2 not verified")
    require(greater(m, walk.add(l, l)), "positive lower bound not verified")
    # In either model at least 1/27 of conjugate launches reach the selected
    # leaf, which is more probable than its negative-score sibling.
    gap = walk.sub(walk.divide(walk.ONE, walk.add(l, l)), walk.divide(walk.ONE, m))
    bound = walk.divide(gap, (27, 0))
    require(greater(bound, walk.divide((1, 0), (100, 0))), "population bound <= 0.01")
    parent_mass = prefix_mass[(2, 3)]
    require(parent_mass == walk.mul((8, 0), m), "conditional middle coefficient")
    require(greater(parent_mass, walk.mul((43, 0), l)), "conditional gap lower bound")
    require(greater(walk.mul(parent_mass, bound), walk.divide((1, 0), (2, 0))),
            "conditional-weight per-conjugate-launch bound <= 1/2")
    print("Verified all 27 positive leaves, both conjugate prefix maxima, "
          "the unique global maximum, raw gap > 1/100 and analyzer-scaled gap > 1/2.")


if __name__ == "__main__":
    main()
