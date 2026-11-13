"""Cross-review program xr19 (own code; imports nothing from Director_G).

Run: python3 -I xr19_contact.py OUTDIR      (refuses to overwrite OUTDIR/xr19_contact_result.json)
Exact integer / Fraction arithmetic throughout. Seed 20261113.

Construction taken from the note text only:
 planes: J|0>=|1>, J|1>=-|0>;  contact Q=-J_A J_C read by H-control-H on blank |00>;
 negative grade corrected by Z on the second plane;
 data: real Phi+ on A B1 and B2 C, Bob projects B1B2 on the four real Bell vectors (p,s);
 Alice analyzers Z, X, J_data J_ref;  Charlie V=(3j +/- 4k)/5 for (j,k)=(Z,X),(Z,Y),(X,Y),
 read by an H-control-H meter whose controlled-V is one "call": Walsh on 8 labels,
 acted arm labels 0-2 -> j, 3-6 -> +/-k, 7 -> junk flip; idle arm labels 0-4 -> I, 5-7 -> junk flip,
 inverse Walsh; success = junk 0 and label 0.  On failure: call again (inverse), read reset
 yes/no, call again, recheck.  Deadline 1+2l calls.  Timeout -> Charlie emits a fresh fair sign.
 Score = sum over pairs, tilt, Alice i in {j,k}, Bob b of  P(b) t_i(b) d_i E(ac|b), with
 t_Z=(-1)^p, t_X=(-1)^s, t_Y=-t_Z t_X, d_j=+1, d_k=tilt.  ALL trials in the denominator.

PREDICATES (fixed before first run)
 P1  every (reference, Alice setting, Charlie setting, deadline) table over (a,b,c) sums to exactly 1
     with timeouts included.
 P2  end-to-end undelivered mass after 1+2l calls equals (39/64)(1073/2048)^l, l=0..3, for every
     setting pair, Bob outcome, Alice outcome and reference tested (state independence).
 P3  corrected contact from blank |00> (both grades, each prob 1/2, Z on grade -): seven-call
     all-trial score equals (42/5)(1-f_3) exactly, prints as 7.663838 at 6 decimals, and is
     strictly greater than 76605/10000; margin prints as 0.003338.
 P4  same reference: 5 calls -> 6.994912; 1 and 3 calls (not reported in the note) equal (42/5)(1-f_l).
 P5  9 calls -> 8.014306 and 11 calls (not reported) = (42/5)(1-f_5), using f_4,f_5 from a
     Kraus-level propagation of all 8 input basis columns, 6 selectors (Python big ints);
     at that level every column has the same failure mass (hypothesis of state independence tested).
 P6  uncorrected contact (both grades summed, no feed-forward): score = (26/5)(1-f_l), l=0..3.
 P7  mixed omega_nu=(I+nu K)/4 built from K-eigenvectors: score=(1-f_l)(26+16nu)/5 for
     nu in {-1,0,1/2,3/4,1}; nu=3/4 is not in the note or its result file.
 P8  independent real product references (hypothesis tested per instance: each is a tensor product of
     two nonzero real vectors, checked by rank-1 determinant test; number qualifying reported):
     <K>=0 exactly for all; end-to-end score for the first 3 equals (26/5)(1-f_l) < bound at all l<=3.
 P9  reflecting BOTH reference planes (Z on each) leaves the complete (a,b,c|x,z) table identical at
     every deadline (absolute label not identified by these records); reflecting ONE plane changes it
     and gives score 2(1-f_l).
 MEASURED ONLY (no pass/fail; no threshold used)
 M1  minimum nu for strict crossing at each deadline: (5*B/(1-f_l)-26)/16 with B=76605/10000.
 M2  score if timeouts are dropped (post-selected) instead of filled: 42/5; and margin against
     B'=7.66 (main-text rounding quoted in the author's result file) and B+0.00005 (half unit of
     the last printed digit of 7.6605, the only basis used).
 M3  score when the grade record does not reach Charlie's plane but the scorer relabels the tilt of
     the Y-containing settings by grade afterwards.
 M4  one-plane marginals and purity of the contact output (is the reference entangled across A|C?).
"""
import sys, json, random, os
from fractions import Fraction as F
from itertools import product
import numpy as np

SEED = 20261113
B = F(76605, 10000)
PAIRS = (('Z', 'X'), ('Z', 'Y'), ('X', 'Y'))
AX = ('Z', 'X', 'Y')
H8 = np.array([[(-1) ** bin(i & j).count('1') for j in range(8)] for i in range(8)], dtype=np.int64)


