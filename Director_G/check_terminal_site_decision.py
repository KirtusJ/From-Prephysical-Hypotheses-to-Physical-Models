"""Exact terminal-site identities and the native four-tick ring instrument."""

from fractions import Fraction
from itertools import product

IDENTITY = (1, 0, 0, 1)


def tick(columns, a, b, period=None):
    """Apply the integer coin [[a,b],[b,-a]], then stream the two rows."""
    result = {}
    for x, (r0, r1, l0, l1) in columns.items():
        right, left = x + 1, x - 1
        if period is not None:
            right, left = right % period, left % period
        row = result.setdefault(right, [0, 0, 0, 0])
        row[0] += a*r0 + b*l0
        row[1] += a*r1 + b*l1
        row = result.setdefault(left, [0, 0, 0, 0])
        row[2] += b*r0 - a*l0
        row[3] += b*r1 - a*l1
    return {x: tuple(rows) for x, rows in result.items()}


def effect(k):
    a, b, c, d = k
    return a*a+c*c, a*b+c*d, b*b+d*d


def signed_sites(a, b, horizon):
    state = {0: IDENTITY}
    norm_squared = a*a+b*b
    checked = 0
    for t in range(1, horizon+1):
        state = tick(state, a, b)
        total = [0, 0, 0]
        for x, matrix in state.items():
            r, cross, l = effect(matrix)
            trace = matrix[0]+matrix[3]
            contrast = a*(r-l)+2*b*cross
            assert t*(matrix[0]-matrix[3]) == x*trace, (a,b,t,x)
            assert t*a*contrast == x*norm_squared*trace**2, (a,b,t,x)
            if a == 0:
                assert contrast == 0
            for i, value in enumerate((r, cross, l)):
                total[i] += value
            checked += 1
        assert total == [norm_squared**t, 0, norm_squared**t]
    return checked


def multiply(left, right):
    a,b,c,d = left
    e,f,g,h = right
    return a*e+b*g, a*f+b*h, c*e+d*g, c*f+d*h


def ring_and_line():
    # Arrivals below are scaled by four. Check both columns at every start.
    targets = {0: (-1,-1,1,-1), 2: (3,1,1,1),
               4: (1,1,-1,1), 6: (1,-1,-1,3)}
    null_inverse = (1,-1,1,1)  # HZ times sqrt(2)
    for start in range(8):
        state = {start: IDENTITY}
        for _ in range(4):
            state = tick(state, 1, 1, 8)
        assert state == {(start+x)%8: k for x,k in targets.items()}
    assert multiply(null_inverse,targets[0]) == (-2,0,0,-2)
    assert multiply(null_inverse,targets[4]) == (2,0,0,2)
    line = {0: IDENTITY}
    for _ in range(3):
        line = tick(line,1,1)
    assert {x: effect(k) for x, k in line.items()} == {
        -3: (1,-1,1), -1: (1,-1,5), 1: (5,1,1), 3: (1,1,1)
    }
    line = tick(line,1,1)
    assert tuple(a+b for a,b in zip(line[-4],line[4])) == targets[4]
    # An X+ input reaches the right extreme only, whereas a sharp R
    # retains both components of the coherent antipodal output.
    right_input = (1,0)
    folded = (targets[4][0],targets[4][2])
    assert folded == (1,-1)
    undone = (folded[0]-folded[1], folded[0]+folded[1])
    assert undone == (2*right_input[0],2*right_input[1])
    assert line[-4][0] == line[4][2] == 0
    assert abs(line[-4][2]) == abs(line[4][0]) == 1
    # No intermediate pulse. Compare the two-write joint probabilities
    # on sharp R, before any conditioning on the first outer result.
    ring_word = multiply(targets[2], targets[4])
    line_words = [multiply(line[2], line[x]) for x in (-4, 4)]
    assert Fraction(effect(ring_word)[0], 4**4) == Fraction(1, 64)
    assert Fraction(sum(effect(k)[0] for k in line_words), 4**4) == Fraction(3, 64)
    # Fixed m=2, no corrections, retain the same informative sign twice.
    for bits in product((2,6), repeat=2):
        matrix = multiply(targets[bits[1]],targets[bits[0]])
        r,_,l = effect(matrix)
        rate = Fraction(r+l, 2*4**4)
        assert rate == (Fraction(17,64) if bits[0] == bits[1] else Fraction(1,64))
    fifth = tick(line,1,1)
    plus,minus = {},{}
    for x,matrix in fifth.items():
        r,c,l = effect(matrix)
        for sign, law in ((1,plus),(-1,minus)):
            law[x] = Fraction(3*(r+l) + sign*2*(r-l+2*c), 6*2**5)
    def best(groups, prior):
        return sum(max(prior*sum(plus[x] for x in group),
                       (1-prior)*sum(minus[x] for x in group)) for group in groups)
    full = [[x] for x in fifth]
    side = [[x for x in fifth if x<0], [x for x in fifth if x>0]]
    assert best(full,Fraction(1,2)) == best(side,Fraction(1,2)) == Fraction(5,6)
    assert best(full,Fraction(1,10)) == Fraction(15,16)
    assert best(side,Fraction(1,10)) == Fraction(9,10)


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Run without -O so that exact assertions are checked.")
    cases = [(1,1,400),(3,4,75),(-5,12,75),(4,-3,75),(1,0,75),(0,1,75)]
    for a,b,t in cases:
        print(f"coin ({a},{b}), ticks 1..{t}: {signed_sites(a,b,t)} site identities")
    ring_and_line()
    print("All eight ring launches, both raw nulls, line control, two-block words and prior tests passed.")
