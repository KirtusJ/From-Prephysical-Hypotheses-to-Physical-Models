"""Run python -B check_network_functional.py OUTPUT_DIRECTORY (standard library).

Read two archived outcome tables adjacent to this script in results/. Write a
separate audit JSON. Exact entries are rational coefficients of 1 and 1/sqrt(2).
"""
import argparse
import hashlib
import json
from collections import Counter
from fractions import Fraction as F
from itertools import product
from pathlib import Path


BELLS = ((0,0),(1,0),(0,1),(1,1))  # archived (parity,phase), in named Bell order
SETTINGS = tuple(product(range(1,4),range(1,7)))
SIGNS = tuple(product((1,-1),repeat=2))
DOMAIN = tuple((x,z,p,s,a,c) for x,z in SETTINGS for p,s in BELLS for a,c in SIGNS)


def e3(x,z,b1,b2,a,c):
    """Direct numbered-setting transcription of Appendix E Eq. (E3)."""
    Z, X, Y = (-1)**b2,(-1)**b1,-(-1)**(b1+b2)
    numeric = {
        (1,1):Z, (1,2):Z, (2,1):X, (2,2):-X,
        (1,3):Z, (1,4):Z, (3,3):Y, (3,4):-Y,
        (2,5):X, (2,6):X, (3,5):Y, (3,6):-Y,
    }
    return numeric.get((x,z),0)*a*c


def named(x,z,p,s,a,c):
    # Local checkers use Pauli letters and the ordered-pair tilt.
    axis = ('Z','X','Y')[x-1]
    (i,j),tilt = list(product((('Z','X'),('Z','Y'),('X','Y')),(1,-1)))[z-1]
    weight = 1 if axis==i else tilt if axis==j else 0
    bell = {'Z':1-2*p,'X':1-2*s,'Y':-(1-2*p)*(1-2*s)}
    return a*c*weight*bell[axis]


def coefficient_audit():
    alphabet = []
    bad = []
    for row in DOMAIN:
        x,z,p,s,a,c = row
        published = e3(x,z,s,p,a,c)
        assert published==named(*row)
        if published!=e3(x,z,p,s,a,c):
            bad.append(row)
        alphabet.append(published)
    assert Counter(alphabet)=={-1:96,0:96,1:96} and len(bad)==64
    return dict(total=len(DOMAIN),coefficients_in_domain_order=alphabet,
                counts={str(k):v for k,v in sorted(Counter(alphabet).items())},
                mismatches=0,wrong_bob_bit_order_mismatches=len(bad),
                first_wrong_bit_witness=list(bad[0]))


def pair_sum(raw):
    return [sum(v[i] for v in raw) for i in range(2)]


