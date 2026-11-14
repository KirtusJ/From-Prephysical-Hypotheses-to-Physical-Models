"""Replay a bin calibration using the walk, inverse and phased source. Standard library."""
import argparse
import cmath
import json
import math
from fractions import Fraction as Q
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def walk(state, inverse=False):
    n = len(state) // 2
    output = [0j] * (2 * n)
    root_two = math.sqrt(2)
    for x in range(n):
        right = 2 * ((x + 1) % n)
        left = 2 * ((x - 1) % n) + 1
        if inverse:
            a, b = state[right], state[left]
            output[2*x], output[2*x+1] = (a+b)/root_two, (a-b)/root_two
        else:
            a, b = state[2*x:2*x+2]
            output[right], output[left] = (a+b)/root_two, (a-b)/root_two
    return output


def three_ticks(state, inverse=False):
    for _ in range(3):
        state = walk(state, inverse)
    return state


def squared(values):
    return sum(abs(v)**2 for v in values)


def exact_phase(p):
    # x+i*y*sqrt(d), d=(1-x²), y=1. The returned phase is used for both masks.
    real = 1 - 1/(2*p)
    d = 1-real*real
    require(d >= 0, "single phase pair cannot separate this component")
    # Bad component is multiplied by 1+(e^iφ−1)[1+p(e^iφ−1)].
    # Compute its real and imaginary coefficients separately over the rationals.
    a, b = real-1, 1+p*(real-1)
    cancellation = [1+a*b-p*d, a*p+b]
    require(cancellation == [0,0], "exact complement cancellation")
    return real, d, cmath.rect(1, math.acos(float(real)))


def physically_separate(psi, support, p):
    real, d, phase = exact_phase(p)
    tagged = [v*phase if i in support else v for i,v in enumerate(psi)]
    source_frame = three_ticks(tagged, inverse=True)
    source_frame[0] *= phase
    final = three_ticks(source_frame)
    leakage = squared(v for i,v in enumerate(final) if i not in support)
    overlap = abs(sum(psi[i].conjugate()*final[i] for i in support))**2/float(p)
    require(leakage < 1e-26 and abs(overlap-1) < 2e-13, "three-tick flight calibration")
    return dict(p=str(p), cosine=str(real), sin_squared=str(d), exact_bad_coefficients=[0,0],
                direct_leakage_below_1e_minus_26=True, direct_overlap_with_projection_within_2e_minus_13=True)


def rare_calibrator(k):
    p = 2.0**(-k)
    theta = math.asin(math.sqrt(p))
    j = max(0, math.floor((math.pi/2-theta)/(2*theta)))
    g, b = math.sin(theta), math.cos(theta)
    for _ in range(j):
        g, b = (1-2*p)*g+2*math.sqrt(p*(1-p))*b, (1-2*p)*b-2*math.sqrt(p*(1-p))*g
    alpha = (2*j+1)*theta
    require(abs(g-math.sin(alpha))+abs(b-math.cos(alpha)) < 3e-12, "Grover rotation")
    if abs(b) >= 1e-13:
        c = -b*(1-2*p)/(2*g*math.sqrt(p*(1-p)))
        require(abs(c) <= 1+1e-12, "phase matching infeasible")
        phase = cmath.rect(1,math.acos(max(-1,min(1,c))))
        overlap = math.sqrt(p)*phase*g+math.sqrt(1-p)*b
        final_phase = 1-b/(math.sqrt(1-p)*overlap)
        require(abs(abs(final_phase)-1) < 4e-12, "source phase not unitary")
        b += (final_phase-1)*math.sqrt(1-p)*overlap
    require(abs(b)<1e-12,"residual in unwanted packet")
    return dict(p=str(Q(1,2**k)), ordinary_pairs=j, final_bad_norm_below_1e_minus_12=True)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory",type=Path)
    args=parser.parse_args()
    source=[0j]*32
    source[0]=1
    psi=three_ticks(source)
    # Numerators in the order R,L; x is represented modulo the sixteen-site ring.
    counts={-3:(0,1), -1:(-1,0), 1:(2,1), 3:(1,0)}
    expected=[0j]*32
    for x,(r,l) in counts.items():
        expected[2*(x%16):2*(x%16)+2] = [r/math.sqrt(8),l/math.sqrt(8)]
    require(max(abs(a-b) for a,b in zip(expected,psi))<1e-14,"direct path amplitudes")
    support={2,3}
    p=Q(5,8)
    bright=physically_separate(psi,support,p)
    dark=physically_separate(psi,set(range(32))-support,1-p)
    site_norms={x:Q(r*r+l*l,8) for x,(r,l) in counts.items()}
    alternative=site_norms[1]**2/sum(w*w for w in site_norms.values())
    require(alternative==Q(25,28) and alternative-p==Q(15,56),"spatial alternative")
    signed_pair=[p+Q(1,8),p-Q(1,8)]
    require(sum(signed_pair)/2==p and signed_pair[0]!=p,"sign-only loophole")
    result=dict(positions_R_L_numerators=counts,position_squared_norms={x:str(v) for x,v in site_norms.items()},
        bright_support=bright,dark_support=dark,random_bin_sign_rates=[str(p),str(p)],
        labels_per_eight_calibrator_preparations={"bright":5,"dark":3},
        normalized_square_of_site_norms=str(alternative),mixture_gap=str(alternative-p),
        phase_sensitive_counterexample=[str(v) for v in signed_pair],
        zero_and_one_bin="one supported ray only; test that boundary directly",
        phase_invariance_only_model="square of the total site mass before choosing rail",
        rare_branch_replays=[rare_calibrator(k) for k in (1,2,3,4,5,6,10,15,20)])
    args.directory.mkdir(parents=True,exist_ok=True)
    with (args.directory/"spatial_bin_response.json").open("x",encoding="utf8",newline="\n") as dst:
        json.dump(result,dst,indent=2)
        dst.write("\n")


if __name__=="__main__":
    main()
