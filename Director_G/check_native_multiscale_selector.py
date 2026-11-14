"""Fixed-H field-on selector using only sharp base records (Python standard library).

Run python -B check_native_multiscale_selector.py OUTDIR; result file must be new.
The complete small-ring word checks are exact on physical sheet coordinates.
Finite score margins/power bounds use binary64 conditional probabilities.
"""
import argparse
import cmath
import json
import math
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import product
from pathlib import Path


GAP = 1/2048
SCORE_SCALE = 2**15
EPSILON = 1/10
ORDERS = (3, 4, 5, 8, 12, 17, 31, 64, 97, 128, 257, 512, 1024)
STRESS_ORDERS = (2048, 4093, 8192)


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def clock(m, d):
    low, high = 0, m
    while low+1 < high:
        mid = (low+high)//2
        if 4*d*d*mid**3 <= m*m:
            low = mid
        else:
            high = mid
    require(4*d*d*low**3 <= m*m < 4*d*d*(low+1)**3, "integer horizon")
    return low


def field_law(m, charge, t, home=0, incoming="R"):
    """Both rail arrays indexed by j with displacement 2*j-t from the sharp home."""
    norm = math.sqrt(0.5)
    gains = {u: norm*cmath.exp(2j*math.pi*((charge*u) % m)/m)
             for u in range((home-t)//2, (home+t)//2+1)}
    right = [int(incoming == "R")]
    left = [int(incoming == "L")]
    for age in range(t):
        offset = (home-age)//2
        rr = [0j]
        ll = []
        for i, (r, l) in enumerate(zip(right, left)):
            kick = gains[offset+i]
            rr.append((r+l)*kick)
            ll.append((r-l)*kick)
        right, left = rr, ll+[0j]
    r = [abs(a)**2 for a in right]
    l = [abs(a)**2 for a in left]
    require(abs(math.fsum(r+l)-1) < 1e-12, "character probability mass")
    return r, l


def count_law(t):
    den = 2**t
    return ([0]+[math.comb(t-1, j)/den for j in range(t)],
            [math.comb(t-1, j)/den for j in range(t)]+[0])


def score_table(t):
    table = []
    for j in range(t+1):
        x = 2*j-t
        if t <= 4*x and 2*x <= t:
            v = x/t
            kappa = math.acos(v/math.sqrt(1-v*v))
            omega = math.asin(math.sin(kappa)/math.sqrt(2))
            # -sin(Phi) = -cos(2*x*kappa-2*t*omega).
            z = -SCORE_SCALE*math.cos(2*x*kappa-2*t*omega)
            numerator = (1 if z >= 0 else -1)*math.ceil(abs(z)-0.5)
            table.append((j, numerator))
    return table


def expected_score(law, table):
    return math.fsum(law[0][j]*q/SCORE_SCALE for j, q in table)


def physical_block(m, home, incoming, t):
    """Integer polynomial of every exit, indexed by the actual cyclic base and sheet."""
    bins = defaultdict(Counter)
    for word in product("RL", repeat=t):
        x, rail, y, sign = home, incoming, 0, 1
        for out in word:
            y = (y+x//2) % m
            if rail == out == "L":
                sign = -sign
            x = (x + (1 if out == "R" else -1)) % (4*m)
            rail = out
        bins[x,rail][y] += sign
    return bins


def exact_two_records():
    records = []
    for m in (3, 4, 5, 8, 9):
        for home, incoming in ((0, "R"), (4*m-1, "L")):
            first = physical_block(m, home, incoming, 3)
            cells = []
            max_error = 0
            for (x1, r1), f in sorted(first.items()):
                second = physical_block(m, x1, r1, 4)
                for (x2, r2), g in sorted(second.items()):
                    out = Counter()
                    for i, a in f.items():
                        for j, b in g.items():
                            out[(i+j) % m] += a*b
                    numerator = sum(a*a for a in out.values())
                    # Intermediate sharp read preserves this entire integer sheet vector.
                    fresh = sum(a*a for a in f.values())*sum(b*b for b in g.values())
                    cells.append([x1,r1,x2,r2,numerator,fresh])
                    mix = 0
                    for k in range(m):
                        root = cmath.exp(2j*math.pi*k/m)
                        decode = lambda h: sum(a*root**u for u, a in h.items())
                        mix += abs(decode(f)*decode(g))**2/m
                    max_error = max(max_error, abs(mix-numerator)/128)
            require(sum(row[-2] for row in cells) == 128, "retained two-read mass")
            require(sum(row[-1] for row in cells) == 128, "refreshed two-read mass")
            require(max_error < 2e-14, "persistent sector transcript")
            tv = Fraction(sum(abs(row[-2]-row[-1]) for row in cells), 256)
            require(tv > 0, "fresh-sheet rival was accidentally equivalent")
            witness = max(cells, key=lambda row: abs(row[-2]-row[-1]))
            records.append(dict(M=m, home=home, entrance=incoming, clocks=[3,4],
                                occupied_port_pairs=len(cells), exact_normalizer=128,
                                exact_persistent_vs_refreshed_tv=str(tv),
                                witness_port_pair_and_two_numerators=witness,
                                maximum_fourier_error=max_error))
    return records


def coordinate_checks():
    rows = []
    for m in (3, 4, 7, 11):
        err = canonical = 0
        for t in range(1, min(7, 2*m-1)+1):
            for k in range(m):
                reference = field_law(m,k,t)
                for home, incoming in ((0,"R"), (1,"L"), (4*m-1,"R"), (4*m-1,"L")):
                    rr,ll = field_law(m,k,t,home,incoming)
                    if incoming == "R":
                        canon = rr,ll
                    else:
                        canon = ll[::-1],rr[::-1]
                    canonical = max(canonical, max(abs(a-b) for u,v in zip(reference,canon)
                                                    for a,b in zip(u,v)))
                    bins = physical_block(m,home,incoming,t)
                    for j, (r,l) in enumerate(zip(rr,ll)):
                        x = (home+2*j-t) % (4*m)
                        for out, value in (("R",r), ("L",l)):
                            coeff = bins.get((x,out), {})
                            z = sum(a*cmath.exp(2j*math.pi*((y*k)%m)/m) for y,a in coeff.items())
                            err = max(err,abs(abs(z)**2/(2**t)-value))
        require(max(err,canonical) < 3e-14, "word/rail/reflection discrepancy")
        rows.append(dict(M=m, largest_word_error=err, largest_frame_error=canonical))
    return rows


def dark(m, d):
    return 0.25 if d == "count" else 0.5*math.sin(math.pi*d/m)**2


def count_stage(m):
    candidates = []
    for t, x, direction in ((3,-1,"L"), (4,0,"L")):
        j = (x+t)//2
        rail = int(direction == "L")
        target = field_law(m,1,t)[rail][j]
        rival = count_law(t)[rail][j]
        candidates.append(dict(t=t, x=x, rail=direction, target=target, count=rival,
                               gap=abs(target-rival)))
    return max(candidates,key=lambda row:row["gap"]), candidates


def exact_count_alias_four():
    rings = []
    for t in (3,4):
        bins = physical_block(4,0,"R",t)
        counts = Counter()
        for word in product("RL",repeat=t):
            x = sum(1 if c == "R" else -1 for c in word) % 16
            counts[x, word[-1]] += 1
        cells = []
        for (x,rail), p in sorted(bins.items()):
            norm = (p[0]-p[2])**2 + (p[1]-p[3])**2
            cells.append([x,rail,norm,counts[x,rail]])
        tv = Fraction(sum(abs(v-w) for x,r,v,w in cells),2**(t+1))
        require((tv == 0) == (t == 3), "three-tick count alias")
        if t == 4:
            require([0,"L",5,3] in cells, "four-tick count discriminator")
        rings.append(dict(ticks=t, normalized_by=2**t, order_four_unit_vs_count=cells,tv=str(tv)))
    return rings


def band_stage(m, d):
    t = clock(m,d)
    require(t >= 1, "empty programmed block")
    table = score_table(t)
    labels = [0] if d == 1 else range(d,min(2*d-1,m//2)+1)
    target = expected_score(field_law(m,1,t),table)
    signed = 1 if d == 1 else -1  # target minus competitor for d=1, opposite otherwise
    means = [[k, expected_score(field_law(m,k,t),table)] for k in labels]
    raw, worst = min((signed*(target-y),k) for k,y in means)
    # Binary64 finite choices with a buffer; the article supplies the separate
    # certified compiler. Keep missed and reversed scores for every label.
    if raw > GAP+1e-10:
        name = "rounded_fringe"
        read_ticks, actual_gap, target_mean = t, raw, target
        oriented = signed
        adversary = worst
    else:
        name = "three_tick_dark"
        read_ticks, target_mean = 3, dark(m,1)
        actual_gap, adversary = min((signed*(target_mean-dark(m,k)),k) for k in labels)
        oriented = signed
        for k in labels:
            if k in (adversary,0):
                measured = field_law(m,k,3)[1][1]
                require(abs(measured-dark(m,k)) < 1e-14, "dark fallback phase")
    require(actual_gap > 0, "unseparated folded label")
    threshold = target_mean-oriented*actual_gap/2
    return dict(d=d, fringe_ticks=t, scored_right_cells=table, target_raw_mean=target,
                conditional_rival_means=means, raw_worst_gap=raw, raw_worst_label=worst,
                raw_gap_minus_threshold=raw-GAP, selected=name, ticks=read_ticks,
                target_mean=target_mean, least_separated=adversary, gap=actual_gap,
                target_side=oriented, midpoint=threshold)


def schedule(m):
    stages=[]
    d=1
    while d<=m//2:
        stages.append(band_stage(m,d))
        d*=2
    sensor, alternatives=count_stage(m)
    stages.append(dict(d="count", selected="native_port", ticks=sensor["t"],
                       gap=sensor["gap"], target_side=1 if sensor["target"]>sensor["count"] else -1,
                       midpoint=(sensor["target"]+sensor["count"])/2, candidates=alternatives))
    charged=0
    range_charged=0
    miss=wrong=0
    for j, stage in enumerate(stages):
        is_count=stage["d"]=="count"
        denom = m if is_count else stage["d"]
        h=EPSILON/(8*(j+1)**2*denom)
        # Indicator read is in [0,1]. The bounded fringe score is in [-1,1].
        span = 2 if stage["selected"]=="rounded_fringe" else 1
        reps=math.ceil(8*math.log(1/h)/stage["gap"]**2)
        range_reps=math.ceil(2*span**2*math.log(1/h)/stage["gap"]**2)
        charged+=stage["ticks"]*reps
        range_charged+=stage["ticks"]*range_reps
        stage.update(repetitions=reps, repetitions_using_actual_range=range_reps, per_stage_hoeffding=h)
        miss+=h
        if not is_count:
            wrong+=h*sum(1 if k==0 or 2*k==m else 2 for k,y in stage["conditional_rival_means"])
    good=2*max(0,1-miss)
    return dict(M=m, stages=stages, fixed_budget_ticks=charged, range_sensitive_ticks=range_charged,
                target_miss_bound=miss,
                wrong_square_joint_upper_per_launch=wrong/m,
                false_count_upper=stages[-1]["per_stage_hoeffding"],
                localized_square_true_accepted_lower=good/m,
                localized_square_posterior_error_upper=wrong/(good+wrong))


def run():
    full=[schedule(m) for m in ORDERS]
    stress=[dict(M=m, stage=band_stage(m,d)) for m in STRESS_ORDERS for d in (1,2,4,8)]
    return dict(score="rounded -sin(Phi), integers / 32768 in scored_right_cells [j,numerator]; "
                      "x_relative=2*j-t. Nonwindow and opposite-rail scores are zero.",
                certificate="Binary64 finite mean and budget evaluations; accepted raw gaps "
                            "have 1e-10 buffer over 1/2048. Worst-case inequalities assume "
                            "these expectations, identical sharp-record instruments, persistent "
                            "labels, fresh block choices, correctly calibrated model, and "
                            "conditional fair count. No asymptotic cutoff inferred from rows.",
                epsilon=EPSILON, coordinate_checks=coordinate_checks(), joint=exact_two_records(),
                count_alias_exact=exact_count_alias_four(),
                all_folded_and_count=full, selected_large_order_stress=stress)


if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("directory",type=Path)
    directory=p.parse_args().directory
    evidence=run()
    directory.mkdir(parents=True,exist_ok=True)
    with (directory/"native_multiscale_selector.json").open("x",encoding="utf8",newline="\n") as f:
        json.dump(evidence,f,separators=(",",":"),allow_nan=False)
        f.write("\n")
