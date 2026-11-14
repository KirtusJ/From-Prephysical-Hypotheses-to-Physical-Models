"""Check reversible nearest-neighbor counts and small one-pass permutation readers."""

from argparse import ArgumentParser
from fractions import Fraction
from itertools import permutations, product
from pathlib import Path
import json


def require(ok, message):
    if not ok:
        raise ValueError(message)


def schedule(n):
    """Two disjoint inward sweeps followed by a central merge, edges source to target."""
    left, right = 0, n-1
    layers = []
    while right-left > 2:
        layers.append([(left,left+1),(right,right-1)])
        left += 1
        right -= 1
    if right-left == 2:
        layers.append([(left,left+1)])
        left += 1
    if right > left:
        layers.append([(right,left)])
    return layers, left


def run(word, layers, center):
    n = len(word)
    regs = list(word)
    for edges in layers:
        touched = [i for a,b in edges for i in (a,b)]
        require(len(set(touched)) == len(touched) and all(abs(a-b)==1 for a,b in edges),
                "edge layer must be a nearest-neighbor matching")
        for a,b in edges:
            regs[b] = (regs[b]+regs[a])%(n+1)
    count = regs[center]
    for edges in reversed(layers):
        for a,b in edges:
            regs[b] = (regs[b]-regs[a])%(n+1)
    require(regs == list(word), "inverse count schedule did not restore workspace")
    return count


def gauge_fixed_readers(n, width):
    # Read-zero maps can be made identities by a separate permutation of the
    # head's basis at each time. Accepting states may be any subset.
    perms = list(permutations(range(width)))
    words = list(product((0,1),repeat=n))
    possible = [0]*n
    for moves in product(perms,repeat=n):
        by_count = [set() for _ in range(n+1)]
        for word in words:
            head = 0
            for bit, move in zip(word,moves):
                if bit:
                    head = move[head]
            by_count[sum(word)].add(head)
        for j in range(1,n+1):
            low = set.union(*by_count[:j])
            high = set.union(*by_count[j:])
            possible[j-1] += low.isdisjoint(high)
    return possible


def backward_intervals(n):
    """All possible backward cones starting at any single terminal."""
    intervals = {(j,j) for j in range(n)}
    sizes = [1]
    for _ in range((n+1)//2):
        new = set()
        for l,r in intervals:
            for left,right in product((0,1),repeat=2):
                if l-left<0 or r+right>=n or (l==r and left and right):
                    continue
                new.add((l-left,r+right))
        intervals = new
        sizes.append(max(r-l+1 for l,r in intervals))
    return sizes


def main():
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("output_file",type=Path)
    dest = cli.parse_args().output_file
    checked_words = {}
    for n in range(1,11):
        layers, center = schedule(n)
        require(len(layers) == (0 if n==1 else (n+1)//2), "central edge depth")
        require(backward_intervals(n) == [1]+[min(n,2*d) for d in range(1,(n+1)//2+1)],
                "all possible backward-cone widths")
        for word in product((0,1),repeat=n):
            require(run(word,layers,center) == sum(word), "count at the physical terminal")
        checked_words[n] = 2**n
    width_trials = {w: gauge_fixed_readers(3,w) for w in (1,2,3)}
    require(all(row == [0,0,0] for row in width_trials.values()), "unexpected three-state threshold")
    n = 3
    good = [0,0,0]
    for word in product((0,1),repeat=n):
        state = 0
        for bit in word:
            state = (state+bit)%4
        for j in range(1,4):
            good[j-1] += (state>=j) == (sum(word)>=j)
    require(good == [8,8,8], "four-state head")
    layers, center = schedule(48)
    w = tuple(int(i%3==1) for i in range(48))
    require(run(w,layers,center)==16 and len(layers)==24, "48-bank check")
    # With three product banks whose site-hit masses are p=5/8, an input-
    # preserving one-bit head could hold parity; it cannot hold majority.
    p = Fraction(5,8)
    parity = 3*p*(1-p)**2+p**3
    majority = 3*p**2*(1-p)+p**3
    require(parity == Fraction(65,128) and majority == Fraction(175,256), "parity-vs-majority")
    data = dict(words_checked=checked_words,three_bank_layers=schedule(3)[0],
                forty_eight_bank_depth=len(layers),forty_eight_bank_terminal=center,
                admissible_programs_for_each_threshold=width_trials,
                width_four_words_correct=good,three_bank_parity=parity,three_bank_majority=majority)
    with dest.open("x",encoding="utf-8",newline="\n") as f:
        json.dump(data, f, indent=2, default=str)
        f.write("\n")


if __name__=="__main__":
    main()
