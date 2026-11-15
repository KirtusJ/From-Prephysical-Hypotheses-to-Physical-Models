"""Exact nine-qubit effects for the 4:2:1 anchored herald and return.

    python -I -B -O check_anchored_herald.py

q0 is rail, q1 idle/acted, q2,q3 the two path bits, q4 rejection,
and q5 the protected fair Pell choice. W is the n=2 coherent circuit of
check_heralded_gate_reference.py. Three additional fresh fair bits produce
one final five-way write. All tag coordinates in a cell are pooled before
scoring. The reversed, protected W uses the original six qubits; the hidden
copy in the Lüders arm is inaccessible. A retained, then erased, copy is a
separate control. This checker computes predicted effects on all inputs.
"""

from fractions import Fraction as F


def require(ok, name):
    if not ok:
        raise ArithmeticError(name)


def sign(bit_count):
    return 1-2*(bit_count % 2)


def unitary():
    """Integer numerators of all 64x64 entries of W; divide by sqrt(32)."""
    out = [[0]*64 for _ in range(64)]
    for src in range(64):
        rail, control = src & 1, (src >> 1) & 1
        initial_path, flag, old_branch = (src >> 2) & 3, (src >> 4) & 1, src >> 5
        for branch, (a, b) in enumerate(((1,1),(3,2))):
            for path in range(4):
                # W applies H to branch and both path bits, does the
                # reversible signed routing, then Hadamards both path bits.
                flip = control and b <= path < 2*b
                reject = path >= (2*b if control else a)
                zphase = control and path < b and rail
                for final_path in range(4):
                    dst = ((branch << 5) | ((flag ^ reject) << 4) | (final_path << 2)
                           | (control << 1) | (rail ^ flip))
                    phases = (old_branch*branch + zphase
                              + ((initial_path ^ final_path) & path).bit_count())
                    out[dst][src] += sign(phases)
    for i in range(64):
        for j in range(i+1):
            require(sum(row[i]*row[j] for row in out) == 32*(i == j), "unitary columns")
    return out


def herald(index):
    return index & 0b11100 == 0  # q4 rejection cleared and q3:q2 = 00


def returned(index):
    return index < 4             # four protected ancillas q2 through q5 are zero


def after_inverse(W, selected):
    # W times a blank-ancilla input, cut projection, then W transpose on
    # the trusted six only. Rows cover all 64 final trusted coordinates;
    # the four columns span arbitrary input rail and control states.
    rows = [row for i,row in enumerate(W) if selected(i)]
    return [[sum(row[i]*row[j] for row in rows) for j in range(4)] for i in range(64)]


def five_effects(branches, denominator, signal):
    # Every tag has ordinary squared amplitude 1/8. Unresolved external
    # labels distinguish the branches, which therefore add as effects.
    pieces = [[[0]*4 for _ in range(4)] for _ in range(5)]
    for table in branches:
        for coordinate, row in enumerate(table):
            for tag in range(8):
                if tag < 4:
                    cell = 0
                elif tag < 6:
                    cell = 1
                elif tag == 6:
                    cell = 2
                else:
                    cell = 3 if signal(coordinate) else 4
                for i in range(4):
                    for j in range(4):
                        pieces[cell][i][j] += row[i]*row[j]
    masses = []
    for effect in pieces:
        weight = effect[0][0]
        require(all(effect[i][j] == weight*(i == j) for i in range(4) for j in range(4)),
                "every cell acts as a scalar on the input")
        masses.append(F(weight, 8*denominator))
    require(sum(masses) == 1, "all launches recorded")
    return tuple(masses)


def expected(w):
    return F(1,2), F(1,4), F(1,8), w/8, (1-w)/8


def check_physical():
    W = unitary()
    source = [row[:4] for row in W]
    copied = (after_inverse(W,herald), after_inverse(W,lambda i: not herald(i)))
    # With the tag erased before reversal the two projected amplitudes add
    # coherently. Holding the tag inaccessible adds their two Gram matrices.
    erased = [[a+b for a,b in zip(r,s)] for r,s in zip(*copied)]
    intact = after_inverse(W, lambda _: True)
    require(erased == intact, "access to erase the external label restores the intact amplitude")
    cases = (("direct", [source], 32, herald, F(5,16)),
             ("intact return", [intact], 32**2, returned, F(1)),
             ("unread herald return", copied, 32**2, returned, F(73,128)),
             ("erased-copy return", [erased], 32**2, returned, F(1)))
    for label, branches, denominator, signal, w in cases:
        table = five_effects(branches, denominator, signal)
        require(table == expected(w), label)
        print(f"{label}: w={w}; H M L signal failure =", *(str(x) for x in table))


def escort(weights, q):
    # Zero and negative exponents operate on positive support only.
    unnormalized = [x**q if x else F(0) for x in weights]
    return tuple(x/sum(unnormalized) for x in unnormalized)


def contrast(table):
    H, M, L = table[:3]
    return H-4*M+4*L


def check_score():
    for w in (F(0), F(1), F(1,2), F(5,16), F(73,128), F(1,3)):
        weights = (F(4), F(2), F(1), w, 1-w)
        for q in (-7,-1,0,1,2,9):
            table = escort(weights,q)
            z = sum(x**q for x in weights if x)
            # For all finite real q the three numerators are t²,t,1 for
            # t=2^q>0. The numerator (t-2)^2 vanishes exactly at q=1.
            require(contrast(table)*z == (F(2)**q-2)**2, "finite contrast")
            require((contrast(table) == 0) == (q == 1), "finite equality")
            if q == 1:
                require(table == expected(w), "finite contact has H=1/2")
        # Enumerate every extreme tie choice, including the L versus unit-
        # weight signal tie when w is sharp. Mixtures preserve the score.
        for extreme in (max(weights), min(x for x in weights if x)):
            for i, weight in enumerate(weights):
                if weight == extreme:
                    point = tuple(F(i==j) for j in range(5))
                    require(contrast(point) >= 0, "extreme contrast")
                    if not contrast(point):
                        require(point[0] == 0 and i in (3,4), "extreme zero has H=0")
    print("Finite contrast (2^q-2)^2/Z; every signed-infinite zero has H=0.")


def check_nested():
    w = F(73,128)
    # An ordinary outer write of H/M/L/science, followed by a separate
    # maximum-power science read. w>1/2 makes every science outcome pass.
    outer = escort((F(4),F(2),F(1),F(1)), 1)
    inner = (w,1-w)
    maxima = tuple(F(mass == max(inner)) for mass in inner)
    nested = outer[:3] + tuple(outer[3]*n/sum(maxima) for n in maxima)
    require(nested == expected(F(1)), "hidden-return counterfeit")
    # A finite nested counterfeit of the *ordinary dephased* five-cell
    # table also exists: use 0 or 2, never 1, at the science binary read.
    prob_zero = 2*w*(1-w)
    apparent = prob_zero/2 + (1-prob_zero)*w*w/(w*w+(1-w)**2)
    require(apparent == w, "finite nested counterfeit")
    print(f"Ordinary outer routing plus inner maximum makes w={w} appear perfect. "
          f"Inner q=0 with weight {prob_zero} and q=2 otherwise gives the ordinary dephased table.")


if __name__ == "__main__":
    check_physical()
    check_score()
    check_nested()
