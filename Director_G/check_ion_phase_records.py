"""Replay the two-clock comparison from the authors' six pinned ion GST count files.

python -B check_ion_phase_records.py OUTPUT_DIRECTORY [--inputs ExperimentalData]
The input directory is optional. Otherwise fetch public source blobs at the pinned commit.
"""
import argparse
from collections import defaultdict
from decimal import Decimal
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import re
from urllib.request import urlopen


COMMIT = "fc939f90f7a2b32a20aec34f36465259f38837a3"
REMOTE = f"https://raw.githubusercontent.com/pyGSTio/supplemental-info-arXiv-1605.07674/{COMMIT}/ExperimentalData/"
SOURCES = {
    "2014_04_17-compensatedTraining.txt": "77d0da7bba7c9a54f5e79fb8e2c00f962d5ea75be72b770f08c7c5d729656d99",
    "2014_12_02-GSTCompensatedDrift_randomized_condensed.txt": "2a3536a2078373e4808d83fed147a3f8eff140d2ee866a1a9fcda2cc36801910",
    "2015_02_09-GSTCompensatedDrift_condensed.txt": "d76439b88c30559421c7170a0706b0f1afed2be50fe9d2056c449dcf6bb7897c",
    "2015_03_02-GST_condensed.txt": "3a03ba695f57f4e098d350b61659d3ca1804e90407e0ccd10764efd701bdd4c1",
    "2015_03_19-GSTBest_condensed.txt": "4f2053233f282cabe65bd587d64688f7c16d4e7d52357da8ee66edd419178be1",
    "2015_03_30-GST_BB1_XYXY_8192_condensed.txt": "5ca509cb8e6cfe8996b8a1339457bc7f96d4efe0a3bdb8b550c3c496ce53f686",
}
BLOCKS = {"Y": ("Gy",-1), "YX": ("GyGx",0), "XY": ("GxGy",0)}
SELECT = {"{}", "GxGx", "GyGyGyGy"} | {b*k for b,_ in BLOCKS.values() for k in (1,2,3)}


def require(ok, why):
    if not ok:
        raise ValueError(why)


def read_rows(filename, folder):
    if folder is None:
        with urlopen(REMOTE+filename, timeout=30) as response:
            data = response.read()
    else:
        data = (folder/filename).read_bytes()
    require(hashlib.sha256(data).hexdigest()==SOURCES[filename], "input digest "+filename)
    rows = defaultdict(list)
    for line, row in enumerate(data.decode("utf8").splitlines(), 1):
        if not row.strip() or row.startswith("#"):
            continue
        word, plus, total, *other = row.split()
        # The longest selected word has six gates. No positive factor longer than it fits.
        def expand(match):
            primitive, power = match.groups()
            return primitive * min(int(power), 7)
        full = re.sub(r"\(((?:G[ixy])+)\)\^(\d+)", expand, word)
        if full not in SELECT:
            continue
        k,n = Decimal(plus), Decimal(total)
        require(k==int(k) and n==int(n) and 0<=k<=n and n>0, "bad counts")
        rows[full].append(dict(line=line, label=word, plus=int(k), total=int(n),
                               trailing_fields=other))
    return {word:rows[word] for word in sorted(SELECT)}


def pooled(rows):
    k = sum(r["plus"] for r in rows)
    n = sum(r["total"] for r in rows)
    return k,n


def upper(k, n, alpha):
    """One-sided Clopper-Pearson upper endpoint by binomial-CDF inversion."""
    if k==n:
        return 1.0
    low, high = 0.0, 1.0
    lc = [math.lgamma(n+1)-math.lgamma(j+1)-math.lgamma(n-j+1) for j in range(k+1)]
    for _ in range(50):
        p = (low+high)/2
        lp, lq = math.log(p), math.log1p(-p)
        cdf = sum(math.exp(v+j*lp+(n-j)*lq) for j,v in enumerate(lc))
        if cdf > alpha:
            low = p
        else:
            high = p
    return high


