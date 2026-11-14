"""Check repeated signed staircase filters with all retained positions read coherently.

Run python check_staircase_position_repeats.py OUTDIR. The output must be new.
"""
import argparse
from collections import Counter
from fractions import Fraction
import json
from pathlib import Path


def require(ok, message):
    if not ok:
        raise ValueError(message)


def masks(n, home, order):
    size = 4 * order
    rows = []
    for t in range(1, 2*n+1):
        r = min(t, 2*n-t)
        rows.append({(home-r) % size, (home+r) % size})
    rows.append({(home+1) % size})
    return rows


def replay(rows, home, order, incoming="R"):
    size = 4 * order
    histories = [("", home, incoming, 1, 0)]
    for row in rows:
        following = []
        for word, x, rail, sign, gain in histories:
            # Both daughters acquire the gain of the physical departure site.
            step_gain = (gain + x//2) % order
            for c, dx in (("R", 1), ("L", -1)):
                y = (x + dx) % size
                if y in row:
                    s = -sign if c == rail == "L" else sign
                    following.append((word+c, y, c, s, step_gain))
        histories = following
    return histories


def lifted_words(n, home, order, incoming="R"):
    result = []
    for word in ("R"*n+"L"*n+"R", "L"*n+"R"*n+"R"):
        x, gain = home, 0
        for c in word:
            gain += x//2
            x += 1 if c == "R" else -1
        sign = (-1)**sum(c == prev == "L" for c, prev in zip(word, incoming+word))
        result.append((word, x % (4*order), "R", sign, gain % order))
    return result


def spectral_counts(histories, order):
    """Integer Fourier coefficients of the unnormalized squared character amplitude."""
    coefficients = Counter()
    for first in histories:
        for second in histories:
            coefficients[(first[4]-second[4]) % order] += first[3]*second[3]
    return {j:n for j, n in coefficients.items() if n}


def convolution(left, right, order):
    result = Counter()
    for i, a in left.items():
        for j, b in right.items():
            result[(i+j) % order] += a*b
    return {j:n for j,n in result.items() if n}


def folded_cosine_key(residue, order):
    # cos(2*pi*r/M) agrees exactly when r is equal up to sign modulo M.
    # A rational quarter turn has zero cosine, as does the count component's extra term.
    r = residue % order
    if (4*r) % order == 0 and (2*r) % order != 0:
        return "zero"
    return min(r, order-r)


def run():
    orders = (3, 4, 5, 6, 7, 8, 9, 10, 12, 15, 16)
    panels = []
    home_checks = 0
    for m in orders:
        seam_panels = []
        for n in (1, 2):
            for h in range(4*m):
                first_mask = masks(n, h, m)
                first = replay(first_mask, h, m)
                second = lifted_words(n, h+1, m)
                listed = lifted_words(n, h, m)
                require(first == listed, "arm word, rail, sign or departure gain")
                delta = (first[0][4]-first[1][4]) % m
                require(delta == n*n % m and all(v[3] == (-1)**(n-1) for v in first),
                        "symmetric arm gain or sign")
                two = replay(first_mask+masks(n, h+1, m), h, m)
                products = {(a[0]+b[0], b[1], "R", a[3]*b[3], (a[4]+b[4]) % m)
                            for a in first for b in second}
                require(set(two) == products and len(two) == 4, "translated serial product")
                f = spectral_counts(first, m)
                expected = Counter([0, 0, delta, (-delta) % m])
                require(f == expected, "collapsed Fourier lags")
                require(spectral_counts(two, m) == convolution(f, f, m), "component serial square")
                home_checks += 1
                if h == 4*m-1:
                    seam_panels.append(dict(n=n, home=h, one_tick_length=2*n+1,
                                            word_columns=["word", "site", "rail", "sign", "gain_mod_M"],
                                            words=first, repeated_words=two, lag_coefficients=sorted(f.items())))

        labels = ["count"] + list(range(m//2+1))
        keys = {s: ("zero", "zero") if s == "count" else
                (folded_cosine_key(s, m), folded_cosine_key(4*s, m)) for s in labels}
        equal_first = [[s, t] for j,s in enumerate(labels) for t in labels[j+1:]
                       if keys[s][0] == keys[t][0]]
        require(equal_first == ([["count", m//4]] if m % 4 == 0 else []),
                "first-filter count/quarter-turn collision")
        require(len(set(keys.values())) == len(labels), "surviving two-filter degeneracy")
        panels.append(dict(order=m, folded_labels=labels, first_filter_ties=equal_first,
                           two_filter_ties=[], seam=seam_panels))

    # At order four, a half count, half folded-s=1 preparation is invisible to filter 1.
    quarter = []
    for n,counter,character in ((1,Fraction(1,4),Fraction(1,4)),
                                (2,Fraction(1,16),Fraction(1,8))):
        one = (counter+character)/2
        two = (counter**2+character**2)/2
        gap = two-one**2
        require(gap == (0 if n == 1 else Fraction(1,1024)), "quarter-turn variance")
        quarter.append(dict(n=n, count=counter, character=character, one=one,
                            two=two, independent=one**2, gap=gap))

    # Wrong input rail reverses precisely the left-first sign, changing the character fringe.
    rails = [replay(masks(2,0,5),0,5,c) for c in "RL"]
    require(rails[0][0][3] == rails[1][0][3] and rails[0][1][3] == -rails[1][1][3],
            "sign-sensitive input control")
    # Failing to translate the repeated block makes its first mask the wrong position parity.
    missed = replay(masks(2,0,5)*2,0,5)
    require(not missed, "untranslated second mask should miss every retained word")
    return dict(scope="Stationary nonnegative count/character mixtures. Equalities use all launches.",
                tested_home_filter_pairs=home_checks, orders=panels, quarter_turn_half_mix=quarter,
                wrong_input_signs={c:[w[3] for w in h] for c,h in zip("RL",rails)},
                untranslated_second_block_survivors=len(missed))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    directory = parser.parse_args().directory
    result = run()
    directory.mkdir(parents=True, exist_ok=True)
    with (directory/"staircase_position_repeats.json").open("x", encoding="utf8", newline="\n") as f:
        json.dump(result, f, default=str, separators=(",", ":"))
        f.write("\n")
