"""Re-evaluate the published bank statistics and certify the 62% walk design."""
import json
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCALE = 10**12


def require(condition, message):
    if not condition:
        raise ValueError(message)


def binomial_tail(n, p, k):
    """Sum weights relative to a common denominator by integer recurrence."""
    if k == 0:
        return F(1)
    if k > n:
        return F(0)
    a, d = p.as_integer_ratio()
    b = d - a
    weight = a**n
    total = weight
    for j in range(n, k, -1):
        weight, remainder = divmod(weight*j*b, (n-j+1)*a)
        require(remainder == 0, 'inexact mass recurrence')
        total += weight
    return F(total, d**n)


def rounded(q):
    return [q*SCALE//1, -((-q*SCALE)//1)]


def main():
    # Eqs. (9) and (26) of Sekatski et al., using (none, T only, R only, both).
    for key, expected in enumerate((0, 1, 1, -1)):
        none, t, r, both = (int(i == key) for i in range(4))
        average = F((4*t + none - 1) + (4*r + none - 1), 2)
        require(average == expected, 'bank score mapping')

    # 9x^2 - 4x - 2 = 0 at the twofold-imbalance extremum.
    # At this root the cubic -1+2x+2x^2-3x^3 equals (44x-23)/27.
    cap = F('.359581455')
    for bound, is_upper in ((cap, True), (cap-F(1,10**9), False)):
        x = (27*bound + 23)/44
        require(x > F(2,3) and (9*x*x - 4*x - 2 > 0) == is_upper,
                'bank ceiling bracket')
    table = [(62, '0.561', '0.678'), (52, '0.460', '0.573'), (42, '0.376', '0.465')]
    lower_scores = {eff: (F(t)+F(r))/2-F('.0005') for eff,t,r in table}
    require(all(v > cap for v in lower_scores.values()), 'displayed central values')
    # pi=54/125. At the optical maximum, y^51 = (.49(1-pi)/pi)^49.
    pi, eta = F(54,125), F(31,50)
    lo, hi = F(49,100), F(51,100)
    field = F('.621874655')
    for bound, is_upper in ((field, True), (field-F(1,10**9), False)):
        left = ((bound-pi)/((1-pi)*(1-lo)))**51
        right = (lo*(1-pi)/pi)**49
        require((left > right) == is_upper, 'attenuation ceiling bracket')
    data = json.loads((HERE/'single_port_timing_output.json').read_text())[0]
    require(data['max_ticks'] == 3_999_996, 'wrong sampler')
    q0 = F(data['null_ceiling'])
    q1 = eta*F(data['ideal_floor']) + (1-eta)*(1-F(data['always_click']))
    optical = pi*eta+(1-pi)*(1-hi*eta)
    n, ho, ht = 2500, 1595, 639
    size_o, size_t = binomial_tail(n,field,ho), binomial_tail(n,pi*q0,ht)
    power_o, power_t = binomial_tail(n,optical,ho), binomial_tail(n,pi*q1,ht)
    joint = power_o+power_t-1
    require(max(size_o,size_t) < F(1,20), 'rival size')
    require(joint > F('.97324'), 'combined power')
    prior_pi = F(78,125)
    prior = binomial_tail(158, prior_pi*eta+(1-prior_pi)*(1-hi*eta), 118)
    require(prior < F('.003728'), 'old optical power at g=.51')
    # Sign comparison after raising both nonnegative sides to power 100.
    def separate(e):
        return (1-hi*e)**100 > (1-e)**49
    require(not separate(F('.147910776')) and separate(F('.147910777')),
            'two-setting identifiability boundary')
    print(json.dumps(dict(
        published_central_bank_scores_less_last_digit_rounding={k:str(v) for k,v in lower_scores.items()},
        bank_ceiling_strict_upper=str(cap), preparations=n, full_probability=str(pi),
        detection_efficiency=str(eta), optical_cutoff=ho, full_timing_cutoff=ht,
        optical_size=rounded(size_o), timing_size=rounded(size_t),
        optical_power=rounded(power_o), timing_power=rounded(power_t), joint_lower_bound=rounded(joint),
        old_design_optical_power_at_high_transmission=rounded(prior), probability_grid=SCALE,
        two_setting_boundary=['0.147910776','0.147910777']
    ),indent=2))


if __name__ == '__main__':
    main()
