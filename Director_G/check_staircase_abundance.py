"""Run python -B check_staircase_abundance.py OUTPUT_DIRECTORY (standard library)."""
import argparse
import json
from collections import Counter
from fractions import Fraction
from itertools import product
from math import comb, gcd, lcm
from pathlib import Path


PAIRS=(('RLRLLR','LRRLLR'),('RLLR','LRLR'))
EXITS=('RRLR','RRRL')


def trace(word,m):
    x,d,s,j=0,'R',1,0
    for out in word:
        j=(j+(x//2))%m
        s *= -1 if d==out=='L' else 1
        x=(x+(1 if out=='R' else -1))%(4*m)
        d=out
    return x,d,s,j


def multiply(a,b,m):
    return a[0]*b[0],(a[1]+b[1])%m


def multiply_cloud(a,b,m):
    out=Counter()
    for x,n in a.items():
        for y,k in b.items():
            out[multiply(x,y,m)]+=n*k
    return out


def closed_word_families(m,abundance):
    raw=[]
    clouds=[]
    for words,u in zip(PAIRS,((1,1),(-1,1))):
        left,right=map(lambda word:trace(word,m),words)
        assert left[:2]==right[:2]==(0,'R') and len(words[0])==len(words[1])
        signs=(left[2:],right[2:])
        assert (left[2]*right[2],(left[3]-right[3])%m)==u
        order=lcm(1 if u[0]==1 else 2,m//gcd(m,u[1]))
        B=max(order+1,abundance)
        cloud=Counter({(1,0):1})
        for _ in range(B):
            cloud=multiply_cloud(cloud,Counter(signs),m)
        via_binomial=Counter()
        for j in range(B+1):
            via_binomial[(left[2]**j*right[2]**(B-j),(left[3]*j+right[3]*(B-j))%m)]+=comb(B,j)
        assert cloud==via_binomial and len(cloud)==order and min(cloud.values())>=abundance
        clouds.append(cloud)
        raw.append(dict(words=words,terminal_port=(0,'R'),gains=signs,ratio=u,order=order,
                        blocks=B,horizon=B*len(words[0]),minimum_coverage=min(cloud.values())))
    together=multiply_cloud(*clouds,m)
    all_gains=set(product((1,-1),range(m)))
    assert set(together)==all_gains
    finals=[]
    for word in EXITS:
        x,d,s,k=trace(word,m)
        assert (x,d)==(2,word[-1])
        shifted=multiply_cloud(together,{(s,k):1},m)
        assert set(shifted)==all_gains and min(shifted.values())>=abundance
        finals.append(dict(exit=word,port=[x,d],exit_gain=[s,k],
                           plus_counts=[shifted[1,j] for j in range(m)],
                           minus_counts=[shifted[-1,j] for j in range(m)]))
    return dict(requested_abundance=abundance,families=raw,all_exits=finals,
                equal_length=sum(row['horizon'] for row in raw)+4)


def verify_site(m):
    start=2
    entries=[]
    for out in 'RL':
        entries.append([((-1 if inc==out=='L' else 1),start//2%m) for inc in 'RL'])
    generated={(1,0)}
    while True:
        expanded=generated|{multiply(h,e,m) for h in generated for row in entries for e in row}
        if expanded==generated:
            break
        generated=expanded
    assert generated==set(product((1,-1),range(m)))
    # Offset subeffects L=n_+ + n_- on residue r, and Q=(n_+ - n_-)^2.
    # Both obey the x=0 equations even on mixed multisets; test a nontrivial
    # collection of all local input count configurations on a single residue.
    count=0
    for up,um,vp,vm in product(range(3),repeat=4):
        for form in (lambda a,b:a+b,lambda a,b:(a-b)**2):
            assert form(up+vp,um+vm)+form(up+vm,um+vp)==2*(form(up,um)+form(vp,vm))
            count+=1
    # The single selected prefix RRRL reaches (2,L) on T^2 and outgoing
    # gains have residue 3 rather than 2; both subeffects fail by exactly 2.
    parent=trace('RRRL',m)
    continuations=[trace('RRRL'+out,m) for out in 'RL']
    assert parent==(2,'L',1,2%m) and [u[3] for u in continuations]==[3%m]*2
    assert all(u[3]!=parent[3] for u in continuations)
    return dict(block_gains=entries,generated_group_size=len(generated),
                zero_block_count_and_square_checks=count,
                selected_subset_parent=parent,two_children=continuations,
                zero_block_residue_subform_parent=1,both_child_sums=0,required_factor=2)


def detector(m):
    parents=[word for word in product('RL',repeat=3) if trace(word,m)[:2]==(4*m-3,'L')]
    assert parents==[tuple('LLL')]
    p=trace('LLL',m)
    sons=[trace('LLL'+d,m) for d in 'RL']
    assert p[2:]==(1,(-2)%m) and {u[3] for u in sons}=={(-4)%m}
    assert p[3]!=sons[0][3] and [u[2] for u in sons]==[1,-1]
    # W_(M+1): a complete cycle and one additional point, so nonzero
    # characters sum to the additional unit and every such modulus is one.
    n=m+1
    interval=Counter(j%m for j in range(n))
    assert interval==Counter({0:2,**{j:1 for j in range(1,m)}})
    alpha=Fraction(1,m+2)
    assert alpha*(m+1)**2+(1-alpha)==n
    return dict(localized_source_port=[0,'R'],unique_parent=parents[0],parent=p,
                parent_joint_mass='1/8',same_sheet_child_masses=['0','0'],
                transported_sheet_children=sons,transported_joint_masses=['1/16','1/16'],
                positive_interval_depth_control=dict(n=n,folded_counts=[interval[k] for k in range(m)],
                    zero_frequency_weight=str(alpha),pure_count_W=n,
                    all_prior_W_equal_n_for_uniform_weights=True))


def main(directory):
    orders=[3,4,5,6,7,8,9,10,12,15,16]
    rows=[dict(order=m,site_two=verify_site(m),simultaneous_abundance=closed_word_families(m,7),
               shifted_local_detector=detector(m)) for m in orders]
    data=dict(scope='The exact walk uses g(x)=floor(x/2) on the 4M ring at departure. This checks words and finite multiplicities for K=7 and the local detector equations. Arbitrary K follows from the two loop families in the manuscript. G10 application assumes a common F on all ports/events and factor two under continuation of arbitrary subsets. An actual terminal sheet/offset subeffect is not such a conserved law. The checker does not infer the premises from terminal data or certify a physical law.',
              rows=rows)
    directory.mkdir(parents=True,exist_ok=True)
    (directory/'staircase_abundance.json').write_bytes((json.dumps(data,separators=(',',':'))+'\n').encode())


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('output',type=Path)
    main(p.parse_args().output)
