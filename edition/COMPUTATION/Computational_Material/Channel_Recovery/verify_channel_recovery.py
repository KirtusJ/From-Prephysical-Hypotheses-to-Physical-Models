#!/usr/bin/env python3
"""Transparent finite checks for Stochastic Recovery and Capacity Equality.

New implementation for this study. No archived program is imported or executed.
Fraction identities are exact. Logarithmic evaluations use 80-digit mpmath
arithmetic and are explicitly numerical checks, not certified enclosures.
Universal conclusions are proved in channel_recovery_body.tex.
"""
from fractions import Fraction as F
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import platform
import mpmath as mp

mp.mp.dps = 80
HERE = Path(__file__).resolve().parent
checks = []


def plain(x):
    if isinstance(x, F):
        return str(x)
    if isinstance(x, (list, tuple)):
        return [plain(v) for v in x]
    if isinstance(x, dict):
        return {k: plain(v) for k, v in x.items()}
    return x


def check(name, condition, details=None, kind="exact rational check"):
    if not condition:
        raise AssertionError(name)
    checks.append({"name": name, "passed": True, "kind": kind,
                   "details": plain(details)})


def matrix(rows):
    return [[F(x) for x in row] for row in rows]


def mul(a, b):
    return [[sum((a[i][k]*b[k][j] for k in range(len(b))), F(0))
             for j in range(len(b[0]))] for i in range(len(a))]


def stochastic(a):
    return all(all(x >= 0 for x in row) and sum(row) == 1 for row in a)


def tv(a, b):
    return sum((abs(x-y) for x, y in zip(a, b)), F(0))/2


def m(x):
    return mp.mpf(x.numerator)/x.denominator if isinstance(x, F) else mp.mpf(x)


def entropy(p):
    return -sum((m(x)*mp.log(m(x), 2) for x in p if x), mp.mpf(0))


def divergence(p, q):
    assert all(y > 0 for x, y in zip(p, q) if x)
    return sum((m(x)*mp.log(m(x)/m(y), 2)
                for x, y in zip(p, q) if x), mp.mpf(0))


def mutual(p, w):
    return entropy(mul([p], w)[0])-sum(
        (m(px)*entropy(row) for px, row in zip(p, w)), mp.mpf(0))


def reverse(p, w, k):
    mu = mul([p], w)[0]
    nu = mul([mu], k)[0]
    return [[mu[y]*k[y][v]/nu[v] if nu[v] else F(1, len(mu))
             for y in range(len(mu))] for v in range(len(nu))]


def average(a, b):
    return [(x+y)/2 for x, y in zip(a, b)]


W = matrix([[F(1,2), F(1,2), 0, 0],
            [0, 0, F(1,2), F(1,2)],
            [F(1,2), 0, F(1,2), 0]])
K = matrix([[1,0], [1,0], [0,1], [0,1]])
Q = mul(W, K)
Lstar = matrix([[F(3,4), F(1,4), 0, 0],
               [0, 0, F(3,4), F(1,4)]])
Rstar = mul(Q, Lstar)
check("three-input channel and merger are stochastic", stochastic(W) and stochastic(K))
check("coarse rows", Q == matrix([[1,0], [0,1], [F(1,2), F(1,2)]]), Q)
check("candidate minimax recovery is stochastic", stochastic(Lstar), Lstar)
errors = [tv(a,b) for a,b in zip(W,Rstar)]
check("all three attained recovery errors are one quarter", errors == [F(1,4)]*3, errors)
gap = tv(W[2], average(W[0], W[1]))
check("convex-relation obstruction is one half", gap == F(1,2),
      {"gap":gap, "lower_bound_gap_over_two":gap/2,
       "proof_role":"Triangle inequality and convexity in the manuscript give the universal lower bound."})
check("coarse third row is average of first two", Q[2] == average(Q[0], Q[1]))
anchored = mul(Q, W[:2])
check("exact reconstruction of first two rows leaves third error one half",
      [tv(a,b) for a,b in zip(W, anchored)] == [0,0,F(1,2)])
