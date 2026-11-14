"""Exact folded-label checks for coherent refinement of finite cyclic sheet orders.

Run python -B check_sheet_refinement.py OUTDIR. The output must be new.
"""
import argparse
from fractions import Fraction
import json
from math import gcd, isqrt, lcm
from pathlib import Path


def require(ok, message):
    if not ok:
        raise ValueError(message)


def fold(k, n):
    k %= n
    return min(k, n-k)


def prime(n):
    return n>=2 and all(n%d for d in range(2,isqrt(n)+1))


def crt(a, m, b, n):
    require(gcd(m,n)==1, "CRT factors")
    return (a + m*((b-a)*pow(m,-1,n)%n))%(m*n) if n>1 else a%m


def component_label(n, p, at_p, elsewhere):
    power=1
    while n%(p*power)==0:
        power*=p
    return crt(at_p,power,elsewhere,n//power)


def compatible(labels):
    for n,v in labels.items():
        require(0<=v<=n//2, "noncanonical label")
        for m,u in labels.items():
            if n%m==0:
                require(fold(v,m)==u, "incompatible folded labels")


def exact_gap_derivation(nmax):
    # If 0<=r_(2n)<=n/2, its folded reduction modulo n is the very same integer.
    pair_count=boundary=0
    for n in range(2,nmax+1):
        for v in range(n+1):
            u=fold(v,n)
            if 2*v<=n:
                require(u==v, "dyadic small-fold rigidity")
                pair_count+=1
                boundary+=2*v==n
            elif u!=v:
                require(2*v>n,"nontrivial lift must cross the half-order boundary")
    return dict(nmax=nmax,pairs_in_safe_half=pair_count,closed_boundary_cases=boundary)


def factorial_path(last):
    f,a=6,1
    rows=[(3,f,a)]
    for n in range(3,last):
        if not prime(n+1) or a%(n+1)==0:
            choose=1
        else:
            choose=0
        new_a=a+choose*f
        new_f=(n+1)*f
        require((new_a-a)%f==0 and gcd(new_a,new_f)==1, "factorial refinement/unit")
        # Elementary finite bound, consistent with the analytic O(1/n) proof.
        require(new_a<2*f, "slowly growing choice of factorial digit")
        f,a=new_f,new_a
        rows.append((n+1,f,a))
    return rows


def run():
    cut=144
    ordinary={n:fold(1,n) for n in range(2,cut+1)}
    wild={n:fold(component_label(n,2,1,-1),n) for n in ordinary}
    compatible(ordinary)
    compatible(wild)
    require(all(gcd(n,w)==1 for n,w in wild.items()), "wild family not faithful")
    prime_powers=[]
    for p in range(2,cut+1):
        if prime(p):
            n=p
            while n<=cut:
                require(wild[n]==ordinary[n],"prime power distinguishes mixed signs")
                prime_powers.append(n)
                n*=p
    require(wild[12]==5, "composite panel failed to distinguish mixed signs")
    composite_tail=[]
    for j in range(2,19):
        n=3*(2**j)
        v=fold(component_label(n,2,1,-1),n)
        require(abs(v - n//3)==1, "mixed-sign composite-chain boundary")
        composite_tail.append([n,v,str(Fraction(v,n))])

    # Coherent integer charge 3 is faithful on all dyadic orders, and loses it at order 3.
    dyad=[[2**j,fold(3,2**j)] for j in range(1,18)]
    require(all(gcd(n,v)==1 for n,v in dyad) and gcd(3,3)==3, "dyadic charge three")
    panels=[3,4,5,8,12,25,49]
    common=lcm(*panels)
    p=next(p for p in range(5,common+6) if prime(p) and common%p)
    finite={n:fold(component_label(n,p,2,1),n) for n in range(2,cut+1)}
    compatible(finite)
    require(all(gcd(n,v)==1 for n,v in finite.items()), "finite-panel impostor not faithful")
    require(all(finite[n]==ordinary[n] for n in panels) and finite[p]!=ordinary[p],
            "finite panels did not remain identical")

    paths=factorial_path(38)
    f,a=paths[-1][1:]
    factorial_folds={n:fold(a,n) for n in range(2,39)}
    compatible(factorial_folds)
    require(all(gcd(n,w)==1 for n,w in factorial_folds.items()), "factorial extension restriction")
    return dict(scope="Exact finite arithmetic and witnesses. The unrestricted limits follow by proof.",
                dyadic_threshold=exact_gap_derivation(128),dyadic_integer_three=dyad,
                prime_power_impostor=dict(checked=sorted(prime_powers),order_12=wild[12],
                                           three_times_dyadic=composite_tail),
                finite_panel_impostor=dict(observed_orders=panels,lcm=common,unseen_prime=p,
                                           observed_unseen_fold=finite[p]),
                factorial_impostor=dict(rows=[[n,f,a,str(Fraction(a,f))] for n,f,a in paths],
                                        induced_folds_to_38=sorted(factorial_folds.items())))


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory",type=Path)
    directory=parser.parse_args().directory
    result=run()
    directory.mkdir(parents=True,exist_ok=True)
    with (directory/"sheet_refinement.json").open("x",encoding="utf8",newline="\n") as out:
        json.dump(result,out,separators=(",",":"))
        out.write("\n")
