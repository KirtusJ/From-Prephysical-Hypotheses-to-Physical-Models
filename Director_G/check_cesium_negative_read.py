"""Run python check_cesium_negative_read.py PUBLISHED_PDF OUTPUT_DIRECTORY.

Requires pdfplumber. Read Fig. 3's vector bars after checking the source
digest and axis geometry. Preserve every plotted site and displaced count.
Test the two reported fair-coin statistics, extremize distribution distance
over arm mixtures, and enumerate all 16 signed words in each instrument.
"""
import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
from itertools import product
import json
from pathlib import Path

import pdfplumber


DIGEST = "513fb6d398c0c6c51523e5154def4c154c8b35809f1348765d3ea3735b232c31"
SOURCE = "https://quantum-technologies.iap.uni-bonn.de/assets/pdf/SDT/physrevx-alberti.pdf"
SITES = range(-8, 9)


def require(test, message):
    if not test:
        raise ValueError(message)


def figure_counts(path):
    require(hashlib.sha256(path.read_bytes()).hexdigest() == DIGEST, "source PDF has changed")
    with pdfplumber.open(path) as pdf:
        page = pdf.pages[4]
        ticks = sorted((r["top"] + r["bottom"]) / 2 for r in page.rects
                       if 73.8 < r["x0"] < 74.3 and 2.3 < r["width"] < 2.6 and r["top"] < 270)
        require(len(ticks) == 15, "expected five calibrated y ticks per panel")
        bars = [r for r in page.rects + page.curves if r["x1"] < 298 and r["bottom"] < 270
                and 6 < r["width"] < 7 and r["non_stroking_color"] == (0.75294, 0.98824, 0.4549)]
        panels = []
        for index in range(3):
            y_ticks = ticks[5*index:5*index+5]
            pitch = (y_ticks[-1] - y_ticks[0]) / 160
            counts = dict.fromkeys(SITES, 0)
            geometry = {}
            for bar in bars:
                if abs(bar["bottom"] - y_ticks[-1]) > 0.2:
                    continue
                # Measured site-0 centre and 1-site spacing on this PDF page.
                site_coord = ((bar["x0"] + bar["x1"]) / 2 - 184.355) / 12.777
                site = round(site_coord)
                height = bar["height"] / pitch
                require(site in SITES and abs(site-site_coord) < 0.005 and site not in geometry,
                        "unassigned or duplicate site")
                require(abs(height-round(height)) < 0.15, "ambiguous integer bar")
                counts[site] = round(height)
                geometry[site] = dict(shape=bar["object_type"], raw_height_in_atoms=height,
                                      site_coordinate=site_coord)
            panels.append(dict(tick_centres=y_ticks, counts=counts, bars=geometry))
    require([sum(p["counts"].values()) for p in panels] == [230,404,404], "unexpected denominators")
    return panels


def distribution(counts):
    n = sum(counts.values())
    return {x:F(counts[x],n) for x in SITES}


def tv(a,b):
    return sum(abs(a[x]-b[x]) for x in a)/2


def positive(p):
    return sum(y for x,y in p.items() if x > 0)


def common_target(p, q):
    # Faithful sites, arbitrary setting-dependent removal, a shared target.
    upper = {j:max(p[j],q[j]) for j in SITES}
    retained = 1/sum(upper.values())
    target = {j:retained*upper[j] for j in SITES}
    require(sum(target.values()) == 1 and 1/retained == 1+tv(p,q), "common-target mass")
    gains = []
    for observed in (p,q):
        response = {j:observed[j]/upper[j] if upper[j] else F(0) for j in SITES}
        require(all(0 <= response[j] <= 1 and target[j]*response[j] == retained*observed[j]
                    for j in SITES), "selection witness failed")
        gains.append(response)
    return dict(target=target, retention=retained, loss=1-retained, response=gains)


