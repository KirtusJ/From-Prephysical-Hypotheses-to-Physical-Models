"""Exact routing on eight-site Hadamard rings and an obstruction for other sizes."""
import argparse
from collections import deque
import hashlib
import json
from math import log2
from pathlib import Path


def bank(parity, modules):
    return [16*m + 2*x + c for m in range(modules)
            for x in range(parity, 8, 2) for c in (0, 1)]


def identity_columns(n):
    return [tuple(int(i == j) for i in range(n)) for j in range(n)]


def reflect_or_exchange(rows, exchanges):
    for a, b in exchanges:
        rows[a], rows[b] = rows[b], rows[a]


def tick(rows, n, modules, pre=(), post=()):
    """One unnormalized physical tick, simultaneously on every basis-input column."""
    rows = list(rows)
    reflect_or_exchange(rows, pre)
    coin = []
    for a, b in zip(rows[::2], rows[1::2]):
        coin.extend((tuple(x+y for x,y in zip(a,b)), tuple(x-y for x,y in zip(a,b))))
    reflect_or_exchange(coin, post)
    out = [None] * len(coin)
    for m in range(modules):
        off = 2*n*m
        for x in range(n):
            out[off + 2*((x+1) % n)] = coin[off + 2*x]
            out[off + 2*((x-1) % n)+1] = coin[off + 2*x+1]
    return out


