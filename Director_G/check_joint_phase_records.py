"""Replay physical two-walk position flags and compute the exact dimension of their character data.

Usage: python -B check_joint_phase_records.py NEW_OUTPUT_DIRECTORY
Only the native equal-clock lag word generator and the standard library are required.
"""
from collections import Counter
from fractions import Fraction
from itertools import product
import argparse
import json
from pathlib import Path

from check_equal_clock_lags import branches, path, return_to_home


def require(predicate, message):
    if not predicate:
        raise ValueError(message)


def make_menu(order):
    raw = [branches(13+(r-13) % order) for r in range(order)]
    clock = max(len(w)+abs(w.count("R")-w.count("L")+1)+1 for w, _ in raw)
    return [tuple(return_to_home(words, clock)) for words in raw]


def site_masks(words, order, home):
    traces = [path(w, home)[0] for w in words]
    return [set(x % (4*order) for x in pair) for pair in zip(*traces)]


def surviving_pairs(order, home, a, b, flag):
    """Return actual oriented word pairs, including the diagnostic first settings.

    The first-direction coordinates here label enumerated *histories*. They become
    orthogonal record bits only in the dephased comparator below.
    """
    size = 4*order
    ma, mb = site_masks(a, order, home), site_masks(b, order, home)
    require(len(ma) == len(mb), "different clocks")
    live = [(home % size, home % size, "", "")]
    for tick, (allowed_a, allowed_b) in enumerate(zip(ma, mb)):
        following = []
        for x, y, wa, wb in live:
            for (ca, da), (cb, db) in product((("R",1),("L",-1)), repeat=2):
                u, v = (x+da) % size, (y+db) % size
                if u in allowed_a and v in allowed_b:
                    if tick or flag is None or (u == v) == flag:
                        following.append((u, v, wa+ca, wb+cb))
        live = following
    return sorted(live)


