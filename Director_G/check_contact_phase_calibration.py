"""Check the three-tick contact calibration using integer real and imaginary amplitudes."""
from itertools import product

from check_two_coin_contact import score, tensor

Z = [[1, 0], [0, -1]]
J = [[0, -1], [1, 0]]  # Y = iJ
ZZ = tensor(Z, Z)
JJ = tensor(J, J)
ZJ = tensor(Z, J)
JZ = tensor(J, Z)
COINS = list(product(range(2), repeat=2))


def effects(separation, phase, contact_rails=None):
    """Return numerator of the signed effect. Tick t amplitudes have scale (2d)^t."""
    c, s, d = phase
    ends = {}
    for starts in COINS:
        paths = {(0, separation, *starts): (1, 0)}
        for _ in range(3):
            moved = {}
            for (x, z, a, b), (real, imag) in paths.items():
                for u, v in COINS:
                    y, w = x + 1 - 2*u, z + 1 - 2*v
                    hit = y == w and (contact_rails is None or (u, v) == contact_rails)
                    cr, si = (c, s) if hit else (d, 0)
                    sign = (-1)**(a*u + b*v)
                    key = (y, w, u, v)
                    r, i = moved.get(key, (0, 0))
                    moved[key] = (r + sign*(cr*real - si*imag),
                                  i + sign*(si*real + cr*imag))
            paths = moved
        ends[starts] = paths

    signed, norm = [], []
    for left, right in product(COINS, repeat=2):
        rr = ii = total_r = total_i = 0
        for key, (a, b) in ends[left].items():
            x, z, _, _ = key
            c1, d1 = ends[right][key]
            real, imag = a*c1 + b*d1, a*d1 - b*c1
            rr += score(x, z-separation)*real
            ii += score(x, z-separation)*imag
            total_r += real
            total_i += imag
        signed.append((rr, ii))
        norm.append((total_r, total_i))
    scale = (2*d)**6
    if norm != [(scale*int(i == j), 0) for i, j in product(range(4), repeat=2)]:
        raise ValueError("walk isometry")
    return signed, scale


def predicted(separation, phase):
    c, s, d = phase
    terms = []
    for i, j in product(range(4), repeat=2):
        if abs(separation) == 2:
            terms.append(((d+c)*ZZ[i][j] + (d-c)*JJ[i][j],
                          (1 if separation == 2 else -1)*s*(ZJ[i][j]-JZ[i][j])))
        else:
            terms.append((2*d*ZZ[i][j], 0))
    return terms


def main():
    phases = [(1, 0, 1), (-1, 0, 1), (0, 1, 1), (0, -1, 1),
              (3, 4, 5), (3, -4, 5), (-3, 4, 5), (-3, -4, 5)]
    for phase, spacing in product(phases, (-4, -2, 1, 2, 4)):
        actual, scale = effects(spacing, phase)
        target = predicted(spacing, phase)
        if any(8*phase[2]*a != scale*t
               for entry, expected in zip(actual, target) for a, t in zip(entry, expected)):
            raise ValueError((phase, spacing, "signed terminal effect"))
    # Same physical locations, a sign on just one coincident rail pair.
    # Keep every branch and compare its effect with the scalar calibration.
    print("40 phase/spacing panels; normalized and matched every signed effect entry.")
    for spacing, inward in ((2, (0, 1)), (-2, (1, 0))):
        scalar, _ = effects(spacing, (-1, 0, 1))
        free, _ = effects(spacing, (1, 0, 1))
        if scalar == free:
            raise ValueError("controls coincide")
        for rail in COINS:
            selective, _ = effects(spacing, (-1, 0, 1), rail)
            if selective != (scalar if rail == inward else free):
                raise ValueError((spacing, rail, "selective sign"))
        print(f"At separation {spacing}, only rail {inward} matches the scalar sign.")


if __name__ == "__main__":
    main()
