"""Check uniform logical labels, a five-qubit symmetry audit and routed reads."""
from argparse import ArgumentParser
from collections import Counter
from fractions import Fraction as Q
from itertools import permutations, product
import json
from math import comb
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def source(n, m):
    words = list(product((0, 1), repeat=n))
    mlabels = 2**m
    next_index = Counter()
    assignment = {}
    for word in words:
        k = sum(word)
        index = next_index[k]
        next_index[k] += 1
        group, label = divmod(index, mlabels)
        if (group+1)*mlabels <= comb(n, k):
            assignment[word] = (k, group, label)
    require(len(assignment) == len(set(assignment.values())), "lost orthogonal coordinate")
    for k in range(n+1):
        nlabels = Counter(label for layer, _, label in assignment.values() if layer == k)
        require(all(nlabels[j] == comb(n,k)//mlabels for j in range(mlabels)),
                "unequal label counts")
    return assignment


def physical_site(label, k, pool_a, pool_b):
    group = min(label//k, 2)
    route = ("RRLLLLLL", "RRRRLLLL", "RRRRRRRR")[group]
    x = sum(1 if r == "R" else -1 for r in route)
    rail = route[-1]
    if group < 2 and not (pool_a, pool_b)[group] and label == group*k:
        rail = "R" if rail == "L" else "L"
    return (x+(1 if rail == "R" else -1)) % 24


def settings_at_bias(assignment, p):
    cells = {coord: p**sum(word)*(1-p)**(len(word)-sum(word))
             for word, coord in assignment.items()}
    total = sum(cells.values())
    require(total == 8*p*p*(1-p)**2, "five-slot mass")
    if not total:
        return dict(pass_norm=total, square_rates=None)
    rates = []
    for a,b in product((False,True), repeat=2):
        panel = Counter()
        for (_, _, label), mass in cells.items():
            panel[physical_site(label, 3, a, b)] += mass/total
        require(sum(panel.values()) == 1 and panel[9] == Q(1, 4), "spectator mass")
        rates.append(panel[9]**2/sum(v*v for v in panel.values()))
    contrast = rates[0]-rates[1]-rates[2]+rates[3]
    require(rates == [Q(2,7),Q(2,9),Q(2,9),Q(2,11)] and contrast == Q(16,693),
            "original accepted-launch rates")
    return dict(pass_norm=total, square_rates=rates, contrast=contrast)


def swapped(word, i):
    return word[:i]+(word[i+1],word[i])+word[i+2:]


def symmetry_checks():
    words = list(product((0, 1), repeat=5))
    sample = {(0,0,0,0,0), (1,0,0,0,0)}
    overlaps = [Q(len(sample & {swapped(w,i) for w in sample}),2) for i in range(4)]
    require(overlaps == [Q(1,2),1,1,1], "counterexample swap expectations")
    # Project each layer onto its common coefficient for input amplitudes 1/sqrt(2).
    counts = Counter(sum(w) for w in sample)
    outside = 1-sum(Q(v*v,2*comb(5,k)) for k,v in counts.items())
    require(outside == Q(2,5), "counterexample symmetric projection")
    for word in words:
        for i in range(3):
            require(swapped(swapped(swapped(word,i),i+1),i) ==
                    swapped(swapped(swapped(word,i+1),i),i+1), "braid")
    require(all(len(set(word)) < len(word) for word in words), "fixed by a transposition")
    lengths = [sum(p[i] > p[j] for i in range(5) for j in range(i+1,5))
               for p in permutations(range(5))]
    require(Q(sum(lengths),len(lengths)) == 5, "mean adjacent-swap length")
    # Eigenvalue sign assignments compatible with all adjacent braid relations.
    signs = [s for s in product((-1,1),repeat=4) if all(
             s[i]*s[i+1]*s[i] == s[i+1]*s[i]*s[i+1] for i in range(3))]
    require(signs == [(-1,)*4,(1,)*4], "braid sign assignments")
    errors = {}
    for q in (1,2,4,8):
        ratio = 31*Q(3,31)**q
        errors[q] = ratio/(1+ratio)
    require(errors[1] == Q(3,4) and errors[8] < Q(1,10**6), "small observed error")
    return dict(swap_expectations=overlaps, squared_mass_outside_symmetric=outside,
                nonlinear_echo_errors=errors, inversion_counts=sorted(Counter(lengths).items()))


def main():
    p = ArgumentParser(description=__doc__)
    p.add_argument("output",type=Path)
    args = p.parse_args()
    counts = {}
    for n in range(1,9):
        for m in range(1,5):
            counts[f"{n},{2**m}"] = len(source(n,m))
    require([counts[f"{n},8"] for n in range(1,6)] == [0,0,0,0,16], "first source")
    assignment = source(5,3)
    outcomes = {str(p): settings_at_bias(assignment,p) for p in
                (Q(0),Q(1,64),Q(1,4),Q(1,2),Q(3,4),Q(63,64),Q(1))}
    data = dict(accepted_word_counts=counts, five_slot_panels=outcomes, echo=symmetry_checks())
    with args.output.open("x",encoding="utf-8",newline="\n") as out:
        json.dump(data,out,indent=2,default=str)
        out.write("\n")


if __name__ == "__main__":
    main()
