"""Run python -B check_rational_network_ports.py OUTPUT_DIRECTORY (standard library).

All stored probabilities and score comparisons use integer arithmetic. The local
Walsh selector is verified on a complete basis, through every recovery record.
"""
import argparse
import json
from fractions import Fraction as F
from itertools import product
from pathlib import Path

from check_rational_bypass import norm, walsh


PAIRS = (('Z','X'),('Z','Y'),('X','Y'))
AXES = ('Z','X','Y')
SIGNS = (1,-1)
BELLS = ((0,0),(1,0),(0,1),(1,1))
P = F(25,64)
BOUND = F(76605,10000)


def unsigned_axis(point, axis, data, plane):
    """Target coordinate and sign under Z, X or J_data J_plane."""
    xb = point >> data & 1
    if axis=='Z':
        return point, 1-2*xb
    if axis=='X':
        return point^(1<<data), 1
    assert axis=='Y'
    return point^(1<<data)^(1<<plane), (1-2*xb)*(1-2*((point>>plane)&1))


def observed(v,axis,data,plane):
    out = [0]*len(v)
    for point,value in enumerate(v):
        k,s = unsigned_axis(point,axis,data,plane)
        out[k] += s*value
    return out


def selector(pair, orient):
    # Outermost bit junk, inner logical bits [coin/data,plane,acted arm],
    # innermost three bits Walsh address. States 0..3 are the idle arm.
    permutation = []
    for idx in range(128):
        logical,label = divmod(idx,8)
        junk,mode = divmod(logical,8)
        factor = 1
        if mode>=4 and label<7:
            axis = pair[int(label>=3)]
            mode,factor = unsigned_axis(mode,axis,0,1)
            if label>=3:
                factor *= orient
        elif label >= (7 if mode>=4 else 5):
            junk ^= 1
        permutation.append(((8*junk+mode)*8+label,factor))
    assert sorted(i for i,_ in permutation)==list(range(128))
    assert all(permutation[j]==(i,s) for i,(j,s) in enumerate(permutation))

    def traverse(v):
        raw = v.copy()
        walsh(raw,8)
        out = [0]*len(raw)
        for x,(i,s) in zip(raw,permutation):
            out[i] = s*x
        walsh(out,8)
        return out
    return traverse


def retain(v,yes):
    return [x if ((i<64 and i%8==0)==yes) else 0 for i,x in enumerate(v)]


def freeze_branches(pair,orient,rounds):
    """Propagate eight input basis columns through W, coarse flags and retries."""
    W = selector(pair,orient)
    initial = [[int(i==8*j) for i in range(128)] for j in range(8)]
    first = [W(v) for v in initial]
    assert all(W(v)==[64*x for x in raw] for v,raw in zip(first,initial))
    wanted = []
    for j in range(8):
        unit = [int(i==j) for i in range(8)]
        ideal = ([5*x for x in unit] if j<4 else
                 [3*x+4*orient*y for x,y in zip(observed(unit,pair[0],0,1),observed(unit,pair[1],0,1))])
        assert [first[j][8*i] for i in range(8)]==ideal
        wanted.append(ideal)

    def mass(cols,scale,success):
        if success:
            # Identical signed scalar on all columns, so all coherences transfer.
            multiple = F(cols[0][0],5)
            assert all([col[8*i] for i in range(8)]==[multiple*y for y in target]
                       for col,target in zip(cols,wanted))
        # Every branch effect is a scalar identity including the terminal timeout.
        shared_norm = norm(cols[0])
        assert all(norm(v)==shared_norm for v in cols)
        assert all(sum(a*b for a,b in zip(cols[i],cols[j]))==0 for i in range(8) for j in range(i))
        return F(shared_norm,scale)

    live = {'0':[retain(v,False) for v in first]}
    successes = {'1':mass([retain(v,True) for v in first],64,True)}
    rows = []
    for ell in range(rounds+1):
        scale = 64**(1+2*ell)
        failures = {s:mass(cols,scale,False) for s,cols in live.items()}
        total = sum(failures.values())
        assert total==(1-P)*(1-2*P*(1-P))**ell and total+sum(successes.values())==1
        rows.append(dict(retry_pairs=ell,timeout_words={s:str(x) for s,x in failures.items()},
                         success_words_at_or_before_deadline={s:str(x) for s,x in successes.items()},
                         timeout=str(total)))
        if ell==rounds:
            break
        new = {}
        for word,cols in live.items():
            back = [W(v) for v in cols]
            for bit in (0,1):
                amps = [W(retain(v,bool(bit))) for v in back]
                stem = word+str(bit)
                successes[stem+'1'] = mass([retain(v,True) for v in amps],scale*64**2,True)
                new[stem+'0'] = [retain(v,False) for v in amps]
        live = new
    return rows


