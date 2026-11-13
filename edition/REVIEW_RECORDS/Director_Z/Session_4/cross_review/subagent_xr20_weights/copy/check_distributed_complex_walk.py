"""Run python -B check_distributed_complex_walk.py OUTPUT_DIRECTORY (standard library).

Physical amplitudes are signed integers with a common denominator. A probability
is computed as the exact fraction of squared norm in each port.
"""
import argparse
import json
from fractions import Fraction
from pathlib import Path


def norm(v):
    return sum(x*x for x in v)


def blank(bits):
    return [1]+[0]*((1 << bits)-1)


def hadamard(v, bit):
    step = 1 << bit
    return [v[m]+v[m ^ step] if not m & step else v[m ^ step]-v[m]
            for m in range(len(v))]


def apply_j(v, site):
    bit = 1 << site
    return [v[m ^ bit] if m & bit else -v[m ^ bit] for m in range(len(v))]


def edge_q(v, i, j):
    return [-x for x in apply_j(apply_j(v, i), j)]


def edge_meter(v, i, j):
    """One clean control: H, controlled -J_i then controlled J_j, H; read it."""
    bit = len(v)
    tagged = hadamard(v+[0]*bit, bit.bit_length()-1)
    for site, scalar in ((i, -1), (j, 1)):
        tagged[bit:] = [scalar*x for x in apply_j(tagged[bit:], site)]
    out = hadamard(tagged, bit.bit_length()-1)
    plus, minus = out[:bit], out[bit:]
    qv = edge_q(v, i, j)
    assert plus == [a+b for a,b in zip(v,qv)]
    assert minus == [a-b for a,b in zip(v,qv)]
    assert norm(plus)+norm(minus)==4*norm(v)
    return plus, minus


def signs(outcomes):
    orientation = [1]
    for q in outcomes:
        orientation.append(orientation[-1]*q)
    return orientation


def correct(v, orientation):
    mask = sum(1 << i for i,s in enumerate(orientation) if s<0)
    return [x*(-1)**((m & mask).bit_count()%2) for m,x in enumerate(v)]


def attach(v, i, j):
    """Fresh j at |0>. One contact gate (controlled -J_i)(I x H_j)."""
    assert all(not x for m,x in enumerate(v) if m >> j & 1)
    v = hadamard(v,j)
    moved = apply_j(v,i)
    return [-moved[m] if m >> j & 1 else x for m,x in enumerate(v)]


def code(n):
    # Even/odd coefficients of the product (|0>+i|1>)^tensor n.
    pattern = (1,0,-1,0)
    e0 = [pattern[m.bit_count()%4] for m in range(1 << n)]
    e1 = [pattern[(m.bit_count()-1)%4] for m in range(1 << n)]
    assert norm(e0)==norm(e1)==1 << (n-1)
    assert sum(a*b for a,b in zip(e0,e1))==0
    assert all(apply_j(e0,i)==e1 and apply_j(e1,i)==[-x for x in e0] for i in range(n))
    return e0,e1


