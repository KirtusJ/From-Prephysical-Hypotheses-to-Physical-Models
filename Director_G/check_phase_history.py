"""Three monitored Hadamard flights from a localized maximally mixed coin.

Compare a site measurement followed by diag(1,i) with a site measurement
that also dephases R/L. Every displacement zero is kept. Exact dyadic
arithmetic, standard library. Example: python -I check_phase_history.py 3 16.
"""
import argparse
from fractions import Fraction
from itertools import product
from math import sqrt
from pathlib import Path
from runpy import run_path


def require(value, message):
    if not value:
        raise AssertionError(message)


def multiply(a, b):
    return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]


def instrument(weights, quarter):
    """Maps sign-bin to its integer 4x4 superoperator; denominator 2^ticks.
    Coordinates A, B, D, C represent [[A,B+iD],[B-iD,C]].
    diag(1,i) sends B+iD to D-iB after each measured flight.
    """
    bins = {s:[[0]*4 for _ in range(4)] for s in (-1,0,1)}
    for disp,(a,b,c,d) in weights.items():
        row_a = [a*a,2*a*b,0,b*b]
        row_b = [a*c,a*d+b*c,0,b*d]
        row_c = [c*c,2*c*d,0,d*d]
        row_i = [0,0,a*d-b*c,0]
        after = ([row_a,row_i,[-v for v in row_b],row_c] if quarter
                 else [row_a,[0]*4,[0]*4,row_c])
        action = bins[(disp>0)-(disp<0)]
        for i in range(4):
            for j in range(4):
                action[i][j] += after[i][j]
    return bins


def sign_law(flights,quarter):
    ops = [instrument(board,quarter) for board in flights]
    hist = {(): [[1],[0],[0],[1]]}
    for op in ops:
        nxt = {}
        for prefix,rho in hist.items():
            for sign, action in op.items():
                nxt[prefix+(sign,)] = multiply(action,rho)
        hist = nxt
    return {bits: rho[0][0]+rho[3][0] for bits,rho in hist.items()}


def brute_words(steps):
    """Sum signed words explicitly for BOTH input rails, independently of kernel recurrence."""
    result = {}
    for word in product((0,1),repeat=steps):
        pos = sum(1 if r==0 else -1 for r in word)
        m = result.setdefault(pos,[[0,0],[0,0]])
        for incoming in (0,1):
            prev,amp = incoming,1
            for rail in word:
                if rail==prev==1:
                    amp=-amp
                prev=rail
            m[word[-1]][incoming] += amp
    return result


def brute_joint(lengths,quarter):
    """Sum each resolved site history in chronological order, then pool signs.
    The tiny-clock oracle uses integer-valued Gaussian amplitudes; its
    magnitudes stay below 2^53 so Python complex arithmetic is exact.
    """
    require(max(lengths)<=5 and sum(lengths)<=12,"oracle magnitude limit")
    walks = [brute_words(n) for n in lengths]
    bins = {bits:0 for bits in product((-1,0,1),repeat=3)}
    for path in product(*(w.items() for w in walks)):
        signs = tuple((x>0)-(x<0) for x,_ in path)
        for initial in [(1,0),(0,1)]:
            branches = [initial]
            for step,(_,m) in enumerate(path):
                new = []
                for R,L in branches:
                    r,s = m[0][0]*R+m[0][1]*L, m[1][0]*R+m[1][1]*L
                    if step==2:
                        power = r.real*r.real+r.imag*r.imag+s.real*s.real+s.imag*s.imag
                        bins[signs] += int(power)
                    elif quarter:
                        new.append((r,1j*s))
                    else:
                        new.extend([(r,0),(0,s)])
                branches = new
    return bins


def pair(hist,i,j):
    return {(s,t):sum(c for tags,c in hist.items() if tags[i]==s and tags[j]==t)
            for s,t in product((-1,0,1),repeat=2)}


def turns(counts):
    return tuple(sum(n for (x,y),n in counts.items() if (x*y>0,x*y<0,x*y==0)[idx])
                 for idx in range(3))


def verify(lengths,kernels,oracle=False):
    flights = [kernels(n) for n in lengths]
    total = 2 << sum(lengths)  # unweighted I in the numerator, I/2 in the law
    # Summing all observed positions of a localized I/2 state leaves I/2:
    # unitality follows also from the unitary Fourier fibers.
    for n,board in zip(lengths,flights):
        for quarter in [False,True]:
            ops = instrument(board,quarter)
            residual = [sum(m[i][0]+m[i][3] for m in ops.values()) for i in range(4)]
            require(residual==[2**n,0,0,2**n],"unconditional maximally mixed coin")
    # Full signed displacement pairs, independent of sign pooling. The
    # post-read real off-diagonal for either protocol is zero from I/2.
    # Only the quarter has an imaginary part. A real next kernel gives
    # coefficient zero to that component in its trace. Independently
    # build the two cell traces via the two different amplitude formulas.
    for current,following in zip(flights,flights[1:]):
        for a,b,c,d in current.values():
            for u,v,w,z in following.values():
                dephase = (u*u+w*w)*(a*a+b*b)+(v*v+z*z)*(c*c+d*d)
                # Frobenius norm squared of T_y diag(1,i) T_x, summed
                # over the two equally populated input rails.
                rotate = sum(h*h for h in (u*a,v*c,u*b,v*d,w*a,z*c,w*b,z*d))
                require(dephase==rotate,"full adjacent displacement law")
    dephased, rotated = [sign_law(flights,mode) for mode in (False,True)]
    require(sum(dephased.values())==sum(rotated.values())==total, "incident mass")
    require(min(dephased.values())>=0 and min(rotated.values())>=0,"negative bin")
    for i in (0,1):
        require(pair(dephased,i,i+1)==pair(rotated,i,i+1),"adjacent sign-pair differs")
    if len(set(lengths))==1:
        require(pair(rotated,0,1)==pair(rotated,1,2),"stationary adjacent bins differ")
    if oracle:
        require(brute_joint(lengths,True)==rotated, "explicit rotated path words")
        require(brute_joint(lengths,False)==dephased,"explicit dephased path words")
    return total,dephased,rotated


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("lengths",nargs="*",type=int,help="one equal-flight clock per argument")
    parser.add_argument("--counts",action="store_true",help="print exact incident and event counts")
    options=parser.parse_args()
    ns=options.lengths or [3,16,64,256]
    if min(ns)<1:
        parser.error("all flight lengths must be positive")
    # Resolve the sibling even under python -I, which omits the script
    # directory from sys.path. No third-party or package installation needed.
    kernels=run_path(str(Path(__file__).with_name("check_velocity_collisions.py")))["kernels"]
    for lengths in [(1,2,3),(3,3,3),(3,4,5)]:
        verify(lengths,kernels,oracle=True)
    print("clock read pair same opposite tie" + (" | incident counts" if options.counts else ""))
    for n in ns:
        total,dephased,rotated=verify([n]*3,kernels)
        for tag,h in [("dephased",dephased),("quarter",rotated)]:
            for label,i,j in [("adjacent",0,1),("lag-two",0,2)]:
                counts=turns(pair(h,i,j))
                rates=" ".join(f"{float(Fraction(k,total)):.10f}" for k in counts)
                print(n,tag,label,rates,*(["|",total,*counts] if options.counts else []))
    c=1-1/sqrt(2)
    print(f"continuum lag-two same: dephased={.5+c/8:.10f} quarter={.5+(3*c-1)/8:.10f}")


if __name__=="__main__":
    main()
