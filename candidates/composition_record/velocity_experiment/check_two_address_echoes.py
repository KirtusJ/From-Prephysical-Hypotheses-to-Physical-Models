"""Verify the two-address echoes exactly by phase-tagged signed path sums.

Each amplitude is a polynomial in eta_A, eta_B scaled by (sqrt(2))^-d,
where d is the total tick count. Coefficients are elements of Z[sqrt(2)].
Probability polynomials are Laurent polynomials since each eta has modulus 1.
Only Python's standard library is needed. No files are written.
"""
from itertools import product


def require(condition, message):
    if not condition:
        raise ArithmeticError(message)


def add_poly(poly, key, pair):
    a, b = poly.get(key, (0, 0))
    x, y = a+pair[0], b+pair[1]
    if x or y:
        poly[key] = (x, y)
    else:
        poly.pop(key, None)


def multiply(u, v):
    a, b = u
    c, d = v
    return a*c+2*b*d, a*d+b*c


def paths(schedule, marks):
    # Brute-force all proposed L/R steps, including those killed by I or X.
    amplitudes = {}
    for moves in product((0, 1), repeat=len(schedule)):
        left_count = physical = rail = a_power = b_power = 0
        coeff = (1, 0)
        word = []
        for t, (gate, output) in enumerate(zip(schedule, moves), start=1):
            y = left_count % 2
            if gate in "AB":
                if y:
                    a_power += gate == "A"
                    b_power += gate == "B"
                    gate = "H"
                else:
                    gate = "X"
            if gate == "H":
                if rail == output == 1:
                    coeff = (-coeff[0], -coeff[1])
            elif output == (rail ^ (gate == "X")):
                # I/X nonzero entries are 1. Restore the global omitted sqrt(2).
                coeff = multiply(coeff, (0, 1))
            else:
                break
            rail = output
            left_count += rail
            physical = (physical + 1-2*rail) % 4
            require(physical == (t-2*(left_count % 2)) % 4, "four-site encoding")
            if t in marks:
                word.append(left_count % 2)
        else:
            poly = amplitudes.setdefault((tuple(word), physical, rail), {})
            add_poly(poly, (a_power, b_power), coeff)

    result = {}
    for (word, _, _), poly in amplitudes.items():
        mass = result.setdefault(word, {})
        for (a, b), coeff in poly.items():
            for (c, d), other in poly.items():
                add_poly(mass, (a-c, b-d), multiply(coeff, other))
    return {word: poly for word, poly in result.items() if poly}


def expected(schedule, denominator, sign, difference):
    scale = (1 << len(schedule)) // denominator
    other_power = -1 if difference else 1
    return {(0, 0): (2*scale, 0), (1, other_power): (sign*scale, 0),
            (-1, -other_power): (sign*scale, 0)}


def main():
    sum_schedule = "HAIBH"
    sum_law = paths(sum_schedule, {5})
    require(len(sum_law) == 2, "sum support")
    for (y,), poly in sum_law.items():
        require(poly == expected(sum_schedule, 4, 1-2*y, False), "sum identity")

    difference_schedule = "HAIXXBIHHHI"
    difference_law = paths(difference_schedule, {10, 11})
    require(len(difference_law) == 4, "difference support")
    for (y, z), poly in difference_law.items():
        require(poly == expected(difference_schedule, 8, 1 if y == z else -1, True),
                "difference identity")
    # I at the final tick preserves each rail; the record at tick ten is an
    # actual exact site write. Summing the two stationary address words gives
    # the claimed R probability.
    print("5 ticks: exact P(y5=0) = (1+cos(phi_A+phi_B))/2")
    print("11 ticks: exact P(y10=y11) = (1+cos(phi_A-phi_B))/2")
    print("Verified every address word and term, including both pulse phases.")


if __name__ == "__main__":
    main()