def op(arr, name, d, r):
    """Apply Z or X on axis d, or J(x)J on axes d,r.  J|0>=|1>, J|1>=-|0>."""
    a = np.moveaxis(arr, (d, r), (0, 1))
    out = a.copy()
    if name == 'Z':
        out[1] = -a[1]
    elif name == 'X':
        out[0], out[1] = a[1], a[0]
    else:  # (J(x)J v)[d,r] = sg(d) sg(r) v[1-d,1-r], sg(1)=+1, sg(0)=-1
        for i, k in product(range(2), repeat=2):
            out[i, k] = (1 if i else -1) * (1 if k else -1) * a[1 - i, 1 - k]
    return np.moveaxis(out, (0, 1), (d, r))


def call(arr, j, k, tilt):
    """One selector call. Last five axes: cD, cR, ctrl, junk, label. Amplitude scale x8."""
    n = arr.ndim
    cD, cR = n - 5, n - 4
    w = arr.dot(H8.astype(arr.dtype))
    out = np.zeros_like(w)
    for l in range(8):
        idle = w[..., 0, :, l]
        out[..., 0, :, l] = idle if l < 5 else idle[..., ::-1]
        act = w[..., 1, :, l]            # axes ..., cD, cR, junk
        if l < 3:
            res = op(act, j, cD, cR)
        elif l < 7:
            res = tilt * op(act, k, cD, cR)
        else:
            res = act[..., ::-1]
        out[..., 1, :, l] = res
    return out.dot(H8.astype(arr.dtype))


def split(v):
    ok = np.zeros_like(v)
    ok[..., 0, 0] = v[..., 0, 0]
    return ok, v - ok


def nrm(v):
    return int((v.reshape(-1) * v.reshape(-1)).sum())


def protocol(v, j, k, tilt, L):
    """Returns successes [(ncalls, vec)] and failure mass numerators per level (scale 64^(1+2l))."""
    succ, fail = [], []
    ok, bad = split(call(v, j, k, tilt))
    succ.append((1, ok))
    live = [bad]
    for l in range(L + 1):
        fail.append(sum(nrm(x) for x in live))
        if l == L:
            break
        new = []
        for x in live:
            back = call(x, j, k, tilt)
            for part in split(back):          # reset yes / reset no, both kept
                ok, bad = split(call(part, j, k, tilt))
                succ.append((3 + 2 * l, ok))
                new.append(bad)
        live = new
    return succ, fail


def bob_state(p, s):
    d = np.zeros((2, 2), dtype=np.int64)
    for a in range(2):
        d[a, a ^ p] = (-1) ** (s * a)
    return d


def table_for(ref, L=3, relabel_tilt=1):
    """ref: integer 2x2 array over (aR,cR). Returns {l: {(x,pair,tilt,b,a,c): prob}}, fail-mass set."""
    tabs = {l: {} for l in range(L + 1)}
    fails = set()
    Nref = nrm(ref)
    for x, (pi, (j, k)), tilt, (p, s) in product(AX, enumerate(PAIRS), (1, -1), product(range(2), repeat=2)):
        data = bob_state(p, s)
        psi = np.einsum('ac,br->abcr', data, ref)
        Apsi = op(psi, x, 0, 1)
        eff_tilt = tilt * (relabel_tilt if 'Y' == k else 1)
        for a in (1, -1):
            v = np.zeros((2, 2, 2, 2, 2, 2, 8), dtype=np.int64)
            pa = psi + a * Apsi
            v[..., 0, 0, 0] = pa
            v[..., 1, 0, 0] = pa
            N0 = 2 * Nref * 4 * 2          # data norm, Alice projector scale, control H
            succ, fail = protocol(v, j, k, eff_tilt, L)
            pA = F(nrm(pa), 2 * Nref * 4)   # P(a|b)
            for l in range(L + 1):
                done = {1: F(0), -1: F(0)}
                for ncalls, vec in succ:
                    if ncalls <= 1 + 2 * l:
                        plus = vec[..., 0, 0, 0] + vec[..., 1, 0, 0]
                        minus = vec[..., 0, 0, 0] - vec[..., 1, 0, 0]
                        done[1] += F(nrm(plus), N0 * 64 ** ncalls * 2)
                        done[-1] += F(nrm(minus), N0 * 64 ** ncalls * 2)
                tmo = F(fail[l], N0 * 64 ** (1 + 2 * l))
                assert done[1] + done[-1] + tmo == pA, 'internal bookkeeping'
                fails.add((l, tmo / pA if pA else None))
                for c in (1, -1):
                    tabs[l][(x, pi, tilt, (p, s), a, c)] = F(1, 4) * (done[c] + tmo / 2)
    return tabs, fails


def score(tab):
    T = F(0)
    for (x, pi, tilt, (p, s), a, c), pr in tab.items():
        j, k = PAIRS[pi]
        d = 1 if x == j else tilt if x == k else 0
        t = {'Z': (-1) ** p, 'X': (-1) ** s, 'Y': -(-1) ** (p + s)}[x]
        T += t * d * a * c * pr
    return T