def contract(bins,weight=F(1)):
    assert len(bins)==len(DOMAIN)
    by_bell = {b:[F(),F()] for b in BELLS}
    by_pair = [[F(),F()] for _ in range(3)]
    wrong = [F(),F()]
    for start in range(0,len(bins),16):
        assert pair_sum(bins[start:start+16])==[weight,0]
        for b in range(4):
            off = start+b*4
            assert pair_sum(bins[off:off+4])==[weight/4,0]
    for (x,z,p,s,a,c),v in zip(DOMAIN,bins):
        C = e3(x,z,s,p,a,c)
        for i in range(2):
            by_bell[p,s][i] += C*v[i]
            by_pair[(z-1)//2][i] += C*v[i]
            wrong[i] += e3(x,z,p,s,a,c)*v[i]
    total = pair_sum(by_bell.values())
    assert total==pair_sum(by_pair)
    return total,by_pair,dict(T=list(map(str,total)),T_b=[list(map(str,by_bell[b])) for b in BELLS],
                              three_terms=[list(map(str,q)) for q in by_pair],
                              wrong_bits_T=list(map(str,wrong)))


def rational_family(data):
    cases = []
    count = 0
    for state in data['states_and_controls']:
        indices = state['bin_indices']
        assert len(indices)==288
        baseline = state['completed_bin_dictionary']
        rows = [('completed',baseline,state['completed_score'],state['completed_CHSH'])]
        rows.extend((row['calls'],row['unconditional_bin_dictionary'],row['score'],row['unconditional_CHSH'])
                    for row in state['deadlines'])
        checked = []
        for deadline,values,target,three in rows:
            table = [[F(values[i]),F()] for i in indices]
            total,terms,out = contract(table)
            assert total==[F(target),0] and [t[0] for t in terms]==list(map(F,three))
            count += 1
            checked.append(dict(deadline=deadline,**out))
        cases.append(dict(nu=state['nu'],weights_reversed=state['weights_reversed'],
                          tilt_sign_reversed=state['second_coefficient_reversed'],contractions=checked))
    assert count==42
    return dict(cases=cases,full_tables=count,individual_bins=count*len(DOMAIN))


def plane_family(data):
    cases = []
    for state in data['states']:
        tables = [[],[],[]]
        assert [(r['x'],r['z']) for r in state['full_table']]==list(SETTINGS)
        for row in state['full_table']:
            assert [tuple(b['b']) for b in row['bell_rows']]==list(BELLS)
            for bell in row['bell_rows']:
                blocks = [bell['all_grades'],*bell['grade_joint']]
                for dest,block in zip(tables,blocks):
                    dest.extend([list(map(F,v)) for v in block])
        assert all(pair_sum((b,c))==a for a,b,c in zip(*tables))
        total,terms,mix = contract(tables[0])
        assert total==[0,F(state['score_numerator_over_sqrt2'])]
        assert [q[1] for q in terms]==list(map(F,state['CHSH_numerators_over_sqrt2']))
        grade = []
        for table,info in zip(tables[1:],state['grades']):
            w = F(info['mass'])
            g,components,out = contract(table,w)
            assert [q[1] for q in components]==list(map(F,info['joint_CHSH_numerators']))
            assert g[0]==0
            grade.append(dict(grade=info['grade'],joint_mass=str(w),**out))
        cases.append(dict(nu=state['nu'],unconditioned=mix,joint_grade_contractions=grade))
    return dict(cases=cases,full_tables=3*len(cases),individual_bins=3*len(cases)*len(DOMAIN))


def main(directory):
    root = Path(__file__).resolve().parent/'results'
    sources = {}
    for name in ('rational_network_ports','independent_source_phase'):
        raw = (root/(name+'.json')).read_bytes()
        sources[name] = (json.loads(raw),hashlib.sha256(raw).hexdigest())
    data = dict(primary_E3='https://arxiv.org/pdf/2101.10873#page=11',
        peer_reviewed='https://doi.org/10.1038/s41586-021-04160-4',
        optical_convention='https://doi.org/10.1103/PhysRevLett.129.140401',
        domain='For increasing numbered x=1..3 and z=1..6, then (p,s)=(00,10,01,11), then (a,c)=(++,+-,-+,--). The 288 coefficient entries multiply the JOINT P(a,b,c | x,z). Bell bits in Renou are (b1,b2)=(s,p), with names Phi+,Psi+,Phi-,Psi-. The singlet convention differs by an overall vector sign, which leaves its projector unchanged.',
        tables='Every number pair [r,t] denotes r+t/sqrt(2). T_b contributions are in published b1b2 order 00,01,10,11. S_b(x,z) in E3 is the signed sum of four joint probabilities. Its conditional version given Bob would require dividing by P(b); only the version weighted by P(b) is summed in T. Dividing by each P(b)=1/4 and summing without restoring their weights yields four times T, including 24 sqrt(2) for the ideal reference. The two endpoint names are already those of Renou; the separate Wu experiment puts the six settings at the opposite endpoint.',
        scope='Independent literal E3 coefficient and archive contraction. No SDP, optical experiment or data fit was rerun. The real bilocal ceiling 7.6605 and its source premises are from Appendix E, Theorem 3, Eq. E4. The seven-call score uses a shared reference at nu=1 outside the real product-source assumption.',
        archive_raw_sha256={k:row[1] for k,row in sources.items()},coefficient_audit=coefficient_audit(),
        rational_network=rational_family(sources['rational_network_ports'][0]),
        independent_plane=plane_family(sources['independent_source_phase'][0]))
    directory.mkdir(parents=True,exist_ok=True)
    (directory/'network_functional.json').write_bytes((json.dumps(data,separators=(',',':'))+'\n').encode())


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('output',type=Path)
    main(p.parse_args().output)
