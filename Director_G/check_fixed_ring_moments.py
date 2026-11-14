"""Exact fixed-ring character tomography. Run with Python 3 and a fresh output directory."""
import argparse
import json
from collections import Counter
from math import comb, gcd
from pathlib import Path

from check_character_tomography import reduced


def check(test, message):
    if not test:
        raise ValueError(message)


def physical(d, q, clocks):
    """Propagate positive word counts on (physical site, rail, z bit, g exponent)."""
    state = Counter({(0, 0, 0, 0): 1})
    for t in range(1, max(clocks)+1):
        new = Counter()
        for (x, rail, sign, s), n in state.items():
            new[(x+1) % (2*d), 0, sign, s] += n
            new[(x-1) % (2*d), 1, sign ^ rail, (s+1) % q] += n
        state = new
        if t in clocks:
            check(sum(state.values()) == 1 << t, "unsigned physical mass")
            yield t, state


def at_port(state, q, x, rail):
    a = [state[x,rail,0,s]-state[x,rail,1,s] for s in range(q)]
    count = sum(state[x,rail,0,s]+state[x,rail,1,s] for s in range(q))
    return a, count


def run_count(t, left):
    """Signed compositions of left runs interspersed with rights, with a final R."""
    if left == 0:
        return 1
    return sum((-1)**(left-p)*comb(left-1,p-1)*comb(t-left,p)
               for p in range(1,min(left,t-left)+1))


def direct_read(q, a, count, weights, c):
    """Return the weighted squared signal in Z[X]/Phi_q (unscaled by 2^t)."""
    lags = [sum(a[j]*a[(j+h) % q] for j in range(q)) for h in range(q)]
    signal = [c*count]+[0]*(q-1)
    for s, w in enumerate(weights):
        for h, v in enumerate(lags):
            signal[(s*h) % q] += w*v
    return reduced(signal,q)


def moment_rhs(q, signal, estimated, constant, coeff, divisor):
    rem = [0]*q
    for i, x in enumerate(signal):
        rem[i] = x
    rem[0] -= constant
    for m, k in zip(estimated,coeff):
        for i,x in enumerate(m):
            rem[i] -= k*x
    check(abs(divisor) == 1, "unit triangular pivot")
    return reduced([v*divisor for v in rem],q)