def compare(panels):
    blank, left, right = [p["counts"] for p in panels]
    # The marked drop regions in panels (b),(c) are at +4..+8, -8..-4.
    b = {x:(left[x] if x < 4 else 0) for x in SITES}
    c = {x:(right[x] if x > -4 else 0) for x in SITES}
    q = {x:b[x]+c[x] for x in SITES}
    require((sum(b.values()), sum(c.values())) == (201,196), "retained runs")
    p, qb, qc, pooled = map(distribution, (blank,b,c,q))
    breaks = {F(0),F(1)}
    for x in SITES:
        if qb[x] != qc[x]:
            w = (p[x]-qc[x])/(qb[x]-qc[x])
            if 0 < w < 1:
                breaks.add(w)
    mixtures = [(w,tv(p,{x:w*qb[x]+(1-w)*qc[x] for x in SITES})) for w in sorted(breaks)]
    require(min(mixtures,key=lambda pair:pair[1]) == (1,F(4937,46230)), "arm mixture minimum")
    surplus = [x for x in SITES if p[x] > pooled[x]]
    delta = positive(pooled)-positive(p)
    require(surplus == [-3,-1] and tv(p,pooled) == F(21981,91310), "observed TV")
    ratio = F(q[1]*blank[-1], q[-1]*blank[1])
    arm_ratios = [F(z[1]*blank[-1],z[-1]*blank[1]) for z in (b,c)]
    event = (-3,-1,2)
    event_mass = [sum(v[x] for x in event) for v in (p,qb,qc)]
    require(event_mass == [F(147,230),F(107,201),F(13,49)] and
            {x for x in SITES if p[x] > qb[x]} == set(event), "arm-mixture certificate")
    pooled_witness = common_target(p,pooled)
    arm_witness = common_target(p,qb)
    require([w["loss"] for w in (pooled_witness,arm_witness)] ==
            [F(21981,113291),F(4937,51167)], "sharp loss values")
    return dict(retained_b=b, retained_c=c, displaced_counts=[sum(left.values())-sum(b.values()),
                sum(right.values())-sum(c.values())], printed_K="1.435 +/- 0.074 (bootstrap)",
                printed_K_alternate_uncertainty="0.068 (Monte Carlo)",
                first_arm_weights=[F(sum(b.values()),sum(q.values())), F(sum(c.values()),sum(q.values()))],
                positive_blank=positive(p), positive_retained=positive(pooled),
                positive_difference=delta, reconstructed_K=1+2*delta,
                TV=tv(p,pooled), blank_surplus_sites=surplus, free_mixture_breakpoints_and_TV=mixtures,
                odds_ratio=ratio, limits_from_each_pure_arm=arm_ratios, event_mass=event_mass,
                blank_minus_retained={x:p[x]-pooled[x] for x in SITES},
                common_target_pooled=pooled_witness, common_target_negative_arm=arm_witness)


def ideal():
    reported = {}
    for selection, shift in (("unobserved",None),("displace_plus",1),("displace_minus",0)):
        signed = Counter()
        words = []
        for word in product((0,1),repeat=4):
            previous = 0
            sign = 1
            for coin in word:
                sign *= -1 if coin == previous == 1 else 1
                previous = coin
            endpoint = sum(2*c-1 for c in word)//2
            displaced = word[0] == shift
            if displaced:
                endpoint += 5*(2*word[0]-1)
            signed[endpoint,previous] += sign
            words.append([word,endpoint,previous,sign,displaced])
        site = Counter()
        for (x,coin),tally in signed.items():
            site[x] += F(tally*tally,16)
        require(sum(site.values()) == 1, "integer walk norm")
        reported[selection] = dict(words=words, site_mass=dict(sorted(site.items())))
    bare = reported["unobserved"]["site_mass"]
    shield = {x:sum(reported[s]["site_mass"].get(x,0) for s in ("displace_plus","displace_minus"))
              for x in range(-2,3)}
    require(sum(shield.values()) == 1 and 1+2*(positive(shield)-positive(bare)) == F(3,2),
            "author fair-coin prediction")
    # Group the blank words by first arm *and* final spin before forming any square.
    ports = Counter()
    for word, j, spin, sign, displaced in reported["unobserved"]["words"]:
        ports[j,spin,word[0]] += sign
    def observable(law):
        return law[-1]-law[1]-4*(law[-2]-law[2])
    support = range(-2,3)
    diagonal, interference, arms = {}, {}, []
    for arm in (0,1):
        row = {j:sum(F(ports[j,spin,arm]**2,8) for spin in (0,1)) for j in support}
        require(sum(row.values()) == 1 and observable(row) == 0, "tagged arm observable")
        arms.append(row)
    for j in support:
        diagonal[j] = (arms[0][j]+arms[1][j])/2
        interference[j] = sum(F(2*ports[j,spin,0]*ports[j,spin,1],16) for spin in (0,1))
    require(diagonal == shield and [16*interference[j] for j in support] == [0,4,0,-4,0],
            "sign-plate cross term")
    require(all(diagonal[j]+interference[j] == bare[j] for j in support) and
            observable(interference) == F(1,2), "phase observable")
    # These affine identities also cover every intermediate projection cos(phi).
    for t in (-1,0,1):
        phase = {j:diagonal[j]+t*interference[j] for j in support}
        gains = {-2:F(3,5), -1:F(3+2*t,5), 0:F(3,5), 1:F(3-2*t,5), 2:F(3,5)}
        require(all(diagonal[j]*gains[j] == F(3,5)*phase[j] for j in support),
                "phase-linked response counterexample")
    return dict(panels=reported, shield_pooled=shield, blank_positive=positive(bare),
                proposed_phase=dict(single_arm_laws=arms, diagonal=diagonal, cosine_term=interference),
                shield_positive=positive(shield), K=1+2*(positive(shield)-positive(bare)),
                TV=tv(bare,shield), two_port_odds_ratio=shield[1]*bare[-1]/(shield[-1]*bare[1]))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path)
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()
    args.directory.mkdir(parents=True, exist_ok=True)
    dest = args.directory/"cesium_negative_read.json"
    if dest.exists():
        parser.exit(2, f"Refusing to overwrite {dest}\n")
    panels = figure_counts(args.pdf)
    result = dict(source=SOURCE, source_sha256=DIGEST, figure=3,
                  digitized=panels, retained_analysis=compare(panels), model=ideal())
    with dest.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(result, stream, default=str, indent=2, allow_nan=False)
        stream.write("\n")


if __name__ == "__main__":
    main()
