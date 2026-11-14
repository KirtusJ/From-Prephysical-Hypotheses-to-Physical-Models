"""Cyclic gain permutations in the two-rail score equation.

Run with standard Python: python -B check_gain_orbit_forms.py NEW_DIRECTORY
The input coordinates are multiplicities of atoms. All arithmetic is exact.
"""
import argparse
from collections import Counter, deque
from fractions import Fraction as Q
from itertools import combinations_with_replacement, product
import json
from pathlib import Path


def require(ok, message):
    if not ok:
        raise ArithmeticError(message)


def multisets(q, cap):
    result = []
    for size in range(cap+1):
        for word in combinations_with_replacement(range(q), size):
            counts = Counter(word)
            result.append(tuple(counts[i] for i in range(q)))
    return result


def shift(v, perm):
    out = [0]*len(v)
    for i, dest in enumerate(perm):
        out[dest] = v[i]
    return tuple(out)


def add(u, v):
    return tuple(a+b for a,b in zip(u,v))


def cycles(perm):
    require(sorted(perm)==list(range(len(perm))), "map must permute atoms")
    seen = set()
    result = []
    for x in range(len(perm)):
        if x in seen:
            continue
        orbit = []
        while x not in seen:
            seen.add(x)
            orbit.append(x)
            x = perm[x]
        result.append(orbit)
    return result


def features(v, orbits):
    counts = [sum(v[i] for i in orbit) for orbit in orbits]
    z = [sum((-1)**j*v[i] for j,i in enumerate(orbit))
         for orbit in orbits if len(orbit)%2==0]
    return counts+[z[i]*z[j] for i,j in combinations_with_replacement(range(len(z)),2)]


def rank(rows):
    """Sparse row elimination over Q; each stored leading coefficient is one."""
    pivots = {}
    for raw in rows:
        row = {j:Q(k) for j,k in raw.items() if k}
        while row:
            j = max(row)
            c = row[j]
            if j not in pivots:
                pivots[j] = {i:x/c for i,x in row.items()}
                break
            for i,x in pivots[j].items():
                row[i] = row.get(i,0)-c*x
                if not row[i]:
                    del row[i]
    return len(pivots)


def finite_rank(perm, cap):
    q = len(perm)
    orbits = cycles(perm)
    words = multisets(q,cap)
    coords = {v:i for i,v in enumerate(words[1:])}
    n = len(coords)
    basis = {v:features(v,orbits) for v in words}
    rows = []
    # Establish the single-input (including equal-rail) equations first.
    # This ordering keeps exact elimination sparse on the larger finite boxes.
    pairs = [(u,words[0]) for u in words] + [(words[0],v) for v in words[1:]]
    pairs.extend((u,v) for u in words[1:] for v in words[1:] if sum(u)+sum(v)<=cap)
    for u,v in pairs:
        left, right = add(u,v), add(u,shift(v,perm))
        row = Counter()
        for offset, word, c in ((0,left,1),(n,right,1),(0,u,-2),(n,v,-2)):
            if word in coords:
                row[offset+coords[word]] += c
        require(all(x+y==2*(a+b) for x,y,a,b in
                    zip(basis[left],basis[right],basis[u],basis[v])),
                "a proposed basis function violates the full two-rail equation")
        rows.append(row)
    exact_rank = rank(rows)
    feature_rank = rank(dict(enumerate(basis[v])) for v in words)
    dimension = len(basis[words[0]])
    require(exact_rank+feature_rank==2*n, "unaccounted solutions on the truncated box")
    return dict(permutation=perm, orbits=orbits, cap=cap, unknowns=2*n, equations=len(rows),
                rank_Q=exact_rank, nullity_Q=2*n-exact_rank,
                candidate_columns=dimension, evaluated_column_rank_Q=feature_rank)


def check_reference():
    source = Path(__file__).resolve().parents[1]/"Director_Z/computation/Product_Events/gains_of_order_q/onesite_q_result.json"
    report = json.loads(source.read_text(encoding="utf-8"))
    selected = [r for r in report["main"] if r["n"] in (2,3)] + report["side"]
    answer = []
    for r in selected:
        q,h,n = (r[k] for k in ("q","h","n"))
        result = finite_rank([(i+h)%q for i in range(q)], n)
        require([result[k] for k in ("unknowns","equations","rank_Q","nullity_Q")]==
                [r[k] for k in ("unknowns","equations","rank","nullity")], "published rank mismatch")
        answer.append(dict(q=q,h=h,published_modular_rank=r["rank"],**result))
    return answer


