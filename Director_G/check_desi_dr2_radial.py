"""Profile the released DESI DR2 Gaussian likelihood on its six radial coordinates."""
from argparse import ArgumentParser
from hashlib import sha256
import json
from math import exp, sqrt
from pathlib import Path

import numpy as np


RELEASE = "b7b8a36e9bccb063081f811f323cada21ab5fbdd"
STEM = "desi_gaussian_bao_ALL_GCcomb_"
HASHES = {
    "mean": "9ac154ab583ce759c0f7eef3c978c7c70a6ead2d18774caceadf1a350a640585",
    "cov": "252a143274c8a07c78694c119617d36594f6d7965d00319ca611c6ffb886e509",
}
TRACERS = ("LRG1","LRG2","LRG3+ELG1","ELG2","QSO","Lya")


def require(value, message):
    if not value:
        raise ValueError(message)


def read_input(directory, key):
    raw = (directory / (STEM + key + ".txt")).read_bytes()
    require(sha256(raw).hexdigest() == HASHES[key], "upstream digest mismatch: " + key)
    return raw.decode("ascii").splitlines()


def fit(z, observed, covariance, radiation):
    inverse = np.linalg.inv(covariance)
    x = (1+z)**3 - 1
    rad = radiation*((1+z)**4 - 1)

    def profile(matter):
        shape = 1/np.sqrt(1 + matter*x + rad)
        metric_shape = inverse@shape
        scale = (observed@metric_shape)/(shape@metric_shape)
        # All measured data and fitted scales here are positive. The closed
        # physical amplitude domain also admits zero as a limiting model.
        scale = max(0., float(scale))
        predicted = scale*shape
        residual = observed-predicted
        chi2 = float(residual@inverse@residual)
        return chi2, scale, predicted, residual

    grid = np.linspace(0.,1-radiation,1001)
    scores = [profile(m)[0] for m in grid]
    candidates = [float(grid[0]), float(grid[-1])]
    for i in range(1, len(grid)-1):
        if scores[i] > scores[i-1] or scores[i] >= scores[i+1]:
            continue
        lo,hi = grid[i-1],grid[i+1]
        for _ in range(64):
            left,right = (2*lo+hi)/3, (lo+2*hi)/3
            if profile(left)[0] < profile(right)[0]:
                hi = right
            else:
                lo = left
        candidates.append(float((lo+hi)/2))
    matter = min(candidates, key=lambda m: profile(m)[0])
    chi2, scale, predicted, residual = profile(matter)
    return {
        "radiation_fraction_fixed": radiation, "matter_fraction": matter,
        "scale_c_over_H0rd": scale, "A": 1/scale**2, "B": matter/scale**2,
        "chi2": chi2, "predicted":predicted.tolist(), "observed_minus_fit":residual.tolist(),
        "residual_over_marginal_sd":(residual/np.sqrt(np.diag(covariance))).tolist(),
        "closed_matter_domain_endpoint_chi2": [scores[0],scores[-1]],
    }


def run(directory):
    rows = [line.split() for line in read_input(directory,"mean") if not line.startswith("#")]
    full = np.loadtxt(read_input(directory,"cov"))
    require(len(rows) == 13 and full.shape == (13,13) and np.array_equal(full,full.T),
            "release shape and covariance symmetry")
    np.linalg.cholesky(full)
    indices = [i for i,row in enumerate(rows) if row[2] == "DH_over_rs"]
    require(indices == [2,4,6,8,10,11], "radial labels, including reversed Ly-alpha port order")
    z, observed = np.array([[float(rows[i][0]), float(rows[i][1])] for i in indices]).T
    covariance = full[np.ix_(indices,indices)]
    require(np.count_nonzero(covariance-np.diag(np.diag(covariance))) == 0,
            "released radial cross-bin covariance changed")
    joint_precision = np.linalg.inv(full)
    conditioned = np.linalg.inv(joint_precision[np.ix_(indices,indices)])
    require(np.all(np.diag(conditioned) < np.diag(covariance)), "conditioning control")
    fits = [fit(z,observed,covariance,r) for r in (0.,0.00005,0.00010,0.00020)]
    baseline = fits[0]
    require(0 < baseline["B"] < baseline["A"] and baseline["chi2"] <
            min(baseline["closed_matter_domain_endpoint_chi2"]), "physical interior fit")
    # Noise-free pure vacuum, matter-only and a known interior solution.
    for m in (0.,0.31,1.):
        pure = 28/np.sqrt(1+m*((1+z)**3-1))
        recovered = fit(z,pure,covariance,0.)
        require(abs(recovered["matter_fraction"]-m) < 1e-7 and recovered["chi2"] < 1e-15,
                "noiseless limit")
    # Rescaling all distance data and their covariance together preserves shape and chi-square.
    rescaled = fit(z,3*observed,9*covariance,0.)
    require(abs(rescaled["chi2"]-baseline["chi2"]) < 1e-8 and
            abs(rescaled["matter_fraction"]-baseline["matter_fraction"]) < 1e-7 and
            abs(rescaled["scale_c_over_H0rd"]/baseline["scale_c_over_H0rd"]-3) < 1e-7,
            "distance-unit control")
    h = baseline["chi2"]/2
    sd = np.sqrt(np.diag(covariance))
    for entry in fits:
        correction = entry["radiation_fraction_fixed"]*((1+z)**4-1)
        matter_term = baseline["matter_fraction"]*((1+z)**3-1)
        unchanged = baseline["scale_c_over_H0rd"]/np.sqrt(1+matter_term+correction)
        entry["max_abs_shift_over_sd_at_fixed_baseline_parameters"] = float(
            max(abs(unchanged-np.array(baseline["predicted"]))/sd))
        entry["max_abs_shift_over_sd_after_refit"] = float(
            max(abs(np.array(entry["predicted"])-np.array(baseline["predicted"]))/sd))
    return {"release_commit":RELEASE, "sha256":HASHES,"zero_based_rows":indices,
            "tracers":TRACERS, "z":z.tolist(),"observed_DH_over_rd":observed.tolist(),
            "radial_marginal_covariance":covariance.tolist(),
            "radial_marginal_sd":sd.tolist(),
            "radial_sd_conditioning_on_all_omitted_coordinates":np.sqrt(np.diag(conditioned)).tolist(),
            "fits":fits,"baseline_asymptotic_chi_square_4_upper_tail":exp(-h)*(1+h)}


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("output",type=Path)
    parser.add_argument("--inputs",type=Path,
                        default=Path(__file__).resolve().parent/"results"/"desi_dr2_radial_source")
    options = parser.parse_args()
    result = run(options.inputs)
    with options.output.open("x",encoding="utf8",newline="\n") as out:
        json.dump(result,out,indent=2,allow_nan=False)
        out.write("\n")
