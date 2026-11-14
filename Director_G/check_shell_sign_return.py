"""Compare an actual signed forward/inverse trajectory with its scalar-shell prediction."""
import argparse
from fractions import Fraction
import json
from pathlib import Path


def require(condition, explanation):
    if not condition:
        raise ValueError(explanation)


def propagate(state, ticks, inverse=False):
    # Array index j labels -t+2j after t ordinary ticks. A reversed shift
    # aligns incoming right and left at the same site before undoing the coin.
    # On reversal the array must grow too: sign errors can escape the
    # original cone, including beyond the forward endpoints.
    for _ in range(ticks):
        if inverse:
            right = [r for r, _ in state] + [0]
            left = [0] + [l for _, l in state]
            state = [(r+l, r-l) for r, l in zip(right, left)]
        else:
            right = [0] + [r+l for r, l in state]
            left = [r-l for r, l in state] + [0]
            state = list(zip(right, left))
    return state


def ratio_bounds(x, scale=10**14):
    lo, rem = divmod(x.numerator * scale, x.denominator)
    return [lo, lo+int(rem != 0)]


def test_mask(ticks, selected, groups, expected):
    denominator = 2**ticks
    returns = []
    for launch in [(1,0), (0,1)]:
        flight = propagate([launch], ticks)
        actual = sum(r*r+l*l for j,(r,l) in enumerate(flight)
                     if abs(2*j-ticks) in selected)
        require(Fraction(actual, denominator)==expected, "wrong direct effect")
        signed = [(-r,-l) if abs(2*j-ticks) in selected else (r,l)
                  for j,(r,l) in enumerate(flight)]
        back = propagate(signed, ticks, inverse=True)
        origin = back[ticks]
        require(origin == tuple((denominator-2*actual)*a for a in launch),
                "actual return column disagrees with reflected amplitude")
        require(sum(r*r+l*l for r,l in back)==denominator**2, "full return norm")
        escape = sum(r*r+l*l for j,(r,l) in enumerate(back) if j!=ticks)
        require(Fraction(escape, denominator**2)==4*expected*(1-expected),
                "escape missed a rail or site")
        returns.append(list(origin))
    return {"tick":ticks, "groups":groups, "mass":str(expected),
            "origin_columns_numerator":returns, "return_amplitude_denominator":str(denominator),
            "escape_mass":str(4*expected*(1-expected))}


def build():
    panels = [test_mask(2, set(), "no intervention", Fraction(0)),
              test_mask(2, {0}, "central well", Fraction(1,2)),
              test_mask(3, {3}, "outer wells", Fraction(1,4))]
    reg=Path(__file__).with_name("results")/"shifted_site_mask.json"
    menu=json.loads(reg.read_bytes())["three_bit_mirrored_shell_bins"]
    require(menu["tick"]==256 and menu["origin_count"]==8, "different mask menu")
    rates=[]
    for start, numerator in enumerate(menu["seed_mass_numerators"]):
        bins=[(start+j)%8 for j in range(5)]
        radii={r for j in bins for r in menu["bin_radii"][j]}
        s=Fraction(int(numerator),int(menu["denominator"]))
        panels.append(test_mask(256,radii,bins,s))
        T=lambda x:4*x*(1-x)
        square=lambda x:x*x/(x*x+(1-x)**2)
        direct=square(s)
        echo=square(T(s))
        transform=T(direct)
        rates.append((T(s),echo,transform,echo-transform))
    means=[sum(col)/8 for col in zip(*rates)]
    return {"sign_echoes":panels, "power_two_at_eight_masks":{
        "scale":10**14, "quantities":["ordinary escape","power-two escape",
                                     "transform of each power-two direct rate","residual"],
        "mean_bounds":[ratio_bounds(x) for x in means],
        "range_bounds":[[ratio_bounds(min(col))[0],ratio_bounds(max(col))[1]]
                        for col in zip(*rates)]}}


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output",type=Path)
    args=parser.parse_args()
    data=build()
    with args.output.open("x",encoding="utf-8",newline="\n") as out:
        json.dump(data,out,indent=2)
        out.write("\n")
