"""Exact rank and physical replay for unfiltered terminal well measurements."""
import argparse
import json
from fractions import Fraction
from math import comb, gcd
from pathlib import Path

from check_character_tomography import Rank, reduced
from check_fixed_ring_moments import at_port, check, direct_read, physical, run_count


def left_rail(t, left):
    if left == 0:
        return 0
    return sum((-1)**(left-r)*comb(left-1,r-1)*comb(t-left,r-1)
               for r in range(1,min(left,t-left+1)+1))


def site_row(d, q, t, x):
    """Return physical count and its differences from coherent cosine scores.

    Row variables are total coherent mass, then its cosine moments at lags 1..K.
    """
    m = q//gcd(q,d)
    l0 = ((t-x)//2)%d
    ls = range(l0,t+1,d)
    right = [run_count(t,l) for l in ls]
    left = [left_rail(t,l) for l in ls]
    count = sum(comb(t,l) for l in ls)
    row = [-count]+[0]*(m//2)
    for h in range(len(right)):
        ac = sum(right[i]*right[i+h]+left[i]*left[i+h] for i in range(len(right)-h))
        j = h%m
        row[min(j,m-j)] += (2 if h else 1)*ac
    return count,row


def gap_moments(d,q,t,x):
    """Compare every character including its conjugate in the physical cyclotomic basis."""
    fair,row = site_row(d,q,t,x)
    signals = []
    for s in range(q):
        p = [2*fair]+[0]*(q-1)
        for h,coef in enumerate(row):
            p[(h*d*s)%q] += coef
            p[(-h*d*s)%q] += coef
        rem = reduced(p,q)
        check(all(v%2==0 for v in rem),"integral physical rate")
        signals.append([v//2 for v in rem])
    return fair,signals


def census(d,q,physical_replay=False):
    k = q//gcd(q,d)//2
    # Do not give the search the claimed answer.
    rank, semicircle = Rank(), Rank()
    history, window_history, native = [], [], []
    t = 0
    while len(rank.rows) < k+1:
        t += 1
        window = [0]*(k+1)
        for x in range(t%2,2*d,2):
            _,row = site_row(d,q,t,x)
            rank.enter(row,(t,x))
            if x<d:
                window = [a+b for a,b in zip(window,row)]
        semicircle.enter(window,t)
        history.append(len(rank.rows))
        window_history.append(len(semicircle.rows))
    if physical_replay:
        for tick, state in physical(d,q,set(range(1,t+1))):
            site_rows = []
            for x in range(tick%2,2*d,2):
                fair, signals = gap_moments(d,q,tick,x)
                actual = []
                for rail in range(2):
                    a,c = at_port(state,q,x,rail)
                    actual.append((a,c))
                check(fair==sum(c for _,c in actual),"fair physical rate")
                for s in range(q):
                    w = [int(i==s) for i in range(q)]
                    terms = [direct_read(q,a,c,w,0) for a,c in actual]
                    p = [0]*q
                    for term in terms:
                        for i,v in enumerate(term):
                            p[i] += v
                    check(reduced(p,q)==signals[s],"summed physical rail rates")
                site_rows.append(dict(x=x,fair=fair,characters=signals))
            native.append(dict(t=t,sites=site_rows))
    expected = (2*k+3) if d==2 else max(3,k*d+1)
    check(t==expected,"optimal maximum clock")
    check(len(semicircle.rows)==k+1,"fixed contiguous semicircle rank")
    return dict(D=d,q=q,effective=q//gcd(q,d),earliest_full_clock=t,
                ranks_after_each_clock=history,witnesses=rank.witness,
                fixed_window_ranks=window_history,fixed_window_witness_clocks=semicircle.witness,
                physical_rows=native)


def four_well_inverse():
    # The fixed detector always accepts the adjacent pair {0,1}.
    # x=1 is reachable at clocks 3 and 5. Fair is the last entry.
    a,b = [gap_moments(2,3,t,1) for t in (3,5)]
    rows = [[s[0] for s in coeff]+[count] for count,coeff in (a,b)]
    check(rows==[[8,5,5,4],[16,7,7,16]],"same physical window, two clocks")
    outputs = []
    for w in ((1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1),(1,2,3,4)):
        reads = [Fraction(sum(x*y for x,y in zip(row,w)),sum(w)*2**t)
                 for t,row in zip((3,5),rows)]
        p3,p5 = reads
        pair = (16-32*p5)/9
        trivial = (8*p3-4-pair)/4
        count = 1-pair-trivial
        recovered = [trivial,pair,count]
        check(recovered==[Fraction(v,sum(w)) for v in (w[0],w[1]+w[2],w[3])],"inverse")
        outputs.append(dict(input_units=w,rates=list(map(str,reads)),
                            recovered=list(map(str,recovered))))
    return outputs


def four_well_kernel():
    """Check the signed-kernel polynomial on exact rational cosine nodes."""
    kmax = 14
    # X_(2k+1) and X_(2k+2) have degree <=k, so >=k+1 nodes suffice.
    nodes = [Fraction(j,kmax) for j in range(kmax+1)]
    for a in nodes:
        cosines = [1,1-2*a]
        for k in range(2,kmax+1):
            cosines.append(2*(1-2*a)*cosines[-1]-cosines[-2])
        prior = []
        for k in range(kmax+1):
            for t in (2*k+1,2*k+2):
                # q=4kmax+2 leaves every lag through kmax unfolded.
                fair,row = site_row(2,4*kmax+2,t,t%4)
                bias = 2*(fair+sum(v*c for v,c in zip(row,cosines)))/Fraction(1<<t)-1
                if t%2:
                    prior.append(bias)
                else:
                    check(bias==prior[-1],"paired even clock")
            g = [1,a,2-2*a,a,1]
            coeff = sum(g[j]*prior[k-j] for j in range(min(k,4)+1))
            check(coeff==([0,a-1,-a,-1][k] if k<4 else 0),"kernel numerator")
    fake = [Fraction(1)]
    for k in range(1,kmax+1):
        t=2*k+1
        _,row=site_row(2,4*kmax+2,t,t%4)
        fake.append(-sum(row[j]*fake[j] for j in range(k))/row[k])
    check(all(a>b for a,b in zip(fake,fake[1:])),"signed fair moments")
    return dict(maximum_degree=kmax,rational_nodes=list(map(str,nodes)),
                signed_formal_count_cosine_moments=list(map(str,fake)))


def main():
    cmd = argparse.ArgumentParser(description=__doc__)
    cmd.add_argument("output",type=Path)
    out = cmd.parse_args().output
    native_cases = [(2,q) for q in (1,2,3,4,5,7,8,12)]+[(3,3),(3,4),(4,5),(5,8)]
    panels = [census(d,q,True) for d,q in native_cases]
    # A separate full rank history for every effective order m=1..64.
    # D=2 and q=2m realize every such m. The source-order sweep retains all cases.
    timing = [census(2,2*m) for m in range(1,65)]
    tiny = []
    for t,state in physical(1,3,set(range(1,9))):
        x=t%2
        pairs=[at_port(state,3,x,r) for r in range(2)]
        check(sum(c for _,c in pairs) == 1<<t,"two-well fair parity")
        for s in range(3):
            w = [int(i==s) for i in range(3)]
            p = [0]*3
            for a,c in pairs:
                for i,v in enumerate(direct_read(3,a,c,w,0)):
                    p[i] += v
            check(reduced(p,3)==[1<<t],"two-well blindness")
        tiny.append([t,x])
    data = dict(scope="Unfiltered C2 x Cq walk, initial (0,R). All original-launch site "
                      "numerators use denominator 2^t. Each character is encoded modulo Phi_q. "
                      "The rank test uses total coherent weight and its K folded cosine moments.",
                four_well_fixed_window_inverse=four_well_inverse(),
                kernel=four_well_kernel(),
                tiny_D1_only_occupied_site_by_clock=tiny,
                native_panels=panels,four_well_effective_orders=timing)
    out.mkdir(parents=True,exist_ok=True)
    with (out/"position_only_winding.json").open("x",encoding="utf8",newline="\n") as f:
        json.dump(data,f,indent=2)
        f.write("\n")


if __name__=="__main__":
    main()
