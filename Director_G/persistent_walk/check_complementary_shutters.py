"""Certify fixed-sample optical tests using full, left-only and right-only gates."""
from fractions import Fraction
import json
from math import isqrt

F = Fraction
GRID = 10**64
HALF = F(1, 2)


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sqrt_interval(x):
    low = isqrt(x.numerator*GRID*GRID//x.denominator)
    return F(low, GRID), F(low+1, GRID)


def power_interval(x, n):
    """Exponentiation by squaring with both endpoints rounded out at every product."""
    def product(u, v):
        return (u[0]*v[0]//GRID, (u[1]*v[1]+GRID-1)//GRID)

    scaled = x*GRID
    factor = (scaled//1, -((-scaled)//1))
    result = (GRID, GRID)
    while n:
        if n%2:
            result = product(result, factor)
        factor = product(factor, factor)
        n //= 2
    return F(result[0], GRID), F(result[1], GRID)


def weights(eta, split_floor=F(49, 100)):
    h = split_floor*(1-split_floor)
    b = h*eta/3
    a = b*(HALF+h*eta)
    null = 1+b*h*eta**2/4
    inverse = 1+eta/2*(-a/(1+a)+b/(2*(1-b)))
    return a, b, null, inverse


def affinity(eta):
    """Hellinger affinity to a fixed balanced coherent intensity, directed bounds."""
    q = eta/2
    slo, shi = sqrt_interval(1-eta)
    # At full transmission both models have the same click probability eta.
    left = (sqrt_interval(q*(1-shi))[0], sqrt_interval(q*(1-slo))[1])
    right = (sqrt_interval((1-q)*slo)[0], sqrt_interval((1-q)*shi)[1])
    return (1+left[0]+right[0])/2, (1+left[1]+right[1])/2


def main():
    # Full no-click = u*v for independent Poisson arms with empty probabilities u, v.
    # Disabling either arm at random gives exactly half of full occupancy plus
    # half the counterfactual coincidence probability.
    for u, v in ((F(1,4), F(2,3)), (F(1), F(3,7)), (F(1,2), F(1,2))):
        full = 1-u*v
        selected = 1-(u+v)/2
        require(2*selected-full == (1-u)*(1-v), 'counterfactual coincidence identity')
        if u == 1:
            require(selected == full/2 and full > 0, 'one-arm classical imitation')
    # The field bound A is exactly the maximum of the quadratic relaxation.
    eta = F(1,10)
    a, b, null, _ = weights(eta)
    h = F(49,100)*F(51,100)
    for full in (F(0), eta, F(1)):
        relaxed = 1 + (a-b/2)*full/2 - b*h*full**2/4
        require(null-relaxed == b*h*(full-eta)**2/4, 'uniform field factor')
    rows = []
    cases = (
        ('0.05', 3171029, 18775529),
        ('0.10', 368528, 2393857),
        ('0.15', 101213, 723990),
        ('0.42', 2858, 37334),
        ('0.62', 555, 12927),
        ('0.98', 20, 4149),
    )
    for value, lower, upper in cases:
        eta = F(value)
        a, b, null, inverse = weights(eta)
        require(0 < a < 1 and 0 < b < 1 and null*inverse < 1, 'test weights')
        # Markov for the field product and the ideal reciprocal product.
        require(power_interval(null*inverse, upper)[1] < F(1,400), 'power certificate')
        require(power_interval(null*inverse, upper-1)[0] > F(1,400),
                'first sample satisfying this sufficient certificate')
        lo, hi = affinity(eta)
        require(power_interval(lo, 2*(lower-1))[0] > F(19,100), 'necessary bound')
        require(power_interval(hi, 2*lower)[1] < F(19,100), 'affinity endpoint')
        rows.append(dict(efficiency=value,necessary_at_least=lower,sufficient=upper,
                         full_click_increment=str(a),selected_click_decrement=str(b),
                         null_factor=str(null)))
    print(json.dumps(rows, indent=2))


if __name__ == '__main__':
    main()
