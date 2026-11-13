#!/usr/bin/env python3
"""Exact finite certificates accompanying Observation, Memory, Control, and Time.

This newly written program uses no archived-source imports. It checks concrete
identities and finite decision problems; the manuscript proofs carry statements
over arbitrary dimensions, histories, sample sizes, and real parameters.
Run with Python 3 and SymPy. Output is JSON on stdout.
"""
from fractions import Fraction as F
from itertools import product
from math import comb
import json
import sympy as sp

checks = []
results = {}


def require(condition, name):
    if not bool(condition):
        raise ArithmeticError(name)
    checks.append(name)


def describe(value):
    return {"exact": str(value), "decimal_summary": float(value)}


def optimal_test(null, alternative, alpha=F(1, 20)):
    """Solve the finite randomized Neyman--Pearson problem by ratio ordering."""
    require(sum(null) == sum(alternative) == 1, "test probabilities normalized")
    order = sorted(range(len(null)), key=lambda i: alternative[i] / null[i],
                   reverse=True)
    size = F(0)
    power = F(0)
    accepted = []
    for k in order:
        if size + null[k] >= alpha:
            gamma = (alpha - size) / null[k]
            return {"power": power + gamma * alternative[k],
                    "boundary": k, "gamma": gamma, "full": accepted,
                    "order": order}
        size += null[k]
        power += alternative[k]
        accepted.append(k)
    raise ArithmeticError("positive null has insufficient probability mass")


def binomial(n, p):
    return [F(comb(n, k)) * p**k * (1-p)**(n-k) for k in range(n+1)]


def noisy_counts(L, eta, epsilon, horizon):
    """Integer forward recursion on detector history and even-parity count."""
    en, ed = epsilon.numerator, epsilon.denominator
    even = (1+eta)/2
    pn, pd = even.numerator, even.denominator
    states = list(product((0, 1), repeat=L))
    mass = {h: [en**sum(h)*(ed-en)**(L-sum(h))] for h in states}
    denominator = ed**L
    for m in range(1, horizon+1):
        new = {h: [0]*(m+1) for h in states}
        for h in states:
            for bit in (0, 1):
                destination = h[1:] + (bit,)
                noise_weight = en if bit else ed-en
                even_weight = pn if (sum(h)+bit) % 2 == 0 else pd-pn
                for count, weight in enumerate(mass[h]):
                    new[destination][count+1] += weight*noise_weight*even_weight
                    new[destination][count] += weight*noise_weight*(pd-even_weight)
        denominator *= ed*pd
        mass = new
        values = [F(sum(mass[h][k] for h in states), denominator)
                  for k in range(m+1)]
        yield m, values


def innovation_law(L, eta, epsilon, m):
    """Direct finite summation, independent of the count recursion."""
    out = {w: F(0) for w in product((0, 1), repeat=m)}
    even = (1+eta)/2
    for source in product((0, 1), repeat=m):
        source_p = even**(m-sum(source))*(1-even)**sum(source)
        for noise in product((0, 1), repeat=L+m):
            noise_p = epsilon**sum(noise)*(1-epsilon)**(L+m-sum(noise))
            word = tuple(source[t] ^ (sum(noise[t:t+L+1]) % 2)
                         for t in range(m))
            out[word] += source_p*noise_p
    return out


ideal = {}
for m in (39, 40):
    ideal[m] = optimal_test(binomial(m, F(1, 2)), binomial(m, F(3, 4)))
require(ideal[39]["power"] < F(19, 20) < ideal[40]["power"],
        "ideal randomized testing boundary 39/40")
require(ideal[40]["boundary"] == 25
        and ideal[40]["gamma"] == F(4423136507, 16760560440),
        "ideal 40-innovation randomization")
require(sum(binomial(42, F(1, 2))[27:]) < F(1, 20)
        and sum(binomial(42, F(3, 4))[27:]) > F(19, 20),
        "ideal nonrandomized 42-innovation sufficient rule")
results["ideal_testing"] = {
    str(m): {"power": describe(v["power"]), "boundary": v["boundary"],
             "gamma": str(v["gamma"])} for m, v in ideal.items()}

eta, epsilon, L = F(1, 2), F(1, 10), 2
law = innovation_law(L, eta, epsilon, 3)
require(law[(0, 0, 1)] == F(681, 5000)
        and law[(0, 1, 0)] == F(609, 5000), "count is not sufficient")
