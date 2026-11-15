"""Exact physical-coordinate checks for the rotation and early-write experiment."""

from fractions import Fraction as Q


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


if __name__ == "__main__":
    selection_witness()
    physical_rotations()
    check_menus()
    print("All signed columns at 8 origins and both rail inputs passed.")
    print("65 incident rays passed the two-tick and opposite-rotation comparisons.")
    print("Cubic right-edge/center ratios: coherent 162/125, written 81/250.")
    print("Changing only f(5/8) to 1 gives six-tick acceptance 8/11.")