def mixed():
    perm = [0,2,3,1,5,4,7,8,9,6]  # lengths 1,3,2,4
    orbits = cycles(perm)
    words = multisets(len(perm),2)
    # z^T [[1,1],[1,2]] z plus one coefficient per orbit.
    def score(v):
        return sum(a*b for a,b in zip(features(v,orbits),[2,5,3,1,1,2,2]))
    for u,v in product(words,repeat=2):
        tv = shift(v,perm)
        require(score(add(u,v))+score(add(u,tv))==2*(score(u)+score(v)), "mixed equation")
        require(score(add(u,v))==score(add(u,shift(tv,perm))), "contextual square")
    u = (0,0,0,0,1,0,1,0,0,0)
    flipped_one = (0,0,0,0,0,1,1,0,0,0)
    require(score(u)==score(shift(u,perm)) and score(u)!=score(flipped_one),
            "independent parity flips are extra")
    # The indefinite matrix [[1,-2],[-2,1]] has positive axis tests.
    def indefinite(x,y):
        return x*x-4*x*y+y*y
    require(indefinite(1,0)>0 and indefinite(0,1)>0 and indefinite(1,1)<0,
            "axis-only nonnegativity counterexample")
    return dict(rank=finite_rank(perm,2), tested_context_pairs=len(words)**2,
                positive_matrix=[[1,1],[1,2]], orbit_counts=[2,5,3,1],
                source=list(u), both_rotated=list(shift(u,perm)),
                independently_rotated=list(flipped_one),
                scores=[score(u),score(shift(u,perm)),score(flipped_one)],
                indefinite_matrix=[[1,-2],[-2,1]],unit_axis_scores=[1,1],mixed_score=-2)


def lift(size, period):
    vertices = list(product(range(size),(1,-1),range(period)))
    def move(v,out):
        x,rail,t = v
        return ((x+out)%size,out,(t+int(rail==out==-1))%period)
    graph = {v:[move(v,out) for out in (1,-1)] for v in vertices}
    indegrees = Counter(w for edges in graph.values() for w in edges)
    require(all(indegrees[v]==2 for v in vertices),"lift indegree")
    seen = {vertices[0]}
    queue = deque(seen)
    while queue:
        for w in graph[queue.popleft()]:
            if w not in seen:
                seen.add(w)
                queue.append(w)
    require(len(seen)==len(vertices), "unreachable orbit grades")
    # For a balanced finite digraph forward reachability from one root
    # suffices, but also compute the harmonic nullity without that argument.
    ids = {v:i for i,v in enumerate(vertices)}
    rows = []
    for v in vertices:
        row = Counter({ids[v]:2})
        for w in graph[v]:
            row[ids[w]] -= 1
        rows.append(row)
        if v[1]==1:
            cursor = v
            for out in (-1,-1,1,1):
                cursor=move(cursor,out)
            require(cursor==(v[0],1,(v[2]+1)%period),"closed LLRR shift")
    nullity = len(vertices)-rank(rows)
    require(nullity==1,"nonconstant finite harmonic score")
    return dict(ring=size, actual_shift_period=period, vertices=len(vertices),
                reachable=len(seen), common_indegree=2, harmonic_nullity_Q=nullity)


def line_control():
    # Common continuation with a positive nonconstant score on the line.
    # At x both rails use 2**x per atom. The two daughters live at x±1.
    gamma = Q(5,2)
    sizes = range(4)
    checked = 0
    for x,n,m in product(range(-4,5),sizes,sizes):
        w = Q(2)**x
        require((Q(2)**(x+1)+Q(2)**(x-1))*(n+m)==gamma*w*(n+m),"unbounded line tilt")
        checked += 1
    return dict(weight="2^x times the multiset size on either rail", factor=str(gamma),
                checked=checked, positions=list(range(-4,5)), operand_sizes=list(sizes))


def run():
    return dict(source="Director_Z/computation/Product_Events/gains_of_order_q/onesite_q_result.json",
                definitions="All U,V with total cardinality at most cap, separate rail unknowns with both vacuum scores fixed to zero. Basis columns comprise orbit counts and unordered products of even-orbit alternating differences. Column rank on the box measures dependence introduced by truncating amplitude counts.",
                reference_comparisons=check_reference(), mixed_cycles=mixed(),
                cap_one_unresolved_parameters=finite_rank([1,0,3,2],1),
                spatial_rings=[lift(n,t) for n in (3,4,5) for t in (1,2,3,4)],
                infinite_line=line_control(),
                limits="Finite equality ranks and lift checks use rational arithmetic. Positive semidefiniteness tests all integer multiples and directions in the infinite cone. Full-input classifications need arbitrary preparations; cyclic translations of one launch alone need not realize them.")


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination",type=Path)
    path=parser.parse_args().destination/"gain_orbit_forms.json"
    if path.exists():
        raise FileExistsError(path)
    result=run()
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("x",encoding="utf-8",newline="\n") as f:
        json.dump(result,f,indent=2,allow_nan=False)
        f.write("\n")
