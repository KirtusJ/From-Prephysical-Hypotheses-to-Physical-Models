"""Exact physical-coordinate checks for the rotation and early-write experiment."""

from fractions import Fraction as Q
from collections import Counter
from math import comb
from itertools import product


def field(ticks, rail, origin=0):
    sites = [(0, 0)] * 8
    sites[origin] = rail
    for _ in range(ticks):
        sites = [
            (sum(sites[(x - 1) % 8]), sites[(x + 1) % 8][0] - sites[(x + 1) % 8][1])
            for x in range(8)
        ]
    return sites


def norm(pair):
    return sum(a * a for a in pair)


def mass_table(ticks, rail):
    return [Q(norm(pair), 2**ticks * norm(rail)) for pair in field(ticks, rail)]


def require(equality, claim):
    if not equality:
        raise AssertionError(claim)


def physical_rotations():
    for origin in range(8):
        for r, l in [(1, 0), (0, 1)]:
            center = field(2, (r, l), origin)[origin]
            for offset, sign in [(0, -1), (4, 1)]:
                padded = field(4, center, origin)[(origin + offset) % 8]
                require(padded == (2 * sign * r, 2 * sign * l), "six-tick padding column")
            for ticks, direction in [(6, -1), (18, 1)]:
                sites = field(ticks, (r, l), origin)
                scale = 2 ** (ticks // 2 - 2)
                expected = (scale * (3 * r - direction * l), scale * (direction * r + 3 * l))
                require(sites[(origin + 4) % 8] == expected, "antipodal signed column")
                ordinary = (scale * (r + direction * l), scale * (l - direction * r))
                for offset in [0, 2, 6]:
                    sign = -1 if offset == 0 else 1
                    require(sites[(origin + offset) % 8] == tuple(sign * a for a in ordinary),
                            "ordinary signed column")
            sites = field(12, (r, l), origin)
            for offset in range(8):
                sign = 0 if offset % 2 else (-1 if offset == 4 else 1)
                require(sites[(origin + offset) % 8] == (32 * sign * r, 32 * sign * l),
                        "twelve-step identity column")


def rotate(rail, direction):
    r, l = rail
    return 3 * r - direction * l, direction * r + 3 * l


def orbit(n):
    ray = (1, 1)
    for _ in range(abs(n)):
        ray = rotate(ray, 1 if n > 0 else -1)
    return ray


def cubic(w):
    return w * (4 * w - 3) ** 2


def check_menus():
    cos_prev, cos_now = Q(1), Q(4, 5)
    for n in range(1, 41):
        require(mass_table(1, orbit(n))[1] == (1 + cos_now) / 2, "phase convention")
        cos_prev, cos_now = cos_now, Q(8, 5) * cos_now - cos_prev
    half = Q(1, 2)
    for n in range(-32, 33):
        ray = orbit(n)
        w = mass_table(1, ray)[1]
        two = mass_table(2, ray)
        require((two[2], two[0], two[6]) == (w / 2, half, (1 - w) / 2), "two-step refinement")
        for ticks in [6, 18]:
            require(sorted(mass_table(ticks, ray)) == [0]*4 + [Q(1, 8)]*3 + [Q(5, 8)],
                    "input-independent herald masses")
        adjacent = [mass_table(1, rotate(ray, d))[1] for d in [-1, 1]]
        for score, bias in [(lambda x: x, Q(9, 10)), (cubic, Q(81, 250))]:
            require(sum(score(a) for a in adjacent) / 2 ==
                    bias * score(w) + (1 - bias) * score(1 - w), "randomized rotation identity")
    w = mass_table(1, orbit(1))[1]
    coherent_ratio = cubic(w / 2) / cubic(half)
    require((coherent_ratio, cubic(w)) == (Q(162, 125), Q(81, 250)), "cubic rejection")
    require((cubic(Q(3, 4)), cubic(Q(3, 8))) == (0, Q(27, 32)), "cubic zero obstruction")
    def alternate_score(x):
        return Q(1) if x == Q(5, 8) else x

    for n in range(-32, 33):
        w = mass_table(1, orbit(n))[1]
        for mass in (w, 1 - w, w / 2, (1 - w) / 2, half):
            require(alternate_score(mass) == mass, "one-point change on the tested angles")
    q = [alternate_score(w) for w in mass_table(6, (1, 1))]
    require(q[4] / sum(q) == Q(8, 11), "changed six-tick acceptance")
    accepts = ((1, 0), (0, 1))
    for arm, accepted in enumerate(accepts):
        require(sum(accepted) / Q(2) == half, "identical arm acceptance")
        require(sum(bit * a for bit, a in enumerate(accepted)) / Q(sum(accepted)) == arm,
                "different conditional type")


def selection_witness():
    triples = [(1,-1,-1)]*9 + [(1,1,-1)]*9 + [(1,1,1)]*36
    panels = [(0,1,Q(1,10),Q(5,8)), (1,2,Q(1,10),Q(5,8)),
              (0,2,Q(9,25),Q(25,64))]
    for a,b,expected,yield_rate in panels:
        eligible = [j for j,x in enumerate(triples) if (x[a] != x[b]) == (b-a == 1)]
        rejected = set(eligible[:4])
        accepted = [x for j,x in enumerate(triples) if j not in rejected]
        keep = yield_rate / Q(len(accepted),len(triples))
        wrong = sum(x[a] != x[b] for x in accepted)
        require(len(accepted) == 50 and 0 < keep <= 1, "acceptance threshold")
        require(keep * Q(wrong,len(triples)) == yield_rate*expected, "per-launch mismatch")


def recovery_yields(rounds):
    # After the initial positive attempt, r=0 is the only unfinished exponent.
    pending = {0: Q(3,8)}
    yields = [Q(5,8)]
    for _ in range(rounds):
        following = Counter()
        for r, mass in pending.items():
            for hits in range(5):
                new = r + (hits if r < 1 else -hits)
                probability = Q(comb(4,hits)*5**hits*3**(4-hits), 8**4)
                if new != 1:
                    following[new] += mass*probability
        require(set(following) <= {-2,-1,0,2,3,4}, "reachable controller states")
        pending = following
        yields.append(1-sum(pending.values()))
    return yields


def recovered_gate():
    yields = recovery_yields(10)
    require(yields[-2]**2 < Q(25,27) < yields[-1]**2, "two-gate yield")
    q = yields[-1]
    require(q*q*Q(9,25) > 2*(1-q+q*Q(1,10)), "loss-inclusive binary bound")
    win = lambda y: (2*y*Q(9,10) + y*y*Q(9,25))/3
    print("First winning round budget:", next(i for i,y in enumerate(yields) if win(y)>Q(2,3)))
    print("Ten-round unconditional win probability:", float(win(q)))
    return q


def finite_response_grid():
    anchors = {Q(0), Q(1,2), Q(1)}
    rays = [(1,1), (1,0)]
    for depth in range(1,42):
        rays = [rotate(ray,1) for ray in rays]
        for ray in rays:
            w = mass_table(1,ray)[1]
            anchors.update((w,1-w))
        grid = sorted(anchors)
        gap = max(b-a for a,b in zip(grid,grid[1:]))
        require((gap < Q(1,100)) == (depth == 41), "first sub-percent mesh")
    yields = recovery_yields(23)
    require(yields[22]**41 < Q(95,100) < yields[23]**41, "longest panel exposure")
    print("41-rotation mesh and ordinary longest-panel yield:", float(gap), float(yields[23]**41))


def multiwell_control():
    def score(u):
        return u*(1+u*(1-u))

    for n in range(-41,42):
        w = mass_table(1,orbit(n))[1]
        require(score(w)/(score(w)+score(1-w)) == w, "binary control")
        masses = mass_table(2,orbit(n))
        require((masses[0],masses[2],masses[6]) ==
                (Q(1,2),w/2,(1-w)/2), "center and both calibration edges")
    masses = mass_table(2,(1,0))
    require(score(masses[0])/sum(map(score,masses)) == Q(20,39), "multiwell control")


def post_write_probe():
    for n in range(-41,42):
        r,l = orbit(n)
        den = r*r+l*l
        x,z = Q(2*r*l,den), Q(r*r-l*l,den)
        masses = mass_table(3,(r,l))
        actual = tuple(masses[j] for j in (3,5,1,7))
        require(actual == tuple(v/8 for v in (1+x,1-x,3+x+2*z,3-x-2*z)),
                "three-tick conditional histogram")
    coherent = mass_table(3,(1,2))
    dephased = [(a+4*b)/5 for a,b in zip(mass_table(3,(1,0)),mass_table(3,(0,1)))]
    require([40*dephased[j] for j in (3,5,1,7)] == [5,5,9,21], "dephased branch")
    require(sum(abs(a-b) for a,b in zip(coherent,dephased))/2 == Q(1,5), "write disturbance")


def binary_record_game():
    # Any acceptance mask can depend on the hidden signs and the panel.
    maximum = 0
    for x,y,z in product((-1,1), repeat=3):
        wanted = [x == y, y == z, x != z]
        for accepted in product((0,1), repeat=3):
            maximum = max(maximum, sum(a*b for a,b in zip(accepted,wanted)))
    require(maximum == 2, "sharp three-panel game bound")


def next_rotation_challenge():
    low, knot, high = Q(1,4), Q(81,250), Q(9,25)
    def score(x):
        if low < x <= knot:
            return low + (x-low)*(Q(7,20)-low)/(knot-low)
        if knot < x < high:
            return high - (high-x)*(high-Q(7,20))/(high-knot)
        return x

    for n in range(4):
        for ticks in (6,12,18):
            masses = mass_table(ticks,orbit(n))
            require([score(x) for x in masses] == masses, "feedback write changed")
        w = mass_table(1,orbit(n))[1]
        measured = score(w)/(score(w)+score(1-w))
        if n < 3:
            require(measured == w, "calibration rate changed")
        else:
            require((w,measured) == (knot,Q(175,513)), "third rotation missed rival")


def complementary_branch_scores():
    for site in (0,2,4,6):
        p = Q(5,8) if site == 4 else Q(1,8)
        for dephase in (False,True):
            scores = []
            for ray in ((1,0),(0,1),(1,1),(1,-1)):
                target = field(18,ray)[site]
                q = Q(norm(target),2**18*norm(ray))
                r,l = target
                x,z = Q(2*r*l,norm(target)), Q(r*r-l*l,norm(target))
                wells = mass_table(3,target)
                if dephase:
                    wells = [(r*r*a+l*l*b)/norm(target) for a,b in
                             zip(mass_table(3,(1,0)),mass_table(3,(0,1)))]
                observed_x = 4*(wells[3]-wells[5])
                observed_z = 2*(wells[1]-wells[7])-observed_x/2
                scores.append(q*(1+x*observed_x+z*observed_z)/2)
                require(q == p, "unconditional branch yield")
            lower = sum(scores)/2-p
            require(lower == (p/2 if dephase else p), "complementary branch bound")


def shared_sheet_probe(reflect, fixed=False):
    """Propagate integer signed paths on eight wells, two rails and three sheets."""
    state = {(0,1,0): 1}
    ticks = 0
    def step(center, phase, retain):
        nonlocal state,ticks
        following = Counter()
        for (x,rail,y), count in state.items():
            relative = (x-center+4)%8-4
            for direction in (1,-1):
                site = (x+direction)%8
                if retain(site,direction):
                    sign = -1 if rail == direction == -1 else 1
                    shift = int(x in (1,6)) if fixed else phase*relative
                    following[site,direction,(y+shift)%3] += sign*count
        state = following
        ticks += 1
    def excursion():
        step(7,1,lambda x,r: x in (6,0))
        step(7,1,lambda x,r: x == 7)

    for j in range(3):
        step(0,1,lambda x,r: j < 2 or (x,r)==(7,-1))
    require(sum(v*v for v in state.values()) == 2, "dipole source")
    excursion()
    for length,port in (((4,3),(4,7)) if fixed else ((18,3),(6,7))):
        for j in range(length):
            step(0,0,lambda x,r: j+1 < length or x == port)
        if port == 3 and reflect:
            state = {(x,r,(-y)%3): count for (x,r,y),count in state.items()}
    excursion()
    excursion()
    rates = tuple(Q(sum(v*v for (_,r,_),v in state.items() if r==rail),2**ticks)
                  for rail in (1,-1))
    expected = (175,25) if reflect else (25,175)
    if fixed:
        expected = (7,1) if reflect else (1,7)
    require(rates == tuple(Q(n,16384) for n in expected), ("shared-sheet branch probe",rates))
    return rates


def free_sheet_read(ticks, flip):
    numerators = Counter()
    for word in product((1,-1),repeat=ticks):
        x,r,y,sign = 0,1,0,1
        for j,d in enumerate(word):
            if j == flip:
                y = -y
            y = (y+int(x in (1,6)))%3
            sign *= -1 if r==d==-1 else 1
            x,r = (x+d)%8,d
        numerators[x,r,y] += sign
    return tuple(sum(a*a for (x,_,_),a in numerators.items() if x==site)
                 for site in range(8))


def earliest_free_sheet_read():
    for t in range(1,5):
        reference = free_sheet_read(t,None)
        for k in range(t+1):
            actual = free_sheet_read(t,k)
            require(sum(actual)==2**t, "all launches")
            require((actual != reference) == (t==4 and k==2), "first unfiltered reflection")
    require(reference==(6,0,6,0,2,0,2,0), "ordinary free read")
    require(free_sheet_read(4,2)==(4,0,6,0,2,0,4,0), "reflected free read")


def static_inverse_search():
    # The shorter off-diagonal target entry has Eisenstein norm four.
    matches = tested = 0
    for inner in product(range(3), repeat=6):
        shifts = (0,)+inner+(0,)
        if shifts[1] == shifts[7] or shifts[0] == shifts[6]:
            continue
        tested += 1
        columns = []
        for incoming in (1,-1):
            state = Counter({(3,incoming,0):1})
            for _ in range(6):
                later = Counter()
                for (x,r,y),count in state.items():
                    for d in (1,-1):
                        later[(x+d)%8,d,(y+shifts[x])%3] += -count if r==d==-1 else count
                state = later
            for d in (1,-1):
                a,b,c = [state[7,d,y] for y in range(3)]
                columns.append((a-c,b-c))
        units = ((1,0),(0,1),(-1,-1),(-1,0),(0,-1),(1,1))
        matches += any(columns == [(u*v,w*v) for v in (6,-2,2,6)] for u,w in units)
    require((tested,matches)==(324,0), "fixed-shift six-tick inverse control")


if __name__ == "__main__":
    earliest_free_sheet_read()
    static_inverse_search()
    for reflect in (False,True):
        print("Shared-sheet probe, reflection",reflect,shared_sheet_probe(reflect))
        print("Fixed shift, reflection",reflect,shared_sheet_probe(reflect,True))
    complementary_branch_scores()
    post_write_probe()
    multiwell_control()
    finite_response_grid()
    next_rotation_challenge()
    binary_record_game()
    print("Ten recovery rounds, two-gate yield:", float(recovered_gate()**2))
    selection_witness()
    physical_rotations()
    check_menus()
    print("All signed columns at 8 origins and both rail inputs passed.")
    print("65 incident rays passed the two-tick and opposite-rotation comparisons.")
    print("Cubic right-edge/center ratios: coherent 162/125, written 81/250.")
    print("Changing only f(5/8) to 1 gives six-tick acceptance 8/11.")
