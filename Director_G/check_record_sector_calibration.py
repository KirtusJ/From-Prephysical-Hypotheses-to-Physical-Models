"""Exact rank of the physical calibration rows, in the real circulant basis.

Run python -B check_record_sector_calibration.py NEW_DIRECTORY.
"""
import argparse
from fractions import Fraction as Q
import json
from pathlib import Path


def require(test, why):
    if not test:
        raise ValueError(why)


def features(m, words):
    # Raw coefficient basis [a,K_0,...,K_D]. K_j=sum_d b_d cos(2pi*d*j/M).
    row = [len(words)] + [0]*(m//2+1)
    for sign, x in words:
        for other, y in words:
            difference = (x-y) % m
            row[1+min(difference, m-difference)] += sign*other
    return row


def children(m, u, v, site=0):
    gain = site//2
    def shifted(words, parity):
        return [(parity*s, (g+gain) % m) for s,g in words]
    return shifted(u,1)+shifted(v,1), shifted(u,1)+shifted(v,-1)


def rank(rows):
    basis = {}
    for original in rows:
        row = list(map(Q, original))
        for col in sorted(basis):
            if row[col]:
                row = [a-row[col]*b for a,b in zip(row, basis[col])]
        if any(row):
            pivot = next(i for i,a in enumerate(row) if a)
            basis[pivot] = [a/row[pivot] for a in row]
    return len(basis)


def scan(m):
    d, single = m//2, [(1,0)]
    probes = [single, [(1,0),(-1,0)]] + [[(1,0),(1,r)] for r in range(1,d+1)]
    first_rows = [features(m,u) for u in probes]
    require(rank(first_rows) == d+2, "missing parent score direction")
    pair_inputs = [(u,[]) for u in probes] + [(single,[(1,r)]) for r in range(d+1)]
    rows = []
    for u,v in pair_inputs:
        right, left = children(m,u,v,site=4*m-1)
        f,g = features(m,right), features(m,left)
        a,b = features(m,u), features(m,v)
        require([i+j for i,j in zip(f,g)] == [2*(i+j) for i,j in zip(a,b)],
                "blank block conservation")
        rows.append(f+g)
    dim = 2*(d+2)
    r = rank(rows)
    nullvec = [1]+[0]*(d+1)+[-1]+[0]*(d+1)
    require(r == dim-1 and all(sum(a*b for a,b in zip(row,nullvec)) == 0 for row in rows),
            "writing-row null space")
    fair = features(m,single)
    with_fair = rank(rows+[fair+[-a for a in fair]])
    require(with_fair == dim, "singleton fairness leaves unresolved bias")
    return dict(M=m, single_rail_deterministic_rank=rank(first_rows),
                child_parameters=dim, streamed_writer_rank=r,
                count_bias_nullvector=nullvec, with_fair_fork_rank=with_fair,
                tested_direction_write_pairs=len(rows))


def controls():
    m = 5
    for u in ([],[(1,0)],[(1,0),(-1,0)],[(1,2),(1,4),(-1,1)]):
        for v in ([], [(1,0)], [(-1,1),(1,3)]):
            ro,le = children(m,u,v)
            require(Q(3,2)*len(ro)+Q(1,2)*len(le) == 2*(len(u)+len(v)),
                    "biased count did not conserve")
    # Same parent is an equal mixture of trivial and first character. On pure
    # incoming words, either child gain translation preserves each score.
    # Joint U=V={+0} gives 4 and 0 for BOTH characters, which cannot see this
    # opposite perturbation. Use instead a half-turn at M=4.
    r,l = children(4, [(1,0)], [(1,2)])
    def two_scores(words):
        return (sum(sign for sign,g in words)**2,
                sum(sign*(1 if g == 0 else -1) for sign,g in words)**2)
    require(two_scores(r) == (4,0) and two_scores(l) == (0,4),
            "opposite-character test at order four")
    return dict(count_bias=dict(parent="1", child_scores=["3/2","1/2"],
                                named_singleton_fractions=["3/4","1/4"]),
                missed_two_rail_test=dict(M=4,r=2,parent_coefficients=["1/2","1/2"],
                                         child_characters=[0,1], writing_total=8,
                                         conserved_total=4),
                cancel_doublet_after_uncalibrated_position_write=dict(
                    parent_count=2, child_trivial_square=0))


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("outdir", type=Path)
    target = cli.parse_args().outdir/"record_sector_calibration.json"
    result = dict(rows=[scan(m) for m in (3,4,5,6,7,8,9,12,15,16,31,32,64)],
                  controls=controls())
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("x", encoding="utf8", newline="\n") as out:
        json.dump(result, out, sort_keys=True, separators=(",", ":"))
        out.write("\n")