def block_generator(edge):
    """An isolated transposition in the native clock frame after exactly 24 ticks."""
    a, b, frame = edge
    idle = ((), ())
    if frame == "before":
        return [(((a,b),), ())] + [idle]*23
    # Undo the streaming of both indices. For an internal generator these two
    # entrances share one coin; a connector uses the R entrance at site zero
    # in each of two neighboring modules.
    def unstream(mode):
        off = (mode//16)*16
        x, coin = divmod(mode-off,2)
        return off + 2*((x-1+2*coin)%8) + coin
    pair = (unstream(a), unstream(b))
    return [idle]*23 + [((), (pair,))]


def edges_for(parity, modules):
    edges = []
    for m in range(modules):
        off = 16*m
        for x in range(parity,8,2):
            edges.append((off+2*x, off+2*x+1, "before"))
        for x in range(1-parity,8,2):
            edges.append((off+2*((x+1)%8), off+2*((x-1)%8)+1, "after"))
    # A single switch between neighboring modules' site-zero R rails, accessible
    # before or after their coins, suffices for either parity bank.
    for m in range(modules-1):
        edges.append((16*m+2*parity, 16*(m+1)+2*parity, "after" if parity else "before"))
    return edges


def route_swap(a, b, edges):
    """Swap the endpoints of a shortest path and restore all intermediate wires."""
    if a == b:
        return []
    previous = {a: None}
    queue = deque([a])
    while queue and b not in previous:
        z = queue.popleft()
        for edge in edges:
            i, j, _ = edge
            if z == i or z == j:
                other = i+j-z
                if other not in previous:
                    previous[other] = (z, edge)
                    queue.append(other)
    assert b in previous
    forward = []
    while b != a:
        b, edge = previous[b]
        forward.append(edge)
    forward.reverse()
    return forward + forward[-2::-1]


def permutation_word(dest, edges):
    """dest maps each initial physical location to its requested output location."""
    assert set(dest) == set(dest.values())
    occupant = {p:p for p in dest}
    result = []
    for p in dest:
        a, b = occupant[p], dest[p]
        if a == b:
            continue
        elsewhere = next(q for q, z in occupant.items() if z == b)
        result.extend(route_swap(a, b, edges))
        occupant[p], occupant[elsewhere] = b, a
    assert occupant == dest
    return result


def apply_word(rows, word, modules):
    before = len(rows)
    for edge in word:
        for pre, post in block_generator(edge):
            rows = tick(rows, 8, modules, pre, post)
        assert all(v % 4096 == 0 for row in rows for v in row)
        rows = [tuple(v//4096 for v in row) for row in rows]
    assert len(rows) == before
    return rows


def matching(rows, parity, pairs, modules):
    """Compile a logical ordered-matching H in alternating parity banks."""
    src, dst = bank(parity, modules), bank(1-parity, modules)
    assert sorted(a for pair in pairs for a in pair) == list(range(len(src)))
    pre, post = {}, {}
    for physical_pair, (a,b) in enumerate(pairs):
        r, l = src[2*physical_pair:2*physical_pair+2]
        pre[src[a]], pre[src[b]] = r, l
        off = (r//16)*16
        x = (r-off)//2
        post[off+2*((x+1)%8)] = dst[a]
        post[off+2*((x-1)%8)+1] = dst[b]
    w1 = permutation_word(pre, edges_for(parity, modules))
    w2 = permutation_word(post, edges_for(1-parity, modules))
    rows = apply_word(rows, w1, modules)
    rows = tick(rows,8,modules)
    rows = apply_word(rows, w2, modules)
    return rows, dict(pre_exchanges=len(w1), post_exchanges=len(w2), ticks=24*(len(w1)+len(w2))+1)


def encoded_columns(rows, modes):
    active = set(modes)
    assert all(not any(row) for physical,row in enumerate(rows) if physical not in active)
    return [rows[physical] for physical in modes]


def native_matching_tests(modules):
    size = 8*modules
    rows = [(0,)*size for _ in range(16*modules)]
    for mode, row in zip(bank(0,modules),identity_columns(size)):
        rows[mode] = row
    expected = identity_columns(size)
    cases = []
    bits = int(log2(size))
    for layer in range(bits):
        bit = 1 << layer
        pairs = [(j,j^bit) for j in range(size) if not j & bit]
        rows, stats = matching(rows, layer%2, pairs, modules)
        following = expected.copy()
        for a,b in pairs:
            following[a] = tuple(v+w for v,w in zip(expected[a], expected[b]))
            following[b] = tuple(v-w for v,w in zip(expected[a], expected[b]))
        expected = following
        assert encoded_columns(rows,bank((layer+1)%2,modules)) == expected
        cases.append(dict(ordered_pairs=pairs, **stats))
    assert expected == [tuple((-1)**((a&b).bit_count()) for b in range(size)) for a in range(size)]
    # A ready common-depth upper bound for any matching: at most size-1 transpositions
    # per permutation, each using at most 2*size-3 adjacent edges. Pad with idle U^24.
    common = 1 + 48*(size-1)*(2*size-3)
    assert all(common >= row["ticks"] and (common-row["ticks"]) % 24 == 0 for row in cases)
    return dict(modules=modules, logical_modes=size, active_inputs=bank(0,modules),
                native_generators_by_parity=[edges_for(p,modules) for p in (0,1)],
                all_input_columns_checked=size, walsh_layers=cases,
                common_ticks_per_matching_upper_bound=common,
                tested_program_ticks=sum(s["ticks"] for s in cases),
                logical_walsh_matrix_numerators=expected, squared_denominator=size)


def periods_and_generators():
    table = []
    for n in (4,6,8,10,12,16):
        start = identity_columns(2*n)
        rows = start
        observed = []
        for t in range(1,49):
            rows = tick(rows,n,1)
            if t%2 == 0 and all(tuple(v*(1<<(t//2)) for v in row) == new
                                for row,new in zip(start,rows)):
                observed.append(t)
        if n == 8:
            assert observed == [24,48]
        if n == 4:
            assert observed == list(range(8,49,8))
        if n in (6,10,12,16):
            assert observed == []
        table.append(dict(N=n, homogeneous_full_identity_through_48=observed))
    for parity in (0,1):
        for edge in edges_for(parity,2):
            expected = identity_columns(32)
            reflect_or_exchange(expected,[edge[:2]])
            assert apply_word(identity_columns(32),[edge],2) == expected
    return table


def mod_two_obstructions():
    tests = []
    for n in (4,6,8,10,12,14,15,16,18):
        r, l = 1, 0
        periods = []
        for t in range(1,129):
            z = r^l
            r = ((z<<1) | (z>>(n-1))) & ((1<<n)-1)
            l = (z>>1) | ((z&1)<<(n-1))
            if not (r or l):
                periods.append(t)
        odd = n
        while odd % 2 == 0:
            odd //= 2
        if odd > 1:
            assert not periods
        else:
            assert periods[0] == 1+n//2
        tests.append(dict(N=n, odd_part=odd, first_zero_column_mod_2_through_128=next(iter(periods),None)))
    return tests


def main(output):
    result = dict(
        supplies="Flat sheet gain; a local coin exchange swaps R and L at a specified "
                 "site before H or after H before streaming. No intermediate output measurement. "
                 "The optional two-module device adds one switch between neighboring modules' site-zero "
                 "R rails, accessible before or after their coins.",
        clock="The native clock counts every H and nearest-neighbor stream; each generator costs "
              "24 native ticks. The encoded banks alternate site parity at each logical H.",
        homogeneous=periods_and_generators(), mod_two=mod_two_obstructions(),
        programs=[native_matching_tests(m) for m in (1,2)],
        obstruction="All balanced signed ticks reduce to the same B=diag(z,z^-1)J modulo 2. "
                    "B^t=(z+z^-1)^(t-1) B in F2[z]/(z^N-1). A primitive odd-order root "
                    "of order dividing N makes this nonzero on either input coin. Thus no positive "
                    "even-depth column can be a normalized basis mode; odd depth would require "
                    "an irrational numerator. On an even ring every tick flips site parity. "
                    "These obstructions concern exact success with no postselection.",
        scope="No result for inhomogeneous routing on a lone power-of-two ring of size >=16. "
              "Homogeneous nonperiodicity outside sizes 2,4,8 is known; the finite table only checks 48 ticks. "
              "The intermodule connector is an added local operation and is not part of the original isolated ring.",
        homogeneous_period_reference="https://arxiv.org/abs/1504.06396")
    output.mkdir(parents=True,exist_ok=True)
    dest = output/"walk_router.json"
    dest.write_bytes((json.dumps(result,indent=1)+"\n").encode())
    print(dest,hashlib.sha256(dest.read_bytes()).hexdigest())


if __name__ == "__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_directory",type=Path)
    main(parser.parse_args().output_directory)
