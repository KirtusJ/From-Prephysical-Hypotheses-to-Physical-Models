"""Run python -B check_prepared_force.py OUTPUT_DIRECTORY (NumPy).

Start on one right rail, copy a single flight-window bit, and evolve the
accepted real rails under the plate before each four-tick block. Test the
free case against spectral propagation. Record terminal probabilities near
the ideal ray and at its two sides for every force, including failed shots.
The half-unit reporting interval defines an observable, not a pass threshold.
"""
import argparse
import json
from pathlib import Path

from check_flight_window import np, spectral_flight


def time_step(right, left):
    return np.roll(right + left, 1) / np.sqrt(2), np.roll(right - left, -1) / np.sqrt(2)


def panel(inverse_delta, p0, origin):
    delta = 1 / inverse_delta
    epsilon = delta ** 0.9
    pitch = epsilon * delta
    tick = epsilon * delta**2
    duration = round(delta ** -2.8)
    blocks = round(0.8 / (4 * tick))
    time = blocks * 4 * tick
    width = delta ** 1.1
    radius = abs(origin) + duration + 4 * blocks
    size = 1 << (2 * radius + 2).bit_length()
    labels = np.arange(size)
    x = np.where(labels < size // 2, labels, labels - size)
    right = np.zeros(size)
    left = np.zeros(size)
    right[origin % size] = 1
    for _ in range(duration):
        right, left = time_step(right, left)
    distance = (x - origin) / duration
    take = np.abs(distance - delta * p0) <= width
    mass = right**2 + left**2
    yes, no = mass[take].sum(), mass[~take].sum()
    if yes <= 0:
        raise ValueError("empty accepted branch at the requested finite scale")
    resolution = np.finfo(float).eps * (duration + 4 * blocks + 3)
    if abs(yes + no - 1) > 16 * resolution:
        raise ArithmeticError("source norm loss exceeds the accumulated rounding allowance")
    start_r = np.where(take, right / np.sqrt(yes), 0)
    start_l = np.where(take, left / np.sqrt(yes), 0)
    release_mean = pitch * np.sum(x * (start_r**2 + start_l**2))
    release_target = origin * pitch + p0 * tick * duration
    rows = []
    for slope in (-1, 0, 1):
        angle = -4 * slope * epsilon * delta**3 * x
        cosine, sine = np.cos(angle), np.sin(angle)
        r, l = start_r.copy(), start_l.copy()
        for _ in range(blocks):
            r, l = cosine * r - sine * l, sine * r + cosine * l
            for _ in range(4):
                r, l = time_step(r, l)
        weight = r**2 + l**2
        full = weight.sum()
        spectral_error = None
        if slope == 0:
            independent = spectral_flight(np.stack((start_r, start_l)),
                                          4 * blocks, 2 * np.pi * np.fft.fftfreq(size))
            spectral_error = float(np.linalg.norm(np.stack((r, l)) - independent))
            if spectral_error > 32 * resolution:
                raise ArithmeticError("direct free walk and spectral free walk disagree")
        if abs(full - 1) > 16 * resolution:
            raise ArithmeticError("conditional norm loss exceeds the rounding allowance")
        classical_displacement = p0 * time - slope * time**2 / 2
        bins = []
        for reference, target in (("limiting_origin", origin * pitch + classical_displacement),
                                  ("finite_release", release_target + classical_displacement)):
            offset = pitch * x - target
            lower, upper = weight[offset < -0.5].sum(), weight[offset > 0.5].sum()
            inside = weight[np.abs(offset) <= 0.5].sum()
            bins.append(dict(reference=reference, target=target, below=float(lower),
                             inside=float(inside), above=float(upper),
                             unconditioned_success_and_inside=float(yes * inside)))
        rows.append(dict(potential_slope=slope, conditional_norm_residual=float(full-1),
                         right_mass=float(r @ r), left_mass=float(l @ l),
                         mean_position=float(pitch * (x @ weight)),
                         forbidden_parity_mass=float(weight[(x-origin-duration) % 2 != 0].sum()),
                         free_spectral_error=spectral_error, position_events=bins))
    return dict(inverse_delta=inverse_delta, launch_site=origin, p0=p0, epsilon=epsilon,
                pitch=pitch, preparation_ticks=duration, preparation_time=duration*tick,
                block_count=blocks, attained_time=time, ring_size=size, window_width=width,
                success=float(yes), failure=float(no), success_leading=2*width/np.pi,
                release_mean=float(release_mean), release_target=release_target, flights=rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    folder = parser.parse_args().directory
    folder.mkdir(parents=True, exist_ok=True)
    output = folder / "prepared_force.json"
    if output.exists():
        parser.exit(2, f"Refusing to overwrite {output}\n")
    rows = [panel(k, p0, origin) for k in (6, 10, 14)
            for p0, origin in ((1, 0), (0, 1), (-1, 1))]
    with output.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump({"radius": 0.5, "panels": rows}, stream, indent=2, allow_nan=False)
        stream.write("\n")


if __name__ == "__main__":
    main()
