"""Cross-review program xr16/echo for 'Autonomous records and local echoes'.

Own implementation; imports nothing from the repository. Exact arithmetic
(int, Fraction) except the one logarithm in P11. Seed 20261113. The result
file is opened in exclusive mode and is never overwritten.

Model written from the note's text. Mode 2*j+r = wire j, private bit r.
A tick is a list of two-in/two-out blocks with out=(x+y, x-y) (unnormalised).
'bit': H on the private bit of each wire. 'swap k': H on the private bit and
move wire k<->k+1. 'logical': H between adjacent slots (2i,2i+1) for each r.
'pair a': H between wires a,a+1 for each r, other wires 'bit'.
A pair-local law of exponent e sends the block's incoming total to its two
outputs in proportion |out|^e (e=2 squared, e=4 the note's quartic, e=6 is a
parameter the note does not report). Instance data taken from the note's
checker as data only: the four matchings PREP and the localized source.

PREDICATES (fixed before the first run; a failed one is kept, not edited)
P1  216 ticks for PREP; wire amplitudes*4 == [-2,0,-1,1,0,0,3,1], private bits blank;
    e=2 pair-local masses equal global normalised squares; wires 3,7 = (1/16,1/16).
P2  e=4 masses on wires 3,7 == (5/656, 1/16).
P3  wires (3,7), e=4: 230 ticks; after first H (23/328,0); post-echo (23/656,23/656);
    TV(echo,idle) over all 16 modes == 9/328; e=2: TV == 0; echo and idle words are
    the same integer map on all 16 basis modes.
P3c controls under e=4: opposite sign (2,3) TV>0 with bright/dark exchanged;
    single occupied (1,2) TV==0; empty (4,5) TV==0; unequal (0,6) TV > 9/328.
P4  wire-level model (no microticks) reproduces the microtick wire masses for PREP and
    for 10 random preparations, e in {2,4,6}.  [not reported in the note]
P5  hypotheses of the forward laws, tested per block for every tick of P1-P3, each e:
    (a) zero amplitude => zero mass (sharp dark port / empty), (b) exactly one occupied
    input => equal output masses, (c) block total conserved. Counts reported.
P6  periodicity: PREP followed by its layers in reverse order returns amplitudes
    (up to the power of two) and masses of e=2,4,6 to the localized source.
P7  search, 300 random preparations (depth 2..6, width 8). Qualifying instance = a pair
    of wires with equal nonzero signed amplitude (hypothesis tested per pair) on a
    preparation where P5(a,b,c) hold. For each e:
    (i)  e=2: every qualifying pair has p_a == p_b;
    (ii) for every e: [p_a == p_b] <=> [echo TV == 0] <=> [transpose of the bright
         column is fair], and echo TV == |p_a-p_b|/2;
    (iii) counterexample count for e=4 and e=6: qualifying pairs with p_a != p_b
         (forward hypotheses hold, reciprocity and echo premises fail). Expected > 0.
P8  weaker premises do not suffice (e=4, wires 3,7): (a) the pair sum is preserved by
    the echo; (b) the forward array after the bright port is fair, but it is not the
    transpose of the array into the bright port.
P9  s=(a^2-b^2)/(a^2+b^2), u=2ab/(a^2+b^2) interchange under H; (1+G(s))/2 with
    G(s)=2s/(1+s^2) equals a^4/(a^4+b^4); G in {s, s^3, 2s/(1+s^2)} restores the
    two-mode assignment after H,H; 500 random integer pairs, (0,0) excluded and counted.
P10 round robin for h=2..30: every round a perfect matching, every unordered pair
    exactly once, round of two finite labels == half-sum mod 2h-1.
P11 ceil(8 log(4/0.05)/d^2) == 46562 for d=9/328, and 4exp(-n d^2/8) <= 0.05 at n,
    > 0.05 at n-1.
P12 D_echo: 200 random class-path layouts; resolved TV == (1/4) sum |b_a-b_b| and
    max within-class spread <= 4*TV.
P13 reversible fine-graining of the 3-phase orbit (5,41)/46 -> (46,0)/46 -> (23,23)/46
    -> back, D=46 and D=92: P is a bijection; forward-sheet marginals correct; J V J ==
    V^-1 on every doubled state; predecessors of the bright fiber number (5,41)*D/46
    (unequal: reverse fairness fails although exact reversal holds).
P14 in the model of P13, single-occupied-input fairness holds for the J-image
    (backward-sheet) ensemble at the bright port.  [stated as a test of whether the
    countermodel keeps the note's own forward fairness premise on both sheets]
P15 arithmetic: 22304*5/656==170, 22304*41/656==1394, 2*14*22304==624512, 2*14*32==896,
    half-mixture of (5/46,41/46) and (1/2,1/2) == (7/23,16/23), (5+41)/656==23/328.
"""
import json, math, random, sys
from fractions import Fraction as Fr
from pathlib import Path

