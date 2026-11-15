"""Replay the addressed spatial splitter with exact signed dyadic amplitudes.

Usage: python -I -B check_track_resolution.py
Runs every physical tick of both k=2 schedules, including the long translation.
At k=3,4 it checks every splitting pulse and proves that the intervening
ballistic paths cannot collide by testing their complete swept intervals.
No data files are written.
"""
from fractions import Fraction


def require(condition, label):
    if not condition:
        raise ArithmeticError(label)


def fractions(k, thin_outside, literal=False):
    depth = k + k*k
    span = (1 << depth) - 1
    run = span * span
    # One state per occupied site at the start of each pulse.
    # Each value is (direction, amplitude sign, power-of-two mass exponent,
    #                  all first k direction choices point right).
    state = {0: (1, 1, 0, True)}
    for j in range(1, depth + 1):
        length = 1 << (depth - j)
        previous = None
        endpoints = {}
        for site, (rail, sign, exponent, outside) in sorted(state.items()):
            split = j <= k or outside == thin_outside
            directions = (-1, 1) if split else (rail,)
            # Every descendant of even an unsplit parent stays inside this
            # closed interval until the next pulse. Different parent cones
            # must be disjoint at *every* intervening physical time.
            if previous is not None:
                require(previous < site-length, "overlapping parent cones")
            previous = site+length
            for direction in directions:
                target = site + direction*length
                require(target not in endpoints, "colliding pulse outputs")
                minus = split and rail == direction == -1
                endpoints[target] = (direction, -sign if minus else sign,
                                     exponent + int(split),
                                     outside and (j > k or direction == 1))
        if literal:
            # Direct coin-and-stream propagation, without using the endpoint
            # shortcut. Same-site rail collisions are checked before each tick.
            direct = state
            for step in range(length):
                walked = {}
                for site, (rail, sign, exponent, outside) in direct.items():
                    split = step == 0 and (j <= k or outside == thin_outside)
                    for direction in ((-1, 1) if split else (rail,)):
                        target = site + direction
                        require(target not in walked, "two paths on a split-stage site")
                        minus = split and rail == direction == -1
                        walked[target] = (direction, -sign if minus else sign,
                                          exponent + int(split),
                                          outside and (step != 0 or j > k or direction == 1))
                direct = walked
            require(direct == endpoints, "direct ticks disagree with pulse endpoints")
        state = endpoints

    terminal = {}
    for site, (_, sign, exponent, outside) in state.items():
        direction = 1 if outside else -1
        target = site + direction*run
        require(target not in terminal, "final positions coincide")
        require(abs(target - direction*run) <= span, "outside assigned interval")
        terminal[target] = (direction, sign, exponent, outside)
    if literal:
        # At a crossing, I sends each direction onward unchanged. Distinct
        # rail keys at a site are valid. Merging into the same rail is not.
        moving = {(x, 1 if outside else -1): (sign, exponent, outside)
                  for x, (_, sign, exponent, outside) in state.items()}
        for _ in range(run):
            walked = {(x+r, r): payload for (x, r), payload in moving.items()}
            require(len(walked) == len(moving), "same-rail collision during translation")
            moving = walked
        require({x: (r, *data) for (x, r), data in moving.items()} == terminal,
                "direct translation disagrees with endpoint calculation")

    counts = {}
    for _, sign, exponent, outside in terminal.values():
        require(sign in (-1, 1), "invalid amplitude sign")
        counts[outside, exponent] = counts.get((outside, exponent), 0) + 1
    mass = {o: sum(Fraction(n, 1 << e) for (side, e), n in counts.items() if side == o)
            for o in (True, False)}
    m = 1 << k
    require(mass[True] == Fraction(1, m) and sum(mass.values()) == 1,
            "ordinary terminal mass")
    # All exponents are multiples of k, hence applying q=(k±1)/k
    # gives integer exponents and permits an entirely rational comparison.
    numerator = k-1 if thin_outside else k+1
    require(all((e*numerator) % k == 0 for _, e in counts), "fractional dyadic exponent")
    scores = {o: sum(Fraction(n, 1 << (e*numerator//k))
                     for (side, e), n in counts.items() if side == o)
              for o in (True, False)}
    measured = scores[True]/sum(scores.values())
    require(measured == Fraction(m, 2*m-1), "powered terminal leakage")
    return len(terminal), mass[True], measured


if __name__ == "__main__":
    for k in (2, 3, 4):
        for thin_outside in (False, True):
            sites, ordinary, powered = fractions(k, thin_outside, literal=(k == 2))
            shift = "-" if thin_outside else "+"
            print(f"k={k} q=1{shift}1/{k}: wells={sites}, ordinary={ordinary}, powered={powered}")
