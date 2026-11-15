"""Exact whole-word power witnesses for the eight nine-tick circuits.
Run python -I -O check_joint_power.py. No saved outputs or dependencies.
"""
from collections import Counter, defaultdict
from fractions import Fraction as Q
from pathlib import Path
from runpy import run_path


BASE = run_path(str(Path(__file__).with_name("generate.py")))
require = BASE["require"]


def power(weights, exponent):
    """Common power, once over the complete output alphabet. Strings denote limits."""
    if exponent in ("+inf", "-inf"):
        extreme = (max if exponent=="+inf" else min)(weights.values())
        scores = {w:int(m==extreme) for w,m in weights.items()}
    else:
        scores = {w:Q(m)**exponent for w,m in weights.items()}
    z = sum(scores.values())
    return {w:Q(m,z) for w,m in scores.items()}


def witnesses(weights, law):
    count = Counter(weights.values())
    masses = defaultdict(Q)
    for word,m in weights.items():
        masses[m] += law[word]
    h = {m:mass/count[m] for m,mass in masses.items()}
    rectangle = h[77]/77 + h[9]/9 - h[33]/33 - h[21]/21
    square = 25*h[1]-10*h[5]+h[25]
    return rectangle, square


def prefix_power(weights,q):
    """Alternative scoring order. Power four ordinary conditional next-address
    chances at each recorded clock; normalize within the observed prefix."""
    mass = {():sum(weights.values())}
    for prefix_word,v in weights.items():
        for k in (1,2,3):
            prefix=prefix_word[:k]
            mass[prefix]=mass.get(prefix,0)+v
    prob = {():Q(1)}
    for _ in range(3):
        nxt={}
        for prefix,w in prob.items():
            children=[prefix+(d,) for d in range(4)]
            denominator=sum(mass[h]**q for h in children)
            for h in children:
                nxt[h]=w*Q(mass[h]**q,denominator)
        prob=nxt
    require(sum(prob.values()) == 1,"conditional normalization")
    return prob


def main():
    laws = BASE["verify"]()
    weights = laws[0, (1,1)]
    require(Counter(weights.values()) ==
            {1:28,5:21,9:3,13:1,17:1,21:4,25:2,29:1,33:1,49:1,77:1},
            "R,S,S multiplicities")
    require(weights[(1,2,3)]==77,"maximum word or clock order")
    children=[(1,2,last) for last in range(4)]
    require([weights[w] for w in children]==[49,29,13,77],"sibling weights")
    keys=[f'{a+4*b+16*c:06b}' for a,b,c in children]
    require(keys==['001001','011001','101001','111001'],"sibling register bit order")
    path=()
    for _ in range(3):
        subtree=[sum(v for w,v in weights.items() if w[:len(path)+1]==path+(i,))
                 for i in range(4)]
        require(subtree.count(max(subtree))==1,"greedy maximum unique")
        path += (subtree.index(max(subtree)),)
        print("Prefix maximum:",path,"child masses:",subtree)
    require(path==(1,2,3) and max(weights.values())==weights[path] and
            list(weights.values()).count(weights[path])==1,"greedy equals global maximum")
    for q in (-2,-1,0,1,2,4,5):
        r,s=witnesses(weights,power(weights,q))
        z=sum(Q(m)**q for m in weights.values())
        expected=Q(9)**(q-1)*(Q(7,3)**(q-1)-1)*(Q(11,3)**(q-1)-1)/z
        require(r==expected and s==(Q(5)**q-5)**2/z, "factorization")
        require(min(r,s)>0 if q!=1 else (r,s)==(0,0), "finite-power strictness")
    require(77*9==33*21 and Q(21,9)==Q(77,33)==Q(7,3) and
            Q(33,9)==Q(77,21)==Q(11,3),"exact bases for every real exponent")
    require(witnesses(weights,power(weights,"+inf"))==(Q(1,77),0),
            "maximum support")
    require(witnesses(weights,power(weights,"-inf"))==(0,Q(25,28)),
            "minimum support")
    require(witnesses(weights,power(weights,0))[1]==Q(1,4),"uniform q=0")

    gaps={}
    for q in (0,1,4,5):
        signed=Q()
        for (_,phases), board in laws.items():
            same,_=BASE["turns"](power(board,q),0,2)
            signed += (-1 if phases[0]==phases[1] else 1)*same/4
        gaps[q]=signed
    require(gaps=={0:Q(),1:Q(1,8),4:Q(142669510080,871237026361),
                   5:Q(72526324761481,670822171549928)},"lag-two phase gaps")
    mix=(gaps[1]-gaps[5])/(gaps[4]-gaps[5])
    require(0<mix<1 and mix*gaps[4]+(1-mix)*gaps[5]==gaps[1],"camouflage mixture")
    print("Opposite-minus-equal endpoint phase contrast at q=4,5:",gaps[4],gaps[5])
    print("Mixing weight on q=4 to reproduce ordinary 1/8:",mix)
    print("R,S,S rectangle and square at q=0 and the two infinite limits:")
    for q in (0,"+inf","-inf"):
        print(q,*witnesses(weights,power(weights,q)))
    require(prefix_power(weights,1)==power(weights,1),"ordinary conditioning")
    nested=prefix_power(weights,2)
    # Two words with identical ideal mass can receive unequal probabilities
    # when the output is scored at each read rather than after all nine ticks.
    pair=next((a,b) for a in weights for b in weights if
              weights[a]==weights[b] and nested[a]!=nested[b])
    a,b=pair
    require(power(weights,2)[a]==power(weights,2)[b],"whole-word symmetry")
    print("Conditional q=2 distinguishes equal-mass chronological words",
          a,b,"with probabilities",nested[a],nested[b])


if __name__=="__main__":
    main()