def swap_bell(parity,phase):
    # Contract real Phi+ sources AB1 & B2C at Bob with the full Bell basis.
    swapped = [0]*4
    for a,b1,b2,c in product(range(2),repeat=4):
        swapped[a+2*c] += int(a==b1 and b2==c and b1^b2==parity)*(-1)**(phase*b1)
    assert norm(swapped)==2  # two Bell preparations and one Bell bra give denominator sqrt(8)
    return swapped


def source(swapped,grade,seed):
    raw = [0]*16
    for i,x in enumerate(swapped):
        a,c = i&1,i>>1
        left,right = seed&1,seed>>1
        k = a+2*left+4*c+8*right
        raw[k] += x
        raw[k^10] -= grade*(1-2*left)*(1-2*right)*x
    assert norm(raw)==4
    return raw


def ideal_table(nu,reverse_weights=False,reverse_tilt=False):
    wa,wb = (4,3) if reverse_weights else (3,4)
    flip = -1 if reverse_tilt else 1
    table = []
    witness = [F()]*3
    for x,(pair_idx,pair),tilt in product(AXES,enumerate(PAIRS),SIGNS):
        settings = []
        for parity,phase in BELLS:
            bins = [F()]*4
            swapped = swap_bell(parity,phase)
            for grade,seed in product(SIGNS,range(2)):
                v = source(swapped,grade,seed)
                # p(Bell)=1/4, p(grade)=(1+grade*nu)/2, two normalized seeds per grade.
                branch = F(norm(swapped),8)*(1+grade*nu)/4
                alice = observed(v,x,0,1)
                for idx,(a,c) in enumerate(product(SIGNS,repeat=2)):
                    after_a = [u+a*w for u,w in zip(v,alice)]
                    first = observed(after_a,pair[0],2,3)
                    second = observed(after_a,pair[1],2,3)
                    # Final H of the held arm yields numerator 5I +/- (wa A +/- wb B).
                    out = [5*u+c*(wa*w+flip*tilt*wb*y) for u,w,y in zip(after_a,first,second)]
                    bins[idx] += branch*F(norm(out),400*norm(v))
            assert sum(bins)==F(1,4)
            sign = {'Z':(-1)**parity,'X':(-1)**phase,'Y':-(-1)**(parity+phase)}[x]
            active = 1 if x==pair[0] else tilt if x==pair[1] else 0
            for p,(a,c) in zip(bins,product(SIGNS,repeat=2)):
                witness[pair_idx] += sign*active*a*c*p
            settings.extend(bins)
        assert sum(settings)==1
        table.extend(settings)
    closed = F(2,5)*(3*wa+flip*wb*(1+2*nu))
    assert sum(witness)==closed
    return table,witness


def score_bins(table):
    data = iter(table)
    terms = [F()]*3
    for x,(j,pair),tilt in product(AXES,enumerate(PAIRS),SIGNS):
        for parity,phase in BELLS:
            z_sign,x_sign = 1-2*parity,1-2*phase
            weight = dict(zip(AXES,(z_sign,x_sign,-z_sign*x_sign)))[x]
            weight *= {pair[0]:1,pair[1]:tilt}.get(x,0)
            pp,pm,mp,mm = [next(data) for _ in range(4)]
            terms[j] += weight*(pp+mm-pm-mp)
    assert next(data,None) is None
    return terms