def inverse(q, d, moments):
    g = gcd(q,d)
    m = q//g
    # Moments are sums of twice-cosines; fill upper lags by conjugate symmetry.
    all_lags = [moments[min(h,m-h)] for h in range(m)]
    recovered = []
    for s in range(m//2+1):
        poly = [0]*q
        for h, val in enumerate(all_lags):
            for exponent, v in enumerate(val):
                poly[(exponent-g*s*h) % q] += v
        folded = reduced(poly,q)
        check(len(folded)==1,"inverse DFT leaves the rational scalars")
        divisor = m*(2 if s == (-s)%m else 1)
        check(folded[0]%divisor == 0,"integral recovered weight")
        recovered.append(folded[0]//divisor)
    return recovered


def analyze(d,q):
    g = gcd(q,d)
    m = q//g
    depth = m//2
    # Include k=1 even when m=1 to verify complete aliasing and single-clock census.
    times = {3} | {1+k*d for k in range(1,max(depth,1)+1)}
    rows = []
    for t, state in physical(d,q,times):
        if t == 3:
            dark, dark_count = at_port(state,q,(-1)%(2*d),1)
            check(dark == [0]*q and dark_count == 2,"three-tick sharp L anchor")
        if t == d+1:
            one, n_one = at_port(state,q,d-1,0)
            check(n_one == d and one == [d if s==1%q else 0 for s in range(q)],
                  "one-left R anchor")
        if (t-1)%d or (t-1)//d == 0:
            continue
        k = (t-1)//d
        a, count = at_port(state,q,t%(2*d),0)
        v = [run_count(t,h*d) for h in range(k+1)]
        coeff = [sum(v[i]*v[i+h] for i in range(k+1-h)) for h in range(k+1)]
        check(v[0]==1 and v[k]==(-1)**(k*d-1),"extreme right-ending words")
        check(coeff[k]==v[k],"top lag")
        residues = [0]*q
        for h,x in enumerate(v):
            residues[(h*d)%q] += x
        check(residues==a,"signed run formula vs physical arc counts")
        check(count==sum(comb(t-1,h*d) for h in range(k+1)),"physical count")
        rows.append(dict(t=t,k=k,a=a,count=count,lift_coefficients=v,lag_coefficients=coeff))

    cases = []
    for label,w,c in (("asymmetric",[1+s*s for s in range(q)],3),
                      ("pure_count",[0]*q,1),("trivial_winding",[1]+[0]*(q-1),0),
                      ("unit_winding",[int(i==1%q) for i in range(q)],0),
                      ("asymmetric_conjugate",[1+((-s)%q)**2 for s in range(q)],3)):
        total = c+sum(w)
        anchor = direct_read(q,dark,dark_count,w,c)
        check(len(anchor)==1 and anchor[0]%2==0,"recover counting mass")
        recovered_count = anchor[0]//2
        total_coherent = total-recovered_count
        moments = [[2*total_coherent]]
        observations = []
        binary64 = [1.0]
        for row in rows:
            k, t, ac = row["k"],row["t"],row["lag_coefficients"]
            signal = direct_read(q,row["a"],row["count"],w,c)
            observations.append(signal)
            if k > depth:
                continue
            solved = moment_rhs(q,signal,moments[1:],
                                recovered_count*row["count"]+total_coherent*ac[0],
                                ac[1:k],ac[k])
            direct = [0]*q
            for s, weight in enumerate(w):
                direct[(k*d*s)%q] += weight
                direct[(-k*d*s)%q] += weight
            check(solved==reduced(direct,q),"recovered twice-cosine moment")
            moments.append(solved)
            if label=="trivial_winding":
                # A deliberately inexact repeat on the original-launch probability
                # illustrates cancellation in this estimator, even with no shot noise.
                probability = signal[0]/(1<<t)
                back = (probability*(1<<t)-ac[0]
                        -sum(2*ac[j]*binary64[j] for j in range(1,k)))/(2*ac[k])
                binary64.append(back)
        actual = inverse(q,d,moments)
        want = [0]*(depth+1)
        for s,v in enumerate(w):
            e = (s*(d//g))%m
            want[min(e,m-e)] += v
        check(actual==want and recovered_count==c,"folded weights from independent physical inputs")
        result = dict(case=label,oriented_weight_units=w,count_units=c,weight_denominator=total,
                      dark_numerator=anchor,physical_numerators=observations,
                      recovered_twice_cosine_moments=moments,recovered_count_units=recovered_count,
                      recovered_folded_units_in_winding_order=actual)
        if label=="trivial_winding":
            result["binary64_cosine_estimates_true_value_one"]=binary64
        cases.append(result)
    check(cases[0]["physical_numerators"]==cases[-1]["physical_numerators"],"conjugate ambiguity")
    collisions = []
    first = rows[0]
    for s in range(q):
        weights = [int(i==s) for i in range(q)]
        winding = direct_read(q,first["a"],first["count"],weights,0)
        tie = winding==[first["count"]]
        check(tie == (4*d*s % q == 0 and 2*d*s % q != 0),"quarter-turn collision")
        if tie:
            collisions.append(s)
            check(direct_read(q,dark,dark_count,weights,0)==[0],"dark anchor breaks count tie")
    return dict(D=d,q=q,effective_order=m,gcd=g,
                native_rows=[{name:v for name,v in row.items() if name!="a"} for row in rows],
                one_left_anchor=dict(t=d+1,x=d-1,rail="R",coherent=d*d,count=d),
                first_clock_oriented_labels_tied_with_count=collisions,cases=cases)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_directory",type=Path)
    args = parser.parse_args()
    # D=1 has identical physical destinations for ±1; its three-tick L anchor fails.
    _, s = next(physical(1,3,{3}))
    dark, miss = at_port(s,3,1,1)
    check(dark!=[0]*3 and miss!=2,"tiny-ring exception")
    rows = [analyze(d,q) for d,q in ((2,1),(3,2),(2,3),(2,4),(2,5),(3,3),(3,4),(3,7),
                                      (4,5),(4,8),(5,8),(5,9),(8,21))]
    result = dict(scope="Unfiltered C2 x Cq gain walk; sharp (0,R), LL carries sign minus. "
                        "Physical numerator coefficients in ascending monomials modulo Phi_q. "
                        "For a row at t, divide its numerator by weight_denominator times 2^t. "
                        "Recovered moments and weights use input integer weight units. "
                        "The dark count anchor is at t=3, x=-1, L. The two R anchors at "
                        "t=D+1 pin down count and the first cosine when q=3 and 3 does not divide D.",
                  alias="Recovered index is the folded residue of (D/gcd(D,q))*s modulo q/gcd(D,q).",
                  precision="The deliberately rounded trivial-winding reconstruction uses binary64 "
                            "input rates and recursion. Exact inversions above use integers.",
                  tiny_control=dict(D=1,q=3,three_tick_L_signed=dark,count=miss),panels=rows)
    args.output_directory.mkdir(parents=True,exist_ok=True)
    with (args.output_directory/"fixed_ring_moments.json").open("x",encoding="utf8",newline="\n") as f:
        json.dump(result,f,indent=2,allow_nan=False)
        f.write("\n")


if __name__ == "__main__":
    main()