selected = {}
failed_horizons = []
for m, probabilities in noisy_counts(L, eta, epsilon, 188):
    if m == 3:
        require(probabilities == [
            sum(p for w, p in law.items() if m-sum(w) == k)
            for k in range(m+1)], "count recursion versus direct summation")
    decision = optimal_test(binomial(m, F(1, 2)), probabilities)
    if m < 183:
        require(decision["power"] < F(19, 20),
                "noisy count-only lower horizon %d" % m)
        failed_horizons.append(m)
    if m in (40, 182, 183, 188):
        selected[m] = (probabilities, decision)
require(selected[183][1]["power"] > F(19, 20),
        "noisy count-only horizon 183 succeeds")
p183 = selected[183][0]
simple_size = sum(binomial(183, F(1, 2))[104:]) + F(43, 50)*binomial(183, F(1, 2))[103]
simple_power = sum(p183[104:]) + F(43, 50)*p183[103]
require(simple_size < F(1, 20) and simple_power > F(19, 20),
        "noisy rational 43/50 decision succeeds")
require(sum(binomial(188, F(1, 2))[106:]) < F(1, 20)
        and sum(selected[188][0][106:]) > F(19, 20),
        "noisy nonrandomized 188-innovation sufficient rule")
p40 = selected[40][0]
mean40 = sum(F(k)*p for k, p in enumerate(p40))
var40 = sum(F(k*k)*p for k, p in enumerate(p40)) - mean40**2
require(mean40 == F(628, 25) and var40 == F(185736, 15625),
        "noisy overlapping-innovation mean and variance")
results["noisy_count_testing"] = {
    "smaller_horizons_checked": failed_horizons,
    "selected": {str(m): {"power": describe(v[1]["power"]),
                         "boundary": v[1]["boundary"],
                         "gamma": str(v[1]["gamma"])} for m, v in selected.items()},
    "simple_183_size": describe(simple_size),
    "simple_183_power": describe(simple_power),
    "mean40": str(mean40), "variance40": str(var40)}

# The sequential certificate has one fixed alternative, not a uniform horizon.
require(157**383 * 93**267 < 4800 * 125**650
        <= 157**384 * 93**266, "sequential parity likelihood boundary 384")
miss = sum(binomial(650, F(157, 250))[:384]) + F(1, 40)
require(miss < F(1, 20), "1950-output sufficient power certificate")
results["sequential_1950"] = {"miss_upper_bound": describe(miss),
                             "power_lower_bound": describe(1-miss)}
require(65**13 * 35**7 < 53**20, "normalized factor negative log growth")
require(13**13 * 7**7 > 12**13 * 8**7, "clipped factor positive log growth")

# Exact noisy block law by independent readout convolution.
words = list(product((0, 1), repeat=4))
source4 = {}
for w in words:
    source4[w] = F(1, 4)
    for t in range(2):
        source4[w] *= (1+eta*(-1)**sum(w[t:t+3]))/2
observed4 = {}
for out in words:
    observed4[out] = sum(p*epsilon**sum(x != y for x, y in zip(w, out))
                         *(1-epsilon)**sum(x == y for x, y in zip(w, out))
                         for w, p in source4.items())
blocks = list(product((0, 1), repeat=2))
H = sp.Matrix([[sp.Rational(observed4[x+y].numerator,
                            observed4[x+y].denominator)
                for y in blocks] for x in blocks])
expected_H = sp.Matrix([[209, 105, 81, 105], [81, 105, 209, 105],
                       [105, 81, 105, 209], [105, 209, 105, 81]])/2000
require(H == expected_H, "noisy block matrix by full-word convolution")
require((H*H.T).eigenvals() ==
        {sp.Rational(1, 16): 1, sp.Rational(64, 15625): 2,
         sp.Rational(1, 625): 1}, "exact noisy singular spectrum")
require(sum(abs(v-sp.Rational(1, 16)) for v in H)/2 == sp.Rational(21, 125),
        "matched-marginal rank-one total variation")
tails = {1: F(153, 15625), 2: F(89, 15625), 3: F(1, 625)}

def log_interval_from_atanh(x, terms=50):
    lower = 2*sum(x**(2*j+1)/F(2*j+1) for j in range(terms))
    remainder = 2*x**(2*terms+1)/(F(2*terms+1)*(1-x*x))
    return lower, lower+remainder

