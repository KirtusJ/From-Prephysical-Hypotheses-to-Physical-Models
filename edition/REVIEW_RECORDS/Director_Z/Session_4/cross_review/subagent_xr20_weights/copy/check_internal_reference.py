"""Check a finite, fixed signed graph supplying internal character-phase references."""
import argparse
import hashlib
import json
from collections import Counter
from fractions import Fraction
from functools import reduce
from itertools import product
from math import comb, gcd, sqrt
from pathlib import Path

CASES = ((3,2),(5,2),(5,3),(9,2),(15,2))


def fold(value, order):
    residue = value % order
    return min(residue, order-residue)


def dot(a, b):
    return sum(x*y for x,y in zip(a,b))


def spatial_graph(order, dim):
    menu = list(product(range(order), repeat=dim))
    zero = (0,)*dim
    increments = [zero]*(2*len(menu))
    total = zero
    for j, v in enumerate(menu):
        total = tuple((a+b) % order for a,b in zip(total,v))
        increments[2*j+1] = total
    assert total == zero
    return menu, increments


def check_diamonds(order, menu, increments):
    """Enumerate all eight real three-step histories in physical (position,coin,sheet) coordinates."""
    length, dim = len(increments), len(increments[0])
    negative_terms = positive_terms = zero_blocks = 0
    for x, incoming in product(range(length),(1,-1)):
        vector = menu[x//2] if x % 2 == 0 else (0,)*dim
        diff = tuple((a-b) % order for a,b in zip(increments[(x+1) % length],
                                                   increments[(x-1) % length]))
        assert diff == vector
        branches = {}
        for word in product((1,-1),repeat=3):
            pos, coin, sheet, sign = x, incoming, [0]*dim, 1
            for out in word:
                for i,gain in enumerate(increments[pos]):
                    sheet[i] = (sheet[i]+gain) % order
                if coin == out == -1:
                    sign = -sign
                pos, coin = (pos+out) % length, out
            branches.setdefault((pos,coin),Counter())[tuple(sheet)] += sign
        dark = branches.pop(((x-incoming) % length,-incoming))
        bright = branches.pop(((x+incoming) % length,incoming))
        assert sorted(sum(abs(n) for n in values.values()) for values in branches.values()) == [1]*4
        dark = {v:n for v,n in dark.items() if n}
        if any(vector):
            assert sorted(dark.values()) == [-1,1]
            assert sorted(bright.values()) in ([-1,-1],[1,1])
            assert dark.keys() == bright.keys()
            points = list(dark)
            displacements = {tuple((a-b) % order for a,b in zip(points[i],points[1-i])) for i in (0,1)}
            assert vector in displacements
            negative_terms += 2
            positive_terms += 2
        else:
            assert not dark and list(map(abs,bright.values())) == [2]
            zero_blocks += 1
    return dict(all_centres_and_incoming=2*length, three_step_histories=16*length,
                destructive_terms_at_nonzero_gain=negative_terms,
                constructive_terms_at_nonzero_gain=positive_terms, zero_gain_blocks=zero_blocks)


def primes(n):
    return [i for i in range(2,n+1) if n%i == 0 and all(i%j for j in range(2,i))]


def sectors(order, dim, menu):
    faithful = 0
    classes = Counter()
    checksum = hashlib.sha256()
    signed_recoveries = reversed_labels = 0
    for r in menu:
        image_order = order//reduce(gcd,r,order)
        values = {v:fold(dot(v,r),order) for v in menu}
        labels = sorted(set(values.values()))
        assert len(labels) == (image_order+1)//2
        classes[image_order] += 1
        checksum.update(bytes(values.values()))
        if image_order != order:
            continue
        faithful += 1
        vstar = next(v for v in menu if values[v] == 1)
        kstar = dot(vstar,r) % order
        assert kstar in (1,order-1)
        for orientation in (1,-1):
            anchor = tuple(orientation*v % order for v in vstar)
            k = (orientation*kstar) % order
            for v, rank in values.items():
                neighbour = tuple((i+j) % order for i,j in zip(v,anchor))
                matches = {i%order for i in (rank,-rank) if fold(i+1,order) == values[neighbour]}
                decoded, = matches
                assert decoded == (dot(v,r)*pow(k,-1,order)) % order
                signed_recoveries += 1
                if orientation < 0:
                    reversed_labels += 1
            for t in range(order):
                assert values[tuple(t*x % order for x in anchor)] == fold(t,order)
    expected = Fraction(len(menu))
    for p in primes(order):
        expected *= 1-Fraction(1,p**dim)
    assert expected == faithful
    return dict(hidden_tuples=len(menu), subgroup_order_counts=dict(sorted(classes.items())),
                faithful=faithful, limiting_yield=str(Fraction(faithful,len(menu))),
                possible_settings=len(menu), signed_label_checks=signed_recoveries,
                opposite_anchor_checks=reversed_labels, full_integer_fold_table_sha256=checksum.hexdigest())


def image_relabellings(order, dim, menu):
    """Keep the physical settings fixed; the character convention is permuted together with hidden labels."""
    units=[u for u in range(1,order) if gcd(u,order)==1]
    checks=0
    distinguish=0
    for u in units:
        inv=pow(u,-1,order)
        for r in menu:
            new=tuple(inv*x % order for x in r)
            for v in menu:
                old=fold(dot(v,r),order)
                relabelled=fold(u*dot(v,new),order)
                assert old==relabelled
                checks+=1
                distinguish+=old!=fold(u*dot(v,r),order)
    return dict(units=units, matched_hidden_setting_cases=checks,
                changed_tagged_cases_when_label_held_fixed=distinguish)


def product_ring(a,b):
    return a[0]*b[0]+5*a[1]*b[1],a[0]*b[1]+a[1]*b[0]


def pair_sum(pairs):
    return tuple(map(sum,zip(*pairs)))


def powers(pair,n):
    values=[(1,0)]
    for j in range(n):
        values.append(product_ring(values[-1],pair))
    return values


def finite_five(n=16):
    """All count outcomes of two fixed-length scans of the localized 5-sheet register.

    Dark vs non-dark is a classical coarse graining of full per-block coordinate records.
    Successive steps of the scan start at the desired centre using sheet-blind transfer.
    """
    # Raw three-step dark mass = (1-cos(2*pi*fold/5))/4 = (5 +/- sqrt(5))/16.
    # Pair entries are integer coefficients in Q(sqrt(5)); use a common denominator.
    likelihoods={}
    for sign in (-1,1):
        hits=powers((5,sign),n)
        misses=powers((11,-sign),n)
        values=[]
        for k in range(n+1):
            a,b=product_ring(hits[k],misses[n-k]); c=comb(n,k)
            values.append((c*a,c*b))
        assert pair_sum(values)==(16**n,0)
        likelihoods[sign]=values
    norm=5*16**(2*n)
    rows=[]
    totals=Counter()
    accepted_correct_integer=accepted_correct_irrational=0
    for a,b in product(range(n+1),repeat=2):
        # For physical diamond h=1, the ±1 pair has the lower dark response.
        plane_1=product_ring(likelihoods[-1][a],likelihoods[1][b])
        plane_2=product_ring(likelihoods[1][a],likelihoods[-1][b])
        assert plane_2[0]==plane_1[0] and plane_2[1]==-plane_1[1]
        zero_numerator=16**(2*n) if a==b==0 else 0
        numerator=zero_numerator+2*(plane_2[0]+plane_1[0])
        gain=1 if a<b else 2 if b<a else None
        mass=Fraction(numerator,norm)
        totals[str(gain) if gain else "tie"]+=mass
        if gain:
            right=plane_1 if gain==1 else plane_2
            accepted_correct_integer+=2*right[0]
            accepted_correct_irrational+=2*right[1]
        rows.append(dict(dark_gain_one=a,dark_gain_two=b,selected_gain=gain,
                         total_probability=str(mass),
                         plane_2_numerator=list(plane_2),plane_1_numerator=list(plane_1),
                         count_pair_probability_given_trivial=int(zero_numerator!=0)))
    assert sum(totals.values())==1 and totals['1']==totals['2']
    accepted=1-totals['tie']
    # Rationalize neither the posterior nor the weight; keep exact pairs.
    accepted_num=int(accepted*norm)
    correct=(Fraction(accepted_correct_integer,accepted_num),Fraction(accepted_correct_irrational,accepted_num))
    err=(1-correct[0],-correct[1])
    next_rate=product_ring(correct,(Fraction(5,16),Fraction(-1,16)))
    wrong_rate=product_ring(err,(Fraction(5,16),Fraction(1,16)))
    measured=pair_sum((next_rate,wrong_rate))
    assert measured[1]==0
    return dict(order=5,independent_sheets=1,blocks_each_gain=n,total_probe_ticks=6*n,
                physical_diamond_order=[1,2],retention="Strict lower counted raw dark rate wins; ties all rejected. All non-dark suboutcomes retained as classical alternatives.",
                prior="Localized sheet; mass 1/5 trivial and 2/5 on each pair.",
                likelihood_denominator_per_hidden_pair=16**(2*n),
                scaled_prior_denominator=norm,
                outcome_masses={k:str(v) for k,v in totals.items()},
                total_acceptance=str(accepted),correct_given_acceptance=[str(x) for x in correct],
                wrong_given_acceptance=[str(x) for x in err],
                observed_next_dark_probability=str(measured[0]),
                numeric=dict(acceptance=float(accepted),wrong_given_acceptance=float(err[0])+sqrt(5)*float(err[1]),
                             observed_next_dark=float(measured[0])),rows=rows)


def tagged_diamond_oracle(finite):
    """Exact M=5 signed-path cone, cyclotomic character evaluation and named conditional count rows."""
    order=5
    menu,inc=spatial_graph(order,1)
    # 4*cos(2*pi*j/5) as rational + irrational*sqrt(5), indexed by the actual character exponent.
    cosine4=((4,0),(-1,1),(-1,-1),(-1,-1),(-1,1))
    rows=[]
    dark_masses={}
    for h,incoming,r in product(range(order),(1,-1),range(order)):
        centre=2*menu.index((h,))
        port=((centre-incoming)%len(inc),-incoming)
        counts=[0]*order
        for word in product((1,-1),repeat=3):
            x,c,y,sign=centre,incoming,0,1
            for d in word:
                y=(y+inc[x][0])%order
                sign*=(-1 if c==d==-1 else 1)
                x,c=(x+d)%len(inc),d
            if (x,c)==port:
                counts[y]+=sign
        # Evaluate |sum_y counts[y]*zeta^(r*y)|²/8 directly, without reading the analytic block.
        vals=[(a*b*cosine4[r*(i-j)%5][0],a*b*cosine4[r*(i-j)%5][1])
              for i,a in enumerate(counts) for j,b in enumerate(counts)]
        aa,bb=pair_sum(vals)
        value=(Fraction(aa,32),Fraction(bb,32))
        cc,ss=cosine4[(r*h)%order]
        expected=(Fraction(4-cc,16),Fraction(-ss,16))
        assert value==expected
        if (h,r) in dark_masses:
            assert value==dark_masses[h,r]
        dark_masses[h,r]=value
        rows.append(dict(physical_diamond_h=h,site=centre,incoming=incoming,tag=r,
                         named_dark_sheet_counts=counts,dark_probability=[str(x) for x in value]))
    named_numerators={}
    n=finite["blocks_each_gain"]
    for h,r in product((1,2),(1,2)):
        q=dark_masses[h,r]
        # The table numerator uses 16^n for each binomial likelihood.
        hit=tuple(v*16 for v in q)
        miss=(16-hit[0],-hit[1])
        hv,mv=powers(hit,n),powers(miss,n)
        for k in range(n+1):
            named_numerators[h,r,k]=tuple(comb(n,k)*v for v in product_ring(hv[k],mv[n-k]))
    verified=0
    for row in finite["rows"]:
        a,b=row["dark_gain_one"],row["dark_gain_two"]
        for r in (1,2):
            correct=product_ring(named_numerators[1,r,a],named_numerators[2,r,b])
            assert tuple(row[f"plane_{r}_numerator"])==correct
            verified+=1
    return dict(scope="Raw probabilities expressed as rational plus coefficient times sqrt(5), using the "
                      "named convention T maps to exp(2*pi*i*r/5). The oracle calculates each port from "
                      "signed coordinate paths and evaluates every cyclic autocorrelation before averaging any tags.",
                all_named_single_port_checks=len(rows), finite_named_plane_mass_checks=verified,rows=rows)



def signed_gram(order):
    """Verify a Fourier-norm coefficient via the cosine Gram matrix in the integral group ring."""
    # Store 2*Gram_ij formally in Z[T]/(T^M-1); 4*p = 1-cos from the integer diamond.
    profiles=([1,-2,3,0,1],[2,-1,0,1,-3],[3,0,-1,2,0])
    def correlation(a,b):
        result=[0]*order
        for i,av in enumerate(a):
            for j,bv in enumerate(b):
                result[(i-j)%order]+=av*bv
        return result
    def gram(a,b):
        result=[0]*order
        for i,av in enumerate(a):
            for j,bv in enumerate(b):
                # The signed dark diamond gives |T^(i-j)-1|² / 8.
                shift=(i-j)%order
                dark=[0]*order
                dark[0]-=1; dark[shift]+=1
                dark_square=correlation(dark,dark)
                result[0]+=2*av*bv
                for t,c in enumerate(dark_square):
                    result[t]-=c*av*bv
        return result
    rows=[]
    for a,b in ((profiles[0],profiles[0]),(profiles[0],profiles[1]),(profiles[1],profiles[2])):
        direct=correlation(a,b)
        real2=[direct[t]+direct[-t % order] for t in range(order)]
        reconstructed=gram(a,b)
        assert reconstructed==real2
        rows.append(dict(first=a,second=b,twice_real_gram_ring_coefficients=reconstructed))
    return dict(order=order,interpretation="For real integer A,B, this reconstructs Re[A(z) conjugate(B(z))]; A=B gives |A(z)|^2. "
                                      "The calibrated variable z is the phase of the physical path-translation difference h. Its relation to a departure increment depends on the graph.",
                polynomial_pairs=rows)


def physical_profile_control():
    # This test applies fixed signed path polynomials on a fresh localized sheet,
    # rather than interpreting a postselection as a primitive new vector source.
    order=5
    menu,inc=spatial_graph(order,1)
    rows=[]
    for gain in (1,2,3,4):
        centre=2*menu.index((gain,))
        state={(centre,1,0):1}
        widths=[]
        for destructive in (False,False,True,True):
            # Fixed direction routing before the next block only translates the sheet.
            site,coin,_=next(iter(state))
            while site!=centre:
                step=1 if (centre-site)%len(inc)<=len(inc)//2 else -1
                site_new=(site+step)%len(inc)
                state={(site_new,step,(y+inc[site][0])%order): val*(-1 if coin==step==-1 else 1)
                       for (_,coin,y),val in state.items()}
                site,coin=site_new,step
            chosen=(site-coin,-coin) if destructive else (site+coin,coin)
            for _ in range(3):
                after=Counter()
                for (x,c,y),val in state.items():
                    for d in (1,-1):
                        after[(x+d)%len(inc),d,(y+inc[x][0])%order]+=val*(-1 if c==d==-1 else 1)
                state=after
            state={key:v for key,v in state.items() if key[:2]==(chosen[0]%len(inc),chosen[1]) and v}
            widths.append(len(state))
        counts=[0]*order
        for (_,_,y),v in state.items():
            counts[y]=v
        # (1+T^h)^2(1-T^h)^2 = 1-2T^(2h)+T^(4h) up to translation and global sign.
        oracle=[0]*order
        for j,v in ((0,1),(2,-2),(4,1)):
            oracle[(j*gain)%order]+=v
        assert any(counts==[sg*oracle[(j-offset)%order] for j in range(order)]
                   for sg in (1,-1) for offset in range(order))
        c=sum(x*x for x in counts)
        assert c==6
        rows.append(dict(selected_gain=gain,finite_word="constructive twice, then destructive twice",
                         occupied_sheet_sites_after_each_probe=widths,physical_counts=counts,
                         normalized_sheet_probabilities=[str(Fraction(x*x,c)) for x in counts]))
    # Replacing labelled gain 1 with 2 changes physical spacings, even allowing ring translations.
    x,y=[r["normalized_sheet_probabilities"] for r in rows[:2]]
    assert not any(x==[y[(sg*j-offset)%order] for j in range(order)]
                   for sg in (-1,1) for offset in range(order))
    return dict(rows=rows,interpretation="Fixed physical gain, input, and record give the same coordinate table "
                "under every change of Fourier embedding. A genuinely different selected physical gain need "
                "not preserve spacings under native T-neighbour isometries. The example uses prescribed "
                "single-step transfers; its sheet table is conditional on that route and the four outcomes.")


def coordinate_tree():
    """Independent finite-grid dark-count law from physical sheets, summing every recorded outcome.

    Use the density matrix twirled over sheet shifts. This preserves a fresh localized
    input's law for the sheet-unresolved effects, which commute with translations.
    The cyclic autocorrelation of initially localized counts is exactly delta at zero.
    """
    order=5
    menu,inc=spatial_graph(order,1)
    lookup={}
    for gain in (1,2):
        x=2*menu.index((gain,))
        for coin in (1,-1):
            branches={}
            for word in product((1,-1),repeat=3):
                w,c,y,sign=x,coin,0,1
                for d in word:
                    y=(y+inc[w][0])%order
                    sign*=(-1 if d==c==-1 else 1)
                    w,c=(w+d)%len(inc),d
                branches.setdefault((w,c),Counter())[y]+=sign
            kernels={True:[0]*order,False:[0]*order}
            for outcome,counts in branches.items():
                category=outcome==((x-coin)%len(inc),-coin)
                for i,v in counts.items():
                    for j,z in counts.items():
                        kernels[category][(i-j)%order]+=v*z
            if gain in lookup:
                assert kernels==lookup[gain]
            lookup[gain]=kernels
    n=16
    states={(0,0):[1,0,0,0,0]}
    for which,gain in enumerate((1,2)):
        for t in range(n):
            new={}
            for pair,autocorr in states.items():
                for dark,kernel in lookup[gain].items():
                    idx=list(pair)
                    idx[which]+=int(dark)
                    dest=new.setdefault(tuple(idx),[0]*order)
                    for i,w in enumerate(autocorr):
                        for j,v in enumerate(kernel):
                            dest[(i+j)%order]+=w*v
            states=new
    return {pair:Fraction(v[0],8**(2*n)) for pair,v in states.items()}



def robust_cluster_controls(order, dim):
    # Rational rate surrogates exercise finite classification stratagems. Their
    # values are adversarial test inputs for the estimator, not simulated data.
    n=12*order**2
    rows=[]
    for subgroup_order in range(1,order+1,2):
        if order%subgroup_order:
            continue
        step=order//subgroup_order
        true=[j*step for j in range((subgroup_order+1)//2)]
        items=[(j,max(0,e+noise)) for j in true for e in (24*j,)
               for noise in (-3,2)]
        def classify(values):
            groups=[]
            for true_fold,count in sorted(values,key=lambda v:v[1]):
                if not groups or count-groups[-1][-1][1] > n//order**2:
                    groups.append([])
                groups[-1].append((true_fold,count))
            return [sorted({j for j,_ in group}) for group in groups]
        result=classify(items)
        assert result==[[j] for j in true]
        reversed_order=list(reversed(items))
        assert classify(reversed_order)==result
        bad=list(items)
        if len(true)>1:
            # A gross counting outlier for the final class crosses the separation threshold.
            bad[-2]=(true[-1],0)
            assert classify(bad)!=result
        rows.append(dict(image_order=subgroup_order,raw_trial_denominator=n,
                         synthetic_finite_counts=items,clusters=result,
                         reversed_input_same=True,outlier_counts=bad if len(true)>1 else None,
                         outlier_clusters=classify(bad) if len(true)>1 else None))
    return dict(scope="Exact rational stress of the finite clustering and reversed input order. Actual "
                "localized count probabilities are evaluated separately in finite_five.",rows=rows)



def main(out):
    cases=[]
    for order,dim in CASES:
        menu,inc=spatial_graph(order,dim)
        cases.append(dict(order=order,dimensions=dim,ring_sites=len(inc),diamonds=check_diamonds(order,menu,inc),
                          sectors=sectors(order,dim,menu),simultaneous_relabelling=image_relabellings(order,dim,menu),
                          gram=signed_gram(order),finite_sort_stress=robust_cluster_controls(order,dim)))
    finite=finite_five()
    direct=coordinate_tree()
    for row in finite["rows"]:
        assert str(direct[row["dark_gain_one"], row["dark_gain_two"]]) == row["total_probability"]
    finite["all_count_masses_verified_in_physical_coordinates"]=True
    result=dict(cases=cases,finite_five=finite,physical_profile=physical_profile_control(),
                named_five_diamond_oracle=tagged_diamond_oracle(finite),
                indexing="Across every fixed graph the menu label v is the literal physical diamond h, so the folded rank is fold(r dot v). "
                         "The archived first-index report used twice this rank, swapping the two named five-sheet planes while leaving aggregate probabilities invariant.",
                limitations="The exact five-sheet finite table is a one-register gain-one/gain-two classifier including all count-pair outcomes. "
                            "The multisheet yields are ideal identification limits, not finite-time observations. "
                            "Single-step routing records give known sheet translations; the stated fixed scanner block count excludes routing. "
                            "The exact group-ring identity concerns real Gram entries. The sign of the imaginary orientation is free.")
    out.mkdir(parents=True,exist_ok=True)
    dest=out/"internal_reference.json"
    dest.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(len(cases),"graph cases;",len(result["finite_five"]["rows"]),"finite count outcomes; SHA-256",hashlib.sha256(dest.read_bytes()).hexdigest())


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("directory",type=Path)
    main(parser.parse_args().directory)
