"""Exact spectral refinement of the temporal optical-circle gain constraint.

Consumes the pinned PR #301 saved interval JSON, not raw observations.
Exit code 0 establishes arithmetic and source-value consistency only.
"""

from fractions import Fraction as F
from hashlib import sha1
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "unequal_circle_gains_output.json"


def require(predicate, explanation):
    if not predicate:
        raise AssertionError(explanation)


def add(z, w):
    return z[0] + w[0], z[1] + w[1]


def minus_i(z):
    return z[1], -z[0]


def dot_conjugate(z, w):
    return z[0]*w[0] + z[1]*w[1], z[0]*w[1] - z[1]*w[0]


def effects(t_max=13, sites=10):
    """For the homogeneous (I - i X)/sqrt(2) coin and R/L unit shifts.

    Each amplitude is an integer Gaussian numerator; the common amplitude
    denominator at step t is 2^(t/2).  Returns all 2x2 position effects.
    """
    states = []
    for input_rail in (0, 1):
        state = [[(0, 0), (0, 0)] for _ in range(sites)]
        state[0][input_rail] = (1, 0)
        states.append(state)
    result = {}
    for t in range(t_max+1):
        for m in range(sites):
            first, second = states[0][m], states[1][m]
            a = sum(dot_conjugate(v,v)[0] for v in first)
            d = sum(dot_conjugate(v,v)[0] for v in second)
            b = (sum(dot_conjugate(first[j],second[j])[k] for j in (0,1))
                 for k in (0,1))
            result[t,m] = (a,tuple(b),d)
        next_states = []
        for state in states:
            nxt = [[(0,0), (0,0)] for _ in range(sites)]
            for pos, (right, left) in enumerate(state):
                nxt[(pos+1)%sites][0] = add(nxt[(pos+1)%sites][0], add(right,minus_i(left)))
                nxt[(pos-1)%sites][1] = add(nxt[(pos-1)%sites][1], add(left,minus_i(right)))
            next_states.append(nxt)
        states = next_states
    return result


def gain_factor(r, bounds, t1=11, t2=13):
    q11 = [[F(v) for v in x] for x in bounds[str(t1)]]
    q13 = [[F(v) for v in x] for x in bounds[str(t2)]]
    common = q11[1][0]/q13[1][1] * r[t2]/r[t1]
    return (common*q13[0][0]/q11[0][1],
            common*q13[2][0]/q11[2][1])


def main():
    raw = SOURCE.read_bytes()
    data = json.loads(raw)
    # A Git blob digest is provenance, not scientific validation.
    blob_id = sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
    require(data["ideal_pair_to_target"]["11"] == "451/281", "changed round-11 orbit ratio")
    require(data["ideal_pair_to_target"]["13"] == "1398/941", "changed round-13 orbit ratio")
    require(data["round_11_and_13_constraints"] ==
            [["97/366","125/732","40139/102846"],
             ["167/732","31/183","10252/57401"]], "changed source constraints")

    E = effects()
    require(E[9,3] == (13,(0,-9),85), "round-nine reference effect")
    require(E[11,3] == (505,(0,351),397), "round-eleven site-five effect")
    require(E[11,7] == (397,(0,-351),505), "round-eleven reflected partner")
    require(E[13,3] == (722,(0,988),2074), "round-thirteen site-five effect")
    require(E[13,7] == (2074,(0,-988),722), "round-thirteen reflected partner")
    require(E[11,5] == (562,(0,0),562), "round-eleven antipode")
    require(E[13,5] == (1882,(0,0),1882), "round-thirteen antipode")
    for t in (11,13):
        a,b,d = E[t,3]
        a2,b2,d2 = E[t,7]
        require(a+a2 == d+d2 and add(b,b2)==(0,0), "reflection orbit scalar")
    p7 = {11:F(281,1024),13:F(941,4096)}
    p59 = {11:F(451,1024),13:F(699,2048)}
    require(p59[11]/p7[11] == F(data["ideal_pair_to_target"]["11"]), "round-11 pair ratio")
    require(p59[13]/p7[13] == F(data["ideal_pair_to_target"]["13"]), "round-13 pair ratio")
    A,B = gain_factor(p7,data["experiment_bands_5_7_9"])
    require((A,B)==(F(13986083,9594464),F(2596219,1545500)), "band or gain coefficient changed")
    require(A < B, "spectral refinement direction")
    # Spectral maximal site-five probability is (451+sqrt(126117))/2048.
    # Both square inequalities are strict integer-rational certificates.
    s_lo, s_hi = F(355129,1000), F(355130,1000)
    require(s_lo*s_lo < 126117 < s_hi*s_hi, "radical bracket")
    def K_of_s(s):
        return (F(451)*(A+B) + (A-B)*s)/699
    k_lower,k_upper = K_of_s(s_hi),K_of_s(s_lo)  # A-B is negative
    old = F(573429403,304842288)
    require(k_lower > old and k_lower > F(191,100), "strict improvement")
    require(k_lower < k_upper < F(192,100), "refined interval")

    # Check sharpness *only* for the three-site, independently chosen-band
    # relaxation. Round 13 can have the needed site-five probability w.
    def W_of_s(s):
        z = (F(451)+s)/2048
        return A*z/K_of_s(s)
    # W(s) is strictly increasing, since derivative numerator is 902*A*B.
    w_lo,w_hi = W_of_s(s_lo), W_of_s(s_hi)
    require(F(3,10) < w_lo < w_hi < F(301,1000), "round-thirteen balance witness")
    # Round 13's exact effect has spectrum (2796±sqrt(5732480))/16384.
    require(F(2394)**2 < 5732480 < F(2395)**2, "round-thirteen spectrum bracket")
    require((F(2796)-F(2394))/16384 < F(3,100), "round-thirteen minimum below witness")
    require((F(2796)+F(2394))/16384 > F(31,100), "round-thirteen maximum above witness")
    # Adverse cases: an unprepared arbitrary input is NOT presumed to obey
    # a single-rail state; the full experimental panel is NOT certified.
    print(json.dumps({
        "source_file": SOURCE.name,
        "source_blob_sha1_provenance": blob_id,
        "round_11_site_5_effect_numerator": [505,[0,351],397],
        "round_11_effect_denominator": 2048,
        "round_11_site_5_spectral_upper_form": "(451+sqrt(126117))/2048",
        "A": str(A), "B": str(B),
        "necessary_max_relative_gain_change": "[451*(A+B)+(A-B)*sqrt(126117)]/699",
        "rigorous_bound_interval": [str(k_lower),str(k_upper)],
        "previous_relaxed_bound": str(old),
        "round_13_site_5_witness_bracket": [str(w_lo),str(w_hi)],
        "logic": "conditional saved figure intervals; three-site relaxation only"
    },indent=2))


if __name__ == "__main__":
    main()