l2, u2 = log_interval_from_atanh(F(1, 3))
l5, u5 = log_interval_from_atanh(F(2, 3))
lo, hi = 2*l2+l5, 2*u2+u5
require(F(2995732, 10**6) < lo < hi < F(2995733, 10**6),
        "rational enclosure of log 20")
require(F(968245, 10**6)**2 < F(15, 16) < F(968246, 10**6)**2,
        "rational square-root enclosure one")
require(F(1730818, 10**6)**2 < lo and hi < F(1730819, 10**6)**2,
        "rational square-root enclosure two")
clo, chi = F(2699063, 10**6), F(2699065, 10**6)
budgets = {1: 2976, 2: 5116, 3: 18213}
for D, n in budgets.items():
    require(4*chi**2 < n*tails[D] and 4*clo**2 >= (n-1)*tails[D],
            "first integer for sufficient rank bound D=%d" % D)
results["rank"] = {"matrix": [[str(v) for v in row] for row in H.tolist()],
                   "squared_tails": {str(k): str(v) for k, v in tails.items()},
                   "sufficient_iid_record_budgets": budgets,
                   "outputs_per_record": 4}

# Positive Mealy realization, exact controls, and calibration path.
p = [F(3, 5), F(3, 20), F(1, 5), F(1, 20)]
pp = [F(3, 20), F(3, 5), F(1, 5), F(1, 20)]
require((p[0]+p[1], p[2]+p[3]) ==
        (pp[0]+pp[1], pp[2]+pp[3]) == (F(3, 4), F(1, 4)),
        "full-support fine laws have the same coarse input")
require(abs((p[0]+p[2])-(pp[0]+pp[2])) == F(9, 20),
        "full-support coarse permutation contrast 9/20")
T0 = sp.Matrix([[6, 2], [1, 3]])/20
T1 = sp.Matrix([[4, 8], [7, 9]])/20
pi = sp.Matrix([[sp.Rational(4, 9), sp.Rational(5, 9)]])
one = sp.ones(2, 1)
S = sp.Matrix([[9, 1], [2, 8]])/10
B0, B1, pib = S.inv()*T0*S, S.inv()*T1*S, pi*S
require(B0 == sp.Matrix([[449, 151], [19, 181]])/1400
        and B1 == sp.Matrix([[67, 93], [125, 115]])/280,
        "positive similarity pair")
J = sp.Matrix([[(pi*X*Y*one)[0] for Y in (T0, T1)] for X in (T0, T1)])
require(J == sp.Matrix([[81, 179], [179, 461]])/900
        and J.det() == sp.Rational(53, 8100), "passive rank-two witness")
a, b, t = sp.symbols("a b t", real=True)
K = sp.Matrix([[1-a, a], [b, 1-b]])
gap = sp.factor((pi*K*T0*one-pib*K*B0*one)[0])
require(sp.simplify(gap-(2*a-b)/35) == 0, "exact fixed-control contrast")
R2 = sp.Matrix([[0, 1], [0, 1]])
U = sp.Matrix([[sp.Rational(9, 10), sp.Rational(1, 10)], [0, 1]])
require(U*R2 == R2*U == R2, "second reset-preserving similarity")
require(S.inv()*R2*S == sp.Matrix([[sp.Rational(1, 5), sp.Rational(4, 5)]]*2),
        "sharp 20 percent reset-nuisance witness")
K1 = sp.Matrix([[sp.Rational(3, 4), sp.Rational(1, 4)],
                [sp.Rational(1, 2), sp.Rational(1, 2)]])
K2 = sp.Matrix([[sp.Rational(1, 2), sp.Rational(1, 2)],
                [sp.Rational(1, 4), sp.Rational(3, 4)]])
St = sp.Matrix([[1-t, t], [2*t, 1-2*t]])
require(sp.simplify(St.inv()*K1*St-K1) == sp.zeros(2),
        "calibration path keeps first control fixed")
require(sp.simplify(St.inv()*K2*St-K2)
        == sp.Matrix([[3*t/4, -3*t/4]]*2), "calibration path error")
path_numerators = []
for Ty in (T0, T1):
    path_numerators += [sp.factor(v*20*(1-3*t)) for v in St.inv()*Ty*St]
require(all(sp.expand(x-y) == 0 for x, y in zip(path_numerators,
        [6-15*t-t*t, 2-5*t+t*t, 1-8*t-t*t, 3-12*t+t*t,
         4-3*t-35*t*t, 8-37*t+35*t*t, 7-4*t-35*t*t, 9-36*t+35*t*t])),
        "all eight calibration-path numerators")