SEED = 20261113
W = 8
PREP = [[(1,5),(0,4),(7,2),(3,6)], [(6,1),(5,0),(3,4),(7,2)],
        [(3,5),(4,7),(1,2),(0,6)], [(2,7),(0,4),(3,6),(1,5)]]
RES = {}
HYP = {"dark_checked":0,"dark_failed":0,"single_checked":0,"single_failed":0,
       "conserve_checked":0,"conserve_failed":0}

def rec(name, ok, **info):
    RES[name] = dict(passed=bool(ok), **info)
    print(name, "PASS" if ok else "FAIL", info)

# ---------------- microtick model ----------------
def blocks(tick, width=W):
    kind = tick[0]
    if kind == "bit":
        return [((2*x,2*x+1),(2*x,2*x+1)) for x in range(width)]
    if kind == "swap":
        k = tick[1]; out = []
        for x in range(width):
            y = k+1 if x == k else k if x == k+1 else x
            out.append(((2*x,2*x+1),(2*y,2*y+1)))
        return out
    if kind == "logical":
        return [((2*x+r,2*x+2+r),(2*x+r,2*x+2+r)) for x in range(0,width,2) for r in (0,1)]
    if kind == "pair":
        a = tick[1]
        out = [((2*x,2*x+1),(2*x,2*x+1)) for x in range(width) if x not in (a,a+1)]
        return out + [((2*a+r,2*a+2+r),(2*a+r,2*a+2+r)) for r in (0,1)]
    raise ValueError(kind)

def step(v, masses, bl):
    """masses: dict e -> list of Fractions. Returns new (v, masses); counts hypotheses."""
    out = [0]*len(v)
    for (a,b),(c,d) in bl:
        out[c], out[d] = v[a]+v[b], v[a]-v[b]
    new = {}
    for e, m in masses.items():
        q = [Fr(0)]*len(v)
        for (a,b),(c,d) in bl:
            tot = m[a]+m[b]
            wc, wd = abs(out[c])**e, abs(out[d])**e
            if wc+wd:
                q[c] = tot*Fr(wc, wc+wd); q[d] = tot-q[c]
            elif tot != 0:
                HYP["conserve_failed"] += 1
            HYP["conserve_checked"] += 1
            HYP["conserve_failed"] += int(q[c]+q[d] != tot)
            for z in (c,d):
                if out[z] == 0:
                    HYP["dark_checked"] += 1; HYP["dark_failed"] += int(q[z] != 0)
            if (v[a] != 0) != (v[b] != 0):
                HYP["single_checked"] += 1; HYP["single_failed"] += int(q[c] != q[d])
        new[e] = q
    return out, new

def compile_layer(pairs, width=W):
    order = list(range(width)); arranged = [i for p in pairs for i in p]; swaps = []
    for j, w in enumerate(arranged):
        k = order.index(w)
        while k > j:
            swaps.append(k-1); order[k-1], order[k] = order[k], order[k-1]; k -= 1
    word = []
    for k in swaps: word += [("swap",k),("bit",)]
    word.append(("logical",))
    for k in reversed(swaps): word += [("swap",k),("bit",)]
    return word

def run_word(v, masses, word):
    for t in word:
        v, masses = step(v, masses, blocks(t))
    return v, masses

def source():
    v = [1]+[0]*(2*W-1)
    return v, {e:[Fr(x) for x in v] for e in (2,4,6)}

def wires(m): return [m[2*j]+m[2*j+1] for j in range(W)]

