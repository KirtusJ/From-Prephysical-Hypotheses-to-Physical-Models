"""Check a passive selector flip, a tagged-control failure and finite prefix errors."""

import argparse
import json
from fractions import Fraction as Q
from pathlib import Path


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def flag(x, selector, crossed):
    if x == "O":
        return 1
    if x == "N":
        return 0
    return selector ^ int(crossed and x == "C")


def write(amplitudes, crossed, keep_tag=False, selector=(1, 1)):
    """Sparse full column (spatial address, selector, F, old selector tag, environment)."""
    column = {}
    for (x, env), amplitude in amplitudes.items():
        for label, coefficient in enumerate(selector):
            column[x, label, flag(x, label, crossed), label if keep_tag else 0, env] = amplitude*coefficient
    return column


def flip(column):
    return {(x,l ^ int(x == "C"),f,tag,e):v for (x,l,f,tag,e),v in column.items()}


def distance(a, b):
    keys = a.keys() | b.keys()
    return Q(sum((a.get(key, 0)-b.get(key, 0))**2 for key in keys), sum(x*x for x in b.values()))


def contrast(rate, bits):
    lower, upper = Q(0), Q(1)
    rows = []
    for bit in bits:
        mid = (lower+upper)/2
        mids = rate(mid)
        residual = mids-(rate(lower)+rate(upper))/2
        rows.append([str(lower),str(upper),str(mids),str(residual)])
        lower,upper = (mid,upper) if bit == "1" else (lower,mid)
    return rows


def weighted_recurrence(bits, lower, upper, delta, carry):
    p = Q(int(bits,2),1 << len(bits))
    predicted = (1-p)*lower + p*upper
    weights = []
    for k,bit in enumerate(bits):
        mid = (lower+upper)/2+delta[k]
        remainder = bits[k+1:]
        z = Q(int(remainder,2),1 << len(remainder)) if remainder else Q(0)
        weight = 1-z if bit == "1" else z
        weights.append(weight)
        lower,upper = (mid+carry[k][0],upper+carry[k][1]) if bit == "1" else (lower+carry[k][0],mid+carry[k][1])
        predicted += weight*delta[k]+(1-z)*carry[k][0]+z*carry[k][1]
    require(predicted == lower, "weighted recurrence must reproduce final lower endpoint")
    return weights


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output",type=Path)
    dest=parser.parse_args().output
    # Both children of an H on one occupied port have identical amplitudes
    # on every environmental coordinate. Old spectator amplitudes may differ.
    amplitudes={("O",0):2,("O",1):-1,("N",0):1,("N",1):3,
                ("A",0):-2,("C",0):-2,("A",1):1,("C",1):1}
    norm=sum(x*x for x in amplitudes.values())
    child_norm=sum(v*v for (x,_),v in amplitudes.items() if x == "C")
    bare=write(amplitudes,False)
    crossed=write(amplitudes,True)
    require(flip(bare)==crossed and flip(flip(bare))==bare,"passive selector gate")
    # Swap the two children alone after a D-branch write; keep F and E fixed.
    def branch(l):
        return {(x,flag(x,l,True),env):v for (x,env),v in amplitudes.items()}
    complement_swap={("C" if x=="A" else "A" if x=="C" else x,f,env):v for (x,f,env),v in branch(0).items()}
    require(complement_swap == branch(1),"crossed standalone settings")
    tagged=distance(flip(write(amplitudes,False,True)),write(amplitudes,True,True))
    require(tagged==2*Q(child_norm,norm),"retained tag gives orthogonal branches on C")
    opposite=distance(flip(write(amplitudes,False,selector=(1,-1))),write(amplitudes,True,selector=(1,-1)))
    require(opposite==4*Q(child_norm,norm),"balanced magnitudes with wrong relative sign")
    # Even one occupied control cell suffices to invalidate the tagged swap.
    minimal={("C",0):1}
    require(distance(flip(write(minimal,False,True)),write(minimal,True,True))==2, "minimal lost-state witness")
    # A normalized squared response respects all dark/bright and child symmetries.
    def square(p):
        return p*p/(p*p+(1-p)*(1-p))
    rows=contrast(square,"1001")
    require(rows[1]==["1/2","1","9/10","3/20"],"second-depth adverse contrast")
    require(square(Q(9,16))==Q(81,130),"terminal adverse response")
    tested=0
    for t in range(1,10):
        for p in range(0,1<<t):
            bits=f"{p:0{t}b}"
            # Artificial signed residual inputs test the linear error identity;
            # the checker makes no sampling or independence assumption about them.
            delta=[Q(i%3-1,97) for i in range(t)]
            carry=[(Q((i+1)%4-1,157),Q(1-i%5,181)) for i in range(t)]
            weighted_recurrence(bits,Q(1,17),Q(13,14),delta,carry)
            tested+=1
    weights=weighted_recurrence("1001",Q(0),Q(1),[Q(0)]*4,[(Q(0),Q(0))]*4)
    require(weights==[Q(7,8),Q(1,4),Q(1,2),Q(1)],"suffix weights")
    payload=dict(ordered_basis="spatial carrier, selector L, pointer F, old L tag, spectator",
                 signed_amplitudes=[[x,e,v] for (x,e),v in amplitudes.items()],
                 complete_occupied_cells=len(bare),squared_normalization=2*norm,passive_flip_exact=True,
                 standalone_child_swap_exact=True,tagged_squared_difference=str(tagged),
                 balanced_wrong_phase_squared_difference=str(opposite),
                 sole_C_tagged_squared_difference="2",tested_error_recurrences=tested,
                 nine_of_sixteen=dict(digits="1001",rival_rows_lower_upper_read_residual=rows,
                                      rival_final="81/130",ordinary_final="9/16",
                                      difference="63/1040",local_residual_weights=list(map(str,weights))))
    dest.write_bytes((json.dumps(payload,indent=2)+"\n").encode())


if __name__=="__main__":
    main()
