"""Exact channels of the signed-routing rail probe, including every null and retry."""
from fractions import Fraction as F
from itertools import product


I = (1, 0, 0, 1)
X = (0, 1, 1, 0)
Z = (1, 0, 0, -1)
S = (1, 1, 1, -1)
BASIS = tuple(tuple(int(i == j) for i in range(4)) for j in range(4))


def mul(a, b):
    return tuple(sum(a[2*i+k]*b[2*k+j] for k in range(2)) for i,j in product(range(2), repeat=2))


def scale(a, x):
    return tuple(x*t for t in a)


def outer_action(operator, matrix):
    return mul(mul(operator, matrix), (operator[0], operator[2], operator[1], operator[3]))


def trace(matrix):
    return matrix[0]+matrix[3]


def raw_branches():
    routes = (I, X, Z, I)
    found = []
    correction = tuple(x-z for x,z in zip(X,Z))  # X H X up to the factor 1/sqrt(2)
    for output in range(4):
        k = tuple(sum((-1)**((output & path).bit_count()) * route[j]
                      for path, route in enumerate(routes)) for j in range(4))
        if output in (1,2):
            k = mul(correction,k)
            assert k in (scale(I,2), scale(I,-2))
            found.append((0,k,F(1,32)))
        else:
            found.append((1 if output==0 else -1,k,F(1,16)))
    return found


def solve(matrix, rhs):
    """Solve the finite matrix renewal equations for four input matrix units."""
    n = len(matrix)
    data = [list(map(F,row+values)) for row,values in zip(matrix,rhs)]
    for col in range(n):
        pivot = next(i for i in range(col,n) if data[i][col])
        data[col],data[pivot] = data[pivot],data[col]
        d = data[col][col]
        data[col] = [v/d for v in data[col]]
        for i in range(n):
            if i!=col and data[i][col]:
                c = data[i][col]
                data[i] = [a-c*b for a,b in zip(data[i],data[col])]
    return [row[n:] for row in data]


def replay(m, branches):
    size = 4*(2*m-1)
    eq = [[int(i==j) for j in range(size)] for i in range(size)]
    rhs = [[0]*4 for _ in range(size)]
    def index(d, r):
        return 4*(d+m-1)+r
    for c,e in enumerate(BASIS):
        rhs[index(0,c)][c] = 1
        for disp,k,weight in branches:
            col = scale(outer_action(k,e),weight)
            for d in range(1-m,m):
                if abs(d+disp)<m:
                    for r in range(4):
                        eq[index(d+disp,r)][index(d,c)] -= col[r]
    visits = solve(eq,rhs)
    # Direct powers of the two successful signed matrices give the
    # closed-form stopped maps; compare their full superoperators to renewal.
    a,b = 1,0
    for _ in range(m):
        a,b = 2*a+2*b, a+2*b
    norm = 2*(a*a+2*b*b)
    gain_over_root_two = F(2*a*b, a*a+2*b*b)
    for disp,k,weight in (branches[0],branches[3]):
        kstop = tuple(a*i+disp*b*s for i,s in zip(I,S))
        for c,e in enumerate(BASIS):
            at_edge = tuple(visits[index(disp*(m-1),r)][c] for r in range(4))
            assert scale(outer_action(k,at_edge),weight) == scale(outer_action(kstop,e),F(1,norm))
    mean = sum((visits[index(d,r)][0]+visits[index(d,r)][3])/2
               for d in range(1-m,m) for r in (0,3))
    assert mean == 2*m*gain_over_root_two
    # Start mixed, keep each tag, apply one fresh raw probe with the grouping
    # (dark, 00, 11 or 01, 10). Correcting a null preserves its probability.
    panels = []
    for tag in (1,-1):
        state = tuple((F(i)+tag*gain_over_root_two*s)/2 for i,s in zip(I,S))
        masses = [weight*trace(outer_action(k,state)) for _,k,weight in branches]
        panel = (0,masses[0],masses[3]+masses[1],masses[2])
        assert sum(panel)==1 and panel[1]==F(3,8)+tag*gain_over_root_two/2
        panels.append(panel)
        # The matching Ramsey port has Kraus (I + tag*sign*S/sqrt(2))/2.
        # Sum the two paths and their cross terms in Q + Q sqrt(2).
        for sign in (1,-1):
            constant = (trace(state) + trace(outer_action(S,state))/2)/4
            radical = tag*sign*(trace(mul(S,state))+trace(mul(state,S)))/8
            assert constant == F(1,2) and radical == sign*gain_over_root_two/2
    print(f"m={m}, eta/sqrt(2)={gain_over_root_two}, mean raw probes={mean}, "
          f"tagged code 1=({panels[0][1]}, {panels[1][1]})")
    return panels


def classify_filters():
    for a,b in ((1,0),(2,1),(3,2),(17,12),(99,70)):
        assert a*a>2*b*b
        paths = 1 << (a+2*b-1).bit_length()
        yield_prob = F(a*a+2*b*b,paths**2)
        assert yield_prob>F(1,12)
        bell_overlap = F()
        for sign in (1,-1):
            slots = [I]*a + [scale(X,sign)]*b + [scale(Z,sign)]*b
            slots += [(0,0,0,0)]*(paths-len(slots))
            accepted = tuple(sum(route[k] for route in slots) for k in range(4))
            assert accepted == tuple(a*i+sign*b*s for i,s in zip(I,S))
            bell_overlap += F(trace(accepted)**2,8*(a*a+2*b*b))
        assert bell_overlap == F(a*a,a*a+2*b*b) > F(1,2)


if __name__ == "__main__":
    branches = raw_branches()
    for m in (1,2,3,4):
        panel = replay(m,branches)
        if m==2:
            assert [p[1] for p in panel]==[F(99,136),F(3,136)]
    classify_filters()
