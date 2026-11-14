"""Run python -B check_gauss_string.py OUTPUT_DIRECTORY (standard library).

Exact open-line occupation/link coordinates. A vector is a sparse dictionary of
Gaussian-integer numerators; all branches at the same step use one denominator.
"""
import argparse
import json
from fractions import Fraction as F
from itertools import combinations
from math import gcd
from pathlib import Path


TILTS = ((3,4),(4,3))
FIELDS = {'idle':(1,0,1),'quarter':(0,1,1),'minus_quarter':(0,-1,1),
          'half':(-1,0,1),'rational':(3,4,5)}


def add(z,v):
    return z[0]+v[0],z[1]+v[1]


def scale(z,k):
    return z[0]*k,z[1]*k


def mult(z,w):
    return z[0]*w[0]-z[1]*w[1],z[0]*w[1]+z[1]*w[0]


def energy(state):
    return sum(x*x+y*y for x,y in state.values())


def deposit(out,k,val):
    out[k]=add(out.get(k,(0,0)),val)


def clean(out):
    return {k:v for k,v in out.items() if v!=(0,0)}


def charge_set(mask,n):
    return [j for j in range(n) if mask & (1<<j)]


def flux(mask,n):
    left=links=0
    for j in range(n-1):
        left ^= (mask>>j)&1
        links |= left<<j
    assert mask.bit_count()%2==0
    return links


def defect(mask,links):
    return mask^links^(links<<1)


def bond(state,j,c,s,contact):
    out = {}
    for (m,e),z in state.items():
        occ = (m>>j)&3
        if occ in (0,3):
            deposit(out,(m,e),scale(z,5*(contact if occ==3 else 1)))
        else:
            deposit(out,(m,e),scale(z,c))
            deposit(out,(m^(3<<j),e^(1<<j)),scale(z,s if occ==1 else -s))
    return clean(out)


def single_link_kicks(state,n,w):
    x,y,b=w
    for j in range(n-1):
        state = {key:mult(z,(x,y)) if key[1]>>j&1 else scale(z,b)
                 for key,z in state.items()}
    return state,b**(n-1)


def physical(state,n,half,w,contact=1,back=False):
    c,s=TILTS[half%2]
    den=1
    if back:
        state,den=single_link_kicks(state,n,(w[0],-w[1],w[2]))
        s=-s
    for j in range(half%2,n-1,2):
        state=bond(state,j,c,s,contact)
        den*=5
    if not back:
        state,k=single_link_kicks(state,n,w)
        den*=k
    return state,den


def wedge_layer(state,n,half,w):
    """Independent exterior square of the whole one-body layer, then string potential."""
    V=[[int(i==j)*5 for j in range(n)] for i in range(n)]
    c,s=TILTS[half%2]
    for j in range(half%2,n-1,2):
        V[j][j],V[j+1][j+1]=c,c
        V[j][j+1],V[j+1][j]=-s,s
    out={}
    for p,q in combinations(range(n),2):
        string=(1<<q)-(1<<p)
        factor=(1,0)
        for _ in range(q-p):
            factor=mult(factor,w[:2])
        factor=scale(factor,w[2]**(n-1-(q-p)))
        z=(0,0)
        for (m,e),v in state.items():
            i,j=charge_set(m,n)
            assert e==flux(m,n)
            z=add(z,scale(v,V[p][i]*V[q][j]-V[p][j]*V[q][i]))
        if z!=(0,0):
            out[(1<<p)|(1<<q),string]=mult(z,factor)
    return out,25*w[2]**(n-1)


def equal(a,da,b,db):
    return a.keys()==b.keys() and all(scale(a[k],db)==scale(b[k],da) for k in a)


def raw_rows(state,n,norm2):
    rows=[]
    for (m,e),(a,b) in sorted(state.items()):
        rows.append([m,e,a,b,str(F(a*a+b*b,norm2))])
    return rows