def bounded_zero(rows, family):
    # For m=0, W=2(1-p3)=(q3-q0)/(q1-q0). Assume one stable, informative
    # bright-response channel with q1>q0. Four one-sided limits allow for an uncertain calibration contrast.
    (k0,n0),(k1,n1),(k3,n3) = (pooled(r) for r in rows)
    alpha4 = 0.05/(4*family)
    l0,u0 = max(0.,1-upper(n0-k0,n0,alpha4)),upper(k0,n0,alpha4)
    l1,u3 = max(0.,1-upper(n1-k1,n1,alpha4)),upper(k3,n3,alpha4)
    certified = None if l1<=u0 else max(0.,(u3-l0)/(l1-u0))
    return dict(CP_sides_each_alpha=alpha4, q0_lower=round(l0,9), q0_upper=round(u0,9),
                q1_lower=round(l1,9),q3_upper=round(u3,9),
                W_upper_95=None if certified is None else math.ceil(certified*10**8)/10**8)


def analyze(rows, block, m):
    clocks = [rows["{}"]] + [rows[block*k] for k in (1,2,3)]
    if not all(clocks):
        return {"missing_clocks":[t for t,rs in enumerate(clocks) if not rs]}
    q = [Fraction(*pooled(rs)) for rs in clocks]
    contrast = q[1]-q[0]
    require(contrast!=0, "zero point contrast in this archived run")
    p = [1-(v-q[0])/(2*contrast) for v in q]
    w = 2*(1-p[3])-2*m*(2*p[2]-1)+m*m
    ideal = 2*q[3]-2*m*(1-2*q[2])+m*m
    out = dict(bright=list(map(str,q)), fitted_bright_given_R=str(q[0]),
               fitted_bright_given_L=str(2*q[1]-q[0]),
               calibrated_R_at_2_3=list(map(str,p[2:])), calibrated_W=str(w),
               ideal_classifier_W=str(ideal))
    detector_b = 2*q[1]-q[0]
    check_controls = {}
    for word in ("GxGx", "GyGy", "GyGyGyGy"):
        if not rows[word]:
            continue
        observed = Fraction(*pooled(rows[word]))
        predicted = q[0] if word=="GyGyGyGy" else detector_b
        check_controls[word] = dict(measured_bright=str(observed), observed_minus_prediction=str(observed-predicted))
    out["other_nominal_R_L_controls"] = check_controls
    if m==0:
        triple = [clocks[j] for j in (0,1,3)]
        out["per_run_binomial_bound"] = bounded_zero(triple, 1)
        out["six_date_simultaneous_bound"] = bounded_zero(triple, 6)
    return out


def classical_order_test(rows):
    """Exact conditional lower tail for q3 >= q2 given all recorded bright counts."""
    k2,n2 = pooled(rows["GyGx"*2])
    k3,n3 = pooled(rows["GyGx"*3])
    bright = k2+k3
    denom = math.comb(n2+n3, bright)
    numer = sum(math.comb(n3,j)*math.comb(n2,bright-j)
                for j in range(max(0,bright-n2),k3+1))
    require(k3*n2 < k2*n3,"expected sign of the observed order test")
    return dict(two_block_bright=[k2,n2],three_block_bright=[k3,n3],
                exact_tail=str(Fraction(numer,denom)),
                log10_tail=round(math.log10(numer)-math.log10(denom),6))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output",type=Path)
    parser.add_argument("--inputs",type=Path)
    args = parser.parse_args()
    reports=[]
    for name in SOURCES:
        rows=read_rows(name,args.inputs)
        reports.append(dict(filename=name,sha256=SOURCES[name],selected=rows,
                            classical_two_state=classical_order_test(rows),
                            blocks={key:analyze(rows,b,m) for key,(b,m) in BLOCKS.items()}))
    require(len(reports)==6,"run count")
    end = reports[-1]["blocks"]["YX"]
    require(end["bright"]==["0","23/50","29/50","0"] and end["calibrated_W"]=="0",
            "final run coordinate, denominators and calibration")
    require(reports[0]["selected"]["GyGx"*3][1]["plus"]==23,"duplicate April entry")
    require(sum("missing_clocks" in r["blocks"]["XY"] for r in reports)==5,"reverse order absences")
    data=dict(source_commit=COMMIT,plus_label="outcome |1>; return R is |0>",
              block_labels={"Y":"Gy","YX":"GyGx","XY":"GxGy"},
              denominators="per reported circuit repetitions; shared-rate duplicates pooled within date only",
              intervals="per date and selected word under binomial repeats, four simultaneous one-sided endpoints",
              runs=reports)
    args.output.mkdir(exist_ok=True,parents=True)
    with (args.output/"ion_phase_records.json").open("x",encoding="utf8",newline="\n") as handle:
        json.dump(data,handle,indent=2,allow_nan=False)
        handle.write("\n")


if __name__ == "__main__":
    main()