def mix(parts):
    out = {}
    for w, tabs in parts:
        for l, tab in tabs.items():
            o = out.setdefault(l, {})
            for key, pr in tab.items():
                o[key] = o.get(key, F(0)) + w * pr
    return out


def sums_ok(tabs):
    for tab in tabs.values():
        acc = {}
        for (x, pi, tilt, b, a, c), pr in tab.items():
            acc[(x, pi, tilt)] = acc.get((x, pi, tilt), F(0)) + pr
        if any(v != 1 for v in acc.values()):
            return False
    return True


def kraus_fail(L):
    """Failure mass per level from all 8 basis columns of (cD,cR,ctrl), all 6 selectors, big ints."""
    global H8
    res = None
    for (j, k), tilt in product(PAIRS, (1, -1)):
        per_col = []
        for m in range(8):
            v = np.zeros((2, 2, 2, 2, 8), dtype=object)
            v[...] = 0
            v[m >> 2 & 1, m >> 1 & 1, m & 1, 0, 0] = 1
            _, fail = protocol(v, j, k, tilt, L)
            per_col.append(tuple(F(fail[l], 64 ** (1 + 2 * l)) for l in range(L + 1)))
        if len(set(per_col)) != 1:
            return None, 'columns differ'
        if res is None:
            res = per_col[0]
        elif res != per_col[0]:
            return None, 'selectors differ'
    return res, 'ok'


