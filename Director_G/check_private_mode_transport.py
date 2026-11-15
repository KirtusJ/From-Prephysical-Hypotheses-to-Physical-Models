"""Independent exact review of the projected four-step Hadamard walk and hidden modes."""
from collections import Counter, defaultdict
from fractions import Fraction as F
from itertools import product

POS = (-4, -2, 0, 2, 4)
MODES = (F(1, 2), F(25, 146))
PI = (F(55, 128), F(73, 128))
ROWS = {"none": (1, 6, 2, 6, 1), "full": (1, 4, 6, 4, 1),
        "right": (1, 6, 4, 4, 1), "left": (1, 4, 4, 6, 1)}


def signed_words(rail, writes):
    """Pool signed paths with the same physically recorded values before squaring."""
    groups = Counter()
    for steps in product((-1, 1), repeat=4 * len(writes)):
        x = origin = 0
        last = rail
        sign = 1
        record, final = [], []
        for j, step in enumerate(steps):
            if step == last == -1:
                sign = -sign
            last = step
            x += step
            clock = j % 4 + 1
            act = writes[j // 4]
            if clock in (1, 3, 4) or act == "full":
                record.append(x)
            elif act in ("right", "left"):
                target = 2 if act == "right" else -2
                record.append(x == origin + target)
            if clock == 4:
                final.append(x - origin)
                origin = x
        groups[tuple(final), tuple(record), last] += sign
    weights = Counter()
    for (d, _, _), amplitude in groups.items():
        weights[d] += amplitude**2
    return weights


def dist(states, rho, action):
    """Direct (state, absolute displacement) recursion, without moment recurrences."""
    following = defaultdict(F)
    for (i, x), mass in states.items():
        for j, p in enumerate(MODES):
            transition = rho * (i == j) + (1 - rho) * PI[j]
            for d, a, b in zip(POS, ROWS["none"], ROWS[action]):
                following[j, x+d] += mass * transition * ((1-p)*a + p*b) / 16
    return following


def verify_hidden():
    s = sum(w*p for w, p in zip(PI, MODES))
    v = sum(w*(p-s)**2 for w, p in zip(PI, MODES))
    assert (s, v) == (F(5, 16), F(495, 18688))
    for action, rho in product(("full","right","left"), (F(0),F(1,7),F(5,8),F(1))):
        states = {(i, 0): w for i, w in enumerate(PI)}
        for n in range(1, 9):
            states = dist(states, rho, action)
            moments = [sum(p*x**k for (_,x),p in states.items()) for k in range(5)]
            hsum = sum((n-h)*rho**h for h in range(1,n))
            assert moments[0] == 1
            if action == "full":
                V = 5 - s
                assert moments[1:4] == [0,n*V,0]
                assert moments[4] == n*(44-4*s)+3*n*(n-1)*V**2+6*v*hsum
            else:
                assert moments[1] == (1 if action == "left" else -1)*n*s/4
                assert moments[2] - moments[1]**2 == n*(5-s/2-s**2/16)+v*hsum/8


def main():
    for source, first, second in product((-1,1), ROWS, ROWS):
        assert signed_words(source,(first,)) == {(x,): w for x,w in zip(POS,ROWS[first])}
        joint = signed_words(source,(first,second))
        assert joint == {(x,y): u*v for x,u in zip(POS,ROWS[first])
                          for y,v in zip(POS,ROWS[second])}
    verify_hidden()
    print("Pass: 4 kernels, 32 eight-tick sequences (both sharp rails and both sides),"
          " 96 exact finite-n HMM laws. No sampling.")


if __name__ == "__main__":
    main()
