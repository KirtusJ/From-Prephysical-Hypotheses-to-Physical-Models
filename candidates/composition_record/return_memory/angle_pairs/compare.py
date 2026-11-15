"""Compare all complementary gate angles using the public 99-setting first-return table."""
import argparse
import csv
import hashlib
import io
import math
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "../../first_return_data/first_returns.csv"
DIGEST = "d2f2d7aca97a70de0c75533dbf9b2c5b59b856af89a7b6b0b63914dd932a74f4"
PAIR_COUNT = 48
ALPHA = 0.01
CATEGORIES = ("hit1", "hit2", "hit3", "no_hit_through_3")


def require(condition, explanation):
    if not condition:
        raise ValueError(explanation)


def jobs_from_csv():
    source = SOURCE.read_bytes().replace(b"\r\n", b"\n")
    require(hashlib.sha256(source).hexdigest() == DIGEST, "first-return source digest")
    rows = list(csv.DictReader(io.StringIO(source.decode("ascii"))))
    jobs = {}
    for k, row in enumerate(rows, 1):
        theta = float(row["J_radians"])
        require(abs(theta - k * math.pi / 50) < 2e-14, f"k={k}: grid")
        shots = int(row["shots"])
        full = [int(row[f"hit_{t:02}"]) for t in range(1, 21)]
        censored = int(row["no_hit_by_20"])
        require(shots == 40_000 and min(full + [censored]) >= 0 and sum(full) + censored == shots,
                f"k={k}: shot accounting")
        jobs[k] = (row["job_id"], shots, full[:3] + [sum(full[3:]) + censored])
    require(len(jobs) == 99 and len({job[0] for job in jobs.values()}) == 99, "99 distinct jobs")
    return jobs


def rotate(state, left, right, cosine, sine):
    a, b = state[left], state[right]
    state[left], state[right] = cosine * a - 1j * sine * b, cosine * b - 1j * sine * a


def first_three(theta, pulse=False, classical=False):
    c, s = math.cos(theta), math.sin(theta)
    state = [1.0, 0.0, 0.0]
    hits = []
    for tick in range(1, 4):
        for left, right in ((1, 2), (0, 1)):
            if classical:
                a, b = state[left], state[right]
                state[left], state[right] = c*c*a + s*s*b, s*s*a + c*c*b
            else:
                rotate(state, left, right, c, s)
        hits.append(state[0] if classical else abs(state[0])**2)
        state[0] = 0.0
        if pulse and not classical and tick == 2:
            state[2] *= -1
    return hits


def close(left, right):
    return math.isclose(left, right, rel_tol=2e-13, abs_tol=2e-14)


def decimal(x):
    return f"{x:.10f}"


def make_table():
    jobs = jobs_from_csv()
    output = io.StringIO(newline="")
    table = csv.writer(output, lineterminator="\n")
    fields = ["family", "j", "k_a", "k_b", "job_a", "job_b"]
    for arm in ("a", "b"):
        fields += [f"{arm}_shots"] + [f"{arm}_{name}" for name in CATEGORIES]
    fields += ["ideal_F1_both", "ideal_F2_both", "ideal_F3_a", "ideal_F3_b",
               "site_markov_F3_both", "ideal_gap", "count_gap", "observed_gap",
               "gap_lower_99_familywise", "gap_upper_99_familywise",
               "observed_F3_a_minus_ideal", "observed_F3_b_minus_ideal"]
    table.writerow(fields)
    included = set()
    for family in ("positive_sine", "negative_sine"):
        for j in range(1, 25):
            ka, kb = (j, 50-j) if family == "positive_sine" else (100-j, 50+j)
            included.update((ka, kb))
            a_id, na, fa = jobs[ka]
            b_id, nb, fb = jobs[kb]
            theta = ka * math.pi / 50
            partner = kb * math.pi / 50
            c, s = math.cos(theta), math.sin(theta)
            weak = (s**4 - s**2*c**3)**2
            strong = (s**4 + s**2*c**3)**2
            average = s**8 + s**4*c**6
            h1, h2 = c*c, s**4*c*c
            scenarios = ((theta, False, False, weak), (partner, False, False, strong),
                         (theta, True, False, strong), (theta, False, True, average),
                         (partner, False, True, average))
            for angle, pulse, classical, third in scenarios:
                f = first_three(angle, pulse=pulse, classical=classical)
                require(all(close(x, y) for x, y in zip(f, [h1, h2, third])),
                        f"gate composition differs at j={j}, {family}")
            require(close(strong-weak, 4*s**6*c**3), "sign and prefactor")
            delta = fb[2]/nb - fa[2]/na
            # Hoeffding for the difference of two independent bounded sample means.
            radius = math.sqrt((1/na + 1/nb) * math.log(2*PAIR_COUNT/ALPHA) / 2)
            table.writerow([family, j, ka, kb, a_id, b_id, na, *fa, nb, *fb,
                            *map(decimal, [h1, h2, weak, strong, average, strong-weak]),
                            fb[2]-fa[2], *map(decimal, [delta, max(-1.0, delta-radius),
                            min(1.0, delta+radius), fa[2]/na-weak, fb[2]/nb-strong])])
    require(included == set(range(1, 100)) - {25, 50, 75}, "pair coverage")
    return output.getvalue().encode("ascii")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="create the regenerated table at a fresh path")
    args = parser.parse_args()
    actual = make_table()
    if args.output:
        with args.output.open("xb") as out:
            out.write(actual)
    else:
        stored = (HERE / "pairs.csv").read_bytes().replace(b"\r\n", b"\n")
        require(actual == stored, "table differs from the checked-in result")
        print(f"Verified {PAIR_COUNT} angle pairs. SHA-256 {hashlib.sha256(actual).hexdigest()}")


if __name__ == "__main__":
    main()