def physical_label(word, order, home):
    x, sign, gain, previous = home % (4*order), 1, 0, "R"
    for c in word:
        gain = (gain+x//2) % order
        sign *= -1 if previous == c == "L" else 1
        x = (x+(1 if c == "R" else -1)) % (4*order)
        previous = c
    return x, previous, sign, gain


def panel(order, home, a, b, flag, target):
    actual = surviving_pairs(order, home, a, b, flag)
    expected = sorted((wa,wb) for wa,wb in product(a,b)
                      if flag is None or (wa[0] == wb[0]) == flag)
    require([(wa,wb) for _,_,wa,wb in actual] == expected,
            "a replayed word disagreed with the first-branch labels")
    bins = []
    for x,y,wa,wb in actual:
        xa,ra,sa,ga = physical_label(wa,order,home)
        xb,rb,sb,gb = physical_label(wb,order,home)
        require((x,y,xa,xb,ra,rb) == (target,target,target,target,"R","R"),
                "wrong named terminal port")
        bins.append((sa*sb,ga,gb))
    return bins


def scan(order, home):
    menu = make_menu(order)
    receipts = []
    for a,b in product(range(order),repeat=2):
        for same in (True,False):
            cells = panel(order,home,menu[a],menu[b],same,home)
            (h,g,k),(j,p,q) = cells
            require(h == j, "different signs on the admitted alternatives")
            lag = ((p-g)%order,(q-k)%order)
            target = (a,b if same else -b%order)
            require(lag in (target,tuple(-v%order for v in target)), "wrong joint lag")
            receipts.append([a,b,int(same),[list(c) for c in cells]])
    return dict(order=order, home=home, ticks=len(menu[0][0]), rows=receipts)


def contact_menu(order):
    """Use a sharp, individually masked prefix ending R, then two raw arms.
    The arms meet at the original physical home on opposite incoming rails.
    """
    raw = [tuple(w[:-1] for w in branches(13+(r-13)%order)) for r in range(order)]
    def displacement(w):
        return w.count("R")-w.count("L")
    clock = max(len(a)+abs(displacement(a))+2 for a,b in raw)
    require(clock%2==0,"contact clock parity")
    menu = []
    for a,b in raw:
        d = displacement(a)
        p = clock-len(a)
        right = (p-d)//2
        prefix = "L"*(p-right)+"R"*right
        require(right>=1 and displacement(prefix)==-d and displacement(b)==d and
                (a[-1],b[-1])==("L","R"), "invalid contact prefix or endpoints")
        menu.append((prefix,(prefix+a,prefix+b)))
    return menu


def contact_histories(order,home,lag,prefix,words):
    # This is a complete branching path enumeration, including potential
    # windings/cross-arcs. The prefix has no internal record of a route.
    size=4*order
    live=[(home,"")]
    for tick,allowed in enumerate(site_masks(words,order,home),1):
        live=[((x+step)%size,w+c) for x,w in live for c,step in (("R",1),("L",-1))
              if (x+step)%size in allowed]
        if tick<=len(prefix):
            require(live==[((home+prefix[:tick].count("R")-prefix[:tick].count("L"))%size,
                            prefix[:tick])],"prefix branch leaked")
    require(sorted(live)==sorted((home,w) for w in words),"unexpected incoming word")
    labels=[physical_label(w,order,home) for w in words]
    (x,ra,sa,ga),(y,rb,sb,gb)=labels
    require((x,y,ra,rb)==(home,home,"L","R") and sa==sb and (ga-gb)%order==lag,
            "translated staircase, sign, or incoming rails")
    return labels


def contact_tag(at_contact,ra,rb,pointer):
    # Codes 0 blank, 1 equal, 2 different. Controlled modular addition is
    # reversible on every pointer input, and is the identity off contact.
    displacement=(1 if ra==rb else 2) if at_contact else 0
    return (pointer+displacement)%3


def contact_scan(order,home):
    menu=contact_menu(order)
    clock=len(menu[0][1][0])
    arrivals=[contact_histories(order,home,r,prefix,w) for r,(prefix,w) in enumerate(menu)]
    rows=[]
    for a,b in product(range(order),repeat=2):
        daughters=Counter()
        rr={1:[],2:[]}
        for (_,ra,sa,ga),(_,rb,sb,gb) in product(arrivals[a],arrivals[b]):
            mark=contact_tag(True,ra,rb,0)
            for ca,cb in product("RL",repeat=2):
                sign=sa*sb*(-1 if ra==ca=="L" else 1)*(-1 if rb==cb=="L" else 1)
                ha=(ga+home//2)%order
                hb=(gb+home//2)%order
                daughters[ca,cb,mark]+=1
                if ca==cb=="R":
                    rr[mark].append((sign,ha,hb))
        require(len(daughters)==8 and set(daughters.values())=={2} and
                sum(daughters.values())==16,"incorrect pointer or outgoing cell census")
        for mark in (1,2):
            (s,g,k),(j,p,q)=rr[mark]
            require(s==j,"contact RR sign")
            desired=(a,b if mark==1 else -b%order)
            require(((g-p)%order,(k-q)%order) in
                    (desired,tuple(-z%order for z in desired)), "contact RR lag")
            rows.append([a,b,mark,[list(c) for c in rr[mark]]])
    den=4**clock
    tag_mass=Fraction(2,den)
    return dict(order=order,home=home,contact_tick=clock,final_tick=clock+1,
                in_flags_count_among_admitted=[0,2,2],in_denominator_per_launch=den,
                per_launch_at_contact={"admitted_blank":"0","equal":str(tag_mass),
                                       "different":str(tag_mass),
                                       "prior_or_current_mask_failure":str(1-2*tag_mass)},
                daughter_port=[(home+1)%(4*order),"R"],out_denominator=4**(clock+1),
                programs=[[p,list(w)] for p,w in menu],rows=rows)


def pointer_controls():
    for on,ra,rb in product((False,True),"RL","RL"):
        require(sorted(contact_tag(on,ra,rb,p) for p in range(3))==[0,1,2],
                "nonreversible qutrit write")
        if not on:
            require(all(contact_tag(on,ra,rb,p)==p for p in range(3)),"off-contact effect")
    # Input count of unit-weight, already distinct rail cells at the contact.
    # Reading the marked subset alone changes normalization if the input changes.
    controls={}
    for name,rows in (("four",list(product("RL",repeat=2))),
                      ("only_LR",[("L","R")]),("only_LL",[("L","L")])):
        counts=Counter(contact_tag(True,a,b,0) for a,b in rows)
        controls[name]=[counts[p] for p in range(3)]
    require(controls=={"four":[0,2,2],"only_LR":[0,0,1],"only_LL":[0,1,0]},
            "contact normalization control")
    # With the writer delayed until after the outgoing rail is chosen,
    # the named RR port labels every history equal. A one-rail mismatch
    # that flips the incoming R/L discriminator exchanges the two records.
    late=[contact_tag(True,"R","R",0) for _ in range(4)]
    require(late==[1]*4 and all(contact_tag(True,a,b,0)+
            contact_tag(True,a,("R" if b=="L" else "L"),0)==3
            for a,b in product("RL",repeat=2)), "pointer timing/label control")
    return dict(pointer_input_counts_blank_equal_different=controls,
                late_writer_RR_tag_counts=[0,4,0],unaddressed_contact_blank=True)


def orbit(x,y,m):
    """Representative of simultaneous conjugation on ordered pairs."""
    return min((x%m,y%m),(-x%m,-y%m))


def exact_rank(rows):
    """Sparse rational elimination with no tolerance."""
    echelon = {}
    for data in rows:
        row = {key:Fraction(v) for key,v in data.items() if v}
        while row:
            key = min(row)
            if key not in echelon:
                z = row[key]
                echelon[key] = {a:b/z for a,b in row.items()}
                break
            scale = row[key]
            for k,value in echelon[key].items():
                new = row.get(k,0)-scale*value
                if new:
                    row[k] = new
                else:
                    row.pop(k,None)
    return len(echelon)


def ranks(m):
    # Real cosine moments C(u,v) indexed by simultaneous-conjugacy orbits.
    # The invertible real Fourier transform relates these coordinates to real
    # character orbit weights. The directly visible product cos*cos is the
    # sum of the two moments below, up to the same nonzero scalar on each row.
    products, orientation, moments = [], [], set()
    for u,v in product(range(m),repeat=2):
        a,b = orbit(u,v,m),orbit(u,-v,m)
        products.append(Counter([a,b]))
        row = Counter([a])
        row.subtract([b])
        orientation.append(row)
        moments.add(a)
    p,k,full = exact_rank(products),exact_rank(orientation),exact_rank(products+orientation)
    r,u = m//2+1,(m-1)//2
    require((p,k,full)==(r*r,u*u,len(moments)) and full==p+k, "rank failure")
    # Independent preparation rows: (N, Fourier coefficients of the signed
    # autocorrelation). The cancelling pair and singleton separate N from
    # the zeroth moment; same-sign pairs generate each remaining cosine.
    local = [{"count":2}, {"count":1,0:1}]
    local += [{"count":2,0:2,h:2} for h in range(1,r)]
    def compound(row_a,row_b,allow_mixed):
        return {(str(a),str(b)):v*w for a,v in row_a.items() for b,w in row_b.items()
                if allow_mixed or (a=="count")== (b=="count")}
    product_counts = [exact_rank([compound(a,b,mixed) for a,b in product(local,repeat=2)])
                      for mixed in (False,True)]
    require(product_counts==[1+p,(r+1)**2],"count cross-term rank")
    return dict(order=m,coherent_product=p,relative_orientations=k,full=full,
                product_including_global_count=product_counts[0],full_including_global_count=1+full,
                product_with_separate_count_choices=product_counts[1])


def short(order):
    words = ("RLR","LRR")
    bins = {name:panel(order,0,words,words,flag,1)
            for name,flag in (("equal",True),("different",False),("no_flag",None))}
    incoming=contact_histories(order,0,1,"",tuple(w[:-1] for w in words))
    by_mark={1:[],2:[]}
    for (_,a,s,g),(_,b,j,k) in product(incoming,repeat=2):
        by_mark[contact_tag(True,a,b,0)].append((s*j,g,k))
    require(all(sorted(by_mark[mark])==sorted(bins[name]) for mark,name in
                ((1,"equal"),(2,"different"))),"three-tick contact vs first flag")
    require(len(bins["equal"])==len(bins["different"])==2 and len(bins["no_flag"])==4,
            "short history census")
    # Exact central rates. An ordered pair [a,b] represents a+b*sqrt(5).
    # For order 4 the second coefficient always vanishes.
    class Quad(tuple):
        def __new__(cls,a=0,b=0):
            return tuple.__new__(cls,(Fraction(a),Fraction(b)))
        def __add__(x,y):
            return Quad(x[0]+y[0],x[1]+y[1])
        def __rmul__(x,y):
            return Quad(x[0]*y,x[1]*y)
        def strings(x):
            return [str(v) for v in x]
    if order == 4:
        cosines = [Quad(1),Quad(),Quad(-1),Quad()]
    else:
        require(order==5,"expected fourth/fifth-root cosine table")
        c,d = Quad(Fraction(-1,4),Fraction(1,4)),Quad(Fraction(-1,4),Fraction(-1,4))
        cosines = [Quad(1),c,d,d,c]
    entries={}
    for name,cells in bins.items():
        probabilities={}
        def coherent(orientation, archive_a=False, archive_b=False):
            # Only histories sharing the archived first directions can interfere.
            # Here each walk has two words, with distinct residues 0,-1 that
            # explicitly identify its first direction.
            val = Quad()
            for h,g,k in cells:
                for j,p,q in cells:
                    if (not archive_a or g==p) and (not archive_b or k==q):
                        val += (h*j)*cosines[(g-p+orientation*(k-q))%order]
            return Fraction(1,64)*val
        for orientation in (1,-1):
            probabilities["aligned" if orientation==1 else "opposite"]=coherent(orientation).strings()
        counted=str(Fraction(len(cells),64))
        probs = [coherent(1, bool(a), bool(b)) for a,b in product(range(2),repeat=2)]
        require(probs[3].strings()==[counted,"0"], "permanent orthogonal records")
        probabilities.update(count=counted,resolved_both_first_bits=counted,
                             count_A_character_B=probs[2].strings(),
                             character_A_count_B=probs[1].strings())
        # Independent local counting weights c_A=1/3 and c_B=2/5, with
        # coherent orientation aligned whenever both factors are coherent.
        mixed = Quad()
        for weight,val in zip((6,4,3,2),probs):
            mixed += Fraction(weight,15)*val
        probabilities["independent_counts_one_third_two_fifths"]=mixed.strings()
        entries[name]=dict(bins=[list(c) for c in cells],probabilities=probabilities)
    eq,ne=entries["equal"]["probabilities"],entries["different"]["probabilities"]
    require(eq["opposite"]==ne["aligned"]==["1/16","0"],"wrong bright probability")
    require(eq["aligned"]==ne["opposite"]==(["0","0"] if order==4 else ["3/128","-1/128"]),
            "wrong interference probability")
    require(eq["count"]==ne["count"]=="1/32" and
            entries["no_flag"]["probabilities"]["aligned"]==
            entries["no_flag"]["probabilities"]["opposite"],"count or reality control")
    # No preparatory masks. Enumerate all 16 paths to the tick-2 native
    # writer, including unaddressed pairs. Each ends in a distinct pair
    # of physical (position, incoming rail) cells, also for the coherent law.
    singles=[physical_label(x+y,order,0)[:2] for x,y in product("RL",repeat=2)]
    require(len(set(singles))==4,"two-tick paths interfere before writer")
    writer=Counter(contact_tag(x==y==0,ra,rb,0)
                   for (x,ra),(y,rb) in product(singles,repeat=2))
    require([writer[k] for k in range(3)]==[12,2,2],"writer-alone probability census")
    return dict(order=order, ticks=3, terminal=[1,"R",1,"R"], entries=entries,
                contact_tick=2,
                contact_tag_rates_per_launch={name:str(Fraction(writer[k],16))
                    for k,name in enumerate(("blank_off_contact","equal","different"))},
                contact_tag_rates_given_both_return={"blank":"0","equal":"1/2","different":"1/2"})


def run():
    orders = (3,4,5,6,7,8,9,12)
    return dict(schema="joint-phase-records-v3",
                panel_columns=["lag_A","lag_B","equal_flag","[sign,gain_A,gain_B] histories"],
                probabilities="Unconditional per double launch. Quadratic pair [a,b] denotes a+b*sqrt(5).",
                short_panels=[short(m) for m in (4,5)],
                exact_ranks=[ranks(m) for m in orders],
                scans=[scan(m,home) for m in orders for home in (0,4*m-1)],
                contact_columns=["lag_A","lag_B","qutrit_1_equal_2_different",
                                 "[sign,gain_A,gain_B] histories at (home+1,R) twice"],
                contact_controls=pointer_controls(),
                contact_scans=[contact_scan(m,home) for m in orders for home in (0,4*m-1)])


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory",type=Path)
    directory=parser.parse_args().directory
    out=directory/"joint_phase_records.json"
    if out.exists():
        parser.exit(2,f"Refusing to overwrite {out}\n")
    result=run()
    directory.mkdir(parents=True,exist_ok=True)
    with out.open("x",encoding="utf8",newline="\n") as f:
        json.dump(result,f,separators=(",",":"),allow_nan=False)
        f.write("\n")
