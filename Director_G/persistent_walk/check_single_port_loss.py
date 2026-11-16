"""Integer enclosure for all settings under independent loss per physical tick."""
from pathlib import Path
from runpy import run_path
from fractions import Fraction as Q
import json
D = Path(__file__).resolve().parent
code = run_path(str(D / 'check_single_port_timing.py'))


def main():
    """Bracket the first loss rates at which the two prespecified rules lose 95% power."""
    rates = list(map(Q, ('0', '0.0000000001876', '0.0000000001877', '0.00000001183', '0.00000001184')))
    N = 1000000
    G = code['GRID']
    B = code['BINS']
    rt, cn, unit, add, sub, div, mul, conj, advance = (
        code[k] for k in ('root', 'constant', 'unit_phase', 'plus', 'minus',
                          'divide', 'times', 'conjugate', 'forward')
    )
    sq = rt(cn(5))
    u = unit(div(sub(cn(3), sq), 8))
    v = unit(div(add(cn(3), sq), 8))
    base = code['centers']([mul(u, conj(v)), u, mul(u, v), v])
    phase_centers = [(G, 0)] * 4
    survival = [G] * len(rates)
    steps = [int((1 - r) ** 2 * G) for r in rates]
    weighted = [0] * len(rates)
    m1 = positive_m1 = 0
    total = neg = 0
    for j in range(2 * N - 1):
        z = sum((x[0] for x in phase_centers[:3]))
        sign = 1 if z >= 0 else -1
        signed = (N - abs(j - (N - 1))) * sign * min(B, B * abs(z) // (3 * G))
        amp = G + 2 * (phase_centers[1][0] + phase_centers[3][0])
        a = signed * amp ** 2
        total += abs(signed)
        neg += max(-signed, 0)
        # Repeated downward multiplication encloses survival within 2*j grid units.
        for i, s in enumerate(survival):
            weighted[i] += a * s
            survival[i] = s * steps[i] // G
        m1 += a * (2 * j)
        positive_m1 += max(a, 0) * (2 * j)
        phase_centers = [advance(x, b) for x, b in zip(phase_centers, base)]
    if total != 1308791557480504867339:
        raise ValueError('unexpected integer timing weight')
    den = 25 * G ** 2 * total
    last = 2 * N - 2
    T = 2 * last
    error = Q((3 * 260 + 2) * last + 1, G)
    # For rho in [0,1.2e-8], (1-rho)^(t-1)>=1-(t-1)*rho.
    # Thus sum t*w*I*survival/total >= moment - (T-1)*rho*positive_moment.
    intensity_tol = Q(3 * 260 * last, G)
    derivative_floor = (Q(m1, den) - T * intensity_tol
                        - (T - 1) * Q('0.000000012') * (Q(positive_m1, den) + T * intensity_tol))
    if derivative_floor < 1:
        raise ValueError('monotone loss effect unproved')
    res = []
    if error >= Q(1, 10 ** 12):
        raise ValueError('outward decimal bounds too narrow')
    for r, num in zip(rates, weighted):
        p = Q(neg, total) + Q(num, G * den)
        row = dict(per_tick_loss=str(r), signed_success_lower=p * 10 ** 12 // 1 - 1, signed_success_upper=-(-p * 10 ** 12 // 1) + 1)
        for n, h, t in ((57, 38, Q(33, 64)), (61, 40, Q(0))):
            lp = code['decision'](n, p - error, h, t)
            up = code['decision'](n, p + error, h, t)
            row[str(n) + '_power'] = [lp * 10 ** 12 // 1, -(-up * 10 ** 12 // 1)]
        res.append(row)
    if not (res[1]['57_power'][0] > 950000000000 > res[2]['57_power'][1] and res[3]['61_power'][0] > 950000000000 > res[4]['61_power'][1]):
        raise ValueError('power crossing')
    print(json.dumps(dict(rates=res, decrease_in_score_per_unit_loss_at_least=int(derivative_floor), power_grid=10 ** 12), indent=2))

if __name__ == '__main__':
    main()
