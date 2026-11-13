"""Compressed phase-reference menus, cross-order alignment and sign-sensitive controls."""

import argparse
import json
from fractions import Fraction
from itertools import product
from math import gcd
from pathlib import Path

from check_internal_reference import check_diamonds, dot, fold


def prime_powers(n):
    factors = []
    p = 3
    remaining = n
    while p*p <= remaining:
        power = 1
        while remaining % p == 0:
            power *= p
            remaining //= p
        if power > 1:
            factors.append((p, power))
        p += 2
    if remaining > 1:
        factors.append((remaining, remaining))
    return factors


def spatial_menu(order, dimensions):
    factors = prime_powers(order)
    idempotents = [(order//q)*pow(order//q, -1, q) for _, q in factors]
    vectors = []
    for choice in product(range(dimensions), repeat=len(factors)):
        v = tuple(sum(e for j, e in zip(choice, idempotents) if j == i) % order
                  for i in range(dimensions))
        for j, (_, q) in zip(choice, factors):
            assert tuple(a % q for a in v) == tuple(int(i == j) for i in range(dimensions))
        vectors.append(v)
    menu = [tuple(t*a % order for a in v) for v in vectors for t in range(order)]
    inc = [(0,)*dimensions]*(2*len(menu))
    total = (0,)*dimensions
    for j, gain in enumerate(menu):
        total = tuple((a+b) % order for a,b in zip(total,gain))
        inc[2*j+1] = total
    assert total == (0,)*dimensions
    return vectors, menu, inc


def coverage(order, dim):
    vectors, menu, inc = spatial_menu(order, dim)
    physical = check_diamonds(order, menu, inc)
    histogram = [0]*(len(vectors)+1)
    recovered = 0
    first_mixed = None
    for r in product(range(order), repeat=dim):
        phases = [dot(v,r) % order for v in vectors]
        eligible = [i for i, x in enumerate(phases) if gcd(x,order) == 1]
        faithful = gcd(order, *r) == 1
        assert bool(eligible) == faithful
        histogram[len(eligible)] += 1
        if not eligible:
            continue
        j = eligible[0]
        rank = [fold(t*phases[j],order) for t in range(order)]
        assert set(rank) == set(range((order+1)//2))
        t = rank.index(1)
        h = tuple(t*a % order for a in vectors[j])
        assert dot(r,h) % order in (1, order-1)
        for s in range(order):
            assert rank[t*s % order] == fold(s,order)
        if first_mixed is None and all(gcd(x,order) > 1 for x in r):
            first_mixed = dict(tuple=r, seed=vectors[j], multiple=t, selected=h, exponent=dot(r,h)%order)
        recovered += 1
    expected = Fraction(order**dim)
    for p,_ in prime_powers(order):
        expected *= 1-Fraction(1,p**dim)
    assert expected == recovered
    return dict(order=order, dimensions=dim, seed_vectors=vectors, number_of_settings=len(menu),
                ring_size=len(inc), exhaustive_physical_diamonds=physical,
                histogram_number_of_eligible_seeds=histogram, recovered=recovered,
                prior_yield=str(Fraction(recovered,order**dim)), faithful_with_no_unit_coordinate=first_mixed)


def alignment(m,n):
    assert n % m == 0
    rows = []
    for a,b in product((1,-1), repeat=2):
        # At order n, compare z_m^a against z_n^(±bn/m).
        ranks = {str(s):fold((n//m)*(a+s*b),n) for s in (1,-1)}
        assert list(ranks.values()).count(0) == 1
        assert ranks[str(-a*b)] == 0 and ranks[str(a*b)] == fold(2*(n//m), n)
        rows.append(dict(sign_m=a, sign_n=b, difference_and_sum_ranks=ranks,
                         null_combination=-a*b, nonnull_cosine_numerator=2))
    return dict(smaller=m, larger=n, rows=rows)


def gram_moments(order, d, powers):
    """Uniform-character average from exact orthogonality, independent of floating cosines."""
    total = 0
    for signs in product((-1,1), repeat=len(powers)):
        total += all(sum(s*v[i] for s,v in zip(signs,powers)) % order == 0 for i in range(d))
    return Fraction(total,2**len(powers))


def dark_joint(order, settings):
    dim = len(settings[0])
    total = Fraction(0)
    for include in product((False,True), repeat=len(settings)):
        factors = [v for v,w in zip(settings,include) if w]
        total += (-1)**len(factors)*gram_moments(order,dim,factors)
    return total / 4**len(settings)


def signed_dark_branch(order, settings):
    """Sheet numerator for a string of destructive outcomes; discard common translations."""
    sheet = {(0,)*len(settings[0]):1}
    for h in settings:
        out = {}
        for y,value in sheet.items():
            out[y] = out.get(y,0)-value
            z = tuple((a+b)%order for a,b in zip(y,h))
            out[z] = out.get(z,0)+value
        sheet = out
    return Fraction(sum(x*x for x in sheet.values()), 8**len(settings))


def record_moments():
    order, d = 5, 2
    settings = [(0,0),(1,0),(0,1),(2,0),(4,0),(1,1)]
    rows = []
    for h,g in product(settings, repeat=2):
        p = dark_joint(order, [h,g])
        total = signed_dark_branch(order, [h,g])
        assert p == total
        marginals = [dark_joint(order,[v]) for v in (h,g)]
        cov = p-marginals[0]*marginals[1]
        rows.append(dict(first=h, second=g, joint=str(p), marginals=list(map(str,marginals)),
                         same_reference_covariance=str(cov)))
        if h != (0,0) and g != (0,0):
            opposite = tuple(-x % order for x in h)
            assert cov == (Fraction(1,32) if g in (h,opposite) else 0)
    # The triple correlation can see a shared relation invisible in each pair covariance.
    triad = [(1,0),(0,1),(1,1)]
    triple = dark_joint(order,triad)
    assert triple == signed_dark_branch(order,triad) == Fraction(3,256)
    assert gram_moments(order,d,triad) == Fraction(1,4)
    return dict(order=order, dimensions=d, pairs=rows,
                triad=dict(settings=triad, same_reference_all_dark=str(triple),
                           fresh_reference_each_block=str(Fraction(1,64))))


def coherent_clock(order):
    """Compare holding a localized arm with advancing it three ordinary walk ticks."""
    start = (1,1,0)
    counts = {}
    for w in product((1,-1),repeat=3):
        x,c,y = start
        sign = 1
        for new in w:
            y = (y+x)%order
            sign *= -1 if c == new == -1 else 1
            x,c = (x+new)%order,new
        cell = (x,c,y)
        counts[cell] = counts.get(cell,0)+sign
    assert sum(v*v for v in counts.values()) == 8
    ret = counts.get(start,0)
    return dict(ring_and_sheet_order=order, signed_return=ret, source=start,
                cell_counts=[(list(k),v) for k,v in sorted(counts.items())],
                port_0_coefficients_in_basis_1_sqrt2=["1/2",str(Fraction(ret,8))],
                arm_recorded_port_0="1/2")


def main(output):
    scans = [coverage(m,d) for m,d in [(3,1),(5,2),(5,3),(9,2),(15,2),(45,2),(105,2)]]
    aligned = [alignment(m,n) for m,n in [(3,9),(5,15),(9,45),(15,105)]]
    clock = [coherent_clock(n) for n in (3,4,5,6)]
    assert [row["signed_return"] for row in clock] == [1,0,0,0]
    report = dict(compressed_scans=scans, unequal_orders=aligned, moment_controls=record_moments(), clock=clock)
    output.mkdir(exist_ok=True, parents=True)
    (output/"reference_comparison.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf8")
    print("Checked",len(scans),"compressed menus,",len(aligned),"refinement pairs and all sign controls.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("directory",type=Path)
    main(parser.parse_args().directory)
