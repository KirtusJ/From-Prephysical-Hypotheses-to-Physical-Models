"""Native parity and prime reads, finite certificates and classical controls.

Run python -B check_prime_port_records.py NEW_DIRECTORY. No packages needed.
"""
import argparse
import json
from collections import Counter
from fractions import Fraction
from itertools import product
from math import ceil, cos, gcd, lcm, pi
from pathlib import Path


def require(ok, message):
    if not ok:
        raise ValueError(message)


def histories(m,t,site,rail):
    rows=[]
    for letters in product("RL",repeat=t):
        x,c,g,s=0,"R",0,1
        for h in letters:
            g=(g+x//2)%m
            s*= -1 if c==h=="L" else 1
            c=h
            x=(x+(1 if c=="R" else -1))%(4*m)
        if (x,c)==(site%(4*m),rail):
            rows.append(["".join(letters),g,s])
    return rows


def lag_coefficients(rows,m):
    """Polynomials in folded cosine lags; every ordered pair is included."""
    coeff=Counter()
    for _,g,s in rows:
        for _,h,j in rows:
            u=(g-h)%m
            coeff[min(u,(-u)%m)]+=s*j
    return {i:v for i,v in sorted(coeff.items()) if v}


def parity():
    words=histories(4,4,0,"L")
    co=lag_coefficients(words,4)
    require(co=={0:3,2:-2},"wrong fourth-tick lag coefficients")
    rates=[Fraction(sum(v*((-1)**k if u==2 else 1) for u,v in co.items()),16)
           for k in range(4)]
    require(rates==[Fraction(1,16),Fraction(5,16)]*2,"parity failure")
    return dict(order=4,words=words,coefficients=co,denominator=16,
                rates_k0_to_3=list(map(str,rates)),count=str(Fraction(len(words),16)))


def prime_rows(primes):
    result=[]
    for p in primes:
        dark=histories(p,3,-1,"L")
        bright=histories(p,3,1,"R")
        require(lag_coefficients(dark,p)=={0:2,1:-2} and
                lag_coefficients(bright,p)=={0:2,1:2},"prime-port word coefficients")
        # For K=1, dark probability D=(1/2)sin²(pi/p)>=2/p² by the
        # chord bound sin x>=2x/pi. Independent misses are <=exp(-n*D).
        # Taking n>=3p²/2 gives failure <=exp(-3)<1/20.
        n=ceil(Fraction(3*p*p,2))
        require(n*Fraction(2,p*p)>=3 and
                sum(Fraction(3**j,factorial) for j,factorial in
                    enumerate((1,1,2,6,24,120,720,5040,40320,362880)))>20,
                "95 percent launch certificate")
        result.append(dict(order=p,dark=dark,bright=bright,
                           dark_cos_coefficients={"0":2,"1":-2},denominator=8,
                           safe_launch_count_95_ordinary=n))
    return result


def homogeneous_markov():
    # r=P(R|R), l=P(R|L). Polynomials below use increasing powers of r.
    # The three word probabilities sum to (1-l)r²(1-r)+2l*r*(1-r)².
    def multiply(a,b):
        out=[Fraction(0)]*(len(a)+len(b)-1)
        for i,x in enumerate(a):
            for j,y in enumerate(b):
                out[i+j]+=x*y
        return out
    for poly,root,offset in (([Fraction(4,27),0,-1,1],Fraction(2,3),[Fraction(1,3),1]),
                             ([Fraction(4,27),-1,2,-1],Fraction(1,3),[Fraction(4,3),-1])):
        require(multiply(multiply([-root,1],[-root,1]),offset)==poly,
                "exact Markov extremum factorization")
    words=[w for w,_,_ in histories(4,4,0,"L")]
    def word_prob(w,r,l):
        prev="R"
        prob=Fraction(1)
        for c in w:
            right=r if prev=="R" else l
            prob*=right if c=="R" else 1-right
            prev=c
        return prob
    for r,l in product((Fraction(0),Fraction(1,3),Fraction(2,3),Fraction(1)),repeat=2):
        observed=sum(word_prob(w,r,l) for w in words)
        require(observed==(1-l)*r*r*(1-r)+2*l*r*(1-r)**2,"wrong Markov paths")
    r,l=Fraction(1,3),Fraction(1)
    hard=sum(word_prob(w,r,l) for w in words)
    gap=Fraction(5,16)-hard
    require(hard==Fraction(8,27) and gap==Fraction(7,432),"wrong exact maximum")
    # Homogeneous transition on (mode,index), index advances cyclically.
    # Stable hidden mode is sampled once; no external time-dependent coin.
    modes=[("RRLL",Fraction(5,16)),("RRRR",Fraction(11,16))]
    counter=Fraction(0)
    hidden=[]
    for sequence,weight in modes:
        index,x,c=0,0,"R"
        for _ in range(4):
            c=sequence[index]
            index=(index+1)%4
            x=(x+(1 if c=="R" else -1))%16
        if (x,c)==(0,"L"):
            counter+=weight
        hidden.append([sequence,str(weight),x,c])
    require(counter==Fraction(5,16),"hidden memory control")
    return dict(rail_only_maximum=str(hard),maximizing_r_l=[str(r),str(l)],gap=str(gap),
                hidden_initial_modes_and_outputs=hidden,hidden_port=str(counter))


def fold(k,m):
    return min(k%m,(-k)%m)


def invert_ports(a,b):
    c1=(16*(a+b)-6)/4
    c2=(3-16*a)/2
    return c1,c2,(1+c2)/2-c1*c1


def exact_panel(m,parts):
    """At orders four and six all character cosine values are rational."""
    f=Fraction
    root={3:[f(1),f(-1,2),f(-1,2)],4:list(map(f,(1,0,-1,0))),
          6:[f(1),f(1,2),f(-1,2),f(-1),f(-1,2),f(1,2)]}[m]
    require(sum(w for _,w in parts)==1 and all(w>=0 for _,w in parts),"bad weights")
    def port(site,rail):
        rows=histories(m,4,site,rail)
        coeff=lag_coefficients(rows,m)
        return sum(w*(len(rows) if k is None else
                      sum(v*root[(l*k)%m] for l,v in coeff.items())) for k,w in parts)/16
    a,b=port(0,"L"),port(2,"R")
    x,y,gap=invert_ports(a,b)
    c=sum(w for k,w in parts if k is None)
    co=[(root[k%m],w) for k,w in parts if k is not None]
    mean=sum(v*w for v,w in co)
    variance=sum(w*(v-mean)**2 for v,w in co)+c*mean**2
    require(x==mean and y==sum(w*(2*v*v-1) for v,w in co) and
            gap==variance+f(c,2),"incorrect exact four-tick moment identity")
    return dict(order=m,parts=[["count" if k is None else k,str(w)] for k,w in parts],
                A=str(a),B=str(b),C1=str(x),C2=str(y),gap=str(gap),
                variance_including_count_at_zero=str(variance),count=str(c))


def simultaneous_panel():
    f=Fraction
    orders=range(3,65)
    scans=[]
    for m in orders:
        left=lag_coefficients(histories(m,4,0,"L"),m)
        right=lag_coefficients(histories(m,4,2,"R"),m)
        expect_a=Counter({0:3})
        expect_b=Counter({0:3,1:4})
        expect_a[fold(2,m)]-=2
        expect_b[fold(2,m)]+=2
        require(left==expect_a and right==expect_b,"incorrect cyclic autocorrelation")
        # Folded gap = 2 sin(pi/m) sin((2k+1)pi/m). The distance
        # of the odd integer to 0 mod m is smallest at k=0 and ties
        # also at the last gap exactly when m is even and m>=4.
        ks=range(m//2)
        gap_ranks=[min(2*k+1,m-2*k-1) for k in ks]
        minima=[k for k,v in enumerate(gap_ranks) if v==1]
        require(minima==([0] if m%2 else sorted({0,m//2-1})),"odd-order endpoint gap")
        # Numerical checks are diagnostics only; the exact autocorrelation
        # and double-angle identity establish the formulas for all labels.
        residuals=[]
        for s in range(m//2+1):
            def evaluate(coeff):
                return sum(v*cos(2*pi*s*h/m) for h,v in coeff.items())/16
            x,y,gap=invert_ports(evaluate(left),evaluate(right))
            residuals.append([x-cos(2*pi*s/m), y-cos(4*pi*s/m),gap])
        scans.append(dict(order=m,coefficients_A=left,coefficients_B=right,
                          minimizing_adjacent_indices=minima,binary64_residuals=residuals))
    exact={}
    for name,m,parts in (
        ("count",4,[(None,f(1))]),("quarter",4,[(1,f(1))]),
        ("unequal_neighbor",4,[(0,f(1,100)),(1,f(99,100))]),
        ("unequal_neighbor_near_zero",6,[(0,f(99,100)),(1,f(1,100))]),
        ("count_shadow",4,[(None,f(1,100)),(1,f(99,100))]),
        ("coarse_three",3,[(1,f(1))]),("fine_six",6,[(0,f(3,4)),(3,f(1,4))])):
        exact[name]=exact_panel(m,parts)
    require(exact["count"]["gap"]=="1/2" and exact["quarter"]["gap"]=="0" and
            exact["count_shadow"]["gap"]=="1/200" and
            exact["unequal_neighbor"]["gap"]=="99/10000" and
            exact["unequal_neighbor_near_zero"]["gap"]=="99/40000","boundary mixtures")
    coarse=exact["coarse_three"]
    fine=exact["fine_six"]
    apparent=(1+f(coarse["C1"]))/2-f(fine["C1"])**2
    require(apparent==0 and fine["gap"]=="3/4" and fine["C2"]!=coarse["C1"],
            "dyadic unlinked-preparation control")
    # Separate efficiency/read settings can fabricate both entries. At M=4
    # order a device measures A with quarter character and B with counting
    # plus a 1/3 throughput. Same use of the unconditioned pair would
    # disallow this change of source law and detector efficiency.
    switched=(f(exact["quarter"]["A"]),f(exact["count"]["B"])/3)
    require(invert_ports(*switched)[2]==0,"address-dependent assay control")
    # A single stationary enlarged device also reproduces the joint A,B
    # table for that character: choose a hidden deterministic directional
    # program at launch, then advance its internal phase cyclically.
    modes=[("RRLL",f(5,16)),("RRLR",f(1,16)),("RRRR",f(10,16))]
    hits=Counter()
    for word,weight in modes:
        x=word.count("R")-word.count("L")
        hits[x,word[-1]]+=weight
    hidden=(hits[0,"L"],hits[2,"R"])
    require(hidden==switched and sum(hits.values())==1,"simultaneous hidden model")
    return dict(scan=scans,exact_examples=exact,
                dyadic_false_gap=str(apparent),
                addressed_settings_false_panel=list(map(str,switched)),
                hidden_programs=[[w,str(p)] for w,p in modes],
                hidden_same_panel=list(map(str,hidden)))


def controls(primes):
    # Each odd prime can divide at most one of 3 and 5. Their mixture has
    # positive dark probability at every tested prime, and both are odd.
    require(gcd(3,5)==1,"invalid mixed control")
    mixture=[[p,3%p!=0,5%p!=0] for p in primes]
    require(all(a or b for _,a,b in mixture),"mixed qualitative false pass")
    orders=[4,*primes[:5]]
    alias=1+lcm(*orders)
    require(alias!=1 and all(fold(alias,m)==1 for m in orders),"finite alias")
    # Once n exceeds 3K the closed-third criterion is automatic forever.
    def tail(k,n):
        initial=n
        rows=[]
        while True:
            f=fold(k,n)
            rows.append([n,f,3*f<=n])
            if n>=3*k:
                break
            n*=2
        return dict(k=k,start=initial,rows=rows,passes=all(x[2] for x in rows))
    cases=[tail(k,n) for k,n in ((1,4),(3,4),(3,8),(3,16),(5,16),(16,12),(32,12))]
    require([c["passes"] for c in cases]==[True,False,False,True,True,True,True],
            "closed-third cutoff controls")
    for start in range(4,25):
        for k in range(128):
            d=fold(k,start)
            if 3*d<start and tail(k,start)["passes"]:
                require(k==d,"strict-anchor failure")
    return dict(mixed_3_and_5_dark_nonzero=mixture,
                finite_alias=dict(orders=orders,k=alias),
                known_cutoff_cases=cases)


def run():
    primes=(3,5,7,11,13,17,19,31,101,1009)
    return dict(scope="Prime tests assume a pure, locked K; simultaneous panel tests count/character mixtures. Per launch.",
                parity=parity(),prime_records=prime_rows(primes),
                markov=homogeneous_markov(),controls=controls(primes),
                simultaneous_four_tick_panel=simultaneous_panel())


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory",type=Path)
    folder=parser.parse_args().directory
    file=folder/"prime_port_records.json"
    if file.exists():
        parser.exit(2,f"Refusing to overwrite {file}\n")
    data=run()
    folder.mkdir(parents=True,exist_ok=True)
    with file.open("x",encoding="utf8",newline="\n") as out:
        json.dump(data,out,separators=(",",":"))
        out.write("\n")
