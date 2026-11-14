"""A permanently driven physical walk, with one central coherent position aperture."""
import argparse
import json
import math
from fractions import Fraction
from pathlib import Path

import numpy as np


def require(test, message):
    if not test:
        raise ValueError(message)


def stream(right, left, lo, steps, order, s):
    # Arrays have spacing two, with lo the smallest departure position.
    # Each layer uses one staircase gain for both daughters at the well.
    phase = np.exp(-2j*np.pi*s*np.arange(order)/order)/math.sqrt(2)
    for _ in range(steps):
        kick = phase[(lo//2 + np.arange(right.size)) % order]
        r = np.zeros(right.size+1, dtype=np.complex128)
        l = np.zeros_like(r)
        r[1:] = (right+left)*kick
        l[:-1] = (right-left)*kick
        right,left = r,l
        lo -= 1
    return right,left,lo


def density(r,l):
    return abs(r)**2 + abs(l)**2


def sharp(steps, order, s, rail):
    return stream(np.array([int(rail==0)], complex), np.array([int(rail==1)], complex),
                  0, steps, order, s)


def cut(r,l,lo,size):
    x = lo+2*np.arange(len(r))
    keep = abs(x) <= size
    mass = density(r[keep],l[keep]).sum()
    require(mass > 0, "empty central aperture")
    return r[keep]/math.sqrt(mass), l[keep]/math.sqrt(mass), int(x[keep][0]), float(mass)


def sinc(z):
    return math.sin(z)/z if z else 1.


def fixed_cf(xi, s, kappa, time, radius):
    length = max(0., 2*radius-abs(time*xi))
    return (length/(2*radius)*sinc(xi*(1+time/kappa)*length/2)
            * math.cos(s*xi*time*(kappa+time)/2))


def pooled_position(r, l, n, order, s):
    # Translate the two sharp input columns to each measured well, then sum
    # probabilities. Both columns receive the same overall translation phase.
    rr, lr, _ = sharp(n, order, s, 0)
    rl, ll, _ = sharp(n, order, s, 1)
    right = np.convolve(abs(r)**2, density(rr, lr))
    left = np.convolve(abs(l)**2, density(rl, ll))
    cross = np.convolve(r*np.conj(l), rr*np.conj(rl)+lr*np.conj(ll))
    law = right+left+2*cross.real
    require(abs(law.sum()-1) < 2e-10 and law.min() >= -2e-13,
            "pooled site probabilities")
    return law


def direct_pool(r, l, lo, n, order, s):
    # Independent small-order control, with the actual two-rail spinor at
    # its measured input well and every departure phase recomputed there.
    result = np.zeros(len(r)+n)
    for j, (a, b) in enumerate(zip(r, l)):
        er, el, _ = stream(np.array([a]), np.array([b]), lo+2*j, n, order, s)
        result[j:j+n+1] += density(er, el)
    return result


def count_comparison(t, first_site, last_site, n, terminal_limit):
    # The fair count component branches into two positive equiprobable
    # histories at every tick. Prefix sums preserve exact integer counts.
    prefix = [0]
    for j in range(n+1):
        prefix.append(prefix[-1]+math.comb(n, j))
    require(prefix[-1] == 2**n, "count flight denominator")
    accepted = joint = 0
    for x in range(first_site, last_site+1, 2):
        histories = math.comb(t, (x+t)//2)
        accepted += histories
        # -terminal_limit <= x+2j-n <= terminal_limit.
        jmin = max(0, (n-x-terminal_limit+1)//2)
        jmax = min(n, (n-x+terminal_limit)//2)
        if jmin <= jmax:
            joint += histories*(prefix[jmax+1]-prefix[jmin])
    require(0 < accepted <= 2**t and 0 <= joint <= accepted*2**n, "count bounds")
    passage = Fraction(accepted, 2**t)
    terminal = Fraction(joint, accepted*2**n)
    return dict(exact_pass=str(passage), pass_probability=float(passage),
                exact_joint_compact=str(Fraction(joint, 2**(t+n))),
                exact_compact_given_pass=str(terminal), compact_given_pass=float(terminal))


def count_scalings():
    # Exact source-only controls across shrinking, order-one and broad windows.
    records = []
    for t in (64, 256, 1024, 4096):
        for name, width in (("narrow", math.isqrt(math.isqrt(t))),
                            ("unit", math.isqrt(t)),
                            ("broad", math.isqrt(t)*math.isqrt(math.isqrt(t)))):
            limit = width - (width-t) % 2
            tally = sum(math.comb(t, (x+t)//2) for x in range(-limit,limit+1,2))
            exact = Fraction(tally, 2**t)
            u = width/math.sqrt(t)
            records.append(dict(t=t, regime=name, radius=width, actual_parity_limit=limit,
                                width_over_sqrt_t=u, exact_pass=str(exact),
                                pass_probability=float(exact), normal_window=math.erf(u/math.sqrt(2)),
                                narrow_window_leading=math.sqrt(2/math.pi)*u))
    return records


def trial(order,s,rail,regime):
    fixed = regime == "fixed"
    delta = (math.pi/order)**(1/(3 if fixed else 4))
    pitch = delta if fixed else delta**2
    tau = delta**2 if fixed else delta**3
    t = round(1/tau) if fixed else round(delta**(-9/4))
    n = round(.75/tau)
    kappa, time = t*tau, n*tau
    halfwidth = 1/delta if fixed else t*delta**(17/16)
    require(t+n<2*order, "unwrapped source and flight")
    r,l,lo=sharp(t,order,s,rail)
    require(abs(density(r,l).sum()-1)<2e-10, "source norm")
    r,l,lo,survival = cut(r,l,lo,halfwidth)
    source_x = lo+2*np.arange(len(r))
    if fixed:
        targets = [1.,3.]
        predicted = [fixed_cf(x,s,kappa,time,1.) for x in targets]
    else:
        targets = [1.,3.]
        predicted = [math.cos(s*x*time**2/2) for x in targets]
    pooled = pooled_position(r, l, n, order, s)
    er,el,end = stream(r,l,lo,n,order,s)
    d = density(er,el)
    xx = pitch*(end+2*np.arange(len(d)))
    require(abs(d.sum()-1)<2e-10, "released norm")
    cf = [np.sum(d*np.exp(1j*x*xx)) for x in targets]
    pooled_cf = [np.sum(pooled*np.exp(1j*x*xx)) for x in targets]
    # The normalization and bin wavenumbers use actual rounded clocks.
    rows = [dict(xi=x, coherent=[float(y.real),float(y.imag)],
                 predicted=z,coherent_error=float(abs(y-z)),
                 site_copied=[float(e.real),float(e.imag)])
            for x,y,z,e in zip(targets,cf,predicted,pooled_cf)]
    limit = math.floor(2/pitch)
    compact = abs(end+2*np.arange(len(d))) <= limit
    count = count_comparison(t, int(source_x[0]), int(source_x[-1]), n, limit)
    a = halfwidth/math.sqrt(t)
    count['halfwidth_over_sqrt_t'] = a
    count['normal_window_comparison'] = math.erf(a/math.sqrt(2))
    control = None
    if order == 127:
        direct = direct_pool(r,l,lo,n,order,s)
        control = dict(max_pointwise_error=float(np.max(abs(direct-pooled))),
                       compact_error=float(abs(direct[compact].sum()-pooled[compact].sum())))
        require(max(control.values()) < 2e-12, "direct site-by-site dephasing")
    return dict(M=order,s=s,rail=rail,regime=regime,delta=delta,
                source_ticks=t,flight_ticks=n,source_time=kappa,flight_time=time,
                requested_halfwidth=halfwidth,occupied_wells=len(source_x),
                pass_probability=survival,pass_over_asymptote=survival/(2*halfwidth/(math.pi*t)),
                characteristic=rows, count=count,
                compact=dict(radius=2., last_lattice_site=limit,
                             coherent_given_pass=float(d[compact].sum()),
                             copied_given_pass=float(pooled[compact].sum()),
                             coherent_joint=float(survival*d[compact].sum()),
                             copied_joint=float(survival*pooled[compact].sum())),
                direct_dephasing_control=control)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory",type=Path)
    dest=parser.parse_args().directory
    rows=[]
    for regime,orders in (("fixed",(127,512,2048,8191,32768)),
                          ("shrinking",(127,512,2048,8191))):
        for order in orders:
            for s,rail in ((1,0),(-1,0),(0,0),(1,1)):
                rows.append(trial(order,s,rail,regime))
    for i in range(0,len(rows),4):
        right,conj,zero,left=rows[i:i+4]
        for j in range(2):
            def c(row): return complex(*row["characteristic"][j]["coherent"])
            require(abs(c(right)-c(conj))<1e-10, "conjugate position law")
            require(abs(c(right)-c(left).conjugate())<1e-10, "start rail reflection")
        require(zero["pass_probability"]>0, "zero-field control")
    dest.mkdir(parents=True,exist_ok=True)
    with (dest/"central_window_flight.json").open("x",encoding="utf8",newline="\n") as f:
        json.dump(dict(scope="Model trials. Coherent and site-copied terminal probabilities are "
                       "conditional on the aperture unless marked joint. Count probabilities use "
                       "exact fair binomial words; normal-window comparisons are approximations. "
                       "The site read retains the post-read rail spinor at each selected well.",
                       rows=rows, extra_count_scalings=count_scalings()),f,indent=2,allow_nan=False)
        f.write("\n")


if __name__=="__main__":
    main()
