"""Exact adjoints, classical return probabilities and reversible record controls.

Run python -B check_staircase_echo.py OUTPUT_DIRECTORY. Standard library.
Data are indexed by (position, rail in {1,-1}, sheet residue).
"""
import argparse
from collections import Counter, defaultdict
from fractions import Fraction as F
from itertools import product
import json
from math import comb, cos, pi
from pathlib import Path

from check_character_tomography import word_data


RAILS = (1, -1)


def edges(m, state, reverse=False, signed=True):
    x, d, j = state
    if reverse:
        u = (x-d) % (4*m)
        for c in RAILS:
            yield (u, c, (j-u//2) % m), -1 if signed and c == d == -1 else 1
    else:
        for c in RAILS:
            yield ((x+c) % (4*m), c, (j+x//2) % m), -1 if signed and c == d == -1 else 1


def step(m, vector, reverse=False, signed=True):
    out = Counter()
    for state, a in vector.items():
        for dest, sign in edges(m, state, reverse, signed):
            out[dest] += a*sign
    return {s:a for s,a in out.items() if a}


def perm(m, mode, name):
    x, d, j = mode
    if name == "mirror":
        return ((1-x+d) % (4*m), d, j), 1
    if name == "lane_sheet_sign":
        return ((x-d) % (4*m), -d, -j % m), -d
    if name == "lane_sheet_no_sign":
        return ((x-d) % (4*m), -d, -j % m), 1
    if name == "lane_sign_no_sheet":
        return ((x-d) % (4*m), -d, j), -d
    if name == "stream_and_gain":
        return ((x+d) % (4*m), d, (j+x//2) % m), 1
    raise ValueError(name)


def switch(m, v, name):
    w = {}
    for s, a in v.items():
        u, b = perm(m,s,name)
        w[u] = a*b
    return w


def forward_word(m, state, name):
    return switch(m,step(m,switch(m,{state:1},name)),name)


def matrix_tests(m):
    n = 4*m
    names = ("mirror","lane_sheet_sign","lane_sheet_no_sign","lane_sign_no_sheet")
    mismatches = {s:0 for s in names}
    first_failure = {}
    for state in product(range(n), RAILS, range(m)):
        direct = dict(edges(m,state,True))
        for name in names:
            compiled = forward_word(m,state,name)
            if compiled != direct:
                mismatches[name] += 1
                first_failure.setdefault(name, dict(input=state, compiled=sorted(compiled.items()), expected=sorted(direct.items())))
        for name, phase in (("mirror",1),("lane_sheet_sign",-1)):
            u,b = perm(m,state,name)
            dest,c = perm(m,u,name)
            assert dest==state and b*c==phase
        u=state
        for _ in range(n):
            u,_=perm(m,u,"stream_and_gain")
        assert u==state
        assert step(m,step(m,{state:1}),True)=={state:2}
    assert mismatches["mirror"]==mismatches["lane_sheet_sign"]==0
    assert mismatches["lane_sheet_no_sign"]>0
    return dict(M=m,physical_basis_columns=n*2*m,transpose_mismatches=mismatches,
                first_failure=first_failure,stream_gain_forward_period=n)


def literal_oracle(m,t):
    # A column of the signed numerator A=2^(t/2) U^t for every base mode
    # and sheet zero. Translation of the sheet supplies all other columns.
    columns={}
    for x,c in product(range(4*m),RAILS):
        col=Counter()
        for w in product(RAILS,repeat=t):
            (u,d),g,sign=word_data(w,m,x)
            if c==w[0]==-1:  # helper assumes initial rail R
                sign=-sign
            col[u,d,g%m]+=sign
        columns[x,c]={s:a for s,a in col.items() if a}
        recursive={(x,c,0):1}
        for _ in range(t):
            recursive=step(m,recursive)
        assert recursive==columns[x,c]
    # Translation-covariant Gram rows A* A; exercise all physical columns.
    for start,col in columns.items():
        for (x,c),other in columns.items():
            for offset in range(m):
                gram=sum(a*other.get((u,d,(j-offset)%m),0) for (u,d,j),a in col.items())
                assert gram==(2**t if (x,c)==start and offset==0 else 0)
    return dict(M=m,t=t,spatial_rail_columns=len(columns),word_visits=len(columns)*2**t,
                gram_entries_up_to_common_sheet_translation=len(columns)**2*m,diagonal=2**t)


def count_column(m, t, x0):
    """p_t(v) numerators with denominator 2^t; t>=1."""
    dist = Counter()
    for r in range(t):
        for d in RAILS:
            dist[(x0+2*r-(t-1)+d)%(4*m),d] += comb(t-1,r)
    return dist


def count_row(m,t,x0,d0):
    den = 4**t
    col = count_column(m,t,x0)
    match = F(sum(v*v for v in col.values()),den)
    assert sum(col.values())==2**t
    unfolded = F(comb(2*t-2,t-1),2*4**(t-1))
    alias_sum = sum(comb(2*t-2,j) for j in range(2*t-1) if (j-(t-1))%(2*m)==0)
    assert match==F(alias_sum,2*4**(t-1))
    # Direct forward and transpose runs on all base ports, ignoring amplitudes.
    def flight(v, back):
        for _ in range(t):
            out=Counter()
            for (x,d),num in v.items():
                for c in RAILS:
                    dest=((x-d if back else x+c)%(4*m),c)
                    out[dest]+=num
            v=out
        return v
    fwd=flight(Counter({(x0,d0):1}),False)
    echo=flight(fwd,True)
    assert fwd==col and echo[x0,d0]==den*match
    assert echo[x0,1]+echo[x0,-1]==den*2*match
    assert sum(echo.values())==den and match>=F(1,4*m)
    return dict(t=t,base_and_rail_return=str(match),position_only_return=str(2*match),
                line_return=str(unfolded),extra_from_winding=str(match-unfolded),
                forward_counts=[[x,c,k] for (x,c),k in sorted(fwd.items())],
                echo_counts=[[x,c,k] for (x,c),k in sorted(echo.items())])


def record_instrument(m,t,launch,mode):
    """Rail copies form labels at forward outputs and/or reverse inputs.

    Reversible erasure XORs with the matching reverse input *before* H.
    New reverse tags have fresh indices. Endpoint filtering happens only once.
    """
    initial=(*launch,0)
    v={(initial,0):1}
    allbits=(1<<t)-1
    masks={
        "coherent":(0,0,0),
        "forward_archive":(allbits,0,0),
        "midpoint_rail_only":(1<<(t-1),0,0),
        "complete_erase":(allbits,allbits,0),
        "omit_first_erase":(allbits,allbits^1,0),
        "independent_both_archives":(allbits,0,allbits)}
    forward, erase, fresh = masks[mode]
    for h in range(2*t):
        back = h>=t
        i = 2*t-1-h if back else h
        bit=1<<i
        out=Counter()
        for (s,z),a in v.items():
            for dest, sign in edges(m,s,back):
                tag=z
                if not back and forward & bit and dest[1]==-1:
                    tag ^= bit
                if back and s[1]==-1:
                    if erase & bit:
                        tag ^= bit
                    if fresh & bit:
                        tag ^= bit<<t
                out[dest,tag] += a*sign
        v={s:a for s,a in out.items() if a}
    den=4**t
    assert sum(a*a for a in v.values())==den
    if mode in ("coherent","complete_erase"):
        assert v=={(initial,0):2**t}
    rows=defaultdict(lambda:defaultdict(lambda:[0]*m))
    for ((x,c,j),tag),a in v.items():
        rows[x,c][tag][j]=a
    def group_corr(tags):
        return [sum(a*v[(j+h)%m] for v in tags.values() for j,a in enumerate(v)) for h in range(m)]
    ac={s:group_corr(tags) for s,tags in rows.items()}
    # Character probability at s is Fourier(ac[s])/den, traced over every tag.
    assert [sum(z[h] for z in ac.values()) for h in range(m)]==[den]+[0]*(m-1)
    target=ac.get(launch,[0]*m)
    if mode=="independent_both_archives":
        for row in ac.values():
            assert row[1:]==[0]*(m-1)
        assert target[0]==sum(v*v for v in count_column(m,t,launch[0]).values())
        counts=count_row(m,t,*launch)["echo_counts"]
        assert {(x,c):v for x,c,v in counts}=={s:v[0] for s,v in ac.items()}
    if mode=="omit_first_erase":
        assert target==[den//2]+[0]*(m-1)
    if mode=="midpoint_rail_only":
        # Each chosen midpoint rail has equal mass at the first tick, but need
        # not have equal mass at later ticks in every signed character.
        if t==1:
            assert target==[2]+[0]*(m-1)
    return dict(mode=mode,denominator=den,base_rail_autocorrelation=[[x,c,*row] for (x,c),row in sorted(ac.items())],
                target_pair_coefficients=target,localized_sheet_unread_return=str(F(target[0],den)),
                target_returns_by_k=[round(sum(a*cos(2*pi*k*h/m) for h,a in enumerate(target))/den,12) for k in range(m)],
                final_nonempty_tags=len({tag for s,tag in v}))


def visibility_control():
    # The two midpoint branches share tag |0> or rotate it by the real
    # rational matrix [[v,-s],[s,v]]. After unstream, subtraction of the
    # two actual departure gains and the final H, trace the untouched tag.
    trials=[]
    for v,s in ((F(1),F(0)),(F(3,5),F(4,5)),(F(0),F(1)),(F(-3,5),F(4,5)),(F(-1),F(0))):
        assert v*v+s*s==1
        midpoint={(0,1,0,0):F(1)}
        first=Counter()
        for (x,c,j,tag),amp in midpoint.items():
            for (u,d,z),sign in edges(6,(x,c,j)):
                tag_vector=(1,0) if d==1 else (v,s)
                for b,coef in enumerate(tag_vector):
                    first[u,d,z,b]+=sign*amp*coef
        terminal=Counter()
        for (x,c,j,tag),amp in first.items():
            for dest,sign in edges(6,(x,c,j),True):
                terminal[*dest,tag]+=sign*amp
        ports=[sum(a*a for (x,d,j,b),a in terminal.items() if d==c)/4 for c in RAILS]
        assert ports==[(1+v)/2,(1-v)/2]
        trials.append(dict(real_overlap=str(v),orthogonal_coefficient=str(s),two_rail_probabilities=list(map(str,ports))))
    return trials


def calibration(m,t,c,eta,observed_error):
    count=count_column(m,t,0)
    r=F(sum(n*n for n in count.values()),4**t)
    rows=[]
    for loss in (F(0),eta/2,eta):
        actual=c*r+(1-c)*(1-loss)
        for delta in (-observed_error,0,observed_error):
            p=max(0,min(1,actual+delta))
            lo=max(F(0),(1-eta-p-observed_error)/(1-r-eta))
            hi=min(F(1),(1-p+observed_error)/(1-r))
            assert lo<=c<=hi
            rows.append(dict(coherent_loss=str(loss),observed=str(p),ideal_inversion=str((1-p)/(1-r)),
                             permitted_count=[str(lo),str(hi)]))
    return dict(M=m,t=t,actual_count=str(c),count_return=str(r),max_coherent_loss=str(eta),
                absolute_observation_error=str(observed_error),trials=rows)


def main():
    cases=[]
    for m,x0,d0 in ((3,0,1),(4,15,-1),(6,0,1),(6,23,-1)):
        cases.append(dict(M=m,launch=[x0,d0],counts=[
            count_row(m,t,x0,d0) for t in sorted({1,2,3,4,5,8,2*m,2*m+1,4*m,8*m})]))
    modes=("coherent","complete_erase","midpoint_rail_only","omit_first_erase",
           "forward_archive","independent_both_archives")
    tags=[]
    for m,x,c,horizons in ((6,0,1,range(1,7)),(3,11,-1,(2,5)),(4,15,-1,(3,5)),(6,1,-1,(3,5))):
        for t in horizons:
            rows=[record_instrument(m,t,(x,c),mode) for mode in modes]
            if (m,x,c,t)==(6,0,1,5):
                numerators=[round(256*v) for v in rows[4]["target_returns_by_k"]]
                assert numerators==[31,33,37,39,37,33]
                assert rows[5]["localized_sheet_unread_return"]=="35/256"
            tags.append(dict(M=m,launch=[x,c],t=t,instruments=rows))
    return dict(
        walk="N=4M, d=+1 (R) or -1 (L), phase index j mod M. U is H, then add floor(x/2) to j at departure, then stream by outgoing d. One negative Hadamard entry LL. Reverse counts and squares use the same 2t balanced splitters. Input is localized in the initial base and rail. All terminal base ports sum over sheet and tag; character runs specify their sheet eigenlabel.",
        adjoint="On input (x,d,j), a reverse tick first unstreams to u=x-d, subtracts g(u) from j, then takes H from d to outgoing c. The two signed amplitudes share the same coordinate u and the known balanced denominator. These are actual inverse operations the instrument must supply.",
        forward_compilers={
            "mirror":"J(x,d,j)=(1-x+d,d,j). J^2=I, J U J=U*. Indeed g(1-u)=-g(u) mod M and H is symmetric. Two J permutations around U^t implement (U*)^t with exactly t splitters; copy from irreversible postprocessing cannot substitute for transport during the circuit. Spatial reflection moves some amplitudes a distance approaching half the base circumference.",
            "lane_sheet_sign":"A(x,d,j)=(-d)|(x-d,-d,-j)>. A is a signed permutation: sheet reflection P, disjoint swaps B of adjacent directed lanes, then rail sign Z. A^2=-I and A U A=U*: d*c*H[-c,-d]=H[c,d]. Thus A U^t A=(-1)^(t-1)(U*)^t, up to one known global sign; repeated A U A gives exact phase. Two local cross-bond lane exchanges plus two rail signs and two sheet inversions for the block. A spatially local base register can contain the reflection on its sheet labels; on a physical cyclic sheet with nearest-neighbor motion P has distance cost up to 2*floor(M/4) for even M and floor(M/2) for odd M. Costs of compiling it are outside the base-tick count.",
            "independent_strokes":"Writing U=L H, independent deterministic L=stream after staircase has L^(4M)=I because each rail visits all sites, summing 2M(M-1) modulo M. Applying 4M-1 forward L strokes then H implements U*. Replacing independent L by U H introduces extra balanced history choices; count return must be recalculated for that changed schedule.",
            "scope":"The fixed operation U acting alone has not been shown to synthesize an inverse. Each construction declares which extra held controls it uses. The exact column checks score both damaging omitted primitives."},
        basis_tests=[matrix_tests(m) for m in (3,4,5,6,9)],
        independent_full_gram=[literal_oracle(3,4),literal_oracle(4,3)],
        count_formula="For t>=1 put n=t-1. In counting the probability of returning to the initial spatial AND rail port is r_t=2^(-2n-1) sum_l binom(2n,n+2M*l), with out-of-range binomials zero. This follows by folding the binomial law of the first n fair steps modulo 2M right-step counts, taking its squared norm, multiplying by 1/2 for the last rail, and applying Vandermonde. The full return law is (P^t)^T P^t applied to the launch. Raw forward/echo count denominators are 2^t/4^t. Before t=2M+1, r_t=binom(2n,n)/(2*4^n). At fixed M the finite cyclic lazy convolution mixes the right-step count mod 2M to uniform, giving r->1/(4M). Position-only return is 2r since the last reverse H randomizes the terminal rail. At t=1 a position-only detector always records return.",
        count_trials=cases,record_trials=tags,one_tick_partial_visibility=visibility_control(),
        record_encoding="Each base_rail_autocorrelation row lists x,c,A_0,...,A_(M-1). Exact numerator for character k is sum_h A_h cos(2*pi*k*h/M); sum over all unobserved orthogonal tags. A localized sheet gives A_0 after summing its terminal sheet. Each row divides by 4^t. Omitted base ports have probability zero. The decimal table is illustrative; integer coefficients are sufficient.",
        record_scope="In complete erase, each forward rail bit is XORed again from that rail at the matched reverse time before the inverse H. When only the first bit survives the inner forward/reverse pairs cancel, leaving a single recorded split and return 1/2. A forward-only archive still permits interference on the reverse leg. Fresh permanent archives on both legs reproduce counting at every base port. Missing or unobserved tags are operationally different from erase.",
        inference="With the same c and nonnegative signed-character weights on this composition, exact deterministic undo gives R=(1-c)+c*r, so c=(1-R)/(1-r). A probability error Delta gives count error <=Delta/(1-r) if every signed return is exactly one. If the mean signed return is only known to lie in [1-eta,1] and |Robs-R|<=Delta, an interval is [max(0,(1-eta-Robs-Delta)/(1-r-eta)),min(1,(1-Robs+Delta)/(1-r))] for eta<1-r. Unknown history tags can duplicate the count response at c=0. These records alone cannot distinguish such an environment from an intrinsic counting coefficient.",
        bounded_error_checks=calibration(6,5,F(1,4),F(1,20),F(1,100)))


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("directory",type=Path)
    directory=parser.parse_args().directory
    directory.mkdir(parents=True,exist_ok=True)
    result=main()
    (directory/"staircase_echo.json").write_bytes((json.dumps(result,separators=(",",":"))+"\n").encode())
    print(len(result["basis_tests"]),"full-basis tests,",len(result["record_trials"]),"tagged series")
