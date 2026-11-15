"""Probe (no predicate; exploratory, double precision, kept as such). Question: is gap(T)*T - (1/2)log2 T constant, and does
the constant match the Stirling term  c* + (1/2) E[log2(pi (1-v^2)/2)]  under the recalled limiting law?
Inputs: result_dial_run1.json (this folder; T = 300, 600, 1200) and the director's published gap(2400) = 0.002683 (WHY_ABANDONED.md).
Usage: python3 kappa_probe.py OUT.json (refuses to overwrite)."""
import json, math, sys
N = 4000; k = math.pi * math.sqrt(2); c = 0.7715533031636120
s = 0.0
for j in range(N):
    t = -math.pi/2 + 2*math.pi*j/N; v2 = math.sin(t)**2/2
    s += 0.5*math.log2(math.pi*(1-v2)/2)/(1-v2)
stir = c + s*(2*math.pi/N)/2/k
r = json.load(open("result_dial_run1.json"))["report"]["rates"]
obs = {T: (c - float(r[str(T)]))*T - 0.5*math.log2(T) for T in (300, 600, 1200)}
obs[2400] = 0.002683*2400 - 0.5*math.log2(2400)
out = {"argv": sys.argv, "gapT_minus_half_log2T": obs, "stirling_constant": stir}
json.dump(out, open(sys.argv[1], "x"), indent=1); print(out)
