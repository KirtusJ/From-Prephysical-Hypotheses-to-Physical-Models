"""Check the finite part of the record-multiplicity comparison using integers."""
import json
from math import comb


def main():
    # Signed sums on the right and left rails. The probability denominator is 2**n.
    state = {0: (1, 0)}
    rows = []
    for n in range(22):
        denominator = 2 ** n
        mass = sum(right ** 2 + left ** 2 for right, left in state.values())
        if mass != denominator:
            raise ValueError(f"Normalization failed at horizon {n}")

        differences = {}
        for radius in range(n % 2, n + 1, 2):
            difference = 0
            for site in range(-radius, radius + 1, 2):
                right, left = state[site]
                difference += comb(n, (n + site) // 2) - right ** 2 - left ** 2
            differences[radius] = difference

        strict_radii = [radius for radius, value in differences.items() if value > 0]
        if min(differences.values()) < 0 or differences[n] != 0:
            raise ValueError(f"Central mass comparison failed at horizon {n}")
        if bool(strict_radii) != (n >= 4):
            raise ValueError(f"Equality condition failed at horizon {n}")
        rows.append({
            "n": n,
            "cumulative_count_minus_quantum_numerators": differences,
            "denominator": denominator,
            "strict_at_radii": strict_radii,
        })

        next_state = {}
        for site in range(-n - 1, n + 2, 2):
            u, v = state.get(site - 1, (0, 0))
            w, z = state.get(site + 1, (0, 0))
            next_state[site] = (u + v, w - z)
        state = next_state
    print(json.dumps(rows, indent=2))


if __name__ == "__main__":
    main()
