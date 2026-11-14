"""Check microscopic powered odds on ballistic velocity shells and an interior window."""
from argparse import ArgumentParser
from fractions import Fraction
import json
from math import isqrt, sqrt
from pathlib import Path

from check_velocity_readout import explicit_line, fold_port, line_step, reflected, velocity_cdf

DIGITS = 10**10
ROOT_SCALE = 2**36


def shell(t, x, n):
    """Exactly test v*-2/n <= x/t < v*-1/n with integer arithmetic."""
    lower = n*x+2*t
    upper = n*x+t
    return lower >= 0 and 2*lower**2 >= (n*t)**2 and (upper < 0 or 2*upper**2 < (n*t)**2)


def power_bounds(value, twice_q):
    if twice_q == 0:
        return (int(value > 0),)*2
    if twice_q % 2 == 0:
        return (value**(twice_q//2),)*2
    root = isqrt(value*ROOT_SCALE**2)
    more = int(root**2 != value*ROOT_SCALE**2)
    multiplier = value**(twice_q//2)
    return multiplier*root, multiplier*(root+more)


def ratio_interval(num, den):
    if den[0] == 0:
        return None
    return [DIGITS*num[0]//den[1], -(-DIGITS*num[1]//den[0])]


def rows(t,r,l):
    xcoords = [2*k-t for k in range(t+1)]
    ordinary = [a*a+b*b for a,b in zip(r,l)]
    assert sum(ordinary) == 2**t
    ref = [i for i,x in enumerate(xcoords) if 0 <= 4*x < t]
    base_limit = velocity_cdf(.25)-velocity_cdf(0)
    cases = []
    for n in [24,48,96,192]:
        cells = [i for i,x in enumerate(xcoords) if shell(t,x,n)]
        theory = (velocity_cdf(sqrt(.5)-1/n)-velocity_cdf(sqrt(.5)-2/n))/base_limit
        observed = {}
        for rule in ('pooled_site','resolved_rails','alternating_split'):
            def scores(i):
                return (r[i]**2,l[i]**2) if (rule=='resolved_rails' or
                     (rule=='alternating_split' and i%2==1)) else (ordinary[i],)
            values = [v for i in cells for v in scores(i)]
            ref_values = [v for i in ref for v in scores(i)]
            ratios = {}
            for twice_q in [0,1,2,3,4]:
                v_bounds = [power_bounds(v,twice_q) for v in values]
                r_bounds = [power_bounds(v,twice_q) for v in ref_values]
                num = [sum(row[j] for row in v_bounds) for j in range(2)]
                den = [sum(row[j] for row in r_bounds) for j in range(2)]
                ratios[str(Fraction(twice_q,2))] = ratio_interval(num,den)
            observed[rule] = ratios
        assert len({tuple(table['1']) for table in observed.values()})==1
        cases.append({'inverse_shell_width':n,'sites_in_shell':len(cells),'sites_in_reference':len(ref),
                  'shell_to_reference_ordinary_limit':theory,'interval_numerators':observed})
    return {'tick':t,'shells':cases}


def reflection_check():
    """A time shorter than length has one occupied-parity lift per physical site."""
    checked = 0
    for t in range(3,60,3):
        length=4*t//3
        source=length//8
        r,l=[1],[0]
        for _ in range(t):
            r,l=line_step(r,l)
        fr,fl=reflected(length,source,t)
        mapped={}
        for k,(a,b) in enumerate(zip(r,l)):
            p,swap=fold_port(source+2*k-t,length)
            assert p not in mapped
            mapped[p]=(b*b,a*a) if swap else (a*a,b*b)
        assert [mapped.get(x,(0,0)) for x in range(length)] == [(a*a,b*b) for a,b in zip(fr,fl)]
        checked += 1
    return checked


def run():
    clocks = (12,24,48,96,192,384,768,1536)
    result = []
    r,l=[1],[0]
    for t in range(max(clocks)+1):
        if t <= 10:
            assert [list(v) for v in zip(r,l)] == explicit_line(t)
        if t in clocks:
            result.append(rows(t,r,l))
        if t < max(clocks):
            r,l=line_step(r,l)
    return {'reference_velocity':'[0,1/4)', 'front_shell':'[sqrt(1/2)-2/n,sqrt(1/2)-1/n)',
            'ratio_interval_denominator':DIGITS, 'root_scale_in_half_integer_powers':ROOT_SCALE,
            'independent_reflection_checks':reflection_check(),'all_flights':result}


if __name__ == '__main__':
    parser=ArgumentParser(description=__doc__)
    parser.add_argument('output',type=Path)
    with parser.parse_args().output.open('x',encoding='utf-8',newline='\n') as dst:
        dst.write(json.dumps(run(),indent=2)+'\n')