def main(outdir):
    path = os.path.join(outdir, 'xr19_contact_result.json')
    if os.path.exists(path):
        sys.exit('refusing to overwrite ' + path)
    rng = random.Random(SEED)
    R = {'seed': SEED, 'bound_used': str(B), 'predicates': {}, 'measured': {}, 'followups': []}
    P = R['predicates']
    f = [F(39, 64) * F(1073, 2048) ** l for l in range(6)]

    # contact on blank |00>:  P_+-|00> = (|00> +- Q|00>)/2, Q=-J(x)J
    blank = np.zeros((2, 2), dtype=np.int64); blank[0, 0] = 1
    Qb = -op(blank, 'Y', 0, 1)
    gplus, gminus = blank + Qb, blank - Qb
    grade_prob = (F(nrm(gplus), 4), F(nrm(gminus), 4))
    corr_minus = op(gminus, 'Z', 1, 0)        # Z on second plane
    R['contact'] = dict(grade_plus=gplus.tolist(), grade_minus=gminus.tolist(),
                        grade_probs=list(map(str, grade_prob)), corrected_minus=corr_minus.tolist())

    tp, fp = table_for(gplus)
    tm_corr, fm1 = table_for(corr_minus)
    tm_raw, fm2 = table_for(gminus)
    corrected = mix([(grade_prob[0], tp), (grade_prob[1], tm_corr)])
    uncorrected = mix([(grade_prob[0], tp), (grade_prob[1], tm_raw)])
    allfails = fp | fm1 | fm2

    # K eigenvectors for mixed omega_nu
    e01p = np.array([[0, 1], [1, 0]], dtype=np.int64)       # |01>+|10>  (K=+1)
    e01m = np.array([[0, 1], [-1, 0]], dtype=np.int64)      # |01>-|10>  (K=-1)
    Kchk = [(nm, (-op(v, 'Y', 0, 1) == sgn * v).all()) for nm, v, sgn in
            (('00-11', gplus, 1), ('01+10', e01p, 1), ('00+11', gminus, -1), ('01-10', e01m, -1))]
    R['K_eigen_hypothesis'] = [[n, bool(b)] for n, b in Kchk]
    t01p, f3 = table_for(e01p); t01m, f4 = table_for(e01m)
    allfails |= f3 | f4

    def omega(nu):
        return mix([((1 + nu) / 4, tp), ((1 + nu) / 4, t01p), ((1 - nu) / 4, tm_raw), ((1 - nu) / 4, t01m)])

    nus = [F(-1), F(0), F(1, 2), F(3, 4), F(1)]
    om = {nu: omega(nu) for nu in nus}

    # independent product references
    qual, kzero, prods = 0, 0, []
    for _ in range(200):
        u = [rng.randint(-9, 9) for _ in range(2)]; w = [rng.randint(-9, 9) for _ in range(2)]
        ref = np.array([[u[0] * w[0], u[0] * w[1]], [u[1] * w[0], u[1] * w[1]]], dtype=np.int64)
        ok = nrm(ref) > 0 and ref[0, 0] * ref[1, 1] - ref[0, 1] * ref[1, 0] == 0
        if not ok:
            continue
        qual += 1
        kexp = int((ref * (-op(ref, 'Y', 0, 1))).sum())
        kzero += kexp == 0
        prods.append(ref)
    prod_scores = []
    for ref in prods[:3]:
        t, ff = table_for(ref); allfails |= ff
        prod_scores.append([score(t[l]) for l in range(4)])

    both_ref, f5 = table_for(op(op(gplus, 'Z', 0, 1), 'Z', 1, 0))
    one_ref, f6 = table_for(op(gplus, 'Z', 0, 1))
    allfails |= f5 | f6

    sc = {l: score(corrected[l]) for l in range(4)}
    P['P1_normalised'] = all(sums_ok(t) for t in [corrected, uncorrected, both_ref, one_ref] + list(om.values()))
    P['P2_timeout_mass_state_independent'] = allfails == {(l, f[l]) for l in range(4)}
    P['P3_seven_call'] = (sc[3] == F(42, 5) * (1 - f[3]) and '%.6f' % float(sc[3]) == '7.663838'
                          and sc[3] > B and '%.6f' % float(sc[3] - B) == '0.003338')
    P['P4_other_deadlines'] = ('%.6f' % float(sc[2]) == '6.994912'
                               and all(sc[l] == F(42, 5) * (1 - f[l]) for l in (0, 1)))
    kf, why = kraus_fail(5)
    P['P5_nine_eleven_calls'] = (kf is not None and tuple(kf) == tuple(f)
                                 and '%.6f' % float(F(42, 5) * (1 - f[4])) == '8.014306')
    R['kraus_level'] = dict(status=why, fail=None if kf is None else list(map(str, kf)))
    P['P6_uncorrected'] = all(score(uncorrected[l]) == F(26, 5) * (1 - f[l]) for l in range(4))
    P['P7_omega_nu'] = all(score(om[nu][l]) == (1 - f[l]) * (26 + 16 * nu) / 5 for nu in nus for l in range(4))
    P['P8_independent_products'] = (qual > 0 and kzero == qual and all(
        s[l] == F(26, 5) * (1 - f[l]) and s[l] < B for s in prod_scores for l in range(4)))
    R['P8_counts'] = dict(drawn=200, qualifying=qual, K_zero=kzero, end_to_end=len(prod_scores))
    P['P9_conjugation'] = (all(both_ref[l] == tp[l] for l in range(4))
                           and all(one_ref[l] != tp[l] and score(one_ref[l]) == 2 * (1 - f[l]) for l in range(4)))

    M = R['measured']
    M['scores_corrected_contact'] = {str(1 + 2 * l): [str(sc[l]), float(sc[l])] for l in range(4)}
    M['score_9_11_calls_closed_form_with_kraus_f'] = {str(1 + 2 * l): [str(F(42, 5) * (1 - f[l])), float(F(42, 5) * (1 - f[l]))] for l in (4, 5)}
    M['exact_margin_7_calls'] = [str(sc[3] - B), float(sc[3] - B)]
    M['M1_min_nu'] = {str(1 + 2 * l): [str((5 * B / (1 - f[l]) - 26) / 16), float((5 * B / (1 - f[l]) - 26) / 16)] for l in range(6)}
    M['M2_postselected_score'] = str(F(42, 5))
    M['M2_margin_vs_7.66'] = float(sc[3] - F(766, 100))
    M['M2_margin_vs_bound_plus_half_last_digit'] = float(sc[3] - B - F(5, 100000))
    M['M2_max_delivery_shortfall_tolerated_at_7_calls'] = float(1 - B / F(42, 5) - f[3])
    tm_rel, _ = table_for(gminus, relabel_tilt=-1)
    rel = mix([(grade_prob[0], tp), (grade_prob[1], tm_rel)])
    M['M3_scorer_relabels_by_grade'] = {str(1 + 2 * l): str(score(rel[l])) for l in range(4)}
    M['M3_no_record_at_charlie'] = {str(1 + 2 * l): str(score(uncorrected[l])) for l in range(4)}
    rho = np.einsum('ab,cd->abcd', gplus, gplus)        # unnormalised, norm 2
    margA = np.einsum('abcb->ac', rho)
    M['M4_contact_output'] = dict(vector_aR_cR=gplus.tolist(), norm2=nrm(gplus),
                                  marginal_A_times_2=margA.tolist(),
                                  schmidt_rank=int(gplus[0, 0] * gplus[1, 1] - gplus[0, 1] * gplus[1, 0] != 0) + 1,
                                  note='pure, Schmidt rank 2 with marginal I/2: entangled across A|C')
    for name, okv in P.items():
        if not okv:
            R['followups'].append(name + ': FAILED, kept; see report')
    R['predicate_counts'] = dict(met=sum(map(bool, P.values())), failed=sum(not v for v in P.values()), measured_only=4)
    P.update({k: bool(v) for k, v in P.items()})
    with open(path, 'x') as fh:
        fh.write(json.dumps(R, indent=1) + '\n')
    print(json.dumps(R, indent=1))


if __name__ == '__main__':
    main(sys.argv[1])
