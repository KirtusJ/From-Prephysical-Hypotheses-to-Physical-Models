"""Direct interval evolution of a parity-supported traveling packet, using only Python."""
import cmath
import json
import math


def source(length, sign):
    # With the +ikx transform, exp(-ik0*x) peaks at k0. The parity mask
    # duplicates it at k0+pi, where U changes sign with the same coin vectors.
    k0 = math.acos(1 / math.sqrt(3))
    omega = math.asin(math.sin(k0) / math.sqrt(2))
    ratio = math.sqrt(2) * cmath.exp(1j * (omega - k0)) - 1
    scale = math.sqrt(1 + abs(ratio) ** 2)
    ur, ul = 1 / scale, ratio / scale
    if sign == -1:
        ur, ul = -ul.conjugate(), ur.conjugate()
    assert abs((abs(ur) ** 2 - abs(ul) ** 2) - sign / 2) < 1e-14
    center = length / 4 - 0.5
    envelope = [cmath.exp(-(x - center) ** 2 / (4 * length) - 1j * k0 * (x - center))
                if x % 2 == 0 else 0j for x in range(length)]
    norm = math.sqrt(math.fsum(abs(z) ** 2 for z in envelope))
    return [ur * z / norm for z in envelope], [ul * z / norm for z in envelope]


def fold(y):
    return 1 - abs(1 - (y % 2))


def run_packet(length, sign):
    right, left = source(length, sign)
    times = {0: "launch", length: "before_right_impact",
             3 * length // 2: "right_impact", 9 * length // 4: "after_right_impact"}
    scale = 1 / math.sqrt(2)
    rows = []
    for tick in range(max(times) + 1):
        if tick in times:
            probabilities = [abs(r) ** 2 + abs(l) ** 2 for r, l in zip(right, left)]
            total = math.fsum(probabilities)
            assert abs(total - 1) < 1e-10
            target = fold(0.25 + tick / (2 * length))
            own_ray = fold(0.25 + sign * tick / (2 * length))

            def mean_distance(ray):
                return math.fsum(p * abs((x + 0.5) / length - ray)
                                 for x, p in enumerate(probabilities)) / total

            rows.append({"tick": tick, "positive_ray_clock": times[tick],
                         "positive_ray": target, "prepared_band_ray": own_ray,
                         "mean_distance_to_positive_ray": mean_distance(target),
                         "mean_distance_to_prepared_band_ray": mean_distance(own_ray),
                         "total_probability": total})
        if tick < max(times):
            # Actual outward proposals stay at the wall and reverse rail.
            plus = [(r + l) * scale for r, l in zip(right, left)]
            minus = [(r - l) * scale for r, l in zip(right, left)]
            right, left = [minus[0], *plus[:-1]], [*minus[1:], plus[-1]]
    return rows


if __name__ == "__main__":
    result = {"source": "Even physical wells; Gaussian envelope of probability width sqrt(L), "
                        "centred at (x+1/2)/L=1/4; carrier k0=acos(1/sqrt(3)); "
                        "constant normalized coin from the chosen band at k0.",
              "step": "Hadamard then shift; outward proposals stay one tick and reverse rail with sign +1.",
              "lengths": {}}
    for length in (64, 128, 256, 512, 1024):
        result["lengths"][length] = {"velocity_plus_half": run_packet(length, 1),
                                     "velocity_minus_half": run_packet(length, -1)}
    print(json.dumps(result, indent=2))
