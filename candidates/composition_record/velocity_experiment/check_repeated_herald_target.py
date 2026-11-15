"""Exact stopped histories for a herald measured repeatedly toward a scratch target.

    python -I -B -O check_repeated_herald_target.py

The two scratch trials have a product preparation with common success mass
s. The fresh science input and fair bit are independent of those trials in
this circuit model. On disagreement use the fair bit; on agreement keep
the common scratch label. A timeout publishes the actual science outcome.
Timing, private scratch results and the cap flag are omitted from the
legacy single-bit output but included in the checks. No empirical counts.
"""

from collections import defaultdict
from fractions import Fraction as F
from itertools import product


def require(ok, reason):
    if not ok:
        raise ArithmeticError(reason)


def weight(s, state):
    x, y = state
    return (1-s)*x*x+s*y*y


def reflect(s, state):
    # In the unnormalized orthogonal directions v0=Pi0 W|psi> and
    # v1=Pi1 W|psi>, the Gram is diag(1-s,s). Assuming the same
    # isoclinic herald W on all data inputs, reflected amplitudes are
    # (2 W B W†-I)(x v0+y v1), where B is the blank-ancilla projector.
    x, y = state
    overlap = (1-s)*x+s*y
    result = (2*overlap-x, 2*overlap-y)
    require(weight(s,result) == weight(s,state), "reflection norm")
    return result


def science_histories(s, target, cap):
    finished = {}
    def measure(before, history):
        # Retain the unnormalized coefficient with its sign. No fresh
        # per-round draw with prescribed flip probability enters this replay.
        for actual, after in enumerate(((before[0],F(0)), (F(0),before[1]))):
            record = history+(actual,)
            reflections = len(record)-1
            if actual == target or reflections == cap:
                finished[record] = weight(s,after)
            else:
                measure(reflect(s,after), record)
    measure((F(1),F(1)), ())
    require(sum(finished.values()) == 1, "actual science histories complete")
    return finished


def scratch_outcomes(s):
    # Do not start by stipulating the mode weights. Resolve all four
    # ordered, singly measured scratch outputs before constructing them.
    scratch = {}
    one = (1-s,s)
    for a,b in product(range(2), repeat=2):
        target = (int(a == 0),int(a == 1)) if a == b else (F(1,2),F(1,2))
        scratch[a,b] = (one[a]*one[b], target)
    return scratch


def replay(s, cap):
    scratch = scratch_outcomes(s)
    science = [science_histories(s,t,cap) for t in (0,1)]
    group_prob, group_target, group_final = (defaultdict(F) for _ in range(3))
    mismatch = reflections = F(0)
    raw_final = [F(0),F(0)]
    used = [F(0)]*(cap+1)
    for (a,b), (prep, targets) in scratch.items():
        group = "agreement" if a == b else "disagreement"
        group_prob[group] += prep
        group_target[group] += prep*targets[1]
        for target, target_prob in enumerate(targets):
            for history, science_mass in science[target].items():
                joint = prep*target_prob*science_mass
                n = len(history)-1
                final = history[-1]
                raw_final[final] += joint
                used[n] += joint
                group_final[group] += joint*final
                mismatch += joint*(final != target)
                reflections += joint*n
    D = s*s+(1-s)**2
    tau = 4*s*(1-s)
    residual = 1-tau
    require(dict(group_prob) == {"agreement": D,"disagreement": 1-D}, "raw scratch parity")
    require(group_target["agreement"]/D == s*s/D, "agreement target, binary power 2")
    if 1-D:
        require(group_target["disagreement"]/(1-D) == F(1,2), "disagreement target, power 0")
    for group, p in group_prob.items():
        require(group_final[group] == (1-residual**cap)*group_target[group] +
                residual**cap*p*s, "capped conditional return")
    require(raw_final == [1-s,s], "unconditional published label")
    require(mismatch == tau/2*residual**cap, "cap timeout publishes the observed label")
    require(sum(used) == 1 and reflections == (1-residual**cap)/2, "capped mean")
    for j in range(1,cap+1):
        require(sum(used[j:]) == tau/2*residual**(j-1), "tail-sum identity")
    require(reflections == sum(j*m for j,m in enumerate(used)), "reflection-count probabilities")
    return group_prob, group_final, mismatch, reflections


def check_pairs(s, cap, weights, hits):
    # Fresh modes: independent scratch and science each launch. Held-mode
    # comparison: draw ONE agreement/disagreement class; generate a new
    # target independently WITHIN THAT CLASS for each independent science
    # launch. Reusing a full raw scratch pair or its chosen bit is a
    # different experiment and yields different joint hit probabilities.
    groups = [(p,hits[g]/p) for g,p in weights.items() if p]
    held = sum(p*v*v for p,v in groups)
    fresh = sum(p*r*v*w for p,v in groups for r,w in groups)
    residual = (1-2*s)**2
    D = s*s+(1-s)**2
    variance = s*(1-s)*residual/(2*D)
    require(fresh == s*s and held-fresh == (1-residual**cap)**2*variance,
            "held parity versus fresh paired coincidence")
    return held-fresh


if __name__ == "__main__":
    for s in map(F, ("0","1/64","1/5","5/16","1/2","11/16","4/5","63/64","1")):
        for cap in (0,1,2,5,9):
            groups, hits, timeout, mean = replay(s,cap)
            excess = check_pairs(s,cap,groups,hits)
            if s == F(5,16) and cap in (1,2):
                print(f"s={s}, cap={cap}, scratch P(disagreement,agreement)="
                      f"({groups['disagreement']},{groups['agreement']}), "
                      f"actual hit given these classes=({hits['disagreement']/groups['disagreement']},"
                      f"{hits['agreement']/groups['agreement']}), "
                      f"timeout={timeout}, mean reflections={mean}, held-pair excess={excess}")
    print("Verified all four scratch outcomes, full stopped science histories, original launch "
          "probabilities, actual timeout labels, and fresh/held moments for 45 fixtures.")
