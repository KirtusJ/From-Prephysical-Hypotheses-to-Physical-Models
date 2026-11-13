"""Exact finite checks of labelled odd-cycle refinement geometry and a tagged sign control."""
import argparse
import json
from collections import deque
from fractions import Fraction
from math import gcd
from pathlib import Path


GENERATORS = (1, 2)
ORDERS = tuple(range(3, 100, 2))
CALIBRATION = (3, 5, 7, 9, 15, 21, 25, 27, 35, 45, 63, 75)
HIDDEN_PRIME = 11


def cycle_distances(order, generator):
    distances = [None] * order
    distances[0] = 0
    queue = deque([0])
    while queue:
        vertex = queue.popleft()
        for direction in (generator, -generator):
            neighbour = (vertex + direction) % order
            if distances[neighbour] is None:
                distances[neighbour] = distances[vertex] + 1
                queue.append(neighbour)
    assert None not in distances
    return distances


def cycle_checks():
    tables = {(n, g): cycle_distances(n, g) for n in ORDERS for g in GENERATORS}
    orders = []
    embeddings = []
    for n in ORDERS:
        units = [u for u in range(1, n) if gcd(u, n) == 1]
        rows = []
        for g in GENERATORS:
            dist = tables[n, g]
            factors = []
            for u in units:
                # Every pair is a translate of (0, displacement).
                predicted = min(u, n-u)
                observed = max(Fraction(dist[(u*d) % n], dist[d]) for d in range(1, n))
                assert observed == predicted and dist[(u*g) % n] == predicted
                factors.append(int(observed))
            rows.append(dict(generator=g, unit_lipschitz_factors=factors))
        orders.append(dict(order=n, residue_units=units, labelled_generators=rows))
        for larger in ORDERS:
            if larger <= n or larger % n:
                continue
            scale = larger//n
            for g in GENERATORS:
                source, target = tables[n, g], tables[larger, g]
                good = all(target[scale*d]*n == source[d]*larger for d in range(n))
                assert good
                embeddings.append(dict(source=n, target=larger, multiplier=scale,
                                       generator=g, displacements_tested=n, isometric=good))
    return orders, embeddings


def inverse_cases():
    rows = []
    for n in (3**j for j in range(1, 13)):
        inv = pow(2, -1, n)
        for g in GENERATORS:
            # One angular grid step corresponds to residue g under the chosen label.
            input_residue = g % n
            preimage = inv*input_residue % n
            coordinate = preimage*pow(g, -1, n) % n
            assert (2*preimage) % n == input_residue
            input_distance = Fraction(1, n)
            preimage_distance = Fraction(min(coordinate, n-coordinate), n)
            assert preimage_distance == Fraction(n-1, 2*n)
            rows.append(dict(order=n, generator=g, input_residue=input_residue, inverse_image=preimage,
                             input_distance=str(input_distance), inverse_image_distance=str(preimage_distance),
                             forward_lipschitz=min(2, n-2), inverse_lipschitz=min(inv, n-inv)))
    return rows


def locality_cases(orders):
    units_tested = 0
    totals = []
    for row in orders:
        n = row["order"]
        covered = 0
        for u in row["residue_units"]:
            inverse = pow(u, -1, n)
            a = u if 2*u < n else u-n
            b = inverse if 2*inverse < n else inverse-n
            assert (a*b-1) % n == 0
            if n > abs(a)*abs(b)+1:
                assert a*b == 1 and a == b and abs(a) == 1
                covered += 1
        totals.append(dict(order=n, units=len(row["residue_units"]), satisfying_strict_bound=covered))
        units_tested += len(row["residue_units"])

    boundaries = []
    for budget in range(2, 21):
        inverse_length = budget if budget % 2 == 0 else budget-1
        n = budget*inverse_length+1
        assert n % 2 == 1 and (-budget*inverse_length) % n == 1
        assert 2*budget <= n and 2*inverse_length <= n
        boundaries.append(dict(budget=budget, odd_order=n, forward=budget, inverse=-inverse_length,
                               product=1-n))
    return dict(units_tested=units_tested, orders=totals, sharp_equal_budget_examples=boundaries)


def crt_unit(n):
    # Identity away from the untested prime; doubling on its full primary component.
    factor = 1
    other = n
    while other % HIDDEN_PRIME == 0:
        factor *= HIDDEN_PRIME
        other //= HIDDEN_PRIME
    if factor == 1:
        return 1
    return (1+other*pow(other, -1, factor)) % n


