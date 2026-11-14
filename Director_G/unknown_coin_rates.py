"""Exact finite readout predictions for a three-tick walk on the line."""

from fractions import Fraction as F


def require(ok, reason):
    if not ok:
        raise ArithmeticError(reason)


def three_tick_rows():
    """Signed path counts (input R, input L), with common denominator sqrt(8)."""
    rows = {(0, 0): (1, 0), (0, 1): (0, 1)}
    for _ in range(3):
        outgoing = {}
        for (x, rail), row in rows.items():
            for end, shift in ((0, 1), (1, -1)):
                key = (x + shift, end)
                sign = -1 if rail == 1 and end == 1 else 1
                a, b = outgoing.get(key, (0, 0))
                outgoing[key] = (a + sign * row[0], b + sign * row[1])
        rows = outgoing
    require((rows[1, 0], rows[1, 1]) == ((2, 0), (1, 1)), "site +1 signed rows")
    return rows


def square_read(p):
    return p*p / (p*p + (1-p)*(1-p))


def rates(rows, rr, re, im):
    """rho_RL=re+i*im, rho_RR=rr. Both measured analyzer matrices are real."""
    ll = 1 - rr
    require(0 <= rr <= 1 and re*re + im*im <= rr*ll, "invalid coin density")
    masses = {(x, rail): (a*a*rr + 2*a*b*re + b*b*ll)/8
              for (x, rail), (a, b) in rows.items()}
    require(sum(masses.values()) == 1 and min(masses.values()) >= 0, "launch accounting")
    site = sum(w for (x, rail), w in masses.items() if x == 1)
    x_plus, z_plus = (rr + ll + 2*re)/2, rr
    require(site == x_plus/4 + z_plus/2, "independent analyzer identity")
    sq_site, sq_x, sq_z = (square_read(p) for p in (site, x_plus, z_plus))
    sq_fit = sq_x/4 + sq_z/2
    diluted = F(1, 4) + site/2
    source_mix = F(1, 4) + sq_site/2
    analyzer_mix = F(1, 4) + sq_x/8 + sq_z/4
    require(diluted == F(1, 4) + x_plus/8 + z_plus/4, "ordinary mixture agreement")
    require(source_mix - analyzer_mix == (sq_site - sq_fit)/2, "square mixture gap")
    return dict(rho_RR=rr, rho_RL_real=re, rho_RL_imag=im, rho_LL=ll,
                ordinary_site=site, ordinary_X=x_plus, ordinary_Z=z_plus,
                ordinary_coherent_and_assigned_mixes=diluted, square_site=sq_site,
                square_X=sq_x, square_Z=sq_z, square_analyzer_inference=sq_fit,
                square_coherent=square_read(diluted), square_assigned_source=source_mix,
                square_assigned_analyzer=analyzer_mix,
                square_site_minus_analyzer=sq_site-sq_fit)


def rate_controls():
    rows = three_tick_rows()
    half = F(1, 2)
    states = {"R": (F(1), 0, 0), "L": (F(0), 0, 0), "+": (half, half, 0),
              "-": (half, -half, 0), "+i": (half, 0, -half),
              "maximally_mixed": (half, 0, 0),
              "rational_mixed": (F(3, 4), F(1, 8), 0)}
    fixtures = {name: rates(rows, *map(F, rho)) for name, rho in states.items()}
    require([r["ordinary_site"] for r in fixtures.values()] ==
            list(map(F, ("5/8", "1/8", "1/2", "1/4", "3/8", "3/8", "17/32"))),
            "signed-walk site controls")
    require(fixtures["maximally_mixed"]["square_site_minus_analyzer"] == F(-15, 136)
            and fixtures["rational_mixed"]["square_site_minus_analyzer"] == F(-12507, 174760),
            "mixed-state normalized-square witnesses")
    hidden = (fixtures["R"]["square_site"] + fixtures["L"]["square_site"])/2
    require(hidden == F(321, 850) and hidden != square_read(F(3, 8)),
            "per-type read followed by averaging must differ from homogeneous pooling")

    names = ("Ordinary site read", "Normalized-square site read",
             "Inferred from normalized-square X and Z reads")
    series = [dict(name=name, data=[]) for name in names]
    for j in range(-12, 13):
        u = F(j, 12)
        rr = 1/(1 + u*u)
        record = rates(rows, rr, u*rr, 0)
        require(record["ordinary_site"] == (4 + (1+u)**2)*rr/8,
                "normalized pure column gives signed site control")
        for chart, key in zip(series, ("ordinary_site", "square_site",
                                       "square_analyzer_inference")):
            y = str(record[key])
            chart["data"].append([str(u), y, y])
    return dict(
        definition="Each fixture is one homogeneous joint source. The square reader applies "
                   "g(p)=p^2/(p^2+(1-p)^2) to the pooled mass of each binary read. "
                   "Classically assigned arms average those separately read rates. "
                   "All rates are per original launch with sharp dark and bright endpoints.",
        signed_endpoints=[dict(site=x, rail=("R", "L")[rail], input_numerators=list(row))
                          for (x, rail), row in sorted(rows.items())],
        fixtures={s: {k: str(v) for k, v in r.items()} for s, r in fixtures.items()},
        hidden_R_or_L_equal_frequency=dict(
            description="Each launch retains the R or L type and the square reader acts "
                        "within that type before averaging. The reduced coin is I/2.",
            typewise_square_site=str(hidden),
            homogeneous_square_site=str(fixtures["maximally_mixed"]["square_site"])),
        plot=dict(title="Three-step site read for a varying input coin",
                  provenance="model", source="Signed Hadamard walk, site +1, normalized R + u L",
                  x_label="Real input amplitude ratio u", y_label="Rate per original launch",
                  x_domain=[-1, 1], y_domain=[0, 1], series=series))