require(sp.expand((pi*St)[0]) == sp.Rational(4, 9)+2*t/3,
        "latent preparation interval coordinate")
q = (pi*T0*one)[0]
qs = [(pi*control*T0*one)[0] for control in (K1, K2)]
design = sp.Matrix([[sp.Rational(1, 2), -sp.Rational(3, 4)],
                    [sp.Rational(1, 4), -sp.Rational(3, 4)]])
d, k = design.inv()*sp.Matrix([v-q for v in qs])
require((d, k) == (sp.Rational(1, 5), sp.Rational(4, 45)),
        "two-control reconstruction of contrast and preparation")
AA = sp.Matrix.vstack(pi, pi*K1)
FF = sp.Matrix.hstack(one, T0*one)
for Ty in (T0, T1):
    CY = sp.Matrix([[(pi*Ty*one)[0], (pi*Ty*T0*one)[0]],
                    [(pi*K1*Ty*one)[0], (pi*K1*Ty*T0*one)[0]]])
    require(AA.inv()*CY*FF.inv() == Ty, "short controlled-word reconstruction")

reset_tests = {}
for n in (467, 468):
    decision = optimal_test(binomial(n, F(1, 7)), binomial(n, F(1, 5)))
    reset_tests[n] = decision
require(reset_tests[467]["power"] < F(19, 20) < reset_tests[468]["power"],
        "exact reset-trial boundary 467/468")
results["reset_testing"] = {
    str(n): {"power": describe(v["power"]), "boundary": v["boundary"],
             "gamma": str(v["gamma"])} for n, v in reset_tests.items()}
results["controls"] = {"next_output_gap": str(gap),
                       "calibration_numerators": [str(x) for x in path_numerators],
                       "calibration_epsilon_001_interval": ["4/9", "34/75"]}

# Quantum fragment product versus common-CZ branches.
E = sp.Matrix([9, 12, 12, 16])/25
Fbranch = sp.Matrix([9, 12, 12, -16])/25
def first_fragment_density(v):
    return sp.Matrix(2, 2, lambda i, j:
                     sum(v[2*i+k]*v[2*j+k] for k in (0, 1)))
rhoE, rhoF = first_fragment_density(E), first_fragment_density(Fbranch)
require((E.T*E)[0] == (Fbranch.T*Fbranch)[0] == 1,
        "fragment branches normalized")
require(sp.Matrix(2, 2, list(E)).det() == 0
        and sp.Matrix(2, 2, list(Fbranch)).det() == -sp.Rational(288, 625),
        "quantum tensor-factorization witness")
pE = sp.Rational(1, 2)+rhoE[0, 1]
pF = sp.Rational(1, 2)+rhoF[0, 1]
require(pE == sp.Rational(49, 50) and pF == sp.Rational(457, 1250)
        and pE-pF == sp.Rational(384, 625), "environmental X readout")

# Continuous-generator formulas reduce to these exact algebraic identities.
C = sp.Matrix([[0, 1, 0], [0, 0, 1], [1, 0, 0]])
Pi = sp.ones(3)/3
R = sp.eye(3)-Pi
A = C-C*C
require(A*A == -3*R and A*Pi == Pi*A == sp.zeros(3)
        and R*A == A*R == A, "generator invariant-subspace algebra")
c = sp.symbols("c", real=True)
Q = -12*R + c*A
require(Q*sp.ones(3, 1) == sp.zeros(3, 1)
        and sp.ones(1, 3)*Q == sp.zeros(1, 3), "generator stationary rows")
lam = sp.symbols("lambda")
require(sp.expand(Q.charpoly(lam).as_expr()
        - lam*(lam**2+24*lam+144+3*c*c)) == 0, "generator characteristic polynomial")
require(4-sp.Rational(2)*sp.Rational(22, 7)/sp.sqrt(3) > 0,
        "strictly positive off-diagonal rates for c=2pi/sqrt3")
results["records_and_generators"] = {
    "environmental_X_gap": "384/625",
    "quarter_time_contrast": "2*exp(-3)/sqrt(3)",
    "quarter_time_decimal_summary": float(2*sp.exp(-3)/sp.sqrt(3))}

print(json.dumps({"status": "PASS", "finite_check_count": len(checks),
                  "scope": "Exact finite certificates; unrestricted claims use manuscript proofs.",
                  "archived_programs_executed": False,
                  "checks": checks, "results": results}, indent=2))
