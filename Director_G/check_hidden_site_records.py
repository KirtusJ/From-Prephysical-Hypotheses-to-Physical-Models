"""Compare literal two-rail propagation with renewal over hidden site records."""

import argparse
from collections import defaultdict
from fractions import Fraction
import json
import math
from pathlib import Path


def require(condition, explanation):
    if not condition:
        raise ValueError(explanation)


def free_prefixes(m):
    a = [Fraction(1)]
    for j in range(1, m + 1):
        a.append(a[-1] * Fraction(2*j-1, 2*j))
    return a


def composition_survival(a, p):
    """Cut at the first internal copy. The last read can always be pooled."""
    q = 1 - p
    s = [a[0]]
    for j in range(1, len(a)):
        mass = q**(j-1) * a[j]
        for k in range(1, j):
            mass += p * q**(k-1) * a[k] * s[j-k]
        s.append(mass)
    return s


def physical_survival(m, p, signed_root):
    # +1 or -1 is the character phase for one sheet unit. For two
    # chronological steps enumerate the actual signed Hadamard daughters.
    rho = {(0, 0): Fraction(1)}
    incoming = 1
    survival = [Fraction(1)]
    for _ in range(m):
        outgoing = -incoming
        def daughters(x):
            for first in (1, -1):
                sign = -1 if incoming == first == -1 else 1
                if first == outgoing == -1:
                    sign *= -1
                gain = x//2 + (x+first)//2
                phase = signed_root if gain % 2 else 1
                yield x+first+outgoing, sign*phase
        next_rho = defaultdict(Fraction)
        for (x, y), element in rho.items():
            for xx, sx in daughters(x):
                for yy, sy in daughters(y):
                    next_rho[xx, yy] += element * sx * sy / 4
        rho = {xy: (val if xy[0] == xy[1] else (1-p)*val)
               for xy, val in next_rho.items() if val}
        survival.append(sum(val for (x,y),val in rho.items() if x == y))
        incoming = outgoing
    return survival


def exact_rows():
    rows = []
    for root in (1, -1):
        a = physical_survival(10, Fraction(0), root)
        if root == 1:
            require(a == free_prefixes(10), "free binomial prefix")
        for p in map(Fraction, (0, "1/5", "1/2", 1)):
            by_cut = composition_survival(a, p)
            direct = physical_survival(10, p, root)
            require(by_cut == direct, "composition and density matrix disagree")
            if p == 1:
                require(all(x == Fraction(1,2**j) for j,x in enumerate(direct)),
                        "fully copied source")
            for m in (2, 5, 10):
                rows.append(dict(root=root, p=str(p), m=m, success=str(direct[m]),
                                 no_copy_given_success=str((1-p)**m*a[m]/direct[m]),
                                 renewal_ticks=str(2*sum(direct[:m])/direct[m])))
    return rows


def free_survival_scaled(m, p):
    # Work with S_j/q^j. Rationalizing the radical can introduce an
    # extraneous pole for some p; this positive renewal avoids it.
    q = 1-p
    a = [1.]
    scaled = [1.]
    for j in range(1, m+1):
        a.append(a[-1]*(1-.5/j))
        convolution = math.fsum(a[k]*scaled[j-k] for k in range(1, j))
        scaled.append((a[j]+p*convolution)/q)
    logq = math.log1p(-p)
    survive = scaled[m] * math.exp(m*logq)
    return a[m], a[m]/scaled[m], math.log(scaled[m])+m*logq, (
        2*math.fsum(x*math.exp(j*logq) for j,x in enumerate(scaled))/survive)


def scaling_rows():
    rows = []
    for m in (16, 64, 256, 1024):
        for label, p in (("p=1/m", 1/m), ("p=m^-3/4", m**-.75),
                         ("p=1/sqrt(m)", m**-.5), ("p=1/5", .2)):
            a, clean, log_s, ticks = free_survival_scaled(m, p)
            row = dict(m=m, p=p, regime=label, no_copy_given_success=clean,
                       log_success=log_s, log_success_over_ideal=log_s-math.log(a),
                       mean_ticks_divided_by_4m=ticks/(4*m))
            if label == "p=1/sqrt(m)":
                row["limiting_clean_fraction"] = 1/(1+math.sqrt(math.pi)*math.e*math.erfc(-1))
            if label == "p=1/5":
                row["success_divided_by_fixed_p_asymptote"] = math.exp(
                    log_s+m*math.log1p(p)) * (1+p)/(2*p)
            rows.append(row)
    return rows


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    out = parser.parse_args().directory
    out.mkdir(exist_ok=True,parents=True)
    data = dict(exact=exact_rows(), zero_field_scaling=scaling_rows())
    with (out/"hidden_site_records.json").open("x",encoding="utf8",newline="\n") as handle:
        json.dump(data,handle,indent=2,allow_nan=False)
        handle.write("\n")