def reduce_amp(v):
    g = 0
    for x in v: g = math.gcd(g, abs(x))
    return [x//g for x in v] if g else v

# ---------------- wire-level model ----------------
def wire_layer(a, masses, pairs):
    out = list(a); new = {e:list(m) for e,m in masses.items()}; ok = True
    for (i,j) in pairs:
        out[i], out[j] = a[i]+a[j], a[i]-a[j]
        for e, m in masses.items():
            tot = m[i]+m[j]; wi, wj = abs(out[i])**e, abs(out[j])**e
            if wi+wj:
                new[e][i] = tot*Fr(wi,wi+wj); new[e][j] = tot-new[e][i]
            else:
                new[e][i] = new[e][j] = Fr(0); ok = ok and tot == 0
    return out, new, ok

def wire_prep(layers):
    a = [1]+[0]*(W-1); m = {e:[Fr(x) for x in a] for e in (2,4,6)}; ok = True
    for L in layers:
        a, m, o = wire_layer(a, m, L); ok = ok and o
    return a, m, ok

def main():
    rng = random.Random(SEED)
    dest = Path(sys.argv[1])/"xr16_echo_results.json"
    fh = open(dest, "x")   # refuses to overwrite

    # P1
    word = [t for L in PREP for t in compile_layer(L)]
    v, m = run_word(*source(), word)
    red = reduce_amp(v)
    tot2 = sum(x*x for x in v)
    born = [Fr(x*x, tot2) for x in v]
    scale4 = [Fr(x*x,tot2) for x in v]
    amp_ok = red[::2] == [-2,0,-1,1,0,0,3,1] and not any(red[1::2]) and sum(x*x for x in red) == 16
    rec("P1", len(word)==216 and amp_ok and m[2]==born and wires(m[2])[3]==Fr(1,16)==wires(m[2])[7],
        ticks=len(word), reduced_wire_amplitudes=red[::2], norm=sum(x*x for x in red))
    # P2
    w4 = wires(m[4])
    rec("P2", (w4[3],w4[7])==(Fr(5,656),Fr(1,16)), wires_3_7=[str(w4[3]),str(w4[7])],
        e6=[str(wires(m[6])[3]),str(wires(m[6])[7])])

    def probe(a, b):
        appr = list(range(b-1, a, -1))
        route = [t for k in appr for t in (("swap",k),("bit",))]
        unroute = [t for k in reversed(appr) for t in (("swap",k),("bit",))]
        v1, m1 = run_word(v, m, route)
        vb, mb = step(v1, m1, blocks(("pair",a)))
        vc, mc = step(vb, mb, blocks(("pair",a)))
        ve, me = run_word(vc, mc, unroute)
        vi, mi = run_word(v, m, route+[("bit",),("bit",)]+unroute)
        same_map = True
        for i in range(2*W):
            s = [int(i==j) for j in range(2*W)]
            z = {2:[Fr(x) for x in s]}
            x1,_ = run_word(s, z, route+[("pair",a)]*2+unroute)
            x2,_ = run_word(s, z, route+[("bit",)]*2+unroute)
            same_map = same_map and x1 == x2
        tv = {e: sum(abs(x-y) for x,y in zip(me[e],mi[e]))/2 for e in (2,4,6)}
        return dict(ticks=216+len(route)+2+len(unroute), same_map=same_map, tv=tv,
                    mid={e:(wires(mb[e])[a],wires(mb[e])[a+1]) for e in (2,4,6)},
                    after2={e:(wires(mc[e])[a],wires(mc[e])[a+1]) for e in (2,4,6)},
                    pre={e:(wires(m[e])[a],wires(m[e])[b]) for e in (2,4,6)},
                    post={e:(wires(me[e])[a],wires(me[e])[b]) for e in (2,4,6)},
                    amp_equal_arms= ve==vi, idle_restores={e: mi[e]==m[e] for e in (2,4,6)})
    p = probe(3,7)
    rec("P3", p["ticks"]==230 and p["mid"][4]==(Fr(23,328),0) and p["post"][4]==(Fr(23,656),)*2
        and p["tv"][4]==Fr(9,328) and p["tv"][2]==0 and p["same_map"] and p["amp_equal_arms"]
        and all(p["idle_restores"].values()),
        ticks=p["ticks"], mid4=list(map(str,p["mid"][4])), post4=list(map(str,p["post"][4])),
        tv={e:str(t) for e,t in p["tv"].items()}, same_map=p["same_map"])
    o, s, em, un = probe(2,3), probe(1,2), probe(4,5), probe(0,6)
    rec("P3c", o["tv"][4]>0 and o["mid"][4][0]==0 and o["mid"][4][1]>0 and s["tv"][4]==0
        and em["tv"][4]==0 and un["tv"][4]>Fr(9,328),
        opposite_tv=str(o["tv"][4]), opposite_mid=list(map(str,o["mid"][4])),
        single_tv=str(s["tv"][4]), empty_tv=str(em["tv"][4]), unequal_tv=str(un["tv"][4]),
        opposite_tv_e2=str(o["tv"][2]), unequal_tv_e2=str(un["tv"][2]))
    # P8
    pre, mid, post = p["pre"][4], p["mid"][4], p["post"][4]
    # array into bright: F = [[pa,0],[pb,0]] forced by the dark column; array out of bright: G=[[m/2,m/2],[0,0]]
    F_T_row = (pre[0], pre[1]); G_row = (post[0], post[1])
    rec("P8", sum(pre)==sum(post) and G_row[0]==G_row[1] and F_T_row != G_row and pre[0]!=pre[1],
        pre=list(map(str,pre)), post=list(map(str,post)),
        transpose_bright_row=list(map(str,F_T_row)), forward_fair_row=list(map(str,G_row)))
    # P6
    back = [t for L in reversed(PREP) for t in compile_layer(L)]
    v6, m6 = run_word(v, m, back)
    r6 = reduce_amp(v6)
    rec("P6", r6==[1]+[0]*(2*W-1) and all(m6[e]==[Fr(x) for x in r6] for e in (2,4,6)), ticks=len(word)+len(back))
    hyp_line = dict(HYP)
    rec("P5", hyp_line["dark_failed"]==0 and hyp_line["single_failed"]==0 and hyp_line["conserve_failed"]==0, **hyp_line)

    # P4 + P7
    def rand_prep():
        d = rng.randint(2,6); layers = []
        for _ in range(d):
            perm = list(range(W)); rng.shuffle(perm)
            layers.append([(perm[2*i],perm[2*i+1]) for i in range(W//2)])
        return layers
    a0, mw, ok0 = wire_prep(PREP)
    p4_ok = ok0 and all(wires(m[e])==mw[e] for e in (2,4,6)) and a0==red[::2]
    preps = [rand_prep() for _ in range(300)]
    micro_cmp = 0
    for layers in preps[:10]:
        wd = [t for L in layers for t in compile_layer(L)]
        vv, mm = run_word(*source(), wd)
        aa, mw2, okk = wire_prep(layers)
        micro_cmp += 1
        p4_ok = p4_ok and okk and all(wires(mm[e])==mw2[e] for e in (2,4,6)) and reduce_amp(vv)[::2]==reduce_amp(aa)
    rec("P4", p4_ok, random_preparations_compared=micro_cmp)
    stats = {e:dict(qualifying=0, equal_mass=0, unequal_mass=0, equiv_fail=0, tv_formula_fail=0) for e in (2,4,6)}
    preps_ok = 0; preps_with_pairs = 0; example = None
    for layers in preps:
        aa, mm, okk = wire_prep(layers)
        if not okk: continue
        preps_ok += 1
        prs = [(i,j) for i in range(W) for j in range(i+1,W) if aa[i]==aa[j]!=0]
        preps_with_pairs += int(bool(prs))
        for (i,j) in prs:
            for e in (2,4,6):
                st = stats[e]; st["qualifying"] += 1
                pa, pb = mm[e][i], mm[e][j]
                # echo on this pair, computed by the block law
                b1, mid_, ok1 = wire_layer([aa[i],aa[j]], {e:[pa,pb]}, [(0,1)])
                b2, fin, ok2 = wire_layer(b1, mid_, [(0,1)])
                dark_ok = b1[1]==0 and mid_[e][1]==0
                tv = (abs(fin[e][0]-pa)+abs(fin[e][1]-pb))/2
                # transpose of the array into the bright port: entries (pa,pb) since the dark column is zero
                rev_fair = pa == pb
                st["equal_mass" if pa==pb else "unequal_mass"] += 1
                if not (dark_ok and ok1 and ok2 and (rev_fair == (tv==0))): st["equiv_fail"] += 1
                if tv != abs(pa-pb)/2: st["tv_formula_fail"] += 1
                if e==4 and pa!=pb and example is None:
                    example = dict(layers=layers, wires=[i,j], amplitudes=[aa[i],aa[j]], masses=[str(pa),str(pb)], tv=str(tv))
    rec("P7", stats[2]["unequal_mass"]==0 and all(s_["equiv_fail"]==0 and s_["tv_formula_fail"]==0 for s_ in stats.values())
        and stats[4]["unequal_mass"]>0 and stats[6]["unequal_mass"]>0,
        preparations=len(preps), preparations_meeting_forward_hypotheses=preps_ok,
        preparations_with_a_qualifying_pair=preps_with_pairs, stats=stats, first_e4_counterexample=example)

    # P9
    Gs = {"s":lambda s:s, "s^3":lambda s:s**3, "quartic":lambda s:2*s/(1+s*s)}
    bad = 0; n9 = 0; excl = 0
    for _ in range(500):
        a, b = rng.randint(-9,9), rng.randint(-9,9)
        if a==0 and b==0: excl += 1; continue
        n9 += 1
        sv = Fr(a*a-b*b, a*a+b*b); uv = Fr(2*a*b, a*a+b*b)
        a1, b1 = a+b, a-b
        s1 = Fr(a1*a1-b1*b1, a1*a1+b1*b1); u1 = Fr(2*a1*b1, a1*a1+b1*b1)
        a2, b2 = a1+b1, a1-b1
        s2 = Fr(a2*a2-b2*b2, a2*a2+b2*b2)
        if (s1,u1) != (uv,sv): bad += 1
        if (1+Gs["quartic"](sv))/2 != Fr(a**4, a**4+b**4): bad += 1
        for G in Gs.values():
            if (1+G(s2))/2 != (1+G(sv))/2: bad += 1
            if G(Fr(1)) != 1 or G(-sv) != -G(sv): bad += 1
    rec("P9", bad==0, instances=n9, excluded_zero_pairs=excl, failures=bad)

    # P10
    bad = 0
    for h in range(2,31):
        n = 2*h-1; seen = {}
        for s in range(n):
            rnd = [("inf", s)] + [((s+j)%n, (s-j)%n) for j in range(1,h)]
            labs = [x for pr in rnd for x in pr]
            if sorted(map(str,labs)) != sorted(map(str,["inf"]+list(range(n)))): bad += 1
            for x,y in rnd:
                key = frozenset((x,y))
                if key in seen: bad += 1
                seen[key] = s
                if x != "inf" and (x+y)*pow(2,-1,n) % n != s: bad += 1
        if len(seen) != h*(2*h-1): bad += 1
    rec("P10", bad==0, h_range=[2,30], failures=bad)

    # P11
    d = 9/328; n = math.ceil(8*math.log(4/0.05)/d**2)
    rec("P11", n==46562 and 4*math.exp(-n*d*d/8)<=0.05 and 4*math.exp(-(n-1)*d*d/8)>0.05, n=n,
        bound_at_n=4*math.exp(-n*d*d/8), bound_at_n_minus_1=4*math.exp(-(n-1)*d*d/8))

    # P12
    bad = 0; edges_total = 0
    for _ in range(200):
        classes = [[Fr(rng.randint(0,20), 200) for _ in range(rng.randint(1,7))] for _ in range(rng.randint(1,5))]
        before = {}; after = {}; formula = Fr(0); spread = Fr(0)
        for ci, cl in enumerate(classes):
            for k, bm in enumerate(cl):
                for st in (0,1): before[(ci,k,st)] = bm/2; after[(ci,k,st)] = bm/2
            for k in range(len(cl)-1):
                st = k % 2          # 1st, 3rd,... edges in setting 0; even-numbered in setting 1
                val = (cl[k]+cl[k+1])/4
                assert after[(ci,k,st)] == cl[k]/2 and after[(ci,k+1,st)] == cl[k+1]/2  # matching: untouched so far
                after[(ci,k,st)] = after[(ci,k+1,st)] = val
                formula += abs(cl[k]-cl[k+1])/4; edges_total += 1
            spread = max(spread, max(cl)-min(cl))
        tv = sum(abs(before[k]-after[k]) for k in before)/2
        if tv != formula or spread > 4*tv: bad += 1
    rec("P12", bad==0, layouts=200, edges=edges_total, failures=bad)

    # P13, P14
    p13 = {}; p13_ok = True; p14_ok = True
    for D in (46, 92):
        k_ = D//46
        marg = [(5*k_,41*k_), (46*k_,0), (23*k_,23*k_)]
        Lp = 3
        def fmap(k):
            p_, q_ = marg[k], marg[(k+1)%Lp]
            F = [[0,0],[0,0]]; r = list(p_); c = list(q_)
            for u in (0,1):
                for w in (0,1):
                    z = min(r[u], c[w]); F[u][w] = z; r[u] -= z; c[w] -= z
            assert r==[0,0] and c==[0,0]
            src_start = [0, p_[0]]; dst_start = [0, q_[0]]
            f = {}
            used_dst = [0,0]
            # destination fibre w is filled in the order u=0,1
            dst_off = [[0,0],[0,0]]
            for w in (0,1):
                dst_off[0][w] = dst_start[w]; dst_off[1][w] = dst_start[w]+F[0][w]
            for u in (0,1):
                pos = src_start[u]
                for w in (0,1):
                    for t in range(F[u][w]):
                        f[pos+t] = dst_off[u][w]+t
                    pos += F[u][w]
            return f, F
        maps = [fmap(k) for k in range(Lp)]
        P = {(k,i):((k+1)%Lp, maps[k][0][i]) for k in range(Lp) for i in range(D)}
        bij = len(set(P.values()))==Lp*D and len(P)==Lp*D
        Pinv = {y:x for x,y in P.items()}
        V = {};
        for x in P: V[(+1,)+x] = (+1,)+P[x]; V[(-1,)+x] = (-1,)+Pinv[x]
        J = lambda s_: (-s_[0],)+s_[1:]
        Vinv = {y:x for x,y in V.items()}
        jvj = all(J(V[J(s_)]) == Vinv[s_] for s_ in V)
        port = lambda k,i: 0 if i < marg[k][0] else 1
        fwd_marg = all(sum(1 for i in range(D) if port(k,i)==0)==marg[k][0] for k in range(Lp))
        # every forward step lands in fibres with the right sizes
        fwd_marg = fwd_marg and all(sorted(maps[k][0].values())==list(range(D)) for k in range(Lp))
        bright = [i for i in range(D) if port(1,i)==0]
        pred = [0,0]; succ = [0,0]
        for i in bright:
            pred[port(0, Pinv[(1,i)][1])] += 1      # backward sheet: V acts as P^-1
            succ[port(2, P[(1,i)][1])] += 1         # forward sheet
        ok = bij and jvj and fwd_marg and pred==[5*k_,41*k_] and len(V)==2*Lp*D
        p13_ok = p13_ok and ok
        p14_ok = p14_ok and pred[0]==pred[1]
        p13[str(D)] = dict(bijection=bij, JVJ_is_Vinv=jvj, forward_marginals=fwd_marg, doubled_states=len(V),
                          bright_predecessors=pred, bright_forward_successors=succ,
                          couplings=[mp[1] for mp in maps])
    rec("P13", p13_ok, **p13)
    rec("P14", p14_ok, note="backward-sheet response of the bright fibre vs forward-sheet response of the same fibre",
        backward={D:p13[D]["bright_predecessors"] for D in p13}, forward={D:p13[D]["bright_forward_successors"] for D in p13})

    # P15
    half = ((Fr(5,46)+Fr(1,2))/2, (Fr(41,46)+Fr(1,2))/2)
    rec("P15", Fr(22304*5,656)==170 and Fr(22304*41,656)==1394 and 2*14*22304==624512 and 2*14*32==896
        and half==(Fr(7,23),Fr(16,23)) and Fr(5+41,656)==Fr(23,328), half=list(map(str,half)))

    summary = dict(seed=SEED, met=sum(r["passed"] for r in RES.values()),
                   failed=[k for k,r in RES.items() if not r["passed"]], total=len(RES))
    json.dump(dict(summary=summary, predicates=RES), fh, indent=1, default=str); fh.close()
    print(summary)

if __name__ == "__main__":
    main()
