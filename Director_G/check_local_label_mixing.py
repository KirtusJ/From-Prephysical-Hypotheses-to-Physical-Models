"""Enumerate signed forward paths with one branch bit and three protected routing bits."""
import argparse
from collections import defaultdict
from fractions import Fraction as Q
import json
from pathlib import Path


def check(value, name):
    if not value:
        raise ValueError(name)


def split_labels(bits):
    labels=[0]
    for j in range(bits):
        labels += [i+(1<<j) for i in labels]
    return labels


def make_state():
    # Label and destination sectors are both prepared by Hadamards on blank bits.
    # All 16 numerators share the denominator 4 before the late operation.
    state={}
    for a in split_labels(3):
        for label in split_labels(1):
            if a<2:
                directions="RRLLLL"
            elif a<4:
                directions="RRRLLL"
            elif a<7:
                directions="RRRRRL"
            else:
                directions="RRRRRR"
            x,rail=0,"R"
            incoming="R"+directions[:-1]
            for desired,scheduled_in in zip(directions,incoming):
                # The preprogrammed permutation applies to both input rails.
                if desired!=scheduled_in:
                    rail = "L" if rail=="R" else "R"
                x += 1 if rail=="R" else -1
            state[x,rail,a,label]=-1 if x==0 and label==1 else 1
    return state


def table(mix, drift=False):
    state=make_state()
    masses=defaultdict(int)
    for x,rail,a,label in state:
        pair=[state[x,rail,a,j] for j in (0,1)]
        if mix and x in (-2,0):
            num=pair[0]+(1-2*label)*pair[1]
            mass=num*num
        else:
            mass=2*pair[label]**2
        if drift and label==1 and x==4:
            mass=0
        masses[label,x]+=mass
    return [[Q(masses[l,x],2) for x in (-2,0,4,6)] for l in (0,1)]


def site_power(masses,q):
    weights=[v**q if v else 0 for v in masses]
    return [w/sum(weights) for w in weights]


def rates(t,q,w):
    cond=[site_power(row,q) for row in t]
    return [w*x+(1-w)*y for x,y in zip(*cond)]


def main():
    arg=argparse.ArgumentParser(description=__doc__)
    arg.add_argument("output",type=Path)
    path=arg.parse_args().output
    idle,mixed=table(False),table(True)
    check(idle==[[2,2,3,1]]*2 and mixed==[[4,0,3,1],[0,4,3,1]],"physical table")
    check([sum(r) for r in idle+mixed]==[8]*4,"branch norms")
    before,after=[[sum(v) for v in zip(*p)] for p in (idle,mixed)]
    check(before==after==[4,4,6,2],"all global populations")
    rows=[]
    for q in (0,1,2,3,6,15,50):
        # q=0 denotes the right limit on occupied supports. For integers use
        # exact arithmetic, retaining opposite label biases on the two settings.
        r=rates(idle,q,Q(1))
        s=rates(mixed,q,Q(0))
        d=[a-b for a,b in zip(r,s)]
        witness=d[2]-3*d[3]
        check(witness>=0 and (witness==0)==(q==1),"signed witness")
        for w in (Q(0),Q(1,3),Q(1,2),Q(1)):
            check(rates(idle,q,w)[2:]==r[2:] and rates(mixed,q,w)[2:]==s[2:],
                  "arbitrary branch weights")
        if q==0:check(witness==Q(1,6),"zero boundary")
        if q==2:check(witness==Q(4,39),"square witness")
        rows.append(dict(q=q,bare_monitors=r[2:],mixed_monitors=s[2:],witness=witness))
    # At the unaltered control (never mix), even a fourth-power detector passes.
    q=2
    wrong=table(True,drift=True)
    check(rates(wrong,q,Q(1))[2:]!=rates(wrong,q,Q(0))[2:],"asymmetric monitor makes priors matter")
    # Fully refined (route,label) tags have just one occupied site each.
    # If one chooses a label kinematically and powers *there*, the result
    # is the normalized aggregate at every exponent, on every input row here.
    groups=[-2,-2,0,0,4,4,4,6]
    refined=[Q(groups.count(x),len(groups)) for x in (-2,0,4,6)]
    check(refined==[x/sum(before) for x in before],"finer normalization boundary")
    with path.open("x",encoding="utf8",newline="\n") as out:
        json.dump(dict(site_order=[-2,0,4,6],idle=idle,mixed=mixed,
                       global_site_numerators=before,integer_powers=rows,
                       asymmetrically_modified_label_rows=wrong,route_label_evasion=refined),
                  out,indent=2,default=str)
        out.write("\n")


if __name__=="__main__":
    main()