for rho in [F(0), F(1,10), F(1,4), F(1,2)]:
    lr = matrix([[F(1,2)+rho,F(1,2)-rho,0,0],
                 [0,0,F(1,2)+rho,F(1,2)-rho]])
    er = [tv(a,b) for a,b in zip(W,mul(Q,lr))]
    check("attained anchor tradeoff at rho="+str(rho),
          stochastic(lr) and er == [rho,rho,F(1,2)-rho], er)
check("original capacity is attained by first two equally", mul([[F(1,2),F(1,2),0]],W)[0] == [F(1,4)]*4)
check("all original rows have two equiprobable entries", all(sorted(row)==[0,0,F(1,2),F(1,2)] for row in W))

# A full-support optimizer of the original channel alone is insufficient.
W4 = W + [matrix([[0,F(1,2),0,F(1,2)]])[0]]
Q4 = mul(W4,K)
u4 = [F(1,4)]*4
check("four-input full-support optimizer has uniform original output", mul([u4],W4)[0]==u4)
check("four-input third and fourth coarse rows coincide but original rows differ",
      Q4[2]==Q4[3] and W4[2]!=W4[3])
check("four-input uniform-prior information values", abs(mutual(u4,W4)-1)<mp.mpf('1e-70') and abs(mutual(u4,Q4)-mp.mpf('0.5'))<mp.mpf('1e-70'),
      {"original_bits":mp.nstr(mutual(u4,W4),45), "coarse_bits":mp.nstr(mutual(u4,Q4),45)},
      "80-digit logarithmic check; capacity proof is analytic")
eta = F(1,2)
Wp = [[(1-eta)*z+eta*F(1,4) for z in row] for row in W4]
Qp = mul(Wp,K)
check("strictly positive original-optimizer counterexample", stochastic(Wp) and all(z>0 for row in Wp for z in row))
check("positive counterexample has equal row-entropy patterns and uniform average",
      all(sorted(row)==[F(1,8),F(1,8),F(3,8),F(3,8)] for row in Wp)
      and mul([u4],Wp)[0]==u4)
check("positive coarse first two rows are a binary symmetric channel",
      Qp[:2]==matrix([[F(3,4),F(1,4)],[F(1,4),F(3,4)]]))
check("positive counterexample still cannot recover its distinct equal-coarse rows",
      Qp[2]==Qp[3] and Wp[2]!=Wp[3])
check("positive four-row exact minimax witness", [tv(a,b) for a,b in zip(Wp,mul(Qp,W[:2]))] == [0,0,F(1,4),F(1,4)],
      {"separation_lower_bound":tv(Wp[2],Wp[3])/2})

# A valid sufficient statistic supplies the positive control.
goodL = matrix([[F(3,5),F(2,5),0,0],[0,0,F(3,10),F(7,10)]])
goodW = mul(Q,goodL)
probe = [F(1,5),F(3,10),F(1,2)]
goodReverse = reverse(probe,goodW,K)
check("recoverable positive control", goodReverse==goodL and mul(mul(goodW,K),goodReverse)==goodW)

# The rare-probe family keeps the experiment fixed while its probe changes.
rare = []
for eps in [F(1,3),F(1,10),F(1,100),F(1,10000),F(1,100000000)]:
    p = [(1-eps)/2,(1-eps)/2,eps]
    lp = reverse(p,W,K)
    expected = matrix([[(1+eps)/2,(1-eps)/2,0,0],
                       [0,0,(1+eps)/2,(1-eps)/2]])
    er = [tv(a,b) for a,b in zip(W,mul(Q,lp))]
    check("rare-probe reverse and row errors at eps="+str(eps),
          lp==expected and er==[eps/2,eps/2,(1-eps)/2])
    delta = mutual(p,W)-mutual(p,Q)
    formula = entropy([(1+eps)/2,(1-eps)/2])-1+m(eps)
    check("rare-probe loss identity at eps="+str(eps), abs(delta-formula)<mp.mpf('1e-70') and delta>0 and delta<m(eps),
          kind="80-digit logarithmic check; formula and 0<loss<eps proved analytically")
    rare.append({"epsilon":str(eps),"loss_bits":mp.nstr(delta,50),
                 "bayesian_row_errors":plain(er),"minimax_error":"1/4"})