def crt_cases():
    witness = {3*HIDDEN_PRIME**j for j in range(1, 7)}
    levels = sorted(set(ORDERS) | set(CALIBRATION) | witness)
    rows = []
    for n in levels:
        multiplier = crt_unit(n)
        assert gcd(multiplier, n) == 1
        if n in CALIBRATION:
            assert multiplier == 1
        if n in witness:
            assert min(multiplier, n-multiplier)*4 >= n
        rows.append(dict(order=n, multiplier=multiplier, in_calibration=n in CALIBRATION,
                         input_distance=str(Fraction(1,n)),
                         image_distance=str(Fraction(min(multiplier,n-multiplier),n)),
                         witness_sequence=n in witness))
    pairs = [(m, n) for m in levels for n in levels if m < n and n % m == 0]
    assert all(crt_unit(n) % m == crt_unit(m) for m, n in pairs)
    return dict(hidden_prime=HIDDEN_PRIME, finite_calibration=CALIBRATION,
                compatibility_pairs_checked=len(pairs), orders=rows)


def floor_scaled_probability(scale, coefficient):
    # For p=1/2+c sqrt(2), compare integers exactly with the ordinary positive sqrt(2).
    def at_most(k):
        left = Fraction(k, scale) - Fraction(1, 2)
        if coefficient >= 0:
            return left <= 0 or left*left <= 2*coefficient*coefficient
        return left < 0 and left*left >= 2*coefficient*coefficient

    low, high = 0, scale+1
    while high-low > 1:
        middle = (low+high)//2
        if at_most(middle):
            low = middle
        else:
            high = middle
    return low


def tagged_sign_controls():
    # Input ray (1,(1-sqrt(2))^n). Its conjugate has reciprocal second-entry magnitude.
    a, b = 1, 0
    rows = []
    previous = Fraction(0)
    grid_bits = 32
    scale = 2**grid_bits
    for n in range(1, 17):
        a, b = a-2*b, b-a
        x, y = a*a+2*b*b, 2*a*b
        assert x*x-2*y*y == 1
        # p = w²/(1+w²). Rationalizing yields 1/2 + c sqrt(2).
        coefficient = Fraction(y, 2*(1+x))
        assert coefficient < previous and (1+x)*coefficient == Fraction(y, 2)
        assert 2*coefficient*coefficient < Fraction(1, 4)
        previous = coefficient
        direct_cells = floor_scaled_probability(scale, coefficient)
        conjugate_cells = floor_scaled_probability(scale, -coefficient)
        assert direct_cells + conjugate_cells == scale-1
        rows.append(dict(n=n, tagged_amplitude=[a,b], ordinary_p_L_sqrt2_coeff=str(coefficient),
                         conjugate_p_L_sqrt2_coeff=str(-coefficient), p_L_rational_part="1/2",
                         fair_bits=grid_bits, definitely_accept_cells_under_ordinary_cut=direct_cells,
                         definitely_accept_cells_under_conjugate_cut=conjugate_cells,
                         undecided_cells_per_cut=1, total_cells=scale))
    return dict(preparation="Externally supplied ray (1,(1-sqrt(2))^n); directly read coin direction L.",
                ordinary_coefficient="p_L=1/2+c sqrt(2), sqrt(2) the ordinary positive real root.",
                fair_coin_control="A fixed comparison cut on uniform fair bits has the same law in both "
                                  "native descriptions; choosing the other cut changes the programmed reference.",
                rows=rows)


def main(directory):
    orders, refinements = cycle_checks()
    result = dict(geometry="Normalized shortest path distance. Refinement sends y to (N/M)y. "
                           "T and T² select separate consistently labelled distance conventions.",
                  finite_scope="Exhaustive on listed orders and all residue displacements/units. "
                               "The global extension and circle endomorphism statements are analytic.",
                  orders=orders, refinements=refinements, finite_locality=locality_cases(orders),
                  doubling_inverse=inverse_cases(),
                  crt_impostor=crt_cases(), tagged_sqrt2=tagged_sign_controls())
    directory.mkdir(parents=True, exist_ok=True)
    (directory/"refinement_geometry.json").write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    print(len(orders), "cycle orders;", len(refinements), "labelled refinements;",
          len(result["doubling_inverse"]), "inverse cases;", len(result["tagged_sqrt2"]["rows"]), "tagged rays.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output_directory", type=Path)
    main(parser.parse_args().output_directory)