def grow(n):
    root = (n-1)//2
    left = root
    right = root
    rounds = []
    v = blank(n)
    while left>0 or right+1<n:
        # Both ends can spread simultaneously once there are two different ends.
        edges = []
        if right+1<n:
            edges.append((right,right+1))
        if left>0 and (left!=right or not edges):
            edges.append((left,left-1))
        assert len({i for edge in edges for i in edge})==2*len(edges)
        for i,j in edges:
            assert abs(i-j)==1
            v = attach(v,i,j)
        rounds.append(edges)
        left = min([left]+[j for _,j in edges])
        right = max([right]+[j for _,j in edges])
    e0,_ = code(n)
    assert v==e0 and len(rounds)==(n//2+(n%2) if n>1 else 0)
    return dict(sites=n,disjoint_contact_layers=rounds,depth=len(rounds),
                code_norm_chosen_denominator=norm(v),max_unconditioned_endpoint_overlap_before_contact="1/2")


def syndrome_branches(n):
    states = {():blank(n)}
    for i in range(n-1):
        new = {}
        for history,v in states.items():
            for sign,raw in zip((1,-1),edge_meter(v,i,i+1)):
                new[history+(sign,)] = raw
        states = new
    return states


def port_probability(v, bit, value):
    return Fraction(sum(x*x for m,x in enumerate(v) if (m>>bit & 1)==value),norm(v))


def move_data(v, i, j):
    assert j==i+1
    mask = (1<<i)|(1<<j)
    return [v[m ^ mask] if ((m>>i)^(m>>j))&1 else v[m] for m in range(len(v))]


def s_gate(v, data, plane, sign):
    jv = apply_j(v,plane)
    return [sign*jv[m] if m>>data & 1 else x for m,x in enumerate(v)]


def travelling(n, planes):
    v = planes + [0]*(len(planes)*((1<<n)-1))
    v = s_gate(hadamard(v,n),n,0,1)
    for i in range(n,2*n-1):
        v = move_data(v,i,i+1)
    v = hadamard(s_gate(v,2*n-1,n-1,-1),2*n-1)
    return port_probability(v,2*n-1,0)


def joint_y(planes):
    # Prepare a real Bell state by H and a neighboring data CNOT.
    v = hadamard(planes+[0]*(3*len(planes)),2)
    v = [v[m ^ 8] if m & 4 else v[m] for m in range(len(v))]
    for i in (0,1):
        v = hadamard(s_gate(v,2+i,i,-1),2+i)
    return [Fraction(sum(x*x for m,x in enumerate(v) if m>>2==k),norm(v)) for k in range(4)]


def bell_y():
    plus = [Fraction(0),Fraction(1,2),Fraction(1,2),Fraction(0)]
    minus = [plus[1],plus[0],plus[3],plus[2]]
    uniform = [Fraction(1,4)]*4
    assert joint_y(blank(2))==uniform
    rows = []
    for (s,),v in syndrome_branches(2).items():
        unfixed, fixed = joint_y(v),joint_y(correct(v,[1,s]))
        assert unfixed==(plus if s==1 else minus) and fixed==plus
        rows.append(dict(syndrome=s,weight='1/2',uncorrected=list(map(str,unfixed)),
                         corrected=list(map(str,fixed))))
    return dict(source='H and nearest-neighbor CNOT on real 00, followed by two local Y measurements',
                order=['++','-+','+-','--'],unmeasured_blanks=list(map(str,uniform)),
                syndrome_rows=rows)


def contacts(n):
    e0,_ = code(n)
    base_value = travelling(n,blank(n))
    assert base_value==Fraction(1,2)
    complete = []
    before = after = Fraction(0)
    for hist,v in syndrome_branches(n).items():
        weight = Fraction(norm(v),4**(n-1))
        assert weight==Fraction(1,1<<(n-1))
        orientations = signs(hist)
        fixed = correct(v,orientations)
        assert fixed==e0
        cycle = edge_meter(v,0,n-1)  # closing contact only on the optional ring
        assert norm(cycle[0 if orientations[-1]<0 else 1])==0
        raw, aligned = travelling(n,v), travelling(n,fixed)
        assert raw==int(orientations[-1]>0) and aligned==1
        before += weight*raw
        after += weight*aligned
        complete.append(dict(edge_signs=hist,relative_vertex_signs=orientations,
                             weight=str(weight),unfixed_zero=str(raw),corrected_zero=str(aligned),
                             optional_ring_closure_edge=orientations[-1]))
    assert sum(Fraction(row['weight']) for row in complete)==1 and before==base_value and after==1
    return dict(sites=n,unmeasured_blank_zero=str(base_value),uncorrected_zero=str(before),
                corrected_zero=str(after),postselect_all_plus_yield=str(Fraction(1,1<<(n-1))),
                all_branches=complete)


def ordering():
    # Two initially independent real sites each use its OWN blank to prepare +Y.
    n = 2
    v = blank(2*n)
    for i in range(n):
        v = s_gate(hadamard(v,n+i),n+i,i,1)
    conditional = []
    for s,branch in zip((1,-1),edge_meter(v,0,1)):
        p = Fraction(norm(branch),4*norm(v))
        out = correct(branch,[1,s])
        for i in range(n):
            out = hadamard(s_gate(out,n+i,i,-1),n+i)
        counts = [Fraction(sum(x*x for m,x in enumerate(out) if m>>n==k),norm(out))
                  for k in range(4)]
        assert p==Fraction(1,2) and counts[0 if s==1 else 2]==1
        conditional.append(dict(syndrome=s,weight=str(p),corrected_then_held_Y_read=list(map(str,counts))))
    early = []
    for (s,),branch in syndrome_branches(2).items():
        corrected = correct(branch,[1,s])
        v = corrected+[0]*(3*len(corrected))
        for i in range(n):
            v = s_gate(hadamard(v,n+i),n+i,i,1)
        for i in range(n):
            v = hadamard(s_gate(v,n+i,i,-1),n+i)
        early.append([Fraction(sum(x*x for m,x in enumerate(v) if m>>n==k),norm(v)) for k in range(4)])
    assert early[0]==early[1]==[1,0,0,0]
    late = [sum(Fraction(row['corrected_then_held_Y_read'][i])*Fraction(row['weight'])
                for row in conditional) for i in range(4)]
    return dict(columns_little_endian=['++','-+','+-','--'],late_alignment=conditional,
                late_unconditional=list(map(str,late)),align_before_program=list(map(str,early[0])))


def lifted(v, n, acting, mat, plane):
    """Literal real plane action of each matrix numerator A+iB."""
    out = [0]*len(v)
    mask = sum(1 << (n+j) for j in acting)
    offsets = [sum(((label>>q)&1) << (n+j) for q,j in enumerate(acting)) for label in range(len(mat))]
    for m,w in enumerate(v):
        if not w:
            continue
        column = sum(((m>>(n+j)) & 1) << q for q,j in enumerate(acting))
        for offset,row in zip(offsets,mat):
            z = row[column]
            target = (m & ~mask)|offset
            out[target] += int(z.real)*w
            out[target^(1<<plane)] += (-1 if m>>plane & 1 else 1)*int(z.imag)*w
    return out


def complex_step(v, acting, mat):
    # Separate reference: contract output rows with each input-mode column.
    result = []
    for m in range(len(v)):
        row = sum((m>>site & 1) << q for q,site in enumerate(acting))
        total = 0j
        for i,z in enumerate(mat[row]):
            j = m
            for k,site in enumerate(acting):
                j = (j & ~(1<<site))|((i>>k & 1)<<site)
            total += z*v[j]
        result.append(total)
    return result


def encode(v,n):
    e0,e1 = code(n)
    return [int(z.real)*a+int(z.imag)*b for z in v for a,b in zip(e0,e1)]


def circuit():
    n = 3
    # Gaussian-integer numerators; H, rational chiral phase and 3/5 damping.
    H = [[1,1],[1,-1]]
    R = [[5,0],[0,3+4j]]
    S = [[1,0],[0,1j]]
    CX = [[1,0,0,0],[0,0,0,1],[0,0,1,0],[0,1,0,0]]
    K0 = [[5,0],[0,3]]
    K1 = [[0,4],[0,0]]
    gates = [([0],H),([0,1],CX),([1],R),([1,2],CX),([0],S)]

    def apply(pair,sites,matrix):
        data,phys = pair
        data = complex_step(data,sites,matrix)
        outs = [lifted(phys,n,sites,matrix,plane) for plane in sites]
        assert all(u==encode(data,n) for u in outs)
        return data,outs[0]

    pair = (blank(n),encode(blank(n),n))
    for sites,matrix in gates:
        pair = apply(pair,sites,matrix)
    records = []
    before = norm(pair[1])
    for bit,measurement in enumerate((K0,K1)):
        data,phys = apply(pair,[1],measurement)
        prior = Fraction(norm(phys),25*before)
        if bit:
            data,phys = apply((data,phys),[2],S)
        for site in (0,1,2):
            data,phys = apply((data,phys),[site],H)
        squares = [int(z.real)**2 + int(z.imag)**2 for z in data]
        denom = norm(phys)
        joint = [prior*Fraction(sum(x*x for x in phys[k<<n:(k+1)<<n]),denom) for k in range(1<<n)]
        assert joint == [prior*Fraction(a,sum(squares)) for a in squares]
        records.append(dict(damping_record=bit,weight=str(prior),joint_data_records=list(map(str,joint))))
    assert sum(Fraction(x) for row in records for x in row['joint_data_records'])==1

    # A non-real input tests both encoding rails, independent of state preparation.
    arbitrary = [2-3j,-1+4j,5j,3,0,7-2j,-1j,2+1j]
    pair = arbitrary,encode(arbitrary,n)
    for sites,matrix in gates:
        pair = apply(pair,sites,matrix)
    return dict(sites=n,source_data='real localized 000; alternatively eight arbitrary Gaussian integer entries',
                operations=['H0','CX01','diag(1,(3+4i)/5)_1','CX12','S0',
                            'amplitude damping instrument on 1 with survival 3/5',
                            'conditional S2','H0 H1 H2','all base bits'],
                unused_choice_of_plane_on_each_two_site_gate_gives_same_state=True,
                every_branch_checked_against_independent_complex_update=True,all_records=records)


def main(directory):
    result = dict(
        representation='E(psi)=Re(psi) tensor e0 + Im(psi) tensor e1. e0,e1 are the normalized even-cosine and odd-sine coefficient vectors of the local product (|0>+i|1>)^n. Every J_i e0=e1, J_i e1=-e0. The signed local map A tensor I+B tensor J_i intertwines with A+iB for any matrix, including Kraus operators. Thus all joint sequential probabilities agree when the same encoded preparation and Born rule apply. Mixed states admit R(rho)/2 on the code.',
        measured_chains=[contacts(n) for n in range(2,6)],
        deterministic_growth=[grow(n) for n in range(1,12)],
        source_order=ordering(),bell_two_local_Y=bell_y(),complex_instrument=circuit(),
        depth='With two-site nearest-neighbor gates in disjoint matching layers, one input site can influence an interval of width at most 2d for d>=1 after d layers. Without a common input ancestor the end cones of an independent real product preparation factor, and each real one-point expectation of antisymmetric J vanishes. P(Q_end=+) is then 1/2, whereas the aligned code gives 1. Consequently ceil(n/2) contact layers are necessary for n>=2 on a chain and the paired center-out attachment achieves them. An attachment is one two-site orthogonal gate or a local H followed by a controlled signed permutation.',
        measured_cost='On a chain two edge colors suffice for local nondemolition syndrome acquisition if a disjoint-contact read is a layer. Site Z corrections need prefix parity relative to a shared root, propagated at the communication speed. Constant acquisition depth can instead herald the all-plus sector with weight 2^(1-n); identifying that global success still requires comparison. All contacts and corrections must precede protected data preparation unless frame conjugations of past data are independently handled.',
        scope='Distributed realification with physical signed quarter-turn control, neighboring real reversible contact circuits, clean meter, and Born/read/feedback. A held signed travelling-qubit comparator transports its data by nearest-neighbor SWAPs. Not an experiment or a derivation of Born weights; an acquired entangled reference changes the resource assumptions for strictly independent source networks. One cannot identify absolute complex conjugation from jointly transported preparations and reads.',
        prior_work=['https://doi.org/10.1103/PhysRevLett.102.020505','https://doi.org/10.1038/s41586-021-04160-4',
                    'Records_and_complex_structure.md, section on orientation of independent planes'])
    directory.mkdir(parents=True,exist_ok=True)
    (directory/'distributed_complex_walk.json').write_bytes((json.dumps(result,indent=2)+'\n').encode())


if __name__=='__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('output',type=Path)
    main(p.parse_args().output)