# General stochastic postprocessing: check the exact joint construction and
# numerical KL identity/inequality at one nontrivial rational instance.
wg = matrix([[F(1,3),F(2,3)],[F(3,4),F(1,4)]])
kg = matrix([[F(3,4),F(1,4)],[F(1,5),F(4,5)]])
pg = [F(2,5),F(3,5)]
qg = mul(wg,kg)
lg = reverse(pg,wg,kg)
rg = mul(qg,lg)
true_joint = [pg[x]*wg[x][y]*kg[y][v] for x in range(2) for y in range(2) for v in range(2)]
markov_joint = [pg[x]*qg[x][v]*lg[v][y] for x in range(2) for y in range(2) for v in range(2)]
check("general stochastic reference joint is a law", sum(true_joint)==sum(markov_joint)==1 and stochastic(lg))
for x in range(2):
    for y in range(2):
        marginal = sum((pg[x]*qg[x][v]*lg[v][y] for v in range(2)),F(0))
        check(f"recovered marginal identity x={x},y={y}",marginal==pg[x]*rg[x][y])
delta = mutual(pg,wg)-mutual(pg,qg)
djoint = divergence(true_joint,markov_joint)
drows = sum((m(pg[x])*divergence(wg[x],rg[x]) for x in range(2)),mp.mpf(0))
tv2 = sum((m(pg[x])*m(tv(wg[x],rg[x]))**2 for x in range(2)),mp.mpf(0))
check("general stochastic KL-loss identity and marginal inequality",
      abs(delta-djoint)<mp.mpf('1e-70') and drows<=delta,
      {"loss_bits":mp.nstr(delta,50),"joint_KL_bits":mp.nstr(djoint,50),"weighted_row_KL_bits":mp.nstr(drows,50)},
      "80-digit logarithmic check, not a universal or interval certificate")
check("general stochastic weighted Pinsker bound", tv2<=mp.log(2)*delta/2,
      {"weighted_squared_TV":mp.nstr(tv2,50),"bound":mp.nstr(mp.log(2)*delta/2,50)},
      "80-digit numerical check of a proved inequality")

# An unused coarse label has no effect, even though its reverse row is arbitrary.
k_unused = [row+[F(0)] for row in K]
l_unused = reverse(probe,goodW,k_unused)
check("zero-output-mass reverse row is harmless", stochastic(l_unused) and mul(mul(goodW,k_unused),l_unused)==goodW)

report = {
    "study":"Stochastic Recovery from Information Loss and Equality of Channel Capacity",
    "timestamp":datetime.now(timezone.utc).isoformat(),
    "timestamp_convention":"UTC execution timestamp",
    "implementation":"New transparent implementation; no archived code executed",
    "environment":{"python":platform.python_version(),"mpmath":mp.__version__,"decimal_digits":mp.mp.dps},
    "script_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "checks":checks,
    "counts":{"total":len(checks),"exact_rational":sum(c['kind']=='exact rational check' for c in checks),
              "numerical":sum(c['kind']!='exact rational check' for c in checks)},
    "rare_probe_examples":rare,
    "all_passed":True,
    "scope_limits":["No proof assistant was used.","No physical observations or calibrated apparatus were assessed.",
                    "Finite checks corroborate displayed algebra only; the manuscript supplies universal proofs.",
                    "High-precision logarithms are approximate checks, not certified interval enclosures.",
                    "Same model lineage and common source exposure; no independent replication claim."]
}
target=HERE/'Channel_Recovery_Checks.json'
target.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({"report":str(target),"sha256":hashlib.sha256(target.read_bytes()).hexdigest(),
                  "counts":report['counts'],"all_passed":True},indent=2))
