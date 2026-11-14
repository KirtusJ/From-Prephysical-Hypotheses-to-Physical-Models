"""Compare all positions and times of Asapanna et al. Figure 2, Dataverse v2.0."""
import argparse
import csv
from decimal import Decimal, localcontext
from hashlib import md5
from pathlib import Path


# File MD5s published for Figure 2 in doi:10.57745/7MIDRA, version 2.0.
FILES = {
    "figure2_position_n": "ecbe4c0594cbefabe4b8de800ad7f3b9",
    "figure2_time_M": "81204104feca038f5611e2c3e8db5597",
    "figure2a_data": "f991bed781c30ea0e61d2ea1270ce318",
    "figure2b_alpha": "4ee3636322f03e9f4deae356a495c25c",
    "figure2b_beta": "ff30adab8f51cf20c5b8ed01ba52b53d",
    "figure2b_total": "8006d4f52a8d38e1cb7be1f2e58cbf2f",
    "figure2c_data": "3c7d31e94dc092ea69af33cebbbd3ca7",
    "figure2d_alpha": "34252b1085bfb304aa36b8750978537e",
    "figure2d_beta": "a8f5f4fed9c80f96c48605d77099e332",
    "figure2d_total": "9fb87f2116d6a600921571044ecd9729",
    "figure2e_data": "365bfec75bba281bcd981ce81704dbb7",
    "figure2f_alpha": "e01512c3639fd487236100059afaab08",
    "figure2f_beta": "c72ee0e63c54827961b7a032148f86df",
    "figure2f_total": "143caf07ab672e9681a72e0ece8b3516",
}


def table(folder, name):
    data = (folder / (name + ".txt")).read_bytes()
    if md5(data).hexdigest() != FILES[name]:
        raise ValueError(f"Unexpected v2.0 file: {name}")
    return [[Decimal(value) for value in line.split(",")] for line in data.decode().splitlines()]


def vector(folder, name):
    return [value for (value,) in table(folder, name)]


def panel(folder, matrix_letter, curve_letter, n_sites, n_times):
    grid = table(folder, "figure2" + matrix_letter + "_data")
    if len(grid) != n_sites or any(len(row) != n_times for row in grid):
        raise ValueError("Unexpected position-time grid")
    curves = [vector(folder, "figure2" + curve_letter + "_" + name)
              for name in ("alpha", "beta", "total")]
    columns = []
    for spatial, alpha, beta, total in zip(zip(*grid), *curves, strict=True):
        weight = sum(spatial)
        if min(spatial) < 0 or min(weight, beta, total) <= 0:
            raise ValueError("Invalid intensity normalization")
        if abs(alpha + beta - total) > Decimal("2e-15"):
            raise ValueError("Source ring totals disagree beyond decimal export precision")
        columns.append((total, tuple(value/weight for value in spatial), weight/beta))
    return columns


def distance(p, q):
    return sum(abs(x-y) for x,y in zip(p,q,strict=True))/2


def replay(folder, dest):
    times = vector(folder, "figure2_time_M")
    positions = vector(folder, "figure2_position_n")
    if times != list(range(1,41)) or len(positions) != 64 or positions != sorted(set(positions)):
        raise ValueError("Unexpected Fig. 2 axes")
    samples = [panel(folder, m, c, len(positions), len(times)) for m,c in zip("ace","bdf")]
    for p in samples:
        factors = [scale for _,_,scale in p]
        if max(factors) - min(factors) > Decimal("1e-11"):
            raise ValueError("Site sums and beta-ring traces use a time-varying scale")
    with dest.open("w",encoding="utf-8",newline="") as out:
        writer = csv.writer(out,lineterminator="\n")
        writer.writerow(["period","no_noise_total","redrawn_total","held_total",
                         "redrawn_vs_clean_profile_half_L1","held_vs_clean_profile_half_L1"])
        for time, clean, redraw, hold in zip(times,*samples,strict=True):
            writer.writerow([time, clean[0], redraw[0], hold[0],
                             f"{distance(clean[1],redraw[1]):.12f}",
                             f"{distance(clean[1],hold[1]):.12f}"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("figure2_folder", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    with localcontext() as ctx:
        ctx.prec = 50
        replay(args.figure2_folder, args.output)