def compile_case(nu,raw_logs,reverse_weights=False,reverse_tilt=False):
    table,witness = ideal_table(nu,reverse_weights,reverse_tilt)
    unique = sorted(set(table))
    encoded = [unique.index(x) for x in table]
    deadlines = []
    for record in raw_logs:
        ell = record['retry_pairs']
        timeout = F(record['timeout'])
        # Complete failure-word effects are state-independent. A fresh H on a
        # local blank yields an unbiased bit, independent of a and Bob's result.
        missed = timeout/16
        total = [(1-timeout)*x+missed for x in unique]
        for off in range(0,len(encoded),16):
            assert sum(total[i] for i in encoded[off:off+16])==1
        timed_terms = score_bins(total[i] for i in encoded)
        assert timed_terms==[(1-timeout)*x for x in witness]
        w = sum(timed_terms)
        deadlines.append(dict(calls=2*ell+1,timeout_joint_per_abc=str(missed),
                              unconditional_bin_dictionary=list(map(str,total)),
                              unconditional_CHSH=list(map(str,timed_terms)),
                              score=str(w),score_decimal=float(w),gap_to_7_6605=str(w-BOUND)))
    return dict(nu=str(nu),weights_reversed=reverse_weights,second_coefficient_reversed=reverse_tilt,
                completed_score=str(sum(witness)),completed_CHSH=list(map(str,witness)),
                completed_bin_dictionary=list(map(str,unique)),bin_indices=encoded,deadlines=deadlines)


def main(directory):
    logs = [freeze_branches(pair,t,4) for pair,t in product(PAIRS,SIGNS)]
    assert all(row==logs[0] for row in logs)
    rows = [compile_case(nu,logs[0]) for nu in map(F,(-1,0,F(1,2),1))]
    rows += [compile_case(F(0),logs[0],reverse_weights=True),
             compile_case(F(1),logs[0],reverse_weights=True),
             compile_case(F(1),logs[0],reverse_tilt=True)]
    threshold = []
    for rec in logs[0]:
        delivery = 1-F(rec['timeout'])
        threshold.append(str((5*BOUND/delivery-26)/16))
    ideal = rows[3]['deadlines']
    assert [r['calls'] for r in ideal if F(r['score'])>BOUND]==[7,9]
    result = dict(
        apparatus='Two complete real Bell sources and Bell analyzer on the data coordinates. Endpoint plane density (I+nu Q)/4, Q=-J_A J_C. Alice uses signed Z, X, or J_data J_plane between Ramsey Hadamards. Charlie measures a synchronized controlled V=(3A +/- 4B)/5 between Ramsey Hadamards. A three-bit Walsh, conditional signed permutation and inverse Walsh implement one oracle call. Coarse clean-port read, then alternating adjoint/forward recovery. Timeouts emit a fresh fair local bit. No settings or Bob outcomes are dropped.',
        table_order='Each bin_indices array contains 288 entries. Outer to inner: Alice Z,X,Y; ordered Charlie pair ZX,ZY,XY and plus,minus within pair; Bob (00,10,01,11) parity then phase; outcomes (a,c)=(++,+-,-+,--). Look up the index in completed_bin_dictionary or the desired unconditional_bin_dictionary. Both give joint p(a,b,c|x,z), including Bob. Timeout_joint_per_abc is the raw contribution of timeout in any bin; divide each timeout word mass by 16 for its individual joint contribution. Each success word contributes its mass times the completed bin.',
        selector='All six nominal signed selectors were propagated from every one of the eight input basis columns. For every success history the selected operator is one common scalar times 5I on idle and 3A +/- 4B on acted. Every terminal failure-word Gram matrix is scalar identity. The coarse pointer is essential. Reverse-weight control permutes coefficient roles, giving 4A +/- 3B, with the same local success Gram factors by exchange of the signed involutions. Reversing the tilt swaps the two Charlie settings under held scoring labels.',
        columns_tested=8,selector_settings_tested=6,shared_record_weights=logs[0],
        states_and_controls=rows,minimum_nu_for_strict_crossing_by_deadline=threshold,
        published_bound='Renou et al. Appendix E, Theorem 3, Eq. (E4): T <= 7.6605 for the stated real product-source model, including shared classical randomness. Main text displays 7.66. The authors report a computer-precision SDP dual bound. This checker verifies the signed-network probabilities and compares to their published figure; it does not re-solve their SDP.',
        primary='https://arxiv.org/pdf/2101.10873#page=12',
        scope='Nonzero nu supplies an additional shared real quantum reference across the putatively independent source cut. The crossing is a rational circuit prediction under that preparation and the Born rule, not a violation by independent real sources or an observed experimental score. The deadline counts Walsh-selector calls only, not contact, gate-layer, propagation or physical preparation time.')
    directory.mkdir(parents=True,exist_ok=True)
    (directory/'rational_network_ports.json').write_bytes((json.dumps(result,separators=(',',':'))+'\n').encode())


if __name__=='__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('output',type=Path)
    main(p.parse_args().output)