def rationalize(state,den):
    d=den
    for a,b in state.values():
        d=gcd(d,gcd(a,b))
    return {k:(a//d,b//d) for k,(a,b) in state.items()},den//d


def launch(n,p,q,background=0):
    m=1<<p|1<<q
    return {(m,flux(m,n)^background):(1,0)}


def signed_permute_pair(key,bond_id):
    m,e=key
    if ((m>>bond_id)&3) in (0,3):
        return m^(3<<bond_id),e^(1<<bond_id)
    return key


def swap_dressed(key,bond_id):
    m,e=key
    if ((m>>bond_id)&3) in (1,2):
        return m^(3<<bond_id),e^(1<<bond_id)
    return key


def run(n,state,steps,w,contact=1,schedule='layers'):
    ref=state.copy()
    den=rd=1
    base=energy(state)
    defects={defect(m,e) for m,e in state}
    rows=[]
    for t in range(steps+1):
        assert defects=={defect(m,e) for m,e in state}
        assert energy(state)==den**2*base
        if defects=={0} and contact==1:
            assert equal(state,den,ref,rd)
        rows.append(dict(half_layers=t,amplitude_denominator=den,
                         bins=raw_rows(state,n,den**2*base)))
        if t==steps:
            break
        field=w if schedule=='layers' or t%2==1 else FIELDS['idle']
        nxt,d=physical(state,n,t,field,contact)
        inv,e=physical(nxt,n,t,field,contact,True)
        assert equal(inv,d*e,state,1)
        state,den=rationalize(nxt,den*d)
        if defects=={0} and contact==1:
            nxt,d=wedge_layer(ref,n,t,field)
            ref,rd=rationalize(nxt,rd*d)
    return rows


def scan():
    counts=[]
    for n in (4,5,6,7,8):
        for schedule in ('layers','cycles'):
            changed=[0]*5
            adjacent=[0]*5
            for p,q in combinations(range(n),2):
                v=launch(n,p,q)
                left=run(n,v,4,FIELDS['idle'],schedule=schedule)
                right=run(n,v,4,FIELDS['quarter'],schedule=schedule)
                for t in range(5):
                    a={i[0]:F(i[-1]) for i in left[t]['bins']}
                    b={i[0]:F(i[-1]) for i in right[t]['bins']}
                    changed[t]+=a!=b
                    adjacent[t]+=int(a!=b and q==p+1)
            assert changed[:3]==[0,0,0] and any(changed)
            counts.append(dict(sites=n,kicks=schedule,all_launches=n*(n-1)//2,
                               different_raw_matter_distributions=changed,adjacent_different=adjacent))
    return counts


def gauge_read():
    # A single dressed bond interferometer, from two adjacent charge placements.
    n=4
    logs=[]
    for sign in (1,-1):
        v={**launch(n,0,2),**{k:(sign,0) for k in launch(n,1,2)}}
        assert len({e for _,e in v})==2
        full=bond(v,0,3,4,1)
        target=(5,3)
        coherent=F(sum(z*z for z in full[target]),energy(full))
        flagged={flag:{key:z for key,z in v.items() if key[1]&1==flag} for flag in (0,1)}
        keep=[]
        for flag,arm in flagged.items():
            assert all((e&1)==flag for _,e in arm)
            after=bond(arm,0,3,4,1)
            keep.append(dict(electric_bit=flag,initial_joint_mass=str(F(energy(arm),energy(v))),
                             after_dressed_analyzer=raw_rows(after,n,50)))
        washed=sum(F(r[-1]) for block in keep for r in block['after_dressed_analyzer'] if r[0]==5)
        # Copy E_0 by CNOT into blank. A second CNOT before the analyzer resets
        # every pointer to zero exactly; retaining the copy gives the blocks above.
        copy={(m,e,e&1):z for (m,e),z in v.items()}
        reset={(m,e,b^(e&1)):z for (m,e,b),z in copy.items()}
        assert reset=={(m,e,0):z for (m,e),z in v.items()}
        assert washed==F(1,2) and coherent==(F(1,50) if sign==1 else F(49,50))
        logs.append(dict(relative_sign=sign,dressed_analyzer_return=str(coherent),
                         after_unread_copy_or_partial_trace=str(washed),
                         entire_unmeasured_dressed_read=raw_rows(full,n,50),
                         copied_flag_joint_blocks=keep,reversed_copy_return=str(coherent)))
    return logs


def preparation(n,p,q):
    # Explicit gauge-preserving neutral-pair source: interchange 00 and 11
    # on p,p+1 and toggle their link. Acts identically on single occupations.
    keys=[(0,0)]
    m,e=signed_permute_pair(keys[0],p)
    keys.append((m,e))
    for j in range(p+1,q):
        assert (m>>j)&3==1
        m,e=swap_dressed((m,e),j)
        keys.append((m,e))
    assert all(defect(a,b)==0 for a,b in keys) and (m,e)==next(iter(launch(n,p,q)))
    backwards=[keys[-1]]
    for j in reversed(range(p+1,q)):
        backwards.append(swap_dressed(backwards[-1],j))
    backwards.append(signed_permute_pair(backwards[-1],p))
    assert backwards==list(reversed(keys))
    return dict(sites=n,start=[p,p+1],final=[p,q],forward_port_keys=keys,
                reverse_dressed_swaps_then_pair_annihilation=list(reversed(keys)),
                occupied_link_strokes=q-p,needs_local_non_number_preserving_pair_source=True)


def disjoint_packets():
    n,p=8,3
    # Two disjoint Givens sweeps fan the adjacent charges outwards. The chosen
    # rotations implement a geometric envelope with equal local denominators.
    seed=launch(n,p,p+1)
    v=seed
    left_bonds=[2,1]
    right_bonds=[4,5]
    for l,r in zip(left_bonds,right_bonds):
        v=bond(bond(v,l,3,-4,1),r,3,4,1)
    v,den=rationalize(v,5**4)
    left={3:15,2:12,1:16}
    right={4:15,5:12,6:16}
    desired={}
    for l,lval in left.items():
        for r,rval in right.items():
            key=next(iter(launch(n,l,r)))
            desired[key]=(lval*rval,0)
    assert equal(v,den,desired,625)
    recovered=v
    for l,r in reversed(list(zip(left_bonds,right_bonds))):
        recovered=bond(bond(recovered,r,3,-4,1),l,3,4,1)
    assert equal(recovered,den*5**4,seed,1)
    return dict(sites=n,local_vacuum_pair_creation_bond=p,parallel_givens_layers=list(zip(left_bonds,right_bonds)),
                single_packet_amplitudes_from_inner_to_outer=['3/5','12/25','16/25'],
                number_of_nonzero_joint_ports=len(v),amplitude_denominator=den,
                complete_dressed_state=raw_rows(v,n,den**2),inverse_sweep_restores_seed=True,
                general_cost='For disjoint intervals of lengths L and R, a real normalized target vector can be synthesized by successive adjacent Givens rotations splitting its specified coefficient from the remaining tail norm. Requires L+R-2 addressed rotations with depth max(L-1,R-1) when both sweeps run simultaneously; arbitrary precise local angles must be supplied. The example uses fixed rational angles; an empty packet coordinate is handled by angle 0 or pi/2.')


def background_and_clock():
    n=6
    schedules=[]
    for clock in ('layers','cycles'):
        for w in ('idle','quarter'):
            timeline=run(n,launch(n,1,2),4,FIELDS[w],schedule=clock)
            schedules.append(dict(kick_schedule=clock,field=w,from_adjacent_pair=timeline))
    # All links initially flipped into the sector with static boundary defects:
    # its weight (n-1)-length reverses the separation phase slope.
    background=(1<<(n-1))-1
    phys=run(n,launch(n,1,2,background),4,FIELDS['quarter'],schedule='cycles')
    ref=run(n,launch(n,1,2),4,FIELDS['minus_quarter'],schedule='cycles')
    rows=[]
    for t,(d,c) in enumerate(zip(phys,ref)):
        common_phase=(1,0)
        for _ in range(t//2*(n-1)):
            common_phase=mult(common_phase,(0,1))
        transformed={(m,e^background):mult((a,b),common_phase) for m,e,a,b,_ in c['bins']}
        literal={(m,e):(a,b) for m,e,a,b,_ in d['bins']}
        assert equal(literal,d['amplitude_denominator'],transformed,c['amplitude_denominator'])
        rows.append(dict(t=t,common_phase=common_phase,checked_bins=len(literal)))
    m,e=next(iter(launch(n,1,2,background)))
    weights=[(flux(1<<1|1<<q,n)^background).bit_count() for q in range(2,n)]
    assert weights==[4,3,2,1]
    return dict(adjacent_comparison=schedules,full_background_defects=charge_set(defect(m,e),n),
                fixed_left_endpoint_1_right_endpoints_2_to_5_link_weights=weights,
                reverse_slope_amplitude_identity=rows,
                physical_full_background_timeline=phys)


def vacuum_controls():
    n=6
    rows=[]
    for label,e in (('vacuum',0),('all_links_inverted',31),('localized_defect_pair',4)):
        state={(0,e):(1,0)}
        phases=[]
        for t in range(4):
            state,den=physical(state,n,t,FIELDS['quarter'])
            state,den=rationalize(state,den)
            assert den==1 and len(state)==1 and energy(state)==1 and (0,e) in state
            phases.append(list(state[0,e]))
        rows.append(dict(case=label,charge_mask=0,link_mask=e,defects=charge_set(defect(0,e),n),
                         state_after_each_kicked_layer=phases))
    return rows


def causal():
    n=8
    v=launch(n,1,4)
    u=launch(n,1,6)
    (m,e),(mm,ee)=next(iter(v)),next(iter(u))
    diff={('n',j) for j in range(n) if (m^mm)>>j&1}
    diff|={('E',j) for j in range(n-1) if (e^ee)>>j&1}
    runs=[run(n,s,8,FIELDS['quarter']) for s in (v,u)]
    out=[]
    for t in range(9):
        cone={('n',0)}
        for h in reversed(range(t)):
            for j in range(h%2,n-1,2):
                sites={('n',j),('E',j),('n',j+1)}
                if cone&sites:
                    cone|=sites
        vals=[sum(F(row[-1]) for row in run0[t]['bins'] if row[0]&1) for run0 in runs]
        if not cone&diff:
            assert vals[0]==vals[1]
        out.append(dict(half_layers=t,initial_differences_in_receiver_cone=sorted(cone&diff),
                        charge_at_site_zero=list(map(str,vals)),TV=str(abs(vals[0]-vals[1]))))
    return dict(changed_input_coordinates=sorted(diff),records=out)


def main(directory):
    tests=[
        ('four_sites',4,0,2,0,4,'idle',1),('four_sites',4,0,2,0,4,'quarter',1),
        ('quarter_conjugate',4,0,2,0,4,'minus_quarter',1),
        ('adjacent_pair',6,1,2,0,4,'idle',1),('adjacent_pair',6,1,2,0,4,'quarter',1),
        ('same_cell',6,2,3,0,5,'quarter',1),('rational_field',6,1,4,0,4,'rational',1),
        ('alternate_contact',6,1,2,0,4,'quarter',-1),
        ('bare_separated_no_flux',6,1,4,14,4,'quarter',1),
        ('static_external_defects',6,1,4,1,4,'quarter',1),
        ('zero_field',6,1,4,0,4,'idle',1),('half_turn',6,1,4,0,4,'half',1)]
    trials=[]
    for label,n,p,q,bg,t,f,g in tests:
        initial=launch(n,p,q,bg)
        m,e=next(iter(initial))
        trials.append(dict(case=label,sites=n,field=f,contact=g,initial_charges=[p,q],
                           initial_defect_mask=defect(m,e),timeline=run(n,initial,t,FIELDS[f],g)))
    bare=trials[8]
    assert bare['timeline'][0]['bins'][0][1]==0 and bare['initial_defect_mask']!=0
    assert [sorted((row[0],row[-1]) for row in t['bins']) for t in trials[1]['timeline']]==[
        sorted((row[0],row[-1]) for row in t['bins']) for t in trials[2]['timeline']]
    data=dict(convention='Sites 0..N-1, open line segment with exterior flux zero. E_j is a bit on edge j,j+1. Every half-layer acts on the even or odd disjoint bonds with real one-occupant rotations [[3,-4],[4,3]]/5 and [[4,-3],[3,4]]/5. A hop toggles its own link. Vacuum has amplitude 1; double occupancy has amplitude 1 unless marked as an alternate contact. Each explicit physical kick is the product of one-link diagonal phases w^E. The main schedule kicks every half-layer. The additional cycles scan kicks after odd half-layers only.',
        theorem='The binary defect mask m xor E xor (E<<1) is invariant under a hop and its link toggle and under all local diagonal kicks. In the neutral sector with exterior E=0, every even occupation m fixes E uniquely by prefix parity. For exactly two occupied sites p<q its string is p<=j<q, and sum E=q-p. Restriction by the basis isometry |m> -> |m,flux(m)> gives the exterior-square half-layer followed by w^(q-p). Two occupied sublattices of one coarse cell still have one occupied link, and a blocked bond is stationary. A background E xor flux(m) is static and changes the potential to its Hamming weight. This is an external choice of local dynamics with Gauss constraint, coherent dressed preparation and Born readout, not a derivation of a force on independently set bare particle coordinates.',
        output_encoding='Each reported [charge_mask,link_mask,integer_real,integer_imaginary,probability] gives the entire coordinate amplitude divided by the enclosing amplitude_denominator for normalized localized launches. Absent bins vanish. Distinct flux strings orthogonalize different matter configurations under a bare link partial trace. The projected effective amplitudes instead belong to the dressed configuration basis; retaining links permits a gauge-invariant hop analyzer to recombine them. Each snapshot is a possible terminal read on its own realization.',
        examples=trials,all_launch_short_time_scan=scan(),dressed_vs_dephased=gauge_read(),
        constructive_source=preparation(7,1,5),separated_packet_source=disjoint_packets(),
        local_causality=causal(),clock_and_background_controls=background_and_clock(),
        empty_occupation_controls=vacuum_controls())
    directory.mkdir(parents=True,exist_ok=True)
    (directory/'gauss_string.json').write_bytes((json.dumps(data,separators=(',',':'))+'\n').encode())


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('output',type=Path)
    main(p.parse_args().output)
